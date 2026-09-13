# 2026-07-13 Codex Session Delta - Seamgrim Public Physics Wedge

## G0 Baseline

- START_HEAD: `e9b7bdf`
- Branch: `codex/queue-20260706`
- Minimum ancestor: `e9b7bdf` is an ancestor of START_HEAD.
- Current SSOT index: `SSOT_INDEX_v24.14.0.md`
- `docs/ssot/**`: clean.
- Product target paths were clean before changes.
- Existing unrelated dirty/untracked files are preserved and excluded.

## Findings

- Current server default routes `/`, `/index.html`, `/ui`, `/ui/` still serve the legacy shell.
- Approved workbench exists at `solutions/seamgrim_ui_mvp/ui/workbench/index.html`.
- Projectile source/view assets exist under `solutions/seamgrim_ui_mvp/lessons/rep_phys_projectile_xy_v1/`, but the approved workbench project list currently starts with pendulum.
- First-user blockers are entry, projectile first-run, explicit one-file DDN creation, and public-wedge-specific save/share/reopen proof.

## G0 Verification

- PASS: `python tests/run_seamgrim_approved_workbench_promotion_packet_check.py`
- PASS: `python tests/run_seamgrim_workbench_durable_quality_gate_check.py`
- PASS: `python tests/run_seamgrim_workbench_server_project_save_reopen_check.py`
- PASS: `python tests/run_seamgrim_workbench_durable_persistence_adapters_check.py`
- PASS: `python tests/run_seamgrim_workbench_capability_share_clone_check.py`
- PASS: `python tests/run_seamgrim_workbench_durable_full_workflow_viewport_check.py`
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS: `python tests/run_ddn_cli_wasm_true_parity_equality_check.py`
- PASS: `python tests/run_ddn_cli_wasm_sync_gate_check.py`
- PASS: `python tests/run_seamgrim_view_only_state_hash_invariant_check.py`
- PASS: `cargo check`
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS: `python tests/run_ci_sanity_gate.py --profile core_lang`

Logs: `out/seamgrim_public_wedge_g0/`.

## Boundaries

- No SSOT edits.
- No DDN syntax changes.
- No `state_hash` formula changes.
- No legacy shell deletion.
- No IDC or external-user success claim.

## Next

- G1: promote approved workbench as reversible default route while preserving explicit legacy compatibility path.

## G1 Default Route

- Implemented a reversible server routing boundary in `solutions/seamgrim_ui_mvp/tools/ddn_exec_server.py`.
- Default routes `/`, `/index.html`, `/ui`, `/ui/`, and plain `/ui/index.html` now redirect to the approved workbench.
- Explicit legacy routes `/legacy.html` and `/solutions/seamgrim_ui_mvp/ui/legacy.html` continue to serve the legacy shell.
- Old deep links with `legacy`, `tab`, `screen`, or `route` query keys fall back to the legacy shell.
- Capability-like query keys are not preserved through default redirects.

### G1 Verification

- PASS: `python tests/run_seamgrim_public_default_route_check.py`
- PASS: `python tests/run_seamgrim_approved_workbench_promotion_packet_check.py`
- PASS: `git diff --check` (warnings only for pre-existing CRLF normalization notices)
- PASS: `git status --short -- docs/ssot`

## G2 Public Physics First Run

- Added `rep_phys_projectile_xy_v1` as the first approved workbench project.
- Kept the projectile DDN source loaded from `solutions/seamgrim_ui_mvp/lessons/rep_phys_projectile_xy_v1/lesson.ddn`.
- Added deterministic projectile canvas rendering from DDN setup values, plus named semantic observations with units.
- Preserved pendulum/grid/line workbench projects and updated the existing shell runner to expect projectile as the new first project.
- Browser verification clicks the actual run button and waits for a WASM-produced `state_hash`.

### G2 Verification

