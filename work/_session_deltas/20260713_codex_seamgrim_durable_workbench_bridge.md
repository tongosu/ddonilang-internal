# 2026-07-13 Codex — Seamgrim durable workbench bridge

## Goal

- Roadmap: `docs/context/roadmap/CODEX_SUPERLONG_GOAL_SEAMGRIM_WORKBENCH_DURABLE_PROJECT_RUN_LINEAGE_BRIDGE_V1_20260713.md`.
- Branch: `codex/queue-20260706`.
- START_HEAD: `ed62d7b docs(ai): align web context with ssot v24.13.0`.
- Owner-approved brief: `docs/context/briefs/BRIEF_SEAMGRIM_DDN_DETERMINISTIC_PROJECT_WORKBENCH_UI_V1_20260712.md`.
- Fixed decisions: `1C-2C-3B-4B-5B-6C-7C-8B-9C`.

## Boundaries

- `docs/ssot/**` read-only.
- No default shell switch.
- No new DDN syntax.
- No runtime `state_hash` formula change.
- No multi-module resolver, public registry, login/team/cloud, IDC deployment, or HA claim.
- Existing unrelated dirty/untracked files preserved and not staged.

## G0 Baseline

- Hard-blocker product paths were clean:
  - `solutions/seamgrim_ui_mvp/ui/workbench/**`
  - `solutions/seamgrim_ui_mvp/ui/project_snapshot.js`
  - `solutions/seamgrim_ui_mvp/ui/project_service_client.js`
  - `solutions/seamgrim_ui_mvp/tools/project_store.py`
  - `solutions/seamgrim_ui_mvp/tools/ddn_exec_server.py`
- Default server port: `8787`.
- Default data dir: `I:/home/urihanl/ddn/codex/build/seamgrim_project_data` when `SEAMGRIM_PROJECT_DATA_DIR` is unset.
- Baseline report: `docs/reports/impl/SEAMGRIM_WORKBENCH_DURABLE_BRIDGE_BASELINE_V1_20260713.md`.

## Existing Assets To Reuse

- Project snapshot: `seamgrim.project_snapshot.v0`, `seamgrim.project_snapshot_artifact.v0`.
- Project store: SQLite metadata + content-addressed objects + append-only project revisions.
- Project API: `/api/v1/projects` create/read/revisions/restore/clone/delete.
- Capability client: fragment link capture, session storage, URL scrub, Authorization bearer helper.
- Workbench path: `solutions/seamgrim_ui_mvp/ui/workbench/index.html`.
- WASM path: `createWasmVm`/sealed `DdnWasmVmClient` product execution.

## G0 Verification

PASS:

- `python tests/run_seamgrim_approved_workbench_shell_check.py`
- `python tests/run_seamgrim_approved_workbench_runtime_lineage_check.py` (standalone rerun; first parallel run timed out)
- `python tests/run_seamgrim_approved_workbench_semantic_verticals_check.py`
- `python tests/run_seamgrim_approved_workbench_quality_gate_check.py`
- `python tests/run_seamgrim_approved_workbench_promotion_packet_check.py`
- `python tests/run_seamgrim_project_store_check.py`
- `python tests/run_seamgrim_project_save_reopen_check.py`
- `python tests/run_seamgrim_project_share_clone_check.py`
- `python tests/run_seamgrim_project_revision_conflict_restore_check.py`
- `python tests/run_seamgrim_project_restart_backup_recovery_check.py`
- `python tests/run_seamgrim_project_full_workflow_viewport_check.py`
- `python tests/run_seamgrim_wave2e_durable_project_failures_check.py`
- `python tests/run_ddn_cli_wasm_freshness_check.py`
- `python tests/run_ddn_cli_wasm_true_parity_equality_check.py`
- `python tests/run_ddn_cli_wasm_sync_gate_check.py`
- `python tests/run_seamgrim_view_only_state_hash_invariant_check.py`
- `python tests/run_ci_sanity_gate.py --profile core_lang`
- `git status --short -- docs/ssot` no output.

## Next

- G1: isolate workbench persistence adapters.
- G2: connect workbench save/open to existing server project revisions.

## G1-G10 Completion

