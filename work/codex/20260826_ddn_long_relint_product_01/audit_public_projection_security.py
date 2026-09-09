#!/usr/bin/env python3
"""Bounded current-tree security and portability preflight.

Matched secret-like text is never copied into the report; only its category,
location, and SHA-256 are recorded.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re


STRONG_PATTERNS = {
    "PEM_PRIVATE_KEY_HEADER": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "AWS_ACCESS_KEY_ID": re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    "GITHUB_TOKEN": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{36,255}\b"),
    "GOOGLE_API_KEY": re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    "OPENAI_API_KEY": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
    "SLACK_TOKEN": re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{10,}\b"),
}

INTERNAL_MARKERS = {
    "PRIVATE_ABSOLUTE_PATH_I": re.compile(r"I:/home/urihanl/ddn/codex", re.IGNORECASE),
    "PRIVATE_ABSOLUTE_PATH_C": re.compile(r"C:/ddn/codex", re.IGNORECASE),
    "OFFICIAL_STORE_PATH": re.compile(r"official-store", re.IGNORECASE),
    "PRIVATE_SSOT_PATH": re.compile(r"docs/ssot/(?:ssot|pack|walks|age)/", re.IGNORECASE),
}

FORBIDDEN_FILE_NAMES = {
    ".env",
    ".npmrc",
    ".pypirc",
    "credentials",
    "credentials.json",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
    "id_rsa",
}

SENSITIVE_SUFFIXES = {".db", ".key", ".p12", ".pem", ".pfx", ".sqlite", ".sqlite3"}
EXECUTABLE_SUFFIXES = {".dll", ".dylib", ".exe", ".pyc", ".so"}
ARCHIVE_SUFFIXES = {".7z", ".gz", ".rar", ".tar", ".tgz", ".zip"}
REVIEW_BINARY_SUFFIXES = {".bin", ".detbin", ".dtm", ".packet"}
TEXT_SUFFIXES = {
    "", ".cfg", ".conf", ".css", ".csv", ".ddn", ".detjson", ".html",
    ".ini", ".js", ".json", ".jsonl", ".lock", ".md", ".mjs", ".ps1", ".py",
    ".rs", ".sh", ".svg", ".template", ".toml", ".ts", ".tsv", ".txt",
    ".yaml", ".yml",
}
MAX_TEXT_BYTES = 10 * 1024 * 1024


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def match_rows(path: str, text: str, patterns: dict[str, re.Pattern[str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for category, pattern in patterns.items():
            for match in pattern.finditer(line):
                rows.append({
                    "path": path,
                    "line": line_number,
                    "category": category,
                    "match_sha256": digest(match.group(0).encode("utf-8")),
                })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--projection", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    projection = args.projection.resolve()
    if not projection.is_dir():
        raise RuntimeError(f"missing projection: {projection}")

    files = sorted(path for path in projection.rglob("*") if path.is_file())
    secret_findings: list[dict[str, object]] = []
    marker_findings: list[dict[str, object]] = []
    sensitive_files: list[dict[str, object]] = []
    executable_files: list[dict[str, object]] = []
    archive_files: list[dict[str, object]] = []
    review_binary_files: list[dict[str, object]] = []
    skipped_large_or_binary: list[dict[str, object]] = []

    for file in files:
        relative = file.relative_to(projection).as_posix()
        raw = file.read_bytes()
        suffix = file.suffix.lower()
        lower_name = file.name.lower()
        row = {"path": relative, "bytes": len(raw), "sha256": digest(raw)}
        if lower_name in FORBIDDEN_FILE_NAMES or suffix in SENSITIVE_SUFFIXES:
            sensitive_files.append(row)
        if suffix in EXECUTABLE_SUFFIXES:
            executable_files.append(row)
        if suffix in ARCHIVE_SUFFIXES:
            archive_files.append(row)
        if suffix in REVIEW_BINARY_SUFFIXES:
            review_binary_files.append(row)
        if len(raw) > MAX_TEXT_BYTES or suffix not in TEXT_SUFFIXES:
            skipped_large_or_binary.append(row)
            continue
        if b"\x00" in raw:
            skipped_large_or_binary.append(row)
            continue
        text = raw.decode("utf-8", errors="ignore")
        secret_findings.extend(match_rows(relative, text, STRONG_PATTERNS))
        marker_findings.extend(match_rows(relative, text, INTERNAL_MARKERS))

    result = {
        "schema": "ddn.public_projection.security_portability_preflight.v1",
        "status": "FAIL_CLOSED"
        if secret_findings or sensitive_files or executable_files or archive_files
        else "CANDIDATE_REVIEW",
        "projection_file_count": len(files),
        "secret_pattern_findings": sorted(
            secret_findings, key=lambda row: (str(row["path"]), int(row["line"]), str(row["category"]))
        ),
        "internal_marker_findings": sorted(
            marker_findings, key=lambda row: (str(row["path"]), int(row["line"]), str(row["category"]))
        ),
        "sensitive_file_candidates": sensitive_files,
        "executable_file_candidates": executable_files,
        "archive_file_candidates": archive_files,
        "review_binary_candidates": review_binary_files,
        "skipped_large_or_binary_count": len(skipped_large_or_binary),
        "skipped_large_or_binary": skipped_large_or_binary,
        "history_wide_audit_claim": False,
        "fresh_successor_projection_claim": False,
        "matched_secret_values_disclosed": False,
        "network_access": 0,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        f"status={result['status']} files={len(files)} secrets={len(secret_findings)} "
        f"markers={len(marker_findings)} sensitive_files={len(sensitive_files)} "
        f"executables={len(executable_files)} archives={len(archive_files)} "
        f"review_binaries={len(review_binary_files)} "
        f"sha256={digest(args.out.read_bytes())}"
    )


if __name__ == "__main__":
    main()
