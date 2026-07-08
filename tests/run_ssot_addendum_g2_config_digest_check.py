#!/usr/bin/env python
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def preferred_build_root() -> Path:
    primary = Path("I:/home/urihanl/ddn/codex/build")
    fallback = Path("C:/ddn/codex/build")
    if primary.exists():
        return primary
    if fallback.exists():
        return fallback
    return ROOT / "build"


BUILD = preferred_build_root() / "ssot_addendum_g2_config_digest"
REPORT = BUILD / "ssot_addendum_g2_config_digest_report.detjson"


def fail(message: str) -> int:
    print(f"ssot_addendum_g2_config_digest_check: FAIL: {message}", file=sys.stderr)
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


def parse_selftest(stdout: str) -> dict:
    start = stdout.find("{")
    if start < 0:
        raise ValueError("selftest JSON missing")
    return json.loads(stdout[start:])


def main() -> int:
    BUILD.mkdir(parents=True, exist_ok=True)

    selftest = run([sys.executable, "tests/tools/config_digest_proto.py", "--selftest"], timeout=180)
    if selftest.returncode != 0:
        return fail(selftest.stderr.strip() or selftest.stdout.strip())
    if "config_digest_proto: PASS" not in selftest.stdout:
        return fail("selftest did not print PASS")
    selftest_report = parse_selftest(selftest.stdout)
    if selftest_report.get("schema") != "ddn.config_digest_proto.selftest.v2":
        return fail(f"unexpected selftest schema: {selftest_report.get('schema')}")
    pairs = selftest_report.get("pairs", [])
    if len(pairs) != 3:
        return fail(f"expected 3 equivalence pairs, got {len(pairs)}")
    required_hashes = {"run_config_hash", "view_config_hash", "doc_config_hash", "settings_hash"}
    for row in pairs:
        if set(row.get("hashes", {})) != required_hashes:
            return fail(f"missing split hashes in pair {row}")

    sample = BUILD / "sample_settings.ddn"
    sample.write_text(
        '설정 { 문서 { 제목: "G2". }. 누리 { 시앗: 11. 시앗묶음: "physics,policy". }. 실행 { 마디수: 5. }. 보개 { 주보기: "graph2d". }. }.\n',
        encoding="utf-8",
    )
    sample_report_path = BUILD / "sample_settings_report.detjson"
    sample_run = run(
        [
            sys.executable,
            "tests/tools/config_digest_proto.py",
            str(sample),
            "--json-out",
            str(sample_report_path),
        ],
        timeout=180,
    )
    if sample_run.returncode != 0:
        return fail(sample_run.stderr.strip() or sample_run.stdout.strip())
    sample_report = json.loads(sample_report_path.read_text(encoding="utf-8"))
    if set(sample_report.get("hashes", {})) != required_hashes:
        return fail("sample report missing split hashes")
    if sample_report["hashes"]["run_config_hash"] == sample_report["hashes"]["view_config_hash"]:
        return fail("run_config_hash and view_config_hash are not separated")
    classifier = sample_report.get("result_affecting_classifier", {})
    if classifier.get("draft_only") is not True:
        return fail("classifier must be marked draft_only")
    classifier_paths = {row.get("path"): row.get("class") for row in classifier.get("rows", [])}
    for path in ["누리.시앗", "누리.시앗묶음", "실행.마디수"]:
        if classifier_paths.get(path) != "result_affecting":
            return fail(f"missing result-affecting classifier row for {path}: {classifier_paths}")
    seed_fixture = sample_report.get("seed_stream_fixture", {})
    if seed_fixture.get("input_snapshot_written") is not False:
        return fail("derived seed must stop before InputSnapshot")
    streams = seed_fixture.get("streams", [])
    if [row.get("stream_name") for row in streams] != ["physics", "policy"]:
        return fail(f"seed stream names mismatch: {streams}")
    if not all(str(row.get("derived_seed", "")).startswith("blake3:") for row in streams):
        return fail("derived seeds must be BLAKE3 digests")
    for key in ["runtime_schema_touched", "state_hash_touched", "parser_touched"]:
        if sample_report.get(key) is not False:
            return fail(f"{key} must be false")

    product_status = run(["git", "status", "--short", "--", "lang", "core", "tool", "tools/teul-cli/src"], timeout=30)
    if product_status.returncode != 0:
        return fail(product_status.stderr.strip())
    if product_status.stdout.strip():
        return fail(f"product path changed: {product_status.stdout.strip()}")

    report = {
        "schema": "ddn.ssot_addendum_g2_config_digest_check.report.v1",
        "status": "PASS",
        "closure_grade": "닫힘-문서",
        "selftest_pairs": len(pairs),
        "hashes": sample_report["hashes"],
        "classifier_version": classifier.get("version"),
        "seed_streams": streams,
        "sample_report": sample_report_path.as_posix(),
        "runtime_schema_touched": False,
        "state_hash_touched": False,
        "parser_touched": False,
        "product_path_status": product_status.stdout.strip(),
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("ssot_addendum_g2_config_digest_check: PASS")
    print(f"report={REPORT.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
