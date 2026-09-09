# Codex Session Delta - DDN Local Project Graph/Gaji Bridge Wave 1

Date: 2026-07-15 KST

## Resume Seal

- User note: prerequisite blocker `5ba698b` was verified and committed.
- Current branch at resume: `codex/queue-20260706`
- Resume START_HEAD: `674da9a3167b7fb4a34521d51961b77520913751`
- `5ba698b` ancestor check from resume HEAD: PASS
- `12dbffc` ancestor check from resume HEAD: PASS
- `git status --short -- docs/ssot`: clean
- Existing dirty/untracked files remain other-work ownership and were not
  stashed, modified, staged, or committed.

## G0

Baseline:

- Branch: `codex/queue-20260706`
- START_HEAD: `12dbffc91bf8356b373b6c1a952591e0a6c02d16`
- `12dbffc` ancestor check: PASS
- `git status --short -- docs/ssot`: clean
- Pre-existing dirty/untracked status lines: 150
- Existing dirty/untracked files are treated as other-work ownership and were
  not stashed, modified, staged, or committed.

Read:

- `AGENTS.md`
- `AGENT_WORKFLOW.md`
- `SSOT_POLICY.md`
- `ARTIFACT_POLICY.md`
- `docs/context/all/DEV_SUMMARY.md`
- `docs/ssot/ssot/SSOT_INDEX_v24.14.1.md`
- `docs/ssot/ssot/SSOT_LANG_v24.14.1.md` MOD1/PROJECT1
- `docs/ssot/ssot/SSOT_TOOLCHAIN_v24.14.1.md` TC-MOD1
- `docs/ssot/ssot/SSOT_DECISIONS_v24.14.1.md` D20/D27
- `docs/context/briefs/BRIEF_SEAMGRIM_DDN_DETERMINISTIC_PROJECT_WORKBENCH_UI_V1_20260712.md`
- `docs/reports/impl/SEAMGRIM_PORTABLE_PROJECT_CONTENT_EXCHANGE_WAVE1_V1_20260715.md`

Findings:

- D20 marks `쓰임` / `드러냄` / `프로젝트 {}` as
  `confirmed_design_pending_impl`.
- Official `ddonirang-lang` AST has no module/project block surface yet.
- CLI-local parser has partial `쓰임`/`드러냄` AST and parser support.
- CLI-local runtime records import aliases but does not resolve a product
  project graph or exported symbol table.
- Current CLI policy root discovery still looks for `ddn.project.json`, not
  `뿌리.ddn` first.
- WASM currently exposes single-source parse/run APIs, not virtual project
  source.
- Portable exchange Wave 1 keeps `seamgrim.project_snapshot_artifact.v0`; this
  Wave must preserve that wrapper and carry multi-file data in a bounded
  `local_package_payload` candidate kind.

Baseline verification:

- PASS: `python tests/run_seamgrim_portable_project_artifact_check.py`
- PASS: `python tests/run_seamgrim_portable_project_workbench_check.py`
- PASS: `python tests/run_seamgrim_one_file_ddn_create_run_check.py`
- PASS: `python tests/run_ddn_cli_wasm_true_parity_equality_check.py`

G0 artifact:

- `pack/ddn_local_project_graph_v1/baseline.detjson`
- `tests/run_ddn_local_project_graph_check.py`

Next:

- G1: add shared Rust `VirtualProjectSource` and path/limit contract in product
  code, then expose identical normalized manifest bytes to CLI and WASM.

## G1

Implemented:

- Added shared product Rust `tool/src/local_project.rs` for bounded
  `VirtualProjectSource` normalization.
- Enforced G1 path and size contract in one place:
  - max files: 64
  - per-file UTF-8 bytes: 256 KiB
  - serialized artifact bytes: 2 MiB
  - relative NFC `/` paths
  - reject empty, `.`, `..`, backslash, drive/absolute/URL, control char,
    duplicate normalized path, and Windows case-fold collision.
- Added CLI adapter `teul-cli project-normalize` that calls
  `ddonirang_tool::local_project::normalize_virtual_project_source_json`.
- Added WASM export `wasm_normalize_project_source_json` that calls the same
  Rust function.
- Rebuilt `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool*` and refreshed
  `ddonirang_tool.manifest.detjson`.
- Added `ddn_local_project_cli_wasm_parity_v1` pack with G1 fixture and
  expected normalized manifest.
- Added `tests/run_ddn_local_project_cli_wasm_parity_check.py` and
  `tests/ddn_local_project_cli_wasm_parity_runner.mjs`.

Verification:

- PASS: `cargo check -p ddonirang-tool`
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS: `cargo test -p ddonirang-tool local_project -- --nocapture`
- PASS: `python tests/run_ddn_local_project_cli_wasm_parity_check.py`
- PASS: `python tests/run_pack_golden.py ddn_local_project_cli_wasm_parity_v1`
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS: scoped `git diff --check`
- PASS: `git status --short -- docs/ssot`

Non-claims:

- No project graph execution yet.
- No module linker or local gaji lock bridge yet.
- No `state_hash` formula change.

Next:

- G2: project root discovery with `--project`, upward `뿌리.ddn`,
  `ddn.project.json` fallback, and identical disk/in-memory root diagnostics.

## G2

Implemented:

