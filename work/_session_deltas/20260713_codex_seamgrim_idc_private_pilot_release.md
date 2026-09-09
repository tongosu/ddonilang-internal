# Codex Session Delta - Seamgrim IDC Private Pilot Release

- Date: 2026-07-13 KST
- Branch: `codex/queue-20260706`
- Initial START_HEAD: `bff486e`
- Restart START_HEAD: `9c3f7e6` (sealed after user confirmed blocker `5ba698b` was already an ancestor)
- Goal file: `docs/context/roadmap/CODEX_SUPERLONG_GOAL_SEAMGRIM_IDC_PRIVATE_PILOT_RELEASE_V1_20260713.md`
- Current status: G0 complete, G1 complete, G2 complete, G3 complete, G4/G5/G6/G7 complete, G8 local process/browser rehearsal complete, G9 remote inventory blocked by missing IDC input/approval

## Boundary

- `docs/ssot/**` is read-only and unchanged.
- Existing unrelated dirty/untracked files are preserved and must not be staged.
- No IDC SSH, remote file changes, DNS/TLS/firewall changes, package download, or container image download without explicit approval.
- G9-G11 are inactive because `PRIVATE_IDC_DEPLOY_APPROVED` and IDC input are missing.
- Actual external participant count and success count remain `0`.

## G0 Result

- START_HEAD sealed at `bff486e`.
- Restart instruction received after blocker `5ba698b`; `5ba698b` is an ancestor of current work, and `9c3f7e6` was treated as the new START_HEAD without reset/revert.
- Target deploy/server/store/workbench/wasm paths were clean at the G0 start.
- Runtime observed:
  - Python `3.13.5`
  - SQLite `3.49.1`
  - Rust `1.92.0`
  - Cargo `1.92.0`
  - Docker/Compose/nginx unavailable in this shell.
- Baseline report:
  - `docs/reports/impl/SEAMGRIM_IDC_PRIVATE_PILOT_RELEASE_BASELINE_V1_20260713.md`

## Baseline Verification

Log directory: `out/seamgrim_idc_private_pilot_g0/`

- PASS `python tests/run_seamgrim_public_physics_wedge_quality_gate_check.py`
- PASS `python tests/run_seamgrim_workbench_durable_quality_gate_check.py`
- PASS `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS `python tests/run_ddn_cli_wasm_true_parity_equality_check.py`
- PASS `python tests/run_ddn_cli_wasm_sync_gate_check.py`
- PASS `python tests/run_seamgrim_view_only_state_hash_invariant_check.py`
- PASS `cargo check`
- PASS `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS `python tests/run_ci_sanity_gate.py --profile core_lang`

Sanity gate regenerated two open-log files; both were restored.

## Audit Findings

- `docker-compose.yml` currently publishes the app port directly.
- `Dockerfile` runtime binds to `0.0.0.0` and does not seal non-root/read-only release behavior.
- `nginx/seamgrim.conf` has `client_max_body_size 16m`, larger than app 2MB JSON limit.
- `project_store.py` hard-codes `PRAGMA synchronous=NORMAL`.
- Public health and readiness separation needs stronger production policy.
- `IDC_INPUT_SHEET.md` has required fields blank; remote deploy is not enabled.

## G1 Result

- Added explicit `SEAMGRIM_DEPLOY_PROFILE` handling with `dev`, `test`, and `private-pilot`.
- `private-pilot` is fail-closed unless it has:
  - absolute `SEAMGRIM_PROJECT_DATA_DIR`;
  - data dir outside the release tree;
  - SQLite synchronous `FULL`;
  - SQLite floor `3.51.3` or explicit operator attestation;
  - non-wildcard `SEAMGRIM_ALLOWED_HOSTS` and `SEAMGRIM_ALLOWED_ORIGINS`;
  - `SEAMGRIM_DATA_FILESYSTEM=local`;
  - valid trusted proxy policy.
- `SeamgrimProjectStore` now accepts and seals SQLite synchronous mode and exposes runtime pragma diagnostics.
- Private-pilot request boundary rejects invalid `Host`/`Origin` while dev keeps wildcard CORS behavior.
- Startup configuration errors expose stable error codes only, not local paths or secrets.

Verification:

- PASS `python -m py_compile solutions/seamgrim_ui_mvp/tools/ddn_exec_server.py solutions/seamgrim_ui_mvp/tools/project_store.py tests/run_seamgrim_private_pilot_config_check.py`
- PASS `python tests/run_seamgrim_private_pilot_config_check.py`
- PASS `python tests/run_seamgrim_public_default_route_check.py`
- PASS `python tests/run_seamgrim_public_physics_first_run_check.py`

