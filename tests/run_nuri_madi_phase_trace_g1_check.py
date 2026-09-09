#!/usr/bin/env python
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "pack" / "nuri_madi_phase_trace_g1_v1"


def preferred_build_root() -> Path:
    primary = Path("I:/home/urihanl/ddn/codex/build")
    fallback = Path("C:/ddn/codex/build")
    if primary.exists():
        return primary
    if fallback.exists():
        return fallback
    return ROOT / "build"


BUILD = preferred_build_root() / "nuri_madi_phase_trace_g1"
REPORT = BUILD / "nuri_madi_phase_trace_g1_check_report.detjson"


def fail(message: str) -> int:
    print(f"nuri_madi_phase_trace_g1_check: FAIL: {message}", file=sys.stderr)
    return 1


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run(args: list[str], *, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def main() -> int:
    BUILD.mkdir(parents=True, exist_ok=True)
    if not PACK.exists():
        return fail(f"missing pack: {PACK}")

    contract = load_json(PACK / "contract.detjson")
    if contract.get("evidence_tier") != "pack_skeleton":
        return fail("contract must remain pack_skeleton")
    if contract.get("closure_grade") != "닫힘-문서":
        return fail("contract must be docs-closed only")
    for key in ["behavior_closure_claim", "product_runtime_path_verified", "parser_frontdoor_change", "runtime_semantics_change", "state_hash_change"]:
        if contract.get(key) is not False:
            return fail(f"{key} must be false")
    if (PACK / "golden.jsonl").exists():
        return fail("golden.jsonl must not exist for this skeleton pack")

    required = contract.get("required_fixtures", [])
    for name in required:
        if not (PACK / name).exists():
            return fail(f"missing fixture {name}")

    phase = load_json(PACK / "phase_trace.detjson")
    expected_phases = contract["required_phases"]
    actual_phases = [row.get("phase") for row in phase.get("trace", [])]
    if actual_phases != expected_phases:
        return fail(f"phase order mismatch: {actual_phases}")
    commit_phases = [row["phase"] for row in phase["trace"] if row.get("shared_world_commit") is True]
    if commit_phases != ["P6"]:
        return fail(f"shared commit phase mismatch: {commit_phases}")

    action = load_json(PACK / "action_record.detjson")
    records = action.get("records", [])
    statuses = {row.get("action_status") for row in records}
    if statuses != set(contract["required_action_statuses"]):
        return fail(f"action status set mismatch: {statuses}")
    for row in records:
        for key in ["raw_action", "merged_action", "applied_action", "action_status"]:
            if key not in row:
                return fail(f"record {row.get('case_id')} missing {key}")
    rejected = [row for row in records if row.get("action_status") == "거부"]
    if not rejected or any(row.get("merge_candidate") is not False for row in rejected):
        return fail("rejected action must be excluded before merge")

    conflict = load_json(PACK / "write_conflict_fatal.detjson")
    expected = conflict.get("expected", {})
    if expected.get("error_code") != "E_MADI_WRITE_CONFLICT":
        return fail(f"write conflict error code mismatch: {expected}")
    if expected.get("fatal") is not True or expected.get("world_commit_allowed") is not False:
        return fail(f"write conflict fatal boundary mismatch: {expected}")
    if len(conflict.get("conflict", {}).get("writers", [])) < 2:
        return fail("write conflict fixture needs at least two writers")

    existing_contract = load_json(ROOT / "pack" / "nurigym_shared_sync_action_pipeline_v1" / "contract.detjson")
    existing_statuses = set(existing_contract.get("required_statuses", []))
    if existing_statuses != set(contract["required_action_statuses"]):
        return fail(f"linked action status evidence mismatch: {existing_statuses}")
    nuri_gym_src = (ROOT / "tools" / "teul-cli" / "src" / "cli" / "nurigym.rs").read_text(encoding="utf-8")
    for status in contract["required_action_statuses"]:
        if status not in nuri_gym_src:
            return fail(f"tools/teul-cli src missing action status {status}")

    product_status = run(["git", "status", "--short", "--", "lang", "core", "tool", "tools/teul-cli/src"], timeout=30)
    if product_status.returncode != 0:
        return fail(product_status.stderr.strip())
    if product_status.stdout.strip():
        return fail(f"product path changed: {product_status.stdout.strip()}")

    report = {
        "schema": "ddn.nuri_madi_phase_trace_g1.check_report.v1",
        "status": "PASS",
        "closure_grade": "닫힘-문서",
        "pack": PACK.relative_to(ROOT).as_posix(),
        "phase_order": actual_phases,
        "action_statuses": sorted(statuses),
        "write_conflict_error": expected.get("error_code"),
        "linked_existing_action_status_pack": "pack/nurigym_shared_sync_action_pipeline_v1",
        "behavior_closure_claim": False,
        "product_path_status": product_status.stdout.strip(),
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("nuri_madi_phase_trace_g1_check: PASS")
    print(f"report={REPORT.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
