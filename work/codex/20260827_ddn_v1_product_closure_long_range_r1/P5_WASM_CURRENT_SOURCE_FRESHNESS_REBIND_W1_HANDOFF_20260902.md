# P5 tracked-WASM current-source freshness rebind W1 handoff

## Scope and lineage

- Persistent goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1`
- Internal authority read-only: v25.50.0 / RD-001~551
- Public Language SPEC read-only: v0.6.0
- Product baseline: `fa89a871ee503d5c1f6c89500baf81630f6f7e98`
- Product fixed: `258f5ebb65a73a4ec16d47e492159dcf8ac852fd`
- Fixed tree: `23b50fdef799b59a45b726788d798ed5275a1e7c`
- Direct parent: `fa89a871ee503d5c1f6c89500baf81630f6f7e98`; merge count 0.

## User-visible product correction

The tracked web WASM binary and its freshness manifest had drifted from the
current product source. The existing VC11 tracked-WASM parity runner therefore
failed closed before execution with source-file-count/source-tree/source-file
freshness mismatches.

The existing `scripts/build_wasm_tool.ps1` release/web builder and existing
`tests/run_ddn_cli_wasm_freshness_check.py --write-manifest` regeneration path
were used. No source semantics, JS semantic reconstruction, visible UI source,
SSOT, public SPEC, dependency, command membership, or release policy changed.

The fixed commit contains exactly these tracked artifact paths:

1. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
2. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

## Evidence

- Before regeneration: `tests/run_v1_core_control_flow_wasm_parity_w1.mjs`
  failed closed at tracked WASM freshness (`source_file_count`,
  `source_tree_sha256`, and `source_files` mismatch).
- After regeneration: `tests/run_ddn_cli_wasm_freshness_check.py`: PASS.
- After regeneration: `tests/run_v1_core_control_flow_wasm_parity_w1.mjs`:
  `cases=10`, native/WASM exact `10`, deterministic repeats `3`, partial
  publish `0`, freshness PASS.
- Product fixed working-tree artifact identities before Git normalization:
  - WASM: 5,580,088 bytes,
    SHA-256 `C95A52344482E6DDAA672FB00AA4F8035AF6D5844A1604354B317FCFFDAA1EE9`
  - manifest: 30,299 bytes,
    SHA-256 `A2FE211E092E07700235C76DECFB26183F76EFA20CE669C87FFA1A9E1D5E74C5`

## Scope and nonclaims

This is `P5_WASM_CURRENT_SOURCE_FRESHNESS_IMPLEMENTED_UNDER_REVIEW` only. It
does not close VC11, P5, P1, V1, public command membership, teul-cli physical
retirement, release, activation, legal/right attribution, or Owner Human Smoke.
No independent reviewer was created or dispatched by this change.
