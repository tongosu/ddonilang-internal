#!/usr/bin/env python3
"""Project the fixed offline Workbench runtime into a release candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
import shutil
from pathlib import Path, PurePosixPath


MANIFEST_SCHEMA = "ddonirang.workbench_asset_manifest.v1"
COMMON_LESSON_FILES = (
    "active_allowlist.detjson",
    "lesson_cards.v0.detjson",
    "curriculum_crosswalk.v0.detjson",
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_relative(value: str) -> bool:
    path = PurePosixPath(value)
    return bool(value) and not path.is_absolute() and ".." not in path.parts and "\\" not in value


def content_type(path: Path) -> str:
    special = {".wasm": "application/wasm", ".js": "text/javascript", ".json": "application/json", ".detjson": "application/json", ".toml": "text/plain", ".ddn": "text/plain", ".html": "text/html", ".css": "text/css"}
    return special.get(path.suffix.lower()) or mimetypes.guess_type(path.name)[0] or "application/octet-stream"


def copy_file(source: Path, target: Path) -> None:
    if source.is_symlink() or not source.is_file():
        raise RuntimeError("E_WORKBENCH_ASSET_SOURCE_INVALID")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--out-root", type=Path, required=True)
    parser.add_argument("--verify-repeat", action="store_true")
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    ui = repo / "solutions" / "seamgrim_ui_mvp" / "ui"
    lessons = repo / "solutions" / "seamgrim_ui_mvp" / "lessons"
    out = args.out_root.resolve()
    if out.exists():
        raise RuntimeError("E_WORKBENCH_ASSET_OUTPUT_EXISTS")
    out.mkdir(parents=True)

    # The whole tracked UI tree is the product runtime, not a development directory.
    for source in sorted(ui.rglob("*")):
        if source.is_dir():
            continue
        relative = source.relative_to(ui)
        copy_file(source, out / relative)

    allowlist = json.loads((lessons / "active_allowlist.detjson").read_text(encoding="utf-8"))
    ids = allowlist.get("lesson_ids")
    if not isinstance(ids, list) or len(ids) != 15 or len(set(ids)) != 15 or not all(isinstance(item, str) for item in ids):
        raise RuntimeError("E_WORKBENCH_LESSON_ALLOWLIST_INVALID")
    for name in COMMON_LESSON_FILES:
        copy_file(lessons / name, out / "lessons" / name)
    # app.js consumes this existing product index at the bundle root.  It is
    # data, not a generated release-only view, so preserve its tracked bytes.
    copy_file(repo / "solutions" / "seamgrim_ui_mvp" / "learning_spine_index.detjson", out / "learning_spine_index.detjson")
    index_source = json.loads((lessons / "index.json").read_text(encoding="utf-8"))
    rows = index_source.get("lessons") if isinstance(index_source, dict) else None
    if not isinstance(rows, list):
        raise RuntimeError("E_WORKBENCH_LESSON_INDEX_INVALID")
    by_id = {row.get("id"): row for row in rows if isinstance(row, dict) and isinstance(row.get("id"), str)}
    if set(ids) - set(by_id) or len(by_id) != len({row.get("id") for row in rows if isinstance(row, dict)}):
        raise RuntimeError("E_WORKBENCH_LESSON_INDEX_INVALID")
    projected = {"lessons": [by_id[item] for item in ids]}
    (out / "lessons").mkdir(exist_ok=True)
    (out / "lessons" / "index.json").write_text(json.dumps(projected, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    for lesson_id in ids:
        source_dir = lessons / lesson_id
        if not source_dir.is_dir() or source_dir.is_symlink():
            raise RuntimeError("E_WORKBENCH_LESSON_ASSET_MISSING")
        for source in sorted(source_dir.rglob("*")):
            if source.is_dir():
                continue
            copy_file(source, out / "lessons" / source.relative_to(lessons))

    files = []
    for source in sorted(out.rglob("*")):
        if source.is_dir():
            continue
        relative = source.relative_to(out).as_posix()
        if not safe_relative(relative):
            raise RuntimeError("E_WORKBENCH_ASSET_PATH_INVALID")
        data = source.read_bytes()
        role = "entry" if relative == "index.html" else ("wasm" if source.suffix == ".wasm" else ("lesson" if relative.startswith("lessons/") else "runtime"))
        files.append({"path": relative, "bytes": len(data), "sha256": sha256(data), "content_type": content_type(source), "role": role})
    if not any(item["path"] == "index.html" for item in files):
        raise RuntimeError("E_WORKBENCH_INDEX_MISSING")
    manifest = {"schema": MANIFEST_SCHEMA, "files": files}
    rendered = json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    manifest_path = out / "asset_manifest.detjson"
    manifest_path.write_text(rendered, encoding="utf-8")
    if args.verify_repeat and manifest_path.read_text(encoding="utf-8") != rendered:
        raise RuntimeError("E_WORKBENCH_ASSET_MANIFEST_NONDETERMINISTIC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
