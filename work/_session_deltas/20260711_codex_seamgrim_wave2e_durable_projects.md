# 2026-07-11 Codex Session Delta - Seamgrim Wave 2E Durable Projects

## Scope

- Goal: `docs/context/roadmap/CODEX_SUPERLONG_GOAL_SEAMGRIM_WAVE2E_DURABLE_PROJECTS_V1_20260711.md` G0~G9.
- Branch: `codex/queue-20260706`.
- Start HEAD: `50972f3 chore(governance): ignore private archive inputs`.
- Wave2D reference: `44a4e5c`; current HEAD has governance commits `6f27618`, `50972f3` after it.
- Boundary: `docs/ssot/**` read-only, no new DDN syntax, no `state_hash` formula change, no login/cloud/search/collab claim.
- Existing dirty/untracked at start: preserved. Product/test/pack paths for this work were clean; unrelated dirty docs/session/intake files were not staged.

## Read Before Work

- `AGENTS.md`
- `AGENT_WORKFLOW.md`
- `SSOT_POLICY.md`
- `ARTIFACT_POLICY.md`
- `docs/context/all/DEV_SUMMARY.md`
- `work/codex/20260711_user_creation_retention_priority/README.md`
- `work/codex/20260711_idc_pilot_readiness/README.md`
- `docs/ssot/ssot/SSOT_INDEX_v24.12.9.md`
- Relevant SSOT lines in `docs/ssot/ssot/SSOT_DECISIONS_v24.12.9.md` and `README_v24.12.9.md`: Seamgrim save/project/package/registry is shell/server/source-management layer, not core runtime truth.
- `solutions/seamgrim_ui_mvp/ui/platform_contract.js`
- `solutions/seamgrim_ui_mvp/ui/platform_server_adapter_contract.js`
- `solutions/seamgrim_ui_mvp/ui/studio_local_share_package.js`
- `solutions/seamgrim_ui_mvp/ui/app.js`

## G0 Baseline

Commands:

- `python tests/run_seamgrim_wave2d_first_view_authoring_check.py` -> PASS.
- `python tests/run_seamgrim_platform_server_adapter_contract_check.py` -> FAIL before Wave2E changes. Existing harness failure: `appState.studio` missing in `tests/seamgrim_platform_server_adapter_integration_runner.mjs`.
- `python tests/run_seamgrim_platform_server_action_rail_check.py` -> PASS.
- `python tests/run_pack_golden.py studio_local_package_export_action_v1` -> PASS.
- `git status --short -- docs/ssot` -> clean.

G0 failure vectors captured in `pack/seamgrim_wave2e_durable_project_failures_v1/baseline.detjson` by actual browser runner:

- Server save/share UI is still not ready.
- Capability leak guard missing.
- Stale editor-save guard missing.
- Conflict overwrite guard missing.
- View-link escalation guard missing.
- Restart persistence missing.
- Backup/restore missing.

Verification:

- `node tests/seamgrim_wave2e_durable_project_failure_capture_runner.mjs` -> PASS, fixture generated.
- `python tests/run_seamgrim_wave2e_durable_project_failures_check.py` -> PASS.
- `python tests/run_pack_golden.py seamgrim_wave2e_durable_project_failures_v1` -> PASS.
- `git status --short -- docs/ssot` -> clean.

## G0 Status

- Behavior closed: none. G0 is a baseline/failure-vector record.
- Docs closed: none.
- Pending: G1 project snapshot/hash implementation.

## G1 Project Snapshot

Implementation:

- Added `solutions/seamgrim_ui_mvp/ui/project_snapshot.js`.
- Added candidate `seamgrim.project_snapshot.v0` and wrapper `seamgrim.project_snapshot_artifact.v0`.
- Canonical bytes are sorted UTF-8 JSON; `content_sha256` is SHA-256 over those bytes.
- Added app product helper `window.__SEAMGRIM_BUILD_CURRENT_PROJECT_SNAPSHOT__`.
- The helper reads `EditorScreen.getDdn()` and `EditorScreen.getLessonPlanText()` so the visible editor values win over stale `appState.currentLesson`.
- Embedded existing Studio local package payload and kept candidate FNV `package_hash` as compat metadata only.

Evidence:

