#!/usr/bin/env python
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD = Path("I:/home/urihanl/ddn/codex/build/dayrun_g6")
CONFIG_REPORT = BUILD / "config_digest_proto_report.detjson"
RESERVED_REPORT = BUILD / "reserved_sweep_lint_report.detjson"


def fail(message: str) -> int:
    print(f"dayrun_g6_tools_check: FAIL: {message}", file=sys.stderr)
    return 1


def run(args: list[str], *, timeout: int = 120) -> subprocess.CompletedProcess[str]:
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
    config_selftest = run([sys.executable, "tests/tools/config_digest_proto.py", "--selftest"])
    if config_selftest.returncode != 0:
        return fail(config_selftest.stderr.strip() or config_selftest.stdout.strip())
    if "config_digest_proto: PASS" not in config_selftest.stdout:
        return fail("config digest selftest did not report PASS")

    sample = BUILD / "sample.ddn"
    sample.write_text('설정 { title: "데모". run { seed: 7. madi: 12. }. }.\n', encoding="utf-8")
    config_run = run(
        [
            sys.executable,
            "tests/tools/config_digest_proto.py",
            str(sample),
            "--json-out",
            str(CONFIG_REPORT),
        ]
    )
    if config_run.returncode != 0:
        return fail(config_run.stderr.strip() or config_run.stdout.strip())
    config_report = json.loads(CONFIG_REPORT.read_text(encoding="utf-8"))
    if config_report.get("algo") != "blake3" or not str(config_report.get("digest", "")).startswith("blake3:"):
        return fail("config digest report must use BLAKE3")
    if config_report.get("runtime_schema_touched") is not False:
        return fail("config digest prototype must not claim runtime schema changes")
    settings = config_report.get("canonical", {}).get("settings", {})
    if settings.get("실행", {}).get("마디수") != 12 or settings.get("누리", {}).get("시앗") != 7:
        return fail(f"config canonical settings mismatch: {settings}")

    reserved = run(
        [
            sys.executable,
            "tests/tools/reserved_sweep_lint.py",
            "--check",
            "--json-out",
            str(RESERVED_REPORT),
        ],
        timeout=180,
    )
    if reserved.returncode != 0:
        return fail(reserved.stderr.strip() or reserved.stdout.strip())
    reserved_report = json.loads(RESERVED_REPORT.read_text(encoding="utf-8"))
    if reserved_report.get("g1_match") is not True:
        return fail(f"reserved sweep mismatch: {reserved_report.get('mismatches')}")
    measurements = reserved_report.get("measurements", {})
    if measurements.get("reserved_words_count") != 10 or measurements.get("josa_only_count") != 18:
        return fail(f"reserved/josa counts mismatch: {measurements}")

    print("dayrun_g6_tools_check: PASS")
    print(f"config_report={CONFIG_REPORT.as_posix()}")
    print(f"reserved_report={RESERVED_REPORT.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
