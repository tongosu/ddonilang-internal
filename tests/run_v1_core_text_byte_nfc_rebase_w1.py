#!/usr/bin/env python
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import unicodedata
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACK = ROOT / "pack" / "v1_core_text_byte_nfc_rebase_w1"
WASM_RUNNER = ROOT / "tests" / "run_v1_core_text_byte_nfc_wasm_parity_w1.mjs"
FRESHNESS_RUNNER = ROOT / "tests" / "run_ddn_cli_wasm_freshness_check.py"
TARGET_DIR = Path(os.environ.get(
    "DDN_VC06_CARGO_TARGET_DIR",
    r"I:\home\urihanl\ddn\codex\build\vc06_evidence_target",
))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="strict")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stable_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def run(command: list[str], *, env: dict[str, str] | None = None, timeout: int = 600) -> subprocess.CompletedProcess[str]:
    merged = os.environ.copy()
    if env:
        merged.update(env)
    return subprocess.run(
        command,
        cwd=ROOT,
        env=merged,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def require_ok(proc: subprocess.CompletedProcess[str], label: str) -> str:
    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip()
        raise RuntimeError(f"{label} failed exit={proc.returncode}: {detail}")
    return proc.stdout.strip()


def tracked_git_blob(path: Path) -> tuple[str, bytes]:
    try:
        relative = path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError as error:
        raise RuntimeError(f"E_PACK_PATH_OUTSIDE_REPOSITORY:{path}") from error
    proc = subprocess.run(
        ["git", "show", f"HEAD:{relative}"],
        cwd=ROOT,
        capture_output=True,
        timeout=30,
    )
    if proc.returncode != 0:
        detail = proc.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"E_GIT_BLOB_UNAVAILABLE:{relative}:{detail}")
    return relative, proc.stdout


def verify_lf_materialization(path: Path, checkout_raw: bytes) -> dict[str, str]:
    relative, git_blob_raw = tracked_git_blob(path)
    attr = run(["git", "check-attr", "eol", "--", relative], timeout=30)
    attr_text = require_ok(attr, f"materialization attribute {relative}")
    if not attr_text.endswith(": eol: lf"):
        raise RuntimeError(f"E_MATERIALIZATION_ATTR_NOT_LF:{relative}:{attr_text}")

    git_blob_sha256 = sha256(git_blob_raw)
    checkout_sha256 = sha256(checkout_raw)
    if b"\r\n" in checkout_raw:
        raise RuntimeError(
            "E_CHECKOUT_MATERIALIZATION_CRLF:"
            f"{relative}:git_blob_sha256={git_blob_sha256}:"
            f"checkout_sha256={checkout_sha256}"
        )
    if b"\r" in checkout_raw:
        raise RuntimeError(
            "E_CHECKOUT_MATERIALIZATION_NON_LF:"
            f"{relative}:git_blob_sha256={git_blob_sha256}:"
            f"checkout_sha256={checkout_sha256}"
        )
    if checkout_raw != git_blob_raw:
        raise RuntimeError(
            "E_CHECKOUT_MATERIALIZATION_MISMATCH:"
            f"{relative}:git_blob_sha256={git_blob_sha256}:"
            f"checkout_sha256={checkout_sha256}"
        )
    return {
        "path": relative,
        "git_blob_sha256": git_blob_sha256,
        "checkout_raw_sha256": checkout_sha256,
    }