- `node tests/seamgrim_project_snapshot_runner.mjs` -> PASS.
- `python tests/run_seamgrim_project_snapshot_check.py` -> PASS.
- `python tests/run_pack_golden.py seamgrim_project_snapshot_v0` -> PASS.
- `node --check solutions/seamgrim_ui_mvp/ui/app.js` -> PASS.
- `node --check solutions/seamgrim_ui_mvp/ui/project_snapshot.js` -> PASS.
- `git diff --check -- <G1 paths>` -> PASS.
- `git status --short -- docs/ssot` -> clean.

Status:

- Behavior closed: current editor snapshot/hash builder.
- Docs closed: none.
- Pending: G2 SQLite durable store core.

## G2 SQLite Durable Store

Implementation:

- Added `solutions/seamgrim_ui_mvp/tools/project_store.py`.
- Store root is caller-provided data dir; tests use OS temp outside the repo.
- SQLite metadata uses WAL and foreign keys.
- Snapshot canonical JSON is stored in content-addressed object files under `objects/<sha-prefix>/<sha>.json`.
- Object writes use temp file, flush/fsync, and atomic rename.
- Revisions are append-only and require `expected_parent_revision_id`.
- Restore creates a new revision and records `restore_of_revision_id`.
- Clone creates a new project with origin project/revision lineage.
- Soft delete marks projects deleted without removing objects/revisions.
- Reopening a new `SeamgrimProjectStore` instance over the same data dir preserves project heads and objects.

Evidence:

- `python tests/run_seamgrim_project_store_check.py` -> PASS.
- `python tests/run_pack_golden.py seamgrim_project_store_v0` -> PASS.
- `python -m py_compile solutions/seamgrim_ui_mvp/tools/project_store.py tests/run_seamgrim_project_store_check.py` -> PASS.
- `git diff --check -- <G2 paths>` -> PASS.
- `git status --short -- docs/ssot` -> clean.

Status:

- Behavior closed: local durable store core.
- Docs closed: none.
- Pending: G3 same-origin API and capability client.

## G3 Capability Project API

Implementation:

- Extended `project_store.py` with capability hash storage and role authorization.
- Added same-origin `/api/v1/projects` routes to `ddn_exec_server.py`.
- API supports health, create, read, append revision, list revisions, restore, clone, and soft delete.
- Create/clone return raw edit/view capabilities only in response.
- DB stores only `capability_sha256`, never raw capability.
- API requires `Authorization: Bearer <capability>`.
- View capability can read/list/clone only; edit capability can append/restore/delete.
- Added `solutions/seamgrim_ui_mvp/ui/project_service_client.js`.
- Client builds fragment links, captures fragment capability into `sessionStorage`, scrubs URL fragment, and sends API auth via header.
- Fixed existing `saveCurrentWork("local")` harness regression by guarding missing `appState.studio` and optional shell status update.

Evidence:

- `python tests/run_seamgrim_project_api_capability_check.py` -> PASS.
- `node tests/seamgrim_project_service_client_runner.mjs` -> PASS.
- `python tests/run_seamgrim_platform_server_adapter_contract_check.py` -> PASS.
- `python tests/run_seamgrim_platform_server_action_rail_check.py` -> PASS.
- `python tests/run_pack_golden.py seamgrim_project_api_capability_v0` -> PASS.
- `python -m py_compile solutions/seamgrim_ui_mvp/tools/project_store.py solutions/seamgrim_ui_mvp/tools/ddn_exec_server.py tests/run_seamgrim_project_api_capability_check.py` -> PASS.
- `node --check solutions/seamgrim_ui_mvp/ui/app.js` -> PASS.
- `git diff --check -- <G3 paths>` -> PASS.
- `git status --short -- docs/ssot` -> clean.

Status:

- Behavior closed: same-origin capability API and client contract.
- Docs closed: none.
- Pending: G4 product UI save/reopen workflow.

## G4 Product Save/Reopen Workflow

Implementation:

- Added project name input, server save button, status panel, edit link, and recent project list to the Create screen.
- Wired Create-screen save to the same-origin project API from G3.
- Save creates a project on first save and appends a guarded revision when reopening an existing edit session.
- Edit links carry only fragment capability parameters and clear existing query parameters before sharing.
- Reopen captures the fragment capability into session storage, scrubs it from the URL, fetches the project, restores DDN and `lesson_plan.v0`, and opens the editor.
- Reopened projects can be run through the visible product path: editor shell Lab tab -> `수업 실행`.

Evidence:

