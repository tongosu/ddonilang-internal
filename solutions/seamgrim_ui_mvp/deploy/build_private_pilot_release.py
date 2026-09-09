#!/usr/bin/env python
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from verify_private_pilot_release import stable_json, verify_manifest


ROOT = Path(__file__).resolve().parents[3]
APP_ROOT = ROOT / "solutions" / "seamgrim_ui_mvp"
DEPLOY_ROOT = APP_ROOT / "deploy"
VERIFY_SCRIPT = DEPLOY_ROOT / "verify_private_pilot_release.py"
MANIFEST_SCHEMA = "seamgrim.private_pilot.release_manifest.v1"
FORBIDDEN_OUTPUT_DIR_NAMES = {"__pycache__", ".pytest_cache", "node_modules"}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo", ".log", ".tmp"}
TEUL_CLI_CANDIDATES = (
    Path("I:/home/urihanl/ddn/codex/target/debug/teul-cli.exe"),
    Path("C:/ddn/codex/target/debug/teul-cli.exe"),
    ROOT / "target" / "debug" / ("teul-cli.exe" if os.name == "nt" else "teul-cli"),
    ROOT / "tools" / "teul-cli" / "target" / "debug" / ("teul-cli.exe" if os.name == "nt" else "teul-cli"),
)
ALLOWLIST_FILES = (
    APP_ROOT / "ddn.project.json",
    APP_ROOT / "learning_spine_index.detjson",
    APP_ROOT / "_headers",
    APP_ROOT / "_redirects",
)
ALLOWLIST_DIRS = (
    APP_ROOT / "deploy",
    APP_ROOT / "lessons",
    APP_ROOT / "lessons_rewrite_v1",
    APP_ROOT / "samples",
    APP_ROOT / "schema",
    APP_ROOT / "seed_lessons_v1",
    APP_ROOT / "tools",
    APP_ROOT / "ui",
)
ALLOWLIST_TOOL_FILES = (
    APP_ROOT / "tools" / "ddn_exec_server.py",
    APP_ROOT / "tools" / "project_store.py",
)
STATIC_ASSET_PREFIXES = (
    "solutions/seamgrim_ui_mvp/lessons/",
    "solutions/seamgrim_ui_mvp/lessons_rewrite_v1/",
    "solutions/seamgrim_ui_mvp/samples/",
    "solutions/seamgrim_ui_mvp/seed_lessons_v1/",
    "solutions/seamgrim_ui_mvp/ui/",
)


class ReleaseBuildError(RuntimeError):
    pass


def run_git(args: list[str]) -> str:
    proc = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0:
        raise ReleaseBuildError(proc.stderr.strip() or proc.stdout.strip() or f"git {' '.join(args)} failed")
    return proc.stdout.strip()


def run_command(args: list[str]) -> str:
    proc = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        raise ReleaseBuildError(proc.stderr.strip() or proc.stdout.strip() or f"{args!r} failed")
    return proc.stdout.strip()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def repo_rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def copy_rel(src: Path, artifact_root: Path, rel: str) -> dict[str, Any]:
    target = artifact_root / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, target)
    return {"path": rel, "size": target.stat().st_size, "sha256": sha256_file(target)}


def iter_release_source_files() -> list[Path]:
    files: list[Path] = []
    for path in ALLOWLIST_FILES + ALLOWLIST_TOOL_FILES:
        if path.exists():
            files.append(path)
    for root in ALLOWLIST_DIRS:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            if any(part in FORBIDDEN_OUTPUT_DIR_NAMES for part in path.parts):
                continue
            if path.suffix.lower() in FORBIDDEN_SUFFIXES:
                continue
            if APP_ROOT / "data" in path.parents:
                continue
            files.append(path)
    return sorted({path.resolve() for path in files}, key=lambda item: repo_rel(item))


