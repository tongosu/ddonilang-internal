#!/usr/bin/env python3
"""Project a deterministic public-source tree from one clean Git commit.

The manifest is the only path-selection authority. Files are enumerated with
``git ls-tree`` and read as exact blobs with ``git cat-file``; working-tree
bytes and checkout filters are never projection inputs. The tool rejects
missing rules, duplicate output paths, symlinks and unsafe paths, then emits
canonical manifests and a receipt outside the source worktree.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
from typing import NoReturn


TOOL_SCHEMA = "ddn.public_projection_tool.v1"
RETIRED_TEUL_SOURCE = PurePosixPath("tools/teul-cli")
RETIRED_TEUL_BINARIES = {"teul-cli", "teul-cli.exe"}


def fail(message: str) -> NoReturn:
    raise SystemExit(f"ERROR: {message}")


def git(repo: Path, *args: str, binary: bool = False) -> bytes | str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        fail(result.stderr.decode("utf-8", errors="replace").strip())
    return result.stdout if binary else result.stdout.decode("utf-8").strip()


def canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def sha256_identity(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def projected_tool_identity(projected: dict[str, dict[str, object]]) -> str:
    identities = [
        "sha256:" + str(entry["sha256"])
        for entry in projected.values()
        if entry.get("role") == "PROJECTION_TOOL"
    ]
    if len(identities) == 1:
        return identities[0]
    return sha256_identity(Path(__file__).read_bytes())


def normalize_relative(value: str, field: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        fail(f"unsafe {field}: {value!r}")
    return path


def reject_retired_teul_projection(source: PurePosixPath, target: PurePosixPath) -> None:
    if source == RETIRED_TEUL_SOURCE or RETIRED_TEUL_SOURCE in source.parents:
        fail(f"E_PUBLIC_TEUL_CLI_RETIRED: source={source.as_posix()}")
    if (
        target == RETIRED_TEUL_SOURCE
        or RETIRED_TEUL_SOURCE in target.parents
        or target.name.lower() in RETIRED_TEUL_BINARIES
    ):
        fail(f"E_PUBLIC_TEUL_CLI_RETIRED: target={target.as_posix()}")


def match_rule(path: PurePosixPath, rule: dict[str, object]) -> PurePosixPath | None:
    source = normalize_relative(str(rule["source"]), "source")
    target = normalize_relative(str(rule["target"]), "target")
    if rule["kind"] == "file":
        return target if path == source else None
    if rule["kind"] != "tree":
        fail(f"unsupported rule kind: {rule['kind']!r}")
    if path == source:
        return target
    try:
        relative = path.relative_to(source)
    except ValueError:
        return None
    return target / relative


def transform_blob(data: bytes, rule: dict[str, object], source: PurePosixPath) -> bytes:
    """Apply an exact, manifest-owned public projection transform."""
    raw_paths = rule.get("json_remove_paths")
    if raw_paths is None:
        return data
    if rule["kind"] != "file":
        fail(f"json_remove_paths requires a file rule: {source.as_posix()}")
    if not isinstance(raw_paths, list) or not raw_paths:
        fail(f"json_remove_paths must be a non-empty list: {source.as_posix()}")
    try:
        value = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        fail(f"json_remove_paths requires UTF-8 JSON: {source.as_posix()}: {error}")
    if not isinstance(value, dict):
        fail(f"json_remove_paths requires a JSON object: {source.as_posix()}")
    for raw_path in raw_paths:
        if (
            not isinstance(raw_path, list)
            or not raw_path
            or any(not isinstance(part, str) or not part for part in raw_path)
        ):
            fail(f"invalid json_remove_paths entry: {raw_path!r}")
        owner: object = value
        for part in raw_path[:-1]:
            if not isinstance(owner, dict) or part not in owner:
                fail(f"json_remove_paths path missing: {'.'.join(raw_path)}")
            owner = owner[part]
        leaf = raw_path[-1]
        if not isinstance(owner, dict) or leaf not in owner:
            fail(f"json_remove_paths path missing: {'.'.join(raw_path)}")
        del owner[leaf]
    return canonical_json_bytes(value)


def apply_exact_blob_replacements(
    data: bytes, replacements: list[tuple[bytes, bytes, int]], source: PurePosixPath
) -> bytes:
    """Apply exact-count, manifest-owned byte replacements to one projected blob."""
    transformed = data
    for old, new, expected_count in replacements:
        actual_count = transformed.count(old)
        if actual_count != expected_count:
            fail(
                "exact_blob_replacements count mismatch: "
                f"{source.as_posix()} expected={expected_count} actual={actual_count}"
            )
        transformed = transformed.replace(old, new)
    return transformed


def parse_exact_blob_replacements(
    manifest: dict[str, object],
) -> dict[PurePosixPath, list[tuple[bytes, bytes, int]]]:
    raw_mapping = manifest.get("exact_blob_replacements", {})
    if not isinstance(raw_mapping, dict):
        fail("exact_blob_replacements must be an object")
    parsed: dict[PurePosixPath, list[tuple[bytes, bytes, int]]] = {}
    for raw_source, raw_entries in raw_mapping.items():
        source = normalize_relative(str(raw_source), "exact replacement source")
        if not isinstance(raw_entries, list) or not raw_entries:
            fail(f"exact_blob_replacements must be non-empty: {source.as_posix()}")
        entries: list[tuple[bytes, bytes, int]] = []
        for raw_entry in raw_entries:
            if not isinstance(raw_entry, dict):
                fail(f"invalid exact_blob_replacements entry: {raw_entry!r}")
            old = raw_entry.get("old")
            new = raw_entry.get("new")
            count = raw_entry.get("count")
            if (
                not isinstance(old, str)
                or not old
                or not isinstance(new, str)
                or old == new
                or not isinstance(count, int)
                or isinstance(count, bool)
                or count <= 0
            ):
                fail(f"invalid exact_blob_replacements entry: {raw_entry!r}")
            entries.append((old.encode("utf-8"), new.encode("utf-8"), count))
        parsed[source] = entries
    return parsed


def ensure_empty_external_directory(path: Path, repo: Path, label: str) -> None:
    resolved = path.resolve()
    if resolved == repo or repo in resolved.parents:
        fail(f"{label} must be outside the source worktree")
    if resolved.exists() and any(resolved.iterdir()):
        fail(f"{label} already exists and is not empty")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--receipt-dir", required=True, type=Path)
    args = parser.parse_args()

    repo = args.repo.resolve()
    manifest_path = args.manifest.resolve()
    output = args.output.resolve()
    receipt_dir = args.receipt_dir.resolve()
    ensure_empty_external_directory(output, repo, "output")
    ensure_empty_external_directory(receipt_dir, repo, "receipt directory")
    if output == receipt_dir:
        fail("output and receipt directory must be distinct")

    manifest_bytes = manifest_path.read_bytes()
    try:
        manifest = json.loads(manifest_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        fail(f"invalid UTF-8 JSON manifest: {error}")
    if not isinstance(manifest, dict):
        fail("manifest root must be an object")
    exact_replacements = parse_exact_blob_replacements(manifest)
    commit = str(manifest.get("source_commit", ""))
    if not commit:
        fail("manifest source_commit is required")
    if git(repo, "cat-file", "-t", commit) != "commit":
        fail("source identity is not a commit")
    resolved_commit = str(git(repo, "rev-parse", f"{commit}^{{commit}}"))
    if commit != resolved_commit:
        fail("source_commit must be the exact full commit identity")

    rules = manifest.get("rules")
    if not isinstance(rules, list) or not rules:
        fail("manifest has no rules")
    for index, rule in enumerate(rules):
        if not isinstance(rule, dict):
            fail(f"rule {index} is not an object")
        for field in ("kind", "source", "target", "role"):
            if field not in rule:
                fail(f"rule {index} missing field: {field}")
        source = normalize_relative(str(rule["source"]), "source")
        target = normalize_relative(str(rule["target"]), "target")
        reject_retired_teul_projection(source, target)

    source_roots = sorted({str(rule["source"]) for rule in rules})
    tree_listing = git(
        repo,
        "ls-tree",
        "-r",
        "-z",
        "--full-tree",
        resolved_commit,
        "--",
        *source_roots,
        binary=True,
    )
    assert isinstance(tree_listing, bytes)
    matched = [0] * len(rules)
    projected: dict[str, dict[str, object]] = {}
    payloads: dict[str, bytes] = {}
    replaced_sources: set[PurePosixPath] = set()

    for record in tree_listing.split(b"\0"):
        if not record:
            continue
        try:
            header, path_bytes = record.split(b"\t", 1)
            mode, object_type, object_id = header.split(b" ", 2)
            source_text = path_bytes.decode("utf-8")
        except (ValueError, UnicodeDecodeError) as error:
            fail(f"invalid ls-tree record: {error}")
        if mode not in (b"100644", b"100755") or object_type != b"blob":
            fail(f"non-regular tree entry rejected: {source_text}")
        source_path = normalize_relative(source_text, "tree path")
        data = git(repo, "cat-file", "blob", object_id.decode("ascii"), binary=True)
        assert isinstance(data, bytes)
        for index, rule in enumerate(rules):
            target_path = match_rule(source_path, rule)
            if target_path is None:
                continue
            projected_data = transform_blob(data, rule, source_path)
            replacements = exact_replacements.get(source_path)
            if replacements is not None:
                projected_data = apply_exact_blob_replacements(
                    projected_data, replacements, source_path
                )
                replaced_sources.add(source_path)
            matched[index] += 1
            target_key = target_path.as_posix()
            if target_key in projected:
                fail(f"duplicate output path: {target_key}")
            payloads[target_key] = projected_data
            projected[target_key] = {
                "bytes": len(projected_data),
                "role": str(rule["role"]),
                "sha256": hashlib.sha256(projected_data).hexdigest(),
                "source": source_path.as_posix(),
            }

    for index, rule in enumerate(rules):
        required = bool(rule.get("required", False))
        if required and matched[index] == 0:
            fail(f"required rule matched no file: {rule['source']}")
        if rule["kind"] == "file" and matched[index] != 1:
            fail(f"file rule must match exactly once: {rule['source']} ({matched[index]})")
    missing_replacement_sources = sorted(
        source.as_posix() for source in set(exact_replacements) - replaced_sources
    )
    if missing_replacement_sources:
        fail(
            "exact_blob_replacements source was not projected: "
            + ",".join(missing_replacement_sources)
        )

    output.mkdir(parents=True, exist_ok=True)
    receipt_dir.mkdir(parents=True, exist_ok=True)
    for relative, data in sorted(payloads.items()):
        destination = output.joinpath(*PurePosixPath(relative).parts)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)

    tree_lines = [
        f"{path}\t{entry['bytes']}\t{entry['sha256']}\n".encode("utf-8")
        for path, entry in sorted(projected.items())
    ]
    tree_identity = sha256_identity(b"".join(tree_lines))
    manifest_identity = sha256_identity(manifest_bytes)
    projection_tool_identity = projected_tool_identity(projected)
    tree_manifest = {
        "schema": "ddn.public_tree_manifest.v1",
        "file_count": len(projected),
        "files": projected,
        "public_tree_identity": tree_identity,
    }
    receipt = {
        "schema": "ddn.public_projection_receipt.v1",
        "status": str(manifest.get("status", "CANDIDATE_NOT_PUBLICATION_AUTHORIZED")),
        "source_commit": resolved_commit,
        "source_tree_identity": "git-tree:"
        + str(git(repo, "show", "-s", "--format=%T", resolved_commit)),
        "projection_policy_identity": manifest_identity,
        "projection_tool_identity": projection_tool_identity,
        "projection_manifest_identity": manifest_identity,
        "included_path_role_closure_identity": tree_identity,
        "public_spec_identity": str(manifest.get("public_spec_identity", "OPEN")),
        "output_public_tree_identity": tree_identity,
        "validation_receipt_identity": str(
            manifest.get("validation_receipt_identity", "OPEN")
        ),
        "tool_schema": TOOL_SCHEMA,
    }
    (receipt_dir / "PUBLIC_TREE_MANIFEST.detjson").write_bytes(
        canonical_json_bytes(tree_manifest)
    )
    (receipt_dir / "PUBLIC_PROJECTION_RECEIPT.detjson").write_bytes(
        canonical_json_bytes(receipt)
    )
    print(
        json.dumps(
            {
                "file_count": len(projected),
                "public_tree_identity": tree_identity,
                "source_commit": resolved_commit,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
