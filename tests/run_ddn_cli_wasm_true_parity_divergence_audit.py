#!/usr/bin/env python
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BUILD = Path(os.environ.get("DDN_TRUE_PARITY_AUDIT_DIR", "I:/home/urihanl/ddn/codex/build/true_parity_r0"))
RUNTIME_RUNNER = ROOT / "tests" / "seamgrim_wasm_cli_runtime_parity_runner.mjs"
RUNTIME_PACK = ROOT / "pack" / "seamgrim_wasm_cli_runtime_parity_v1"
FOUNDATION_RUNNER = ROOT / "tests" / "seamgrim_foundation12_cli_raw_wasm_parity_runner.mjs"


def fail(message: str) -> int:
    print(f"[ddn-cli-wasm-true-parity-divergence-audit] fail: {message}")
    return 1


def run_json(cmd: list[str], output_path: Path, timeout: int) -> tuple[int, dict[str, Any], str]:
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )
    output_path.write_text(proc.stdout, encoding="utf-8")
    if not proc.stdout.strip():
        return proc.returncode, {}, proc.stderr.strip()
    try:
        return proc.returncode, json.loads(proc.stdout), proc.stderr.strip()
    except json.JSONDecodeError as exc:
        return proc.returncode, {}, f"invalid json: {exc}; stderr={proc.stderr.strip()}"


def hash_status(cli_hash: str, wasm_hash: str, reject: bool) -> str:
    if reject:
        return "reject_no_state_hash_expected"
    if not cli_hash or not wasm_hash:
        return "missing"
    if cli_hash == wasm_hash:
        return "equal"
    return "mismatch"


def summarize_runtime13(report: dict[str, Any]) -> dict[str, Any]:
    rows = []
    accepted = 0
    hash_mismatches = 0
    canonical_mismatches = 0
    envelope_mismatches = 0
    final_row_mismatches = 0
    output_rows_mismatches = 0
    output_log_mismatches = 0
    domain_success_rows = 0
    first_divergence = None
    for row in report.get("cases", []):
        strict = row.get("strict_evidence") if isinstance(row.get("strict_evidence"), dict) else {}
        state_hash = strict.get("state_hash") if isinstance(strict.get("state_hash"), dict) else {}
        envelope = strict.get("execution_envelope") if isinstance(strict.get("execution_envelope"), dict) else {}
        reject = int(row.get("cli_exit_code", 0)) != 0
        status = hash_status(str(state_hash.get("cli", "")), str(state_hash.get("wasm", "")), reject)
        if not reject:
            accepted += 1
            if status == "mismatch":
                hash_mismatches += 1
            if strict.get("canonical_ddn_equal") is not True:
                canonical_mismatches += 1
            if envelope.get("equal") is not True:
                envelope_mismatches += 1
            if (strict.get("output_rows") or {}).get("equal") is False:
                output_rows_mismatches += 1
            if (strict.get("output_log") or {}).get("equal") is False:
                output_log_mismatches += 1
            if (strict.get("final_row") or {}).get("equal") is False:
                final_row_mismatches += 1
            if state_hash.get("comparison") == "domain_mismatch_reported":
                domain_success_rows += 1
        item = {
            "id": row.get("id"),
            "accepted": not reject,
            "canonical_ddn_equal": strict.get("canonical_ddn_equal"),
            "execution_envelope_equal": envelope.get("equal"),
            "cli_state_hash": state_hash.get("cli", ""),
            "wasm_state_hash": state_hash.get("wasm", ""),
            "state_hash_status": status,
            "reported_comparison": state_hash.get("comparison", ""),
            "output_rows_equal": (strict.get("output_rows") or {}).get("equal"),
            "output_log_equal": (strict.get("output_log") or {}).get("equal"),
            "final_row_equal": (strict.get("final_row") or {}).get("equal"),
        }
        if first_divergence is None and not reject and envelope.get("equal") is not True:
            first_divergence = {
                "case_id": row.get("id"),
                "tick_id": 0,
                "field_path": "execution_envelope",
                "classification": "execution_envelope",
                "cli": envelope.get("cli"),
                "wasm": envelope.get("wasm"),
            }
        if first_divergence is None and not reject and strict.get("canonical_ddn_equal") is not True:
            first_divergence = {
                "case_id": row.get("id"),
                "tick_id": 0,
                "field_path": "canonical_ddn",
                "classification": "preprocess/canon",
            }
        if first_divergence is None and status == "mismatch":
            first_divergence = {
                "case_id": row.get("id"),
                "tick_id": 0,
                "field_path": "state_hash",
                "classification": "hash_domain",
                "cli": state_hash.get("cli", ""),
                "wasm": state_hash.get("wasm", ""),
            }
        if first_divergence is None and not reject and (strict.get("output_rows") or {}).get("equal") is False:
            first_divergence = {
                "case_id": row.get("id"),
                "tick_id": 0,
                "field_path": "output_rows",
                "classification": "output_projection",
            }
        if first_divergence is None and not reject and (strict.get("output_log") or {}).get("equal") is False:
            first_divergence = {
                "case_id": row.get("id"),
                "tick_id": 0,
                "field_path": "output_log",
                "classification": "output_projection",
            }
        rows.append(item)
    return {
        "accepted_cases": accepted,
        "state_hash_mismatch_count": hash_mismatches,
        "canonical_mismatch_count": canonical_mismatches,
        "execution_envelope_mismatch_count": envelope_mismatches,
        "output_rows_mismatch_count": output_rows_mismatches,
        "output_log_mismatch_count": output_log_mismatches,
        "final_row_mismatch_count": final_row_mismatches,
        "domain_mismatch_reported_rows": domain_success_rows,
        "first_divergence": first_divergence,
        "cases": rows,
    }


