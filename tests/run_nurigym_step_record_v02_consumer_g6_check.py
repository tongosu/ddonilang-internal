#!/usr/bin/env python
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "pack" / "nurigym_step_record_v02_consumer_g6_v1"
sys.path.insert(0, str(ROOT / "tests" / "tools"))
import config_digest_proto  # noqa: E402

REQUIRED_STATUS = {"맞음", "가만히", "잘림", "거부"}
SHARED_SYNC_CHECK_CMD = [sys.executable, "tests/run_nurigym_shared_sync_action_pipeline_pack_check.py"]
PERF_CHECK_CMD = [sys.executable, "tests/run_perf_baseline_check.py"]


def preferred_build_root() -> Path:
    primary = Path("I:/home/urihanl/ddn/codex/build")
    fallback = Path("C:/ddn/codex/build")
    if primary.exists():
        return primary
    if fallback.exists():
        return fallback
    return ROOT / "build"


BUILD = preferred_build_root() / "nurigym_step_record_v02_consumer_g6"
REPORT = BUILD / "nurigym_step_record_v02_consumer_g6_check_report.detjson"


def fail(message: str) -> int:
    print(f"nurigym_step_record_v02_consumer_g6_check: FAIL: {message}", file=sys.stderr)
    return 1


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run(args: list[str], *, timeout: int = 240) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def materialize_hashes(fixture: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, str]]:
    payload = config_digest_proto.canonical_payload(str(fixture["settings_source"]))
    hashes = config_digest_proto.hash_report(payload)["hashes"]
    records: list[dict[str, Any]] = []
    for record in fixture["records"]:
        row = dict(record)
        if row.get("run_config_hash") == "computed_by_checker":
            row["run_config_hash"] = hashes["run_config_hash"]
        if row.get("settings_hash") == "computed_by_checker":
            row["settings_hash"] = hashes["settings_hash"]
        records.append(row)
    return records, hashes


def legacy_v01_reader(record: dict[str, Any], required_fields: list[str]) -> dict[str, Any]:
    missing = [field for field in required_fields if field not in record]
    if missing:
        raise ValueError(f"legacy field missing: {record.get('id')} {missing}")
    if record.get("schema") != "nurigym.step.v1":
        raise ValueError(f"legacy schema mismatch: {record.get('id')} {record.get('schema')}")
    return {field: record[field] for field in required_fields}


def assert_roundtrip_stable(payload: dict[str, Any]) -> None:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    decoded = json.loads(encoded)
    if decoded != payload:
        raise ValueError("legacy roundtrip changed payload")


def validate_v02_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    statuses = Counter()
    for record in records:
        for field in ["raw_action", "normalized_action", "action_status", "merged_action", "applied_action", "run_config_hash", "settings_hash"]:
            if field not in record:
                raise ValueError(f"{record.get('id')}: missing v0.2 field {field}")
        status = str(record["action_status"])
        statuses[status] += 1
        for hash_field in ["run_config_hash", "settings_hash"]:
            value = str(record[hash_field])
            if not value.startswith("blake3:") or len(value) != len("blake3:") + 64:
                raise ValueError(f"{record.get('id')}: invalid {hash_field}: {value}")
        if status == "거부" and record.get("merge_candidates") != []:
            raise ValueError("reject record must be excluded from merge candidates")
        if status == "잘림" and not record.get("merge_candidates"):
            raise ValueError("clip record must remain merge-candidate after normalization")
    missing_status = sorted(REQUIRED_STATUS - set(statuses))
    if missing_status:
        raise ValueError(f"missing action_status rows: {missing_status}")
    return {"action_status_counts": dict(sorted(statuses.items()))}


def consume_vectorized_rollout(records: list[dict[str, Any]], vector_fixture: dict[str, Any]) -> dict[str, Any]:
    by_id = {str(record["id"]): record for record in records}
    slots = []
    total_steps = 0
    status_counts: Counter[str] = Counter()
    for slot in vector_fixture["env_slots"]:
        slot_records = [by_id[str(record_id)] for record_id in slot["record_ids"]]
        slot_records = sorted(slot_records, key=lambda row: (int(row["madi"]), int(row["agent_id"]), str(row["id"])))
        total_steps += len(slot_records)
        status_counts.update(str(row["action_status"]) for row in slot_records)
        slots.append(
            {
                "env_slot": slot["env_slot"],
                "env_id": slot["env_id"],
                "seed_stream": slot["seed_stream"],
                "step_count": len(slot_records),
                "record_ids": [row["id"] for row in slot_records],
                "last_madi": slot_records[-1]["madi"] if slot_records else None,
            }
        )
    return {
        "schema": "ddn.nurigym.vectorized_consumer.prototype_summary.v1",
        "consumer_layer_api_only": True,
        "env_count": len(slots),
        "total_steps": total_steps,
        "slots": slots,
        "action_status_counts": dict(sorted(status_counts.items())),
    }


