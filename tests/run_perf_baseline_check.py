#!/usr/bin/env python
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "tools" / "scripts" / "run_perf_baseline_v1.py"
BUILD = Path("I:/home/urihanl/ddn/codex/build/perf_baseline_v1")
REPORT = BUILD / "perf_baseline_report.detjson"
BASELINE = BUILD / "perf_baseline_generated_baseline.detjson"
GATE_REPORT = BUILD / "perf_baseline_gate_report.detjson"


def fail(message: str) -> int:
    print(f"perf_baseline_check: FAIL: {message}", file=sys.stderr)
    return 1


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def compare_to_generated_baseline(report: dict, baseline: dict) -> dict[str, object]:
    gate = baseline.get("regression_gate", {})
    allowed_ratio = float(gate.get("allowed_worse_ratio", 0.20))
    baseline_cases = {
        str(case.get("id")): case
        for case in baseline.get("cases", [])
        if isinstance(case, dict)
    }
    rows: list[dict[str, object]] = []
    for case in report.get("cases", []):
        if not isinstance(case, dict):
            continue
        case_id = str(case.get("id", ""))
        base = baseline_cases.get(case_id, {})
        base_summary = base.get("baseline_summary", {}) if isinstance(base, dict) else {}
        current_summary = case.get("summary", {})
        baseline_ms = base_summary.get("median_wall_clock_ms") if isinstance(base_summary, dict) else None
        current_ms = current_summary.get("median_wall_clock_ms") if isinstance(current_summary, dict) else None
        status = "not_compared"
        ratio = None
        if isinstance(baseline_ms, int) and baseline_ms > 0 and isinstance(current_ms, int):
            ratio = round(current_ms / baseline_ms, 4)
            status = "pass" if ratio <= 1.0 + allowed_ratio else "fail"
        rows.append(
            {
                "id": case_id,
                "baseline_median_wall_clock_ms": baseline_ms,
                "current_median_wall_clock_ms": current_ms,
                "ratio": ratio,
                "status": status,
            }
        )
    return {
        "schema": "ddn.perf_baseline.generated_gate_result.v1",
        "allowed_worse_ratio": allowed_ratio,
        "rows": rows,
        "ok": all(row["status"] == "pass" for row in rows),
    }


def main() -> int:
    if not RUNNER.exists():
        return fail(f"missing runner: {RUNNER.relative_to(ROOT).as_posix()}")

    BUILD.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            "--repeat",
            "2",
            "--json-out",
            str(REPORT),
            "--baseline-out",
            str(BASELINE),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=180,
    )
    if proc.returncode != 0:
        return fail(proc.stderr.strip() or proc.stdout.strip() or "runner failed")

    report = load_json(REPORT)
    baseline = load_json(BASELINE)
    if report.get("schema") != "ddn.perf_baseline.report.v1":
        return fail(f"report schema mismatch: {report.get('schema')}")
    if baseline.get("schema") != "ddn.perf_baseline.baseline.v1":
        return fail(f"baseline schema mismatch: {baseline.get('schema')}")
    if baseline.get("status") != "local_measured_baseline":
        return fail(f"baseline status mismatch: {baseline.get('status')}")

    axes = report.get("axes")
    expected_axes = ["tick_throughput", "wasm_load_first_frame", "gym_rollout_step_per_sec"]
    if axes != expected_axes:
        return fail(f"axis mismatch: {axes}")

    cases = report.get("cases")
    if not isinstance(cases, list) or len(cases) != 3:
        return fail("report must contain exactly 3 measured cases")

    for case in cases:
        if not isinstance(case, dict):
            return fail("case row must be an object")
        if case.get("ok") is not True:
            return fail(f"case failed: {case.get('id')}")
        summary = case.get("summary", {})
        if not isinstance(summary, dict):
            return fail(f"summary missing: {case.get('id')}")
        if summary.get("run_count") != 2:
            return fail(f"case must run twice: {case.get('id')}")
        hashes = summary.get("result_sha256_set")
        if not isinstance(hashes, list) or len(hashes) != 1:
            return fail(f"result bytes not bit-identical across 2 runs: {case.get('id')} {hashes}")
        if summary.get("result_bit_identical_within_repeat") is not True:
            return fail(f"result repeat flag false: {case.get('id')}")

    fallback = [
        case
        for case in cases
        if isinstance(case, dict) and case.get("axis") == "wasm_load_first_frame"
    ][0]
    if fallback.get("source_kind") != "cli_startup_fallback":
        return fail("wasm_load_first_frame axis must record CLI startup fallback source_kind")
    if "unavailable" not in str(fallback.get("note", "")):
        return fail("fallback case must record why real WASM first-frame is unavailable")

    gate_report = compare_to_generated_baseline(report, baseline)
    write_json(GATE_REPORT, gate_report)
    if gate_report.get("ok") is not True:
        return fail(f"generated baseline gate failed: {gate_report}")

    print("perf_baseline_check: PASS")
    print(f"report={REPORT.as_posix()}")
    print(f"baseline={BASELINE.as_posix()}")
    print(f"gate_report={GATE_REPORT.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