def summarize_foundation12(report: dict[str, Any]) -> dict[str, Any]:
    rows = []
    hash_mismatches = 0
    canonical_mismatches = 0
    envelope_mismatches = 0
    final_row_mismatches = 0
    output_rows_mismatches = 0
    output_log_mismatches = 0
    first_divergence = None
    for row in report.get("lessons", []):
        strict = row.get("strict_evidence") if isinstance(row.get("strict_evidence"), dict) else {}
        cli = row.get("cli") if isinstance(row.get("cli"), dict) else {}
        wasm = row.get("wasm") if isinstance(row.get("wasm"), dict) else {}
        cli_hash = str(cli.get("state_hash", ""))
        wasm_hash = str(wasm.get("state_hash", ""))
        hash_equal = bool(cli_hash and wasm_hash and cli_hash == wasm_hash)
        if not hash_equal:
            hash_mismatches += 1
        if strict.get("canonical_ddn_comparison") != "equal":
            canonical_mismatches += 1
        if strict.get("execution_envelope_comparison") != "equal":
            envelope_mismatches += 1
        if strict.get("final_row_comparison") != "equal":
            final_row_mismatches += 1
        if strict.get("output_rows_comparison") != "equal":
            output_rows_mismatches += 1
        if strict.get("output_log_comparison") != "equal":
            output_log_mismatches += 1
        item = {
            "lesson_id": row.get("lesson_id"),
            "canonical_ddn_comparison": strict.get("canonical_ddn_comparison"),
            "execution_envelope_comparison": strict.get("execution_envelope_comparison"),
            "final_row_comparison": strict.get("final_row_comparison"),
            "output_rows_comparison": strict.get("output_rows_comparison"),
            "output_log_comparison": strict.get("output_log_comparison"),
            "cli_state_hash": cli_hash,
            "wasm_state_hash": wasm_hash,
            "state_hash_status": "equal" if hash_equal else "mismatch",
            "cli_final_row_key_count": cli.get("final_row_key_count"),
            "wasm_final_row_key_count": wasm.get("final_row_key_count"),
            "cli_output_row_count": cli.get("output_row_count"),
            "wasm_output_row_count": wasm.get("output_row_count"),
        }
        if first_divergence is None and strict.get("execution_envelope_comparison") != "equal":
            first_divergence = {
                "lesson_id": row.get("lesson_id"),
                "tick_id": 0,
                "field_path": "execution_envelope",
                "classification": "execution_envelope",
            }
        if first_divergence is None and strict.get("canonical_ddn_comparison") != "equal":
            first_divergence = {
                "lesson_id": row.get("lesson_id"),
                "tick_id": 0,
                "field_path": "canonical_ddn",
                "classification": "preprocess/canon",
            }
        if first_divergence is None and not hash_equal:
            first_divergence = {
                "lesson_id": row.get("lesson_id"),
                "tick_id": 0,
                "field_path": "state_hash",
                "classification": "hash_domain",
                "cli": cli_hash,
                "wasm": wasm_hash,
            }
        if first_divergence is None and strict.get("final_row_comparison") != "equal":
            first_divergence = {
                "lesson_id": row.get("lesson_id"),
                "tick_id": 0,
                "field_path": "final_row",
                "classification": "state_projection",
            }
        if first_divergence is None and strict.get("output_rows_comparison") != "equal":
            first_divergence = {
                "lesson_id": row.get("lesson_id"),
                "tick_id": 0,
                "field_path": "output_rows",
                "classification": "output_projection",
            }
        if first_divergence is None and strict.get("output_log_comparison") != "equal":
            first_divergence = {
                "lesson_id": row.get("lesson_id"),
                "tick_id": 0,
                "field_path": "output_log",
                "classification": "output_projection",
            }
        rows.append(item)
    return {
        "lesson_count": len(rows),
        "state_hash_mismatch_count": hash_mismatches,
        "canonical_mismatch_count": canonical_mismatches,
        "execution_envelope_mismatch_count": envelope_mismatches,
        "final_row_mismatch_count": final_row_mismatches,
        "output_rows_mismatch_count": output_rows_mismatches,
        "output_log_mismatch_count": output_log_mismatches,
        "first_divergence": first_divergence,
        "lessons": rows,
    }


