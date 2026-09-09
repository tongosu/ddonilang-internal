#!/usr/bin/env python3
"""Deterministic read-only audit for the R1 public projection.

The script reads a clean source checkout, an already generated projection, and
the owner-bound public product scope manifest. It does not alter either tree.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re


TEST_REF = re.compile(r"tests/[A-Za-z0-9_./-]+\.(?:py|mjs|js|json)")
RUST_INCLUDE = re.compile(
    r'include_(?:str|bytes)!\s*\(\s*"([^"]+)"\s*\)', re.DOTALL
)
INTERNAL_MARKERS = (
    "I:/home/urihanl/ddn/codex",
    "I:\\home\\urihanl\\ddn\\codex",
    "docs/ssot/ssot",
    "official-store",
    "work/claude",
    "work/codex",
)
TEXT_SUFFIXES = {
    ".c", ".css", ".ddn", ".detjson", ".h", ".html", ".js",
    ".json", ".md", ".mjs", ".py", ".rs", ".toml", ".ts",
    ".txt", ".yml", ".yaml",
}
FACADE = (
    "README.md", "QUICKSTART.md", "LICENSE", "NOTICE", "SECURITY.md",
    "CONTRIBUTING.md", "SUPPORT.md", "CODE_OF_CONDUCT.md",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bounded_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*") if path.is_file())


def recursive_conformance_closure(
    source: Path, projection: Path, roots: list[str]
) -> dict[str, object]:
    pending = list(sorted(roots))
    seen: set[str] = set()
    missing_source: set[str] = set()
    missing_projection: set[str] = set()
    edges: list[dict[str, str]] = []

    while pending:
        relative = pending.pop(0)
        if relative in seen:
            continue
        seen.add(relative)
        source_path = source / relative
        if not source_path.is_file():
            missing_source.add(relative)
            continue
        if not (projection / relative).is_file():
            missing_projection.add(relative)
        content = source_path.read_text(encoding="utf-8", errors="ignore")
        for dependency in sorted(set(TEST_REF.findall(content))):
            edges.append({"from": relative, "to": dependency})
            if dependency not in seen:
                pending.append(dependency)
        pending.sort()

    return {
        "root_count": len(roots),
        "closure_count": len(seen),
        "edge_count": len(edges),
        "closure": sorted(seen),
        "edges": sorted(edges, key=lambda item: (item["from"], item["to"])),
        "missing_in_source": sorted(missing_source),
        "missing_in_projection": sorted(missing_projection),
    }


def rust_private_fixture_references(source: Path, projection: Path) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for rust_file in sorted(projection.rglob("*.rs")):
        content = rust_file.read_text(encoding="utf-8", errors="ignore")
        relative = rust_file.relative_to(projection).as_posix()
        for match in RUST_INCLUDE.finditer(content):
            literal = match.group(1)
            if "docs/ssot/" not in literal and "pack/" not in literal:
                continue
            projected_target = (rust_file.parent / literal).resolve()
            source_file = source / relative
            source_target = (source_file.parent / literal).resolve()
            findings.append(
                {
                    "source_file": relative,
                    "literal": literal,
                    "target_role": "PRIVATE_SSOT_FIXTURE"
                    if "docs/ssot/" in literal
                    else "INTERNAL_PACK_FIXTURE",
                    "present_in_projection": projected_target.is_file(),
                    "present_in_source": source_target.is_file(),
                }
            )
    return sorted(findings, key=lambda item: (item["source_file"], item["literal"]))


def internal_marker_findings(projection: Path) -> dict[str, list[str]]:
    findings: dict[str, list[str]] = {}
    for path in bounded_files(projection):
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        relative = path.relative_to(projection).as_posix()
        for marker in INTERNAL_MARKERS:
            if marker in content:
                findings.setdefault(marker, []).append(relative)
    return {marker: sorted(paths) for marker, paths in sorted(findings.items())}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--projection", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    source = args.source.resolve()
    projection = args.projection.resolve()
    manifest_path = args.manifest.resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    roots = [
        path
        for role in manifest["roles"]
        if role["role"] == "PUBLIC_CONFORMANCE_SUBSET"
        for path in role.get("required_paths", [])
    ]

    projection_files = bounded_files(projection)
    marker_findings = internal_marker_findings(projection)
    fixture_findings = rust_private_fixture_references(source, projection)
    closure = recursive_conformance_closure(source, projection, roots)
    facade = {path: (projection / path).is_file() for path in FACADE}
    spec_pointer = projection / manifest["expected_public_spec"]["entrypoint"]
    spec_text = spec_pointer.read_text(encoding="utf-8") if spec_pointer.is_file() else ""
    spec_manifest = projection / manifest["expected_public_spec"]["required_manifest"]

    blockers: list[str] = []
    if manifest["expected_public_spec"]["marker"] not in spec_text or not spec_manifest.is_file():
        blockers.append("PUBLIC_SPEC_IDENTITY_MISMATCH")
    if any(not facade[path] for path in manifest["required_public_facade"]):
        blockers.append("PUBLIC_FACADE_RIGHTS_POLICY_FILES_MISSING")
    if closure["missing_in_source"] or closure["missing_in_projection"]:
        blockers.append("PUBLIC_CONFORMANCE_TRANSITIVE_CLOSURE_MISSING")
    if fixture_findings:
        blockers.append("PRIVATE_COMPILE_TIME_FIXTURE_DEPENDENCY")
    if marker_findings:
        blockers.append("INTERNAL_PATH_MARKERS_PRESENT")

    result = {
        "schema": "ddn.public_self_containment.audit.v1",
        "status": "PASS" if not blockers else "FAIL_CLOSED",
        "blockers": blockers,
        "source_head": "905efb4a1601b764e0f4f2554bef3fbd433172a3",
        "projection_file_count": len(projection_files),
        "projection_path_identity": "sha256:"
        + hashlib.sha256(
            "\n".join(path.relative_to(projection).as_posix() for path in projection_files).encode("utf-8")
        ).hexdigest(),
        "scope_manifest_sha256": sha256(manifest_path),
        "public_spec_marker_present": manifest["expected_public_spec"]["marker"] in spec_text,
        "public_spec_manifest_present": spec_manifest.is_file(),
        "facade": facade,
        "conformance": closure,
        "private_rust_fixture_references": fixture_findings,
        "internal_marker_findings": marker_findings,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({key: result[key] for key in ("status", "blockers")}, ensure_ascii=False))
    print(
        "conformance_closure="
        f"{closure['closure_count']} missing_projection={len(closure['missing_in_projection'])} "
        f"private_fixture_refs={len(fixture_findings)} marker_families={len(marker_findings)}"
    )


if __name__ == "__main__":
    main()
