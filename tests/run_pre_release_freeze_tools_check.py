#!/usr/bin/env python
from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def preferred_build_root() -> Path:
    primary = Path("I:/home/urihanl/ddn/codex/build")
    fallback = Path("C:/ddn/codex/build")
    if primary.exists():
        return primary
    if fallback.exists():
        return fallback
    return ROOT / "build"


BUILD = preferred_build_root() / "pre_release_freeze_tools"
REPORT = BUILD / "pre_release_freeze_tools_report.detjson"
SUMMARY = BUILD / "pre_release_freeze_tools_summary.md"
RESERVED_REPORT = BUILD / "reserved_sweep_lint_report.detjson"
FREEZE_REPORT = ROOT / "docs" / "reports" / "audit" / "PRE_RELEASE_FREEZE_SWEEP_V1.md"

SCAN_ROOTS = [
    "core",
    "lang",
    "tool",
    "tools",
    "tests",
    "pack",
    "docs/context",
    "docs/reports",
]

SYNTAX_PATTERNS = [
    "#모두필요",
    "#빈칸채움",
    "@단위계",
    "~분포",
    "~이름",
    "BLOCK_HEADER",
    "HASH_FORBIDDEN",
    "BANG_UNARY_RESERVED",
]

SYNTAX_PROBES = [
    {"id": "tilde_distribution_ident", "source": "~분포"},
    {"id": "tilde_distribution_call", "source": "~분포(정규)"},
    {"id": "tilde_name_call", "source": "~이름(값)"},
    {"id": "hash_candidate_atom", "source": "#동결후보"},
    {"id": "at_bare_candidate", "source": "@단위계"},
    {"id": "at_unit_candidate", "source": "1@단위계"},
]


def fail(message: str) -> int:
    print(f"pre_release_freeze_tools_check: FAIL: {message}", file=sys.stderr)
    return 1


def run(args: list[str], *, timeout: int = 180) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def iter_text_files() -> list[Path]:
    paths: list[Path] = []
    ignored_parts = {".git", "target", "target-wsl", "build", "out", "_out"}
    for root_name in SCAN_ROOTS:
        root = ROOT / root_name
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            rel_parts = set(path.relative_to(ROOT).parts)
            if ignored_parts & rel_parts:
                continue
            if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".exe", ".dll"}:
                continue
            paths.append(path)
    return sorted(paths)


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            return None


def count_lines_with(pattern: str, paths: list[Path]) -> dict[str, Any]:
    line_count = 0
    file_counts: Counter[str] = Counter()
    regex = re.compile(pattern)
    for path in paths:
        text = read_text(path)
        if text is None:
            continue
        rel = path.relative_to(ROOT).as_posix()
        for line in text.splitlines():
            if regex.search(line):
                line_count += 1
                file_counts[rel] += 1
    return {
        "line_count": line_count,
        "top_files": [{"path": path, "lines": count} for path, count in file_counts.most_common(20)],
    }


def literal_counts(paths: list[Path]) -> dict[str, int]:
    counts = {pattern: 0 for pattern in SYNTAX_PATTERNS}
    for path in paths:
        text = read_text(path)
        if text is None:
            continue
        for pattern in SYNTAX_PATTERNS:
            counts[pattern] += text.count(pattern)
    return counts


def e_namespace(paths: list[Path]) -> dict[str, Any]:
    token_re = re.compile(r"\bE_[A-Z0-9_]+\b")
    tokens: set[str] = set()
    prefix_counts: Counter[str] = Counter()
    file_counts: Counter[str] = Counter()
    for path in paths:
        text = read_text(path)
        if text is None:
            continue
        rel = path.relative_to(ROOT).as_posix()
        found = set(token_re.findall(text))
        if not found:
            continue
        tokens.update(found)
        file_counts[rel] += len(found)
        for token in found:
            parts = token.split("_")
            prefix = "_".join(parts[:2]) if len(parts) > 1 else token
            prefix_counts[prefix] += 1
    return {
        "unique_count": len(tokens),
        "prefix_counts": [{"prefix": prefix, "count": count} for prefix, count in prefix_counts.most_common(30)],
        "top_files": [{"path": path, "unique_tokens": count} for path, count in file_counts.most_common(20)],
    }