## Next

Proceed to G3: app/data service hardening for private network binding, explicit persistent data, read-only release, and service limits.

## G2 Result

- Added an allowlist-only private-pilot release builder and artifact self verifier:
  - `solutions/seamgrim_ui_mvp/deploy/build_private_pilot_release.py`
  - `solutions/seamgrim_ui_mvp/deploy/verify_private_pilot_release.py`
- The release manifest records `source_commit`, `source_tree_hash`, runtime versions, teul-cli/WASM/static/deploy hashes, project store schema, deploy config hash, checker summary, non-root runtime identity, read-only release filesystem policy, and dependency digest status.
- The artifact excludes internal docs, work files, pack sources, tests, local logs, build outputs, and local project data by construction.
- `Dockerfile` now switches the runtime stage to non-root `seamgrim` user.
- Base image tags are not `latest`; digest pin remains `verification_required` because no operator-approved image source/digest input exists.

Verification:

- PASS `python -m py_compile solutions/seamgrim_ui_mvp/deploy/build_private_pilot_release.py solutions/seamgrim_ui_mvp/deploy/verify_private_pilot_release.py tests/run_seamgrim_private_pilot_release_check.py`
- PASS `python tests/run_pack_golden.py seamgrim_private_pilot_release_contract_v1`
- PASS `python tests/run_seamgrim_private_pilot_release_check.py`

## G3 Result

- Hardened the reference compose app/data boundary:
  - removed direct host app port publishing;
  - kept app service on an internal private network with `expose: 8787`;
  - required operator-owned project data, backup staging, and log bind paths;
  - set `read_only: true`, `/tmp` tmpfs, no-new-privileges, dropped capabilities, pids/memory/nofile bounds.
- Added `.env.private-pilot.template` with secret-free operator-owned path and host/origin examples.
- Updated Dockerfile runtime paths for project data, backup staging, log, and tmp build directory while keeping the runtime user non-root.
- Added `SEAMGRIM_BUILD_DIR` so production-like read-only release runs can keep temp DDN files outside the release tree.
- Added `/api/run` `Content-Length` enforcement at the same 2MB app limit used by project APIs, returning `413 E_API_RUN_BODY_TOO_LARGE`.

Verification:

- PASS `python -m py_compile solutions/seamgrim_ui_mvp/tools/ddn_exec_server.py tests/run_seamgrim_private_pilot_service_hardening_check.py`
- PASS `python tests/run_seamgrim_private_pilot_service_hardening_check.py`

## G6 Result

- Added `private_pilot_backup.py` with explicit `backup`, `restore-check`, and `plan-offhost-copy` subcommands.
- Backup path runs `SeamgrimProjectStore.audit_integrity()` before `backup_to()` and writes `backup_manifest.detjson` with source commit, tree hash, release manifest hash, project store schema, DB hash, object hashes, and no raw-live-copy claim.
- Restore path verifies manifest/DB/object hashes first, requires an empty target directory, then uses `SeamgrimProjectStore.restore_from_backup(..., sqlite_synchronous="FULL")`.
- Live restore remains non-automatic; offhost copy is dry-run planning only and contains no secrets.
- Checker validates project reopen, run lineage, checkpoint restore, clone lineage, view capability, backup destination outside data, non-empty restore rejection, corrupt backup rejection, and incomplete backup rejection.

Verification:

- PASS `python -m py_compile solutions/seamgrim_ui_mvp/deploy/private_pilot_backup.py solutions/seamgrim_ui_mvp/tools/project_store.py tests/run_seamgrim_private_pilot_backup_restore_check.py`
- PASS `python tests/run_seamgrim_private_pilot_backup_restore_check.py`
- PASS `python tests/run_seamgrim_project_restart_backup_recovery_check.py`
- PASS `python tests/run_pack_golden.py seamgrim_private_pilot_release_contract_v1`

## G7 Result

- Added `private_pilot_deploy.py` with explicit `plan`, `apply`, `verify`, and `rollback` stages.
- `apply` verifies the immutable release artifact, installs it under a release-id directory, creates a pre-deploy application backup, then atomically switches `current_release.detjson`.
- Repeated apply of the same release is idempotent and does not create a duplicate pointer transition.
- `verify` starts the current release artifact on a temporary canary port and checks public health plus private readiness.
- `rollback` switches only the release pointer back to the previous release and does not restore/delete data.
- Bad/tampered release artifacts are rejected before current pointer switch.
- Release builder allowlist was corrected to include product server tool dependencies needed by release-artifact canary startup.