- Added shared product root discovery in `tool/src/local_project.rs`.
- Added discovery constants for `뿌리.ddn`, `ddn.project.json`, and legacy
  non-current names.
- Added disk discovery order:
  1. explicit `--project`
  2. upward `뿌리.ddn`
  3. `ddn.project.json` fallback only after no current root is found
  4. missing-root diagnostic.
- Added virtual in-memory discovery request
  `ddn.project_root_discovery_request.v1` using the same Rust path logic.
- Added fatal diagnostics:
  - `E_LEGACY_PROJECT_ROOT_NAME`
  - `E_PROJECT_ROOT_AMBIGUOUS`
  - `E_PROJECT_BLOCK_VS_PROJECTJSON_CONFLICT`
  - `E_PROJECT_ROOT_MISSING`
  - `E_PROJECT_SYMLINK_ESCAPE`
- Added a narrow root-vs-`ddn.project.json` entry conflict check for G2 fixture
  coverage; full `프로젝트 {}` parsing remains G3 scope.
- Added CLI adapter `teul-cli project-discover`.
- Added WASM export `wasm_discover_project_root_json`.
- Extended `ddn_local_project_graph_v1` with the required G2 fixture IDs:
  - `project_root_discovery_v1`
  - `project_projectjson_fallback_v1`
  - `project_root_conflict_fail_v1`
  - `project_root_ambiguous_fail_v1`
  - `project_block_vs_projectjson_conflict_v1`

Verification:

- PASS: `python tests/run_ddn_local_project_graph_check.py`
- PASS: `python tests/run_pack_golden.py ddn_local_project_graph_v1`
- PASS: `cargo test -p ddonirang-tool local_project -- --nocapture`
- PASS: `python tests/run_ddn_local_project_cli_wasm_parity_check.py`
- PASS: `cargo check -p ddonirang-tool`
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS: `git status --short -- docs/ssot`

Non-claims:

- No full `프로젝트 {}` parser/canon/graph yet.
- No project run frontdoor yet.
- No `state_hash` formula change.

Next:

- G3: parse/canon/graph for bounded `프로젝트 {}` at root only, with target
  path validation and graph hash equality across lang/tool/CLI/WASM frontdoors.

## G3

Implemented:

- Added bounded product parser for root-only `프로젝트 {}` in
  `tool/src/local_project.rs`.
- Parsed and canonicalized the Wave 1 subset:
  - `이름`
  - `첫글`
  - `목표 { 앱: ... }`
  - `모듈길`
  - `가지`
- Validated project paths against the shared G1 path contract.
- Rejected `프로젝트 {}` outside the root file with
  `E_PROJECT_BLOCK_OUTSIDE_ROOT`.
- Preserved `ddn.project.json` as toolchain metadata and added conflict
  detection against root `첫글`.
- Produced `ddn.local_project_graph.v1` with sorted files and deterministic
  `project_graph_sha256`.
- Added CLI adapter `teul-cli project-graph`.
- Added WASM export `wasm_project_graph_json`.
- Extended `ddn_local_project_graph_v1` with project graph success and
  outside-root negative cases.

Verification:

- PASS: `python tests/run_ddn_local_project_graph_check.py`
- PASS: `python tests/run_pack_golden.py ddn_local_project_graph_v1`
- PASS: `cargo test -p ddonirang-tool local_project -- --nocapture`
- PASS: `python tests/run_ddn_local_project_cli_wasm_parity_check.py`
- PASS: `cargo check -p ddonirang-tool`
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS: `git status --short -- docs/ssot`

Non-claims:

- The parser is bounded to Wave 1 project graph metadata, not a full DDN module
  language implementation.
- No import/export symbol linker yet.
- No project execution frontdoor yet.
- No `state_hash` formula change.

Next:

- G4: connect `쓰임`/`드러냄` to a real symbol boundary for direct local
  calculation import/export and alias-qualified lookup.

## G4

Implemented:

- Added product `ddn.local_project_symbol_boundary.v1` artifact in
  `tool/src/local_project.rs`.
- Parsed canonical `쓰임 { alias: "./path". }` from the entry file.
- Parsed canonical `드러냄 { name. }` and `드러냄 { external: internal. }`
  from imported local modules.
- Resolved project-root-relative local module paths and `.ddn` extension.
- Enforced private-by-default by failing alias-qualified access to non-exported
  symbols with `E_SYMBOL_NOT_EXPORTED`.
- Evaluated the bounded Wave 1 scalar symbol subset (`name := 7.` and string
  values) and produced `output_rows`.
- Added CLI adapter `teul-cli project-symbols`.
- Added WASM export `wasm_project_symbols_json`.
- Extended `ddn_local_project_graph_v1` with `project_symbols_v1` success and
  `project_symbol_private_v1` negative cases.

Verification:

- PASS: `python tests/run_ddn_local_project_graph_check.py`
- PASS: `python tests/run_pack_golden.py ddn_local_project_graph_v1`
- PASS: `cargo test -p ddonirang-tool local_project -- --nocapture`
- PASS: `python tests/run_ddn_local_project_cli_wasm_parity_check.py`
- PASS: `cargo check -p ddonirang-tool`
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS: `git status --short -- docs/ssot`

Non-claims:

- Symbol evaluation is a bounded direct local scalar subset, not the full module
  runtime.
