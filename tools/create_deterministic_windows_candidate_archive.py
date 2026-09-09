#!/usr/bin/env python3
"""Seal a public Windows candidate into a deterministic, offline ZIP archive."""

from __future__ import annotations

import argparse
import hashlib
import json
from io import BytesIO
from pathlib import Path, PurePosixPath
from zipfile import ZIP_STORED, ZipFile, ZipInfo


EXPECTED_EXECUTABLES = {"ddonilang.exe", "ddonirang.exe", "또니랑.exe"}


def canonical_bytes(payload: dict) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def valid_relative_path(value: str) -> bool:
    path = PurePosixPath(value)
    return bool(value) and not path.is_absolute() and ".." not in path.parts and "\\" not in value


def load_entries(artifact_root: Path, manifest_path: Path) -> list[dict]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rows = manifest.get("files")
    if manifest.get("schema") != "ddonirang.windows_public_candidate_manifest.v1" or not isinstance(rows, list):
        raise RuntimeError("E_WINDOWS_CANDIDATE_ARCHIVE_MANIFEST_INVALID")
    seen: set[str] = set()
    entries: list[dict] = []
    for row in rows:
        if not isinstance(row, dict):
            raise RuntimeError("E_WINDOWS_CANDIDATE_ARCHIVE_MANIFEST_INVALID")
        name = row.get("path")
        if not isinstance(name, str) or not valid_relative_path(name) or name in seen:
            raise RuntimeError("E_WINDOWS_CANDIDATE_ARCHIVE_ENTRY_INVALID")
        seen.add(name)
        path = artifact_root / name
        data = path.read_bytes() if path.is_file() else None
        if data is None or len(data) != row.get("bytes") or hashlib.sha256(data).hexdigest() != row.get("sha256"):
            raise RuntimeError("E_WINDOWS_CANDIDATE_ARCHIVE_PAYLOAD_MISMATCH")
        entries.append({"path": name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "data": data})
    executable_names = {entry["path"] for entry in entries if entry["path"].endswith(".exe")}
    discovered_executables = {path.relative_to(artifact_root).as_posix() for path in artifact_root.rglob("*.exe")}
    if executable_names != EXPECTED_EXECUTABLES or discovered_executables != EXPECTED_EXECUTABLES:
        raise RuntimeError("E_WINDOWS_CANDIDATE_ARCHIVE_EXECUTABLE_SET")
    if any("teul-cli" in entry["path"].lower() for entry in entries):
        raise RuntimeError("E_WINDOWS_CANDIDATE_ARCHIVE_RETIRED_TEUL")
    return sorted(entries, key=lambda entry: entry["path"])


def render_archive(entries: list[dict]) -> bytes:
    comment = canonical_bytes({
        "files": [{key: entry[key] for key in ("path", "bytes", "sha256")} for entry in entries],
        "schema": "ddonirang.windows_candidate_archive_manifest.v1",
    })
    output = BytesIO()
    with ZipFile(output, "w", compression=ZIP_STORED, strict_timestamps=True) as archive:
        archive.comment = comment
        for entry in entries:
            info = ZipInfo(entry["path"], date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_STORED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, entry["data"])
    return output.getvalue()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--verify-repeat", action="store_true")
    args = parser.parse_args()
    entries = load_entries(args.artifact_root, args.manifest)
    rendered = render_archive(entries)
    if args.verify_repeat and rendered != render_archive(load_entries(args.artifact_root, args.manifest)):
        raise RuntimeError("E_WINDOWS_CANDIDATE_ARCHIVE_NONDETERMINISTIC")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
