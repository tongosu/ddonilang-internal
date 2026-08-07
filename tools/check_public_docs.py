#!/usr/bin/env python3
"""Validate the public GitHub introduction and localization bundle."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLISH = ROOT / "publish"
I18N = PUBLISH / "i18n"

LOCALES = {
    "ay",
    "de",
    "en",
    "es",
    "eu",
    "fr",
    "ja",
    "kn",
    "ko",
    "mn",
    "ne",
    "qu",
    "sym3",
    "ta",
    "te",
    "tr",
    "zh",
}

LEGACY_STUBS = {
    "ay",
    "en",
    "eu",
    "ja",
    "kn",
    "mn",
    "ne",
    "qu",
    "sym3",
    "ta",
    "te",
    "tr",
}

ACTIVE_ROOT_DOCS = [
    ROOT / "README.md",
    PUBLISH / "README.md",
    PUBLISH / "INDEX.md",
    PUBLISH / "QUICKSTART.md",
    PUBLISH / "LEARNING_PATH.md",
    PUBLISH / "PRODUCT_SUPPORT_CURRENT.md",
    PUBLISH / "LOCALIZATION.md",
    PUBLISH / "DDONIRANG_DEV_STRUCTURE.md",
    PUBLISH / "DOWNLOADS.md",
]

REFERENCE_DOCS = [
    PUBLISH / "ddonirang_grammar_summary.md",
    PUBLISH / "ddonirang_grammar_full.md",
]

REMOVED_CURRENT_DOCS = [
    PUBLISH / "GITHUB_RELEASE_DRAFT_20260211.md",
    PUBLISH / "CI_AGGREGATE_GATE_FIX_NOTE_20260223.md",
]

FORBIDDEN_ACTIVE_TEXT = [
    "codex/queue-20260706",
    "Round 1.5",
    "또니랑의 6원소 계약",
    "NuriGym",
]

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def read_utf8(path: Path, errors: list[str]) -> str:
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        fail(errors, f"missing: {path.relative_to(ROOT)}")
        return ""
    if raw.startswith(b"\xef\xbb\xbf"):
        fail(errors, f"UTF-8 BOM: {path.relative_to(ROOT)}")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail(errors, f"not UTF-8: {path.relative_to(ROOT)} ({exc})")
        return ""


def check_format(path: Path, text: str, errors: list[str]) -> None:
    relative = path.relative_to(ROOT)
    if "\r" in text:
        fail(errors, f"CR line ending: {relative}")
    for line_number, line in enumerate(text.split("\n"), 1):
        if line.endswith((" ", "\t")):
            fail(errors, f"trailing whitespace: {relative}:{line_number}")


def check_links(path: Path, text: str, errors: list[str]) -> None:
    for target in LINK_RE.findall(text):
        target = target.strip().strip("<>")
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        file_part = target.split("#", 1)[0]
        resolved = (path.parent / file_part).resolve()
        if not resolved.exists():
            fail(
                errors,
                f"broken link: {path.relative_to(ROOT)} -> {target}",
            )


def main() -> int:
    errors: list[str] = []

    actual_locales = {entry.name for entry in I18N.iterdir() if entry.is_dir()}
    if actual_locales != LOCALES:
        fail(
            errors,
            "locale folders differ: "
            f"missing={sorted(LOCALES - actual_locales)} "
            f"extra={sorted(actual_locales - LOCALES)}",
        )

    generated_docs: list[Path] = [I18N / "INDEX.md"]
    for locale in sorted(LOCALES):
        locale_dir = I18N / locale
        for name in ("README.md", "QUICKSTART.md", "DEV_STRUCTURE.md", "DOWNLOADS.md"):
            generated_docs.append(locale_dir / name)
        if not (locale_dir / "RELEASE_NOTES_20260211.md").exists():
            fail(errors, f"missing historical release note: publish/i18n/{locale}")

    legacy_docs: list[Path] = []
    for locale in sorted(LEGACY_STUBS):
        stub = PUBLISH / f"README_{locale}.md"
        legacy_docs.append(stub)
        text = read_utf8(stub, errors)
        if f"i18n/{locale}/README.md" not in text:
            fail(errors, f"legacy pointer is stale: {stub.relative_to(ROOT)}")
        if len(text.splitlines()) > 12:
            fail(errors, f"legacy pointer is not a short stub: {stub.relative_to(ROOT)}")

    active_docs = ACTIVE_ROOT_DOCS + REFERENCE_DOCS + generated_docs + legacy_docs
    for path in active_docs:
        text = read_utf8(path, errors)
        check_format(path, text, errors)
        check_links(path, text, errors)

    for path in ACTIVE_ROOT_DOCS + generated_docs:
        text = read_utf8(path, errors)
        for token in FORBIDDEN_ACTIVE_TEXT:
            if token in text:
                fail(errors, f"stale public text {token!r}: {path.relative_to(ROOT)}")

    for path in REFERENCE_DOCS:
        text = read_utf8(path, errors)
        if "역사적 참고 요약 / 현행 규범 아님" not in text:
            fail(errors, f"historical grammar banner missing: {path.relative_to(ROOT)}")

    for path in REMOVED_CURRENT_DOCS:
        if path.exists():
            fail(errors, f"obsolete current-public document remains: {path.relative_to(ROOT)}")

    root_readme = read_utf8(ROOT / "README.md", errors)
    for expected in ("Language SPEC v0.5.0", "v24.25.0", "라이선스"):
        if expected not in root_readme:
            fail(errors, f"README boundary missing: {expected}")

    support = read_utf8(PUBLISH / "PRODUCT_SUPPORT_CURRENT.md", errors)
    if "protected `main`" not in support and "보호된 `main`" not in support:
        fail(errors, "product support matrix does not identify protected main")

    if errors:
        print("PUBLIC DOCS CHECK: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "PUBLIC DOCS CHECK: PASS "
        f"({len(LOCALES)} locales, {len(active_docs)} active documents)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