- No re-export/cycle/topological traversal yet.
- No mutable module state or imported module top-level side effects.
- No `state_hash` formula change.

Next:

- G5: deterministic local module graph traversal, one re-export, cycle and
  duplicate diagnostics, and top-level effect boundary.

## G5

Implemented:

- Extended `ddn.local_project_symbol_boundary.v1` with deterministic
  `module_graph_order` and `module_graph_sha256`.
- Added recursive local module graph traversal for the Wave 1 project subset.
- Resolved re-exported symbols such as
  `드러냄 { 속도구하기: 운동.속도구하기. }`.
- Kept direct scalar evaluation bounded to product code; no test-only lowering
  was used.
- Rejected import/re-export cycles with `E_IMPORT_CYCLE`.
- Rejected imported modules that contain top-level `보여주기` effects with
  `E_IMPORTED_TOP_LEVEL_EFFECT_UNSUPPORTED`.
- Added deterministic shuffle fixture coverage for file order independence.
- Rebuilt the WASM tool artifact and refreshed the freshness manifest.

Verification:

- PASS: `python tests/run_ddn_local_project_graph_check.py`
- PASS: `python tests/run_pack_golden.py ddn_local_project_graph_v1`
- PASS: `cargo test -p ddonirang-tool local_project -- --nocapture`
- PASS: `python tests/run_ddn_local_project_cli_wasm_parity_check.py`
- PASS: `cargo check -p ddonirang-tool`
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS: scoped `git diff --check`
- PASS: `git status --short -- docs/ssot`

Non-claims:

- No local gaji lock bridge yet.
- No project run frontdoor yet.
- No `state_hash` formula change.

Next:

- G6: add a local-only gaji bridge and deterministic lock artifact with frozen
  verification, exact pins, and tamper diagnostics.

## G6

Implemented:

- Added product local gaji lock artifact `ddn.local_gaji_lock.v1` in
  `tool/src/local_project.rs`.
- Added vendored local gaji discovery from `프로젝트 { 가지 { ... } }` paths.
- Enforced Wave 1 local path boundary: `vendor/<id>/gaji.toml`.
- Parsed bounded `gaji.toml` fields:
  - `id`
  - `version`
  - exact pinned dependencies via inline table or `[dependencies]`.
- Resolved direct and one-or-more transitive local dependencies without remote
  registry/index input.
- Added deterministic package pins with manifest/package hashes and
  `lock_sha256`.
- Excluded `ddn.lock` itself from lock graph input to avoid self-referential
  graph drift.
- Added frozen verification: a present `ddn.lock` must byte-match the generated
  canonical lock, and `--frozen` fails when `ddn.lock` is missing.
- Added stable diagnostics:
  - `E_LOCK_MISSING`
  - `E_LOCK_HASH_MISMATCH`
  - `E_GAJI_DEP_UNPINNED`
  - `E_GAJI_TRANSITIVE_MISSING`
  - `E_GAJI_ID_PATH_MISMATCH`
- Added CLI adapter `teul-cli project-lock [--frozen]`.
- Added WASM export `wasm_project_gaji_lock_json`.
- Extended `ddn_local_project_graph_v1` with G6 lock generation/frozen/negative
  fixtures and expected detjson.

Verification:

- PASS: `python tests/run_ddn_local_project_graph_check.py`
- PASS: `python tests/run_pack_golden.py ddn_local_project_graph_v1`
- PASS: `cargo test -p ddonirang-tool local_project -- --nocapture`
- PASS: `python tests/run_ddn_local_project_cli_wasm_parity_check.py`
- PASS: `cargo check -p ddonirang-tool`
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS: scoped `git diff --check`
- PASS: `git status --short -- docs/ssot`

Non-claims:

- No remote registry/index support in the local project success path.
- No full gaji package runtime execution yet.
- No project run frontdoor yet.
- No `state_hash` formula change.

Next:

- G7: add the CLI project frontdoor for explicit project/cwd discovery,
  graph/lock inspect evidence, and bounded multi-file run summary.

## G7

Implemented:

- Added bounded product run summary artifact
  `ddn.local_project_run_summary.v1`.
- Added disk project reader that discovers a physical root, reads project files
  into the shared `VirtualProjectSource`, infers existing file roles, and keeps
  host absolute paths out of the artifact.
- Added `teul-cli project-run` with:
  - explicit start path discovery
  - cwd discovery
  - `--project` explicit root option
  - `--target`
  - `--inspect-graph`
  - `--inspect-lock`
  - structured JSON diagnostics via existing `LocalProjectError` payloads.
- Kept the existing single-file `run` command untouched.
- Added physical multi-file fixture under
  `pack/ddn_local_project_graph_v1/project_frontdoor/project_run_v1`.
- The fixture proves:
  - local module import output `7`
  - vendored gaji DDN module output `10`
  - project graph hash
  - local lock hash
  - symbol boundary hash
  - explicit path and cwd discovery.

Verification:

- PASS: `python tests/run_ddn_local_project_graph_check.py`
- PASS: `python tests/run_pack_golden.py ddn_local_project_graph_v1`
- PASS: `cargo test -p ddonirang-tool local_project -- --nocapture`
- PASS: `python tests/run_ddn_local_project_cli_wasm_parity_check.py`
- PASS: `cargo check -p ddonirang-tool`
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS: scoped `git diff --check`
- PASS: `git status --short -- docs/ssot`

