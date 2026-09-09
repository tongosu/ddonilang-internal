#!/usr/bin/env python
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


MANIFEST_SCHEMA = "seamgrim.private_pilot.release_manifest.v1"
FORBIDDEN_PREFIXES = (
    ".git/",
    "build/",
    "docs/",
    "out/",
    "pack/",
    "tests/",
    "work/",
)
REQUIRED_FIELDS = (
    "source_commit",
    "source_tree_hash",
    "release_created_at",
    "python_version",
    "sqlite_version",
    "rust_toolchain",
    "teul_cli_sha256",
    "wasm_sha256",
    "wasm_binding_sha256",
    "static_asset_manifest_sha256",
    "project_store_schema",
    "deploy_config_sha256",
    "checker_summary",
)


class ReleaseVerificationError(RuntimeError):
    pass


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ReleaseVerificationError(f"{path}: JSON root must be an object")
    return data


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReleaseVerificationError(message)


def verify_path_entry(artifact_root: Path, row: dict[str, Any]) -> None:
    rel = str(row.get("path") or "").replace("\\", "/")
    require(rel and not rel.startswith("/") and ".." not in Path(rel).parts, f"invalid file path: {rel!r}")
    require(
        not any(rel.startswith(prefix) for prefix in FORBIDDEN_PREFIXES),
        f"forbidden release file path: {rel}",
    )
    file_path = artifact_root / rel
    require(file_path.is_file(), f"release file missing: {rel}")
    actual_size = file_path.stat().st_size
    actual_hash = sha256_file(file_path)
    require(actual_size == int(row.get("size", -1)), f"size mismatch for {rel}")
    require(actual_hash == row.get("sha256"), f"sha256 mismatch for {rel}")


def verify_manifest(manifest_path: Path) -> dict[str, Any]:
    manifest_path = manifest_path.resolve()
    artifact_root = manifest_path.parent
    manifest = load_json(manifest_path)
    require(manifest.get("schema") == MANIFEST_SCHEMA, "manifest schema mismatch")
    for field in REQUIRED_FIELDS:
        require(field in manifest, f"manifest missing required field: {field}")

    files = manifest.get("files")
    require(isinstance(files, list) and files, "manifest files must be a non-empty list")
    for row in files:
        require(isinstance(row, dict), "manifest file rows must be objects")
        verify_path_entry(artifact_root, row)

    teul_rel = str(manifest.get("teul_cli_path") or "")
    wasm_rel = str(manifest.get("wasm_path") or "")
    binding_rel = str(manifest.get("wasm_binding_path") or "")
    require(teul_rel, "teul_cli_path missing")
    require(wasm_rel, "wasm_path missing")
    require(binding_rel, "wasm_binding_path missing")
    require(sha256_file(artifact_root / teul_rel) == manifest["teul_cli_sha256"], "teul_cli_sha256 mismatch")
    require(sha256_file(artifact_root / wasm_rel) == manifest["wasm_sha256"], "wasm_sha256 mismatch")
    require(
        sha256_file(artifact_root / binding_rel) == manifest["wasm_binding_sha256"],
        "wasm_binding_sha256 mismatch",
    )

    static_manifest = manifest.get("static_asset_manifest")
    require(isinstance(static_manifest, dict) and static_manifest, "static_asset_manifest missing")
    require(
        sha256_text(stable_json(static_manifest)) == manifest["static_asset_manifest_sha256"],
        "static_asset_manifest_sha256 mismatch",
    )

    deploy_config = manifest.get("deploy_config_files")
    require(isinstance(deploy_config, dict) and deploy_config, "deploy_config_files missing")
    require(
        sha256_text(stable_json(deploy_config)) == manifest["deploy_config_sha256"],
        "deploy_config_sha256 mismatch",
    )

    filesystem_policy = manifest.get("release_filesystem_policy")
    require(isinstance(filesystem_policy, dict), "release_filesystem_policy missing")
    require(filesystem_policy.get("read_only_possible") is True, "release must be read-only possible")
    writable_paths = filesystem_policy.get("writable_paths")
    require(isinstance(writable_paths, list) and writable_paths, "writable paths must be explicit")
    for path in writable_paths:
        require(str(path).startswith("operator:"), "writable paths must be operator-owned")

    runtime_identity = manifest.get("runtime_identity")
    require(isinstance(runtime_identity, dict), "runtime_identity missing")
    require(str(runtime_identity.get("user") or "").strip().lower() not in {"", "0", "root"}, "runtime user is root")

    dependency_status = manifest.get("dependency_pin_status")
    require(isinstance(dependency_status, dict), "dependency_pin_status missing")
    require(dependency_status.get("uses_latest_tag") is False, "floating latest dependency tag is forbidden")
    require(
        dependency_status.get("digest_pin") in {"pinned", "verification_required"},
        "digest pin status must be explicit",
    )

    self_verify = manifest.get("self_verify_command")
    require(isinstance(self_verify, list) and "verify_private_pilot_release.py" in " ".join(self_verify), "self verify missing")
    checker_summary = manifest.get("checker_summary")
    require(isinstance(checker_summary, dict), "checker_summary must be an object")
    require(checker_summary.get("release_builder") == "PASS", "release_builder summary not PASS")
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify a Seamgrim private-pilot release artifact.")
    parser.add_argument("manifest", nargs="?", default="manifest.detjson")
    args = parser.parse_args(argv)
    manifest = verify_manifest(Path(args.manifest))
    print(
        json.dumps(
            {
                "schema": "seamgrim.private_pilot.release_verify_result.v1",
                "status": "PASS",
                "release_id": manifest.get("release_id"),
                "source_commit": manifest.get("source_commit"),
                "file_count": len(manifest.get("files", [])),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ReleaseVerificationError as exc:
        print(f"E_RELEASE_VERIFY: {exc}", file=sys.stderr)
        raise SystemExit(1)