def git_status_for_release_inputs() -> list[str]:
    pathspecs = [
        *[repo_rel(path) for path in ALLOWLIST_FILES if path.exists()],
        *[repo_rel(path) for path in ALLOWLIST_TOOL_FILES if path.exists()],
        *[repo_rel(path) for path in ALLOWLIST_DIRS if path.exists()],
    ]
    if not pathspecs:
        return ["no release input pathspecs"]
    proc = subprocess.run(
        ["git", "status", "--short", "--", *pathspecs],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        raise ReleaseBuildError(proc.stderr.strip() or "git status failed")
    return [line for line in proc.stdout.splitlines() if line.strip()]


def resolve_teul_cli() -> Path:
    override = os.environ.get("TEUL_CLI_BIN", "").strip()
    candidates = ([Path(override)] if override else []) + list(TEUL_CLI_CANDIDATES)
    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate.resolve()
    raise ReleaseBuildError("teul-cli binary not found; run cargo check/build before release sealing")


def docker_from_lines(dockerfile: Path) -> list[str]:
    return [
        line.split("#", 1)[0].strip()
        for line in dockerfile.read_text(encoding="utf-8").splitlines()
        if line.split("#", 1)[0].strip().startswith("FROM ")
    ]


def dependency_pin_status(dockerfile: Path) -> dict[str, Any]:
    from_lines = docker_from_lines(dockerfile)
    tags = [line.split()[1] for line in from_lines]
    uses_latest = any(tag.endswith(":latest") or ":" not in tag for tag in tags)
    digest_pinned = all("@sha256:" in tag for tag in tags)
    return {
        "schema": "seamgrim.private_pilot.dependency_pin_status.v1",
        "docker_from": tags,
        "uses_latest_tag": uses_latest,
        "digest_pin": "pinned" if digest_pinned else "verification_required",
        "note": "base image digest verification requires operator-approved image source" if not digest_pinned else "",
    }


def rust_toolchain() -> str:
    try:
        return run_command(["rustc", "--version"])
    except ReleaseBuildError:
        return "verification_required:rustc_unavailable"


def project_store_schema() -> str:
    sys.path.insert(0, str(APP_ROOT / "tools"))
    from project_store import SCHEMA_VERSION

    return str(SCHEMA_VERSION)


def source_commit_created_at(commit: str) -> str:
    try:
        return run_git(["show", "-s", "--format=%cI", commit])
    except ReleaseBuildError:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def build_release(out_dir: Path, *, clean: bool) -> Path:
    source_files = iter_release_source_files()
    dirty_inputs = git_status_for_release_inputs()
    if dirty_inputs:
        raise ReleaseBuildError("release input files are dirty:\n" + "\n".join(dirty_inputs))

    source_commit = run_git(["rev-parse", "HEAD"])
    source_tree_hash = run_git(["rev-parse", "HEAD^{tree}"])
    release_id = f"seamgrim-private-pilot-{source_commit[:12]}-{source_tree_hash[:12]}"
    artifact_root = out_dir.resolve() / release_id
    if artifact_root.exists():
        if not clean:
            raise ReleaseBuildError(f"release artifact already exists: {artifact_root}")
        shutil.rmtree(artifact_root)
    artifact_root.mkdir(parents=True)

    files: list[dict[str, Any]] = []
    for src in source_files:
        rel = repo_rel(src)
        files.append(copy_rel(src, artifact_root, rel))

    teul_cli = resolve_teul_cli()
    teul_rel = f"bin/{teul_cli.name}"
    files.append(copy_rel(teul_cli, artifact_root, teul_rel))
    copy_rel(VERIFY_SCRIPT, artifact_root, "verify_private_pilot_release.py")

    static_asset_manifest = {
        row["path"]: row["sha256"]
        for row in files
        if any(str(row["path"]).startswith(prefix) for prefix in STATIC_ASSET_PREFIXES)
    }
    deploy_config_files = {
        row["path"]: row["sha256"]
        for row in files
        if str(row["path"]).startswith("solutions/seamgrim_ui_mvp/deploy/")
    }
    wasm_path = "solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm"
    wasm_binding_path = "solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.js"
    row_by_path = {str(row["path"]): row for row in files}
    if wasm_path not in row_by_path or wasm_binding_path not in row_by_path:
        raise ReleaseBuildError("WASM artifact or JS binding missing from release inputs")

    manifest = {
        "schema": MANIFEST_SCHEMA,
        "release_id": release_id,
        "source_commit": source_commit,
        "source_tree_hash": source_tree_hash,
        "release_created_at": source_commit_created_at(source_commit),
        "python_version": sys.version.split()[0],
        "sqlite_version": sqlite3.sqlite_version,
        "rust_toolchain": rust_toolchain(),
        "teul_cli_path": teul_rel,
        "teul_cli_sha256": sha256_file(artifact_root / teul_rel),
        "wasm_path": wasm_path,
        "wasm_sha256": row_by_path[wasm_path]["sha256"],
        "wasm_binding_path": wasm_binding_path,
        "wasm_binding_sha256": row_by_path[wasm_binding_path]["sha256"],
        "static_asset_manifest": static_asset_manifest,
        "static_asset_manifest_sha256": sha256_text(stable_json(static_asset_manifest)),
        "project_store_schema": project_store_schema(),
        "deploy_config_files": deploy_config_files,
        "deploy_config_sha256": sha256_text(stable_json(deploy_config_files)),
        "release_filesystem_policy": {
            "schema": "seamgrim.private_pilot.release_filesystem_policy.v1",
            "read_only_possible": True,
            "writable_paths": [
                "operator:SEAMGRIM_PROJECT_DATA_DIR",
                "operator:SEAMGRIM_BACKUP_STAGING_DIR",
                "operator:SEAMGRIM_LOG_DIR",
            ],
            "release_tree_writable": False,
        },
        "runtime_identity": {
            "schema": "seamgrim.private_pilot.runtime_identity.v1",
            "user": "seamgrim",
            "uid": 10001,
            "root_default": False,
        },
        "dependency_pin_status": dependency_pin_status(DEPLOY_ROOT / "Dockerfile"),
        "checker_summary": {
            "schema": "seamgrim.private_pilot.release_checker_summary.v1",
            "release_builder": "PASS",
            "source_allowlist_dirty": "clean",
            "artifact_self_verify": "required",
            "capacity_claim": False,
        },
        "build_context_policy": {
            "schema": "seamgrim.private_pilot.build_context_policy.v1",
            "allowlist_only": True,
            "excluded_prefixes": [".git/", "build/", "docs/", "out/", "pack/", "tests/", "work/"],
            "capability_or_secret_included": False,
            "local_data_included": False,
        },
        "self_verify_command": ["python", "verify_private_pilot_release.py", "manifest.detjson"],
        "files": sorted(files, key=lambda row: str(row["path"])),
    }
    write_json(artifact_root / "manifest.detjson", manifest)
    verify_manifest(artifact_root / "manifest.detjson")
    return artifact_root / "manifest.detjson"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a Seamgrim private-pilot release artifact.")
    parser.add_argument("--out", default="out/seamgrim_private_pilot_release")
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args(argv)
    manifest_path = build_release(Path(args.out), clean=bool(args.clean))
    print(json.dumps({"status": "PASS", "manifest": str(manifest_path)}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ReleaseBuildError as exc:
        print(f"E_RELEASE_BUILD: {exc}", file=sys.stderr)
        raise SystemExit(1)
