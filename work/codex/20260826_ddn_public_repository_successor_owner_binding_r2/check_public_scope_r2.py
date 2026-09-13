#!/usr/bin/env python3
"""Fail-closed membership and portability audit for an R2 public preview tree."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re


TEST_REF = re.compile(r"tests/[A-Za-z0-9_./-]+\.(?:py|mjs|js|json)")
TEXT_SUFFIXES = {".c", ".css", ".ddn", ".detjson", ".h", ".html", ".js", ".json", ".md", ".mjs", ".py", ".rs", ".toml", ".ts", ".txt", ".yml", ".yaml"}
SKIP_DIRS = {".git", "build", "node_modules", "out", "target"}


def bounded_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for current, dirs, names in os.walk(root):
        dirs[:] = sorted(name for name in dirs if name not in SKIP_DIRS)
        base = Path(current)
        files.extend(base / name for name in sorted(names))
    return files


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tree", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    args = parser.parse_args()
    tree = args.tree.resolve()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))

    missing_members: list[str] = []
    role_counts: dict[str, int] = {}
    for role in manifest["roles"]:
        count = 0
        for relative in role.get("required_paths", []):
            if (tree / relative).is_file():
                count += 1
            else:
                missing_members.append(relative)
        for relative in role.get("required_trees", []):
            path = tree / relative
            if path.is_dir() and any(item.is_file() for item in path.rglob("*")):
                count += 1
            else:
                missing_members.append(relative + "/")
        role_counts[role["role"]] = count

    spec = manifest["expected_public_spec"]
    entrypoint = tree / spec["entrypoint"]
    spec_text = entrypoint.read_text(encoding="utf-8") if entrypoint.is_file() else ""
    spec_marker_ok = spec["marker"] in spec_text
    spec_manifest_ok = (tree / spec["required_manifest"]).is_file()

    facade_missing = [path for path in manifest["required_public_facade"] if not (tree / path).is_file()]
    selected_tests = [tree / path for role in manifest["roles"] if role["role"] == "PUBLIC_CONFORMANCE_SUBSET" for path in role["required_paths"]]
    referenced: set[str] = set()
    for path in selected_tests:
        if path.is_file():
            referenced.update(TEST_REF.findall(path.read_text(encoding="utf-8", errors="ignore")))
    missing_test_refs = sorted(path for path in referenced if not (tree / path).is_file())

    marker_hits: dict[str, list[str]] = {}
    marker_hit_counts: dict[str, int] = {}
    all_marker_paths: set[str] = set()
    all_files = bounded_files(tree)
    text_files = [path for path in all_files if path.suffix.lower() in TEXT_SUFFIXES]
    raw_hits: dict[str, list[str]] = {marker: [] for marker in manifest["forbidden_internal_path_markers"]}
    for path in text_files:
        content = path.read_text(encoding="utf-8", errors="ignore")
        relative = path.relative_to(tree).as_posix()
        for marker, hits in raw_hits.items():
            if marker in content:
                hits.append(relative)
    for marker, hits in raw_hits.items():
        if hits:
            ordered_hits = sorted(hits)
            marker_hit_counts[marker] = len(ordered_hits)
            all_marker_paths.update(ordered_hits)
            marker_hits[marker] = ordered_hits[:25]

    blockers = []
    if missing_members:
        blockers.append("REQUIRED_SCOPE_MEMBER_MISSING")
    if not spec_marker_ok or not spec_manifest_ok:
        blockers.append("PUBLIC_SPEC_IDENTITY_MISMATCH")
    if facade_missing:
        blockers.append("PUBLIC_FACADE_RIGHTS_POLICY_FILES_MISSING")
    if missing_test_refs:
        blockers.append("PUBLIC_CONFORMANCE_TRANSITIVE_CLOSURE_MISSING")
    if marker_hits:
        blockers.append("INTERNAL_PATH_MARKERS_PRESENT")

    result = {
        "schema": "ddn.public_product_scope_check.r2.v1",
        "blockers": blockers,
        "facade_missing": facade_missing,
        "internal_marker_file_count": len(all_marker_paths),
        "marker_hit_counts": marker_hit_counts,
        "marker_hits": marker_hits,
        "missing_members": sorted(missing_members),
        "missing_test_refs": missing_test_refs,
        "public_spec_expected": spec["marker"],
        "public_spec_manifest_present": spec_manifest_ok,
        "public_spec_marker_present": spec_marker_ok,
        "role_counts": role_counts,
        "status": "PASS" if not blockers else "FAIL_CLOSED",
        "tree_path_semantic_identity": "sha256:" + hashlib.sha256("\n".join(sorted(path.relative_to(tree).as_posix() for path in all_files)).encode("utf-8")).hexdigest(),
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if not blockers else 1)


if __name__ == "__main__":
    main()