- `node tests/seamgrim_project_save_reopen_runner.mjs` -> PASS.
- `python tests/run_seamgrim_project_save_reopen_check.py` -> PASS.
- `python tests/run_pack_golden.py seamgrim_project_save_reopen_v0` -> PASS.
- `node --check solutions/seamgrim_ui_mvp/ui/app.js` -> PASS.
- `node --check tests/seamgrim_project_save_reopen_runner.mjs` -> PASS.
- `python -m py_compile tests/run_seamgrim_project_save_reopen_check.py` -> PASS.
- `git diff --check -- <G4 paths>` -> PASS.
- `git status --short -- docs/ssot` -> clean.

Status:

- Behavior closed: save-as project, edit-link reopen, URL fragment scrub, and run-after-reopen product workflow.
- Docs closed: none.
- Pending: G5 view-link and clone workflow.

## G5 View Link And Clone Workflow

Implementation:

- Added a view-link anchor and `내 버전 만들기`/clone button to the project save panel.
- First save records both edit and view capability links; both are fragment links, never query parameters.
- View-capability project open is read-only, hides edit-link exposure, disables original save, and keeps clone available.
- Clone uses the same-origin `/api/v1/projects/{project_id}/clone` endpoint and switches the browser into a new edit session for the clone.
- Clone lineage now preserves `source_project_id`, `source_revision_id`, `origin_content_sha256`, and `origin_kind`.
- Project snapshot lineage is preserved across subsequent clone saves.
- Clone edits append to the clone project and leave the original project head/content unchanged.

Evidence:

- `node tests/seamgrim_project_share_clone_runner.mjs` -> PASS.
- `python tests/run_seamgrim_project_share_clone_check.py` -> PASS.
- `python tests/run_pack_golden.py seamgrim_project_share_clone_v0` -> PASS.
- `python tests/run_seamgrim_project_api_capability_check.py` -> PASS.
- `python tests/run_seamgrim_project_save_reopen_check.py` -> PASS.
- `python tests/run_pack_golden.py seamgrim_project_save_reopen_v0 seamgrim_project_api_capability_v0` -> PASS.
- `node --check solutions/seamgrim_ui_mvp/ui/app.js` -> PASS.
- `node --check solutions/seamgrim_ui_mvp/ui/project_snapshot.js` -> PASS.
- `node --check tests/seamgrim_project_share_clone_runner.mjs` -> PASS.
- `python -m py_compile solutions/seamgrim_ui_mvp/tools/project_store.py solutions/seamgrim_ui_mvp/tools/ddn_exec_server.py tests/run_seamgrim_project_share_clone_check.py` -> PASS.
- `git diff --check -- <G5 paths>` -> PASS.
- `git status --short -- docs/ssot` -> clean.

Status:

- Behavior closed: view-link read-only open, clone-as-my-version, origin lineage, and original immutability after clone edit.
- Docs closed: none.
- Pending: G6 revision history, conflict, and restore UI.

## G6 Revision, Conflict, Restore UI

Implementation:

- Added revision list UI to the project save panel.
- Revision rows expose revision id, parent revision id, content SHA, package hash, and restore source when present.
- Save continues to send `expected_parent_revision_id = appState.shell.currentRevisionId`.
- Two edit contexts from the same head now surface a visible conflict panel instead of overwriting.
- Conflict panel distinguishes server head/content from the local stale head and provides a local package preservation action.
- Restore calls `/api/v1/projects/{project_id}/restore` and creates a new head revision instead of overwriting history.

Evidence:

- `node tests/seamgrim_project_revision_conflict_restore_runner.mjs` -> PASS.
- `python tests/run_seamgrim_project_revision_conflict_restore_check.py` -> PASS.
- `python tests/run_pack_golden.py seamgrim_project_revision_conflict_restore_v0 seamgrim_project_share_clone_v0 seamgrim_project_save_reopen_v0 seamgrim_project_api_capability_v0 seamgrim_project_store_v0` -> PASS.
- `python tests/run_seamgrim_project_share_clone_check.py` -> PASS.
- `python tests/run_seamgrim_project_save_reopen_check.py` -> PASS.
- `python tests/run_seamgrim_project_api_capability_check.py` -> PASS.
- `python tests/run_seamgrim_project_store_check.py` -> PASS.
- `node --check solutions/seamgrim_ui_mvp/ui/app.js` -> PASS.
- `node --check tests/seamgrim_project_revision_conflict_restore_runner.mjs` -> PASS.
- `python -m py_compile tests/run_seamgrim_project_revision_conflict_restore_check.py solutions/seamgrim_ui_mvp/tools/project_store.py solutions/seamgrim_ui_mvp/tools/ddn_exec_server.py` -> PASS.
- `git diff --check -- <G6 paths>` -> PASS.
- `git status --short -- docs/ssot` -> clean.