def load_manifest(pack: Path) -> tuple[Path, bytes, dict[str, Any], dict[str, Any]]:
    manifest_path = pack / "manifest.detjson"
    if not manifest_path.is_file():
        raise RuntimeError(f"E_MANIFEST_MISSING:{manifest_path}")
    raw = manifest_path.read_bytes()
    identities = [verify_lf_materialization(manifest_path, raw)]
    manifest = json.loads(raw.decode("utf-8"))
    cases = manifest.get("cases", [])
    required = int(manifest.get("required_case_count", -1))
    if len(cases) != required:
        raise RuntimeError(f"E_CASE_OMISSION:{len(cases)}/{required}")
    ids = [str(row.get("id", "")) for row in cases]
    if len(ids) != len(set(ids)) or any(not value for value in ids):
        raise RuntimeError("E_CASE_ID_BIJECTION")
    for row in cases:
        fixture = pack / str(row["path"])
        if not fixture.is_file():
            raise RuntimeError(f"E_FIXTURE_MISSING:{row['id']}")
        fixture_raw = fixture.read_bytes()
        identity = verify_lf_materialization(fixture, fixture_raw)
        identities.append(identity)
        if identity["git_blob_sha256"] != row.get("fixture_sha256"):
            raise RuntimeError(
                "E_GIT_BLOB_MANIFEST_IDENTITY_MISMATCH:"
                f"{row['id']}:{identity['git_blob_sha256']}"
            )
    materialization = {
        "declared_eol": "lf",
        "git_blob_identities": [
            {"path": row["path"], "sha256": row["git_blob_sha256"]}
            for row in identities
        ],
        "checkout_raw_identities": [
            {"path": row["path"], "sha256": row["checkout_raw_sha256"]}
            for row in identities
        ],
        "checkout_matches_git_blob": True,
    }
    return manifest_path, raw, manifest, materialization


def native_probe(pack: Path, manifest_path: Path) -> dict[str, Any]:
    probe_manifest = pack / "native_probe" / "Cargo.toml"
    proc = run(
        [
            "cargo", "run", "-q",
            "--manifest-path", str(probe_manifest),
            "--", str(manifest_path),
        ],
        env={
            "CARGO_BUILD_JOBS": "1",
            "CARGO_TARGET_DIR": str(TARGET_DIR / "native_probe"),
        },
    )
    text = require_ok(proc, "native probe")
    return json.loads(text.splitlines()[-1])


def wasm_probe(pack: Path) -> dict[str, Any]:
    proc = run(
        ["node", str(WASM_RUNNER)],
        env={"DDN_VC06_PACK_OVERRIDE": str(pack)},
        timeout=180,
    )
    return json.loads(require_ok(proc, "tracked WASM probe"))


def compare_case(native: dict[str, Any], wasm: dict[str, Any]) -> None:
    case_id = native.get("id")
    if case_id != wasm.get("id"):
        raise RuntimeError(f"E_NATIVE_WASM_CASE_ORDER:{case_id}/{wasm.get('id')}")
    for key in ("fixture_sha256", "source_sha256", "run"):
        if native.get(key) != wasm.get(key):
            raise RuntimeError(f"E_NATIVE_WASM_EXACT_MISMATCH:{case_id}:{key}")
    native_canon = native.get("canon")
    wasm_canon = wasm.get("canon")
    if (native_canon is None) != (wasm_canon is None):
        raise RuntimeError(f"E_NATIVE_WASM_CANON_PRESENCE:{case_id}")
    if native_canon is not None:
        for key in (
            "first_outcome", "first_ddn", "second_outcome", "second_ddn", "roundtrip_equal",
        ):
            if native_canon.get(key) != wasm_canon.get(key):
                raise RuntimeError(f"E_NATIVE_WASM_CANON_MISMATCH:{case_id}:{key}")
    native_runtime = native.get("runtime_canon_reparse")
    wasm_runtime = wasm.get("runtime_canon_reparse")
    if (native_runtime is None) != (wasm_runtime is None):
        raise RuntimeError(f"E_NATIVE_WASM_RUNTIME_CANON_PRESENCE:{case_id}")
    if native_runtime is not None:
        for key in ("canonical_ddn_sha256", "canonical_ddn", "reparse", "reparse_green"):
            if native_runtime.get(key) != wasm_runtime.get(key):
                raise RuntimeError(f"E_NATIVE_WASM_RUNTIME_CANON_MISMATCH:{case_id}:{key}")


