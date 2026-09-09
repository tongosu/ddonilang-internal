#!/usr/bin/env python
from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "pack" / "nurigym_step_record_v02_roundtrip_v1"
CONSUMER_PACK = ROOT / "pack" / "nurigym_step_record_v02_consumer_g6_v1"
BASE_PACK_CHECK = ROOT / "tests" / "run_nurigym_step_record_v02_roundtrip_pack_check.py"

LEGACY_REQUIRED_FIELDS = {
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
V02_ADDITIVE_FIELDS = {
    "raw_action",
    "resolved_action",
    "normalized_action",
    "action_status",
    "merge_candidates",
    "merged_action",
    "applied_action",
    "missing_input",
}
DIAGNOSTIC_SHAPES = {
    "E_STEP_RECORD_REJECTED_IN_MERGE": {"severity": "error", "fatal": True},
    "E_STEP_RECORD_CLIP_NOOP": {"severity": "warning", "fatal": False},
    "E_STEP_RECORD_MISSING_STATUS_MISMATCH": {"severity": "error", "fatal": True},
}


def preferred_build_root() -> Path:
    primary = Path("I:/home/urihanl/ddn/codex/build")
    fallback = Path("C:/ddn/codex/build")
    if primary.exists():
        return primary
    if fallback.exists():
        return fallback
    return ROOT / "build"


BUILD = preferred_build_root() / "nurigym_step_record_v02_roundtrip_v1"
REPORT = BUILD / "nurigym_step_record_v02_roundtrip_check_report.detjson"


def fail(message: str) -> int:
    print(f"nurigym_step_record_v02_roundtrip_check: FAIL: {message}", file=sys.stderr)
    return 1


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid json: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"json root must be object: {path}")
    return data


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError as exc:
        raise ValueError(f"missing file: {path}") from exc
    for idx, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid jsonl: {path}:{idx}: {exc}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"jsonl row must be object: {path}:{idx}")
        rows.append(row)
    return rows


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_command(args: list[str]) -> dict[str, Any]:
    proc = subprocess.run(
        args,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
    )
    return {
        "args": args,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def diagnose(record: dict[str, Any]) -> list[dict[str, Any]]:
    diagnostics: list[dict[str, Any]] = []
    action_status = record.get("action_status")
    raw_action = record.get("raw_action")
    normalized_action = record.get("normalized_action")
    merge_candidates = record.get("merge_candidates")
    missing_input = record.get("missing_input")

    if action_status == "거부" and isinstance(merge_candidates, list) and raw_action in merge_candidates:
        diagnostics.append(
            {
                "code": "E_STEP_RECORD_REJECTED_IN_MERGE",
                "severity": "error",
                "fatal": True,
                "path": "merge_candidates",
            }
        )
    if action_status == "잘림" and raw_action == normalized_action:
        diagnostics.append(
            {
                "code": "E_STEP_RECORD_CLIP_NOOP",
                "severity": "warning",
                "fatal": False,
                "path": "normalized_action",
            }
        )
    if isinstance(missing_input, list) and missing_input and action_status != "가만히":
        diagnostics.append(
            {
                "code": "E_STEP_RECORD_MISSING_STATUS_MISMATCH",
                "severity": "error",
                "fatal": True,
                "path": "missing_input",
            }
        )
    return diagnostics


def validate_diagnostic_contracts(contract: dict[str, Any], cases: dict[str, dict[str, Any]]) -> dict[str, Any]:
    rows = contract.get("diagnostic_contracts")
    if not isinstance(rows, list):
        raise ValueError("contract diagnostic_contracts must be a list")
    by_code = {str(row.get("code")): row for row in rows if isinstance(row, dict)}
    if set(by_code) != set(DIAGNOSTIC_SHAPES):
        raise ValueError(f"diagnostic codes mismatch: {sorted(by_code)}")
    for code, shape in DIAGNOSTIC_SHAPES.items():
        row = by_code[code]
        for key, expected in shape.items():
            if row.get(key) != expected:
                raise ValueError(f"{code}: contract {key} mismatch")
        if not str(row.get("source_ref", "")).endswith(".md:36") and code == "E_STEP_RECORD_REJECTED_IN_MERGE":
            raise ValueError(f"{code}: missing source_ref line")

    probes = {
        "E_STEP_RECORD_REJECTED_IN_MERGE": copy.deepcopy(cases["c04_reject"]["wire_record"]),
        "E_STEP_RECORD_CLIP_NOOP": copy.deepcopy(cases["c03_clip"]["wire_record"]),
        "E_STEP_RECORD_MISSING_STATUS_MISMATCH": copy.deepcopy(cases["c02_noop_missing"]["wire_record"]),
    }
    probes["E_STEP_RECORD_REJECTED_IN_MERGE"]["merge_candidates"] = [
        probes["E_STEP_RECORD_REJECTED_IN_MERGE"]["raw_action"]
    ]
    probes["E_STEP_RECORD_CLIP_NOOP"]["normalized_action"] = probes["E_STEP_RECORD_CLIP_NOOP"]["raw_action"]
    probes["E_STEP_RECORD_MISSING_STATUS_MISMATCH"]["action_status"] = "맞음"

    results: dict[str, Any] = {}
    for code, probe in probes.items():
        diagnostics = diagnose(probe)
        selected = [item for item in diagnostics if item.get("code") == code]
        if len(selected) != 1:
            raise ValueError(f"{code}: diagnostic probe did not emit exactly one matching diagnostic")
        emitted = selected[0]
        for key, expected in DIAGNOSTIC_SHAPES[code].items():
            if emitted.get(key) != expected:
                raise ValueError(f"{code}: emitted {key} mismatch")
        results[code] = emitted

    for case_id, case in cases.items():
        if case.get("format_version") != "v0.2":
            continue
        diagnostics = diagnose(case["wire_record"])
        if diagnostics:
            raise ValueError(f"{case_id}: valid fixture emitted diagnostics {diagnostics}")
    return results


def validate_additive_shape(contract: dict[str, Any], cases: dict[str, dict[str, Any]]) -> dict[str, Any]:
    consumer = load_json(CONSUMER_PACK / "step_record_v02_fixture.detjson")
    legacy_required = set(consumer.get("legacy_v01_required_fields") or [])
    if legacy_required != LEGACY_REQUIRED_FIELDS:
        raise ValueError(f"legacy field set mismatch: {sorted(legacy_required)}")

    field_defs = contract.get("field_definitions")
    if not isinstance(field_defs, list):
        raise ValueError("field_definitions must be a list")
    contract_fields = {str(row.get("name")) for row in field_defs if isinstance(row, dict)}
    if contract_fields != V02_ADDITIVE_FIELDS:
        raise ValueError(f"v0.2 additive field set mismatch: {sorted(contract_fields)}")

    case_results: dict[str, Any] = {}
    for case_id, case in cases.items():
        record = case["wire_record"]
        missing_legacy = sorted(LEGACY_REQUIRED_FIELDS - set(record))
        if missing_legacy:
            raise ValueError(f"{case_id}: missing legacy fields {missing_legacy}")
        if case.get("format_version") == "v0.2":
            missing_v02 = sorted(V02_ADDITIVE_FIELDS - set(record))
            if missing_v02:
                raise ValueError(f"{case_id}: missing v0.2 additive fields {missing_v02}")
            case_results[case_id] = {
                "legacy_fields_present": True,
                "v02_fields_present": True,
            }
        elif case.get("format_version") == "v0.1":
            unknown_v02 = sorted((V02_ADDITIVE_FIELDS - {"applied_action"}) & set(record))
            if unknown_v02:
                raise ValueError(f"{case_id}: v0.1 fixture contains v0.2 fields {unknown_v02}")
            if record.get("applied_action") != case["expected_consumer"].get("applied_action"):
                raise ValueError(f"{case_id}: v0.1 minimal replay applied_action mismatch")
            case_results[case_id] = {
                "legacy_fields_present": True,
                "v01_unknown_field_compatible": True,
            }
        else:
            raise ValueError(f"{case_id}: unsupported format_version")
    return {
        "legacy_required_fields": sorted(LEGACY_REQUIRED_FIELDS),
        "v02_additive_fields": sorted(V02_ADDITIVE_FIELDS),
        "cases": case_results,
    }


def validate_shared_merge_provenance(cases: dict[str, dict[str, Any]]) -> dict[str, Any]:
    case = cases["c05_shared_merge"]
    producer_input = case.get("producer_input")
    record = case.get("wire_record")
    if not isinstance(producer_input, dict) or producer_input.get("mode") != "shared":
        raise ValueError("c05_shared_merge: producer_input must be shared mode")
    agents = producer_input.get("agents")
    if not isinstance(agents, list) or len(agents) != 2:
        raise ValueError("c05_shared_merge: expected two source agents")
    agent_actions = [agent.get("raw_action") for agent in agents if isinstance(agent, dict)]
    if record.get("merge_candidates") != agent_actions:
        raise ValueError("c05_shared_merge: merge_candidates must preserve source agent action order")
    winner = agents[0]
    if record.get("agent_id") != winner.get("agent_id"):
        raise ValueError("c05_shared_merge: winner agent_id provenance mismatch")
    if record.get("merged_action") != winner.get("raw_action"):
        raise ValueError("c05_shared_merge: merged_action provenance mismatch")
    if record.get("applied_action") != record.get("merged_action"):
        raise ValueError("c05_shared_merge: applied_action must equal merged_action")
    return {
        "case_id": "c05_shared_merge",
        "source_agent_ids": [agent["agent_id"] for agent in agents],
        "merge_candidates": record["merge_candidates"],
        "winner_agent_id": record["agent_id"],
        "merged_action": record["merged_action"],
        "provenance_ok": True,
    }


def main() -> int:
    try:
        pack_golden = run_command(["python", "tests/run_pack_golden.py", "nurigym_step_record_v02_roundtrip_v1"])
        if pack_golden["returncode"] != 0:
            return fail(pack_golden["stderr"].strip() or pack_golden["stdout"].strip())

        base_check = run_command(["python", str(BASE_PACK_CHECK.relative_to(ROOT))])
        if base_check["returncode"] != 0:
            return fail(base_check["stderr"].strip() or base_check["stdout"].strip())

        contract = load_json(PACK / "contract.detjson")
        golden_rows = load_jsonl(PACK / "golden.jsonl")
        if len(golden_rows) != 6:
            raise ValueError("golden.jsonl must contain six rows")
        cases = {}
        for rel in contract.get("case_files", []):
            case = load_json(PACK / rel)
            cases[str(case["case_id"])] = case
        expected_cases = {
            "c01_valid",
            "c02_noop_missing",
            "c03_clip",
            "c04_reject",
            "c05_shared_merge",
            "c06_v01_backward_read",
        }
        if set(cases) != expected_cases:
            raise ValueError(f"case set mismatch: {sorted(cases)}")

        if contract.get("runtime_semantics_change") is not False:
            raise ValueError("runtime_semantics_change must remain false")
        if contract.get("state_hash_change") is not False:
            raise ValueError("state_hash_change must remain false")

        additive = validate_additive_shape(contract, cases)
        diagnostics = validate_diagnostic_contracts(contract, cases)
        merge = validate_shared_merge_provenance(cases)
    except ValueError as exc:
        return fail(str(exc))

    boundary_status = subprocess.run(
        ["git", "status", "--short", "--", "docs/ssot", "lang", "core", "tool", "tools/teul-cli/src"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )
    if boundary_status.returncode != 0:
        return fail(boundary_status.stderr.strip())
    if boundary_status.stdout.strip():
        return fail(f"boundary path changed: {boundary_status.stdout.strip()}")

    report = {
        "schema": "ddn.nurigym.step_record.v0.2.roundtrip.check_report.v1",
        "status": "PASS",
        "pack_id": "nurigym_step_record_v02_roundtrip_v1",
        "pack_golden": "PASS",
        "base_pack_check": "PASS",
        "additive_shape": additive,
        "diagnostic_shapes": diagnostics,
        "shared_merge_provenance": merge,
        "runtime_semantics_change": False,
        "state_hash_change": False,
        "boundary_path_status": boundary_status.stdout.strip(),
    }
    write_json(REPORT, report)
    print("nurigym_step_record_v02_roundtrip_check: PASS")
    print(f"report={REPORT.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
