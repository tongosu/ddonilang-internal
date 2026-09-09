# Codex Session Delta - Seamgrim Reliability Container IDC Round0

Date: 2026-07-14 KST

## Objective

Active goal file:

`docs/context/roadmap/CODEX_ULTRALONG_GOAL_SEAMGRIM_RELIABILITY_CONTAINER_IDC_ROUND0_V1_20260713.md`

## G0 Baseline

- Branch: `codex/queue-20260706`
- START_HEAD: `618f5fc7d37a4f02e74690d41183ff540f75b32b`
- Resume trigger: predecessor blocker `5ba698b` is committed and is an ancestor of START_HEAD.
- `0c82608` is an ancestor of HEAD.
- Current SSOT index: `docs/ssot/ssot/SSOT_INDEX_v24.14.1.md`
- `docs/ssot/**` status: clean.
- Target deploy/server/store/workbench/wasm/lineage-runner paths: clean at start.
- Existing unrelated dirty/untracked files are preserved and not staged.
- Docker/Podman/Compose/nginx: not available in the current shell.
- Existing node/python process counts are reference-only; no unrelated process was terminated.
- Existing private-pilot release artifact verified:
  - release id `seamgrim-private-pilot-0c826083ba8f-e108453c390e`
  - manifest SHA-256 `3f2192628a0b380866ae652e5f3dde2afab0c3876db579040a377442540800d2`
  - verifier PASS
- Prior empty `project_id` failure status: `observed_once / root_cause_open`.
- Remote IDC status: `NOT_ACTIVATED`, with no SSH or remote changes.

## G0 Verification

- PASS `git merge-base --is-ancestor 0c82608 HEAD`
- PASS `git status --short -- docs/ssot`
- PASS `python solutions/seamgrim_ui_mvp/deploy/verify_private_pilot_release.py out/seamgrim_private_pilot_release_check/seamgrim-private-pilot-0c826083ba8f-e108453c390e/manifest.detjson`

## Next

Proceed to G1. Add structured instrumentation and negative controls for the run archive lineage runner before claiming the reliability issue is fixed.

## G1 Result

- Added structured lifecycle evidence to `tests/seamgrim_workbench_run_archive_lineage_runner.mjs`.
- Added integrated contract pack `seamgrim_runner_lifecycle_reliability_v1` with `reliability_closed_claim=false`.
- Added `tests/run_seamgrim_runner_lifecycle_observation_check.py`.
- Negative controls:
  - `empty-project-id` fails before API request with `E_TEST_PROJECT_ID_EMPTY`.
  - `premature-run` fails before API request with `E_TEST_PROJECT_SAVE_PREREQUISITE`.
  - `no-ready` fails with `E_TEST_SERVER_READY_TIMEOUT` and cleans owned process.
  - `teardown-delay` forces bounded escalation and leaves residual owned PID count `0`.
- Normal lineage runner evidence records redacted owner id, owned child PID, bound port, timing milestones, project id length, API path class, and residual owned PID count without raw capability, Authorization, DDN body, or absolute temp path.

Verification:

- PASS `python -m py_compile tests/run_seamgrim_runner_lifecycle_observation_check.py`
- PASS `python tests/run_seamgrim_runner_lifecycle_observation_check.py`
- PASS `python tests/run_seamgrim_workbench_run_archive_lineage_check.py`

Boundary:

- Root cause is now observable, but not yet closed.
- No retry masking claim.
- No unrelated node/python process was terminated.
- `docs/ssot/**` remains unchanged.

## G2 Result

- Updated `ddn_exec_server.py` to allow `--port 0` and emit `SEAMGRIM_SERVER_READY` with actual bound host/port.
- Updated the lineage runner to consume the structured ready record instead of closing a free port and rebinding later.
- Added `tests/run_seamgrim_runner_lifecycle_process_check.py`.
- Updated `seamgrim_runner_lifecycle_reliability_v1` contract to `current_gate=G2` while keeping `reliability_closed_claim=false`.

