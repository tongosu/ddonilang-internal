#!/usr/bin/env python3
"""Audit reviewed-scope membership and a no-write three-way convergence preview."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile


ADMIN_HEAD = "fab6315ccddbec9b11bac748aed1c419f3ba4dad"
T5_CLOSURE = "905efb4a1601b764e0f4f2554bef3fbd433172a3"
PC01_IMPLEMENTATION = "cf97f134aebc4889bd3e13ff4850cbf76ca4c2d6"
PC01_FIXED = "3ac1cefbffa4c00857f99f8d5fce5911dfd01c652"
PC01_HANDOFF = "9cb28ee8044dd0562d99f8d5fce5911dfd01c652"
PC02_IMPLEMENTATION = "04566a2426b56084f4449b363530192aa1166d2a"
PC02_PARENT = "f03955c01963646c0095fcffb14f9f162c9655ce"
W1_SCOPE_BASE = "2ec750aa576fdbd1ebd0bd400d95775e597e9983"
W1_SCOPE_HEAD = "40cd0473061abe806b4b09ba51ccd7bfbbc82431"

PREREQUISITE_COMMITS = [
    {
        "commit": "15f983fe32e0f04c4783e67118610f7441b401c6",
        "program": "R10_SOURCE_READINESS",
        "integration_state": "IMPLEMENTED_NO_STANDALONE_PLAIN_PASS_CLOSURE_FOUND",
    },
    {
        "commit": "0249aa0ded9ec58832c4c85e6ef169c6356a8fdc",
        "program": "T1_RUNTIMEBRIDGE",
        "integration_state": "IMPLEMENTED_NO_STANDALONE_PLAIN_PASS_CLOSURE_FOUND",
    },
    {
        "commit": "9742086f417d6b2c5bc641f7f245aa2ef9126431",
        "program": "T2_HOSTBRIDGE",
        "integration_state": "IMPLEMENTED_NO_STANDALONE_PLAIN_PASS_CLOSURE_FOUND",
    },
    {
        "commit": "cee6131522eda91708774967ac732f148b170a48",
        "program": "T4_SOURCE_ANALYSIS",
        "integration_state": "IMPLEMENTED_NO_STANDALONE_PLAIN_PASS_CLOSURE_FOUND",
    },
    {
        "commit": "b930832c74dd7089ee02552e27689bdb16f75adc",
        "program": "T4B_CHAEBI_WARNING",
        "integration_state": "IMPLEMENTED_NO_STANDALONE_PLAIN_PASS_CLOSURE_FOUND",
    },
    {
        "commit": "add7c0df0001e1f63469bbbbc07a8ef648f6efc4",
        "program": "T4D_OBSERVATION_MANIFEST",
        "integration_state": "IMPLEMENTED_NO_STANDALONE_PLAIN_PASS_CLOSURE_FOUND",
    },
    {
        "commit": "c0e94daddc7510b1ab5f45deb7d0a75af1e7a88a",
        "program": "T4E_CONTROL_PLAN",
        "integration_state": "IMPLEMENTED_NO_STANDALONE_PLAIN_PASS_CLOSURE_FOUND",
    },
    {
        "commit": "49f3b4db6a941bbcda0a82ee412437445c0d8248",
        "program": "T4F_OBSERVATION_CHANNEL",
        "integration_state": "IMPLEMENTED_NO_STANDALONE_PLAIN_PASS_CLOSURE_FOUND",
    },
    {
        "commit": "b789e1ac557bfa9a9ea14eca1add482e0aa1d0ff",
        "program": "T4H_REPAIR_PROPOSAL",
        "integration_state": "IMPLEMENTED_NO_STANDALONE_PLAIN_PASS_CLOSURE_FOUND",
    },
]


def run(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def git(repo: Path, *args: str) -> str:
    return run(repo, *args).stdout.strip()


def ancestor(repo: Path, older: str, newer: str) -> bool:
    return run(repo, "merge-base", "--is-ancestor", older, newer, check=False).returncode == 0


def changed(repo: Path, base: str, head: str) -> set[str]:
    output = git(repo, "diff", "--name-only", base, head)
    return set(output.splitlines()) if output else set()


def blob_id(repo: Path, commit: str, path: str) -> str:
    output = git(repo, "ls-tree", commit, "--", path)
    return output.split()[2] if output else "ABSENT"


def blob_bytes(repo: Path, commit: str, path: str) -> bytes | None:
    if blob_id(repo, commit, path) == "ABSENT":
        return None
    return subprocess.run(
        ["git", "-C", str(repo), "show", f"{commit}:{path}"],
        check=True,
        capture_output=True,
    ).stdout


def role(path: str) -> str:
    if path in {
        "docs/context/all/DEV_SUMMARY.md",
        "docs/reports/impl/INDEX.md",
        "docs/status/CHANGELOG.md",
        "docs/status/PROJECT_STATUS.md",
    }:
        return "AUTHORITY_DOCUMENT_OVERLAP"
    if path.startswith(("tests/", "pack/")):
        return "TEST_EVIDENCE_OVERLAP"
    if path.startswith("solutions/seamgrim_ui_mvp/ui/wasm/"):
        return "GENERATED_ARTIFACT_OVERLAP"
    if path.startswith(("lang/", "tool/", "tools/teul-cli/", "solutions/")):
        return "SEMANTIC_OVERLAP"
    return "TEXTUAL_OVERLAP"


def merge_text(ours: bytes, base: bytes, theirs: bytes) -> tuple[int, int]:
    with tempfile.TemporaryDirectory(prefix="ddn-reli-merge-audit-") as raw:
        root = Path(raw)
        paths = [root / "ours", root / "base", root / "theirs"]
        for path, payload in zip(paths, (ours, base, theirs), strict=True):
            path.write_bytes(payload)
        proc = subprocess.run(
            ["git", "merge-file", "-p", str(paths[0]), str(paths[1]), str(paths[2])],
            check=False,
            capture_output=True,
        )
        return proc.returncode, proc.stdout.count(b"<<<<<<<")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()

    pc02_paths = changed(repo, PC02_PARENT, PC02_IMPLEMENTATION)
    post_pc02_paths = changed(repo, PC02_IMPLEMENTATION, ADMIN_HEAD)
    later_pc02_overlap = sorted(pc02_paths & post_pc02_paths)

    w1_paths = changed(repo, W1_SCOPE_BASE, W1_SCOPE_HEAD)
    rows: list[dict[str, object]] = []
    for path in sorted(w1_paths):
        effective_commit = PC02_PARENT if path in pc02_paths else ADMIN_HEAD
        base_id = blob_id(repo, W1_SCOPE_BASE, path)
        ours_id = blob_id(repo, effective_commit, path)
        if base_id == ours_id:
            continue
        theirs_id = blob_id(repo, W1_SCOPE_HEAD, path)
        item: dict[str, object] = {
            "path": path,
            "role": role(path),
            "base_blob": base_id,
            "effective_t5_r2_blob": ours_id,
            "w1_scoped_blob": theirs_id,
            "pc02_inverse_source": effective_commit == PC02_PARENT,
        }
        payloads = (
            blob_bytes(repo, effective_commit, path),
            blob_bytes(repo, W1_SCOPE_BASE, path),
            blob_bytes(repo, W1_SCOPE_HEAD, path),
        )
        if any(payload is None for payload in payloads):
            item["merge_preview"] = "ADD_DELETE_OR_ABSENT_REQUIRES_EXACT_PATH_REVIEW"
            item["conflict_hunks"] = None
        elif any(b"\0" in payload for payload in payloads if payload is not None):
            item["merge_preview"] = "GENERATED_BINARY_MUST_REBUILD_NOT_MERGE"
            item["conflict_hunks"] = None
        else:
            code, conflict_hunks = merge_text(*payloads)  # type: ignore[arg-type]
            item["merge_preview"] = (
                "TEXT_AUTO_MERGE" if code == 0 else "TEXT_CONFLICT_REQUIRES_SEMANTIC_COMPOSITION"
            )
            item["conflict_hunks"] = conflict_hunks
        rows.append(item)

    role_counts: dict[str, int] = {}
    preview_counts: dict[str, int] = {}
    for row in rows:
        role_counts[str(row["role"])] = role_counts.get(str(row["role"]), 0) + 1
        preview_counts[str(row["merge_preview"])] = (
            preview_counts.get(str(row["merge_preview"]), 0) + 1
        )

    result = {
        "schema": "ddn.release_integration.scoped_membership_merge_audit.v1",
        "administrative_head": ADMIN_HEAD,
        "t5_closure_head": T5_CLOSURE,
        "t5_closure_is_ancestor_of_administrative_head": ancestor(repo, T5_CLOSURE, ADMIN_HEAD),
        "pc01": {
            "implementation": PC01_IMPLEMENTATION,
            "fixed": PC01_FIXED,
            "handoff": PC01_HANDOFF,
            "integration_state": "CLOSED_INDEPENDENT_PASS_OWNER_ATTESTED_NO_LOCAL_REVIEW_ARTIFACT",
            "is_ancestor_of_t5_closure": ancestor(repo, PC01_IMPLEMENTATION, T5_CLOSURE),
        },
        "pc02": {
            "implementation": PC02_IMPLEMENTATION,
            "parent": PC02_PARENT,
            "integration_state": "IMPLEMENTED_PENDING_INDEPENDENT_REVIEW",
            "is_ancestor_of_t5_closure": ancestor(repo, PC02_IMPLEMENTATION, T5_CLOSURE),
            "is_ancestor_of_administrative_head": ancestor(repo, PC02_IMPLEMENTATION, ADMIN_HEAD),
            "changed_path_count": len(pc02_paths),
            "paths_changed_again_after_pc02_count": len(later_pc02_overlap),
            "paths_changed_again_after_pc02": later_pc02_overlap,
            "inverse_is_blob_separable_at_administrative_head": len(later_pc02_overlap) == 0,
        },
        "t5_prerequisite_programs": PREREQUISITE_COMMITS,
        "prerequisite_commits_all_ancestors_of_t5_closure": all(
            ancestor(repo, item["commit"], T5_CLOSURE) for item in PREREQUISITE_COMMITS
        ),
        "w1_reviewed_scope": {
            "base": W1_SCOPE_BASE,
            "head": W1_SCOPE_HEAD,
            "changed_path_count": len(w1_paths),
        },
        "effective_t5_r2_definition": "ADMIN_HEAD_WITH_PC02_PATCH_INVERTED_CONCEPTUALLY_NO_TREE_WRITTEN",
        "changed_in_both_scoped_count": len(rows),
        "changed_in_both_role_counts": dict(sorted(role_counts.items())),
        "merge_preview_counts": dict(sorted(preview_counts.items())),
        "rows": rows,
        "baseline_eligibility": {
            "administrative_head_as_is": False,
            "reason": "CONTAINS_PC02_IMPLEMENTED_PENDING_REVIEW_AND_UNCLOSED_T5_PREREQUISITE_PROGRAM_BYTES",
            "g8_product_integration_authorized": False,
        },
        "owner_decisions_required": [
            "T5_PREREQUISITE_BYTES_AS_INTEGRATION_DEPENDENCIES",
            "W1_PRE_SCOPE_REVIEWED_BASELINE_BYTES_AS_INTEGRATION_DEPENDENCIES",
            "PC01_OWNER_ATTESTED_PASS_MEMBERSHIP",
            "PC02_EXCLUSION_METHOD",
            "SCOPED_TEXT_CONFLICT_SEMANTIC_COMPOSITION_POLICY",
            "COMBINED_SOURCE_WASM_REBUILD_AND_BINDING",
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    digest = hashlib.sha256(args.out.read_bytes()).hexdigest()
    print(
        f"pc02_paths={len(pc02_paths)} later_overlap={len(later_pc02_overlap)} "
        f"scoped_changed_both={len(rows)} previews={dict(sorted(preview_counts.items()))} "
        f"sha256={digest}"
    )


if __name__ == "__main__":
    main()
