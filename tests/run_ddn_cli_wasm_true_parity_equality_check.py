#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
AUDIT_SCRIPT = ROOT / "tests" / "run_ddn_cli_wasm_true_parity_divergence_audit.py"
BUILD = Path(os.environ.get("DDN_TRUE_PARITY_AUDIT_DIR", "I:/home/urihanl/ddn/codex/build/true_parity_r0"))
REPORT = BUILD / "true_parity_divergence_audit.detjson"


def fail(message: str) -> int:
    print(f"[ddn-cli-wasm-true-parity-equality] fail: {message}")
    return 1


def run_audit() -> None:
    proc = subprocess.run(
        ["python", str(AUDIT_SCRIPT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=520,
    )
    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip() or f"rc={proc.returncode}"
        raise RuntimeError(f"audit failed: {detail}")


def load_report() -> dict[str, Any]:
    if not REPORT.exists():
        run_audit()
    return json.loads(REPORT.read_text(encoding="utf-8"))


def evaluate_equality(report: dict[str, Any]) -> dict[str, Any]:
    failures: list[str] = []
    if report.get("schema") != "ddn.cli_wasm.true_parity.divergence_audit.v1":
        failures.append(f"bad schema: {report.get('schema')}")
    if report.get("audit_ok") is not True:
        failures.append("audit_ok is not true")
    if report.get("parity_equal") is not True:
        failures.append("audit parity_equal is not true")

    runtime = report.get("runtime13") if isinstance(report.get("runtime13"), dict) else {}
    for row in runtime.get("cases", []):
        if not row.get("accepted"):
            continue
        case_id = row.get("id")
        if row.get("canonical_ddn_equal") is not True:
            failures.append(f"runtime13.{case_id}: canonical_ddn_equal is not true")
        if row.get("execution_envelope_equal") is not True:
            failures.append(f"runtime13.{case_id}: execution envelope not equal")
        if row.get("state_hash_status") != "equal":
            failures.append(f"runtime13.{case_id}: state_hash not equal")
        if row.get("reported_comparison") == "domain_mismatch_reported":
            failures.append(f"runtime13.{case_id}: domain_mismatch_reported cannot satisfy equality")
        if row.get("output_rows_equal") is False:
            failures.append(f"runtime13.{case_id}: output_rows not equal")
        if row.get("output_log_equal") is False:
            failures.append(f"runtime13.{case_id}: output_log not equal")
        if row.get("final_row_equal") is False:
            failures.append(f"runtime13.{case_id}: final_row not equal")

    foundation = report.get("foundation12") if isinstance(report.get("foundation12"), dict) else {}
    for row in foundation.get("lessons", []):
        lesson_id = row.get("lesson_id")
        if row.get("canonical_ddn_comparison") != "equal":
            failures.append(f"foundation12.{lesson_id}: canonical_ddn not equal")
        if row.get("execution_envelope_comparison") != "equal":
            failures.append(f"foundation12.{lesson_id}: execution envelope not equal")
        if row.get("state_hash_status") != "equal":
            failures.append(f"foundation12.{lesson_id}: state_hash not equal")
        if row.get("final_row_comparison") != "equal":
            failures.append(f"foundation12.{lesson_id}: final_row not equal")
        if row.get("output_rows_comparison") != "equal":
            failures.append(f"foundation12.{lesson_id}: output_rows not equal")
        if row.get("output_log_comparison") != "equal":
            failures.append(f"foundation12.{lesson_id}: output_log not equal")

    return {
        "schema": "ddn.cli_wasm.true_parity.equality_result.v1",
        "audit_ok": report.get("audit_ok") is True,
        "parity_equal": not failures,
        "closure_claim": "bounded_behavioral_parity",
        "runtime13_case_count": len(runtime.get("cases", [])) if isinstance(runtime.get("cases"), list) else 0,
        "foundation12_lesson_count": len(foundation.get("lessons", [])) if isinstance(foundation.get("lessons"), list) else 0,
        "not_exposed": [
            "runtime13.trace_hash: wasm runner does not expose trace_hash",
            "runtime13.bogae_hash: wasm runner does not expose bogae_hash",
            "runtime13.view_hash: CLI summary keeps view_hash outside state_hash parity denominator",
            "foundation12.view_hash: browser/view-only hash is not part of state_hash parity denominator",
        ],
        "unchecked": [],
        "failure_count": len(failures),
        "failures": failures,
    }


def selftest() -> list[str]:
    base = {
        "schema": "ddn.cli_wasm.true_parity.divergence_audit.v1",
        "audit_ok": True,
        "parity_equal": True,
        "runtime13": {
            "cases": [
                {
                    "id": "r-ok",
                    "accepted": True,
                    "canonical_ddn_equal": True,
                    "execution_envelope_equal": True,
                    "state_hash_status": "equal",
                    "reported_comparison": "equal",
                    "output_rows_equal": True,
                    "output_log_equal": True,
                    "final_row_equal": True,
                }
            ]
        },
        "foundation12": {
            "lessons": [
                {
                    "lesson_id": "f-ok",
                    "canonical_ddn_comparison": "equal",
                    "execution_envelope_comparison": "equal",
                    "state_hash_status": "equal",
                    "final_row_comparison": "equal",
                    "output_rows_comparison": "equal",
                    "output_log_comparison": "equal",
                }
            ]
        },
    }

    def mutated(mutator):
        doc = json.loads(json.dumps(base))
        mutator(doc)
        return evaluate_equality(doc)["parity_equal"]

    failures: list[str] = []
    if evaluate_equality(base)["parity_equal"] is not True:
        failures.append("selftest equal baseline failed")
    cases = {
        "runtime_hash_mismatch": lambda doc: doc["runtime13"]["cases"][0].__setitem__(
            "state_hash_status", "mismatch"
        ),
        "runtime_domain_mismatch": lambda doc: doc["runtime13"]["cases"][0].__setitem__(
            "reported_comparison", "domain_mismatch_reported"
        ),
        "runtime_canonical_mismatch": lambda doc: doc["runtime13"]["cases"][0].__setitem__(
            "canonical_ddn_equal", False
        ),
        "runtime_envelope_mismatch": lambda doc: doc["runtime13"]["cases"][0].__setitem__(
            "execution_envelope_equal", False
        ),
        "foundation_canonical_mismatch": lambda doc: doc["foundation12"]["lessons"][0].__setitem__(
            "canonical_ddn_comparison", "domain_mismatch_reported"
        ),
        "foundation_envelope_mismatch": lambda doc: doc["foundation12"]["lessons"][0].__setitem__(
            "execution_envelope_comparison", "domain_mismatch_reported"
        ),
        "foundation_output_row_mismatch": lambda doc: doc["foundation12"]["lessons"][0].__setitem__(
            "output_rows_comparison", "domain_mismatch_reported"
        ),
        "foundation_final_row_mismatch": lambda doc: doc["foundation12"]["lessons"][0].__setitem__(
            "final_row_comparison", "domain_mismatch_reported"
        ),
    }
    for name, mutator in cases.items():
        if mutated(mutator):
            failures.append(f"selftest {name} unexpectedly passed equality")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--expect-open",
        action="store_true",
        help="Legacy audit mode: pass only when the current audited report is not equality-closed.",
    )
    parser.add_argument(
        "--require-equal",
        action="store_true",
        help="Pass only when the audited report satisfies true equality.",
    )
    args = parser.parse_args()
    if args.expect_open and args.require_equal:
        return fail("--expect-open and --require-equal are mutually exclusive")
    mode = "expect_open" if args.expect_open else "require_equal"

    try:
        run_audit()
        report = load_report()
    except Exception as exc:  # noqa: BLE001
        return fail(str(exc))

    selftest_failures = selftest()
    if selftest_failures:
        return fail("; ".join(selftest_failures))

    result = evaluate_equality(report)
    out_path = BUILD / "true_parity_equality_result.detjson"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if mode == "expect_open":
        if result["parity_equal"] is True:
            return fail("expected current report to remain parity-open, but equality passed")
        print(
            "[ddn-cli-wasm-true-parity-equality] PASS audit_ok parity_open "
            f"failure_count={result['failure_count']} report={out_path}"
        )
        return 0
    if result["parity_equal"] is not True:
        preview = "; ".join(result["failures"][:8])
        return fail(f"equality failed: {preview}")
    print(f"[ddn-cli-wasm-true-parity-equality] PASS equality report={out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