def schema_version_status(paths: list[Path]) -> dict[str, Any]:
    status = count_lines_with(r"schema_version", paths)
    versions: Counter[str] = Counter()
    value_re = re.compile(r"schema_version[\"'\s:=]+([A-Za-z0-9_.-]+)")
    for path in paths:
        text = read_text(path)
        if text is None:
            continue
        for value in value_re.findall(text):
            versions[value.strip("\"' ,})]")] += 1
    status["version_mentions"] = [{"value": value, "count": count} for value, count in versions.most_common(20)]
    return status


def parse_existing_freeze_numbers() -> dict[str, Any]:
    text = FREEZE_REPORT.read_text(encoding="utf-8")
    numbers: dict[str, Any] = {}
    patterns = {
        "reserved_candidate_surfaces": r"새 후보 표면 ([0-9,]+)개",
        "e_unique_wide": r"초기 넓은 스윕 기준 ([0-9,]+)개",
        "e_unique_dayrun": r"DAYRUN 재현 스윕 기준 unique ([0-9,]+)개",
        "schema_version_lines": r"`schema_version` 흔적은 ([0-9,]+)줄",
        "pack_candidates_final": r"최종 표에서는 ([0-9,]+)개 중 충돌 ([0-9,]+)개",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if not match:
            numbers[key] = None
            continue
        if key == "pack_candidates_final":
            numbers[key] = {
                "candidates": int(match.group(1).replace(",", "")),
                "collisions": int(match.group(2).replace(",", "")),
            }
        else:
            numbers[key] = int(match.group(1).replace(",", ""))
    return numbers


def run_reserved_lint() -> tuple[dict[str, Any], dict[str, Any]]:
    proc = run(
        [
            sys.executable,
            "tests/tools/reserved_sweep_lint.py",
            "--check",
            "--json-out",
            str(RESERVED_REPORT),
        ],
        timeout=240,
    )
    log_path = BUILD / "reserved_sweep_lint.log"
    log_path.write_text(proc.stdout + "\n--- stderr ---\n" + proc.stderr, encoding="utf-8")
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip())
    return json.loads(RESERVED_REPORT.read_text(encoding="utf-8")), {
        "command": f"{sys.executable} tests/tools/reserved_sweep_lint.py --check --json-out {RESERVED_REPORT.as_posix()}",
        "exit_code": proc.returncode,
        "log": log_path.as_posix(),
    }


def run_syntax_probe(case: dict[str, str]) -> dict[str, Any]:
    case_dir = BUILD / "syntax_probes"
    case_dir.mkdir(parents=True, exist_ok=True)
    source_path = case_dir / f"{case['id']}.ddn"
    summary_path = case_dir / f"{case['id']}.summary.detjson"
    log_path = case_dir / f"{case['id']}.log"
    source_path.write_text(case["source"] + "\n", encoding="utf-8")
    cmd = [
        "cargo",
        "run",
        "--quiet",
        "--manifest-path",
        "tools/teul-cli/Cargo.toml",
        "--",
        "run",
        str(source_path),
        "--summary-json",
        str(summary_path),
    ]
    proc = run(cmd, timeout=180)
    log_path.write_text(
        "command: " + " ".join(cmd) + "\n"
        + f"exit_code: {proc.returncode}\n"
        + "--- stdout ---\n"
        + proc.stdout
        + "\n--- stderr ---\n"
        + proc.stderr,
        encoding="utf-8",
    )
    combined = proc.stdout + "\n" + proc.stderr
    code_match = re.search(r"\bE_[A-Z0-9_]+\b", combined)
    return {
        "id": case["id"],
        "source": case["source"],
        "exit_code": proc.returncode,
        "error_code": code_match.group(0) if code_match else None,
        "stdout_first_line": proc.stdout.splitlines()[0] if proc.stdout.splitlines() else "",
        "stderr_first_line": proc.stderr.splitlines()[0] if proc.stderr.splitlines() else "",
        "input": source_path.as_posix(),
        "summary_json_exists": summary_path.exists(),
        "log": log_path.as_posix(),
    }


