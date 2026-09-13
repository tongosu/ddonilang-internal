# Fixed64 public WASM raw ingress handoff

## Fixed target

- Product commit: `78b1bdbe1e64dfec1f85c6952fd773c4dc06b4c4`
- Parent: `1a137235df39e6ff55022932d7b4fa9828e92f4b`
- Claim: current public WASM frame-input setters use signed-high-i32 plus
  unsigned-low-u32 Q31.32 parts.  The former f64 void setters are absent from
  the generated current export.  Workbench forwards decimal text only to the
  WASM Fixed64 owner, receives the raw pair, then invokes the versioned raw
  setter.

## Validation

- Focused Rust raw-part boundary test: PASS.
- `cargo check -p ddonirang-tool --lib --target wasm32-unknown-unknown --features wasm --offline`: PASS.
- Official `scripts/build_wasm_tool.ps1` materialization: PASS.
- `python tests/run_ddn_cli_wasm_freshness_check.py`: PASS.
- `node tests/seamgrim_wasm_wrapper_runner.mjs`: PASS.
- `node tests/seamgrim_wasm_vm_runtime_runner.mjs`: PASS.
- `node tests/seamgrim_ui_common_runner.mjs`: PASS.
- `node tests/ddn_cli_wasm_post_wasm_shared_changes_runner.mjs`: PASS.
- `git diff --check`: PASS.

## Mutation evidence

- M1 Q31.32 low-word masking: the focused Rust test was RED at
  `Fixed64::MAX`; restore matched
  `tool/src/wasm_api.rs` SHA-256
  `B1D5F5BF071B858DD02CF380AE6FAD808F510CC35DFD022D59369E42712B0110`
  and blob `2305751a3e923510315bb439935050d3d81dff4f`, then GREEN.
- M2 removal of the wrapper JS-number guard: the wrapper runner was RED at
  `setParamParsed: JS number must not enter Fixed64 path`; restore matched
  `wasm_ddn_wrapper.js` SHA-256
  `D0EF97F4081F1DD2852059F076591E80518BAA5EB6C816C2442395D8104B721F`
  and blob `388f6009a963a7e958490880b07b4e316e6dd1de`, then GREEN.

## Nonclaim

The full host `cargo test -p ddonirang-tool --lib --features wasm` aborts in
an existing wasm-bindgen non-wasm32 test path after unrelated pre-existing
failures; it is not a PASS and is not used as closure evidence.  This product
target is ready for independent review, not self-issued PASS.
