#!/usr/bin/env python3
"""Generate the exact T5G/W1C2 overlap ledger from Git objects."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess


T5G = "905efb4a1601b764e0f4f2554bef3fbd433172a3"
W1C2 = "40cd0473061abe806b4b09ba51ccd7bfbbc82431"
MECHANICAL_CONFLICTS = {
    "AGENT_WORKFLOW.md",
    "AGENTS.md",
    "lang/src/lib.rs",
    "solutions/seamgrim_ui_mvp/ui/screens/run.js",
    "solutions/seamgrim_ui_mvp/ui/seamgrim_runtime_state.js",
    "solutions/seamgrim_ui_mvp/ui/view_plan_runtime.js",
    "solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson",
    "solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm",
    "solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_payload.js",
    "tests/seamgrim_workbench_semantic_view_payload_runner.mjs",
    "tool/src/lib.rs",
    "tool/src/local_project.rs",
    "tools/teul-cli/src/canon.rs",
}


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def changed(repo: Path, base: str, head: str) -> set[str]:
    output = git(repo, "diff", "--name-only", f"{base}..{head}")
    return set(output.splitlines()) if output else set()


def blob(repo: Path, commit: str, path: str) -> str:
    output = git(repo, "ls-tree", commit, "--", path)
    return output.split()[2] if output else "ABSENT"


def role(path: str) -> str:
    if path in {"AGENTS.md", "AGENT_WORKFLOW.md", "CHANGELOG.md", "PROJECT_STATUS.md"}:
        return "AUTHORITY_DOCUMENT_OVERLAP"
    if path.startswith("tests/"):
        return "TEST_EVIDENCE_OVERLAP"
    if path.startswith("solutions/seamgrim_ui_mvp/ui/wasm/"):
        return "GENERATED_ARTIFACT_OVERLAP"
    if path.startswith(("lang/", "tool/", "tools/teul-cli/", "solutions/seamgrim_ui_mvp/ui/")):
        return "SEMANTIC_OVERLAP"
    return "TEXTUAL_OVERLAP"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    base = git(repo, "merge-base", T5G, W1C2)
    t5g_paths = changed(repo, base, T5G)
    w1c2_paths = changed(repo, base, W1C2)
    overlap = sorted(t5g_paths & w1c2_paths)
    rows: list[dict[str, object]] = []
    for path in overlap:
        t5g_blob = blob(repo, T5G, path)
        w1c2_blob = blob(repo, W1C2, path)
        rows.append(
            {
                "path": path,
                "role": role(path),
                "t5g_blob": t5g_blob,
                "w1c2_blob": w1c2_blob,
                "same_final_blob": t5g_blob == w1c2_blob,
                "mechanical_conflict": path in MECHANICAL_CONFLICTS,
                "owner_decision_required": t5g_blob != w1c2_blob
                and role(path) in {"SEMANTIC_OVERLAP", "GENERATED_ARTIFACT_OVERLAP"},
            }
        )
    divergent = [row for row in rows if not row["same_final_blob"]]
    role_counts: dict[str, int] = {}
    for row in divergent:
        role_counts[row["role"]] = role_counts.get(row["role"], 0) + 1
    result = {
        "schema": "ddn.release_integration.overlap_ledger.v1",
        "t5g": T5G,
        "w1c2": W1C2,
        "merge_base": base,
        "t5g_changed_path_count": len(t5g_paths),
        "w1c2_changed_path_count": len(w1c2_paths),
        "overlap_path_count": len(rows),
        "same_final_blob_count": len(rows) - len(divergent),
        "divergent_final_blob_count": len(divergent),
        "mechanical_conflict_count": sum(row["mechanical_conflict"] for row in divergent),
        "owner_decision_required_count": sum(row["owner_decision_required"] for row in divergent),
        "divergent_role_counts": dict(sorted(role_counts.items())),
        "rows": rows,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    digest = hashlib.sha256(args.out.read_bytes()).hexdigest()
    print(
        f"overlap={len(rows)} divergent={len(divergent)} "
        f"mechanical={result['mechanical_conflict_count']} "
        f"owner_required={result['owner_decision_required_count']} sha256={digest}"
    )


if __name__ == "__main__":
    main()
