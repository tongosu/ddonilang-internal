#!/usr/bin/env python3
"""Verify the self-contained public Language SPEC current and SHA-256 seal."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC_ROOT = ROOT / "publish" / "spec"
CURRENT = SPEC_ROOT / "CURRENT.md"
PUBLIC_VERSION = "v0.5.0"
FAMILY = SPEC_ROOT / PUBLIC_VERSION
MANIFEST = FAMILY / "SPEC_MANIFEST_v0.5.0.md"
SEAL = FAMILY / "SPEC_SHA256_v0.5.0.md"
TRACE = FAMILY / "SPEC_TRACE_v0.5.0.detjson"


def fail(message: str) -> None:
    raise SystemExit(f"PUBLIC LANGUAGE SPEC CHECK: FAIL\n- {message}")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def verify_text(path: Path) -> None:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        fail(f"UTF-8 BOM is not allowed: {path.relative_to(ROOT)}")
    if b"\r" in raw:
        fail(f"CR line ending is not allowed: {path.relative_to(ROOT)}")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail(f"invalid UTF-8: {path.relative_to(ROOT)}: {exc}")
    for line_number, line in enumerate(text.splitlines(), 1):
        if line.rstrip(" \t") != line:
            fail(f"trailing whitespace: {path.relative_to(ROOT)}:{line_number}")


def main() -> None:
    for path in (CURRENT, MANIFEST, SEAL, TRACE):
        if not path.is_file():
            fail(f"required file is missing: {path.relative_to(ROOT)}")

    current = CURRENT.read_text(encoding="utf-8")
    marker = (
        "현재 공개판: "
        "[`v0.5.0`](./v0.5.0/SPEC_MANIFEST_v0.5.0.md)"
    )
    if marker not in current:
        fail("publish/spec/CURRENT.md does not select v0.5.0")

    seal_text = SEAL.read_text(encoding="utf-8")
    rows = re.findall(
        r"^\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|$",
        seal_text,
        re.MULTILINE,
    )
    if len(rows) != 17:
        fail(f"seal row count is {len(rows)}, expected 17")

    sealed_paths = {relative for relative, _, _ in rows}
    actual_paths = {
        path.relative_to(FAMILY).as_posix()
        for path in FAMILY.rglob("*")
        if path.is_file() and path != SEAL
    }
    if actual_paths != sealed_paths:
        fail(f"sealed file set drift: {sorted(actual_paths ^ sealed_paths)}")

    for relative, expected_size, expected_hash in rows:
        path = FAMILY / relative
        raw = path.read_bytes()
        if len(raw) != int(expected_size):
            fail(f"sealed byte size drift: {relative}")
        if sha256(raw) != expected_hash:
            fail(f"sealed SHA-256 drift: {relative}")

    trace = json.loads(TRACE.read_text(encoding="utf-8"))
    ranges = [
        (row["rd_start"], row["rd_end"])
        for row in trace.get("decision_projection", [])
    ]
    decisions = [
        number
        for start, end in ranges
        for number in range(start, end + 1)
    ]
    if decisions != list(range(1, 123)):
        fail("RD-001~122 coverage is not continuous and unique")
    if trace.get("public_family") != PUBLIC_VERSION:
        fail("trace public_family is not v0.5.0")
    if trace.get("status") != "public current / owner-approved / independently reviewed / docs-first / product-open":
        fail("trace status does not preserve docs-first/product-open boundary")

    open_gates = "\n".join(trace.get("open_gates", []))
    for marker in ("P1", "C-02", "C-04", "C-05", "C-06", "exact wire"):
        if marker not in open_gates:
            fail(f"required OPEN marker is missing: {marker}")

    for path in [CURRENT, *FAMILY.rglob("*")]:
        if path.is_file():
            verify_text(path)

    print("PUBLIC LANGUAGE SPEC CHECK: PASS")
    print(f"- public_current: {PUBLIC_VERSION}")
    print(f"- sealed_files: {len(rows)}")
    print(f"- manifest_sha256: {sha256(MANIFEST.read_bytes())}")
    print(f"- seal_sha256: {sha256(SEAL.read_bytes())}")
    print("- RD coverage: 001~122 continuous and unique")
    print("- product state: OPEN / NOT RUNTIME LANDED")


if __name__ == "__main__":
    main()