Verification:

- PASS `python -m py_compile solutions/seamgrim_ui_mvp/tools/ddn_exec_server.py`
- PASS `python -m py_compile tests/run_seamgrim_runner_lifecycle_process_check.py`
- PASS `python tests/run_seamgrim_runner_lifecycle_process_check.py`
- PASS `python tests/run_seamgrim_runner_lifecycle_observation_check.py`
- PASS `python tests/run_seamgrim_workbench_run_archive_lineage_check.py`

Evidence:

- Parallel lineage run count: `4`
- Actual bound port collisions: `0`
- Owned residual PID count after normal/failure/timeout/teardown-delay paths: `0`
- `/projects//` network requests: `0`
- Unrelated process termination: `0`

## G3 Result

- User-provided blocker reference `5ba698b` exists locally and is an ancestor of the current branch.
- New sealed START_HEAD for resumed G0-G9 work: `618f5fc7d37a4f02e74690d41183ff540f75b32b`.
- Added run archive product prerequisites in `run_archive_adapter.js`:
  - empty `projectId` -> `E_RUN_ARCHIVE_PROJECT_ID_EMPTY`
  - empty capability -> `E_RUN_ARCHIVE_CAPABILITY_EMPTY`
  - empty `serverRunId` for run mutation/detail -> `E_RUN_ARCHIVE_SERVER_RUN_ID_EMPTY`
- Updated the browser lineage runner to wait for structured saved state instead of relying on the Korean save-status text alone.
- The runner now requires saved `project_id`, saved `head_revision_id`, edit capability link, view capability link, and redacted capability session before run archive API use.
- View capability negative controls now verify rejection for run create, checkpoint, finalize, and restore.
- Empty project id negative control remains blocked before API request, with `/projects//` request count `0`.
- Existing revision conflict workflow remains the evidence for 409 preserving local work.
- Updated `seamgrim_runner_lifecycle_reliability_v1` contract to `current_gate=G3` while keeping `reliability_closed_claim=false`.

Verification:

- PASS `python -m py_compile tests/run_seamgrim_project_run_prerequisite_check.py tests/run_seamgrim_runner_lifecycle_process_check.py tests/run_seamgrim_runner_lifecycle_observation_check.py`
- PASS `node --check tests/seamgrim_workbench_run_archive_lineage_runner.mjs`
- PASS `python tests/run_seamgrim_project_run_prerequisite_check.py`
- PASS `python tests/run_seamgrim_runner_lifecycle_observation_check.py`
- PASS `python tests/run_seamgrim_runner_lifecycle_process_check.py`
- PASS `python tests/run_seamgrim_workbench_run_archive_lineage_check.py`
- PASS `python tests/run_pack_golden.py seamgrim_runner_lifecycle_reliability_v1 seamgrim_workbench_run_archive_lineage_v1`
- PASS `git diff --check -- solutions/seamgrim_ui_mvp/ui/workbench/persistence/run_archive_adapter.js tests/seamgrim_workbench_run_archive_lineage_runner.mjs tests/run_seamgrim_project_run_prerequisite_check.py pack/seamgrim_runner_lifecycle_reliability_v1/contract.detjson`
- PASS `git status --short -- docs/ssot`

Closure boundary:

- Project/run prerequisite failure is now guarded in product adapter code and verified through browser/server workflow.
- No `RELIABILITY_CLOSED` claim yet; G4 consecutive-run matrix is still required.

## G4 Result

- Added `tests/run_seamgrim_first_run_reliability_matrix_check.py`.
- Added `pack/seamgrim_runner_lifecycle_reliability_v1/g4_matrix_contract.detjson`.
- Updated `seamgrim_runner_lifecycle_reliability_v1` to `current_gate=G4`.
- First G4 attempt found a real failure at `lineage-20`:
  - failure code `E_TEST_ARCHIVE_WAIT_TIMEOUT`
  - symptom: reopened browser did not capture the edit-link capability session, leaving `serverProject` empty.
