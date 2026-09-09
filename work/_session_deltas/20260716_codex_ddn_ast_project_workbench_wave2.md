# Codex Session Delta - DDN AST Project Runtime + Seamgrim Workbench Wave 2

Date: 2026-07-16 KST

## Post-blocker resume - new START_HEAD and G0-G9 recheck

- User instruction: predecessor blocker `5ba698b fix(seamgrim): preserve composed trajectory views` has been verified/committed; seal current HEAD as the new START_HEAD and resume G0 through G9.
- Branch: `codex/queue-20260706`
- New START_HEAD: `24bfae5 test(seamgrim): verify multifile workbench viewport quality`
- `5ba698b` ancestry from new START_HEAD: PASS
- Relevant product files for this scope were clean before the recheck.
- `git status --short -- docs/ssot`: clean
- Pre-existing unrelated dirty/untracked files were not reset, stashed, staged, or committed.
- G13 draft files already present in the worktree remained out of scope for this G0-G9 resume and were not staged.

Rechecked G0-G9 evidence from the new START_HEAD:

- PASS: `python tests/run_ddn_local_project_graph_check.py`
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS: `python tests/run_pack_golden.py ddn_local_project_graph_v1`
- PASS: `python tests/run_ddn_local_project_cli_wasm_parity_check.py`
- PASS: `python tests/run_ddn_local_project_workbench_multifile_check.py`
- PASS: `node tests/seamgrim_multifile_project_workbench_runner.mjs`
  - viewports: `1440x900`, `1024x768`, `778x912`, `390x844`
  - physics output: `["7","10"]`
  - grid output: `["3"]`
  - evidence report: `I:/home/urihanl/ddn/codex/out/seamgrim_multifile_project_workbench_v1/latest/evidence.detjson`
