# W110 CLI input-action shared authority handoff

## Identity

- Live authority read-only: internal SSOT v25.49.0 / RD-001~543; public Language SPEC v0.6.0.
- Baseline handoff: `d0b9327648e427b9d47030edf4c3afcadd7524c2`.
- Product fixed: `73a1b6ab234f39d3a3a5c985529caedf53186e1d`.
- Fixed tree: `1617f349b49da26c350ce4e03d64c010a26e48f6`.
- Direct parent: `d0b9327648e427b9d47030edf4c3afcadd7524c2`; merge count 0.

## Product change

`input_action_key_aliases` is now the sole default keyboard-alias authority in
`tool::geoul_snapshot`.  Native `DdnRunner` and the retained private teul
runtime both consume it.  The supported aliases and public source spelling are
unchanged; this removes two duplicated semantic default tables rather than
promoting a teul command or choosing an executable/package name.

Changed product paths are exactly:

- `tool/src/geoul_snapshot.rs`
- `tool/src/ddn_runtime.rs`
- `tools/teul-cli/src/runtime/eval.rs`
- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

## Evidence

- Existing shared snapshot tests: 6/6 PASS.
- Existing native `std_input_map_closure_runtime_maps_explicit_and_default_keys`: 1/1 PASS.
- Existing retained teul runtime version of that workflow: 1/1 PASS.
- `cargo test -p ddonirang-tool --lib`: 615 PASS / 2 FAIL.  Both failures are
  the pre-existing `ai_prompt` tests whose isolated worktree lacks
  `docs/ssot`; no W110 path is implicated.
- Official WASM rebuild and manifest write followed by
  `tests/run_ddn_cli_wasm_freshness_check.py`: PASS.
- `git diff --check`: PASS.

## Risk mutation

The shared right-action canonical entry was changed from `ArrowRight` to
`ArrowLeft`.  The native focused workflow stayed GREEN because its user-facing
input accepts additional right aliases (`d` and `right`); it is therefore not
claimed as the mutation detector.  The existing retained teul workflow,
which supplies the canonical `ArrowRight` state, became RED (exit 1 at
`std_input_map_closure_runtime_maps_explicit_and_default_keys`).  The source
was restored byte-exactly to SHA-256
`ad370515acf73dbf788f74845815c3bd2b8f38ac49d1200d6d875600b32c973a`, then
the shared/native/teul focused workflows returned GREEN.  Residue 0.

## Product value and boundaries

This removes a private teul semantic duplicate from the V1-required keyboard
input workflow while preserving Native/WASM and retained teul consumption of
one typed authority.  It creates no dependency, pack, runner, checker,
meta-test, public command membership, binary/package naming, release claim or
physical teul retirement.  `geoul query/backtrace` remains separately frozen:
the shared runtime has no approved per-tick private-State inspection seam.

Independent review is not dispatched here; rolling-review consolidation and
the next coherent milestone policy remain in force.
