#!/usr/bin/env python3
"""Generate the offline dependency candidate ledger for one exact Git HEAD."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess


def metadata(manifest: Path) -> dict[str, object]:
    result = subprocess.run(
        ["cargo", "metadata", "--offline", "--locked", "--format-version", "1",
         "--manifest-path", str(manifest)],
        check=True, text=True, encoding="utf-8", stdout=subprocess.PIPE,
    )
    return json.loads(result.stdout)


def cargo_rows(scope: str, value: dict[str, object]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for package in value["packages"]:
        source = package.get("source")
        if source is None:
            continue
        rows.append({
            "declared_license": package.get("license") or "UNDECLARED",
            "ecosystem": "cargo", "package": package["name"],
            "release_inclusion": "TRANSITIVE_CANDIDATE",
            "required_notice": "UNRESOLVED_FOR_RELEASE", "scope": scope,
            "selected_license": "UNRESOLVED_FOR_RELEASE", "source": source,
            "status": "OPEN_RELEASE_RIGHTS_REVIEW", "version": package["version"],
        })
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
        rows.append({
            "declared_license": package.get("license", "UNDECLARED"), "ecosystem": "npm",
            "integrity": package.get("integrity", "UNSEALED"),
            "package": package_path.removeprefix("node_modules/"),
            "release_inclusion": "DEV_ONLY_CANDIDATE" if package.get("dev") else "TRANSITIVE_CANDIDATE",
            "required_notice": "UNRESOLVED_FOR_RELEASE", "scope": "root-lock",
            "selected_license": "UNRESOLVED_FOR_RELEASE",
            "source": package.get("resolved", "REGISTRY_SOURCE_UNKNOWN"),
            "status": "OPEN_RELEASE_RIGHTS_REVIEW", "version": package.get("version", "UNKNOWN"),
        })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--source-head", required=True)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    source = args.source.resolve()
    resolved = subprocess.run(
        ["git", "-C", str(source), "rev-parse", "HEAD"], check=True,
        text=True, encoding="ascii", stdout=subprocess.PIPE,
    ).stdout.strip()
    if resolved != args.source_head:
        raise SystemExit(f"source head mismatch: {resolved} != {args.source_head}")
    rows = cargo_rows("root-workspace", metadata(source / "Cargo.toml"))
    rows += cargo_rows("teul-cli", metadata(source / "tools/teul-cli/Cargo.toml"))
    rows += node_rows(source)
    dedup: dict[tuple[str, str, str, str], dict[str, object]] = {}
    for row in rows:
        key = (str(row["ecosystem"]), str(row["package"]), str(row["version"]), str(row["source"]))
        if key in dedup:
            scopes = sorted(set(str(dedup[key]["scope"]).split("+") + [str(row["scope"])]))
            dedup[key]["scope"] = "+".join(scopes)
        else:
            dedup[key] = row
    ordered = [dedup[key] for key in sorted(dedup)]
    result = {
        "cargo_row_count": sum(row["ecosystem"] == "cargo" for row in ordered),
        "legal_review_claim": False, "network_access": 0,
        "npm_lockfile_present": (source / "package-lock.json").is_file(),
        "npm_row_count": sum(row["ecosystem"] == "npm" for row in ordered),
        "notice_resolution_claim": False, "release_inclusion_claim": False,
        "row_count": len(ordered), "rows": ordered,
        "schema": "ddn.public_dependency_rights_ledger.candidate.v2",
        "source_head": args.source_head,
        "status": "CANDIDATE_OPEN_RELEASE_RIGHTS_REVIEW",
        "undeclared_cargo_license_count": sum(
            row["ecosystem"] == "cargo" and row["declared_license"] == "UNDECLARED" for row in ordered
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
                        encoding="utf-8", newline="\n")
    print(f"rows={result['row_count']} cargo={result['cargo_row_count']} npm={result['npm_row_count']} ")


if __name__ == "__main__":
    main()
