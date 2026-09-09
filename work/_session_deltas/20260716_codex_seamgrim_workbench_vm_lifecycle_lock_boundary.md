# 2026-07-16 Codex — Seamgrim Workbench VM Lifecycle / Archive / Lock Boundary

## Scope

- Goal: close approved Seamgrim Workbench multi-file VM lifecycle, failed server archive, and `ddn.lock` trust boundary.
- Branch: `codex/queue-20260706`
- Required baseline HEAD: `be7becb`
- START_HEAD: `be7becb7365869b4efd0a9ba5708677c342cb018`
- Ancestry check: `git merge-base --is-ancestor be7becb HEAD` PASS.
- SSOT boundary: `docs/ssot/**` remains read-only; `git status --short -- docs/ssot` was clean at start.
- Approved UI baseline: `docs/context/briefs/BRIEF_SEAMGRIM_DDN_DETERMINISTIC_PROJECT_WORKBENCH_UI_V1_20260712.md`, decision set `1C-2C-3B-4B-5B-6C-7C-8B-9C`.

## G0 Baseline Seal

The previous Workbench multi-file execution work is accepted as behavior-closed for first-run current project execution, module edit rerun, resolver bypass rejection, and portable roundtrip. This run starts from the next defects only.

Existing green checks at START_HEAD:

- PASS: `python tests/run_seamgrim_multifile_project_workbench_check.py`
- PASS: `python tests/run_seamgrim_multifile_portable_roundtrip_check.py`
- PASS: `python tests/run_ddn_project_workbench_boundary_matrix_check.py`

Those checks do not prove this goal's new closure because they do not require step-by-step project evidence refresh, failed archive finalization after a server run id exists, or fail-closed imported lock validation before regeneration.

## Confirmed Defects

### Defect A — project step evidence remains first-run-bound

Evidence:

- `solutions/seamgrim_ui_mvp/ui/workbench/workbench.js:2444` defines `stepForward()`.
- `solutions/seamgrim_ui_mvp/ui/workbench/workbench.js:2472` passes `sourceText: activeSourceText()` to the VM step path.
- `solutions/seamgrim_ui_mvp/ui/workbench/workbench.js:1328` defines `buildCurrentProjectRunEvidence(...)`, but `stepForward()` does not call it after appending a new frame.
- `solutions/seamgrim_ui_mvp/ui/workbench/workbench.js:416` returns only `state.projectExecution.current.evidence`, so render paths continue to expose stale evidence until a new run is started.

Required closure: for a project run, each successful step must rebuild current project evidence from the actual VM state and current frame while preserving the immutable source/project/link hashes for that run.

### Defect B — failed server run archive can remain running

Evidence:

- `solutions/seamgrim_ui_mvp/ui/workbench/workbench.js:2364` creates a server run archive before project prepare/link and VM runtime success are known.
- `solutions/seamgrim_ui_mvp/ui/workbench/workbench.js:2423` handles start failure by local `current_failure` state.
- `solutions/seamgrim_ui_mvp/ui/workbench/workbench.js:2429` records previous success lineage locally, but the catch path does not call `finalizeRunArchive(..., failed)`.

Required closure: prepare/link preflight should happen before server archive creation where possible; if a server run id already exists and runtime fails, the archive must finalize as `failed`, not remain orphan `running`.

### Defect C — imported lock can be regenerated before validation

Evidence:

- `solutions/seamgrim_ui_mvp/ui/workbench/workbench.js:2329` calls `refreshGeneratedProjectLockForRun(projectSource)` before `prepareCurrentProjectLink(...)`.
- `solutions/seamgrim_ui_mvp/ui/workbench/workbench.js:2157` defines `refreshGeneratedProjectLockForRun(...)`.
- `solutions/seamgrim_ui_mvp/ui/workbench/workbench.js:2168` regenerates `ddn.lock` from the current source and updates `state.fileTexts`.

Required closure: imported/reopened lock bytes must be validated unchanged first. Missing or mismatched locks must fail closed without changing lock/source/current execution state. Only a verified local non-lock edit may use the chosen deterministic lock update policy.

## Planned Gate Mapping

- G1-G4: project run plan retention, step evidence rebuild, stale source step rejection, dynamic 3+ madi browser lifecycle runner.
- G5-G6: prepare/link and archive ordering, failed archive finalize, restart persistence checks.
- G7-G9: imported/reopened lock prevalidation, explicit/tracked lock refresh policy for verified local edits, lock attack negative controls.
- G10-G14: portable/viewport/CLI-WASM/single-file/durable/public wedge regression and final audit.

## Non-Claims

- No new DDN grammar.
- No runtime `state_hash` formula change.
- No JS-only resolver/linker.
- No public registry/cloud/login/IDC expansion.
- No Korean Manim overall completion claim.

## G1-G4 Lifecycle Closure

Commit: `695e0e2 feat(seamgrim): rebind project step evidence`

- Preserved project prepare/link output as `run.project_execution_plan`.
- Rebound project `stepForward()` to the run's linked execution source.
- Rebuilt current project evidence after each successful project VM step.
- Rejected stale source stepping with `E_PROJECT_RUN_STALE_SOURCE_STEP_REJECTED`.
- Added dynamic multi-file project browser workflow with run, two steps, pause, resume, stop, stale edit rejection, and edited-source rerun.

Verification:

- PASS: `python tests/run_seamgrim_multifile_project_workbench_check.py`
- PASS: `python tests/run_pack_golden.py seamgrim_multifile_project_workbench_v1`

## G5-G6 Failed Archive Closure

Commit: `fd0723b feat(seamgrim): finalize failed project run archives`

- Moved project prepare/link preflight before server run archive creation where possible.
- Added failed archive finalization for runtime failures after a server run id exists.
- Added restart persistence check proving stopped and failed archives survive server restart with zero `running` orphan archive.

Verification:

- PASS: `python tests/run_seamgrim_multifile_project_workbench_check.py`

## G7-G9 Lock Boundary Closure

Commit: `67a1b03 feat(seamgrim): validate project lock trust boundary`

- Added Workbench lock trust state.
- Imported/reopened project locks are validated unchanged before any refresh.
- Only a verified local non-lock edit marks the lock refresh path eligible.
- Manual `ddn.lock` edits clear trust and are not overwritten.
- Added valid-outer-wrapper lock attack fixtures for tampered lock, missing lock, project graph hash tamper, package pin/hash tamper, and manual lock edit.
- Added normal verified local module edit refresh evidence.

Verification:

- PASS: `node tests/seamgrim_multifile_project_workbench_runner.mjs`
- PASS: `python tests/run_seamgrim_multifile_project_workbench_check.py`
- PASS: `python tests/run_pack_golden.py seamgrim_multifile_project_workbench_v1`
- PASS: `git diff --check -- solutions/seamgrim_ui_mvp/ui/workbench/workbench.js tests/seamgrim_multifile_project_workbench_runner.mjs tests/run_seamgrim_multifile_project_workbench_check.py pack/seamgrim_multifile_project_workbench_v1/contract.detjson`

## G10-G12 Regression Verification

PASS:

- `python tests/run_seamgrim_multifile_project_workbench_check.py`
- `python tests/run_seamgrim_multifile_portable_roundtrip_check.py`
- `python tests/run_ddn_project_workbench_boundary_matrix_check.py`
- `python tests/run_pack_golden.py seamgrim_multifile_project_workbench_v1 seamgrim_multifile_portable_roundtrip_v1 ddn_project_workbench_boundary_matrix_v1`
- `python tests/run_ddn_cli_wasm_freshness_check.py`
- `python tests/run_ddn_cli_wasm_true_parity_equality_check.py`
- `python tests/run_ddn_cli_wasm_sync_gate_check.py`
- `python tests/run_ddn_local_project_cli_wasm_parity_check.py`
- `python tests/run_seamgrim_one_file_ddn_create_run_check.py`
- `python tests/run_ddn_local_project_workbench_multifile_check.py`
- `python tests/run_seamgrim_workbench_durable_quality_gate_check.py`
- `python tests/run_seamgrim_public_physics_wedge_quality_gate_check.py`
- `cargo check`
- `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- `python tests/run_ci_sanity_gate.py --profile core_lang`
- `git status --short -- docs/ssot`

Notes:

- First `python tests/run_ddn_cli_wasm_sync_gate_check.py` timed out at 300s; rerun with 600s PASS.
- First `python tests/run_ddn_local_project_cli_wasm_parity_check.py` saw a transient Rust target/cache collision while other cargo tasks were running; sequential rerun PASS.
- `git diff --check` exited 0 but printed CRLF warnings for existing unrelated dirty files.
- Sanity-gate-generated open logs were restored:
  - `pack/open_bundle_artifact/run_bundle/geoul.diag.jsonl`
  - `pack/open_end_to_end/open.log.jsonl`

## G13 Report

- Added `docs/reports/impl/SEAMGRIM_WORKBENCH_MULTIFILE_VM_LIFECYCLE_CLOSED_V1_20260716.md`.
- Included independent review request for:
  1. dynamic run -> step -> step hash/trace/pixel changes,
  2. runtime failure archive `failed` after restart,
  3. valid-wrapper tampered lock fail-closed with source/lock/current binding unchanged.

## G14 Final Promotion Gate

Final gate after G13 report commit:

- PASS: `python tests/run_seamgrim_multifile_project_workbench_check.py`
- PASS: `python tests/run_seamgrim_multifile_portable_roundtrip_check.py`
- PASS: `python tests/run_ddn_project_workbench_boundary_matrix_check.py`
- PASS: `python tests/run_pack_golden.py seamgrim_multifile_project_workbench_v1 seamgrim_multifile_portable_roundtrip_v1 ddn_project_workbench_boundary_matrix_v1`
- PASS: `cargo check`
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS: `python tests/run_ci_sanity_gate.py --profile core_lang`
- PASS: `git diff --check` exit code 0. It still prints CRLF warnings for existing unrelated dirty files.
- PASS: `git status --short -- docs/ssot` clean.

Post-sanity generated logs restored again:

- `pack/open_bundle_artifact/run_bundle/geoul.diag.jsonl`
- `pack/open_end_to_end/open.log.jsonl`

Closure claim:

- `WORKBENCH_MULTIFILE_VM_LIFECYCLE_CLOSED` is behavior-closed for the approved Workbench multi-file project path.
- Still non-claims: no new DDN grammar, no runtime `state_hash` formula change, no JS-only resolver/linker, no public registry/cloud/login/IDC, no Korean Manim overall completion.