def main() -> int:
    BUILD.mkdir(parents=True, exist_ok=True)
    runtime_path = BUILD / "runtime13.raw.detjson"
    foundation_path = BUILD / "foundation12.raw.detjson"
    runtime_rc, runtime_report, runtime_err = run_json(
        ["node", "--no-warnings", str(RUNTIME_RUNNER), str(RUNTIME_PACK)],
        runtime_path,
        300,
    )
    if runtime_rc != 0:
        return fail(runtime_err or f"runtime runner rc={runtime_rc}")
    foundation_rc, foundation_report, foundation_err = run_json(
        ["node", "--no-warnings", str(FOUNDATION_RUNNER)],
        foundation_path,
        420,
    )
    if foundation_rc != 0:
        return fail(foundation_err or f"foundation runner rc={foundation_rc}")

    runtime = summarize_runtime13(runtime_report)
    foundation = summarize_foundation12(foundation_report)
    runtime_equal = (
        runtime["state_hash_mismatch_count"] == 0
        and runtime["canonical_mismatch_count"] == 0
        and runtime["execution_envelope_mismatch_count"] == 0
        and runtime["output_rows_mismatch_count"] == 0
        and runtime["output_log_mismatch_count"] == 0
        and runtime["final_row_mismatch_count"] == 0
        and runtime["domain_mismatch_reported_rows"] == 0
    )
    foundation_equal = (
        foundation["state_hash_mismatch_count"] == 0
        and foundation["canonical_mismatch_count"] == 0
        and foundation["execution_envelope_mismatch_count"] == 0
        and foundation["final_row_mismatch_count"] == 0
        and foundation["output_rows_mismatch_count"] == 0
        and foundation["output_log_mismatch_count"] == 0
    )
    parity_equal = runtime_equal and foundation_equal
    summary = {
        "schema": "ddn.cli_wasm.true_parity.divergence_audit.v1",
        "audit_ok": True,
        "parity_equal": parity_equal,
        "base_head": "2ddfe46",
        "raw_reports": {
            "runtime13": str(runtime_path).replace("\\", "/"),
            "foundation12": str(foundation_path).replace("\\", "/"),
        },
        "runtime13": runtime,
        "foundation12": foundation,
        "classification": {
            "primary": "equal" if parity_equal else "divergence_present",
            "notes": [
                "Audit records divergence if present; zero divergence is a valid post-repair result.",
                "domain_mismatch_reported remains audit evidence only and cannot satisfy equality.",
            ],
        },
    }
    out_path = BUILD / "true_parity_divergence_audit.detjson"
    out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    failures = []
    if runtime["accepted_cases"] != 12:
        failures.append(f"runtime accepted count expected 12 got {runtime['accepted_cases']}")
    if foundation["lesson_count"] != 12:
        failures.append(f"foundation lesson count expected 12 got {foundation['lesson_count']}")
    if runtime["domain_mismatch_reported_rows"] != 0:
        failures.append(
            f"runtime domain_mismatch_reported_rows expected 0 got {runtime['domain_mismatch_reported_rows']}"
        )
    if not parity_equal and not (runtime["first_divergence"] or foundation["first_divergence"]):
        failures.append("first divergence evidence missing for non-equal audit")
    if failures:
        return fail("; ".join(failures))
    print(
        "[ddn-cli-wasm-true-parity-divergence-audit] PASS "
        f"runtime_hash_mismatch={runtime['state_hash_mismatch_count']} "
        f"foundation_hash_mismatch={foundation['state_hash_mismatch_count']} "
        f"parity_equal={int(parity_equal)} "
        f"report={out_path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