Verification:

- PASS `python -m py_compile solutions/seamgrim_ui_mvp/deploy/private_pilot_deploy.py tests/run_seamgrim_private_pilot_deploy_rollback_check.py`
- PASS `python tests/run_seamgrim_private_pilot_deploy_rollback_check.py`
- PASS `python tests/run_seamgrim_private_pilot_release_check.py`
- PASS `python tests/run_seamgrim_private_pilot_backup_restore_check.py`

## G8/G9 Result

- Added integrated operations rehearsal pack `seamgrim_private_pilot_operations_rehearsal_v1`.
- Added `tests/run_seamgrim_private_pilot_local_rehearsal_check.py`, which reruns private-pilot config, release, service, edge browser, observability, backup/restore, deploy/canary/rollback, and operations pack gates.
- Local process/browser rehearsal status: `PASS_LOCAL_PROCESS_REHEARSAL`.
- Docker/Compose/nginx operational claims are not made in this shell; missing runtime is recorded and not treated as fake PASS.
- G9 remote IDC read-only inventory was not executed because IDC input and `PRIVATE_IDC_DEPLOY_APPROVED` are missing.
- Remote gate report:
  - `docs/reports/impl/SEAMGRIM_PRIVATE_IDC_REMOTE_GATE_STATUS_V1_20260713.md`
- Local rehearsal summary:
  - `out/seamgrim_private_pilot_local_rehearsal/summary.detjson`

Verification:

- PASS `python -m py_compile tests/run_seamgrim_private_pilot_local_rehearsal_check.py`
- PASS `python tests/run_seamgrim_private_pilot_local_rehearsal_check.py`
- PASS `python tests/run_seamgrim_private_pilot_config_check.py`
- PASS `python tests/run_pack_golden.py seamgrim_private_pilot_release_contract_v1`

## G4 Result

- Replaced the reference nginx profile with an HTTP-to-HTTPS edge, TLS certificate path references, 2MB body limit, write rate limit, connection/request timeouts, WASM MIME/cache policy, trusted forwarded headers, and redacted access log format.
- Added security headers: `Content-Security-Policy`, `X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options`, and `Permissions-Policy`.
- CSP keeps script inline/eval blocked except `wasm-unsafe-eval`; browser smoke found current UI needs inline style allowance, so `style-src 'self' 'unsafe-inline'` is explicitly documented by executable config.
- Added Playwright edge policy runner that serves the workbench with the same CSP/security headers, verifies header presence, WASM MIME/cache policy, first projectile view readiness, and nonblank canvas screenshot pixels without bypassing CSP.
- TLS operational completion is not claimed; certificate material remains operator-owned and repo-free.

Verification:

- PASS `node tests/seamgrim_private_pilot_edge_policy_runner.mjs`
- PASS `python tests/run_seamgrim_private_pilot_edge_policy_check.py`
- PASS `python tests/run_pack_golden.py seamgrim_private_pilot_release_contract_v1`

## G5 Result

- Public health is now `seamgrim.public_health.v1` and returns only process-alive service status.
- Private-pilot readiness detail moved to `/api/private/readiness`, guarded by the management boundary.
- Operator check added at `/api/operator/check`, including release env inputs, exact Python/SQLite/store schema versions, WASM manifest hash, DB integrity, disk summary, backup age summary, and alert inputs.
- In private-pilot profile, legacy public readiness paths return `403 E_PRIVATE_PILOT_READINESS_NOT_PUBLIC`.
- Request logging now records route path only, not query/capability/body/snapshot.
- Compose/env template now carry release commit/manifest hash and backup/log path inputs without secrets.

Verification:

- PASS `python -m py_compile solutions/seamgrim_ui_mvp/tools/ddn_exec_server.py tests/run_seamgrim_private_pilot_observability_check.py`
- PASS `python tests/run_seamgrim_private_pilot_observability_check.py`
- PASS `python tests/run_seamgrim_private_pilot_config_check.py`
- PASS `python tests/run_seamgrim_private_pilot_service_hardening_check.py`

## Final Revalidation - 2026-07-13 KST

- START_HEAD for the resumed run: `9c3f7e6`.
- Implementation HEAD before this revalidation note: `5fd0ab9`.
- Branch: `codex/queue-20260706`.
- `bff486e` remains an ancestor of final HEAD.
- Target status: `READY_FOR_PRIVATE_IDC_INPUT`.
- Local process/browser private-pilot rehearsal remains PASS.
- Real Docker/Compose/nginx/TLS operation claim remains not made in this shell:
  - `docker` unavailable.
  - `docker compose` unavailable.
  - `nginx` unavailable.
