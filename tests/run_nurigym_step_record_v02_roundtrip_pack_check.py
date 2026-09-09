#!/usr/bin/env python
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "pack" / "nurigym_step_record_v02_roundtrip_v1"
CONSUMER_PACK = ROOT / "pack" / "nurigym_step_record_v02_consumer_g6_v1"
SHARED_SYNC_PACK = ROOT / "pack" / "nurigym_shared_sync_action_pipeline_v1"
STATUS_VALUES = {"맞음", "가만히", "잘림", "거부"}
V02_REQUIRED_FIELDS = {
    "raw_action",
    "resolved_action",
    "normalized_action",
    "action_status",
    "merge_candidates",
    "merged_action",
    "applied_action",
    "missing_input",
}
V01_ABSENT_FIELDS = {
    "raw_action",
    "resolved_action",
    "normalized_action",
    "action_status",
    "merge_candidates",
    "merged_action",
    "missing_input",
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
REPORT = BUILD / "nurigym_step_record_v02_roundtrip_pack_check_report.detjson"


def fail(message: str) -> int:
    print(f"nurigym_step_record_v02_roundtrip_pack_check: FAIL: {message}", file=sys.stderr)
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


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def infer_type(field: str, value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return "action_value"
    if isinstance(value, str):
        return "slot_path" if field == "missing_input" else "string"
    if isinstance(value, list):
        if field == "missing_input" and all(isinstance(item, str) for item in value):
            return "array<slot_path>"
        if all((isinstance(item, (int, float)) and not isinstance(item, bool)) for item in value):
            return "array<action_value>"
        return "array<mixed>"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def assert_type_compatible(case_id: str, field: str, value: Any, field_types: dict[str, str]) -> None:
    expected = field_types[field]
    observed = infer_type(field, value)
    if expected == "action_value|null" and observed in {"action_value", "null"}:
        return
    if expected == "array<action_value>" and observed == "array<action_value>":
        return
    if expected == "array<slot_path>" and observed == "array<slot_path>":
        return
    if expected == "enum(맞음,가만히,잘림,거부)|미상" and isinstance(value, str) and value in STATUS_VALUES | {"미상"}:
        return
    if expected == "action_value" and observed == "action_value":
        return
    raise ValueError(f"{case_id}: field type mismatch {field}: observed={observed} expected={expected}")


def sample_type_compatible(declared: str, observed: str, compat_types: set[str]) -> bool:
    if observed == "null":
        return True
    if observed in compat_types:
        return True
    if declared == "action_value|null" and observed == "action_value":
        return True
    if declared == "enum(맞음,가만히,잘림,거부)|미상" and observed == "string":
        return True
    return False


def project_consumer_view(record: dict[str, Any], format_version: str) -> dict[str, Any]:
    if format_version == "v0.1":
        for field in V01_ABSENT_FIELDS:
            if field in record:
                raise ValueError(f"v0.1 fixture must not contain v0.2 additive field: {field}")
        if "applied_action" not in record:
            raise ValueError("v0.1 fixture needs applied_action for minimal replay")
        return {
            "raw_action": None,
            "normalized_action": None,
            "action_status": "미상",
            "merged_action": None,
            "applied_action": record["applied_action"],
            "missing_input": [],
            "minimal_replay": True,
        }

    missing = sorted(V02_REQUIRED_FIELDS - set(record))
    if missing:
        raise ValueError(f"v0.2 fixture missing fields: {missing}")
    return {
        "raw_action": record.get("raw_action"),
        "normalized_action": record.get("normalized_action"),
        "action_status": record.get("action_status"),
        "merged_action": record.get("merged_action"),
        "applied_action": record.get("applied_action"),
        "missing_input": record.get("missing_input"),
        "minimal_replay": False,
    }


def validate_case(case: dict[str, Any], golden: dict[str, Any], field_types: dict[str, str]) -> dict[str, Any]:
    case_id = str(case.get("case_id", ""))
    if not case_id:
        raise ValueError("case_id missing")
    format_version = str(case.get("format_version", ""))
    if format_version not in {"v0.1", "v0.2"}:
        raise ValueError(f"{case_id}: invalid format_version {format_version}")
    if golden.get("case_id") != case_id:
        raise ValueError(f"{case_id}: golden case mismatch {golden.get('case_id')}")
    if golden.get("format_version") != format_version:
        raise ValueError(f"{case_id}: golden format mismatch")

    record = case.get("wire_record")
    if not isinstance(record, dict):
        raise ValueError(f"{case_id}: wire_record must be object")
    encoded = canonical_json(record)
    decoded = json.loads(encoded)
    if decoded != record:
        raise ValueError(f"{case_id}: JSON roundtrip changed wire record")

    view = project_consumer_view(decoded, format_version)
    expected = case.get("expected_consumer")
    if not isinstance(expected, dict):
        raise ValueError(f"{case_id}: expected_consumer must be object")
    for key, value in view.items():
        if expected.get(key) != value:
            raise ValueError(f"{case_id}: consumer view mismatch for {key}: {value!r} != {expected.get(key)!r}")

    if view["action_status"] != golden["expected_status"]:
        raise ValueError(f"{case_id}: status mismatch")
    if view["applied_action"] != golden["expected_applied_action"]:
        raise ValueError(f"{case_id}: applied action mismatch")
    if len(view["missing_input"]) != int(golden["expected_missing_input_count"]):
        raise ValueError(f"{case_id}: missing_input count mismatch")
    if bool(view["minimal_replay"]) != bool(golden["minimal_replay"]):
        raise ValueError(f"{case_id}: minimal_replay mismatch")

    for field in V02_REQUIRED_FIELDS & set(record):
        assert_type_compatible(case_id, field, record[field], field_types)
    if format_version == "v0.1":
        assert_type_compatible(case_id, "applied_action", record["applied_action"], field_types)

    if case_id == "c01_valid":
        if canonical_json(record["raw_action"]) != canonical_json(record["applied_action"]):
            raise ValueError("c01_valid: raw_action and applied_action must be byte-equal")
    elif case_id == "c02_noop_missing":
        if view["action_status"] != "가만히" or len(view["missing_input"]) != 1:
            raise ValueError("c02_noop_missing: expected one missing slot path")
    elif case_id == "c03_clip":
        if record["normalized_action"] == record["raw_action"]:
            raise ValueError("c03_clip: E_STEP_RECORD_CLIP_NOOP would fire")
        if record["applied_action"] != record["normalized_action"]:
            raise ValueError("c03_clip: applied_action must equal normalized_action")
    elif case_id == "c04_reject":
        rejected = record["raw_action"]
        if rejected in record.get("merge_candidates", []):
            raise ValueError("c04_reject: rejected raw action appears in merge_candidates")
    elif case_id == "c05_shared_merge":
        if len(record.get("merge_candidates", [])) != int(golden.get("expected_merge_candidate_count")):
            raise ValueError("c05_shared_merge: merge candidate count mismatch")
        if record["merged_action"] != record["applied_action"]:
            raise ValueError("c05_shared_merge: merged_action must equal applied_action")
    elif case_id == "c06_v01_backward_read":
        absent = set(expected.get("absent_v02_fields", []))
        if not absent.issubset(V01_ABSENT_FIELDS):
            raise ValueError("c06_v01_backward_read: invalid absent field expectation")

    return {
        "case_id": case_id,
        "format_version": format_version,
        "status": "PASS",
        "wire_record_sha256_input": encoded,
        "consumer_view": view,
    }


def crosscheck_fields(contract: dict[str, Any]) -> dict[str, Any]:
    consumer_fixture = load_json(CONSUMER_PACK / "step_record_v02_fixture.detjson")
    shared_contract = load_json(SHARED_SYNC_PACK / "contract.detjson")
    field_defs = contract.get("field_definitions")
    if not isinstance(field_defs, list) or not field_defs:
        raise ValueError("contract field_definitions missing")
    roundtrip_fields = {str(row.get("name")) for row in field_defs if isinstance(row, dict)}
    if "" in roundtrip_fields:
        raise ValueError("contract field name missing")

    consumer_fields = set(consumer_fixture.get("v02_additive_field_candidates") or [])
    shared_fields = set(shared_contract.get("required_pipeline_fields") or [])
    missing_from_consumer = sorted(roundtrip_fields - consumer_fields)
    missing_from_shared = sorted(shared_fields - roundtrip_fields)
    if missing_from_consumer:
        raise ValueError(f"field names missing from consumer pack: {missing_from_consumer}")
    if missing_from_shared:
        raise ValueError(f"shared sync fields missing from roundtrip contract: {missing_from_shared}")

    shared_statuses = set(shared_contract.get("required_statuses") or [])
    if shared_statuses != STATUS_VALUES:
        raise ValueError(f"shared sync status mismatch: {sorted(shared_statuses)}")
    if set(contract.get("required_statuses") or []) != STATUS_VALUES:
        raise ValueError("roundtrip contract required_statuses mismatch")

    field_types = {str(row["name"]): str(row["type"]) for row in field_defs if isinstance(row, dict)}
    if sorted(field_types) != sorted(roundtrip_fields):
        raise ValueError("field type definitions incomplete")

    sample_compat: dict[str, list[str]] = {}
    for record in consumer_fixture.get("records", []):
        if not isinstance(record, dict):
            continue
        for field in sorted(roundtrip_fields & set(record)):
            sample_compat.setdefault(field, [])
            observed = infer_type(field, record[field])
            if observed not in sample_compat[field]:
                sample_compat[field].append(observed)
    for field, observed_types in sample_compat.items():
        declared = field_types[field]
        compat_types = {declared}
        for row in field_defs:
            if isinstance(row, dict) and row.get("name") == field:
                compat_types.update(str(item) for item in row.get("consumer_sample_compat_types", []))
        for observed in observed_types:
            if not sample_type_compatible(declared, observed, compat_types):
                raise ValueError(f"consumer sample type incompatible: {field}: {observed} not in {sorted(compat_types)}")

    return {
        "consumer_pack": str(CONSUMER_PACK.relative_to(ROOT)).replace("\\", "/"),
        "shared_sync_pack": str(SHARED_SYNC_PACK.relative_to(ROOT)).replace("\\", "/"),
        "field_name_count": len(roundtrip_fields),
        "field_names_match_consumer_candidates": True,
        "field_names_match_shared_sync_required_fields": True,
        "status_enum_match_shared_sync": True,
        "roundtrip_type_definitions_complete": True,
        "consumer_sample_types_observed": {key: sorted(value) for key, value in sorted(sample_compat.items())},
    }


def main() -> int:
    required_files = [
        PACK / "README.md",
        PACK / "contract.detjson",
        PACK / "golden.jsonl",
    ]
    missing = [str(path.relative_to(ROOT)).replace("\\", "/") for path in required_files if not path.exists()]
    if missing:
        return fail(f"missing pack files: {missing}")

    try:
        contract = load_json(PACK / "contract.detjson")
        if contract.get("evidence_tier") != "runner_golden":
            raise ValueError("contract evidence_tier must be runner_golden")
        if contract.get("closure_claim") != "no":
            raise ValueError("contract closure_claim must be no")
        for key in ["parser_frontdoor_change", "runtime_semantics_change", "state_hash_change", "gymnasium_compatible_consumer_claim"]:
            if contract.get(key) is not False:
                raise ValueError(f"contract {key} must be false")
        if int(contract.get("new_language_syntax_count", -1)) != 0:
            raise ValueError("new_language_syntax_count must be 0")

        field_types = {
            str(row["name"]): str(row["type"])
            for row in contract["field_definitions"]
            if isinstance(row, dict)
        }
        case_files = [PACK / rel for rel in contract.get("case_files", [])]
        if len(case_files) != 6:
            raise ValueError("contract must list exactly 6 case files")
        for path in case_files:
            if not path.exists():
                raise ValueError(f"missing case file: {path}")
        golden_rows = load_jsonl(PACK / "golden.jsonl")
        if len(golden_rows) != 6:
            raise ValueError("golden.jsonl must contain exactly 6 rows")
        golden_by_id = {str(row.get("case_id")): row for row in golden_rows}
        if len(golden_by_id) != 6:
            raise ValueError("golden case ids must be unique")

        case_results = []
        for path in case_files:
            case = load_json(path)
            case_id = str(case.get("case_id"))
            if case_id not in golden_by_id:
                raise ValueError(f"missing golden row for {case_id}")
            case_results.append(validate_case(case, golden_by_id[case_id], field_types))

        crosscheck = crosscheck_fields(contract)
    except ValueError as exc:
        return fail(str(exc))

    product_status = subprocess.run(
        ["git", "status", "--short", "--", "docs/ssot", "lang", "core", "tool", "tools/teul-cli/src"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )
    if product_status.returncode != 0:
        return fail(product_status.stderr.strip())
    if product_status.stdout.strip():
        return fail(f"boundary path changed: {product_status.stdout.strip()}")

    report = {
        "schema": "ddn.nurigym.step_record.v0.2.roundtrip_pack.check_report.v1",
        "status": "PASS",
        "pack_id": contract["pack_id"],
        "evidence_tier": contract["evidence_tier"],
        "closure_claim": contract["closure_claim"],
        "case_count": len(case_results),
        "cases": case_results,
        "field_crosscheck": crosscheck,
        "boundary_path_status": product_status.stdout.strip(),
    }
    write_json(REPORT, report)

    print("nurigym_step_record_v02_roundtrip_pack_check: PASS")
    print(f"cases={len(case_results)}")
    print("field_crosscheck=PASS")
    print(f"report={REPORT.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