Non-claims:

- This is a bounded project run summary, not a full multi-module language
  runtime.
- No remote registry/index support.
- No WASM project-run parity yet.
- No workbench multi-file authoring yet.
- No `state_hash` formula change.

Next:

- G8: expose the same virtual project run summary to WASM and verify CLI/raw
  WASM equality including negative mismatch controls.

## G8

Implemented:

- Added `bounded_state_sha256` to `ddn.local_project_run_summary.v1`.
  - This is a run-summary equality hash over output rows only.
  - It is not the runtime `state_hash` and does not change the `state_hash`
    formula.
- Added CLI virtual project frontdoor:
  - `teul-cli project-run --virtual <source.json>`.
- Added WASM export:
  - `wasm_project_run_summary_json(source_json, target, inspect_graph,
    inspect_lock)`.
- Extended raw WASM runner `tests/ddn_local_project_graph_runner.mjs` with
  `run` mode.
- Added virtual physics fixture that matches the physical G7 fixture.
- Added virtual grid-game smoke fixture to prove the resolver is not
  physics-specific.
- Added negative mismatch controls in the checker:
  - physics and grid outputs must differ.
  - physics and grid `bounded_state_sha256` values must differ.
- Rebuilt the WASM tool artifact and refreshed freshness manifest.

Verification:

- PASS: `python tests/run_ddn_local_project_graph_check.py`
- PASS: `python tests/run_pack_golden.py ddn_local_project_graph_v1`
- PASS: `cargo test -p ddonirang-tool local_project -- --nocapture`
- PASS: `python tests/run_ddn_local_project_cli_wasm_parity_check.py`
- PASS: `cargo check -p ddonirang-tool`
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS: scoped `git diff --check`
- PASS: `git status --short -- docs/ssot`

Non-claims:

- No full runtime multi-module execution beyond the bounded run summary.
- No browser workbench authoring yet.
- No `state_hash` formula change.

Next:

- G9: add workbench multi-file authoring UI for file navigation,
  create/rename/delete/open, root/entry guards, read-only lock/vendor, and
  project run dependency status.

## G9

Implemented:

- Added a local project workbench panel to the Seamgrim editor world-code
  screen.
- Preserved the existing one-file textarea and run button path.
- Added virtual project file navigation and indicators:
  - current file
  - entry file
  - compact dependency/project-run status.
- Added in-memory project file operations:
  - enable project mode from the current DDN
  - create helper file
  - rename helper file
  - delete non-entry/non-readonly helper file
  - open files from the navigator.
- Added guards:
  - `뿌리.ddn` is read-only.
  - `ddn.lock` is read-only.
  - `vendor/**` is read-only.
  - entry file cannot be renamed or deleted.
- Connected product UI project run to the G8 WASM export
  `wasm_project_run_summary_json`.
- Exposed the initialized WASM module on the existing VM client as an
  additive loader property for module-level product exports.
- Added pack `ddn_local_project_workbench_multifile_v1` with the same virtual
  source tree exercised by the browser workflow.
- Added browser runner
  `tests/ddn_local_project_workbench_multifile_runner.mjs`.
- Added checker
  `tests/run_ddn_local_project_workbench_multifile_check.py`.

Browser workflow evidence:

- Starts from a single-file editor deep link.
- Verifies the one-file editor remains visible before project mode.
- Enables project mode.
- Verifies root/entry/current indicators.
- Opens root, lock, and vendor files and confirms read-only guard state.
- Confirms entry remains editable but cannot be renamed/deleted.
- Creates and deletes an extra helper file.
- Renames `lib/helper.ddn` to `lib/helper_renamed.ddn`.
- Edits `app/main.ddn` to import the renamed helper.
- Runs the project through the WASM product export and gets output `11`.
- Edits the helper value to `12`, reruns, and verifies the project graph hash
  changes.

Verification:

- PASS: `node tests/ddn_local_project_workbench_multifile_runner.mjs`
- PASS: `python tests/run_ddn_local_project_workbench_multifile_check.py`
- PASS: `python tests/run_pack_golden.py ddn_local_project_workbench_multifile_v1`
- PASS: `python tests/run_ddn_local_project_graph_check.py`
- PASS: `python tests/run_pack_golden.py ddn_local_project_graph_v1`
- PASS: `cargo test -p ddonirang-tool local_project -- --nocapture`
- PASS: `python tests/run_ddn_local_project_cli_wasm_parity_check.py`
- PASS: `cargo check -p ddonirang-tool`
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS: `python tests/run_ci_sanity_gate.py --profile core_lang`
- PASS: scoped `git diff --check`
- PASS: `git status --short -- docs/ssot`
- Restored sanity-generated open log changes:
  - `pack/open_bundle_artifact/run_bundle/geoul.diag.jsonl`
  - `pack/open_end_to_end/open.log.jsonl`

Non-claims:

- No real filesystem write/delete in the workbench UI.
- No public package publish/upload.
- No new DDN grammar.
- No full multi-module runtime claim beyond the bounded project summary.
- No `state_hash` formula change.

## G10

Implemented:

- Preserved the existing `seamgrim.project_snapshot_artifact.v0` wrapper.
- Added a bounded multi-file payload under
  `project_snapshot.local_package_payload` with:
  - `kind: seamgrim.local_project_tree.v0`
  - entry path
  - file rows with UTF-8 text, byte length, and SHA-256
  - WASM project run summary hashes
  - `state_hash_formula_change: false`.