- Remote IDC inventory/deploy remains inactive:
  - missing `PRIVATE_IDC_DEPLOY_APPROVED`.
  - IDC input sheet still lacks operator-owned host/domain/TLS/backup/runtime details.
  - no SSH, DNS, firewall, package, service, or remote filesystem changes performed.
- External participant count and success count remain `0`.
- `docs/ssot/**` remains unchanged.
- Existing unrelated dirty/untracked files remain preserved and unstaged.

Revalidated commands:

- PASS `python tests/run_seamgrim_private_pilot_local_rehearsal_check.py`
- PASS `python tests/run_pack_golden.py seamgrim_private_pilot_release_contract_v1 seamgrim_private_pilot_operations_rehearsal_v1`
- PASS `python tests/run_seamgrim_public_physics_wedge_quality_gate_check.py`
- PASS `python tests/run_seamgrim_workbench_durable_quality_gate_check.py`
- PASS `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS `python tests/run_ddn_cli_wasm_true_parity_equality_check.py`
- PASS `python tests/run_ddn_cli_wasm_sync_gate_check.py`
- PASS `python tests/run_seamgrim_view_only_state_hash_invariant_check.py`
- PASS `cargo check`
- PASS `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS `cargo test -p ddonirang-tool --no-run`
- PASS `python tests/run_ci_sanity_gate.py --profile core_lang` with `PYTHONIOENCODING=utf-8`
- PASS `git diff --check` (warnings only for unrelated pre-existing CRLF dirty files)
- PASS `git status --short -- docs/ssot`

Release artifact evidence:

- Release id: `seamgrim-private-pilot-5fd0ab9aea1b-94432842cbe0`
- Manifest path: `out/seamgrim_private_pilot_release_check/seamgrim-private-pilot-5fd0ab9aea1b-94432842cbe0/manifest.detjson`
- Manifest SHA-256: `62e662141662b2023699506ad587e9d306e5ce7eaf44b76599e2abe496d2b9cf`
- Deploy config SHA-256: `fc6a2fd442e599fa239b43b0de826799bd19b70f08bb53ec8b0bbefe3860be8c`
- WASM SHA-256: `b342e1e0a4f3e4d5e1e388f29df31545fa9d5816a005c185e77c6b8727c1f9fa`
- teul-cli SHA-256: `be0183f2ef6e8646bea7f55ca25b01ce2545d6ae7c0ea2643cb51cc7c46c8105`
- Python version recorded by release: `3.13.5`
- SQLite version recorded by release: `3.49.1`
- SQLite private-pilot durability rule: fail-closed unless synchronous `FULL` and SQLite floor `3.51.3` or explicit operator attestation.
- Dependency image tags are non-`latest`; digest pin remains `verification_required` until operator-approved image source/digest input exists.

## Independent Review Request

No external Claude/independent review was executed in this Codex shell. The requested review packet for a reviewer is:

1. Re-run the private-pilot local rehearsal, release contract pack, and final local battery listed above.
2. Inspect whether the app port is exposed on a public interface in the reference compose profile.
3. Inspect whether project data, backup staging, and logs are outside the immutable release lifecycle.
4. Verify private-pilot SQLite fail-closed behavior for synchronous `FULL`, version floor, and operator attestation.
5. Verify release manifest stale/tamper detection and allowlist-only release content.
6. Verify non-root/read-only/resource limits in the reference Dockerfile and compose profile.
7. Verify edge body/rate/timeout/header/CSP policy and the boundary between browser CSP smoke and real nginx/TLS operation.
8. Verify health/readiness/operator endpoints do not expose capability, Authorization, DDN body, project path, or sensitive counts publicly.
9. Verify backup uses product `audit_integrity()` plus application backup, and empty-target restore rejects corrupt/incomplete/non-empty cases.
10. Verify rollback changes only code/current pointer and does not perform implicit data restore or data deletion.
11. Verify remote evidence is absent and correctly reported as blocked, not confused with local rehearsal.
12. Verify actual participant count and success count remain `0`.

Expected reviewer disposition for the current state is not `PASS_PRIVATE_IDC` or `PASS_READY_FOR_INVITED_ROUND0`; the valid disposition is `PASS_WITH_FOLLOW_UP` or `BLOCK_PILOT` depending on operator assessment of the missing real container/nginx/TLS and IDC input.
