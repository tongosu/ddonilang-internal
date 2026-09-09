#!/usr/bin/env python3
"""Generate the read-only V1 CLI identity audit artifacts.

This generator inventories existing source.  It does not select a public CLI,
remove a command, or modify product code.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "work" / "codex" / "20260827_ddn_v1_cli01_official_cli_identity_audit_i1"

TOOL_CORE = {"run", "run-summary", "test", "canon"}
TOOL_SHARED = {"geoul", "query"}
TOOL_INTERNAL = {"ai", "prompt", "preprocess-ai", "build-schema"}

TEUL_CORE = {
    "project-normalize",
    "project-discover",
    "project-graph",
    "project-symbols",
    "project-lock",
    "project-run",
    "run",
    "currentline-run",
    "view",
    "check",
    "test",
    "build",
    "lint",
    "repl",
    "canon",
}
TEUL_SHARED = {
    "historical-async-migration-evidence",
    "deterministic-debug",
    "world-diff",
    "asset",
    "bogae",
    "dotbogi",
    "bdl",
    "replay",
    "geoul",
    "patch",
    "scan",
    "gaji",
    "numeric",
    "symbolic",
    "proof",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def kebab(variant: str) -> str:
    return re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", variant).lower()


def tool_commands() -> list[dict[str, object]]:
    path = ROOT / "tool" / "src" / "main.rs"
    text = path.read_text(encoding="utf-8")
    main = text[text.index("fn main()") :]
    test_at = main.find("#[cfg(test)]")
    if test_at >= 0:
        main = main[:test_at]
    names = sorted(set(re.findall(r'Some\("([a-z0-9_-]+)"\)\s*=>', main)))
    rows = []
    for name in names:
        if name in TOOL_CORE:
            disposition = "KEEP_AS_OFFICIAL_CORE_CANDIDATE"
        elif name in TOOL_SHARED:
            disposition = "MOVE_SEMANTICS_TO_SHARED_LIBRARY_BEFORE_PUBLIC_EXPOSURE"
        elif name in TOOL_INTERNAL:
            disposition = "PRESERVE_INTERNAL_PENDING_V1_MEMBERSHIP"
        else:
            disposition = "PRESERVE_PACK_OR_DEMO_TOOLING_OUTSIDE_MINIMAL_PUBLIC_CLI"
        rows.append(
            {
                "binary": "ddonirang-tool",
                "command": name,
                "current_owner": "tool/src/main.rs",
                "disposition_proposal": disposition,
                "owner_decision_required": True,
            }
        )
    return rows


def teul_commands() -> list[dict[str, object]]:
    path = ROOT / "tools" / "teul-cli" / "src" / "main.rs"
    lines = path.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if "enum Commands {" in line)
    end = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("enum AiCommands"))
    pending_name: str | None = None
    rows: list[dict[str, object]] = []
    depth = 0
    for index in range(start, end):
        line = lines[index]
        if index == start:
            depth = 1
            continue
        if depth == 1:
            named = re.search(r'#\[command\(name\s*=\s*"([^"]+)"', line)
            if named:
                pending_name = named.group(1)
            variant = re.match(r"\s{4}([A-Z][A-Za-z0-9_]*)\s*(?:\{|,)", line)
            if variant:
                variant_name = variant.group(1)
                name = pending_name or kebab(variant_name)
                pending_name = None
                if name in TEUL_CORE:
                    disposition = "MIGRATE_FRONTDOOR_TO_OFFICIAL_CLI_USING_SHARED_PRODUCT_PATH"
                elif name in TEUL_SHARED:
                    disposition = "MOVE_SEMANTICS_TO_SHARED_LIBRARY_THEN_EXPOSE_BY_POLICY"
                else:
                    disposition = "PRESERVE_INTERNAL_OR_DEFERRED_PENDING_V1_MEMBERSHIP"
                rows.append(
                    {
                        "binary": "teul-cli",
                        "command": name,
                        "variant": variant_name,
                        "line": index + 1,
                        "current_owner": "tools/teul-cli/src/main.rs",
                        "disposition_proposal": disposition,
                        "owner_decision_required": True,
                    }
                )
        depth += line.count("{") - line.count("}")
    return rows


def rust_metrics(path: Path) -> dict[str, object]:
    files = [path] if path.is_file() else sorted(path.rglob("*.rs"))
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "rust_file_count": len(files),
        "line_count": sum(len(p.read_text(encoding="utf-8").splitlines()) for p in files),
    }


def write_json(name: str, value: object) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    tool = tool_commands()
    teul = teul_commands()
    registry = {
        "schema": "ddn.v1_cli_identity_audit.i1.command_registry.v1",
        "authority_state": "READ_ONLY_PROPOSAL_NOT_OWNER_DECISION",
        "baseline": "e5454ef5858af4f48a202cffe30ceef010e35162",
        "tool_command_count": len(tool),
        "teul_command_count": len(teul),
        "commands": tool + teul,
    }
    ownership = {
        "schema": "ddn.v1_cli_identity_audit.i1.semantic_ownership.v1",
        "verdict": "SOURCE_OWNERSHIP_CYCLE_WITHOUT_CARGO_CYCLE",
        "edges": [
            {
                "from": "tools/teul-cli",
                "to": "tool",
                "kind": "CARGO_DEPENDENCY",
                "evidence": "tools/teul-cli/Cargo.toml:23",
            },
            {
                "from": "tool/src/lib.rs",
                "to": "tools/teul-cli/src/canon.rs",
                "kind": "PATH_SOURCE_IMPORT",
                "evidence": "tool/src/lib.rs:1",
            },
            {
                "from": "tools/teul-cli/src/main.rs",
                "to": "tool/src/preprocess.rs",
                "kind": "PATH_SOURCE_IMPORT",
                "evidence": "tools/teul-cli/src/main.rs:14",
            },
            {
                "from": "tools/teul-cli/src/lang",
                "to": "tools/teul-cli/src/runtime",
                "kind": "PRIVATE_PARSER_RUNTIME_STACK",
                "evidence": "tools/teul-cli/src/runtime/eval.rs:10-24",
            },
            {
                "from": "tool/src/ddn_runtime.rs",
                "to": "lang",
                "kind": "SHARED_LANGUAGE_RUNTIME_DEPENDENCY",
                "evidence": "tool/src/ddn_runtime.rs:32-38",
            },
        ],
        "metrics": [
            rust_metrics(ROOT / "tool" / "src" / "main.rs"),
            rust_metrics(ROOT / "tool" / "src" / "ddn_runtime.rs"),
            rust_metrics(ROOT / "tools" / "teul-cli" / "src" / "main.rs"),
            rust_metrics(ROOT / "tools" / "teul-cli" / "src" / "canon.rs"),
            rust_metrics(ROOT / "tools" / "teul-cli" / "src" / "lang"),
            rust_metrics(ROOT / "tools" / "teul-cli" / "src" / "runtime"),
            rust_metrics(ROOT / "tools" / "teul-cli" / "src" / "cli"),
        ],
        "source_hashes": {
            "tool/src/main.rs": sha256(ROOT / "tool" / "src" / "main.rs"),
            "tool/src/lib.rs": sha256(ROOT / "tool" / "src" / "lib.rs"),
            "tools/teul-cli/src/main.rs": sha256(ROOT / "tools" / "teul-cli" / "src" / "main.rs"),
            "tools/teul-cli/src/canon.rs": sha256(ROOT / "tools" / "teul-cli" / "src" / "canon.rs"),
        },
    }
    dag = {
        "schema": "ddn.v1_cli_identity_audit.i1.migration_dag.v1",
        "status": "PROPOSAL_NOT_AUTHORIZED_FOR_IMPLEMENTATION",
        "nodes": [
            {"id": "C0", "name": "bind_current_binaries_and_command_registry", "depends_on": []},
            {"id": "C1", "name": "owner_select_public_executable_identity", "depends_on": ["C0"]},
            {"id": "C2", "name": "extract_canon_and_preprocess_to_shared_library", "depends_on": ["C1"]},
            {"id": "C3", "name": "route_core_commands_through_one_product_frontdoor", "depends_on": ["C2"]},
            {"id": "C4", "name": "classify_extended_commands_by_v1_membership", "depends_on": ["C1"]},
            {"id": "C5", "name": "migrate_selected_extended_commands", "depends_on": ["C3", "C4"]},
            {"id": "C6", "name": "preserve_legacy_alias_and_golden_compatibility", "depends_on": ["C5"]},
            {"id": "C7", "name": "independent_cli_wasm_workbench_parity_review", "depends_on": ["C6"]},
            {"id": "C8", "name": "retire_teul_cli_binary_only_after_public_migration", "depends_on": ["C7"]},
        ],
    }
    write_json("cli_command_registry.detjson", registry)
    write_json("cli_semantic_ownership.detjson", ownership)
    write_json("cli_migration_dag.detjson", dag)
    print(
        json.dumps(
            {
                "status": "PASS",
                "tool_commands": len(tool),
                "teul_commands": len(teul),
                "ownership_verdict": ownership["verdict"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