- PASS: `python tests/run_pack_golden.py seamgrim_multifile_project_workbench_v1 ddn_local_project_workbench_multifile_v1`
- PASS: `python tests/run_seamgrim_multifile_project_workbench_check.py`
- PASS: `node tests/ddn_local_project_graph_runner.mjs run pack/ddn_local_project_graph_v1/fixtures/project_run_physics_v1.json 앱`
- PASS: `node tests/ddn_local_project_graph_runner.mjs run pack/ddn_local_project_graph_v1/fixtures/project_run_grid_v1.json 앱`
- PASS: `python tests/run_nurigym_step_record_v02_consumer_g6_check.py`
- PASS: `python tests/run_nurigym_step_record_v02_roundtrip_check.py`
- PASS: `python tests/run_nurigym_step_record_v02_public_schema_check.py`
- PASS: `python tests/run_nurigym_shared_sync_action_pipeline_pack_check.py`
- PASS: `python tests/run_nuri_gym_contract_check.py`
- PASS: `python tests/run_pack_golden.py nurigym_step_record_v02_roundtrip_v1 nurigym_step_record_v02_public_schema_v1 nurigym_shared_sync_action_pipeline_v1 nuri_gym_canon_contract_v1`
- PASS: `cargo check` (existing unused/dead-code warnings only)
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml` (existing unused/dead-code warnings only)
- PASS: `python tests/run_ci_sanity_gate.py --profile core_lang`
- PASS: `git diff --check` (exit 0; CRLF warnings only from pre-existing unrelated dirty files)
- PASS: `git status --short -- docs/ssot` (no output)

Sanity-generated tracked open-log 부산물 were restored after verification:

- `pack/open_bundle_artifact/run_bundle/geoul.diag.jsonl`
- `pack/open_end_to_end/open.log.jsonl`

Boundary notes:

- No new DDN grammar.
- No runtime `state_hash` formula change.
- No `docs/ssot/**` changes.
- This resume revalidates G0-G9 from `24bfae5`; it does not claim G10-G16 completion.

## G0 - START_HEAD reseal and baseline counterexamples

- Branch: `codex/queue-20260706`
- New START_HEAD: `7d9724abf85b3f0c526cd5a568e2a746b5b68630`
- Predecessor blocker: `5ba698b fix(seamgrim): preserve composed trajectory views`
- `5ba698b` ancestry from START_HEAD: PASS
- `git status --short -- docs/ssot`: clean
- Pre-existing dirty/untracked status lines at reseal: 172
- Existing dirty/untracked files are treated as other-work ownership and were not reset, stashed, staged, or committed.

Baseline reproduction:

- Normal local-project alias run:
  - fixture: `I:/home/urihanl/ddn/codex/out/ast_project_wave2_g0_repro/local_normal.json`
  - command: `cargo run -q --manifest-path tools/teul-cli/Cargo.toml -- project-run --virtual <fixture> --target 앱 --inspect-graph`
  - result: PASS, `output_rows=["7","10"]`
- Whitespace alias run before repair:
  - fixture: `I:/home/urihanl/ddn/codex/out/ast_project_wave2_g0_repro/local_space.json`
  - surface: `운동 . 속도구하기 보여주기.` and `물리 . 중력 보여주기.`
  - result: FAIL with `E_PROJECT_RUNTIME`, message `정의되지 않은 변수: 운동`
- Gaji-backed whitespace variant reached `ddn.lock` mismatch first when using the normal fixture lock, confirming lock bytes include source-sensitive graph input. This remains a G3/G4 boundary note, not a runtime alias proof.

Boundary table:

| Surface | Current G0 result | Boundary |
|---|---|---|
| `teul-cli project-run` normal alias | PASS | Product project frontdoor |
| `teul-cli project-run` whitespace alias | FAIL before repair | Product project frontdoor |
| raw WASM project-run | Pending recheck after repair | Existing `tests/ddn_local_project_graph_runner.mjs` currently hardcodes inspect-lock=true |
| official `teul-cli run --summary-json` | Control only after linked source generation | Not a project loader |
| Seamgrim multi-file workbench Bogae binding | Pending | Current Wave1 runner proves project summary, not enough for real Bogae binding |

Non-claims:

- No new DDN grammar.
- No runtime `state_hash` formula change.
- No `docs/ssot/**` changes.
- No 90-cell Ganada or broader Korean Manim completion claim.

Next:

- G1: remove exact-string alias replacement semantics from local project linked-source construction and prove normal/whitespace alias equality without rewriting strings or comments.

## G1 - token/span project alias rewrite repair

Implemented:

- Replaced the remaining exact-string `replace_alias_qualified_refs` path in `tool/src/local_project.rs`.
- Added token/span-based project alias rewrite:
  - uses `ddonirang_lang::Lexer`;
  - rewrites only `alias . symbol` token triples whose gaps are whitespace-only;
  - skips string literals and `//` comments because those are not alias-reference token triples;
  - supports normal `운동.속도구하기` and whitespace `운동 . 속도구하기` project frontdoor surfaces without changing core parser grammar.
- Kept alias-qualified `보여주기` discovery on parser/AST for parser-supported field access, with a project-frontdoor token fallback for whitespace alias access.
- Added fixtures:
  - `pack/ddn_local_project_graph_v1/fixtures/project_run_alias_normal_v1.json`
  - `pack/ddn_local_project_graph_v1/fixtures/project_run_alias_spacing_v1.json`
- Added expected product summaries:
  - `pack/ddn_local_project_graph_v1/expected/project_run_alias_normal_v1.detjson`
  - `pack/ddn_local_project_graph_v1/expected/project_run_alias_spacing_v1.detjson`
- Strengthened `tests/run_ddn_local_project_graph_check.py`:
  - normal and whitespace aliases must have the same `output_rows`, runtime output, final row, runtime state hash, execution envelope, linked source, canonical DDN, linked source hash, canonical hash, symbol boundary hash, and bounded state hash;
  - source-sensitive `project_graph_sha256` must remain different as a negative control;
  - raw WASM runner must match the same selected fields;
  - string/comment fake aliases must remain preserved and must not add output rows.
- Rebuilt Seamgrim WASM product artifact and refreshed `ddonirang_tool.manifest.detjson`.

Verification:

- PASS: `python tests/run_ddn_local_project_graph_check.py`
- PASS: `python tests/run_pack_golden.py ddn_local_project_graph_v1`
- PASS: `node tests/ddn_local_project_graph_runner.mjs run pack/ddn_local_project_graph_v1/fixtures/project_run_alias_normal_v1.json 앱`
- PASS: `node tests/ddn_local_project_graph_runner.mjs run pack/ddn_local_project_graph_v1/fixtures/project_run_alias_spacing_v1.json 앱`
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS: `cargo check -p ddonirang-tool`
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`

Boundary notes:

- No new DDN grammar. The whitespace alias equivalence is a local-project frontdoor linked-source normalization only.
- No runtime `state_hash` formula change.
- No `docs/ssot/**` changes.

Next:

- G2: audit module boundary diagnostics/determinism against the strengthened alias rewrite path, then keep or repair remaining gaps before moving to lock/prep artifact work.

## G2 - module boundary diagnostics and determinism hardening

Implemented:

- Added duplicate module-boundary fixtures:
  - `project_module_duplicate_import_v1.json`
  - `project_module_duplicate_export_v1.json`
- Added pack golden negative rows for:
  - `E_IMPORT_ALIAS_DUPLICATE`
  - `E_EXPORT_DUPLICATE`
- Added optional `source_span` to local project fatal error JSON. Existing errors do not emit the field unless a span is known.
- Kept project metadata duplicate-key behavior unchanged, but changed `쓰임 {}` parsing to preserve duplicate aliases long enough for module-boundary diagnostics.
- Added source-span lookup for duplicate `쓰임` keys and duplicate `드러냄`/`공개` keys.
- Strengthened `tests/run_ddn_local_project_graph_check.py` so duplicate import/export diagnostics must include:
  - stable code,
  - source project file path,
  - ordered integer `source_span.start/end`.

Verification:

- PASS: `python tests/run_ddn_local_project_graph_check.py`
- PASS: `python tests/run_pack_golden.py ddn_local_project_graph_v1`
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS: `cargo check -p ddonirang-tool`
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`

Boundary notes:

- No new DDN grammar.
- No runtime `state_hash` formula change.
- No `docs/ssot/**` changes.
- Span coverage was added for the duplicate diagnostics touched in this gate; it is not a claim that every project diagnostic in the product has source spans.

Next:

- G3: add execution preparation artifact/lock policy evidence without changing the runtime state hash formula.

## G3 - execution preparation artifact and lock boundary

Implemented:

- Added `execution_preparation` to the local project run summary product artifact.
- Artifact schema: `ddn.local_project.execution_preparation.v1`.
- The artifact records:
  - project/root/entry/target identity,
  - project graph hash, module graph order, module graph hash,
  - lock inspection and lock hash boundary,
  - linked execution source hash and canonical hash,
  - runtime frontdoor request (`teul-cli project-run`, requested ticks = 1),
  - local project file/artifact limits,
  - imports, exports, and resolved-symbol provenance,
  - `state_hash_formula_change=false`.
- Included `execution_preparation` in the deterministic summary hash input, while leaving the runtime `state_hash` formula untouched.
- Updated expected product artifacts for:
  - `project_run_summary_v1`
  - `project_run_grid_summary_v1`
  - `project_run_alias_normal_v1`
  - `project_run_alias_spacing_v1`
  - `workbench_project_run_v1`
- Strengthened `tests/run_ddn_local_project_graph_check.py` so CLI, raw WASM, and alias-spacing product summaries must all expose the same execution preparation contract.
- Rebuilt Seamgrim WASM product artifact and refreshed `ddonirang_tool.manifest.detjson`.

Verification:

- PASS: `python tests/run_ddn_local_project_graph_check.py`
- PASS: `python tests/run_pack_golden.py ddn_local_project_graph_v1`
- PASS: `python tests/run_pack_golden.py ddn_local_project_workbench_multifile_v1`
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS: `python tests/run_ddn_local_project_workbench_multifile_check.py`
- PASS: `cargo check -p ddonirang-tool`
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS: `git status --short -- docs/ssot`

Boundary notes:

- No new DDN grammar.
- No runtime `state_hash` formula change.
- `execution_preparation` is a product artifact field and a summary hash input, not a runtime state-hash input.
- No `docs/ssot/**` changes.

Next:

- G4: harden CLI/WASM/shared runtime equality and negative controls around changed source, target selection, stale WASM, alias spacing, and fake assignment surfaces.

## G4 - CLI/WASM/shared runtime parity negative controls

Implemented:

- Strengthened `tests/run_ddn_local_project_graph_check.py` with product-path negative controls:
  - mutate a local module value (`속도구하기 <- 7.` to `8`) and require CLI/raw WASM byte equality, changed output rows, changed runtime final row, changed runtime state hash, changed linked-source/canonical hashes, changed bounded state hash, and changed summary hash;
  - remove one output row and require CLI/raw WASM byte equality plus changed linked-source/canonical/bounded/summary hashes;
  - request a missing target and require `E_PROJECT_TARGET_MISSING` through both CLI and raw WASM;
  - re-run linked product source through the official `teul-cli run --summary-json` shared runtime path for the mutated-value and output-row-removal controls.
- Kept stale WASM protection in the existing `run_ddn_cli_wasm_freshness_check.py` gate.
- Kept the existing fake `:=`, whitespace alias, and string/comment alias negative controls.

Verification:

- PASS: `python tests/run_ddn_local_project_graph_check.py`
- PASS: `python tests/run_pack_golden.py ddn_local_project_graph_v1`
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS: `cargo check -p ddonirang-tool`
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS: `git status --short -- docs/ssot`

Boundary notes:

- This gate changes checker coverage only; no runtime behavior was changed.
- No new DDN grammar.
- No runtime `state_hash` formula change.
- No `docs/ssot/**` changes.

Next:

- G5: move from artifact parity to product project execution lifecycle in the Seamgrim workbench.

## G5 - Seamgrim project execution lifecycle

Implemented:

- Added a product lifecycle panel to the Seamgrim create/editor project workbench:
  - `project-run-lifecycle`
  - `project-run-status`
  - `project-active-run-id`
  - `project-run-archive-count`
  - `project-run-history`
- Added editor-side lifecycle state:
  - `idle -> running -> completed/failed`
  - stable local run ids (`project_run_001`, ...),
  - source candidate hash for the submitted virtual project source,
  - immutable recent run archive rows,
  - summary hash, bounded state hash, graph hash, output rows, diagnostics.
- Existing `project-run-result` JSON output is preserved for current pack/checker compatibility.
- Reset lifecycle state when entering a fresh project mode or loading a different virtual project.
- Strengthened the existing browser runner so the product workflow must prove:
  - first run completes as `project_run_001`;
  - second run after module edit completes as `project_run_002`;
  - archive count grows from 1 to 2;
  - run history order is newest first;
  - summary hash is bound to the visible run record;
  - source candidate hash changes when a module value changes.

Verification:

- PASS: `node tests/ddn_local_project_workbench_multifile_runner.mjs`
- PASS: `python tests/run_ddn_local_project_workbench_multifile_check.py`
- PASS: `python tests/run_pack_golden.py ddn_local_project_workbench_multifile_v1`
- PASS: `git status --short -- docs/ssot`

Boundary notes:

- This is the Seamgrim create/editor product workbench lifecycle, not a new DDN runtime lifecycle primitive.
- No new DDN grammar.
- No runtime `state_hash` formula change.
- No `docs/ssot/**` changes.

Next:

- G6: make the project run summary produce deterministic observation trace rows that can be consumed by product UI and browser runners.

## G6 - deterministic project observation trace

Implemented:

- Added `project_observation_trace` to the product `ddn.local_project_run_summary.v1` artifact.
- Trace schema: `ddn.local_project.observation_trace.v1`.
- Each row records:
  - deterministic row index and `project.obs.N` id,
  - display name and internal name,
  - `value_text` matching `output_rows`,
  - committed madi from the runtime execution envelope,
  - target path,
  - runtime state hash,
  - resolved symbol source when available,
  - `state_hash_participation=false`.
- Added deterministic `trace_sha256` over the trace body.
- Included the trace in the summary hash input, without adding it to the runtime `state_hash` formula.
- Updated CLI expected artifacts for graph and workbench packs.
- Rebuilt Seamgrim WASM and refreshed the WASM manifest.
- Strengthened `tests/run_ddn_local_project_graph_check.py`:
  - CLI, raw WASM, alias spacing, mutated-value, and output-row-removal paths must all expose valid trace rows;
  - normal/spacing alias traces must be byte-equivalent;
  - trace rows must not claim runtime state hash participation.
- Added product UI rendering for the trace in the create/editor workbench:
  - `project-observation-trace`,
  - `project-observation-trace-hash`,
  - `project-observation-rows`.
- Strengthened the browser runner so the visible trace hash and observation rows must match the product summary, and must change after a module value edit.

Verification:

- PASS: `cargo check -p ddonirang-tool`
- PASS: `python tests/run_ddn_local_project_graph_check.py`
- PASS: `node tests/ddn_local_project_workbench_multifile_runner.mjs`
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS: `python tests/run_pack_golden.py ddn_local_project_graph_v1 ddn_local_project_workbench_multifile_v1`
- PASS: `python tests/run_ddn_local_project_workbench_multifile_check.py`
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS: `git status --short -- docs/ssot`

Boundary notes:

- No new DDN grammar.
- No runtime `state_hash` formula change.
- Trace hash is an artifact/view candidate hash, not the runtime state hash.
- No `docs/ssot/**` changes.

Next:

- G7: connect the approved Workbench multi-file authoring surface to the current project run rather than only package preview/static fixtures.

## G7 - approved Workbench current multi-file run evidence

Implemented:

- Preserved local project run fields in the portable project payload built from the create/editor product path:
  - `runtime_state_hash`
  - `summary_sha256`
  - `project_observation_trace`
  - `execution_preparation`
- Added approved Workbench local project run evidence derivation from `local_package_payload`.
- Bound imported multi-file project evidence to product UI:
  - root dataset `projectRunBound=true`,
  - root trace hash and bounded-state hash datasets,
  - run status text `project summary: current multi-file run`,
  - run hash from `bounded_state_sha256`,
  - run lineage from `wasm_project_run_summary_json`,
  - semantic observation rows from `project_observation_trace`.
- Strengthened `tests/seamgrim_multifile_project_workbench_runner.mjs` so the approved Workbench import/open flow must prove:
  - current run evidence is bound after opening a multi-file portable project;
  - trace hash matches the generated product summary;
  - bounded state hash matches the generated product summary;
  - semantic observation values match trace rows;
  - observation rows do not claim `state_hash` participation;
  - all checks hold across `1440x900`, `1024x768`, `778x912`, `390x844`.

Verification:

- PASS: `node tests/seamgrim_multifile_project_workbench_runner.mjs`
- PASS: `python tests/run_seamgrim_multifile_project_workbench_check.py`
- PASS: `python tests/run_pack_golden.py seamgrim_multifile_project_workbench_v1`
- PASS: `python tests/run_ddn_local_project_workbench_multifile_check.py`
- PASS: `git status --short -- docs/ssot`

Boundary notes:

- Approved Workbench now consumes existing product project-run summary evidence; it does not introduce new DDN syntax.
- No runtime `state_hash` formula change.
- No `docs/ssot/**` changes.
- WASM per-madi live stepping for arbitrary multi-file projects remains outside this gate; this gate binds the sealed project-run summary to the current Workbench surface.

Next:

- G8: make the approved Workbench Bogae canvas/view hash change with the current multi-file run result and prove before/after distinction.

## G8 - Bogae canvas and view artifact binding

Implemented:

- Updated approved Workbench `drawPreview()` so local project run evidence drives the primary Bogae canvas when present.
- Added deterministic product-side view artifact metadata:
  - `source=local_project_run_evidence`,
  - trace hash,
  - bounded-state hash,
  - output rows,
  - numeric values,
  - current view role and mode.
- Exposed canvas datasets:
  - `projectRunBound`,
  - `projectRunTraceSha256`,
  - `canvasSignature`,
  - `viewArtifactHash`.
- Kept static project previews for non-local-project or no-summary cases.
- Strengthened `tests/seamgrim_multifile_project_workbench_runner.mjs`:
  - samples canvas pixels,
  - verifies imported multi-file run canvas differs from the static public preview,
  - imports a second artifact with a changed module value,
  - proves trace hash, observation values, bounded-state hash, canvas signature, view artifact hash, and canvas pixels all change.

Verification:

- PASS: `node tests/seamgrim_multifile_project_workbench_runner.mjs`
- PASS: `python tests/run_seamgrim_multifile_project_workbench_check.py`
- PASS: `python tests/run_pack_golden.py seamgrim_multifile_project_workbench_v1`
- PASS: `python tests/run_ddn_local_project_workbench_multifile_check.py`
- PASS: `git status --short -- docs/ssot`

Boundary notes:

- The view artifact hash is a Workbench view/canvas candidate hash, not a runtime `state_hash`.
- No new DDN grammar.
- No runtime `state_hash` formula change.
- No `docs/ssot/**` changes.

Next:

- G9: run representative physics and grid/AI Gym verticals across CLI, raw WASM, and approved Workbench, then run final regression gates.

## G9 - representative vertical verification and final gates

Sealed status:

- START_HEAD for this resumed run remains `7d9724abf85b3f0c526cd5a568e2a746b5b68630`.
- G0 through G8 are split commits on `codex/queue-20260706`; G9 is verification/report only.

Representative physics/grid verticals:

- PASS: raw WASM project run, physics fixture:
  - `node tests/ddn_local_project_graph_runner.mjs run pack/ddn_local_project_graph_v1/fixtures/project_run_physics_v1.json 앱`
  - observed output rows: `["7","10"]`
  - observed trace hash: `357e8a2e886b365f659d8fafdc8bfd7956798906eda630e47908451b466901c2`
  - observed bounded state hash: `fc9cc56ac5abc767f548e76a595595a48c5184cee2e5cab397ef6e394644d254`
- PASS: raw WASM project run, grid fixture:
  - `node tests/ddn_local_project_graph_runner.mjs run pack/ddn_local_project_graph_v1/fixtures/project_run_grid_v1.json 앱`
  - observed output rows: `["3"]`
  - observed trace hash: `bd3fa11f54d759bed2de10ba75b304a9c6a3d3eda70e6c6df4ca9d598ed4682f`
  - observed bounded state hash: `5ca02f2e369ace706b2e06ef0808d0133f7531708a6135f6bf6612f677d99224`
- PASS: `python tests/run_ddn_local_project_graph_check.py`
- PASS: `python tests/run_pack_golden.py ddn_local_project_graph_v1`
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS: `python tests/run_ddn_local_project_cli_wasm_parity_check.py`

Approved Workbench / Bogae vertical:

- PASS: `node tests/seamgrim_multifile_project_workbench_runner.mjs`
  - viewports: `1440x900`, `1024x768`, `778x912`, `390x844`
  - physics output: `["7","10"]`
  - grid output: `["3"]`
  - physics graph: `907f8cd326be3ed6d59167ea4af27aa84208443491f7e670717dd2c9167097ea`
  - grid graph: `b0046380f646320645f9b414b88b1de893649317503937d06562dad6f048a97e`
- PASS: `python tests/run_seamgrim_multifile_project_workbench_check.py`
- PASS: `python tests/run_pack_golden.py seamgrim_multifile_project_workbench_v1 ddn_local_project_workbench_multifile_v1`
- PASS: `python tests/run_ddn_local_project_workbench_multifile_check.py`

AI Gym / NuriGym representative contracts:

- PASS: `python tests/run_nurigym_step_record_v02_consumer_g6_check.py`
- PASS: `python tests/run_nurigym_step_record_v02_roundtrip_check.py`
- PASS: `python tests/run_nurigym_step_record_v02_public_schema_check.py`
- PASS: `python tests/run_nurigym_shared_sync_action_pipeline_pack_check.py`
- PASS: `python tests/run_nuri_gym_contract_check.py`
- PASS: `python tests/run_pack_golden.py nurigym_step_record_v02_roundtrip_v1 nurigym_step_record_v02_public_schema_v1 nurigym_shared_sync_action_pipeline_v1 nuri_gym_canon_contract_v1`
- Note: `nurigym_step_record_v02_consumer_g6_v1` is checker-owned and has no `golden.jsonl`; it was verified with its dedicated checker rather than `run_pack_golden.py`.

Final regression:

- PASS: `cargo check` (existing unused/dead-code warnings only)
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml` (existing unused/dead-code warnings only)
- PASS: `python tests/run_ci_sanity_gate.py --profile core_lang`
- PASS: `git diff --check` (line-ending warnings only for pre-existing dirty files)
- PASS: `git status --short -- docs/ssot` (no output)
- Restored sanity-generated open-log 부산물:
  - `pack/open_bundle_artifact/run_bundle/geoul.diag.jsonl`
  - `pack/open_end_to_end/open.log.jsonl`

Boundary notes:

- No new DDN grammar.
- No runtime `state_hash` formula change.
- No `docs/ssot/**` changes.
- No 한국어 Manim 전체 완료 주장. This run closes only the requested DDN AST project runtime and Seamgrim multi-file deterministic Bogae Workbench vertical gates through G9.

## G10 - immutable project run lineage

Implemented:

- Added `seamgrim.local_project_run_lineage.v0` to local project payloads produced by the editor/project snapshot product path.
- Preserved these lineage fields without changing runtime `state_hash`:
  - `project_graph_hash`
  - `lock_hash`
  - `linked_source_hash`
  - `run_request_hash`
  - `parent_run_id`
  - `branch_madi`
  - `branch_state_hash`
  - `final_state_hash`
  - `view_artifact_hash`
  - `created_revision`
  - `lineage_hash`
- Bound lineage evidence into the approved Workbench:
  - root datasets for lineage/request/revision,
  - rendered run lineage text,
  - local summary archive text,
  - canvas dataset `projectRunLineageHash`,
  - Bogae view artifact hash input via `run_lineage_hash`.
- Strengthened `tests/seamgrim_multifile_project_workbench_runner.mjs` so imported project runs must preserve lineage hash, request hash, and created revision across all four viewports, and module value changes must change lineage hash as well as observation/canvas/view hashes.
- Strengthened `pack/seamgrim_multifile_project_workbench_v1/contract.detjson` and `tests/run_seamgrim_multifile_project_workbench_check.py` with lineage covers and runner token checks.

Verification:

- PASS: `node --check tests/seamgrim_multifile_project_workbench_runner.mjs`
- PASS: `node --check solutions/seamgrim_ui_mvp/ui/app.js`
- PASS: `node --check solutions/seamgrim_ui_mvp/ui/workbench/workbench.js`
- PASS: `python -m py_compile tests/run_seamgrim_multifile_project_workbench_check.py`
- PASS: `node tests/seamgrim_multifile_project_workbench_runner.mjs`
- PASS: `python tests/run_pack_golden.py seamgrim_multifile_project_workbench_v1`
- PASS: `python tests/run_seamgrim_multifile_project_workbench_check.py`

Boundary notes:

- No new DDN grammar.
- No runtime `state_hash` formula change.
- No `docs/ssot/**` changes.
- `view_artifact_hash` remains a Workbench view artifact candidate hash, not a runtime state hash input.

## G11 - save, export, reopen, clone, and recovery roundtrip

Implemented:

- Extended the existing `seamgrim_multifile_portable_roundtrip_v1` product runner instead of adding a parallel storage system.
- Preserved `run_lineage` when the main editor rebuilds a project snapshot from an unchanged saved multi-file project:
  - editor now remembers the loaded local project payload,
  - snapshot builder reuses saved lineage only when project graph, runtime state, summary hash, and bounded state hash still match.
- Strengthened product/browser roundtrip coverage:
  - main editor save/reopen preserves multi-file tree and run lineage,
  - view-link clone preserves multi-file tree and run lineage,
  - Workbench import preview/cancel/open/export preserves current project and run lineage,
  - Workbench server save/reopen preserves local project payload and run lineage,
  - Workbench clone preserves run lineage,
  - corrupt artifact import is rejected without state loss,
  - old wrapper schema import is rejected without state loss,
  - server restart with the same `SEAMGRIM_PROJECT_DATA_DIR` reopens both main editor and Workbench links with the same project tree and run lineage.
- Updated `pack/seamgrim_multifile_portable_roundtrip_v1` contract/readme from the older G10 label to G11 storage/roundtrip behavior.

Verification:

- PASS: `node --check solutions/seamgrim_ui_mvp/ui/app.js`
- PASS: `node --check solutions/seamgrim_ui_mvp/ui/screens/editor.js`
- PASS: `node --check tests/seamgrim_multifile_portable_roundtrip_runner.mjs`
- PASS: `python -m py_compile tests/run_seamgrim_multifile_portable_roundtrip_check.py`
- PASS: `python tests/run_pack_golden.py seamgrim_multifile_portable_roundtrip_v1`
- PASS: `node tests/seamgrim_multifile_portable_roundtrip_runner.mjs`
- PASS: `python tests/run_seamgrim_multifile_portable_roundtrip_check.py`
- PASS: `python tests/run_seamgrim_multifile_project_workbench_check.py`

Boundary notes:

- Reused existing portable project artifact and server project store.
- No new storage wrapper.
- No new DDN grammar.
- No runtime `state_hash` formula change.
- No `docs/ssot/**` changes.

## G12 - four viewport product quality evidence

Implemented:

- Extended `tests/seamgrim_multifile_project_workbench_runner.mjs` to write visual and structured evidence to external local artifact storage:
  - `I:/home/urihanl/ddn/codex/out/seamgrim_multifile_project_workbench_v1/latest/evidence.detjson`
  - one main-editor screenshot per required viewport,
  - import-preview/imported/variant Workbench screenshots per required viewport.
- The structured evidence records, per viewport:
  - editor/file navigator boxes,
  - keyboard focus,
  - overflow checks,
  - import preview box,
  - primary canvas height,
  - project trace/bounded state/lineage hashes,
  - semantic observation rows,
  - canvas signature and pixel hash before/after module value change.
- Strengthened `pack/seamgrim_multifile_project_workbench_v1` and its checker so screenshot/evidence output is part of the product quality gate.

Verification:

- PASS: `node --check tests/seamgrim_multifile_project_workbench_runner.mjs`
- PASS: `python -m py_compile tests/run_seamgrim_multifile_project_workbench_check.py`
- PASS: `python tests/run_pack_golden.py seamgrim_multifile_project_workbench_v1`
- PASS: `node tests/seamgrim_multifile_project_workbench_runner.mjs`
- PASS: `python tests/run_seamgrim_multifile_project_workbench_check.py`
- PASS: external evidence files listed under `I:/home/urihanl/ddn/codex/out/seamgrim_multifile_project_workbench_v1/latest`:
  - `evidence.detjson`
  - 4 `main-editor-*.png`
  - 4 `workbench-import-preview-*.png`
  - 4 `workbench-imported-*.png`
  - 4 `workbench-variant-*.png`

Boundary notes:

- Screenshot/evidence files are local generated artifacts and were not staged.
- No product claim beyond bounded multi-file Workbench visual execution.
- No new DDN grammar.
- No runtime `state_hash` formula change.
- No `docs/ssot/**` changes.

## G13 - failure, security, and resource boundary matrix

Implemented:

- Added product total UTF-8 project payload enforcement in `tool/src/local_project.rs`:
  - new bounded constant: `MAX_PROJECT_TOTAL_UTF8_BYTES = 2 * 1024 * 1024`;
  - failure code: `E_PROJECT_TOTAL_SIZE_LIMIT`;
  - no runtime `state_hash` formula change.
- Rebuilt the product WASM artifact and refreshed `ddonirang_tool.manifest.detjson` so CLI and raw WASM frontdoors share the new limit behavior.
- Added pack `ddn_project_workbench_boundary_matrix_v1`.
- Added runner `tests/ddn_project_workbench_boundary_matrix_runner.mjs`.
- Added checker `tests/run_ddn_project_workbench_boundary_matrix_check.py`.
- The runner directly exercises raw WASM project frontdoors, disk `teul-cli project-run`, portable project artifact parsing, and local project server APIs.
- Boundary matrix PASS rows:
  - `symlink_escape` -> `E_PROJECT_SYMLINK_ESCAPE`
  - `path_escape` -> `E_PROJECT_PATH_SEGMENT`
  - `absolute_path` -> `E_PROJECT_PATH_ABSOLUTE`
  - `windows_drive_path` -> `E_PROJECT_PATH_ABSOLUTE`
  - `unicode_normalization_collision` -> `E_PROJECT_PATH_DUPLICATE`
  - `case_fold_collision` -> `E_PROJECT_PATH_CASE_COLLISION`
  - `file_count_limit` -> `E_PROJECT_FILE_COUNT_LIMIT`
  - `file_size_limit` -> `E_PROJECT_FILE_SIZE_LIMIT`
  - `payload_size_limit` -> `E_PROJECT_TOTAL_SIZE_LIMIT`
  - `module_cycle` -> `E_IMPORT_CYCLE`
  - `private_symbol_access` -> `E_SYMBOL_NOT_EXPORTED`
  - `duplicate_export` -> `E_EXPORT_DUPLICATE`
  - `missing_lock` -> `E_LOCK_MISSING`
  - `tampered_lock` -> `E_LOCK_HASH_MISMATCH`
  - `unpinned_dependency` -> `E_GAJI_DEP_UNPINNED`
  - `running_file_change_fake_summary` -> `E_PROJECT_ENTRY_PARSE`
  - `formatter_alias_spacing_control` -> `E_ALIAS_UNKNOWN`
  - `comment_string_alias_negative_control` -> `STRING_COMMENT_ALIAS_NOT_EXECUTED`
  - `corrupt_portable_artifact` -> `E_PORTABLE_SNAPSHOT_SCHEMA`
  - `old_wrapper_rejected` -> `E_PORTABLE_WRAPPER_SCHEMA`
  - `portable_size_limit` -> `E_PORTABLE_FILE_TOO_LARGE`
  - `view_capability_write_attempt` -> `E_PROJECT_PERMISSION_DENIED`
  - `revision_conflict` -> `E_PROJECT_REVISION_CONFLICT`
  - `branch_state_hash_mismatch` -> `E_PROJECT_REVISION_CONFLICT`
  - `single_file_canvas_negative_control` -> `STATIC_CANVAS_MISUSE_REJECTED`

Verification:

- PASS: `cargo check -p ddonirang-tool`
- PASS: `powershell -ExecutionPolicy Bypass -File scripts/build_wasm_tool.ps1 -Profile release -Target web`
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py --write-manifest`
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS: `node --check tests/ddn_project_workbench_boundary_matrix_runner.mjs`
- PASS: `python -m py_compile tests/run_ddn_project_workbench_boundary_matrix_check.py`
- PASS: `python tests/run_pack_golden.py ddn_project_workbench_boundary_matrix_v1`
- PASS: `node tests/ddn_project_workbench_boundary_matrix_runner.mjs` (`case_count=25`)
- PASS: `python tests/run_ddn_project_workbench_boundary_matrix_check.py`
- PASS: `python tests/run_ddn_local_project_graph_check.py`
- PASS: `python tests/run_seamgrim_multifile_project_workbench_check.py`
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS: `git diff --check -- <G13 files>` (exit 0; CRLF warning only on refreshed WASM manifest)
- PASS: `git status --short -- docs/ssot` (no output)

Boundary notes:

- No new DDN grammar.
- No runtime `state_hash` formula change.
- No `docs/ssot/**` changes.
- No public registry, Git/remote resolver, IDC/cloud/login claim.
- The single-file canvas negative control is a checker-contract guard: it requires the existing multi-file Workbench runner to distinguish imported project canvas signature/pixels from the previous one-file public physics preview.

## G14 - integrated AST project visual Workbench gate

Implemented:

- Added pack `ast_project_visual_workbench_gate_v1`.
- Added checker `tests/run_ast_project_visual_workbench_gate_check.py`.
- The checker directly binds two evidence layers instead of only wrapping older reports:
  - AST module alias lowering parity for normal vs whitespace variant project fixtures;
  - Workbench product visual binding for the imported multi-file project across four viewports.
- The gate now verifies:
  - normal vs whitespace variant have identical output rows, runtime final row, runtime state hash, linked source/canonical hashes, execution envelope, bounded state hash, symbol boundary hash, and observation trace hash;
  - source graph hash remains source-sensitive as a negative control;
  - linked execution source does not leave spaced alias fragments such as `운동 .` or `물리 .`;
  - Workbench import/open/variant flow records four viewport evidence, semantic rows, canvas height/overflow/accessibility, project trace/bounded state/lineage, canvas signature, and canvas pixel hash;
  - imported project canvas signature/pixels change when a module value changes, proving product binding rather than static preview reuse.
- Aligned `tool/src/runtime_surface.rs` run-summary `state_hash` surface with the already-declared `DEFAULT_VIEW_PREFIXES` exclusion used by WASM:
  - this fixes CLI/WASM strict parity for view-producing cases;
  - core runtime `state_hash` formula was not changed.
- Fixed a teul-cli compile boundary where `ddonirang_tool` and `teul-cli` used different `serde_json::Value` versions by serializing the shared runtime summary into the local `JsonValue` before field extraction.
- Rebuilt product WASM and refreshed `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`.

Verification:

- PASS: `python -m py_compile tests/run_ast_project_visual_workbench_gate_check.py`
- PASS: `python tests/run_pack_golden.py ast_project_visual_workbench_gate_v1`
- PASS: `python tests/run_ast_project_visual_workbench_gate_check.py`
- PASS: `python tests/run_ddn_local_project_graph_check.py`
- PASS: `python tests/run_ddn_local_project_cli_wasm_parity_check.py`
- PASS: `python tests/run_seamgrim_wasm_cli_runtime_parity_check.py`
- PASS: `python tests/run_ddn_cli_wasm_true_parity_equality_check.py`
- PASS: `powershell -ExecutionPolicy Bypass -File scripts/build_wasm_tool.ps1 -Profile release -Target web`
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py --write-manifest`
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS: `python tests/run_ddn_cli_wasm_sync_gate_check.py`
- PASS: `python tests/run_ddn_local_project_workbench_multifile_check.py`
- PASS: `python tests/run_seamgrim_multifile_project_workbench_check.py`
- PASS: `python tests/run_seamgrim_view_only_state_hash_invariant_check.py`
- PASS: `python tests/run_seamgrim_workbench_durable_quality_gate_check.py`
- PASS: `cargo test -p ddonirang-tool`
- PASS: `cargo test --manifest-path tools/teul-cli/Cargo.toml`
- PASS: `cargo check`
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS: `python tests/run_ci_sanity_gate.py --profile core_lang`
- PASS: `git diff --check` (exit 0; CRLF warnings only from unrelated dirty files and refreshed manifest)
- PASS: `git status --short -- docs/ssot` (no output)

Boundary notes:

- No new DDN grammar.
- No core runtime `state_hash` formula change.
- `runtime_surface` now exposes the same view-prefix-excluded run-summary hash domain that the WASM product path already used and reported.
- No `docs/ssot/**` changes.
- `pack/open_bundle_artifact/run_bundle/geoul.diag.jsonl` and `pack/open_end_to_end/open.log.jsonl` were touched by sanity gate and restored before staging.

## G15 - implementation report and independent review packet

Implemented:

- Added implementation report:
  - `docs/reports/impl/AST_PROJECT_VISUAL_WORKBENCH_WAVE2_IMPLEMENTATION_V1_20260716.md`
- Added independent review request:
  - `docs/reports/impl/AST_PROJECT_VISUAL_WORKBENCH_WAVE2_INDEPENDENT_REVIEW_REQUEST_V1_20260716.md`
- Updated `docs/reports/impl/INDEX.md` with the two Wave 2 packet entries.
- Updated the top of `docs/context/all/DEV_SUMMARY.md` with a bounded Wave 2 summary and explicit open scopes.

Independent review request explicitly requires:

- direct `운동 . 속도구하기` execution,
- string/comment alias negative controls,
- normal/whitespace CLI/WASM equality with no `domain_mismatch_reported` success,
- Workbench project import before/after canvas distinction,
- module value change observation/canvas signature change,
- state hash/view hash boundary review,
- missing/tampered lock direct attacks,
- save/reopen deterministic lineage reproduction.

Boundary notes:

- Report packet claims only bounded behavior backed by G0-G14 commits and PASS checks.
- External user success count remains `0`.
- No `docs/ssot/**` changes.

## G16 - final audit and closure report

START_HEAD / ancestry:

- Required ancestor `7d9724a` is present.
- Known blocker fix `5ba698b fix(seamgrim): preserve composed trajectory views` is present.
- Pre-final-audit HEAD: `fa8b183 docs(seamgrim): prepare ast project visual workbench review packet`.

Gate commit ledger:

- G0: `82939ab chore(ddn): reseal ast project wave2 baseline`
- G1: `f261de9 fix(ddn): normalize project alias access by token spans`
- G2: `f5eec2a test(ddn): harden module boundary diagnostics`
- G3: `51e6b86 feat(ddn): emit project execution preparation artifact`
- G4: `6ab665c test(ddn): harden project runtime parity controls`
- G5: `d3aabae feat(seamgrim): track local project run lifecycle`
- G6: `af38ec2 feat(ddn): expose deterministic project observation trace`
- G7: `11513c9 feat(seamgrim): bind workbench to multifile run evidence`
- G8: `1598690 feat(seamgrim): bind bogae canvas to project run results`
- G9: `1872741 chore(ddn): record project vertical verification`
- G10: `8671297 feat(seamgrim): preserve multifile project run lineage`
- G11: `62697f0 test(seamgrim): preserve multifile project exchange and recovery`
- G12: `24bfae5 test(seamgrim): verify multifile workbench viewport quality`
- G0-G9 reseal: `02202bb chore(ddn): reseal ast project wave2 g0 g9`
- G13: `af37b47 test(ddn): harden project linker and workbench boundaries`
- G14: `4a49ea1 test(seamgrim): close ast project visual workbench gate`
- G15: `fa8b183 docs(seamgrim): prepare ast project visual workbench review packet`

Final audit PASS:

- PASS: `python tests/run_ast_project_visual_workbench_gate_check.py`
- PASS: `python tests/run_ddn_project_workbench_boundary_matrix_check.py`
- PASS: `python tests/run_seamgrim_multifile_portable_roundtrip_check.py`
- PASS: `python tests/run_ddn_cli_wasm_sync_gate_check.py`
- PASS: `python tests/run_ci_sanity_gate.py --profile core_lang`
- PASS: `cargo check`
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS: `git diff --check` (exit 0; CRLF warnings only from existing unrelated dirty files)
- PASS: `git status --short -- docs/ssot` (no output)

Final audit conclusions:

- Normal and whitespace module access have identical product runtime results.
- String/comment alias negative controls are covered by `ast_project_visual_workbench_gate_v1` and `ddn_project_workbench_boundary_matrix_v1`.
- Project execution uses shared DDN runtime paths, not a project-only evaluator.
- CLI/WASM/shared runtime parity is equality-closed for the bounded project gates; `domain_mismatch_reported` is not counted as success.
- Frozen/strict lock missing, tamper, and unpinned dependency failures are fatal in boundary matrix evidence.
- Approved Workbench supports multi-file editing, file navigation, protected root/lock/vendor boundaries, diagnostics, execution, real project observation rows, and real Bogae rendering.
- Imported module value changes alter observation values and canvas signature/pixels.
- Save/reopen/export/import preview/cancel/clone/server restart recovery preserve deterministic lineage.
- Browser viewport evidence covers `1440x900`, `1024x768`, `778x912`, and `390x844`.
- Generated screenshots/evidence live under local `out/` paths and were not staged.
- External user success count: `0`.

Closure classification:

- `닫힘-동작`: bounded AST local project linker.
- `닫힘-동작`: bounded local gaji lock bridge.
- `닫힘-동작`: bounded project CLI/WASM shared runtime parity.
- `닫힘-동작`: approved Workbench multi-file visual execution.
- `닫힘-동작`: representative physics/grid project verticals.
- OPEN: full DDN module system.
- OPEN: whole gaji ecosystem and public registry.
- OPEN: Git/remote resolver.
- OPEN: full Korean Manim.
- OPEN: IDC/cloud/login/team workflows.
- OPEN: external user validation.

Boundary notes:

- No new DDN grammar.
- No core runtime `state_hash` formula change.
- No `docs/ssot/**` changes.
- Sanity-generated `pack/open_bundle_artifact/run_bundle/geoul.diag.jsonl` and `pack/open_end_to_end/open.log.jsonl` were restored before staging.