Status:

- Behavior closed: stale edit conflict, local package preservation surface, revision audit list, and restore-as-new-revision.
- Docs closed: none.
- Pending: G7 restart, backup, and recovery.

## G7 Restart, Backup, Recovery

Implementation:

- Added project-store `audit_integrity()` for SQLite/object consistency.
- Backup now refuses to proceed when integrity diagnostics are present.
- Restore into a new data dir re-runs integrity audit before returning a usable store.
- Audit diagnostics cover missing object files, object SHA mismatch, revision object path mismatch, missing parent/restore refs, missing head refs, and invalid capability hash shape.
- Added browser restart runner: save project, stop server, restart with same data dir, reopen edit/view capability links, and verify fragment scrub/read-only/editable semantics still hold.
- Hardened the G6 runner to avoid timing assumptions around conflict panel and revision row ordering.

Evidence:

- `node tests/seamgrim_project_restart_links_runner.mjs` -> PASS.
- `python tests/run_seamgrim_project_restart_backup_recovery_check.py` -> PASS.
- `python tests/run_pack_golden.py seamgrim_project_restart_backup_recovery_v0 seamgrim_project_revision_conflict_restore_v0 seamgrim_project_share_clone_v0 seamgrim_project_save_reopen_v0 seamgrim_project_api_capability_v0 seamgrim_project_store_v0` -> PASS.
- `python tests/run_seamgrim_project_revision_conflict_restore_check.py` -> PASS.
- `python tests/run_seamgrim_project_share_clone_check.py` -> PASS.
- `python -m py_compile solutions/seamgrim_ui_mvp/tools/project_store.py tests/run_seamgrim_project_restart_backup_recovery_check.py` -> PASS.
- `node --check tests/seamgrim_project_restart_links_runner.mjs` -> PASS.
- `git diff --check -- <G7 paths>` -> PASS.
- `git status --short -- docs/ssot` -> clean.

Status:

- Behavior closed: restart-safe edit/view links, local backup/restore, and integrity diagnostics.
- Docs closed: none.
- Pending: G8 viewport/accessibility/regression gate.

## G8 Four-Viewport Product Gate

Implementation:

- Added a full workflow browser runner for `1440x900`, `1280x720`, `1024x768`, and `390x844`.
- The runner opens the pendulum lesson, edits DDN and `lesson_plan.v0`, saves as `나의 진자 실험`, closes the first context, reopens the edit link, verifies both edits, saves a new revision, opens the view link read-only, clones into a new project, restarts the local server, and reopens original and clone.
- The runner checks bounding/overflow, keyboard tab focus, icon tooltip/accessibility names, canvas nonblank pixels, run hash, and trace/replay stability boundary.

Evidence:

- `node tests/seamgrim_project_full_workflow_viewport_runner.mjs` -> PASS.
- `python tests/run_seamgrim_project_full_workflow_viewport_check.py` -> PASS.
- `python tests/run_pack_golden.py seamgrim_project_full_workflow_viewport_v0 seamgrim_project_restart_backup_recovery_v0 seamgrim_project_revision_conflict_restore_v0 seamgrim_project_share_clone_v0 seamgrim_project_save_reopen_v0` -> PASS.
- `python tests/run_seamgrim_project_restart_backup_recovery_check.py` -> PASS.
- `python tests/run_seamgrim_project_revision_conflict_restore_check.py` -> PASS.
- `node --check tests/seamgrim_project_full_workflow_viewport_runner.mjs` -> PASS.
- `python -m py_compile tests/run_seamgrim_project_full_workflow_viewport_check.py` -> PASS.
- `git status --short -- docs/ssot` -> clean.

Status:

- Behavior closed: required four-viewport durable project workflow and product quality gate.
- Docs closed: none.
- Pending: G9 final regression and handoff.

## G9 Final Regression And Handoff

Implementation:

