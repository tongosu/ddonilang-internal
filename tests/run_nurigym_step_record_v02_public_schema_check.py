#!/usr/bin/env python
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from _teul_cli_freshness import build_teul_cli_cmd as shared_build_teul_cli_cmd


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "pack" / "nurigym_step_record_v02_public_schema_v1"

LEGACY_FIELDS = {
    "schema",
    "episode_id",
    "agent_id",
    "madi",
    "observation",
    "action",
    "reward",
    "next_observation",
    "done",
}
V02_FIELDS = {
    "step_record_version",
    "terminated",
    "truncated",
    "info",
    "raw_action",
    "resolved_action",
    "normalized_action",
    "action_status",
    "merge_candidates",
    "merged_action",
    "applied_action",
    "missing_input",
}


def fail(message: str) -> None:
    print(f"nurigym_step_record_v02_public_schema_check: FAIL: {message}", file=sys.stderr)
    sys.exit(1)


def preferred_build_root() -> Path:
    for candidate in (
        Path("I:/home/urihanl/ddn/codex/build"),
        Path("C:/ddn/codex/build"),
        ROOT / "build",
    ):
        try:
            candidate.mkdir(parents=True, exist_ok=True)
            return candidate
        except OSError:
            continue
    fail("could not create build root")
    raise AssertionError("unreachable")


def teul_cli_candidates() -> list[Path]:
    suffix = ".exe" if os.name == "nt" else ""
    return [
        Path(f"I:/home/urihanl/ddn/codex/target/debug/teul-cli{suffix}"),
        Path(f"C:/ddn/codex/target/debug/teul-cli{suffix}"),
        ROOT / "target" / "debug" / f"teul-cli{suffix}",
    ]


def build_teul_cli_cmd(args: list[str]) -> list[str]:
    return shared_build_teul_cli_cmd(
        ROOT,
        args,
        candidates=teul_cli_candidates(),
        include_which=False,
        manifest_path=ROOT / "tools" / "teul-cli" / "Cargo.toml",
    )


def run(cmd: list[str], *, timeout: int = 180) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"invalid JSONL row {path}:{idx}: {exc}")
        if not isinstance(row, dict):
            fail(f"JSONL row must be object: {path}:{idx}")
        rows.append(row)
    return rows


