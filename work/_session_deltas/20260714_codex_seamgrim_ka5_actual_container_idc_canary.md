# 2026-07-14 Codex session delta - Seamgrim KA5 actual container IDC canary

## G0 Baseline

- Active goal file: `docs/context/roadmap/CODEX_SUPERLONG_GOAL_SEAMGRIM_KA5_ACTUAL_CONTAINER_IDC_CANARY_V1_20260714.md`
- Branch: `codex/queue-20260706`
- START_HEAD: `8463f48d`
- Restart START_HEAD: `5a20a02` (`chore(seamgrim): record ka5 container activation baseline`)
- Reported blocker commit `5ba698b`: present locally and confirmed as an ancestor of current HEAD.
- Minimum ancestor `8463f48`: satisfied.
- SSOT current: `v24.14.1`
- Goal SHA-256: `D17F8B5959A9CA7D81E368E9D41B2C25F31AE697C03515A62DED8FACAB54F700`
- Workbench brief SHA-256: `1C6A25D286FB6AA7AC5E50CA46FC7ABCFAAD0EF24857549A512C17A4AA00906B`

Read before G0/G1:

- `AGENTS.md`
- `AGENT_WORKFLOW.md`
- `SSOT_POLICY.md`
- `ARTIFACT_POLICY.md`
- `CLAUDE.md`
- `docs/context/all/DEV_SUMMARY.md`
- `docs/ssot/ssot/SSOT_INDEX_v24.14.1.md`
- `docs/ssot/ssot/SSOT_DECISIONS_v24.14.1.md`
- `docs/ssot/ssot/SSOT_LANG_v24.14.1.md`
- `docs/ssot/ssot/SSOT_PLATFORM_v24.14.1.md`
- `docs/ssot/ssot/SSOT_TOOLCHAIN_v24.14.1.md`
- `docs/ssot/ssot/SSOT_ROADMAP_CATALOG_v24.14.1.md`
- `docs/ssot/age/AGE3/INDEX.md`
- `docs/ssot/age/AGE3/AGE3_DEVELOPMENT_GUIDE.md`
- `docs/ssot/walks/seamgrim_sim_viz_catalog_v1/README.md`
- `docs/ssot/walks/seamgrim_sim_viz_catalog_v1/lesson_family_index.md`
- `docs/context/briefs/BRIEF_SEAMGRIM_DDN_DETERMINISTIC_PROJECT_WORKBENCH_UI_V1_20260712.md`
- `docs/context/roadmap/GANADA_MARU_VERIFICATION_CONTRACT_V1_20260710.md`
- `docs/context/roadmap/ROADMAP_V2_GANADA_15_JULGI_6_MARU_20260426.md`
- existing reliability/container/IDC pack contracts and checkers.

Runtime activation snapshot:

- Docker: `NOT_FOUND`
- Podman: `NOT_FOUND`
- docker-compose: `NOT_FOUND`
- nginx: `NOT_FOUND`
- `CONTAINER_IMAGE_PULL_APPROVED`: absent
- `CONTAINER_RUNTIME_INSTALL_APPROVED`: absent
- `PRIVATE_IDC_DEPLOY_APPROVED`: absent
- private IDC required inputs: absent

G0 verification:

- PASS `python tests/run_seamgrim_runner_lifecycle_reliability_check.py`
- PASS `python tests/run_seamgrim_actual_container_readiness_check.py`
- PASS `python tests/run_seamgrim_private_idc_round0_readiness_check.py`
- PASS `git status --short -- docs/ssot`

G0 restart verification after sealing current HEAD:

- PASS `python tests/run_seamgrim_runner_lifecycle_reliability_check.py`
- PASS `python tests/run_seamgrim_actual_container_readiness_check.py`
- PASS `python tests/run_seamgrim_private_idc_round0_readiness_check.py`
- PASS `git status --short -- docs/ssot`

G0 status:

- `RELIABILITY_CLOSED / READY_FOR_CONTAINER_RUNTIME` reconfirmed.
- G3-G7 actual container gates are `NOT_ACTIVATED`.
- G8-G10 private IDC gates are `NOT_ACTIVATED`.
- Actual container commands: `0`.
- Remote commands/changes: `0 / 0`.
- Participants/successes: `0 / 0`.
- Maru automatic promotions: `0`.

Follow-up for G1/G2:

- Independent review reported an EpicGamesLauncher/EpicWebHelper PID false positive risk.
- Treat as `타-2 checker ownership follow-up`.
- Repair must use owner-scoped process identity, not global process table diffs.

## G1 Owner-Scoped Process Identity Repair

Implementation:

- Runner result schema advanced to `seamgrim.workbench_run_archive_lineage.runner_result.v3`.
- Spawned server and helper controls now carry `SEAMGRIM_RUN_OWNER_ID`.
- Process ownership payload records PID, parent PID, creation time, executable name, command-line fingerprint hash, identity hash, and `run_owner_id`.
- Descendant identity snapshot is captured before termination.
- Post-stop residual detection requires the same process identity; same PID with changed identity is ignored as simulated PID reuse.
- Bound socket teardown is checked separately from process teardown.
- Added negative controls: `pid-reuse-simulation`, `owned-leak-injection`, and unrelated helper overlap in the process checker.
- Job Object was not added; recorded fallback is pre-stop identity snapshot plus post-stop identity matching.

