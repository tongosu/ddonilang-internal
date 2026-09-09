#!/usr/bin/env python3
"""Preview the Owner-approved full W1 A/B-through-I2 slice without writing the tree."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile


W1_START = "de9cb9ed95f71910bedd2b1bce0769a8257a7f27"
W1_HEAD = "40cd0473061abe806b4b09ba51ccd7bfbbc82431"


def git(repo: Path, *args: str, binary: bool = False) -> str | bytes:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=not binary,
        encoding=None if binary else "utf-8",
    )
    return proc.stdout


def blob_id(repo: Path, commit: str, path: str) -> str:
    output = str(git(repo, "ls-tree", commit, "--", path)).strip()
    return output.split()[2] if output else "ABSENT"


def blob_bytes(repo: Path, commit: str, path: str) -> bytes | None:
    if blob_id(repo, commit, path) == "ABSENT":
        return None
    return bytes(git(repo, "show", f"{commit}:{path}", binary=True))


def merge_preview(ours: bytes, base: bytes, theirs: bytes) -> tuple[str, int]:
    with tempfile.TemporaryDirectory(prefix="ddn-relint-w1-full-") as raw:
        root = Path(raw)
        files = [root / name for name in ("ours", "base", "theirs")]
        for file, payload in zip(files, (ours, base, theirs), strict=True):
            file.write_bytes(payload)
        proc = subprocess.run(
            ["git", "merge-file", "-p", *(str(file) for file in files)],
            check=False,
            capture_output=True,
        )
        return (
            "TEXT_AUTO_MERGE" if proc.returncode == 0 else "TEXT_CONFLICT",
            proc.stdout.count(b"<<<<<<<"),
        )


def role(path: str) -> str:
    if path.endswith((".wasm", ".detjson")) and "/wasm/" in path:
        return "GENERATED_ARTIFACT"
    if path.startswith(("lang/", "tool/", "tools/teul-cli/", "solutions/")):
        return "PRODUCT"
    if path.startswith(("pack/", "tests/", "scripts/")):
        return "TEST_OR_BUILD_EVIDENCE"
    if path.startswith(("docs/", "work/")) or path in {"CHANGELOG.md", "PROJECT_STATUS.md"}:
        return "AUTHORITY_OR_CUSTODY_DOCUMENT"
    return "OTHER"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--ours", default="HEAD")
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()

    paths = str(git(repo, "diff", "--name-only", W1_START, W1_HEAD)).splitlines()
    rows: list[dict[str, object]] = []
    for path in paths:
        base_id = blob_id(repo, W1_START, path)
        ours_id = blob_id(repo, args.ours, path)
        theirs_id = blob_id(repo, W1_HEAD, path)
        row: dict[str, object] = {
            "path": path,
            "role": role(path),
            "base_blob": base_id,
            "ours_blob": ours_id,
            "w1_head_blob": theirs_id,
        }
        if ours_id == theirs_id:
            row["disposition"] = "ALREADY_EQUAL"
        elif ours_id == base_id:
            row["disposition"] = "TAKE_W1_HEAD"
        else:
            payloads = (
                blob_bytes(repo, args.ours, path),
                blob_bytes(repo, W1_START, path),
                blob_bytes(repo, W1_HEAD, path),
            )
            if any(payload is None for payload in payloads):
                row["disposition"] = "ABSENT_OR_DELETE_REVIEW"
                row["conflict_hunks"] = None
            elif any(b"\0" in payload for payload in payloads if payload is not None):
                row["disposition"] = "GENERATED_BINARY_REBUILD"
                row["conflict_hunks"] = None
            else:
                disposition, conflicts = merge_preview(*payloads)  # type: ignore[arg-type]
                row["disposition"] = disposition
                row["conflict_hunks"] = conflicts
        rows.append(row)

    counts: dict[str, int] = {}
    roles: dict[str, int] = {}
    for row in rows:
        key = str(row["disposition"])
        counts[key] = counts.get(key, 0) + 1
        role_name = str(row["role"])
        roles[role_name] = roles.get(role_name, 0) + 1

    result = {
        "schema": "ddn.release_integration.w1_full_slice_merge_audit.v1",
        "ours": str(git(repo, "rev-parse", args.ours)).strip(),
        "w1_start": W1_START,
        "w1_head": W1_HEAD,
        "path_count": len(paths),
        "disposition_counts": dict(sorted(counts.items())),
        "role_counts": dict(sorted(roles.items())),
        "rows": rows,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    digest = hashlib.sha256(args.out.read_bytes()).hexdigest()
    print(f"paths={len(paths)} dispositions={counts} sha256={digest}")


if __name__ == "__main__":
    main()
