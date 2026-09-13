# 20260715 Codex - Seamgrim Portable Project Content Exchange Wave 1

## G0

- START_HEAD sealed: `bbf0e16dfe137af774bbc0091c521e1e6729f92b`.
- Branch: `codex/queue-20260706`.
- `5ba698b fix(seamgrim): preserve composed trajectory views` is an ancestor of START_HEAD.
- `docs/ssot/**` was clean at start.
- Existing dirty/untracked files were not stashed, reset, staged, or modified.
- The portable exchange goal remains local-only and does not touch blocked container/IDC work.

## Baseline Verification

- PASS: `python tests/run_seamgrim_one_file_ddn_create_run_check.py`
- PASS: `python tests/run_seamgrim_project_share_clone_check.py`
- PASS: `python tests/run_seamgrim_workbench_my_work_reopen_check.py`
- Baseline drift: `python tests/run_seamgrim_workbench_shell_check.py` fails with
  `create button missing` because it targets legacy `ui/index.html` shell DOM
  (`#btn-create`). The current portable product path is `ui/workbench/`.

## Boundary Decisions

- Reuse `seamgrim.project_snapshot_artifact.v0` as the portable JSON basis.
- Do not create a new stable portable schema in Wave 1.
- Do not export capability, Authorization, edit/view link, server path, browser
  history, localStorage keys, run archive, checkpoint archive, or public trust badge.
- Keep `카-3` as primary attribution, with `마-3` and `타-2` as supporting evidence only.

## Next

- G1: product helper for portable artifact generation, exact validation,
  canonical/SHA verification, size limit, forbidden-field scan, diagnostic mapping,
  safe filename, and field-preservation audit.

## G1

- Added `solutions/seamgrim_ui_mvp/ui/workbench/persistence/portable_project_artifact.js`.
- Kept the portable file basis as `seamgrim.project_snapshot_artifact.v0`.
- Added `seamgrim_portable_project_artifact_v1` pack and runner-backed checker.
- Negative controls reject wrong schema, canonical mismatch, SHA mismatch,
  oversize, forbidden capability fields, prototype pollution keys, invalid UTF-8,
  and invalid JSON.

Verification:

- PASS: `node tests/seamgrim_portable_project_artifact_runner.mjs`
- PASS: `python tests/run_seamgrim_portable_project_artifact_check.py`
- PASS: `python tests/run_pack_golden.py seamgrim_portable_project_artifact_v1`
- PASS: `git status --short -- docs/ssot`

Next:

- G2: wire current workbench project export to the portable artifact helper and
  download deterministic UTF-8 JSON without saving a server revision.

## G2

- Added compact toolbar export command `portable-project-export`.
- Export uses the G1 helper and keeps the file schema as
  `seamgrim.project_snapshot_artifact.v0`.
- Export includes current editor source, controls snapshot, metadata candidate,
  and lineage candidate.
- Export does not save server projects, append revisions, or export capability
  links.
- Added `seamgrim_portable_project_workbench_v1` pack/checker and browser runner.

Verification:

- PASS: `python tests/run_seamgrim_portable_project_workbench_check.py`
- PASS: `python tests/run_pack_golden.py seamgrim_portable_project_workbench_v1`
- PASS: `python tests/run_seamgrim_portable_project_artifact_check.py`

Next:

- G3: safe import, validation preview, no auto-run, and current-project
  preservation on invalid/cancelled import.

## G3

- Added compact import command and hidden file input.
- Added import preview panel with integrity/trust boundary text.
- Added local received-project registration after explicit `열기`.
- Import preview and open do not start WASM runs.
- Tampered file rejection preserves current project and run state.
- Old wrapper schema rejection preserves current project and source editor.
- Import cancellation clears the preview without changing current project or
  source editor.
- HTML-like imported metadata is displayed via text nodes.

Verification:

- PASS: `python tests/run_seamgrim_portable_project_workbench_check.py`
- PASS: `python tests/run_seamgrim_portable_project_artifact_check.py`
- PASS: `python tests/run_pack_golden.py seamgrim_portable_project_workbench_v1`

Next:

- G4: metadata descriptors become editable in a compact information section and
  participate in portable hash changes.

## G4

- Added compact content metadata editor to the approved workbench.
- Metadata stays inside existing snapshot `metadata`.
- No new DDN syntax, SSOT key, registry claim, or state_hash input was added.
- Metadata edits change the portable artifact hash and survive export/import
  preview.

Verification:

- PASS: `python tests/run_seamgrim_portable_project_workbench_check.py`
- PASS: `python tests/run_pack_golden.py seamgrim_portable_project_workbench_v1`
- PASS: `python tests/run_seamgrim_portable_project_artifact_check.py`

Next:

- G5: make original/import/clone lineage visible and preserve original content
  hash across import -> my version -> edit/save.

## G5

- Added visible lineage row: original, received file hash, current version.
- Added local clone path for received projects through existing `내 버전 만들기`
  control.
- Local clone preserves imported original content SHA while later edits generate
  a new current content SHA.
- Capability, edit/view link, and server path remain excluded from lineage.

Verification:

- PASS: `python tests/run_seamgrim_portable_project_workbench_check.py`
- PASS: `python tests/run_pack_golden.py seamgrim_portable_project_workbench_v1`
- PASS: `python tests/run_seamgrim_portable_project_artifact_check.py`

