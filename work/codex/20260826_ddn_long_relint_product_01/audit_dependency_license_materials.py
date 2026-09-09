#!/usr/bin/env python3
"""Inventory locally available dependency license/notice materials offline."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


MATERIAL_NAME = re.compile(
    r"^(?:licen[cs]e|copying|copyright|notice|patents?)(?:[._-].*)?$",
    re.IGNORECASE,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def metadata(manifest: Path) -> dict[str, object]:
    process = subprocess.run(
        [
            "cargo",
            "metadata",
            "--offline",
            "--locked",
            "--format-version",
            "1",
            "--manifest-path",
            str(manifest),
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    return json.loads(process.stdout)


def material_rows(crate_root: Path, declared_license_file: str | None) -> list[dict[str, object]]:
    candidates: set[Path] = set()
    if declared_license_file:
        candidate = (crate_root / declared_license_file).resolve()
        if candidate.is_file() and crate_root in candidate.parents:
            candidates.add(candidate)
    for candidate in crate_root.iterdir():
        if candidate.is_file() and MATERIAL_NAME.match(candidate.name):
            candidates.add(candidate.resolve())
    return [
        {
            "relative_path": path.relative_to(crate_root).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        for path in sorted(candidates)
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--source-head", required=True)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    source = args.source.resolve()

    resolved = subprocess.run(
        ["git", "-C", str(source), "rev-parse", "HEAD"],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
        encoding="ascii",
    ).stdout.strip()
    if resolved != args.source_head:
        raise RuntimeError(f"source head mismatch: {resolved}")

    packages: dict[tuple[str, str, str], dict[str, object]] = {}
    manifests = [source / "Cargo.toml", source / "tools/teul-cli/Cargo.toml"]
    for manifest in manifests:
        for package in metadata(manifest)["packages"]:
            package_source = package.get("source")
            if package_source is None:
                continue
            key = (str(package["name"]), str(package["version"]), str(package_source))
            crate_root = Path(str(package["manifest_path"])).resolve().parent
            materials = material_rows(crate_root, package.get("license_file"))
            packages[key] = {
                "package": package["name"],
                "version": package["version"],
                "source": package_source,
                "declared_license": package.get("license") or "UNDECLARED",
                "declared_license_file": package.get("license_file"),
                "material_file_count": len(materials),
                "materials": materials,
                "selected_license": "UNRESOLVED_FOR_RELEASE",
                "required_notice": "UNRESOLVED_FOR_RELEASE",
            }

    rows = [packages[key] for key in sorted(packages)]
    expressions: dict[str, int] = {}
    for row in rows:
        expression = str(row["declared_license"])
        expressions[expression] = expressions.get(expression, 0) + 1
    missing = [
        {"package": row["package"], "version": row["version"], "declared_license": row["declared_license"]}
        for row in rows
        if int(row["material_file_count"]) == 0
    ]
    and_rows = [
        {"package": row["package"], "version": row["version"], "declared_license": row["declared_license"]}
        for row in rows
        if " AND " in str(row["declared_license"])
    ]
    lgpl_rows = [
        {"package": row["package"], "version": row["version"], "declared_license": row["declared_license"]}
        for row in rows
        if "LGPL" in str(row["declared_license"])
    ]

    result = {
        "schema": "ddn.public_dependency_license_material_custody.v1",
        "status": "CANDIDATE_OPEN_LICENSE_SELECTION_AND_NOTICE_REVIEW",
        "source_head": args.source_head,
        "cargo_package_count": len(rows),
        "declared_license_expression_count": len(expressions),
        "declared_license_expression_counts": dict(sorted(expressions.items())),
        "packages_with_material_count": sum(int(row["material_file_count"]) > 0 for row in rows),
        "packages_without_material_count": len(missing),
        "packages_without_material": missing,
        "and_expression_packages": and_rows,
        "lgpl_expression_packages": lgpl_rows,
        "rows": rows,
        "npm_material_audit": "NOT_PERFORMED_LOCKFILE_ONLY_NO_FRESH_PUBLIC_NPM_INSTALL",
        "license_selection_claim": False,
        "notice_resolution_claim": False,
        "release_inclusion_claim": False,
        "legal_review_claim": False,
        "network_access": 0,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        f"packages={len(rows)} expressions={len(expressions)} "
        f"with_material={result['packages_with_material_count']} "
        f"without_material={len(missing)} and={len(and_rows)} lgpl={len(lgpl_rows)} "
        f"sha256={sha256(args.out)}"
    )


if __name__ == "__main__":
    main()