- Fixed the runner to canonicalize the parsed product edit capability into a workbench reopen URL before opening the new browser context.
- Restarted the G4 sequence from zero after the fix; no failed run was counted into the success sequence.

Final G4 verification:

- PASS `python -m py_compile tests/run_seamgrim_first_run_reliability_matrix_check.py`
- PASS `python tests/run_pack_golden.py seamgrim_runner_lifecycle_reliability_v1`
- PASS `node --check tests/seamgrim_workbench_run_archive_lineage_runner.mjs`
- PASS `python tests/run_seamgrim_project_run_prerequisite_check.py`
- PASS `python tests/run_seamgrim_workbench_run_archive_lineage_check.py`
- PASS `python tests/run_seamgrim_first_run_reliability_matrix_check.py`

G4 matrix counts:

- lineage target runner: `20/20`
- public physics wedge quality gate: `5/5`
- durable workbench gate: `5/5`
- private-pilot local rehearsal: `3/3`
- four viewport workflow: `2/2`
- 4x parallel lineage: `3/3`
- bounded contention lineage: `3/3`
- rerun-masked failures in accepted sequence: `0`
- `/projects//` requests: `0`
- owned residual process/temp evidence: `0`

Closure boundary:

- `RELIABILITY_CLOSED` is now claimed for the first-run lifecycle reliability scope only.
- Actual container, TLS, private IDC deployment, and external participant success remain unclaimed.

## G5 Result

- Added integrated pack `seamgrim_actual_container_rehearsal_v1`.
- Added `tests/run_seamgrim_actual_container_readiness_check.py`.
- Verified static container source/config inputs without installing runtime or pulling images:
  - Dockerfile non-root runtime user and no floating `latest` tag.
  - Compose read-only root filesystem, tmpfs, operator-owned data/backup/log binds, internal network, no app host port, `no-new-privileges`, `cap_drop: ALL`, pids/memory/nofile bounds.
  - nginx edge policy: HTTP to HTTPS redirect, operator-owned TLS file paths, 2m body limit, rate/connection limits, security headers, wasm MIME, and no query/Authorization in access log format.
- Re-ran the sealed private-pilot release checker as the source artifact gate.
- Runtime/approval availability at this gate:
  - Docker: `false`
  - Podman: `false`
  - docker-compose: `false`
  - nginx: `false`
  - `CONTAINER_RUNTIME_INSTALL_APPROVED=1`: `false`
  - `CONTAINER_IMAGE_PULL_APPROVED=1`: `false`
- Actual OCI build/run executed: `false`.
- Runtime evidence path: `out/seamgrim_actual_container_rehearsal_v1/g5_readiness.detjson` (not committed).

Verification:

- PASS `python -m py_compile tests/run_seamgrim_actual_container_readiness_check.py`
- PASS `python tests/run_seamgrim_actual_container_readiness_check.py`
- PASS `python tests/run_pack_golden.py seamgrim_actual_container_rehearsal_v1`
- PASS `git status --short -- docs/ssot`

Operator inputs still needed for actual runtime:

- Existing Docker or Podman runtime, or explicit runtime install approval.
- `CONTAINER_IMAGE_PULL_APPROVED=1` before pulling base images.
- Approved base image digest source.

Closure boundary:

- Highest container grade reached: `READY_FOR_CONTAINER_RUNTIME`.
- `ACTUAL_CONTAINER_VERIFIED` is not claimed.

## G6-G8 Status

- Actual OCI image build: `BLOCKED_NOT_EXECUTED`
- Actual OCI container run: `BLOCKED_NOT_EXECUTED`
- Actual Compose persistence/restart: `BLOCKED_NOT_EXECUTED`
- Actual edge/TLS process rehearsal: `BLOCKED_NOT_EXECUTED`
- Reason: Docker/Podman/Compose/nginx were not available in the current shell, and no image pull/install approval env was present.
- No install, pull, Docker, Podman, Compose, nginx, or remote command was executed.
- Static source/config gates remain covered by G5.

