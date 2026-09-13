#!/usr/bin/env python3
"""Generate a deterministic candidate dependency ledger without network access."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess


def cargo_metadata(manifest: Path) -> dict[str, object]:
    completed = subprocess.run(
        [
            "cargo",
            "metadata",
            "--offline",
            "--format-version",
            "1",
            "--locked",
            "--manifest-path",
            str(manifest),
        ],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return json.loads(completed.stdout)


def cargo_rows(scope: str, metadata: dict[str, object]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for package in metadata["packages"]:
        source = package.get("source")
        if source is None:
            continue
        declared = package.get("license") or "UNDECLARED"
        rows.append(
            {
                "ecosystem": "cargo",
                "scope": scope,
                "package": package["name"],
                "version": package["version"],
                "source": source,
                "declared_license": declared,
                "selected_license": "UNRESOLVED_FOR_RELEASE",
                "required_notice": "TO_BE_DETERMINED",
                "release_inclusion": "TRANSITIVE_CANDIDATE",
                "status": "OPEN_RELEASE_RIGHTS_REVIEW",
            }
        )
    return rows


def node_rows(source: Path) -> list[dict[str, object]]:
    lock_path = source / "package-lock.json"
    if not lock_path.is_file():
        return []
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    rows: list[dict[str, object]] = []
    for package_path, package in sorted(lock.get("packages", {}).items()):
        if not package_path.startswith("node_modules/"):
            continue
        name = package_path.removeprefix("node_modules/")
        rows.append(
            {
                "ecosystem": "npm",
                "scope": "root-lock",
                "package": name,
                "version": package.get("version", "UNKNOWN"),
                "source": package.get("resolved", "REGISTRY_SOURCE_UNKNOWN"),
                "integrity": package.get("integrity", "UNSEALED"),
                "declared_license": package.get("license", "UNDECLARED"),
                "selected_license": "UNRESOLVED_FOR_RELEASE",
                "required_notice": "TO_BE_DETERMINED",
                "release_inclusion": "DEV_ONLY_CANDIDATE" if package.get("dev") else "TRANSITIVE_CANDIDATE",
                "status": "OPEN_RELEASE_RIGHTS_REVIEW",
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    source = args.source.resolve()

    rows = cargo_rows("root-workspace", cargo_metadata(source / "Cargo.toml"))
    rows += cargo_rows("teul-cli", cargo_metadata(source / "tools/teul-cli/Cargo.toml"))
    rows += node_rows(source)

    dedup: dict[tuple[str, str, str, str], dict[str, object]] = {}
    for row in rows:
        key = (row["ecosystem"], row["package"], row["version"], row["source"])
        if key in dedup:
            scopes = sorted(set(str(dedup[key]["scope"]).split("+") + [str(row["scope"])]))
            dedup[key]["scope"] = "+".join(scopes)
        else:
            dedup[key] = row
    ordered = [dedup[key] for key in sorted(dedup)]
    license_missing = sum(row["declared_license"] == "UNDECLARED" for row in ordered)
    result = {
        "schema": "ddn.public_dependency_rights_ledger.candidate.v1",
        "status": "CANDIDATE_OPEN_RELEASE_RIGHTS_REVIEW",
        "source_head": "905efb4a1601b764e0f4f2554bef3fbd433172a3",
        "network_access": 0,
        "row_count": len(ordered),
        "cargo_row_count": sum(row["ecosystem"] == "cargo" for row in ordered),
        "npm_row_count": sum(row["ecosystem"] == "npm" for row in ordered),
        "undeclared_cargo_license_count": license_missing,
        "npm_lockfile_present": any(
            (source / name).is_file()
            for name in ("package-lock.json", "npm-shrinkwrap.json", "pnpm-lock.yaml", "yarn.lock")
        ),
        "rows": ordered,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        f"rows={result['row_count']} cargo={result['cargo_row_count']} "
        f"npm={result['npm_row_count']} cargo_license_missing={license_missing} "
        f"npm_lockfile={result['npm_lockfile_present']}"
    )


if __name__ == "__main__":
    main()
