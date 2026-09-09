#!/usr/bin/env python3
"""Compute a bounded public conformance script and fixture closure.

This is a read-only candidate audit. It intentionally does not claim that
static discovery proves runtime completeness; unresolved dynamic references are
reported fail-closed.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path, PurePosixPath
import re


TEST_REF = re.compile(r"tests/[A-Za-z0-9_./-]+\.(?:py|mjs|js|json)")
REPO_REF = re.compile(
    r"(?:core|lang|numeric|proof|symbolic|tool|tools|solutions|scripts|pack|publish|examples)/"
    r"[A-Za-z0-9_./-]+"
)
PACK_REF = re.compile(r"(?<![A-Za-z0-9_])pack/([A-Za-z0-9_.-]+)")
JS_IMPORT = re.compile(
    r"(?:from\s+|import\s*\(|require\s*\()\s*['\"](\.{1,2}/[^'\"]+)['\"]"
)
TEXT_SUFFIXES = {
    ".css", ".ddn", ".detjson", ".html", ".js", ".json", ".md",
    ".mjs", ".py", ".rs", ".toml", ".ts", ".txt", ".yaml", ".yml",
}
EXECUTABLE_SUFFIXES = {".py", ".js", ".mjs"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize(value: str) -> str:
    return PurePosixPath(value.replace("\\", "/")).as_posix().lstrip("./")


def existing_module(source: Path, owner: str, module: str) -> str | None:
    if module.startswith((".", "_")) or "." not in module:
        candidate = PurePosixPath(owner).parent / (module.replace(".", "/") + ".py")
        relative = normalize(candidate.as_posix())
        if (source / relative).is_file():
            return relative
    return None


def python_path_parts(node: ast.AST) -> list[str] | None:
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        left = python_path_parts(node.left)
        right = python_path_parts(node.right)
        if left is None or right is None:
            return None
        return left + right
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return [node.value]
    if isinstance(node, ast.Name) and node.id.lower() in {
        "root", "repo", "repo_root", "root_dir", "project_root"
    }:
        return []
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "Path"
        and len(node.args) == 1
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
    ):
        return [node.args[0].value]
    return None


def resolve_js_import(source: Path, owner: str, literal: str) -> str | None:
    base = PurePosixPath(owner).parent
    candidate = normalize((base / literal).as_posix())
    options = [candidate]
    if not PurePosixPath(candidate).suffix:
        options.extend(candidate + suffix for suffix in (".js", ".mjs", ".json"))
        options.extend(f"{candidate}/index{suffix}" for suffix in (".js", ".mjs"))
    return next((path for path in options if (source / path).is_file()), None)


def discover_file(
    source: Path, relative: str
) -> tuple[set[str], set[str], set[str], set[str]]:
    """Return script deps, pack roots, other repo paths, dynamic unresolved notes."""
    path = source / relative
    if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
        return set(), set(), set(), set()
    text = path.read_text(encoding="utf-8", errors="ignore")
    if path.suffix.lower() not in EXECUTABLE_SUFFIXES:
        return set(), set(), set(), set()
    scripts = set(TEST_REF.findall(text))
    packs: set[str] = set()
    other = {
        normalize(match.rstrip(".,;:)]}`"))
        for match in REPO_REF.findall(text)
        if "{" not in match and (source / normalize(match.rstrip(".,;:)]}`"))).exists()
    }
    unresolved: set[str] = set()

    if path.suffix.lower() == ".py":
        try:
            tree = ast.parse(text, filename=relative)
        except SyntaxError as exc:
            unresolved.add(f"PYTHON_PARSE_ERROR:{relative}:{exc.lineno}")
            return scripts, packs, other, unresolved
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                target = existing_module(source, relative, node.module)
                if target:
                    scripts.add(target)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    target = existing_module(source, relative, alias.name)
                    if target:
                        scripts.add(target)
            parts = python_path_parts(node)
            if parts:
                joined = normalize("/".join(part.strip("/") for part in parts if part))
                if joined.startswith("tests/") and (source / joined).is_file():
                    scripts.add(joined)
                elif joined.startswith("pack/"):
                    bits = PurePosixPath(joined).parts
                    if len(bits) >= 2:
                        packs.add("/".join(bits[:2]))
                elif joined.startswith(("scripts/", "tools/", "solutions/", "lang/", "tool/")):
                    other.add(joined)
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                match = PACK_REF.search(node.value)
                if match and (source / "pack" / match.group(1)).is_dir():
                    packs.add(f"pack/{match.group(1)}")
            if isinstance(node, (ast.List, ast.Tuple)):
                values = [
                    item.value for item in node.elts
                    if isinstance(item, ast.Constant) and isinstance(item.value, str)
                ]
                for index, value in enumerate(values[:-1]):
                    if value == "tests/run_pack_golden.py":
                        name = values[index + 1]
                        if (
                            re.fullmatch(r"[A-Za-z0-9_.-]+", name)
                            and not name.startswith("-")
                            and (source / "pack" / name).is_dir()
                        ):
                            packs.add(f"pack/{name}")
                if relative == "tests/run_seamgrim_wasm_smoke.py":
                    for value in values:
                        if value.startswith("seamgrim_") or value.startswith("observation_"):
                            candidate = source / "pack" / value
                            if candidate.is_dir():
                                packs.add(f"pack/{value}")
    elif path.suffix.lower() in {".js", ".mjs"}:
        for literal in JS_IMPORT.findall(text):
            target = resolve_js_import(source, relative, literal)
            if target:
                scripts.add(target)
            else:
                unresolved.add(f"MISSING_JS_IMPORT:{relative}:{literal}")
        for name in PACK_REF.findall(text):
            if (source / "pack" / name).is_dir():
                packs.add(f"pack/{name}")
    return scripts, packs, other, unresolved


def role(path: str) -> str:
    if path.startswith("tests/"):
        return "CONFORMANCE_SCRIPT_OR_RUNNER"
    if path.startswith("pack/"):
        return "CONFORMANCE_FIXTURE_OR_ORACLE"
    if path.startswith("scripts/"):
        return "BUILD_OR_VALIDATION_SCRIPT"
    if path.startswith(("core/", "lang/", "numeric/", "proof/", "symbolic/", "tool/", "tools/")):
        return "LANGUAGE_RUNTIME_OR_CLI_SOURCE"
    if path.startswith("solutions/"):
        return "WORKBENCH_PRODUCT_SOURCE"
    if path.startswith("publish/"):
        return "PUBLIC_SPEC_OR_DOC"
    return "OTHER"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--projection", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    source = args.source.resolve()
    projection = args.projection.resolve()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    roots = sorted(
        path
        for entry in manifest["roles"]
        if entry["role"] == "PUBLIC_CONFORMANCE_SUBSET"
        for path in entry.get("required_paths", [])
    )

    pending = list(roots)
    seen: set[str] = set()
    edges: set[tuple[str, str, str]] = set()
    pack_roots: set[str] = set()
    other_paths: set[str] = set()
    unresolved: set[str] = set()
    while pending:
        relative = pending.pop(0)
        if relative in seen:
            continue
        seen.add(relative)
        deps, packs, others, dynamic = discover_file(source, relative)
        pack_roots.update(packs)
        other_paths.update(others)
        unresolved.update(dynamic)
        for dep in sorted(deps):
            edges.add((relative, dep, "SCRIPT_OR_IMPORT"))
            if dep not in seen:
                pending.append(dep)
        pending.sort()

    pack_rows: list[dict[str, object]] = []
    fixture_files: set[str] = set()
    for pack_root in sorted(pack_roots):
        root = source / pack_root
        files = sorted(path for path in root.rglob("*") if path.is_file()) if root.is_dir() else []
        relative_files = [path.relative_to(source).as_posix() for path in files]
        fixture_files.update(relative_files)
        pack_rows.append(
            {
                "path": pack_root,
                "present_in_source": root.is_dir(),
                "file_count": len(files),
                "raw_bytes": sum(path.stat().st_size for path in files),
                "present_in_projection_count": sum(
                    (projection / relative).is_file() for relative in relative_files
                ),
                "files": relative_files,
            }
        )

    required_files = sorted(seen | fixture_files | {
        path for path in other_paths if (source / path).is_file()
    })
    missing_source = sorted(path for path in required_files if not (source / path).is_file())
    missing_projection = sorted(path for path in required_files if not (projection / path).is_file())
    rows = [
        {
            "path": path,
            "role": role(path),
            "bytes": (source / path).stat().st_size if (source / path).is_file() else None,
            "sha256": sha256(source / path) if (source / path).is_file() else None,
            "present_in_projection": (projection / path).is_file(),
        }
        for path in required_files
    ]
    role_counts: dict[str, int] = {}
    for row in rows:
        role_counts[str(row["role"])] = role_counts.get(str(row["role"]), 0) + 1

    root_impact: list[dict[str, object]] = []
    for root in roots:
        local_pending = [root]
        local_seen: set[str] = set()
        while local_pending:
            relative = local_pending.pop(0)
            if relative in local_seen:
                continue
            local_seen.add(relative)
            deps, _, _, _ = discover_file(source, relative)
            local_pending.extend(sorted(deps - local_seen))
        root_impact.append({
            "root": root,
            "script_closure_count": len(local_seen),
            "transitive_script_dependencies": sorted(local_seen - {root}),
        })

    umbrella_roots = sorted(
        str(row["root"]) for row in root_impact if int(row["script_closure_count"]) > 10
    )
    leaf_root_rows = [row for row in root_impact if str(row["root"]) not in umbrella_roots]
    leaf_scripts: set[str] = set()
    for row in leaf_root_rows:
        leaf_scripts.add(str(row["root"]))
        leaf_scripts.update(str(path) for path in row["transitive_script_dependencies"])
    leaf_packs: set[str] = set()
    leaf_other: set[str] = set()
    leaf_unresolved: set[str] = set()
    for relative in sorted(leaf_scripts):
        _, packs, others, dynamic = discover_file(source, relative)
        leaf_packs.update(packs)
        leaf_other.update(others)
        leaf_unresolved.update(dynamic)
    leaf_fixture_files = {
        path.relative_to(source).as_posix()
        for pack_root in leaf_packs
        if (source / pack_root).is_dir()
        for path in (source / pack_root).rglob("*")
        if path.is_file()
    }
    leaf_required_files = sorted(
        leaf_scripts
        | leaf_fixture_files
        | {path for path in leaf_other if (source / path).is_file()}
    )

    result = {
        "schema": "ddn.public_conformance.bounded_closure_audit.v1",
        "status": "FAIL_CLOSED" if missing_source or missing_projection or unresolved else "PASS",
        "roots": roots,
        "root_count": len(roots),
        "root_impact": sorted(root_impact, key=lambda row: (-int(row["script_closure_count"]), str(row["root"]))),
        "umbrella_root_analysis": {
            "classification_rule": "SCRIPT_CLOSURE_COUNT_GT_10",
            "umbrella_roots": umbrella_roots,
            "leaf_roots": sorted(str(row["root"]) for row in leaf_root_rows),
            "leaf_script_closure_count": len(leaf_scripts),
            "leaf_pack_roots": sorted(leaf_packs),
            "leaf_required_file_count": len(leaf_required_files),
            "leaf_missing_in_projection": sorted(
                path for path in leaf_required_files if not (projection / path).is_file()
            ),
            "leaf_unresolved_dynamic_references": sorted(leaf_unresolved),
            "candidate_only_not_owner_bound_manifest_rewrite": True,
        },
        "script_closure_count": len(seen),
        "script_edges": [
            {"from": source_path, "to": target, "kind": kind}
            for source_path, target, kind in sorted(edges)
        ],
        "pack_root_count": len(pack_rows),
        "pack_roots": pack_rows,
        "required_file_count": len(required_files),
        "required_raw_bytes": sum(
            (source / path).stat().st_size for path in required_files if (source / path).is_file()
        ),
        "role_counts": dict(sorted(role_counts.items())),
        "required_files": rows,
        "missing_in_source": missing_source,
        "missing_in_projection": missing_projection,
        "other_repo_path_references": sorted(other_paths),
        "unresolved_dynamic_references": sorted(unresolved),
        "static_completeness_claim": False,
        "static_completeness_reason": "DYNAMIC_RUNTIME_PATHS_REQUIRE_FRESH_PUBLIC_REPOSITORY_EXECUTION",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    digest = hashlib.sha256(args.out.read_bytes()).hexdigest()
    print(
        f"status={result['status']} scripts={len(seen)} packs={len(pack_rows)} "
        f"files={len(required_files)} missing_projection={len(missing_projection)} "
        f"unresolved={len(unresolved)} sha256={digest}"
    )


if __name__ == "__main__":
    main()