## G9 Result

- Added `tests/run_seamgrim_storage_error_hardening_check.py`.
- Updated `seamgrim_actual_container_rehearsal_v1` to `current_gate=G9`.
- Verified local storage/error hardening without container runtime:
  - `MAX_RUN_CHECKPOINTS` is enforced in the actual append checkpoint path.
  - `MAX_PROJECT_RUNS` is enforced in the actual create run path.
  - `MAX_CHECKPOINT_CANONICAL_BYTES` is enforced in the actual checkpoint artifact path.
  - raw edit/view capability strings are not stored in SQLite.
  - tampered checkpoint object is detected by integrity audit.
  - existing project store and storage/security/recovery checkers still pass.

Verification:

- PASS `python -m py_compile tests/run_seamgrim_storage_error_hardening_check.py`
- PASS `python tests/run_seamgrim_actual_container_readiness_check.py`
- PASS `python tests/run_seamgrim_storage_error_hardening_check.py`
- PASS `python tests/run_pack_golden.py seamgrim_actual_container_rehearsal_v1`
- PASS `git status --short -- docs/ssot`

Closure boundary:

- G9 local hardening is behavior-checked for the local store/server path.
- Container-specific SQLite/runtime/volume assertions remain blocked until actual runtime is available.
- Highest overall grade remains `READY_FOR_CONTAINER_RUNTIME`.

## G10 Result

- Added `tests/run_seamgrim_local_backup_restore_rollback_rehearsal_check.py`.
- Updated `seamgrim_actual_container_rehearsal_v1` to `current_gate=G10`.
- Local scratch rehearsal:
  - created projectile project with revision, run, two checkpoints, finalize.
  - created pendulum project with revision, run, two checkpoints, finalize.
  - created application-consistent store backup.
  - restored into empty scratch target and compared project head revision, object hash, run/checkpoint chain, edit capability, and view capability.
  - corrupt backup and incomplete backup were rejected.
  - bounded disk pressure was simulated only inside a dedicated scratch directory.
  - existing private-pilot backup/restore checker verified non-empty restore rejection.
  - existing deploy/rollback checker verified bad release rejection and code-only rollback without data restore.

Verification:

- PASS `python -m py_compile tests/run_seamgrim_local_backup_restore_rollback_rehearsal_check.py`
- PASS `python tests/run_seamgrim_local_backup_restore_rollback_rehearsal_check.py`
- PASS `python tests/run_seamgrim_actual_container_readiness_check.py`
- PASS `python tests/run_pack_golden.py seamgrim_actual_container_rehearsal_v1`
- PASS `git status --short -- docs/ssot`

Closure boundary:

- G10 is locally behavior-checked for scratch store and deploy-tool paths.
- Actual container volume backup/restore remains blocked because no actual container runtime is available.

## G11 Result

- Added `tests/run_seamgrim_actual_container_rehearsal_check.py`.
- Updated `seamgrim_actual_container_rehearsal_v1` to `current_gate=G11`.
- Integrated applicable local gates:
  - actual container readiness/static gate
  - storage/error hardening
  - local backup/restore/rollback rehearsal
  - public physics wedge quality gate
  - durable workbench quality gate
  - CLI/WASM freshness
  - CLI/WASM true parity equality
  - CLI/WASM sync gate
  - view-only state_hash invariant
  - pack golden

Verification:

- PASS `python -m py_compile tests/run_seamgrim_actual_container_rehearsal_check.py`
- PASS `python tests/run_seamgrim_actual_container_rehearsal_check.py`
- PASS `git status --short -- docs/ssot`

Closure boundary:

