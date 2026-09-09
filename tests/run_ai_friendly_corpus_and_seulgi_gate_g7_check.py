#!/usr/bin/env python
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CORPUS_PACK = ROOT / "pack" / "llm_corpus_extract_deterministic_v1"
GATE_PACK = ROOT / "pack" / "seulgi_ai_gate_no_authority_g7_v1"
EXTRACTOR = ROOT / "tests" / "tools" / "extract_llm_corpus_v1.py"
OUT_DIR = Path("I:/home/urihanl/ddn/codex/out")
OUT_JSONL = OUT_DIR / "llm_corpus_v1.jsonl"
OUT_MANIFEST = OUT_DIR / "llm_corpus_v1.manifest.detjson"

CORPUS_DETERMINISTIC_CHECK_CMD = [sys.executable, "tests/run_llm_corpus_extract_deterministic_check.py"]
CORPUS_DAYRUN_CHECK_CMD = [sys.executable, "tests/run_llm_corpus_v1_dayrun_check.py"]
SEULGI_GATEKEEPER_CHECK_CMD = [sys.executable, "tests/run_seulgi_gatekeeper_pack_check.py"]
REQUIRED_CORPUS_KINDS = {"grammar_card", "ssot_term", "diagnostic_card", "pack_summary", "example"}


def preferred_build_root() -> Path:
    primary = Path("I:/home/urihanl/ddn/codex/build")
    fallback = Path("C:/ddn/codex/build")
    if primary.exists():
        return primary
    if fallback.exists():
        return fallback
    return ROOT / "build"


BUILD = preferred_build_root() / "ai_friendly_corpus_and_seulgi_gate_g7"
REPORT = BUILD / "ai_friendly_corpus_and_seulgi_gate_g7_check_report.detjson"


def fail(message: str) -> int:
    print(f"ai_friendly_corpus_and_seulgi_gate_g7_check: FAIL: {message}", file=sys.stderr)
    return 1


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        row = json.loads(line)
        if not isinstance(row, dict):
            raise ValueError(f"{path}:{line_no}: row must be object")
        rows.append(row)
    return rows


def sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def run(args: list[str], *, timeout: int = 180) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def run_extract(jsonl: Path, manifest: Path) -> subprocess.CompletedProcess[str]:
    return run(
        [
            sys.executable,
            str(EXTRACTOR),
            "--limit",
            "120",
            "--jsonl-out",
            str(jsonl),
            "--manifest-out",
            str(manifest),
        ],
        timeout=180,
    )


def validate_corpus() -> dict[str, Any]:
    if not EXTRACTOR.exists():
        raise ValueError(f"missing extractor: {EXTRACTOR.relative_to(ROOT).as_posix()}")
    with tempfile.TemporaryDirectory(prefix="ai_friendly_corpus_g7_") as temp_dir:
        temp = Path(temp_dir)
        a_jsonl = temp / "a.jsonl"
        a_manifest = temp / "a.manifest.detjson"
        b_jsonl = temp / "b.jsonl"
        b_manifest = temp / "b.manifest.detjson"
        for jsonl, manifest in [(a_jsonl, a_manifest), (b_jsonl, b_manifest)]:
            proc = run_extract(jsonl, manifest)
            if proc.returncode != 0:
                raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "corpus extract failed")
        if a_jsonl.read_bytes() != b_jsonl.read_bytes():
            raise ValueError("corpus extract is not byte-identical across two runs")
        rows = load_jsonl(a_jsonl)
        manifest = load_json(a_manifest)
        temp_sha256 = sha256_file(a_jsonl)

    kinds = sorted({str(row.get("kind", "")) for row in rows})
    missing_kinds = sorted(REQUIRED_CORPUS_KINDS - set(kinds))
    if missing_kinds:
        raise ValueError(f"missing corpus kinds: {missing_kinds}")
    if len(rows) < 100:
        raise ValueError(f"row_count below 100: {len(rows)}")
    for idx, row in enumerate(rows, 1):
        if row.get("schema") != "ddn.llm_corpus.row.v1":
            raise ValueError(f"row schema mismatch at {idx}")
        if row.get("row_index") != idx:
            raise ValueError(f"row index mismatch at {idx}")
        if not str(row.get("row_hash", "")).startswith("sha256:"):
            raise ValueError(f"row hash missing at {idx}")

    return {
        "row_count": len(rows),
        "kinds": kinds,
        "kind_counts": manifest.get("kind_counts"),
        "temp_sha256": temp_sha256,
    }