- G1 `9b41d2a`: workbench persistence adapters and explicit local fallback boundary.
- G2 `9a49926`: server project create/open/save from workbench.
- G3 `4ce64c5`: revision conflict panel and restore-as-new-revision.
- G4 `d0b7602`: append-only run archive store and HTTP API.
- G5 `6dfc2f2`: sealed WASM run checkpoints, finalize, and branch lineage.
- G6 `4f373f0`: edit/view capability split and clone workflow.
- G7 `46ea005`: local "내 작업" capability index and restart reopen.
- G8 `f5a672d`: storage security/recovery gate for run archive.
- G9 `6eae8c1`: integrated workflow and four viewport browser gate.
- G10: durable quality gate and promotion packet.

## G10 Artifacts

- Quality gate: `python tests/run_seamgrim_workbench_durable_quality_gate_check.py`.
- Promotion packet: `docs/reports/impl/SEAMGRIM_WORKBENCH_DURABLE_BRIDGE_PROMOTION_PACKET_V1_20260713.md`.

## Remaining Open Boundaries

- No default shell switch.
- No login/team/cloud/public registry.
- No actual IDC deployment/HA/TLS.
- No new DDN syntax or runtime `state_hash` formula change.

## Final Verification

PASS:

- `python tests/run_seamgrim_workbench_durable_quality_gate_check.py`
- `python tests/run_pack_golden.py seamgrim_workbench_durable_persistence_adapters_v1 seamgrim_workbench_server_project_save_reopen_v1 seamgrim_workbench_revision_conflict_restore_v1 seamgrim_workbench_run_archive_store_v1 seamgrim_workbench_run_archive_lineage_v1 seamgrim_workbench_capability_share_clone_v1 seamgrim_workbench_my_work_reopen_v1 seamgrim_workbench_storage_security_recovery_v1 seamgrim_workbench_durable_full_workflow_viewport_v1 seamgrim_workbench_durable_quality_gate_v1`
- `python tests/run_seamgrim_approved_workbench_shell_check.py`
- `python tests/run_seamgrim_approved_workbench_runtime_lineage_check.py`
- `python tests/run_seamgrim_approved_workbench_semantic_verticals_check.py`
- `python tests/run_seamgrim_approved_workbench_quality_gate_check.py`
- `python tests/run_seamgrim_approved_workbench_promotion_packet_check.py`
- `python tests/run_seamgrim_project_store_check.py`
- `python tests/run_seamgrim_project_save_reopen_check.py`
- `python tests/run_seamgrim_project_share_clone_check.py`
- `python tests/run_seamgrim_project_revision_conflict_restore_check.py` (first browser timeout rerun passed)
- `python tests/run_seamgrim_project_restart_backup_recovery_check.py`
- `python tests/run_seamgrim_project_full_workflow_viewport_check.py`
- `python tests/run_seamgrim_wave2e_durable_project_failures_check.py`
- `python tests/run_ddn_cli_wasm_freshness_check.py`
- `python tests/run_ddn_cli_wasm_true_parity_equality_check.py`
- `python tests/run_ddn_cli_wasm_sync_gate_check.py`
- `python tests/run_seamgrim_view_only_state_hash_invariant_check.py`
- `cargo check`
- `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- `cargo test -p ddonirang-tool --no-run`
- `python tests/run_ci_sanity_gate.py --profile core_lang`
- `git diff --check`
- `git status --short -- docs/ssot`

Notes:

- `core_lang` refreshed open replay logs; restored generated changes in `pack/open_bundle_artifact/run_bundle/geoul.diag.jsonl` and `pack/open_end_to_end/open.log.jsonl`.

## G9 Representative Project Audit Fix

- Found a completion-audit gap: the original G9 browser runner proved the integrated durable workflow and four viewports, but did not separately prove both required representative projects.
- Fixed product session isolation: selecting a catalog project now clears the previous server capability session and server project state, so saving `rep_grid_game_state_drop_v1` after `rep_phys_pendulum_wave1_v1` creates its own server project instead of appending to the earlier project.
- Extended `tests/seamgrim_workbench_durable_full_workflow_viewport_runner.mjs` to run save/run/checkpoint/stop/branch/view-clone/reopen for both:
  - `rep_phys_pendulum_wave1_v1`
  - `rep_grid_game_state_drop_v1`

PASS:

- `python tests/run_seamgrim_workbench_durable_full_workflow_viewport_check.py`
- `python tests/run_seamgrim_workbench_durable_quality_gate_check.py`
- `python tests/run_pack_golden.py seamgrim_workbench_durable_full_workflow_viewport_v1 seamgrim_workbench_durable_quality_gate_v1`
- `git diff --check`
- `git status --short -- docs/ssot`
