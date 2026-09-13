# 2026-07-16 Codex — Seamgrim Workbench Multi-file Execution Truth

## Scope

- Goal: approved Seamgrim Workbench must execute the currently edited DDN file tree through the common Rust/WASM local-project resolver/linker, then run the linked source through the existing WASM VM lifecycle.
- START_HEAD: `2ac5905`
- Branch: `codex/queue-20260706`
- Ancestor check: `5ba698b` is an ancestor of START_HEAD.
- SSOT boundary: `docs/ssot/**` read-only; `git status --short -- docs/ssot` was clean at start.
- UI baseline: `docs/context/briefs/BRIEF_SEAMGRIM_DDN_DETERMINISTIC_PROJECT_WORKBENCH_UI_V1_20260712.md`, approved choices `1C-2C-3B-4B-5B-6C-7C-8B-9C`.

## G0 Baseline Seal

The existing evidence proves portable project artifact rendering, not direct execution of the current Workbench file tree.

Evidence:

- `solutions/seamgrim_ui_mvp/ui/workbench/workbench.js:1126` defines `activeSourceText()` as `lesson.ddn` or active file text only.
- `solutions/seamgrim_ui_mvp/ui/workbench/workbench.js:1956` starts the current run path.
- `solutions/seamgrim_ui_mvp/ui/workbench/workbench.js:1994` calls `await wasm.updateLogic(source)` with that single source string.
- `tests/seamgrim_multifile_project_workbench_runner.mjs:504` imports `variantArtifactFile` for the changed module result instead of editing the module in the Workbench and rerunning.
- `tool/src/local_project.rs:1192` executes project summary by calling `runtime_surface::run_summary_from_source(...)`; this is a bounded summary path, not the Workbench button lifecycle.

Reproduction:

- `python tests/run_seamgrim_multifile_project_workbench_check.py` PASS at START_HEAD.
- That PASS is a false-positive for `approved Workbench multi-file execution` because the runner imports a second precomputed artifact for the value-change comparison.

## Gate Plan

- G1/G2: add current/imported/previous-success execution state and build deterministic `VirtualProjectSource` from Workbench file tabs and contents.
- G3: add a Rust/WASM prepare/link frontdoor that returns normalized graph, lock status, linked execution source, project graph hash, and deterministic diagnostics before VM execution.
- G4/G5: route Workbench Run through prepare/link plus VM lifecycle and prevent stale Bogae/current lineage after failure.
- G6/G7: prove in-browser module edit -> rerun without second import, with output, observation payload, state hash, trace, canvas signature, and pixel hash changing from actual execution.
- G8/G9: save/reopen/share/clone roundtrip and negative controls for resolver bypass, spacing, comments/strings, missing module, cycles, duplicate paths, and lock failure.

## Verification Log

- PASS: `git status --short -- docs/ssot`
- PASS: `python tests/run_seamgrim_multifile_project_workbench_check.py`

## G0-G9 Execution Closure

- G0 baseline seal: `1ca533f chore(seamgrim): seal workbench multifile execution baseline`
- G1-G2 current/imported/previous execution state model: `66f46e8 feat(seamgrim): model workbench current project source`
- G3 Rust/WASM prepare/link product frontdoor: `e93dfb0 feat(wasm): expose project prepare link frontdoor`
- G4-G7 Workbench Run button through current project tree plus module edit/rerun/failure browser proof: `3cfb810 feat(seamgrim): run workbench project tree through wasm`
- G8 current-run portable save/reopen/clone roundtrip boundary: `0870ad6 test(seamgrim): preserve current workbench project roundtrip`
- G9 resolver bypass and alias spacing boundary matrix: `3a9f29a test(seamgrim): harden workbench resolver bypass boundaries`

Additional verification after G8:

- PASS: `python tests/run_seamgrim_multifile_portable_roundtrip_check.py`
- PASS: `python tests/run_seamgrim_multifile_project_workbench_check.py`
- PASS: `python tests/run_pack_golden.py seamgrim_multifile_project_workbench_v1 seamgrim_multifile_portable_roundtrip_v1`

Additional verification after G9:

- PASS: `python tests/run_ddn_project_workbench_boundary_matrix_check.py`
- PASS: `python tests/run_pack_golden.py ddn_project_workbench_boundary_matrix_v1`

Closure boundary:

- Behavior-closed for the approved Workbench current project tree path: imported portable record is not treated as current execution; Run builds current `VirtualProjectSource`, routes through `wasm_project_prepare_link_json`, executes linked source via the WASM VM lifecycle, binds output/trace/state hash/canvas evidence, and preserves previous success after failure.
- Behavior-closed for G9 negative/positive controls listed in `ddn_project_workbench_boundary_matrix_v1`: direct single-file VM bypass rejection, resolver/linker VM success, alias dot-spacing equivalence, comment/string non-rewrite, missing/cycle/duplicate/private/lock fail-closed cases.
- Non-claims remain: no new DDN grammar, no runtime `state_hash` formula change, no JS-only resolver/linker, no public registry/cloud path, and no 한국어 Manim 전체 완료 claim.