- Kept one-file local package snapshot behavior as the fallback path.
- Routed editor save/reopen/restore/clone through a shared snapshot loader:
  - local project tree snapshots restore into the project workbench.
  - one-file snapshots still use the original `loadLesson` path.
- Updated workbench portable import to preserve project tree files instead of
  collapsing imported artifacts to `lesson.ddn`.
- Updated workbench preview to show entry path, file count, lock presence, and
  vendored gaji count for local project tree artifacts.
- Updated workbench server-save and portable-export paths to carry the current
  local project tree payload. Edited workbench file text updates the payload
  file text, byte length, and SHA-256.
- Added pack `seamgrim_multifile_portable_roundtrip_v1`.
- Added browser runner
  `tests/seamgrim_multifile_portable_roundtrip_runner.mjs`.
- Added checker
  `tests/run_seamgrim_multifile_portable_roundtrip_check.py`.

Browser workflow evidence:

- Starts from the Seamgrim editor and enables the multi-file local project
  workbench.
- Renames `lib/helper.ddn` to `lib/helper_renamed.ddn`.
- Edits `app/main.ddn` to import the renamed helper.
- Runs the project through the WASM virtual project frontdoor and verifies
  output `11`.
- Builds a product snapshot artifact and verifies the wrapper schema plus
  `seamgrim.local_project_tree.v0` payload.
- Saves to the local project server and reopens through the edit link with the
  multi-file tree intact.
- Opens the view link and creates an editable clone with the multi-file tree
  intact.
- Imports the same artifact into the approved workbench.
- Confirms import preview does not change the current project or auto-run.
- Confirms cancel preserves the current project.
- Opens the imported artifact and verifies entry/helper/lock/vendor files are
  visible.
- Saves the imported project to the server and reopens it with the multi-file
  tree intact.
- Verifies corrupt portable import is rejected without changing the current
  project/source.

Verification:

- PASS: `node tests/seamgrim_multifile_portable_roundtrip_runner.mjs`
- PASS: `python tests/run_seamgrim_multifile_portable_roundtrip_check.py`
- PASS: `python tests/run_pack_golden.py seamgrim_multifile_portable_roundtrip_v1`
- PASS: `python tests/run_ddn_local_project_workbench_multifile_check.py`
- PASS: `node tests/seamgrim_portable_project_workbench_runner.mjs`
- PASS: `git diff --check` scoped to G10 files
- PASS: `git status --short -- docs/ssot`

Notes:

- `python tests/run_seamgrim_portable_project_workbench_check.py` had one
  transient browser-close failure during parallel execution. The same browser
  runner was immediately rerun directly and passed.
- No `docs/ssot/**` changes.
- No new DDN grammar.
- No runtime `state_hash` formula change.

Next:

- G11: four viewport and representative vertical regression evidence for the
  bounded local project workflow.

## G11

Implemented:

- Added pack `seamgrim_multifile_project_workbench_v1`.
- Added browser runner
  `tests/seamgrim_multifile_project_workbench_runner.mjs`.
- Added checker
  `tests/run_seamgrim_multifile_project_workbench_check.py`.
- Added a workbench CSS hardening fix so long Korean file names in file tabs
  are width-bounded and ellipsized on mobile viewports.

Browser viewport evidence:

- PASS: `1440x900`
- PASS: `1024x768`
- PASS: `778x912`
- PASS: `390x844`

Each viewport checks:

- Seamgrim editor local project file navigator is usable.
- DDN editor can receive keyboard focus.
- WASM project run result is produced and dependency/graph status is visible.
- Approved workbench import preview fits without horizontal page overflow.
- Long Korean file name can be selected without page-level overflow.
- Import/export controls have accessible names/tooltips.
- Primary Bogae canvas is visible and pixel-nonblank.
- One-file public physics workbench source/canvas regression remains visible.

Representative vertical evidence:

- Multi-file physics project:
  - fixture: `pack/ddn_local_project_graph_v1/fixtures/project_run_physics_v1.json`
  - output rows: `["7", "10"]`
  - graph: `762b2ee7e1b210a6e31b865c86e8a57879ed4ccd5a66b3f27ae4d29152ce22e9`
- Multi-file grid-game smoke:
  - fixture: `pack/ddn_local_project_graph_v1/fixtures/project_run_grid_v1.json`
  - output rows: `["3"]`
  - graph: `0b3dc1da5807e5404d4a79b602eb35784d8ee7853aff283826898c835512f044`
- One-file public physics regression:
  - workbench default public physics source is visible.
  - primary canvas is pixel-nonblank before import.

Verification:

- PASS: `node tests/seamgrim_multifile_project_workbench_runner.mjs`
- PASS: `python tests/run_seamgrim_multifile_project_workbench_check.py`
- PASS: `python tests/run_pack_golden.py seamgrim_multifile_project_workbench_v1`
- PASS via G11 checker: `python tests/run_seamgrim_multifile_portable_roundtrip_check.py`
- PASS: `git status --short -- docs/ssot`

Non-claims:

- No Ganada matrix state upgrade.
- No public registry/Git resolver/remote download.
- No new DDN grammar.
- No runtime `state_hash` formula change.