- Fixed a Wave 2B representative-world regression found during final G9: `rep_phys_projectile_xy_v1` sometimes rendered graph-derived fallback shapes as `graph_series` and omitted `vector_arrow`.
- The product runtime now applies lesson `view_roles` before declared `space2d` fallback and decorates projectile graph fallback with read-only `trajectory_trail`/`vector_arrow` measurement roles.
- The vector arrow uses explicit `vx/vy` when present and falls back to the previous/current drawn points when the first browser frame has only graph/position evidence.
- No DDN syntax, `state_hash` formula, or `docs/ssot/**` files were changed.
- Sanity gate regenerated `pack/open_bundle_artifact/run_bundle/geoul.diag.jsonl` and `pack/open_end_to_end/open.log.jsonl`; both were restored to the pre-run tracked state.

Evidence:

- `python tests/run_seamgrim_project_snapshot_check.py` -> PASS.
- `python tests/run_seamgrim_project_store_check.py` -> PASS.
- `python tests/run_seamgrim_project_api_capability_check.py` -> PASS.
- `python tests/run_seamgrim_project_save_reopen_check.py` -> PASS.
- `python tests/run_seamgrim_project_share_clone_check.py` -> PASS.
- `python tests/run_seamgrim_project_revision_conflict_restore_check.py` -> PASS.
- `python tests/run_seamgrim_project_restart_backup_recovery_check.py` -> PASS.
- `python tests/run_seamgrim_project_full_workflow_viewport_check.py` -> PASS.
- `python tests/run_pack_golden.py seamgrim_wave2e_durable_project_failures_v1 seamgrim_project_snapshot_v0 seamgrim_project_store_v0 seamgrim_project_api_capability_v0 seamgrim_project_save_reopen_v0 seamgrim_project_share_clone_v0 seamgrim_project_revision_conflict_restore_v0 seamgrim_project_restart_backup_recovery_v0 seamgrim_project_full_workflow_viewport_v0` -> PASS.
- `python tests/run_seamgrim_platform_server_adapter_contract_check.py` -> PASS.
- `python tests/run_seamgrim_platform_server_action_rail_check.py` -> PASS.
- `python tests/run_pack_golden.py studio_local_package_export_action_v1` -> PASS.
- `python tests/run_seamgrim_publish_screen_isolation_check.py` -> PASS.
- `python tests/run_seamgrim_wave2d_first_view_authoring_check.py` -> PASS.
- `python tests/run_seamgrim_wave2c_first_success_check.py` -> PASS.
- `python tests/run_seamgrim_wave2c_local_success_check.py` -> PASS.
- `python tests/run_seamgrim_wave2b_representative_worlds_check.py` -> PASS after the product fallback-role fix.
- `python tests/run_seamgrim_wave2b_quality_gate_check.py` -> PASS.
- `python tests/run_seamgrim_pendulum_surface_contract_check.py` -> PASS.
- `python tests/run_seamgrim_pendulum_view_plan_product_check.py` -> PASS.
- `python tests/run_pack_golden.py age2_phys_pendulum_v1 seamgrim_pendulum_view_plan_product_v1` -> PASS.
- `cargo check` -> PASS with pre-existing dead-code warnings.
- `cargo check --manifest-path tools/teul-cli/Cargo.toml` -> PASS.
- `python tests/run_ci_sanity_gate.py --profile core_lang` -> PASS.
- `git diff --check` -> PASS; Git reported CRLF normalization warnings for existing dirty files and the edited JS file.
- `git status --short -- docs/ssot` -> clean.

Observed stale checks not used as Wave 2E evidence:

- `python tests/run_studio_local_share_and_packaging_check.py` still depends on old `DEV_SUMMARY.md` marker tokens.
- `python tests/run_studio_local_packaging_consolidation_check.py` still depends on old `DEV_SUMMARY.md` marker/progress tokens.
- `node tests/studio_local_package_export_action_runner.mjs` is a broad legacy integration runner with stale assumptions from before the independent `#screen-publish` split. I reverted my exploratory edit and did not include it in the commit.

Status:

- Behavior closed: durable server-backed project save/reopen, append-only revisions, stale-write conflict rejection, view/edit capability separation, read-only share links, clone-as-my-version, server restart, local backup/restore, integrity diagnostics, and four-viewport product workflow.
- Docs closed: candidate `seamgrim.project_snapshot.v0`, project API/capability contract, and local IDC-readiness shape as pack/report evidence only.
- Pending and explicitly not claimed: accounts, team permissions, public project search, real-time collaboration, multi-node HA, cryptographic package signing, actual IDC deployment, and global Korean Manim completion.
- Data dirs: all project-store/browser tests used temp dirs or local ephemeral servers; no project data dir was left inside the repo.
- Final commit target: `chore(seamgrim): record durable project verification`.
