#!/usr/bin/env python
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASELINE = ROOT / "pack" / "perf_baseline_v1" / "baseline.detjson"
TEUL = ["cargo", "run", "-q", "--manifest-path", "tools/teul-cli/Cargo.toml", "--"]


CASES: list[dict[str, object]] = [
    {
        "id": "tick_throughput_grid_proxy_v1",
        "axis": "tick_throughput",
        "source_kind": "existing_runtime_proxy",
        "deterministic_input": "pack/benchmark_baseline_v1/c02_seamgrim_local_run.ddn",
        "cmd": TEUL + ["run", "pack/benchmark_baseline_v1/c02_seamgrim_local_run.ddn"],
        "throughput_kind": "madi_per_sec",
        "count_hint": 601,
        "note": "G1 proxy until fixed grid100 actor100 scenario lands.",
    },
    {
        "id": "wasm_load_cli_startup_fallback_v1",
        "axis": "wasm_load_first_frame",
        "source_kind": "cli_startup_fallback",
        "deterministic_input": "tools/teul-cli/Cargo.toml",
        "cmd": TEUL + ["--help"],
        "throughput_kind": None,
        "count_hint": None,
        "note": "Real browser WASM first-frame measurement is unavailable in this local dayrun path; CLI startup fallback is recorded instead.",
    },
    {
        "id": "nurigym_rollout_short_proxy_v1",
        "axis": "gym_rollout_step_per_sec",
        "source_kind": "existing_nurigym_proxy",
        "deterministic_input": "pack/benchmark_baseline_v1/input.nurigym.json",
        "cmd": TEUL + [
            "nurigym",
            "run",
            "pack/benchmark_baseline_v1/input.nurigym.json",
            "--out",
            "{tmp}/nurigym_out",
        ],
        "throughput_kind": "step_per_sec",
        "count_hint": 2,
        "note": "Short deterministic rollout proxy; large rollout is a later baseline run.",
    },
]


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def decode_preview(data: bytes) -> list[str]:
    text = data.decode("utf-8", errors="replace")
    return text.strip().splitlines()[:5]


def result_bytes_hash(exit_code: int, stdout: bytes, stderr: bytes) -> str:
    payload = (
        f"exit_code={exit_code}\n".encode("utf-8")
        + b"\0stdout\0"
        + stdout
        + b"\0stderr\0"
        + stderr
    )
    return sha256_bytes(payload)


def summarize(samples: list[int]) -> dict[str, object]:
    ordered = sorted(samples)
    return {
        "run_count": len(samples),
        "best_wall_clock_ms": ordered[0],
        "median_wall_clock_ms": ordered[len(ordered) // 2],
        "worst_wall_clock_ms": ordered[-1],
        "spread_wall_clock_ms": ordered[-1] - ordered[0],
    }


def run_case(case: dict[str, object], *, repeat: int, tmp_dir: Path) -> dict[str, object]:
    cmd_template = [str(part) for part in case["cmd"]]  # type: ignore[index]
    cmd = [part.replace("{tmp}", tmp_dir.as_posix()) for part in cmd_template]
    samples: list[int] = []
    runs: list[dict[str, object]] = []
    for _ in range(repeat):
        started = time.perf_counter()
        proc = subprocess.run(
            cmd,
            cwd=ROOT,
            capture_output=True,
        )
        elapsed_ms = int((time.perf_counter() - started) * 1000)
        stdout = proc.stdout or b""
        stderr = proc.stderr or b""
        samples.append(elapsed_ms)
        row: dict[str, object] = {
            "exit_code": proc.returncode,
            "wall_clock_ms": elapsed_ms,
            "stdout_preview": decode_preview(stdout),
            "stderr_preview": decode_preview(stderr),
            "stdout_sha256": sha256_bytes(stdout),
            "stderr_sha256": sha256_bytes(stderr),
            "result_sha256": result_bytes_hash(proc.returncode, stdout, stderr),
            "result_sha256_basis": "exit_code + raw stdout bytes + raw stderr bytes",
        }
        count_hint = case.get("count_hint")
        throughput_kind = case.get("throughput_kind")
        if proc.returncode == 0 and isinstance(count_hint, int) and count_hint > 0 and elapsed_ms > 0:
            row[str(throughput_kind)] = round((count_hint * 1000.0) / elapsed_ms, 3)
        runs.append(row)
        if proc.returncode != 0:
            break
    summary = summarize(samples)
    result_hashes = sorted({
        str(run.get("result_sha256"))
        for run in runs
        if run.get("result_sha256")
    })
    summary["result_sha256_set"] = result_hashes
    summary["result_bit_identical_within_repeat"] = len(result_hashes) == 1

    return {
        **{key: case[key] for key in ("id", "axis", "source_kind", "deterministic_input", "throughput_kind", "count_hint", "note")},
        "cmd": cmd,
        "runs": runs,
        "summary": summary,
        "ok": all(int(run.get("exit_code", 1)) == 0 for run in runs),
    }


def dry_case(case: dict[str, object]) -> dict[str, object]:
    return {
        **{key: case[key] for key in ("id", "axis", "source_kind", "deterministic_input", "throughput_kind", "count_hint", "note")},
        "cmd": case["cmd"],
        "runs": [],
        "summary": {"run_count": 0},
        "ok": None,
        "dry_run": True,
    }


def compare_to_baseline(report: dict, baseline: dict) -> dict[str, object]:
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
        "schema": "ddn.perf_baseline.regression_gate_result.v1",
        "allowed_worse_ratio": allowed_ratio,
        "rows": rows,
        "ok": all(row["status"] != "fail" for row in rows),
    }


