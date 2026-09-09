#!/usr/bin/env python3
"""Generate the FD01 product-frontdoor readiness inventory.

This is a read-only audit generator.  It records current reachability and does
not reapply historical PC02 or modify product sources.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "work" / "codex" / "20260827_ddn_v1_fd01_frontdoor_runtimebridge_readiness_audit_i1"


def sha256(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def write_json(name: str, payload: object) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    surfaces = [
        {
            "id": "FD01-S01",
            "surface": "lang_v25_parser",
            "status": "IMPLEMENTED_INTERNAL",
            "evidence": ["lang/src/lib.rs:130-147", "lang/src/parser.rs:227-233"],
        },
        {
            "id": "FD01-S02",
            "surface": "tool_v25_program_constructor",
            "status": "IMPLEMENTED_TEST_REACHABLE_ONLY",
            "evidence": ["tool/src/ddn_runtime.rs:1760-1769", "tool/src/ddn_runtime.rs:19616-19642"],
        },
        {
            "id": "FD01-S03",
            "surface": "official_cli_run_and_run_summary",
            "status": "PRE_V25_DEFAULT_V25_INGRESS_0",
            "evidence": ["tool/src/main.rs:1775-1822", "tool/src/runtime_surface.rs:461-564"],
        },
        {
            "id": "FD01-S04",
            "surface": "wasm_default_vm_constructor",
            "status": "PRE_V25_DEFAULT_V25_INGRESS_0",
            "evidence": ["tool/src/wasm_api.rs:78-101", "tool/src/wasm_api.rs:877-953"],
        },
        {
            "id": "FD01-S05",
            "surface": "shared_source_analysis",
            "status": "CONNECTED_BUT_PRE_V25_PARSER",
            "evidence": ["tool/src/source_analysis.rs:285-345", "tool/src/source_analysis.rs:310"],
        },
        {
            "id": "FD01-S06",
            "surface": "workbench_runtimebridge_source_analysis",
            "status": "CONNECTED_TO_RUST_WASM_FAIL_CLOSED",
            "evidence": ["solutions/seamgrim_ui_mvp/ui/runtime/runtime_bridge.js:106-115", "solutions/seamgrim_ui_mvp/ui/workbench/workbench.js:1827-1878"],
        },
        {
            "id": "FD01-S07",
            "surface": "native_observation_manifest",
            "status": "CONNECTED_FAIL_CLOSED_JS_SYNTHESIS_0",
            "evidence": ["solutions/seamgrim_ui_mvp/ui/runtime/wasm_vm_runtime.js:7-60", "solutions/seamgrim_ui_mvp/ui/runtime/observation_manifest_contract.js:58-126"],
        },
        {
            "id": "FD01-S08",
            "surface": "dead_js_observation_manifest_builder",
            "status": "UNUSED_REEXPORT_HOUSEKEEPING_OPEN",
            "evidence": ["solutions/seamgrim_ui_mvp/ui/runtime/index.js:6", "solutions/seamgrim_ui_mvp/ui/runtime/observation_manifest.js:71"],
        },
        {
            "id": "FD01-S09",
            "surface": "t5f_four_family_current_canonical_results",
            "status": "PARTIAL_GRID_RESULT_OPEN",
            "evidence": ["tests/seamgrim_workbench_four_family_canonical_view_payload_runner.mjs:104", "tests/seamgrim_t5f_current_grid_successor_input_audit_runner.mjs:1-90"],
        },
        {
            "id": "FD01-S10",
            "surface": "current_grid_successor_input",
            "status": "ACCEPTED_WITHOUT_NATIVE_GRID_RESULT",
            "evidence": ["solutions/seamgrim_ui_mvp/lessons/rep_grid_game_state_drop_v1/lesson.ddn", "tests/seamgrim_t5f_current_grid_successor_input_audit_runner.mjs"],
        },
        {
            "id": "FD01-S11",
            "surface": "workbench_lesson_epoch_compatibility",
            "status": "V25_PASS_0_OF_557_GLOBAL_DEFAULT_SWITCH_UNSAFE",
            "evidence": ["tool/tests/v1_fd01_lesson_epoch_inventory.rs"],
        },
    ]
    inventory = {
        "schema": "ddn.v1.fd01.frontdoor_runtimebridge_readiness.i1.v1",
        "authority": {
            "internal_ssot": "v25.15.0",
            "public_language_spec": "v0.5.0",
            "authoritative_v1_membership_rows": 0,
            "verified_product_floor": "UNCLAIMABLE",
        },
        "baseline": "25a63aba7dc6ab362dd3f640385ad9a7ebfa0455",
        "verdict": "FD01_PRODUCT_FRONTDOOR_NOT_YET_CONVERGED",
        "current_v25_public_product_ingress_count": 0,
        "surfaces": surfaces,
        "historical_pc02": {
            "implementation_commit": "04566a2426b56084f4449b363530192aa1166d2a",
            "implementation_status": "IMPLEMENTED_PENDING_INDEPENDENT_REVIEW",
            "independent_review_commit": None,
            "exact_inverse_commit": "0dd73ab9",
            "current_disposition": "EXCLUDED_BY_EXACT_INVERSE_OWNER_BOUND",
            "blind_reapply_authorized": False,
        },
        "lesson_epoch_inventory": {
            "total": 557,
            "both": 0,
            "pre_v25_only": 127,
            "v25_only": 0,
            "neither": 430,
            "v25_pass": 0,
            "v25_error_families": {
                "E_BOIM_LEGACY_REMOVED": 414,
                "E_V25_DEFINITION_BINDING_CATEGORY": 8,
                "E_V25_DEFINITION_MIGRATION_REQUIRED": 135,
            },
            "global_default_switch_safe": False,
        },
        "source_hashes": {
            path: sha256(path)
            for path in [
                "lang/src/frontdoor.rs",
                "lang/src/lib.rs",
                "tool/src/ddn_runtime.rs",
                "tool/src/runtime_surface.rs",
                "tool/src/source_analysis.rs",
                "tool/src/wasm_api.rs",
                "solutions/seamgrim_ui_mvp/ui/runtime/runtime_bridge.js",
                "solutions/seamgrim_ui_mvp/ui/runtime/observation_manifest_contract.js",
                "solutions/seamgrim_ui_mvp/ui/runtime/wasm_vm_runtime.js",
                "solutions/seamgrim_ui_mvp/ui/workbench/source_readiness.js",
                "solutions/seamgrim_ui_mvp/ui/workbench/workbench.js",
            ]
        },
    }
    dag = {
        "schema": "ddn.v1.fd01.successor_dag.v1",
        "status": "OWNER_DECISION_REQUIRED_BEFORE_PRODUCT_IMPLEMENTATION",
        "nodes": [
            {"id": "F0", "name": "bind_pc01_followup_and_g14_review_state", "depends_on": []},
            {"id": "F1", "name": "owner_choose_typed_epoch_routing_not_global_switch", "depends_on": ["F0"]},
            {"id": "F2", "name": "land_internal_typed_current_and_migration_entrypoints", "depends_on": ["F1"]},
            {"id": "F3", "name": "connect_source_analysis_to_explicit_internal_epoch", "depends_on": ["F2"]},
            {"id": "F4", "name": "connect_wasm_runtimebridge_to_explicit_bundled_project_epoch", "depends_on": ["F2", "F3"]},
            {"id": "F5", "name": "select_and_migrate_v1_public_example_membership", "depends_on": ["F4"]},
            {"id": "F6", "name": "land_current_grid_native_result_set", "depends_on": ["F5"]},
            {"id": "F7", "name": "run_positive_negative_migration_determinism_fault_matrix", "depends_on": ["F6"]},
            {"id": "F8", "name": "owner_gate_default_v25_switch_after_coverage", "depends_on": ["F7"]},
            {"id": "F9", "name": "fresh_cli_wasm_workbench_real_edge_review", "depends_on": ["F8"]},
            {"id": "F10", "name": "bind_plain_pass_without_stable_wire_claim", "depends_on": ["F9"]},
        ],
        "forbidden_shortcuts": [
            "CONTENT_SNIFFING_SOURCE_EPOCH_AUTODETECT",
            "BLIND_REAPPLY_PC02_COMMIT",
            "JS_SYNTAX_OR_OBSERVATION_SYNTHESIS",
            "HISTORICAL_PASS_AUTOMATIC_INHERITANCE",
            "STABLE_WIRE_CLAIM",
            "GLOBAL_V25_DEFAULT_SWITCH_BEFORE_LESSON_MIGRATION",
        ],
    }
    tests = {
        "schema": "ddn.v1.fd01.readiness_test_ledger.v1",
        "runs": [
            {"id": "T1", "command": "node tests/seamgrim_workbench_runtime_bridge_t1_runner.mjs", "result": "PASS"},
            {"id": "T2", "command": "node tests/seamgrim_workbench_source_analysis_t4_runner.mjs", "result": "PASS_STATIC"},
            {"id": "T3", "command": "DDN_T4_SOURCE_WASM_DIR=tracked node tests/seamgrim_workbench_source_analysis_t4_runner.mjs", "result": "PASS_TRACKED_WASM"},
            {"id": "T4", "command": "node tests/seamgrim_workbench_observation_manifest_t4d_runner.mjs", "result": "PASS"},
            {"id": "T5", "command": "node tests/seamgrim_workbench_observation_channel_t4f_runner.mjs", "result": "PASS_FAIL_CLOSED"},
            {"id": "T6", "command": "DDN_T5F_SOURCE_WASM_DIR=tracked node tests/seamgrim_workbench_four_family_canonical_view_payload_runner.mjs", "result": "EXPECTED_RED_GRID_NATIVE_RESULT_MISSING"},
            {"id": "T7", "command": "node tests/seamgrim_t5f_current_grid_successor_input_audit_runner.mjs", "result": "OWNER_DECISION_REQUIRED"},
            {"id": "T8", "command": "ddonirang-tool run-summary PC01_positive --madi 1", "result": "EXPECTED_RED_E_SHARED_CANONICAL"},
            {"id": "T9", "command": "cargo test -p ddonirang-tool --test v1_fd01_lesson_epoch_inventory -- --nocapture", "result": "PASS_TOTAL_557_V25_PASS_0_PREV25_ONLY_127_NEITHER_430"},
        ],
    }
    write_json("fd01_surface_inventory.detjson", inventory)
    write_json("fd01_successor_dag.detjson", dag)
    write_json("fd01_test_ledger.detjson", tests)
    print(json.dumps({
        "status": "PASS",
        "surfaces": len(surfaces),
        "v25_public_ingress": inventory["current_v25_public_product_ingress_count"],
        "verdict": inventory["verdict"],
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