Next:

- G12: integration orchestration, final verification, implementation report,
  and independent review packet.

## G12

Implemented:

- Added integration checker
  `tests/run_ddn_local_project_gaji_wave1_quality_gate_check.py`.
- Added final implementation report
  `docs/reports/impl/DDN_LOCAL_PROJECT_GRAPH_GAJI_BRIDGE_WAVE1_V1_20260715.md`.
- Updated `tests/toolchain_golden/ai_prompt_lean.txt` with the product command:
  `cargo run -p ddonirang-tool -- ai prompt --profile lean --out build\ai_prompt_lean_current.txt`.
  The prior golden was still `SSOT_VERSION = v24.12.9`; the current product
  prompt source resolves `SSOT_VERSION = v24.14.1`.
- Repaired `tests/seamgrim_wasm_cli_runtime_parity_runner.mjs` so currentline
  parity cases build `teul-cli` once into `build/teul_cli_runner_target` with
  `CARGO_INCREMENTAL=0`, then execute the product binary for each case. This
  preserves the product CLI frontdoor and removes the previous 38-case
  per-case `cargo run` timeout/cache-collision path.

G12 verification:

- PASS: `python tests/run_ddn_local_project_graph_check.py`
- PASS: `python tests/run_ddn_local_project_cli_wasm_parity_check.py`
- PASS: `python tests/run_ddn_local_project_workbench_multifile_check.py`
- PASS: `python tests/run_seamgrim_multifile_portable_roundtrip_check.py`
- PASS: `python tests/run_seamgrim_multifile_project_workbench_check.py`
- PASS: `python tests/run_ddn_local_project_gaji_wave1_quality_gate_check.py`
- PASS: `python tests/run_pack_golden.py ddn_local_project_graph_v1 ddn_local_project_cli_wasm_parity_v1 ddn_local_project_workbench_multifile_v1 seamgrim_multifile_portable_roundtrip_v1 seamgrim_multifile_project_workbench_v1`
- PASS: `cargo test -p ddonirang-tool`
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS: `python tests/run_ddn_cli_wasm_true_parity_equality_check.py`
- PASS: `python tests/run_ddn_cli_wasm_sync_gate_check.py`
- PASS: `python tests/run_seamgrim_approved_workbench_promotion_packet_check.py`
- PASS: `python tests/run_seamgrim_workbench_durable_quality_gate_check.py`
- PASS: `python tests/run_seamgrim_public_physics_wedge_quality_gate_check.py`
- PASS: `python tests/run_seamgrim_portable_project_artifact_check.py`
- PASS: `python tests/run_seamgrim_portable_project_workbench_check.py`
- PASS: `python tests/run_seamgrim_view_only_state_hash_invariant_check.py`
- PASS: `cargo check`
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS: `python tests/run_ci_sanity_gate.py --profile core_lang`
- PASS: `git diff --check`
- PASS: `git status --short -- docs/ssot`

Notes:

- `python tests/run_ddn_cli_wasm_sync_gate_check.py` initially exposed a
  `vol4_parity_38` timeout/cache-collision path. After the runner repair, the
  standalone Vol4 parity checker and the full sync gate both passed.
- `pack/open_bundle_artifact/run_bundle/geoul.diag.jsonl` and
  `pack/open_end_to_end/open.log.jsonl` were modified by sanity-gate execution
  and restored to their pre-test tracked state before staging.
- Existing unrelated dirty/untracked files remain outside this batch and were
  not staged.
- `docs/ssot/**` remained clean.

Final non-claims:

- No public registry, Git resolver, remote download, account, cloud, or IDC.
- No new DDN grammar.
- No runtime `state_hash` formula change.
- No full module ecosystem or all-gaji compatibility claim.
- External user success count: `0`.

## Post-blocker resume: G0-G9 runtime-semantics repair

START_HEAD sealed:

- `7d2d000e41ffa308891773806bb6464095785e69`
- Branch: `codex/queue-20260706`
- Predecessor blocker reference: `5ba698b` was already committed before this
  resume.

Implemented:

- Replaced local-project fake execution summaries with the product runtime
  path. Project entry now builds a linked execution source and calls
  `runtime_surface::run_summary_from_source`; exported symbol values and
  `output_rows` are derived from runtime `final_row`, not from string-parsed
  `:=` definitions.
- Removed `parse_simple_definitions` from `tool/src/local_project.rs`.
  Alias-qualified `보여줘` discovery remains only as a frontdoor rewrite target
  selector; it no longer computes execution values.
- Added linked execution evidence to project-run summaries:
  `runtime_output_log_texts`, `runtime_final_row`, `runtime_state_hash`,
  `runtime_execution_envelope`, `linked_execution_source`,
  `linked_execution_canonical_ddn`, `linked_execution_source_sha256`, and
  `linked_execution_canonical_sha256`.
- Made strict/frozen `ddn.lock` fatal for gaji-backed project-run success
  paths. The physical project fixture now includes `ddn.lock`; missing/tamper
  cases remain negative evidence.
- Rebuilt the Seamgrim WASM bundle and refreshed the WASM freshness manifest
  after the runtime-surface changes.
- Updated the product workbench seed fixtures from unsupported `:=` examples to
  current product `<-` assignment surface.