- PASS: `python tests/run_seamgrim_public_physics_first_run_check.py`
- PASS: `python tests/run_seamgrim_approved_workbench_shell_check.py`
- PASS: `python tests/run_seamgrim_approved_workbench_promotion_packet_check.py`
- PASS: `python tests/run_seamgrim_public_default_route_check.py`
- PASS: `git diff --check` (warnings only for pre-existing CRLF normalization notices)
- PASS: `git status --short -- docs/ssot`

## G3 One-File DDN Create/Edit/Run

- Added the product command `새 DDN` in the workbench project rail.
- `새 DDN` creates `local_one_file_ddn_v1`, a local single-file project, not an example clone.
- The initial source is a valid minimal DDN file.
- Unsaved edits are recorded as local recovery and are not labeled as server saved.
- Browser reload plus `새 DDN` restores the local draft.
- Empty source is rejected before WASM as `E_SOURCE_EMPTY`; actual runtime failures remain in the existing WASM diagnostic path.

### G3 Verification

- PASS: `python tests/run_seamgrim_one_file_ddn_create_run_check.py`
- PASS: `python tests/run_seamgrim_public_default_route_check.py`
- PASS: `python tests/run_seamgrim_public_physics_first_run_check.py`
- PASS: `python tests/run_seamgrim_approved_workbench_shell_check.py`
- PASS: `git diff --check` (warnings only for pre-existing CRLF normalization notices)
- PASS: `git status --short -- docs/ssot`

## G4 First Physics Change Storyboard

- Added candidate-vs-committed source distinction via `data-source-dirty` and run-status text.
- Edited DDN source values immediately update projectile observations and canvas without mutating runtime state.
- Browser runner performs the product storyboard: open official projectile, run, edit gravity, confirm changed trajectory, run again, save server revision, produce view link.
- Automation timing is not recorded as a human 90-second success claim.

### G4 Verification

- PASS: `python tests/run_seamgrim_public_physics_change_storyboard_check.py`
- PASS: `python tests/run_seamgrim_one_file_ddn_create_run_check.py`
- PASS: `python tests/run_seamgrim_public_physics_first_run_check.py`
- PASS: `python tests/run_seamgrim_public_default_route_check.py`
- PASS: `git diff --check` (warnings only for pre-existing CRLF normalization notices)
- PASS: `git status --short -- docs/ssot`

## G5 Share/Clone/Reopen

- Added public projectile creator/viewer browser workflow coverage.
- Creator saves the edited projectile source to a server revision, then runs it so server run archive evidence exists.
- Independent viewer context opens a view capability, has save disabled, and debug save is rejected with `E_PROJECT_VIEW_WRITE_REJECTED`.
- Viewer creates an editable clone with a distinct project id.
- Server restarts on the same origin and durable data dir; creator opens `내 작업` and reloads the saved server project.

### G5 Verification

- PASS: `python tests/run_seamgrim_public_share_clone_reopen_check.py`
- PASS: `python tests/run_seamgrim_public_physics_change_storyboard_check.py`
- PASS: `python tests/run_seamgrim_workbench_capability_share_clone_check.py`
- PASS: `python tests/run_seamgrim_workbench_server_project_save_reopen_check.py`
- PASS: `git diff --check` (warnings only for pre-existing CRLF normalization notices)
- PASS: `git status --short -- docs/ssot`

## G6 Legacy Compatibility

- Added known project query routing for `project`, `project_id`, `lesson`, `lesson_id`, and `source_lesson_id`.
- Known ids map to the approved workbench; unknown project/lesson ids fall back to legacy.
- `tab`/legacy-style deep links continue to serve the legacy shell.
- Preserved `/solutions/seamgrim_ui_mvp/ui/index.html` as the legacy shell address because legacy capability links carry fragments that the server cannot inspect.
- Updated durable persistence/restart runners whose old first-project/default-route assumptions conflicted with the public workbench promotion.

### G6 Verification