Next:

- G6: integrate received projects into `DDN 찾기` and `내 작업` while keeping
  `공식 모음` restricted to built-in official projects.

## G6

- `DDN 찾기` now searches official, received, and local clone projects together.
- `공식 모음` renders only built-in official projects.
- `내 작업` includes server work plus received portable catalog entries.
- Search includes metadata fields and required gaji.
- Duplicate import creates explicit catalog entries instead of silent overwrite.

Verification:

- PASS: `python tests/run_seamgrim_portable_project_workbench_check.py`
- PASS: `python tests/run_pack_golden.py seamgrim_portable_project_workbench_v1`
- PASS: `python tests/run_seamgrim_portable_project_artifact_check.py`

Next:

- G7: connect received projects to existing save/reopen behavior as new work and
  keep server/local status honest.

## G7

- Received/local clone projects now use the same server artifact builder as the
  save path.
- Server artifact preserves portable origin hash and metadata.
- Saving a received project creates a new server project identity.
- The source lesson id is not used as a server project append target.

Verification:

- PASS: `python tests/run_seamgrim_portable_project_workbench_check.py`
- PASS: `python tests/run_pack_golden.py seamgrim_portable_project_workbench_v1`
- PASS: `python tests/run_seamgrim_portable_project_artifact_check.py`

Next:

- G8: deterministic roundtrip and execution equality across representative
  snapshots.

## G8

- Added `seamgrim_local_content_exchange_quality_v1` pack/checker.
- Covered one-file, projectile, pendulum, grid, and curriculum auxiliary
  snapshots.
- Verified canonical/hash stability, current auxiliary field preservation,
  unknown snapshot field preservation, and edit hash inequality.

Verification:

- PASS: `python tests/run_seamgrim_local_content_exchange_quality_check.py`
- PASS: `python tests/run_pack_golden.py seamgrim_local_content_exchange_quality_v1`
- PASS: `python tests/run_seamgrim_portable_project_workbench_check.py`

Next:

- G9: four viewport browser workflow, accessibility/overflow recovery, and
  invalid/cancel recovery checks.

## G9

- Extended the workbench browser runner across `1440x900`, `1024x768`,
  `778x912`, and `390x844`.
- Each viewport performs new DDN -> metadata edit -> run -> export artifact ->
  import preview -> explicit open -> explicit run.
- Added UI checks for source/Bogae panel height, import/export accessible names,
  visible controls, and horizontal overflow.
- Added browser checks for old-schema rejection and valid-import cancellation
  recovery preserving the current project.
- Fixed a product bug found by the gate: the new one-file default DDN now uses
  `값: 수 <- (1) 매김 { ... }.` so the parser frontdoor accepts it.

Verification:

- PASS: `python tests/run_seamgrim_portable_project_workbench_check.py`
- PASS: `python tests/run_seamgrim_one_file_ddn_create_run_check.py`
- PASS: `python tests/run_pack_golden.py seamgrim_portable_project_workbench_v1 seamgrim_local_content_exchange_quality_v1`

## G10

- Completed final integrated quality/report packet.
- `PORTABLE_PROJECT_ARTIFACT_CLOSED`: behavior-closed.
- `LOCAL_CONTENT_EXCHANGE_CLOSED`: behavior-closed.
- Docs-only/open: public registry, official author identity, signature, formal
  gaji package linkage, maru promotion.
- Not implemented: account/login/team/cloud, IDC/container, multi-module
  resolver/linker, remote dependency resolution, new DDN syntax, `state_hash`
  formula changes, Korean Manim full completion.

G10 verification:

- PASS: `python tests/run_seamgrim_portable_project_artifact_check.py`
- PASS: `python tests/run_seamgrim_portable_project_workbench_check.py`
- PASS: `python tests/run_seamgrim_local_content_exchange_quality_check.py`
- PASS: `python tests/run_pack_golden.py seamgrim_portable_project_artifact_v1 seamgrim_portable_project_workbench_v1 seamgrim_local_content_exchange_quality_v1`
- PASS: `python tests/run_seamgrim_one_file_ddn_create_run_check.py`
- PASS: `python tests/run_seamgrim_public_physics_wedge_quality_gate_check.py`
- PASS: `python tests/run_seamgrim_workbench_durable_quality_gate_check.py`
- PASS: `python tests/run_seamgrim_runner_lifecycle_reliability_check.py`
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS: `python tests/run_ddn_cli_wasm_true_parity_equality_check.py`
- PASS: `python tests/run_ddn_cli_wasm_sync_gate_check.py`
- PASS: `python tests/run_seamgrim_view_only_state_hash_invariant_check.py`
- PASS: `python tests/run_ganada_maru_verification_contract_check.py`
- PASS: `cargo check`
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS: `cargo test -p ddonirang-tool --no-run`
- PASS: `python tests/run_ci_sanity_gate.py --profile core_lang`
- PASS: `git diff --check`
- PASS: `git status --short -- docs/ssot`

Maru impact:

- `카-3`: portable project/share UI product evidence added; no automatic promotion.
- `마-3`: creator workbench product evidence added; no automatic promotion.
- `타-2`: hash/roundtrip/browser gate evidence added; no automatic promotion.
- `카-4`: local exchange evidence only; public registry not implemented.
- `나-4`: required gaji display evidence only; install/registry not implemented.