- Added a fake-summary negative control: a temporary project with
  `값 := 99.` must fail through both CLI/WASM project-run paths with
  parser/runtime diagnostics, proving the old string-summary route cannot pass.
- Moved the CLI binary build cache used by the WASM/CLI parity runner to the
  external artifact-policy build root (`I:/home/urihanl/ddn/codex/build`, with
  `C:/ddn/codex/build` fallback) instead of repo-local `build/`.

Verification:

- PASS: `cargo check -p ddonirang-tool`
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS: `cargo check`
- PASS: `python tests/run_ddn_local_project_graph_check.py`
- PASS: `python tests/run_pack_golden.py ddn_local_project_graph_v1`
- PASS: `python tests/run_pack_golden.py ddn_local_project_workbench_multifile_v1`
- PASS: `node tests/ddn_local_project_workbench_multifile_runner.mjs`
- PASS: `python tests/run_ddn_local_project_workbench_multifile_check.py`
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS: `python tests/run_seamgrim_multifile_project_workbench_check.py`
- PASS: `python tests/run_ddn_local_project_gaji_wave1_quality_gate_check.py`
- PASS: `python tests/run_ci_sanity_gate.py --profile core_lang`
- PASS: `git diff --check`
- PASS: `git status --short -- docs/ssot`

Boundary notes:

- Official `teul-cli run --summary-json` is now used as a comparison control for
  linked source output/effective ticks/canonical generation. Output rows match
  the project-run runtime output.
- Full `state_hash` equality is not claimed in this batch. Project-run uses the
  shared `DdnRunner`/platform runtime state hash, while the current official
  `teul-cli run` summary path still reports the legacy CLI detbin hash. Changing
  that formula is outside this batch and explicitly forbidden.
- Full canonical hash equality is also not claimed: the shared canonicalizer and
  the official CLI canonical summary path still differ on this linked source.
  The checker records nonempty canonical evidence without changing canonical
  semantics.
- No `docs/ssot/**` file was modified.

## Post-blocker resume: official `teul-cli run` shared-runtime parity

Implemented:

- Added a `shared_runtime` block to `teul-cli run --summary-json`. The existing
  legacy evaluator output and top-level legacy `state_hash` remain unchanged,
  but the summary now also records the shared product runtime result from
  `ddonirang_tool::runtime_surface::run_summary_from_source`.
- The `shared_runtime` block records `state_hash`, `view_hash`,
  `output_log_texts`, `final_row`, `execution_envelope`, `canonical_ddn`,
  `preprocessed_source`, and `parity_surface`. If a legacy-only source cannot
  run through the shared runtime, the summary keeps the legacy run result and
  records an `E_SHARED_RUNTIME_SUMMARY` diagnostic instead of hiding the
  mismatch.
- Strengthened `tests/run_ddn_local_project_graph_check.py` so the official
  `teul-cli run --summary-json` control must prove:
  - `shared_runtime.ok == true`
  - `shared_runtime.output_log_texts == project-run.output_rows`
  - `shared_runtime.state_hash == project-run.runtime_state_hash`
  - `shared_runtime.execution_envelope == project-run.runtime_execution_envelope`
  - `shared_runtime.canonical_ddn == project-run.linked_execution_canonical_ddn`
- Fixed the checker temp-file write path to preserve linked-source bytes with
  `write_bytes`; otherwise Windows text-mode newline translation changed only
  `source_bytes_sha256`/`preprocessed_source_sha256` while canonical/output/hash
  already matched.

Verification:

- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS: `cargo test --manifest-path tools/teul-cli/Cargo.toml run_summary_json -- --nocapture`
- PASS: `cargo check`
- PASS: `python tests/run_ddn_local_project_graph_check.py`
- PASS: `python tests/run_pack_golden.py ddn_local_project_graph_v1`
- PASS: `python tests/run_pack_golden.py ddn_local_project_workbench_multifile_v1`
- PASS: `node tests/ddn_local_project_workbench_multifile_runner.mjs`
- PASS: `python tests/run_ddn_local_project_workbench_multifile_check.py`
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS: `python tests/run_seamgrim_multifile_project_workbench_check.py`
- PASS: `python tests/run_ddn_local_project_gaji_wave1_quality_gate_check.py`

Boundary notes:

- The top-level `teul-cli run` legacy `state_hash` is still preserved for legacy
  compatibility. The equality claim for this goal is specifically the
  `shared_runtime` state hash/envelope/output emitted by the official
  `teul-cli run --summary-json` product frontdoor and compared against
  project-run/WASM project-run evidence.
- No runtime `state_hash` formula change.
- No `docs/ssot/**` file was modified.

## Post-blocker resume: AST alias-show extraction

Implemented:

- Removed the remaining `parse_alias_show_requests` string scanner from
  `tool/src/local_project.rs`.
- Alias-qualified `보여주기` rewrite targets are now discovered by:
  1. stripping local-project metadata blocks with the existing product metadata
     stripper,
  2. preparing the remaining DDN through `runtime_surface::prepare_source_for_execution`,
  3. parsing the prepared source with `ddonirang_lang::parse_with_mode`, and
  4. traversing `Stmt::Show` / `ExprKind::FieldAccess` in the AST.
- This keeps alias-target discovery on the parser/AST path and leaves value
  computation entirely to `DdnRunner`.
- Rebuilt the Seamgrim WASM bundle and refreshed
  `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson` because
  `tool/src/local_project.rs` changed.