- Local product behavior and static container input gates are integrated.
- Actual OCI build/run, edge/TLS process, container bounded load, and container behavior evidence remain unexecuted.
- Highest grade remains `READY_FOR_CONTAINER_RUNTIME`, not `ACTUAL_CONTAINER_VERIFIED`.

## G12 Result

- Added integrated pack `seamgrim_private_idc_round0_readiness_v1`.
- Added `tests/run_seamgrim_private_idc_round0_readiness_check.py`.
- Existing IDC input sheet was used:
  - `work/codex/20260711_idc_deployment_intake/IDC_INPUT_SHEET.md`
- Observed activation:
  - `PRIVATE_IDC_DEPLOY_APPROVED=1`: absent
  - required non-secret env inputs: absent
  - input sheet fields: not filled
- Result: `REMOTE_GATE=NOT_ACTIVATED`
- Remote commands: `0`
- Remote changes: `0`

Verification:

- PASS `python -m py_compile tests/run_seamgrim_private_idc_round0_readiness_check.py`
- PASS `python tests/run_seamgrim_private_idc_round0_readiness_check.py`
- PASS `git status --short -- docs/ssot`

## G13-G15 Status

- G13 approved IDC read-only inventory: `NOT_ACTIVATED`
- G14 private IDC canary deploy: `NOT_ACTIVATED`
- G15 IDC restart/recovery/security gate: `NOT_ACTIVATED`
- Reason: G12 activation inputs and approval are missing.
- SSH commands executed: `0`
- Remote changes: `0`

## G16 Result

- Reused and updated existing `work/beta/seamgrim_round0/` assets.
- Added `work/beta/seamgrim_round0/ROUND0_OPERATIONS_PACKET_V1_20260713.md`.
- Updated participant, moderator, session checklist, and manifest to current product workflow:
  - 90-second projectile first run.
  - change one value, inspect graph/trajectory.
  - save with non-identifying title.
  - reopen in new browser/session.
  - view-link share and clone.
  - capability link handling.
  - data retention/delete/support/rollback boundaries.
- Extended `tests/run_seamgrim_private_idc_round0_readiness_check.py` to verify the Round 0 packet.
- Updated `seamgrim_private_idc_round0_readiness_v1` to `current_gate=G16`.

Verification:

- PASS `python -m py_compile tests/run_seamgrim_private_idc_round0_readiness_check.py`
- PASS `python tests/run_seamgrim_private_idc_round0_readiness_check.py`
- PASS `python tests/run_pack_golden.py seamgrim_private_idc_round0_readiness_v1`

Closure boundary:

- Round 0 operations packet is prepared for current workflow.
- Actual invitations sent: `0`
- Actual participants: `0`
- Actual successes: `0`
- `READY_FOR_INVITED_ROUND0` is not claimed because private IDC canary and invitation approval are missing.

## G0-G9 Resume Result 2026-07-14

- User instruction: predecessor blocker `5ba698b` is verified/committed; seal current HEAD as new START_HEAD and resume G0-G9.
- New START_HEAD: `618f5fc7d37a4f02e74690d41183ff540f75b32b`.
- `5ba698b` is an ancestor of START_HEAD.
- `0c82608` is an ancestor of START_HEAD.
- Current SSOT index remains `docs/ssot/ssot/SSOT_INDEX_v24.14.1.md`.
- Docker/Podman/docker-compose/nginx: not available.
- `CONTAINER_RUNTIME_INSTALL_APPROVED`, `CONTAINER_IMAGE_PULL_APPROVED`, and `PRIVATE_IDC_DEPLOY_APPROVED`: unset.
- G6-G8 status remains `NOT_ACTIVATED`; no install, image pull, runtime, edge, TLS, remote, or IDC command was executed.

Verification rerun:

- PASS `python -m py_compile tests/run_seamgrim_runner_lifecycle_reliability_check.py tests/run_seamgrim_project_run_prerequisite_check.py tests/run_seamgrim_runner_lifecycle_process_check.py tests/run_seamgrim_runner_lifecycle_observation_check.py tests/run_seamgrim_actual_container_readiness_check.py tests/run_seamgrim_storage_error_hardening_check.py`
- PASS `python tests/run_seamgrim_runner_lifecycle_reliability_check.py`
- PASS `python tests/run_seamgrim_actual_container_readiness_check.py`
- PASS `python tests/run_seamgrim_storage_error_hardening_check.py`
- PASS `python tests/run_pack_golden.py seamgrim_runner_lifecycle_reliability_v1 seamgrim_actual_container_rehearsal_v1`
- PASS `cargo check`
- PASS `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS `python tests/run_ci_sanity_gate.py --profile core_lang`
- PASS `git diff --check -- tests/run_seamgrim_runner_lifecycle_reliability_check.py docs/reports/impl/SEAMGRIM_RELIABILITY_CONTAINER_IDC_ROUND0_PACKET_V1_20260713.md work/_session_deltas/20260713_codex_seamgrim_reliability_container_idc_round0.md pack/seamgrim_runner_lifecycle_reliability_v1 pack/seamgrim_actual_container_rehearsal_v1`
- PASS `git status --short -- docs/ssot`

Generated sanity open log changes restored before commit:

- `pack/open_bundle_artifact/run_bundle/geoul.diag.jsonl`
- `pack/open_end_to_end/open.log.jsonl`

Current highest honest grade for resumed G0-G9: `READY_FOR_CONTAINER_RUNTIME`.

Not claimed:

- `ACTUAL_CONTAINER_VERIFIED`
- `PRIVATE_IDC_DEPLOYED`
- `READY_FOR_INVITED_ROUND0`
- external Round 0 success

## G17 Result

- Final applicable local/product verification was run at product verification HEAD `324b3b7cef9dd650ffa9a7102011ade63c8478bb`.
- During G17, `python tests/run_seamgrim_public_physics_wedge_quality_gate_check.py` first exposed a real race:
  - nested `run_seamgrim_public_physics_change_storyboard_check.py` saw `project-save-status` reach `server saved` before the view link was rendered.
  - fixed in `324b3b7 fix(seamgrim): render saved project links before status`.
  - the gate was rerun after the fix and passed.

Final verification:

- PASS `python tests/run_seamgrim_runner_lifecycle_reliability_check.py`
- PASS `python tests/run_seamgrim_private_pilot_local_rehearsal_check.py`
- PASS `python tests/run_seamgrim_public_physics_wedge_quality_gate_check.py`
- PASS `python tests/run_seamgrim_workbench_durable_quality_gate_check.py`
- PASS `python tests/run_seamgrim_actual_container_rehearsal_check.py`
- PASS `python tests/run_seamgrim_private_idc_round0_readiness_check.py`
- PASS `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS `python tests/run_ddn_cli_wasm_true_parity_equality_check.py`
- PASS `python tests/run_ddn_cli_wasm_sync_gate_check.py`
- PASS `python tests/run_seamgrim_view_only_state_hash_invariant_check.py`
- PASS `cargo check`
- PASS `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS `cargo test -p ddonirang-tool --no-run`
- PASS `python tests/run_ci_sanity_gate.py --profile core_lang`
- PASS `git diff --check`
- PASS `git status --short -- docs/ssot`

Notes:

- `git diff --check` returned success but printed pre-existing unrelated CRLF warnings for dirty files outside this goal.
- Sanity gate regenerated `pack/open_bundle_artifact/run_bundle/geoul.diag.jsonl` and `pack/open_end_to_end/open.log.jsonl`; both were restored before commit.
- Docker/Podman/docker-compose/nginx remain unavailable.
- Actual OCI build/run, actual edge/TLS, actual remote IDC, and actual participant evidence remain unexecuted.
- Remote commands: `0`.
- Remote changes: `0`.
- External participants: `0`.
- External successes: `0`.
- Highest honest grade remains `READY_FOR_CONTAINER_RUNTIME`.
- `docs/ssot/**` changed files: `0`.

## G4 Regression Correction And Revalidation 2026-07-14

- Trigger: independent rerun showed the previous `RELIABILITY_CLOSED` / `READY_FOR_CONTAINER_RUNTIME` packet was premature.
- Reproduced failure class:
  - durable-workbench matrix path
  - nested `E_TEST_ARCHIVE_WAIT_TIMEOUT`
  - `TypeError: Cannot read properties of undefined (reading 'getSnapshot')`
  - diagnostic immediately after failure showed `archive_count: 2`
- Policy during correction:
  - no container G6+ work started.
  - no archive-count assertion or product data assertion was weakened.
  - all wait predicates touching the workbench API now tolerate pre-init `undefined`.
  - `docs/ssot/**` remained unchanged.

Correction commits:

- `d15c767 fix(seamgrim): wait for workbench api before archive assertions`
  - Added explicit `getSnapshot` API readiness waits.
  - Added undefined-safe archive predicates.
  - Extended matrix evidence with `owned_residual_sockets`.
- `ef159e7 fix(seamgrim): bound project workflow server teardown`
  - Separated a later four-viewport `server health timeout` from the archive race.
  - Added server startup diagnostics, failed-start cleanup, bounded server teardown, and temp data cleanup.
  - Confirmed the observed PID was already gone; this was a child exit-state/readiness robustness issue, not a surviving `ddn_exec_server.py`.
- `64ce179 fix(seamgrim): wait for durable archive persistence before reopen`
  - Fixed a durable reopen race where `runs.length >= 2` could precede archive-list persistence.
  - Added explicit archive-count waits before fresh-context reopen and after reopen.

Reset verification sequence after the final fix:

- PASS lineage runner standalone `10/10`.
- PASS `python tests/run_seamgrim_workbench_durable_quality_gate_check.py`.
- PASS `python tests/run_seamgrim_first_run_reliability_matrix_check.py`.
- PASS second consecutive `python tests/run_seamgrim_first_run_reliability_matrix_check.py`.
- PASS matrix-after `python tests/run_seamgrim_workbench_durable_quality_gate_check.py`.
- PASS `python tests/run_seamgrim_runner_lifecycle_reliability_check.py`.
- PASS `python tests/run_seamgrim_private_pilot_local_rehearsal_check.py`.
- PASS `python tests/run_seamgrim_public_physics_wedge_quality_gate_check.py`.
- PASS `python tests/run_ddn_cli_wasm_freshness_check.py`.
- PASS `python tests/run_ddn_cli_wasm_true_parity_equality_check.py`.
- PASS `python tests/run_ddn_cli_wasm_sync_gate_check.py`.
- PASS `python tests/run_seamgrim_view_only_state_hash_invariant_check.py`.
- PASS `git diff --check` (pre-existing unrelated CRLF warnings only).
- PASS `git status --short -- docs/ssot`.

Preserved local matrix evidence:

- `out/seamgrim_runner_lifecycle_reliability_v1/g4_matrix_run1_after_64ce179.detjson`
- `out/seamgrim_runner_lifecycle_reliability_v1/g4_matrix_run2_after_64ce179.detjson`

Both matrix evidence files:

- `status=PASS`
- `rerun_masked_failures=0`
- `owned_residual_processes=0`
- `owned_residual_sockets=0`
- `owned_residual_temp_dirs=0`
- `double_slash_requests=0`
- required sequence counts: lineage `20`, public wedge `5`, durable workbench `5`, private pilot `3`, four viewport `2`, parallel lineage `3`, bounded contention `3`

Corrected status:

- `RELIABILITY_CLOSED` restored.
- `READY_FOR_CONTAINER_RUNTIME` restored.
- `ACTUAL_CONTAINER_VERIFIED`, `PRIVATE_IDC_DEPLOYED`, and `READY_FOR_INVITED_ROUND0` remain unclaimed.