def baseline_from_report(report: dict, template: dict) -> dict[str, object]:
    return {
        "schema": "ddn.perf_baseline.baseline.v1",
        "pack_id": "perf_baseline_v1",
        "status": "local_measured_baseline",
        "closure_claim": False,
        "product_perf_claim": False,
        "generated_from_report_schema": report.get("schema"),
        "generated_at_utc": report.get("generated_at_utc"),
        "fallback_policy": {
            "wasm_load_first_frame": "cli_startup_fallback_when_real_browser_wasm_first_frame_unavailable"
        },
        "regression_gate": template.get("regression_gate", {}),
        "cases": [
            {
                "id": case.get("id"),
                "axis": case.get("axis"),
                "source_kind": case.get("source_kind"),
                "deterministic_input": case.get("deterministic_input"),
                "baseline_summary": case.get("summary"),
            }
            for case in report.get("cases", [])
            if isinstance(case, dict)
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run or describe perf_baseline_v1 deterministic benchmark contract")
    parser.add_argument("--json-out", default="", help="optional report path")
    parser.add_argument("--baseline-out", default="", help="optional measured baseline detjson output path")
    parser.add_argument("--baseline", default=str(BASELINE), help="baseline detjson path")
    parser.add_argument("--repeat", type=int, default=1, help="repeat measured cases")
    parser.add_argument("--dry-run", action="store_true", help="emit contract report without timing benchmark cases")
    parser.add_argument("--fail-on-regression", action="store_true", help="exit nonzero when measured report exceeds baseline gate")
    args = parser.parse_args()

    repeat = max(1, int(args.repeat))
    baseline_path = Path(args.baseline)
    if not baseline_path.is_absolute():
        baseline_path = (ROOT / baseline_path).resolve()
    baseline = load_json(baseline_path)

    with tempfile.TemporaryDirectory(prefix="perf_baseline_v1_") as temp_dir:
        tmp_dir = Path(temp_dir)
        cases = [dry_case(case) for case in CASES] if args.dry_run else [
            run_case(case, repeat=repeat, tmp_dir=tmp_dir)
            for case in CASES
        ]

    report = {
        "schema": "ddn.perf_baseline.report.v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "pack": "perf_baseline_v1",
        "dry_run": bool(args.dry_run),
        "repeat": 0 if args.dry_run else repeat,
        "baseline_path": str(baseline_path.relative_to(ROOT) if baseline_path.is_relative_to(ROOT) else baseline_path),
        "measurement_contract_hash_source": "pack/perf_baseline_v1/baseline.detjson",
        "axes": [case["axis"] for case in CASES],
        "cases": cases,
        "regression_gate": compare_to_baseline({"cases": cases}, baseline),
    }
    if args.json_out.strip():
        out = Path(args.json_out)
        if not out.is_absolute():
            out = (ROOT / out).resolve()
        write_json(out, report)
        print(out)
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))

    if args.baseline_out.strip():
        baseline_out = Path(args.baseline_out)
        if not baseline_out.is_absolute():
            baseline_out = (ROOT / baseline_out).resolve()
        write_json(baseline_out, baseline_from_report(report, baseline))
        print(baseline_out)

    if args.fail_on_regression and not bool(report["regression_gate"]["ok"]):  # type: ignore[index]
        return 1
    if not args.dry_run and not all(bool(case.get("ok")) for case in cases):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