Verification:

- PASS: `cargo check -p ddonirang-tool`
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS: `python tests/run_ddn_local_project_graph_check.py`
- PASS: `python tests/run_pack_golden.py ddn_local_project_graph_v1`
- PASS: `python tests/run_pack_golden.py ddn_local_project_workbench_multifile_v1`
- PASS: `node tests/ddn_local_project_workbench_multifile_runner.mjs`
- PASS: `python tests/run_ddn_local_project_workbench_multifile_check.py`
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS: `python tests/run_seamgrim_multifile_project_workbench_check.py`

Boundary notes:

- `parse_simple_definitions` and `parse_alias_show_requests` have zero
  remaining references in `tool/src/local_project.rs`.
- No new DDN grammar.
- No runtime `state_hash` formula change.
- No `docs/ssot/**` file was modified.

## Final completion audit for active goal

Latest resume seal:

- User instruction: predecessor blocker `5ba698b` was verified and committed;
  seal the current HEAD as the new START_HEAD and resume G0-G9.
- New START_HEAD: `7db0f8f68710d36b6d419bf7934716eeb8c830d3`
  (`fix(ddn): derive project show rewrites from AST`).
- Branch: `codex/queue-20260706`.
- `5ba698b` ancestor check from latest START_HEAD: PASS.
- Scope: no reset/revert; preserve all committed G0-G9 work and rerun the
  product gates from the latest HEAD. The only uncommitted related file before
  this audit was this session delta.

Latest G0-G9 verification rerun:

- PASS: `python tests/run_ddn_local_project_graph_check.py`
- PASS: `python tests/run_ddn_local_project_cli_wasm_parity_check.py`
- PASS: `python tests/run_pack_golden.py ddn_local_project_graph_v1 ddn_local_project_cli_wasm_parity_v1 ddn_local_project_workbench_multifile_v1 seamgrim_multifile_project_workbench_v1`
- PASS: `python tests/run_ddn_local_project_workbench_multifile_check.py`
- PASS: `node tests/ddn_local_project_workbench_multifile_runner.mjs`
- PASS: `python tests/run_seamgrim_multifile_project_workbench_check.py`
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS: `cargo check -p ddonirang-tool`
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS: `cargo test --manifest-path tools/teul-cli/Cargo.toml run_summary_json -- --nocapture`
- PASS: `cargo check`
- PASS: `python tests/run_ci_sanity_gate.py --profile core_lang`
- PASS: `git diff --check`
- PASS: `git status --short -- docs/ssot`
- Restored sanity-gate open log byproducts:
  `pack/open_bundle_artifact/run_bundle/geoul.diag.jsonl` and
  `pack/open_end_to_end/open.log.jsonl`.

Requirement evidence:

- No string execution semantics: `parse_simple_definitions` and
  `parse_alias_show_requests` have zero remaining references in
  `tool/src/local_project.rs`.
- Parser/AST path: alias-qualified `보여주기` rewrite targets are discovered by
  parsing stripped entry DDN with `ddonirang_lang::parse_with_mode` and walking
  `Stmt::Show` / `ExprKind::FieldAccess`.
- Product runtime path: `project-run` and WASM `wasm_project_run_summary_json`
  both use `runtime_surface::run_summary_from_source` on the linked execution
  source.
- Official `teul-cli run` comparison: `teul-cli run --summary-json` emits a
  `shared_runtime` block, and `tests/run_ddn_local_project_graph_check.py`
  requires its output, state hash, execution envelope, and canonical DDN to
  match the project-run summary.
- Strict/frozen lock: missing/tampered `ddn.lock` cases remain fatal through
  `E_LOCK_MISSING` / `E_LOCK_HASH_MISMATCH`.
- Negative control: `값 := 99.` fake-summary project fails through both
  CLI and WASM project-run paths with parser/runtime diagnostics.
- Artifact policy: `tests/seamgrim_wasm_cli_runtime_parity_runner.mjs` builds
  `teul-cli` into the external artifact build root rather than repo-local
  `build/teul_cli_runner_target`.

Final verification:

- PASS: `python tests/run_ddn_local_project_graph_check.py`
- PASS: `python tests/run_pack_golden.py ddn_local_project_graph_v1`
- PASS: `python tests/run_pack_golden.py ddn_local_project_workbench_multifile_v1`
- PASS: `node tests/ddn_local_project_workbench_multifile_runner.mjs`
- PASS: `python tests/run_ddn_local_project_workbench_multifile_check.py`
- PASS: `python tests/run_seamgrim_multifile_project_workbench_check.py`
- PASS: `python tests/run_seamgrim_multifile_portable_roundtrip_check.py`
- PASS: `python tests/run_seamgrim_one_file_ddn_create_run_check.py`
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS: `cargo check -p ddonirang-tool`
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS: `cargo test --manifest-path tools/teul-cli/Cargo.toml run_summary_json -- --nocapture`
- PASS: `cargo check`
- PASS: `python tests/run_ci_sanity_gate.py --profile core_lang`
- PASS: `git diff --check`
- PASS: `git status --short -- docs/ssot`

Final non-claims:

- No new DDN grammar.
- No runtime `state_hash` formula change.
- No public registry/Git resolver/remote download.
- No unrelated dirty/untracked files staged.
