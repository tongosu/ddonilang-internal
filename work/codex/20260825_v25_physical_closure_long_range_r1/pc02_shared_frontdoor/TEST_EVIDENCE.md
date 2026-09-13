# V25 PC-02 Test Evidence

## Core evidence

```text
cargo test -p ddonirang-tool --test v25_pc02_shared_frontdoor_pack
PASS 1/1

node tests/ddn_v25_pc02_shared_frontdoor_runner.mjs
V25_PC02_SHARED_FRONTDOOR_PACK_PASS cases=7 surfaces=tool,official-cli,teul,wasm,workbench

node tests/ddn_v25_pc02_shared_frontdoor_mutation_runner.mjs
M1 RED; M2 RED; M3 RED; M4 RED; M5 RED; restored GREEN; residue=0

cargo check --workspace
PASS
```

## Regression evidence

- PC-01 language pack: 3/3 PASS.
- PC-01 explicit runtime: 1/1 PASS, Definition then Rebinding remains distinct.
- PC-01 mutation: 3 RED, restored GREEN, residue 0.
- T1 RuntimeBridge, T2 HostBridge, T4 SourceAnalysis, and T4h authoritative repair: PASS.
- T5B console/graph, T5C space2d, T5D table/text/structure, T5E console-grid/grid2d: PASS.
- T5F four-family canonical product path: 4/4 PASS through explicit pre-V25 WASM migration entry; mutation 5/5 RED detected.
- Actual Workbench browser smoke: cached local Chromium, temporary port 38931, readiness `ready`, network install 0; unrelated favicon 404 only.
- `git diff --check`: PASS.

## WASM custody

```text
SOURCE_BUILT_WASM_SHA256: db941a629d141b0e322aaa3ed4af36d09cdfba4c9ca4c6c68eae19d8f0adb1e4
SOURCE_BUILT_WASM_BYTES: 12913811
TRACKED_WASM_SHA256: 22df2f73b2f720871deb34dfe2e2763c5e1ea44cf1bae63bdf8a41a2c9468399
TRACKED_WASM_BYTES: 3979001
TRACKED_MANIFEST_SOURCE_TREE_SHA256: 2cc7b9682ca4a2554878046ab45312154366100b23830d28e5336509d94f6eea
CURRENT_SOURCE_TREE_SHA256: 68a370d2d8a933aa08d06c851267813f537a287edab0ddc5475cfd860c9e4dfc
SOURCE_FILE_COUNT: 79
FRESHNESS: TRACKED_WASM_STALE
```

Source-built JS and type bindings contain the V25 inspection export and the
explicit pre-V25 constructor. Tracked bindings contain neither. Tracked WASM
and manifest diff from baseline is zero.

## Environment-limited checks

The isolated sparse worktree omits protected `docs/ssot/**`. Full teul test
compilation therefore stops at a historical `include_str!` lesson path; the
teul product binary and PC-02 surface compile and pass. Repository-wide rustfmt
also reports baseline formatting debt. Targeted rustfmt for new PC-02 Rust files
and `wasm_api.rs` passes, and no broad formatter write was performed.