def run_case(case_name: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    out_dir = preferred_build_root() / "nurigym_step_record_v02_public_schema_v1" / case_name
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = build_teul_cli_cmd(
        [
            "nurigym",
            "run",
            str((PACK / "cases" / case_name).as_posix()),
            "--out",
            str(out_dir.as_posix()),
        ]
    )
    proc = run(cmd, timeout=240)
    if proc.returncode != 0:
        fail(f"{case_name} run failed:\n{proc.stdout}")
    rows = read_jsonl(out_dir / "nurigym.dataset.jsonl")
    if len(rows) < 2:
        fail(f"{case_name} dataset must contain header and at least one step")
    return rows[0], rows[1:]


def check_pack_golden() -> None:
    proc = run([sys.executable, "tests/run_pack_golden.py", "nurigym_step_record_v02_public_schema_v1"])
    if proc.returncode != 0:
        fail(f"pack golden failed:\n{proc.stdout}")


def check_contract() -> None:
    contract = read_json(PACK / "contract.detjson")
    if contract.get("opt_in_only") is not True:
        fail("contract opt_in_only must be true")
    if contract.get("default_version") != "v0.1" or contract.get("public_version") != "v0.2":
        fail("contract version policy mismatch")
    if contract.get("parser_frontdoor_change") is not False:
        fail("parser_frontdoor_change must be false")
    if contract.get("runtime_state_hash_formula_change") is not False:
        fail("runtime_state_hash_formula_change must be false")
    if set(contract.get("legacy_fields_preserved") or []) != LEGACY_FIELDS:
        fail("legacy field contract mismatch")
    if set(contract.get("v02_additive_fields") or []) != V02_FIELDS:
        fail("v0.2 additive field contract mismatch")
    for case_file in contract.get("case_files") or []:
        if not (PACK / case_file).exists():
            fail(f"missing contract case file: {case_file}")


def check_v02_row(case_name: str, row: dict[str, Any]) -> None:
    missing_legacy = sorted(LEGACY_FIELDS - set(row))
    missing_v02 = sorted(V02_FIELDS - set(row))
    if missing_legacy:
        fail(f"{case_name}: missing legacy fields {missing_legacy}")
    if missing_v02:
        fail(f"{case_name}: missing v0.2 fields {missing_v02}")
    if row.get("schema") != "nurigym.step.v1":
        fail(f"{case_name}: legacy schema changed")
    if row.get("step_record_version") != "v0.2":
        fail(f"{case_name}: step_record_version mismatch")
    if row.get("done") != bool(row.get("terminated") or row.get("truncated")):
        fail(f"{case_name}: done invariant mismatch")
    info = row.get("info")
    if not isinstance(info, dict) or info.get("schema") != "nurigym.step_info.v1":
        fail(f"{case_name}: info shape mismatch")
    expected_reason = "terminated" if row.get("terminated") else "truncated" if row.get("truncated") else "none"
    if info.get("done_reason") != expected_reason:
        fail(f"{case_name}: done_reason mismatch")
    if not isinstance(row.get("merge_candidates"), list):
        fail(f"{case_name}: merge_candidates must be array")
    if not isinstance(row.get("missing_input"), list):
        fail(f"{case_name}: v0.2 missing_input must be array")


def check_v02_cases() -> None:
    header, rows = run_case("c01_v02_gridmaze_terminated.json")
    if header.get("step_record_version") != "v0.2":
        fail("c01 header must record v0.2")
    for row in rows:
        check_v02_row("c01", row)
    if not any(row.get("done") and row.get("terminated") is True and row.get("truncated") is False for row in rows):
        fail("c01 must contain natural terminated row")

    _, rows = run_case("c02_v02_gridmaze_truncated.json")
    for row in rows:
        check_v02_row("c02", row)
    if not any(row.get("done") and row.get("terminated") is False and row.get("truncated") is True for row in rows):
        fail("c02 must contain truncated row")

    _, rows = run_case("c03_v02_shared_clip_missing.json")
    for row in rows:
        check_v02_row("c03", row)
    clipped = [row for row in rows if row.get("action_status") == "잘림"]
    if not clipped:
        fail("c03 must include clipped action rows")
    if not any(row.get("raw_action") != row.get("normalized_action") for row in clipped):
        fail("c03 clipped rows must show normalization")
    missing = [row for row in rows if row.get("missing_input")]
    if not missing:
        fail("c03 must include missing_input array row")
    if not all(isinstance(item, str) and item for row in missing for item in row["missing_input"]):
        fail("c03 missing_input entries must be non-empty strings")


def check_default_v01_unchanged() -> None:
    header, rows = run_case("c04_v01_default_unchanged.json")
    if "step_record_version" in header:
        fail("default v0.1 header must omit step_record_version")
    for row in rows:
        missing_legacy = sorted(LEGACY_FIELDS - set(row))
        if missing_legacy:
            fail(f"default v0.1 row missing legacy fields {missing_legacy}")
        unexpected = sorted(V02_FIELDS & set(row))
        if unexpected:
            fail(f"default v0.1 row must omit v0.2 fields: {unexpected}")


def check_boundaries() -> None:
    proc = run(["git", "status", "--short", "--", "docs/ssot"], timeout=60)
    if proc.returncode != 0:
        fail(f"git status docs/ssot failed:\n{proc.stdout}")
    if proc.stdout.strip():
        fail(f"docs/ssot changed:\n{proc.stdout}")


def main() -> None:
    check_pack_golden()
    check_contract()
    check_v02_cases()
    check_default_v01_unchanged()
    check_boundaries()
    print("nurigym_step_record_v02_public_schema_check: PASS")


if __name__ == "__main__":
    main()
