#!/usr/bin/env python3
"""Seal bounded Git provenance without inferring legal rights."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess


SCOPES = {
    "CODE_RIGHTS_INPUT": [
        "core",
        "lang",
        "numeric",
        "proof",
        "symbolic",
        "tool",
        "tools/teul-cli",
        "solutions/seamgrim_ui_mvp/ui",
        "solutions/seamgrim_ui_mvp/tools",
    ],
    "DOCS_RIGHTS_INPUT": [
        "README.md",
        "QUICKSTART.md",
        "publish/spec/CURRENT.md",
        "publish/spec/v0.5.0",
    ],
    "PC01_FIXTURE_RIGHTS_INPUT": ["pack/ddn_v25_pc01_definition_binding_v1"],
    "SELECTED_EXAMPLE_RIGHTS_INPUT": [
        "solutions/seamgrim_ui_mvp/samples",
        "pack/seamgrim_public_physics_wedge_v1",
    ],
    "ASSET_AND_TRADEMARK_RIGHTS_INPUT": [
        "publish/assets/ddonirang_wordmark.png",
        "publish/assets/ddonirang_wordmark.svg",
    ],
}

HISTORICAL_PROJECTILE_PATHS = [
    "solutions/seamgrim_ui_mvp/lessons/ssot_edu_phys_p001_05_projectile_xy/lesson.ddn",
    "solutions/seamgrim_ui_mvp/lessons_rewrite_v1/ssot_edu_phys_p001_05_projectile_xy/lesson.ddn",
]


def git(repo: Path, *args: str, check: bool = True) -> bytes:
    process = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and process.returncode != 0:
        raise RuntimeError(process.stderr.decode("utf-8", errors="replace"))
    return process.stdout


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def contributors(repo: Path, commit: str, paths: list[str]) -> list[dict[str, object]]:
    output = git(repo, "shortlog", "-sne", commit, "--", *paths).decode("utf-8")
    rows: list[dict[str, object]] = []
    for line in output.splitlines():
        count, identity = line.strip().split(maxsplit=1)
        rows.append({"commit_count": int(count), "git_identity": identity})
    return sorted(rows, key=lambda row: str(row["git_identity"]))


def tree_files(repo: Path, commit: str, paths: list[str]) -> list[str]:
    output = git(repo, "ls-tree", "-r", "--name-only", commit, "--", *paths)
    return sorted(line for line in output.decode("utf-8").splitlines() if line)


def last_commit(repo: Path, commit: str, path: str) -> dict[str, str] | None:
    output = git(
        repo,
        "log",
        "-1",
        "--format=%H%x09%an%x09%ae%x09%aI",
        commit,
        "--",
        path,
    ).decode("utf-8").strip()
    if not output:
        return None
    revision, author_name, author_email, authored_at = output.split("\t")
    return {
        "commit": revision,
        "author_name": author_name,
        "author_email": author_email,
        "authored_at": authored_at,
    }


def blob(repo: Path, commit: str, path: str) -> dict[str, object] | None:
    process = subprocess.run(
        ["git", "-C", str(repo), "show", f"{commit}:{path}"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if process.returncode != 0:
        return None
    return {
        "path": path,
        "bytes": len(process.stdout),
        "sha256": sha256(process.stdout),
        "last_commit": last_commit(repo, commit, path),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--source-head", required=True)
    parser.add_argument("--live-projectile", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    repo = args.repo.resolve()
    live = args.live_projectile.resolve()
    resolved = git(repo, "rev-parse", args.source_head).decode("ascii").strip()
    if resolved != args.source_head:
        raise RuntimeError(f"source head mismatch: {resolved}")
    if not live.is_file():
        raise RuntimeError(f"missing live projectile: {live}")

    scope_rows: dict[str, object] = {}
    for name, paths in SCOPES.items():
        files = tree_files(repo, args.source_head, paths)
        scope_rows[name] = {
            "paths": paths,
            "tracked_file_count": len(files),
            "contributors": contributors(repo, args.source_head, paths),
            "path_last_commits": [
                {"path": path, "last_commit": last_commit(repo, args.source_head, path)}
                for path in paths
            ],
        }

    live_bytes = live.read_bytes()
    live_oid = git(repo, "hash-object", "--no-filters", "--", str(live)).decode("ascii").strip()
    object_process = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "-e", f"{live_oid}^{{blob}}"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    historical = [blob(repo, args.source_head, path) for path in HISTORICAL_PROJECTILE_PATHS]

    result = {
        "schema": "ddn.public_rights_provenance_custody.v1",
        "source_head": args.source_head,
        "scopes": scope_rows,
        "projectile_fixture": {
            "live_path": live.as_posix(),
            "bytes": len(live_bytes),
            "sha256": sha256(live_bytes),
            "git_blob_oid": live_oid,
            "exact_blob_exists_in_repository_object_database": object_process.returncode == 0,
            "historical_product_candidates": historical,
            "historical_candidates_byte_identical_to_live": any(
                row is not None and row["sha256"] == sha256(live_bytes) for row in historical
            ),
        },
        "claims": {
            "git_authorship_is_legal_ownership_proof": False,
            "identity_equivalence_resolved": False,
            "code_rights_resolved": False,
            "docs_rights_resolved": False,
            "asset_rights_resolved": False,
            "trademark_rights_resolved": False,
            "lesson_and_sample_rights_resolved": False,
            "third_party_rights_resolved": False,
        },
        "network_access": 0,
        "product_write_count": 0,
        "ssot_write_count": 0,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        f"source={args.source_head} scopes={len(scope_rows)} "
        f"projectile_git_blob={result['projectile_fixture']['exact_blob_exists_in_repository_object_database']} "
        f"sha256={sha256(args.out.read_bytes())}"
    )


if __name__ == "__main__":
    main()
