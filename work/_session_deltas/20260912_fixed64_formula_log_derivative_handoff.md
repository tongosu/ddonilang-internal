# Fixed64 formula log derivative handoff — 2026-09-12

## Target

- Product: `2d2ab5e831b1dba5ae1ee3939d1af879464bd19b`
- Tree: `72ab1ec794bc7f6f81b07070443b7f71c351c3d4`
- Parent: `c103617b6675b791b913031527cbcc9fb1a6fdad`
- Product paths:
  - `tool/src/ddn_runtime.rs`
  - `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

## Claim

The `log10` and `log2` derivative constants now use the shared checked,
ties-to-even Fixed64 host ingress. The derivative path propagates that typed
failure through `diff_formula_expr` before it can produce a formula result.

The checked values are `ln(10) = 9_889_527_671` raw Q31.32 and `ln(2) =
2_977_044_472` raw Q31.32. The source-built tracked WASM freshness manifest
is bound to the same source tree.

## Fixed restoration identity

- `tool/src/ddn_runtime.rs`
  - Git blob: `9ba40e4ff726d9a1a3f53eef45ffaaba53258521`
  - SHA-256: `d01515dea11811162aa77b77be9a63df8641e671362c8060131af97cec2b916f`
- Manifest Git blob: `dfff269fccc426536b76b3c2302eff140926ea1f`
- Tracked WASM SHA-256: `e9d8d601cf0c76455e2f86e6abfbb1d034f7dbb033e882a70cef0c30a60bcf20`
- Manifest SHA-256: `c684dd39d18c17de45be5cf04ce64bd2a8ced9047cf262827bc39b28f396a16e`

## Focused evidence

- `cargo test -p ddonirang-tool formula_derivative_log_constants_use_checked_host_fixed64_ingress --lib --offline` — PASS.
- `cargo test -p ddonirang-tool fixed64_ --lib --offline` — PASS (24 passed).
- Official source-built WASM build: `scripts/build_wasm_tool.ps1 -Profile release -Target web` with `CARGO_TARGET_DIR=I:\\home\\urihanl\\ddn\\codex\\build\\target-fixed64-units-r3` — PASS.
- `python tests/run_ddn_cli_wasm_freshness_check.py --write-manifest` — PASS.
- `python tests/run_ddn_cli_wasm_freshness_check.py` — PASS.
- `cargo check -p ddonirang-tool --offline --quiet` — PASS (warnings only).
- `git diff --check` before product fixed — PASS.

## Mutation evidence

1. Restored `Fixed64::from_f64_lossy` for both constants. The focused test was RED:
   `ln10` raw was `9_889_527_670`, not checked ties-to-even
   `9_889_527_671`. Restored the fixed source blob and reran GREEN.
2. Replaced the checked `ln10` result with `Fixed64::ZERO`. The focused test
   was RED (raw `0`, expected `9_889_527_671`). Restored the fixed source blob
   and reran GREEN.

## Broader regression classification

`cargo test -p ddonirang-tool --lib --offline` ran with 675 passing and four
failures outside this two-path change: two `ai_prompt` tests require the absent
`docs/ssot` directory in this isolated worktree; the pre-existing BOM parsing
test; and `runtime_surface::supported_profile_canon_is_explicit_and_preserves_legacy_default`.
No failure names or stack locations overlap this product change.

## Review request and nonclaims

Review the checked ingress replacement, Result propagation through the
derivative branch, focused raw-value assertions, and manifest source-tree
binding. This writer does not issue an independent verdict. This target makes
no SSOT, public SPEC, release, Human PASS, public ABI, or support claim.
