#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools/build_repository_duplicate_move_plan_v1.py"
REGISTRY = ROOT / "work/codex/20260711_repository_structure_registry/repository_source_registry_ledger_v1.jsonl"
OUT_DIR = ROOT / "work/codex/20260711_seamgrim_manim_promotion_governance"
EXPECTED_CSV = OUT_DIR / "repository_duplicate_p2_move_table_v1.csv"
EXPECTED_JSON = OUT_DIR / "repository_duplicate_backrefs_v1.detjson"
EXPECTED_EXECUTION = OUT_DIR / "repository_p2a_execution_manifest_v1.detjson"
EXECUTION_RECORD = OUT_DIR / "repository_p2a_execution_record_v1.detjson"
BUILD_ROOTS = (Path("I:/home/urihanl/ddn/codex/build"), Path("C:/ddn/codex/build"))


def select_build_root() -> Path:
    for path in BUILD_ROOTS:
        if path.exists():
            return path
    if os.name == "nt":
        return BUILD_ROOTS[-1]
    return Path(tempfile.gettempdir()) / "ddn-codex-build"


def main() -> int:
    build_root = select_build_root()
    temp = build_root / "repository_duplicate_move_plan_v1_check"
    if temp.exists():
        shutil.rmtree(temp)
    temp.mkdir(parents=True)
    try:
        proc = subprocess.run(
            [
                "python",
                str(TOOL),
                "--repo-root",
                str(ROOT),
                "--registry",
                str(REGISTRY),
                "--out-dir",
                str(temp),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert EXPECTED_CSV.read_bytes() == (temp / EXPECTED_CSV.name).read_bytes()
        assert EXPECTED_JSON.read_bytes() == (temp / EXPECTED_JSON.name).read_bytes()
        assert EXPECTED_EXECUTION.read_bytes() == (
            temp / EXPECTED_EXECUTION.name
        ).read_bytes()
        for path in (EXPECTED_CSV, EXPECTED_JSON, EXPECTED_EXECUTION):
            assert b"\r\n" not in path.read_bytes(), f"CRLF output: {path}"

        payload = json.loads(EXPECTED_JSON.read_text(encoding="utf-8"))
        assert payload["schema"] == "ddn.repository_duplicate_backrefs.v1"
        assert payload["candidate_count"] == len(payload["items"])
        assert sum(payload["status_counts"].values()) == payload["candidate_count"]
        assert payload["missing_explicit_archive_candidates"] == []
        assert sum(payload["explicit_archive_status_counts"].values()) == payload["explicit_archive_candidate_count"]

        execution_record = None
        if EXECUTION_RECORD.is_file():
            execution_record = json.loads(EXECUTION_RECORD.read_text(encoding="utf-8"))
            assert execution_record["schema"] == "ddn.repository_p2a_execution_record.v1"
            assert execution_record["candidate_count"] == 15
            assert execution_record["approval_text"] == "P2-A 15개 이동을 승인합니다."
            assert execution_record["verification"]["finalized"] is True
            assert all(
                item["owner_decision"] == "confirmed"
                and item["execution_status"] == "moved"
                and not (ROOT / item["source"]).exists()
                and (ROOT / item["target"]).is_file()
                for item in execution_record["items"]
            )
            assert payload["executed_source_count"] == 15
            assert payload["explicit_archive_candidate_count"] + 4 == 15
        else:
            assert payload["executed_source_count"] == 0
            assert payload["explicit_archive_candidate_count"] == 15

        explicit = {
            row["source"]: row for row in payload["explicit_archive_items"]
        }
        cited_session_deltas = {
            "work/_session_deltas/20260711_codex_seamgrim_product_to_korean_manim_vertical.md":
                "docs/context/reports/SEAMGRIM_KOREAN_MANIM_DECISION_LEDGER_V1_20260711.detjson",
            "work/_session_deltas/20260711_codex_seamgrim_wave2a_live_semantic_lesson.md":
                "docs/context/reports/SEAMGRIM_KOREAN_MANIM_PROMOTION_LEDGER_V2_20260711.detjson",
            "work/_session_deltas/20260711_codex_seamgrim_wave2b_authoring_deploy_vertical.md":
                "docs/context/reports/SEAMGRIM_KOREAN_MANIM_PROMOTION_LEDGER_V2_20260711.detjson",
            "work/_session_deltas/20260711_codex_wave2a_runtime_role_boundary_fix.md":
                "docs/context/reports/SEAMGRIM_KOREAN_MANIM_PROMOTION_LEDGER_V2_20260711.detjson",
        }
        for source, referrer in cited_session_deltas.items():
            row = explicit[source]
            assert row["reverse_ref_status"] == "blocked_rewrite_required"
            assert referrer in row["exact_path_refs"]
            assert row["execution_status"] == "planned_not_moved"

        execution = json.loads(EXPECTED_EXECUTION.read_text(encoding="utf-8"))
        assert execution["schema"] == "ddn.repository_p2a_execution_manifest.v1"
        assert execution["candidate_count"] == len(execution["items"])
        assert execution["target_collisions"] == []
        assert execution["all_owner_decisions_pending"] is True
        assert execution["all_execution_statuses_planned"] is True
        assert all(
            item["preconditions"]["source_exists"]
            and item["preconditions"]["target_absent"]
            and item["preconditions"]["sha256_matches"]
            and item["preconditions"]["user_approval_required"]
            and item["preconditions"]["latest_registry_recheck_required"]
            for item in execution["items"]
        )
        if execution_record is None:
            assert execution["candidate_count"] == 15
            assert {
                item["category"] for item in execution["items"]
            } == {"exact_duplicate", "root_ddonirang", "session_delta"}
        else:
            executed_sources = {item["source"] for item in execution_record["items"]}
            assert not executed_sources.intersection(
                item["source"] for item in execution["items"]
            )

        with EXPECTED_CSV.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        assert len(rows) == payload["candidate_count"]
        assert all(row["execution_status"] == "planned_not_moved" for row in rows)
        assert all(row["owner_decision"] == "pending" for row in rows)
        assert all(row["source"] != row["representative"] for row in rows)

        replan = next(
            (
                row
                for row in rows
                if row["source"] == "docs/context/proposals/PROPOSAL_SEAMGRIM_REPLAN_V2_1_20260214.md"
            ),
            None,
        )
        if replan is not None:
            assert replan["representative"] == (
                "docs/context/proposals/PROPOSAL_SEAMGRIM_REPLAN_V2_20260214.md"
            )
        print(
            "repository_duplicate_move_plan_v1_check: PASS "
            f"groups={payload['group_count']} candidates={len(rows)} "
            f"explicit_archive_candidates={len(explicit)}"
        )
        return 0
    finally:
        if temp.exists():
            shutil.rmtree(temp)


if __name__ == "__main__":
    raise SystemExit(main())
