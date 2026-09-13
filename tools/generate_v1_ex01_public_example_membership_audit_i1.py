#!/usr/bin/env python3
"""Generate the read-only V1 public-example membership candidate ledger."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "work" / "codex" / "20260827_ddn_v1_ex01_public_example_membership_audit_i1"


def sha256(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def write(name: str, value: object) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def row(
    id: str,
    path: str,
    role: str,
    pre_v25: bool,
    v25: bool,
    pre_error: str,
    v25_error: str,
    migration_tier: str,
    rights: str,
    disposition: str,
) -> dict:
    return {
        "id": id,
        "path": path,
        "sha256": sha256(path),
        "role": role,
        "pre_v25_parse": pre_v25,
        "v25_parse": v25,
        "pre_v25_error_family": pre_error,
        "v25_error_family": v25_error,
        "migration_tier": migration_tier,
        "rights": rights,
        "disposition": disposition,
        "release_member": False,
    }


def main() -> None:
    spec = [
        ("SPEC01", "01_result_and_optional.ddn", False, "E_V25_DEFINITION_MIGRATION_REQUIRED"),
        ("SPEC02", "02_generic_static_header.ddn", False, "UNCLASSIFIED"),
        ("SPEC03", "03_bytes_and_exact_number.ddn", False, "E_V25_DEFINITION_MIGRATION_REQUIRED"),
        ("SPEC04", "04_function_and_optional_map.ddn", False, "E_V25_DEFINITION_MIGRATION_REQUIRED"),
        ("SPEC05", "05_pack_kinds.ddn", False, "E_V25_DEFINITION_MIGRATION_REQUIRED"),
        ("SPEC06", "06_observation_and_mol.ddn", True, "E_V25_DEFINITION_MIGRATION_REQUIRED"),
        ("SPEC07", "07_common_model.ddn", False, "E_V25_DEFINITION_MIGRATION_REQUIRED"),
    ]
    rows = [
        row(
            id,
            f"publish/spec/v0.5.0/examples/{name}",
            "PUBLIC_SPEC_DOCS_FIRST",
            pre,
            False,
            "NONE" if pre else "UNCLASSIFIED",
            v25_error,
            "SPEC_SUCCESSOR_ONLY",
            "PUBLICATION_PRESENT_FINAL_LICENSE_OPEN",
            "KEEP_DOCS_ONLY_UNTIL_PRODUCT_CONVERGENCE",
        )
        for id, name, pre, v25_error in spec
    ]
    rows.extend([
        row(
            "PC01",
            "pack/ddn_v25_pc01_definition_binding_v1/positive_definition_binding.ddn",
            "PUBLIC_CONFORMANCE_CANDIDATE",
            False,
            True,
            "UNCLASSIFIED",
            "NONE",
            "TIER_0_ALREADY_V25",
            "OWNER_CONFIRMATION_REQUIRED",
            "PROPOSE_AFTER_TARGETED_PLAIN_PASS_AND_RIGHTS",
        ),
        row(
            "HELLO",
            "pack/edu_ddn_mc_l01_hello_det/lesson.ddn",
            "FIRST_RUN_CANDIDATE",
            True,
            False,
            "NONE",
            "E_V25_DEFINITION_MIGRATION_REQUIRED",
            "TIER_1_SELECTED_MIGRATION",
            "AUDIT_REQUIRED",
            "PROPOSE_FOR_FIRST_RUN_WORKFLOW",
        ),
        row(
            "PROJECTILE",
            "pack/edu_seamgrim_rep_phys_projectile_xy_v1/lesson.ddn",
            "PHYSICS_SHOWCASE_CANDIDATE",
            True,
            False,
            "NONE",
            "E_V25_DEFINITION_MIGRATION_REQUIRED",
            "TIER_2_AFTER_CORE",
            "OWNER_CONFIRMATION_REQUIRED",
            "DEFER_UNTIL_RIGHTS_AND_CORE_WORKFLOW",
        ),
        row(
            "GRID_CURRENT",
            "solutions/seamgrim_ui_mvp/lessons/rep_grid_game_state_drop_v1/lesson.ddn",
            "WORKBENCH_CURRENT_GRID_CANDIDATE",
            True,
            False,
            "NONE",
            "E_V25_DEFINITION_MIGRATION_REQUIRED",
            "TIER_1_SELECTED_MIGRATION",
            "AUDIT_REQUIRED",
            "PROPOSE_WITH_NATIVE_GRID_RESULT",
        ),
        row(
            "CONSOLE_VIEW",
            "pack/bogae_backend_parity_console_web_v1/fixtures/input.ddn",
            "RENDERER_PARITY_REGRESSION_CANDIDATE",
            False,
            False,
            "UNCLASSIFIED",
            "E_V25_DEFINITION_MIGRATION_REQUIRED",
            "TIER_2_AFTER_CORE",
            "AUDIT_REQUIRED",
            "DEFER_UNTIL_V25_SOURCE_AND_NATIVE_VIEW",
        ),
        row(
            "GRID2D_VIEW",
            "pack/bogae_grid2d_smoke_v1/fixtures/input.ddn",
            "RENDERER_GRID2D_REGRESSION_CANDIDATE",
            False,
            False,
            "UNCLASSIFIED",
            "E_V25_DEFINITION_MIGRATION_REQUIRED",
            "TIER_2_AFTER_CORE",
            "AUDIT_REQUIRED",
            "DEFER_UNTIL_V25_SOURCE_AND_NATIVE_VIEW",
        ),
        row(
            "RICH_TEXT",
            "pack/seamgrim_console_rich_markup_v1/input.ddn",
            "TEXT_UI_CANDIDATE",
            True,
            False,
            "NONE",
            "E_V25_DEFINITION_MIGRATION_REQUIRED",
            "TIER_2_AFTER_CORE",
            "AUDIT_REQUIRED",
            "DEFER_FROM_MINIMUM_FIRST_RUN",
        ),
        row(
            "TENSOR",
            "pack/tensor_stdlib_phase0/input.ddn",
            "BASIC_TENSOR_CANDIDATE",
            True,
            False,
            "NONE",
            "E_V25_DEFINITION_MIGRATION_REQUIRED",
            "TIER_1_SELECTED_MIGRATION",
            "AUDIT_REQUIRED",
            "PROPOSE_AFTER_BASIC_TENSOR_R1_CONTRACT",
        ),
    ])
    ledger = {
        "schema": "ddn.v1.ex01.public_example_membership_candidate.i1.v1",
        "baseline": "07c0ba1f21c047f8339334d1a4191f0bf6ee4f1a",
        "authority": {
            "internal_ssot": "v25.15.0",
            "public_language_spec": "v0.5.0",
            "authoritative_v1_membership_rows": 0,
        },
        "counts": {
            "candidate_rows": len(rows),
            "public_spec_docs_first": 7,
            "pre_v25_parse": sum(item["pre_v25_parse"] for item in rows),
            "v25_parse": sum(item["v25_parse"] for item in rows),
            "neither_parser": sum(not item["pre_v25_parse"] and not item["v25_parse"] for item in rows),
            "proposed_tier_0_or_1": sum(item["migration_tier"] in {"TIER_0_ALREADY_V25", "TIER_1_SELECTED_MIGRATION"} for item in rows),
            "release_members": sum(item["release_member"] for item in rows),
        },
        "rows": rows,
        "recommended_first_migration_ids": ["PC01", "HELLO", "GRID_CURRENT", "TENSOR"],
        "rights_clean_release_membership_authorized": False,
        "product_implementation_authorized": False,
        "verdict": "EX01_CANDIDATE_LEDGER_READY_MEMBERSHIP_0",
    }
    dag = {
        "schema": "ddn.v1.ex01.public_example_migration_dag.v1",
        "nodes": [
            {"id": "E0", "name": "bind_fd01_owner_direction", "depends_on": []},
            {"id": "E1", "name": "bind_pc01_targeted_plain_pass", "depends_on": []},
            {"id": "E2", "name": "resolve_selected_example_rights", "depends_on": []},
            {"id": "E3", "name": "migrate_hello_to_v25", "depends_on": ["E0", "E2"]},
            {"id": "E4", "name": "bind_pc01_as_public_conformance_candidate", "depends_on": ["E1", "E2"]},
            {"id": "E5", "name": "migrate_tensor_after_basic_tensor_r1", "depends_on": ["E0", "E2"]},
            {"id": "E6", "name": "migrate_grid_and_land_native_result", "depends_on": ["E0", "E2"]},
            {"id": "E7", "name": "run_same_source_cli_wasm_workbench_parity", "depends_on": ["E3", "E4", "E5", "E6"]},
            {"id": "E8", "name": "fresh_independent_review", "depends_on": ["E7"]},
            {"id": "E9", "name": "owner_promote_exact_release_membership", "depends_on": ["E8"]},
        ],
        "forbidden": [
            "TREAT_PUBLIC_SPEC_DOCS_EXAMPLES_AS_EXECUTABLE_PRODUCT_PASS",
            "COPY_RIGHTS_OPEN_FIXTURE_TO_PUBLIC_SOURCE",
            "MIGRATE_ALL_557_AS_ONE_GATE",
            "SILENT_SOURCE_EPOCH_FALLBACK",
            "SELF_PROMOTE_RELEASE_MEMBERSHIP",
        ],
    }
    write("example_candidate_ledger.detjson", ledger)
    write("example_migration_dag.detjson", dag)
    print(json.dumps({"status": "PASS", **ledger["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()