- PASS: `python tests/run_seamgrim_legacy_deeplink_compat_check.py`
- PASS: `python tests/run_seamgrim_public_default_route_check.py`
- PASS: `python tests/run_seamgrim_project_restart_backup_recovery_check.py`
- PASS: `python tests/run_seamgrim_workbench_durable_persistence_adapters_check.py`
- PASS: `python tests/run_seamgrim_workbench_durable_quality_gate_check.py`
- PASS: `python tests/run_seamgrim_public_share_clone_reopen_check.py`
- PASS: `python tests/run_seamgrim_public_physics_change_storyboard_check.py`
- PASS: `git diff --check` (warnings only for pre-existing CRLF normalization notices)
- PASS: `git status --short -- docs/ssot`

## G7 Single-Node Serving Readiness

- Added `/ready`, `/readiness`, `/api/readiness`, and `/api/public-wedge/readiness`.
- Readiness distinguishes WASM artifact readiness from project store readiness.
- Response includes file names and byte sizes only; it does not expose absolute paths, capability values, or IDC deployment claims.
- Browser runner verifies a clean browser can open the default route and execute the projectile WASM path.

### G7 Verification

- PASS: `python tests/run_seamgrim_public_single_node_serving_check.py`
- PASS: `python tests/run_seamgrim_legacy_deeplink_compat_check.py`
- PASS: `python tests/run_seamgrim_public_share_clone_reopen_check.py`
- PASS: `git diff --check` (warnings only for pre-existing CRLF normalization notices)
- PASS: `git status --short -- docs/ssot`

## G8 Four-Viewport Quality

- Added four-viewport browser quality runner for `1440x900`, `1024x768`, `778x912`, and `390x844`.
- The runner verifies DDN editor size, primary canvas size, nonblank pixels, no horizontal overflow, keyboard focus, accessible button labels, save/share/clone visibility, console errors, and bounded first render.
- Screenshots and pixel evidence are written to `out/seamgrim_public_wedge_g8/` and are not committed.

### G8 Verification

- PASS: `python tests/run_seamgrim_public_four_viewport_quality_check.py`
- PASS: `python tests/run_seamgrim_public_single_node_serving_check.py`
- PASS: `python tests/run_seamgrim_public_share_clone_reopen_check.py`
- PASS: `git diff --check` (warnings only for pre-existing CRLF normalization notices)
- PASS: `git status --short -- docs/ssot`

## G9 Consolidated Quality Gate

- Added one consolidated pack: `seamgrim_public_physics_wedge_v1`.
- Added `tests/run_seamgrim_public_physics_wedge_quality_gate_check.py`.
- The gate runs the G1-G8 public wedge checkers plus durable quality, CLI/WASM freshness/equality/sync, and view-only state hash invariant checks.
- No extra micro-pack chain was added.

### G9 Verification

- PASS: `python tests/run_pack_golden.py seamgrim_public_physics_wedge_v1`
- PASS: `python tests/run_seamgrim_public_physics_wedge_quality_gate_check.py`
- PASS: `git diff --check` (warnings only for pre-existing CRLF normalization notices)
- PASS: `git status --short -- docs/ssot`

## G10 Promotion Packet

- Added `docs/reports/impl/SEAMGRIM_PUBLIC_PHYSICS_WEDGE_PROMOTION_PACKET_V1_20260713.md`.
- External user success count remains `0`.
- The packet separates behavior-closed product paths from docs-closed pilot/rollback notes.
- Legacy removal, IDC deployment, public registry, login/cloud, and multi-module resolver remain future owner decisions.

### G10 Verification

- PASS: `python tests/run_seamgrim_public_physics_wedge_quality_gate_check.py`
- PASS: `python tests/run_pack_golden.py seamgrim_public_physics_wedge_v1`
- PASS: `cargo check`
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS: `cargo test -p ddonirang-tool --no-run`
- PASS: `python tests/run_ci_sanity_gate.py --profile core_lang`
- PASS: `git diff --check`
- PASS: `git status --short -- docs/ssot`
- Logs: `out/seamgrim_public_wedge_g10_final/`.
- Sanity gate open-log artifacts were restored to pre-test state.