def case_matrix(manifest: dict[str, Any], cases: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    by_id = {row["id"]: row for row in cases}
    matrix: list[dict[str, Any]] = []
    totals = {"GREEN": 0, "RED": 0, "PRODUCT_GAP": 0}
    for expected in manifest["cases"]:
        case_id = expected["id"]
        actual = by_id[case_id]
        run_row = actual["run"]
        output = run_row.get("payload", {}).get("output_log_texts")
        diagnostic = run_row.get("diagnostic", {}).get("code")
        expected_class = expected["expected_class"]
        if expected_class == "GREEN":
            if run_row.get("outcome") != "ACCEPTED":
                raise RuntimeError(f"E_EXPECTED_GREEN_REJECTED:{case_id}:{diagnostic}")
            if output != expected.get("expected_output_log_texts"):
                raise RuntimeError(f"E_EXPECTED_OUTPUT_MISMATCH:{case_id}")
        else:
            if run_row.get("outcome") != expected.get("expected_outcome"):
                raise RuntimeError(f"E_GAP_OUTCOME_DRIFT:{case_id}:{run_row.get('outcome')}")
            if diagnostic != expected.get("expected_diagnostic"):
                raise RuntimeError(f"E_GAP_DIAGNOSTIC_DRIFT:{case_id}:{diagnostic}")

        canon = actual.get("canon")
        runtime_reparse = actual.get("runtime_canon_reparse")
        canon_red = bool(expected.get("canon_roundtrip")) and (
            not canon
            or not canon.get("roundtrip_equal")
            or not runtime_reparse
            or not runtime_reparse.get("reparse_green")
        )
        classification = "RED" if canon_red else expected_class
        totals[classification] += 1
        matrix.append({
            "id": case_id,
            "classification": classification,
            "execution_outcome": run_row.get("outcome"),
            "diagnostic": diagnostic,
            "output_log_texts": output,
            "fixture_sha256": actual.get("fixture_sha256"),
            "source_sha256": actual.get("source_sha256"),
            "payload_sha256": sha256(stable_bytes(run_row)),
            "canon_first_outcome": canon.get("first_outcome") if canon else None,
            "canon_first_error_sha256": sha256(str(canon.get("first_error", "")).encode("utf-8")) if canon and canon.get("first_error") else None,
            "canon_second_outcome": canon.get("second_outcome") if canon else None,
            "canon_roundtrip_equal": canon.get("roundtrip_equal") if canon else None,
            "runtime_canon_reparse_green": runtime_reparse.get("reparse_green") if runtime_reparse else None,
            "runtime_canonical_ddn_sha256": runtime_reparse.get("canonical_ddn_sha256") if runtime_reparse else None,
        })
    if sum(totals.values()) != manifest["required_case_count"]:
        raise RuntimeError("E_CLASSIFICATION_BIJECTION")
    nfd = by_id["T04_RAW_TEXT_NFD_NFC"]["run"]["payload"]["output_log_texts"]
    if len(nfd) != 2 or nfd[0] == nfd[1] or unicodedata.normalize("NFC", nfd[0]) != nfd[1]:
        raise RuntimeError("E_RAW_TEXT_NFD_NFC_CONTRACT")
    transport_ids = [
        by_id[value]["source_sha256"]
        for value in ("T05_DIRECT_LF", "T06_DIRECT_CRLF", "T07_DIRECT_LONE_CR")
    ]
    if len(set(transport_ids)) != 3:
        raise RuntimeError("E_TRANSPORT_IDENTITY_COLLAPSE")
    return matrix, totals


def aux_checks(skip: bool) -> dict[str, Any]:
    if skip:
        return {"freshness": "SKIPPED", "local_project_crlf_unit": "SKIPPED"}
    freshness = run([sys.executable, str(FRESHNESS_RUNNER)], timeout=300)
    require_ok(freshness, "tracked WASM freshness")
    local = run(
        [
            "cargo", "test", "-q", "-p", "ddonirang-tool",
            "canonicalizes_disk_crlf_without_changing_lf_or_lone_cr",
            "--", "--nocapture",
        ],
        env={
            "CARGO_BUILD_JOBS": "1",
            "CARGO_TARGET_DIR": str(TARGET_DIR / "workspace_tests"),
        },
        timeout=600,
    )
    require_ok(local, "local-project CRLF unit")
    return {"freshness": "PASS", "local_project_crlf_unit": "PASS"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pack", type=Path, default=DEFAULT_PACK)
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--require-closure", action="store_true")
    parser.add_argument("--skip-aux", action="store_true")
    args = parser.parse_args()

    pack = args.pack.resolve()
    manifest_path, manifest_raw, manifest, materialization = load_manifest(pack)
    if args.validate_only:
        print(
            "VC06_MATERIALIZATION_VALID "
            f"cases={manifest['required_case_count']} files={len(materialization['git_blob_identities'])} "
            f"manifest_sha256={sha256(manifest_raw)} declared_eol=lf"
        )
        return 0

    repeats = int(manifest["deterministic_repeats"])
    native_reports = [native_probe(pack, manifest_path) for _ in range(repeats)]
    wasm_reports = [wasm_probe(pack) for _ in range(repeats)]
    native_digests = [sha256(stable_bytes(row["cases"])) for row in native_reports]
    wasm_digests = [sha256(stable_bytes(row["cases"])) for row in wasm_reports]
    if len(set(native_digests)) != 1 or len(set(wasm_digests)) != 1:
        raise RuntimeError("E_REPEAT_NONDETERMINISM")

    native_cases = native_reports[0]["cases"]
    wasm_cases = wasm_reports[0]["cases"]
    if len(native_cases) != len(wasm_cases) or len(native_cases) != manifest["required_case_count"]:
        raise RuntimeError("E_NATIVE_WASM_CASE_COUNT")
    for native, wasm in zip(native_cases, wasm_cases, strict=True):
        compare_case(native, wasm)

    # compare_case above performs value-level exact equality.  Keep one
    # projection digest after that check: JSON number spelling can differ
    # between Rust (for example 1.0) and JavaScript (1) without a value drift.
    run_payload_exact_digest = sha256(stable_bytes([row["run"] for row in native_cases]))

    matrix, totals = case_matrix(manifest, native_cases)
    aux = aux_checks(args.skip_aux)
    receipt = {
        "schema": "ddn.vc06.text_byte_nfc_evidence_gap_receipt.v1",
        "fixed_product_baseline": manifest["fixed_product_baseline"],
        "manifest_sha256": sha256(manifest_raw),
        "materialization": materialization,
        "source_profile_identity": manifest["source_profile_identity"],
        "case_count": manifest["required_case_count"],
        "case_matrix": matrix,
        "totals": totals,
        "native_wasm_run_payload_exact_cases": len(native_cases),
        "native_wasm_run_payload_exact_digest": run_payload_exact_digest,
        "native_repeat_digests": native_digests,
        "wasm_repeat_digests": wasm_digests,
        "deterministic_repeats": repeats,
        "tracked_wasm_sha256": wasm_reports[0]["tracked_wasm_sha256"],
        "tracked_wasm_manifest_sha256": wasm_reports[0]["tracked_wasm_manifest_sha256"],
        "aux_checks": aux,
        "static_gap_rows": manifest["static_gap_rows"],
        "stable_public_diagnostic_selected": False,
    }
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    if args.require_closure and (totals["RED"] or totals["PRODUCT_GAP"]):
        print(
            f"VC06_CLOSURE_RED red={totals['RED']} product_gap={totals['PRODUCT_GAP']}",
            file=sys.stderr,
        )
        return 1
    print(
        "VC06_GAP_CAPTURE_PASS "
        f"green={totals['GREEN']} red={totals['RED']} product_gap={totals['PRODUCT_GAP']} "
        f"native_wasm_exact={len(native_cases)} repeats={repeats}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