def product_path_status() -> str:
    proc = run(["git", "status", "--short", "--", "lang", "core", "tool", "tools/teul-cli/src"], timeout=30)
    if proc.returncode != 0:
        return f"git status failed: {proc.stderr.strip()}"
    return proc.stdout.strip()


def write_summary(report: dict[str, Any]) -> None:
    measurements = report["reserved_lint"]["measurements"]
    schema = report["schema_version"]
    e_status = report["e_namespace"]
    comparison = report["comparison_to_pre_release_freeze_sweep_v1"]
    lines = [
        "# pre_release_freeze_tools summary",
        "",
        f"- report: `{REPORT.as_posix()}`",
        f"- reserved words: {measurements['reserved_words_count']}",
        f"- reserved candidates: {len(report['reserved_lint']['reserved_candidate_report_rows'])}",
        f"- syntax probe cases: {len(report['syntax_probes'])}",
        f"- current E_* unique tokens: {e_status['unique_count']}",
        f"- schema_version lines: {schema['line_count']}",
        f"- pack candidates/collisions: {measurements['pack_candidates']}/{measurements['pack_collisions']}",
        f"- product path status: `{report['product_path_status'] or 'clean'}`",
        "",
        "## comparison",
        "",
        "```json",
        json.dumps(comparison, ensure_ascii=False, indent=2),
        "```",
    ]
    SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    try:
        BUILD.mkdir(parents=True, exist_ok=True)
        paths = iter_text_files()
        reserved, reserved_command = run_reserved_lint()
        syntax_probes = [run_syntax_probe(case) for case in SYNTAX_PROBES]
        schema = schema_version_status(paths)
        e_status = e_namespace(paths)
        syntax_static = literal_counts(paths)
        freeze_numbers = parse_existing_freeze_numbers()
        measurements = reserved["measurements"]
        comparison = {
            "baseline": freeze_numbers,
            "current": {
                "reserved_candidate_surfaces": len(reserved["reserved_candidate_report_rows"]),
                "e_unique_wide_from_reserved_lint": measurements["e_unique_tokens_wide"],
                "e_unique_dayrun_from_reserved_lint": measurements["e_unique_tokens_dayrun_reported"],
                "e_unique_current_scan_scope": e_status["unique_count"],
                "schema_version_lines_current_scan_scope": schema["line_count"],
                "pack_candidates": measurements["pack_candidates"],
                "pack_collisions": measurements["pack_collisions"],
            },
        }
        report = {
            "schema": "ddn.pre_release_freeze_tools.report.v1",
            "status": "PASS",
            "closure_grade": "닫힘-문서",
            "generated_by": "python tests/run_pre_release_freeze_tools_check.py",
            "build_dir": BUILD.as_posix(),
            "sources": {
                "existing_freeze_report": FREEZE_REPORT.relative_to(ROOT).as_posix(),
                "reserved_sweep_lint": "tests/tools/reserved_sweep_lint.py",
            },
            "reserved_lint_command": reserved_command,
            "reserved_lint": reserved,
            "syntax_static_counts": syntax_static,
            "syntax_probes": syntax_probes,
            "e_namespace": e_status,
            "schema_version": schema,
            "pack_id_collision_status": {
                "candidate_count": measurements["pack_candidates"],
                "collision_count": measurements["pack_collisions"],
                "collisions": reserved["pack_collisions"],
            },
            "comparison_to_pre_release_freeze_sweep_v1": comparison,
            "product_runtime_parser_changed": False,
            "product_path_status": product_path_status(),
        }
        REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        write_summary(report)
        if report["product_path_status"]:
            return fail(f"product path has pending changes: {report['product_path_status']}")
        print("pre_release_freeze_tools_check: PASS")
        print(f"report={REPORT.as_posix()}")
        print(f"summary={SUMMARY.as_posix()}")
        return 0
    except Exception as exc:
        return fail(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
