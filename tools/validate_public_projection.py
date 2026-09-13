#!/usr/bin/env python3
"""Fail-closed validation for a deterministic public-source projection."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from typing import NoReturn


FULL_COMMIT = re.compile(r"[0-9a-f]{40}")
LOCAL_LINK = re.compile(r"\]\((\./[^)#]+)(?:#[^)]+)?\)")
INTERNAL_PATH = re.compile(
    r"(?ix)(?:"
    r"(?<![A-Z0-9_])[A-Z]:[\\/]"
    r"|\\\\(?:[?.][\\/]|[A-Z0-9._$-]+[\\/][A-Z0-9._$-]+(?:[\\/]|$))"
    r"|\bfile://(?:/[A-Z]:[\\/]|/|[^/\s]+/)"
    r"|/(?:home|users|mnt)/[^\r\n\"'<>\s]*(?:ddn|codex|build|work|official[-_]store)"
    r")"
)
PRIVATE_INCLUDE = re.compile(
    r"(?i)include_(?:str|bytes)!\s*\([^\r\n)]*(?:pack|work|docs[\\/]ssot)"
)
OFFICIAL_STORE = re.compile(
    r"(?ix)(?:[A-Z]:[\\/]|\\\\|/|\bfile://|\.\.?[\\/])"
    r"[^\r\n\"'<>\s]*official[-_]store(?:[\\/][^\r\n\"'<>\s]*)?"
)
VALIDATION_RECEIPT_NAME = "PUBLIC_VALIDATION_RECEIPT.detjson"
SECURITY_PATTERN_NAMES = {"INTERNAL_PATH", "PRIVATE_INCLUDE", "OFFICIAL_STORE"}
PATH_DIAGNOSTIC_CODES = {
    "E_PUBLIC_INTERNAL_ABSOLUTE_PATH",
    "E_PUBLIC_PRIVATE_FIXTURE_INCLUDE",
    "E_PUBLIC_OFFICIAL_STORE_PATH",
}
SEALED_SPEC_PROVENANCE_PATH = "publish/spec/v0.6.0/SPEC_MANIFEST_v0.6.0.md"
SEALED_EXTERNAL_PROVENANCE_TOKEN = re.compile(r"`external:[^`\r\n]+`")
RUST_CFG_TEST_TAIL = re.compile(
    r"(?m)^[ \t]*#\[cfg\(test\)\][ \t]*\r?\n[ \t]*(?:pub(?:\(crate\))?[ \t]+)?mod[ \t]+tests[ \t]*\{"
)
RETIRED_TEUL_SOURCE = PurePosixPath("tools/teul-cli")
RETIRED_TEUL_BINARIES = {"teul-cli", "teul-cli.exe"}


def fail(code: str, message: str) -> NoReturn:
    raise SystemExit(f"{code}: {message}")


def load_json(path: Path, missing_code: str) -> dict[str, object]:
    if not path.is_file():
        fail(missing_code, str(path))
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        fail("E_PUBLIC_PROJECTION_JSON", f"{path}: {error}")
    if not isinstance(value, dict):
        fail("E_PUBLIC_PROJECTION_JSON", f"object required: {path}")
    return value


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def output_files(root: Path) -> set[str]:
    files: set[str] = set()
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if ".git" in relative.parts:
            continue
        if path.is_symlink() or (path.exists() and not path.is_file() and not path.is_dir()):
            fail("E_PUBLIC_PROJECTION_NON_REGULAR", relative.as_posix())
        if path.is_file():
            files.add(relative.as_posix())
    return files


def reject_retired_teul_projection(relative: str, raw_entry: dict[str, object]) -> None:
    target = PurePosixPath(relative)
    source = PurePosixPath(str(raw_entry.get("source", "")))
    if (
        source == RETIRED_TEUL_SOURCE
        or RETIRED_TEUL_SOURCE in source.parents
        or target == RETIRED_TEUL_SOURCE
        or RETIRED_TEUL_SOURCE in target.parents
        or target.name.lower() in RETIRED_TEUL_BINARIES
    ):
        fail(
            "E_PUBLIC_TEUL_CLI_RETIRED",
            f"source={source.as_posix()} target={target.as_posix()}",
        )


def tree_identity(files: dict[str, object]) -> str:
    rows: list[bytes] = []
    for path, raw_entry in sorted(files.items()):
        if not isinstance(raw_entry, dict):
            fail("E_PUBLIC_PROJECTION_TREE_MANIFEST", f"invalid entry: {path}")
        rows.append(
            f"{path}\t{raw_entry.get('bytes')}\t{raw_entry.get('sha256')}\n".encode("utf-8")
        )
    return "sha256:" + sha256(b"".join(rows))


def validate_spec_links(projection: Path) -> None:
    current = projection / "publish" / "spec" / "CURRENT.md"
    if not current.is_file():
        fail("E_PUBLIC_SPEC_CURRENT_MISSING", str(current))
    text = current.read_text(encoding="utf-8")
    links = sorted({match.group(1)[2:] for match in LOCAL_LINK.finditer(text)})
    if not links:
        fail("E_PUBLIC_SPEC_CURRENT_LINK", "CURRENT.md has no local links")
    missing = [link for link in links if not (current.parent / Path(link)).is_file()]
    if missing:
        fail("E_PUBLIC_SPEC_CURRENT_LINK", ",".join(missing))


def omit_lines(text: str, omitted_lines: set[int]) -> str:
    lines = text.splitlines(keepends=True)
    return "".join(
        ("\n" if line.endswith("\n") else "") if number in omitted_lines else line
        for number, line in enumerate(lines, start=1)
    )


def python_structural_omissions(text: str, role: object) -> str:
    try:
        tree = ast.parse(text)
    except SyntaxError as error:
        fail("E_PUBLIC_PROJECTION_VALIDATOR_PARSE", str(error))
    omitted_lines: set[int] = set()
    if role == "PROJECTION_VALIDATOR":
        for node in tree.body:
            if not isinstance(node, ast.Assign) or len(node.targets) != 1:
                continue
            target = node.targets[0]
            if isinstance(target, ast.Name) and target.id in SECURITY_PATTERN_NAMES:
                omitted_lines.update(range(node.lineno, (node.end_lineno or node.lineno) + 1))
    elif role == "PROJECTION_VALIDATOR_TEST":
        for function in ast.walk(tree):
            if not isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if not function.name.startswith("test_"):
                continue
            is_path_red_fixture = any(
                isinstance(call, ast.Call)
                and isinstance(call.func, ast.Attribute)
                and call.func.attr == "assert_red"
                and any(
                    isinstance(argument, ast.Constant)
                    and argument.value in PATH_DIAGNOSTIC_CODES
                    for argument in call.args
                )
                for call in ast.walk(function)
            )
            if not is_path_red_fixture:
                continue
            for literal in ast.walk(function):
                if isinstance(literal, ast.Constant) and isinstance(
                    literal.value, (str, bytes)
                ):
                    omitted_lines.update(
                        range(literal.lineno, (literal.end_lineno or literal.lineno) + 1)
                    )
    return omit_lines(text, omitted_lines)


def security_scan_text(relative: str, role: object, data: bytes) -> str:
    text = data.decode("utf-8", errors="ignore")
    if relative == SEALED_SPEC_PROVENANCE_PATH and role == "PUBLIC_SPEC_EXACT_V0_6_0":
        text = SEALED_EXTERNAL_PROVENANCE_TOKEN.sub("`external:SEALED_CUSTODY_REFERENCE`", text)
    if relative.endswith(".py") and role in {
        "PROJECTION_VALIDATOR",
        "PROJECTION_VALIDATOR_TEST",
    }:
        try:
            text = python_structural_omissions(text, role)
        except SystemExit as error:
            fail("E_PUBLIC_PROJECTION_VALIDATOR_PARSE", f"{relative}: {error}")
    if relative.endswith(".rs") and role in {"PRODUCT_SOURCE", "CLI_SOURCE"}:
        matches = list(RUST_CFG_TEST_TAIL.finditer(text))
        if len(matches) == 1 and text.rstrip().endswith("}"):
            text = text[: matches[0].start()]
    return text


def validate_security(
    projection: Path, files: dict[str, object]
) -> dict[str, object]:
    scanned_roles: set[str] = set()
    scanned_files = 0
    for relative, raw_entry in sorted(files.items()):
        assert isinstance(raw_entry, dict)
        scanned_roles.add(str(raw_entry.get("role", "")))
        scanned_files += 1
        data = (projection / Path(relative)).read_bytes()
        text = security_scan_text(relative, raw_entry.get("role"), data)
        if INTERNAL_PATH.search(text):
            fail("E_PUBLIC_INTERNAL_ABSOLUTE_PATH", relative)
        if PRIVATE_INCLUDE.search(text):
            fail("E_PUBLIC_PRIVATE_FIXTURE_INCLUDE", relative)
        if OFFICIAL_STORE.search(text):
            fail("E_PUBLIC_OFFICIAL_STORE_PATH", relative)
    return {
        "TOTAL_PROJECTED_FILES": len(files),
        "SECURITY_SCANNED_FILES": scanned_files,
        "SCANNED_ROLE_COUNT": len(scanned_roles),
        "UNSCANNED_SECURITY_RELEVANT_FILES": len(files) - scanned_files,
    }


def expected_validation_receipt(
    *, source_commit: str, identity: str, file_count: int,
    required_roles: list[str], spec_links_required: bool,
    validator_tool_identity: str,
    security_scan: dict[str, object],
) -> dict[str, object]:
    return {
        **security_scan,
        "file_count": file_count,
        "public_tree_identity": identity,
        "required_roles": sorted(set(required_roles)),
        "schema": "ddn.public_projection_validation_receipt.v1",
        "source_commit": source_commit,
        "spec_links_required": spec_links_required,
        "status": "PUBLIC_PROJECTION_VALIDATION_PASS",
        "validator_tool_identity": validator_tool_identity,
    }


def projected_validator_identity(files: dict[str, object]) -> str:
    identities = [
        "sha256:" + str(raw_entry.get("sha256"))
        for raw_entry in files.values()
        if isinstance(raw_entry, dict)
        and raw_entry.get("role") == "PROJECTION_VALIDATOR"
    ]
    if len(identities) != 1 or identities[0] == "sha256:None":
        fail(
            "E_PUBLIC_VALIDATION_TOOL_IDENTITY",
            f"exactly one projected validator required: {identities}",
        )
    return identities[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--projection", required=True, type=Path)
    parser.add_argument("--receipt-dir", required=True, type=Path)
    parser.add_argument("--require-role", action="append", default=[])
    parser.add_argument("--require-spec-links", action="store_true")
    validation_mode = parser.add_mutually_exclusive_group()
    validation_mode.add_argument("--write-validation-receipt", action="store_true")
    validation_mode.add_argument("--require-validation-receipt", action="store_true")
    args = parser.parse_args()

    projection = args.projection.resolve()
    receipt_dir = args.receipt_dir.resolve()
    receipt = load_json(
        receipt_dir / "PUBLIC_PROJECTION_RECEIPT.detjson",
        "E_PUBLIC_PROJECTION_RECEIPT_MISSING",
    )
    tree = load_json(
        receipt_dir / "PUBLIC_TREE_MANIFEST.detjson",
        "E_PUBLIC_TREE_MANIFEST_MISSING",
    )
    source_commit = str(receipt.get("source_commit", ""))
    if FULL_COMMIT.fullmatch(source_commit) is None:
        fail("E_PUBLIC_PROJECTION_SOURCE_COMMIT", source_commit)
    files = tree.get("files")
    if not isinstance(files, dict):
        fail("E_PUBLIC_PROJECTION_TREE_MANIFEST", "files object required")
    expected = set(files)
    actual = output_files(projection)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        fail("E_PUBLIC_PROJECTION_FILE_SET", f"missing={missing};extra={extra}")

    roles: set[str] = set()
    for relative, raw_entry in sorted(files.items()):
        if not isinstance(raw_entry, dict):
            fail("E_PUBLIC_PROJECTION_TREE_MANIFEST", relative)
        reject_retired_teul_projection(relative, raw_entry)
        data = (projection / Path(relative)).read_bytes()
        if len(data) != raw_entry.get("bytes") or sha256(data) != raw_entry.get("sha256"):
            fail("E_PUBLIC_PROJECTION_ARTIFACT_HASH", relative)
        roles.add(str(raw_entry.get("role", "")))
    for role in args.require_role:
        if role not in roles:
            fail("E_PUBLIC_PROJECTION_REQUIRED_ROLE", role)

    identity = tree_identity(files)
    for owner in (tree, receipt):
        claimed = owner.get("public_tree_identity", owner.get("output_public_tree_identity"))
        if claimed != identity:
            fail("E_PUBLIC_PROJECTION_TREE_IDENTITY", f"{claimed} != {identity}")
    if receipt.get("included_path_role_closure_identity") != identity:
        fail("E_PUBLIC_PROJECTION_TREE_IDENTITY", "role closure identity mismatch")
    security_scan = validate_security(projection, files)
    if args.require_spec_links:
        validate_spec_links(projection)
    validation = expected_validation_receipt(
        source_commit=source_commit,
        identity=identity,
        file_count=len(files),
        required_roles=args.require_role,
        spec_links_required=args.require_spec_links,
        validator_tool_identity=(
            projected_validator_identity(files)
            if args.write_validation_receipt or args.require_validation_receipt
            else "sha256:" + sha256(Path(__file__).read_bytes())
        ),
        security_scan=security_scan,
    )
    validation_bytes = canonical_json_bytes(validation)
    validation_identity = "sha256:" + sha256(validation_bytes)
    validation_path = receipt_dir / VALIDATION_RECEIPT_NAME
    if args.write_validation_receipt:
        validation_path.write_bytes(validation_bytes)
        receipt["validation_receipt_identity"] = validation_identity
        (receipt_dir / "PUBLIC_PROJECTION_RECEIPT.detjson").write_bytes(
            canonical_json_bytes(receipt)
        )
    elif args.require_validation_receipt:
        actual_validation = load_json(
            validation_path, "E_PUBLIC_VALIDATION_RECEIPT_MISSING"
        )
        if canonical_json_bytes(actual_validation) != validation_bytes:
            fail("E_PUBLIC_VALIDATION_RECEIPT_MISMATCH", str(validation_path))
        if receipt.get("validation_receipt_identity") != validation_identity:
            fail(
                "E_PUBLIC_VALIDATION_RECEIPT_IDENTITY",
                f"{receipt.get('validation_receipt_identity')} != {validation_identity}",
            )
    print(
        f"PUBLIC_PROJECTION_VALIDATION_PASS files={len(files)} identity={identity} "
        f"validation_receipt_identity={validation_identity}"
    )


if __name__ == "__main__":
    main()
