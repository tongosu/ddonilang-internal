#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "tools" / "build_ganada_intake_ledger_v1.py"
WORK_DIR = ROOT / "work" / "codex" / "20260710_ganada_intake_audit"
JUDGEMENTS = WORK_DIR / "ganada_intake_judgements_v1.detjson"
LEDGER = WORK_DIR / "ganada_intake_ledger_v1.jsonl"
SUMMARY = WORK_DIR / "ganada_intake_summary_v1.detjson"
EXECUTION_RECORD = ROOT / (
    "work/codex/20260711_seamgrim_manim_promotion_governance/"
    "repository_p2a_execution_record_v1.detjson"
)
BUILD_ROOTS = (
    Path("I:/home/urihanl/ddn/codex/build"),
    Path("C:/ddn/codex/build"),
)
GANADA_CELL_RE = re.compile(r"^(?:가|나|다|라|마|바|사|아|자|차|카|타|파|하|거)-[0-5]$")


def select_build_root() -> Path:
    for path in BUILD_ROOTS:
        if path.exists():
            return path
    if os.name == "nt":
        return BUILD_ROOTS[-1]
    return Path(tempfile.gettempdir()) / "ddn-codex-build"


def load_entries(path: Path) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        try:
            entry = json.loads(line)
        except json.JSONDecodeError as exc:
            raise AssertionError(f"invalid ledger JSON at line {line_number}: {exc}") from exc
        assert entry.get("schema") == "ddn.ganada.intake_ledger_entry.v1"
        entries.append(entry)
    return entries


def assert_ref_exists(ref: str) -> None:
    path_text, line_text = ref.rsplit(":", 1)
    path = ROOT / path_text
    assert path.is_file(), f"missing ref file: {ref}"
    line_number = int(line_text)
    line_count = len(path.read_text(encoding="utf-8", errors="replace").splitlines())
    assert 1 <= line_number <= line_count, f"ref line out of range: {ref}"


def summary_source_count_hint(path: Path) -> int:
    return int(json.loads(path.read_text(encoding="utf-8"))["source_count"])


def main() -> int:
    assert GENERATOR.is_file()
    assert JUDGEMENTS.is_file()
    assert LEDGER.is_file()
    assert SUMMARY.is_file()

    build_root = select_build_root()
    build_root.mkdir(parents=True, exist_ok=True)
    temp_out = build_root / "ganada_intake_ledger_v1_check"
    if temp_out.exists():
        shutil.rmtree(temp_out)
    temp_out.mkdir(parents=True)
    try:
        proc = subprocess.run(
            [
                "python",
                str(GENERATOR),
                "--repo-root",
                str(ROOT),
                "--judgements",
                str(JUDGEMENTS),
                "--out-dir",
                str(temp_out),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
        regenerated_ledger = temp_out / LEDGER.name
        regenerated_summary = temp_out / SUMMARY.name
        assert LEDGER.read_bytes() == regenerated_ledger.read_bytes(), "ledger is stale or nondeterministic"
        assert SUMMARY.read_bytes() == regenerated_summary.read_bytes(), "summary is stale or nondeterministic"

        all_out = temp_out / "all_metadata"
        all_proc = subprocess.run(
            [
                "python",
                str(GENERATOR),
                "--repo-root",
                str(ROOT),
                "--judgements",
                str(JUDGEMENTS),
                "--out-dir",
                str(all_out),
                "--profile",
                "all_metadata",
                "--output-prefix",
                "repository_source_registry",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        assert all_proc.returncode == 0, all_proc.stdout + all_proc.stderr
        all_summary = json.loads(
            (all_out / "repository_source_registry_summary_v1.detjson").read_text(encoding="utf-8")
        )
        assert all_summary["profile"] == "all_metadata"
        assert all_summary["source_count"] > summary_source_count_hint(SUMMARY)
        assert set(all_summary["consumer_lane_counts"]) == {
            "authority",
            "decision",
            "evidence",
            "reference",
        }
    finally:
        if temp_out.exists():
            shutil.rmtree(temp_out)

    entries = load_entries(LEDGER)
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert summary["profile"] == "decision_sources"
    paths = [str(entry["path"]) for entry in entries]
    assert paths == sorted(paths), "ledger paths must be sorted"
    assert len(paths) == len(set(paths)), "ledger paths must be unique"
    assert summary["source_count"] == len(entries)
    assert {
        "proposal",
        "context_note",
        "docs_note",
        "session_delta",
        "root_ddonirang",
        "ganada_roadmap",
        "design",
        "brief",
        "decision",
        "request",
        "manuscript",
        "ssot",
    }.issubset(summary["collection_counts"])
    archived_root_ddonirang = 0
    if EXECUTION_RECORD.is_file():
        execution_record = json.loads(EXECUTION_RECORD.read_text(encoding="utf-8"))
        archived_root_ddonirang = sum(
            item.get("category") == "root_ddonirang"
            and item.get("owner_decision") == "confirmed"
            and item.get("execution_status") == "moved"
            for item in execution_record.get("items", [])
        )
        assert summary["archived_source_count"] == execution_record["candidate_count"]
    else:
        assert summary["archived_source_count"] == 0
    assert summary["collection_counts"]["root_ddonirang"] + archived_root_ddonirang >= 20
    assert summary["deep_reviewed_count"] >= 15
    assert summary["frozen_tags"] == [
        "declarative_modeling",
        "ai_audit",
        "multilang_curriculum",
        "manim",
        "nurigym_game",
        "freeze",
        "governance",
    ]
    assert summary["allowed_overlays"] == ["seamgrim_public_wedge", "learning_spine_index"]

    duplicate_members: dict[str, set[str]] = {}
    for entry in entries:
        digest = entry.get("exact_duplicate_group")
        if digest:
            duplicate_members.setdefault(str(digest), set()).add(str(entry["path"]))
        for cell in entry.get("primary_ganada_cells", []) + entry.get("support_ganada_cells", []):
            assert GANADA_CELL_RE.fullmatch(cell), f"invalid Ganada cell {cell}: {entry['path']}"
        if entry.get("reflection_status") == "reflected":
            refs = entry.get("ssot_refs", [])
            assert refs
            for ref in refs:
                assert_ref_exists(ref)
        if entry.get("owner_decision") == "confirmed":
            assert entry.get("user_decision_ref")
        if entry.get("implementation_status") == "landed":
            assert entry.get("product_path_refs")
            assert entry.get("pack_or_equivalent_refs")
            evidence = entry.get("verification_evidence", [])
            assert evidence and all(item.get("result") == "PASS" for item in evidence)
        absence = entry.get("absence_claim")
        if absence:
            assert absence.get("level") in {"not_found_in_scope", "verified_absent"}
            assert absence.get("scope")

    for entry in entries:
        digest = entry.get("exact_duplicate_group")
        if digest:
            assert set(entry.get("exact_duplicate_paths", [])) == duplicate_members[str(digest)]
            assert len(duplicate_members[str(digest)]) >= 2

    print(
        "ganada_intake_ledger_v1_check: PASS "
        f"sources={len(entries)} deep={summary['deep_reviewed_count']} "
        f"duplicate_groups={summary['exact_duplicate_group_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