Verification:

- PASS `node --check tests/seamgrim_workbench_run_archive_lineage_runner.mjs`
- PASS `python -m py_compile tests/run_seamgrim_runner_lifecycle_process_check.py tests/run_seamgrim_runner_lifecycle_observation_check.py tests/run_seamgrim_first_run_reliability_matrix_check.py`
- PASS `node tests/seamgrim_workbench_run_archive_lineage_runner.mjs --mode pid-reuse-simulation`
- PASS expected nonzero `node tests/seamgrim_workbench_run_archive_lineage_runner.mjs --mode owned-leak-injection`
- PASS `node tests/seamgrim_workbench_run_archive_lineage_runner.mjs`
- PASS `python tests/run_pack_golden.py seamgrim_runner_lifecycle_reliability_v1`
- PASS `python tests/run_seamgrim_runner_lifecycle_process_check.py`
- PASS `python tests/run_seamgrim_runner_lifecycle_observation_check.py`
- PASS `python tests/run_seamgrim_workbench_run_archive_lineage_check.py`
- PASS `python tests/run_seamgrim_runner_lifecycle_reliability_check.py`
- PASS `git diff --check` on changed G1 paths
- PASS `git status --short -- docs/ssot`

Commit:

- `f9d3edd fix(seamgrim): scope lifecycle cleanup to owned process identities`

## G2 Reliability Reseal

G2 exposed three reliability/product-state issues before the final consecutive run:

- Restart link runner still used free-port TOCTOU and could time out under matrix load. Fixed by using server `--port 0` ready records.
- Durable full workflow runner expected archive count 2 before the branch run was finalized and inherited stale local runs across catalog project switches. Fixed by resetting `state.runs` on project switch and finalizing the active branch before archive assertions.
- Workbench reopen guard rejected valid generated project IDs whose `sgp_` suffix was shorter than 20 characters after URL-safe cleanup. Fixed by aligning the guard with generated ID shape.
- Server ready record was emitted before the accept loop started. Fixed by starting `serve_forever()` on a thread before printing `SEAMGRIM_SERVER_READY`.

G2 commits:

- `95af48f fix(seamgrim): harden durable workflow reliability gates`
- `af7fb7e fix(seamgrim): accept generated project ids on reopen`
- `0f4d1cb fix(seamgrim): emit server ready after accept loop starts`

Final G2 verification:

- PASS final `python tests/run_seamgrim_runner_lifecycle_process_check.py` 10/10 consecutive.
- PASS final `node tests/seamgrim_workbench_run_archive_lineage_runner.mjs` 10/10 consecutive.
- PASS `python tests/run_seamgrim_first_run_reliability_matrix_check.py` 2/2 consecutive after `0f4d1cb`.
  - Run 1: 2529s, evidence copied to `out/seamgrim_runner_lifecycle_reliability_v1/g2_matrix_readyfix_run1_after_0f4d1cb.detjson`.
  - Run 2: 2511s, evidence copied to `out/seamgrim_runner_lifecycle_reliability_v1/g2_matrix_readyfix_run2_after_0f4d1cb.detjson`.
- PASS `python tests/run_seamgrim_workbench_durable_quality_gate_check.py` immediately after each matrix run.
- PASS `python tests/run_seamgrim_runner_lifecycle_reliability_check.py`.
- PASS `python tests/run_pack_golden.py seamgrim_runner_lifecycle_reliability_v1`.
- PASS `git diff --check` on changed G1/G2 paths.
- PASS `git status --short -- docs/ssot`.
- PASS `cargo check`.
- PASS `cargo check --manifest-path tools/teul-cli/Cargo.toml`.
- PASS `python tests/run_ci_sanity_gate.py --profile core_lang`.
- PASS post-G2 `python tests/run_seamgrim_actual_container_readiness_check.py`: `READY_FOR_CONTAINER_RUNTIME`.
- PASS post-G2 `python tests/run_seamgrim_private_idc_round0_readiness_check.py`: `NOT_ACTIVATED`.

Final counters:

- `owned_residual_processes=0`
- `owned_residual_sockets=0`
- `owned_residual_temp_dirs=0`
- `unrelated_process_false_positives=0`
- `rerun_masked_failures=0`

Status:

- `RELIABILITY_CLOSED / READY_FOR_CONTAINER_RUNTIME` maintained.
- G2 is evidence for `타-2` rejudgment proposal only; automatic maru promotion remains 0.

## G3-G9 Activation Decision

Post-G2 activation recheck:

- Docker: `NOT_FOUND`
- Podman: `NOT_FOUND`
- docker-compose: `NOT_FOUND`
- nginx: `NOT_FOUND`
- `CONTAINER_IMAGE_PULL_APPROVED`: absent
- `CONTAINER_RUNTIME_INSTALL_APPROVED`: absent
- `PRIVATE_IDC_DEPLOY_APPROVED`: absent
- private IDC required inputs: absent

Result:

- G3-G7 actual container gates: `NOT_ACTIVATED`.
- G8-G9 private IDC gates: `NOT_ACTIVATED`.
- Actual OCI image build/run commands: `0`.
- Edge/TLS commands: `0`.
- Remote commands/changes: `0 / 0`.
- Participants/successes: `0 / 0`.
- Maru automatic promotions: `0`.
- Status reported as `WAITING_FOR_CONTAINER_ACTIVATION`.