def check_perf_connection(vector_fixture: dict[str, Any]) -> tuple[dict[str, Any], subprocess.CompletedProcess[str]]:
    proc = run(PERF_CHECK_CMD, timeout=300)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "perf baseline check failed")
    report_path = preferred_build_root() / "perf_baseline_v1" / "perf_baseline_report.detjson"
    report = load_json(report_path)
    connection = vector_fixture["perf_baseline_connection"]
    expected_axis = connection["axis"]
    expected_case = connection["case_id"]
    cases = {
        str(case.get("id")): case
        for case in report.get("cases", [])
        if isinstance(case, dict)
    }
    case = cases.get(expected_case)
    if not case:
        raise ValueError(f"perf case missing: {expected_case}")
    if case.get("axis") != expected_axis:
        raise ValueError(f"perf axis mismatch: {case.get('axis')} != {expected_axis}")
    if case.get("ok") is not True:
        raise ValueError(f"perf case not ok: {expected_case}")
    return case, proc


def main() -> int:
    BUILD.mkdir(parents=True, exist_ok=True)
    for name in ["README.md", "contract.detjson", "step_record_v02_fixture.detjson", "vectorized_rollout_fixture.detjson"]:
        if not (PACK / name).exists():
            return fail(f"missing pack file: {name}")

    contract = load_json(PACK / "contract.detjson")
    if contract.get("closure_grade") != "닫힘-문서":
        return fail("contract must remain 닫힘-문서")
    for key in [
        "public_schema_required_field_change",
        "parser_frontdoor_change",
        "runtime_semantics_change",
        "state_hash_change",
        "gymnasium_compatible_consumer_claim",
    ]:
        if contract.get(key) is not False:
            return fail(f"contract {key} must be false")
    for rel_path in contract.get("linked_existing_evidence", []):
        if not (ROOT / rel_path).exists():
            return fail(f"missing linked evidence: {rel_path}")

    shared_proc = run(SHARED_SYNC_CHECK_CMD, timeout=300)
    if shared_proc.returncode != 0:
        return fail(shared_proc.stderr.strip() or shared_proc.stdout.strip() or "shared sync checker failed")

    fixture = load_json(PACK / "step_record_v02_fixture.detjson")
    vector_fixture = load_json(PACK / "vectorized_rollout_fixture.detjson")
    if vector_fixture.get("consumer_layer_api_only") is not True or vector_fixture.get("language_surface_change") is not False:
        return fail("vectorized fixture must stay consumer-layer only")

    try:
        materialized_records, hashes = materialize_hashes(fixture)
        v02_summary = validate_v02_records(materialized_records)
        legacy_rows = [legacy_v01_reader(record, fixture["legacy_v01_required_fields"]) for record in materialized_records]
        for row in legacy_rows:
            assert_roundtrip_stable(row)
        vector_summary = consume_vectorized_rollout(materialized_records, vector_fixture)
        perf_case, perf_proc = check_perf_connection(vector_fixture)
    except (ValueError, RuntimeError, config_digest_proto.ConfigDigestError) as exc:
        return fail(str(exc))

    records_path = BUILD / "step_record_v02_materialized.jsonl"
    records_path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in materialized_records),
        encoding="utf-8",
    )
    legacy_path = BUILD / "legacy_v01_roundtrip.detjson"
    write_json(
        legacy_path,
        {
            "schema": "ddn.nurigym.legacy_v01_roundtrip.v1",
            "record_count": len(legacy_rows),
            "unknown_additive_fields_ignored": True,
            "rows": legacy_rows,
        },
    )
    vector_path = BUILD / "vectorized_consumer_summary.detjson"
    write_json(vector_path, vector_summary)

    product_status = run(["git", "status", "--short", "--", "lang", "core", "tool", "tools/teul-cli/src"], timeout=30)
    if product_status.returncode != 0:
        return fail(product_status.stderr.strip())
    if product_status.stdout.strip():
        return fail(f"product path changed: {product_status.stdout.strip()}")

    report = {
        "schema": "ddn.nurigym_step_record_v02_consumer_g6.check_report.v1",
        "status": "PASS",
        "closure_grade": "닫힘-문서",
        "shared_sync_action_pipeline_check": {
            "command": SHARED_SYNC_CHECK_CMD,
            "passed": True,
            "stdout": shared_proc.stdout.strip(),
        },
        "step_record_v02_fixture": {
            "records": len(materialized_records),
            "materialized_records": records_path.as_posix(),
            "hashes": hashes,
            **v02_summary,
        },
        "legacy_v01_roundtrip": {
            "passed": True,
            "unknown_additive_fields_ignored": True,
            "roundtrip_report": legacy_path.as_posix(),
        },
        "vectorized_consumer_prototype": {
            "passed": True,
            "summary": vector_path.as_posix(),
            **vector_summary,
        },
        "perf_baseline_connection": {
            "command": PERF_CHECK_CMD,
            "passed": True,
            "stdout": perf_proc.stdout.strip(),
            "axis": perf_case.get("axis"),
            "case_id": perf_case.get("id"),
            "source_kind": perf_case.get("source_kind"),
            "summary": perf_case.get("summary"),
        },
        "product_path_status": product_status.stdout.strip(),
        "parser_frontdoor_change": False,
        "runtime_semantics_change": False,
        "state_hash_change": False,
        "gymnasium_compatible_consumer_claim": False,
    }
    write_json(REPORT, report)
    print("nurigym_step_record_v02_consumer_g6_check: PASS")
    print(f"report={REPORT.as_posix()}")
    print(f"records={records_path.as_posix()}")
    print(f"vector_summary={vector_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
