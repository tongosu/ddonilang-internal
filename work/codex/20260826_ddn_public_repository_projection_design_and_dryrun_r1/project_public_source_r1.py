#!/usr/bin/env python3
"""Create a deterministic, non-authoritative public-source preview from a Git commit."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import tarfile


def fail(message: str) -> "NoReturn":
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
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def normalize_relative(value: str, field: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        fail(f"unsafe {field}: {value!r}")
    return path


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
    if output == repo or repo in output.parents:
        fail("output must be outside the source worktree")
    if output.exists() and any(output.iterdir()):
        fail("output already exists and is not empty")
    if receipt_dir.exists() and any(receipt_dir.iterdir()):
        fail("receipt directory already exists and is not empty")

    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes.decode("utf-8"))
    commit = str(manifest["source_commit"])
    commit_type = git(repo, "cat-file", "-t", commit)
    if commit_type != "commit":
        fail(f"source identity is not a commit: {commit_type}")
    resolved_commit = str(git(repo, "rev-parse", f"{commit}^{{commit}}"))
    rules = manifest["rules"]
    if not isinstance(rules, list) or not rules:
        fail("manifest has no rules")

    archive_roots = sorted({str(rule["source"]) for rule in rules})
    archive = git(repo, "archive", "--format=tar", resolved_commit, "--", *archive_roots, binary=True)
    assert isinstance(archive, bytes)
    matched = [0] * len(rules)
    projected: dict[str, dict[str, object]] = {}
    payloads: dict[str, bytes] = {}

    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as tar:
        for member in tar.getmembers():
            if member.isdir():
                continue
            if not member.isfile():
                fail(f"non-regular archive member rejected: {member.name}")
            source_path = normalize_relative(member.name, "archive path")
            selections: list[tuple[int, PurePosixPath, dict[str, object]]] = []
            for index, rule in enumerate(rules):
                target_path = match_rule(source_path, rule)
                if target_path is not None:
                    selections.append((index, target_path, rule))
            for index, target_path, rule in selections:
                matched[index] += 1
                target_key = target_path.as_posix()
                if target_key in projected:
                    fail(f"duplicate output path: {target_key}")
                extracted = tar.extractfile(member)
                if extracted is None:
                    fail(f"failed to read archive member: {member.name}")
                data = extracted.read()
                payloads[target_key] = data
                projected[target_key] = {
                    "bytes": len(data),
                    "role": str(rule["role"]),
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "source": source_path.as_posix(),
                }

    for index, rule in enumerate(rules):
        required = bool(rule.get("required", False))
        if required and matched[index] == 0:
            fail(f"required rule matched no file: {rule['source']}")
        if rule["kind"] == "file" and matched[index] != 1:
            fail(f"file rule must match exactly once: {rule['source']} ({matched[index]})")

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
    tree_identity = "sha256:" + hashlib.sha256(b"".join(tree_lines)).hexdigest()
    manifest_identity = "sha256:" + hashlib.sha256(manifest_bytes).hexdigest()
    projection_tool_identity = "sha256:" + hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    tree_manifest = {
        "schema": "ddn.public_tree_manifest.preview.v1",
        "file_count": len(projected),
        "files": projected,
        "public_tree_identity": tree_identity,
    }
    receipt = {
        "schema": "ddn.public_projection_receipt.preview.v1",
        "status": "NONAUTHORITATIVE_R1_DRY_RUN_ONLY",
        "source_commit": resolved_commit,
        "source_tree_identity": "git-tree:" + str(git(repo, "show", "-s", "--format=%T", resolved_commit)),
        "projection_policy_identity": manifest_identity,
        "projection_tool_identity": projection_tool_identity,
        "projection_manifest_identity": manifest_identity,
        "included_path_role_closure_identity": tree_identity,
        "public_spec_identity": "Language_SPEC_v0.5.0_docs_first",
        "output_public_tree_identity": tree_identity,
        "validation_receipt_identity": "OPEN",
    }
    (receipt_dir / "PUBLIC_TREE_MANIFEST.detjson").write_bytes(canonical_json_bytes(tree_manifest))
    (receipt_dir / "PUBLIC_PROJECTION_RECEIPT.detjson").write_bytes(canonical_json_bytes(receipt))
    print(json.dumps({"file_count": len(projected), "public_tree_identity": tree_identity, "source_commit": resolved_commit}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
