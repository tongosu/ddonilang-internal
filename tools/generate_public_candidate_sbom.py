#!/usr/bin/env python3
"""Generate a deterministic offline dependency inventory for a public candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tomllib
from pathlib import Path


def canonical_bytes(payload: dict) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def cargo_metadata(repo_root: Path) -> dict:
    completed = subprocess.run(
        ["cargo", "metadata", "--locked", "--offline", "--format-version", "1"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return json.loads(completed.stdout)


def lock_checksums(lock_path: Path) -> dict[tuple[str, str, str], str]:
    payload = tomllib.loads(lock_path.read_text(encoding="utf-8"))
    rows: dict[tuple[str, str, str], str] = {}
    for package in payload.get("package", []):
        if not isinstance(package, dict):
            continue
        name = str(package.get("name", ""))
        version = str(package.get("version", ""))
        source = str(package.get("source", ""))
        checksum = str(package.get("checksum", ""))
        if name and version and source and checksum:
            rows[(name, version, source)] = checksum
    return rows


def build_inventory(repo_root: Path) -> dict:
    metadata = cargo_metadata(repo_root)
    checksums = lock_checksums(repo_root / "Cargo.lock")
    packages = []
    unknown_license_count = 0
    for package in metadata.get("packages", []):
        source = package.get("source")
        source_identity = str(source) if source else "workspace"
        license_value = package.get("license") or "UNKNOWN_REQUIRES_REVIEW"
        if license_value == "UNKNOWN_REQUIRES_REVIEW":
            unknown_license_count += 1
        packages.append(
            {
                "checksum": checksums.get((str(package["name"]), str(package["version"]), str(source or "")), None),
                "license": license_value,
                "name": package["name"],
                "source": source_identity,
                "version": package["version"],
            }
        )
    packages.sort(key=lambda item: (item["name"], item["version"], item["source"]))
    lock_bytes = (repo_root / "Cargo.lock").read_bytes()
    return {
        "dependencies": packages,
        "dependency_count": len(packages),
        "license_unknown_count": unknown_license_count,
        "schema": "ddonirang.public_dependency_inventory.v1",
        "source_lock_sha256": hashlib.sha256(lock_bytes).hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--verify-repeat", action="store_true")
    args = parser.parse_args()
    payload = build_inventory(args.repo_root.resolve())
    rendered = canonical_bytes(payload)
    if args.verify_repeat and rendered != canonical_bytes(build_inventory(args.repo_root.resolve())):
        raise RuntimeError("E_PUBLIC_SBOM_NONDETERMINISTIC")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