def validate_gate_fixture() -> dict[str, Any]:
    contract = load_json(GATE_PACK / "contract.detjson")
    if contract.get("closure_grade") != "닫힘-문서":
        raise ValueError("gate contract must remain 닫힘-문서")
    for key in [
        "natural_language_direct_execution",
        "ai_proposal_has_authority_before_gate",
        "parser_frontdoor_change",
        "runtime_semantics_change",
        "state_hash_change",
    ]:
        if contract.get(key) is not False:
            raise ValueError(f"gate contract {key} must be false")
    if contract.get("gate_required") is not True:
        raise ValueError("gate_required must be true")
    if contract.get("sealed_artifact_required_for_authority") is not True:
        raise ValueError("sealed_artifact_required_for_authority must be true")
    for rel_path in contract.get("linked_existing_evidence", []):
        if not (ROOT / rel_path).exists():
            raise ValueError(f"missing linked evidence: {rel_path}")

    fixture = load_json(GATE_PACK / "gate_fixture.detjson")
    cases = fixture.get("cases")
    if not isinstance(cases, list) or len(cases) < 3:
        raise ValueError("gate fixture must include at least three cases")
    decisions = {str(case.get("gate_decision", {}).get("decision", "")) for case in cases if isinstance(case, dict)}
    if decisions != {"accept", "reject"}:
        raise ValueError(f"gate fixture decisions mismatch: {sorted(decisions)}")
    for case in cases:
        if case.get("natural_language_direct_execution") is not False:
            raise ValueError(f"{case.get('id')}: natural language execution must remain false")
        proposal = case.get("ai_proposal")
        if not isinstance(proposal, dict) or proposal.get("authority") != "none":
            raise ValueError(f"{case.get('id')}: AI proposal authority must be none")
        if case.get("authority_before_seal") != "none":
            raise ValueError(f"{case.get('id')}: authority_before_seal must be none")
        artifact = case.get("sealed_artifact")
        decision = case.get("gate_decision", {}).get("decision")
        if decision == "reject" and artifact is not None:
            raise ValueError(f"{case.get('id')}: reject must not produce sealed artifact")
        if decision == "accept":
            if not isinstance(artifact, dict) or artifact.get("sealed") is not True:
                raise ValueError(f"{case.get('id')}: accept must carry sealed artifact in this fixture")
            if case.get("authority_after_seal") != "sealed_artifact_only":
                raise ValueError(f"{case.get('id')}: authority_after_seal mismatch")
    return {
        "case_count": len(cases),
        "decisions": sorted(decisions),
        "sealed_artifact_cases": sum(1 for case in cases if isinstance(case.get("sealed_artifact"), dict)),
    }


def main() -> int:
    BUILD.mkdir(parents=True, exist_ok=True)
    for path in [
        CORPUS_PACK / "contract.detjson",
        GATE_PACK / "README.md",
        GATE_PACK / "contract.detjson",
        GATE_PACK / "gate_fixture.detjson",
    ]:
        if not path.exists():
            return fail(f"missing required file: {path.relative_to(ROOT).as_posix()}")

    for cmd in [CORPUS_DETERMINISTIC_CHECK_CMD, CORPUS_DAYRUN_CHECK_CMD, SEULGI_GATEKEEPER_CHECK_CMD]:
        proc = run(cmd, timeout=240)
        if proc.returncode != 0:
            return fail(proc.stderr.strip() or proc.stdout.strip() or f"command failed: {cmd}")

    try:
        corpus_summary = validate_corpus()
        gate_summary = validate_gate_fixture()
    except (ValueError, RuntimeError, json.JSONDecodeError) as exc:
        return fail(str(exc))

    if not OUT_JSONL.exists() or not OUT_MANIFEST.exists():
        return fail("dayrun corpus output missing")
    out_rows = load_jsonl(OUT_JSONL)
    out_manifest = load_json(OUT_MANIFEST)
    if out_manifest.get("row_count") != len(out_rows):
        return fail("out manifest row_count mismatch")
    out_kinds = {str(row.get("kind", "")) for row in out_rows}
    if not REQUIRED_CORPUS_KINDS.issubset(out_kinds):
        return fail(f"out corpus missing kinds: {sorted(REQUIRED_CORPUS_KINDS - out_kinds)}")

    product_status = run(["git", "status", "--short", "--", "lang", "core", "tool", "tools/teul-cli/src"], timeout=30)
    if product_status.returncode != 0:
        return fail(product_status.stderr.strip())
    if product_status.stdout.strip():
        return fail(f"product path changed: {product_status.stdout.strip()}")

    report = {
        "schema": "ddn.ai_friendly_corpus_and_seulgi_gate_g7.check_report.v1",
        "status": "PASS",
        "closure_grade": "닫힘-문서",
        "corpus": {
            **corpus_summary,
            "out_jsonl": OUT_JSONL.as_posix(),
            "out_manifest": OUT_MANIFEST.as_posix(),
            "out_sha256": sha256_file(OUT_JSONL),
        },
        "seulgi_gate": gate_summary,
        "commands": {
            "deterministic_check": CORPUS_DETERMINISTIC_CHECK_CMD,
            "dayrun_check": CORPUS_DAYRUN_CHECK_CMD,
            "existing_gatekeeper_check": SEULGI_GATEKEEPER_CHECK_CMD,
        },
        "natural_language_direct_execution": False,
        "product_path_status": product_status.stdout.strip(),
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("ai_friendly_corpus_and_seulgi_gate_g7_check: PASS")
    print(f"report={REPORT.as_posix()}")
    print(f"corpus={OUT_JSONL.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
