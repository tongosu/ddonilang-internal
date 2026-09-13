# Fixed64 unit-division overflow handoff — 2026-09-11

## Immutable product target

- Product: `1f6934641a62d09008f83b4e91a28b5c7b810cba`
- Tree: `d0e0ce19b8ea815184dbf4863acdc4d5f5a02d21`
- Parent: `ea9581e915eb1ddd36a70fe3098b364786a8d918`
- Product paths: `core/src/units.rs`, `tool/src/ddn_runtime.rs`,
  `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`, and
  `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`.

## Claim

Current V25 unit-valued infix division now preserves a checked Fixed64 overflow
as `E_RUNTIME_ARITH_OVERFLOW`; it is no longer mislabeled as division by zero.
The nonzero raw-one-ULP divisor rejects before a success result returns. The
same shared core/runtime source was rematerialized into tracked web WASM.

## Evidence

- Core focused gate `unit_division_preserves_overflow_instead_of_misclassifying_it_as_zero_division`: PASS.
- Runtime focused gate `fixed64_infix_division_overflow_is_not_misreported_as_zero_division`: PASS.
- `cargo test -p ddonirang-core --lib --offline`: 138 passed.
- `cargo test -p ddonirang-tool --lib --offline`: 670 passed; five inherited failures outside this change: two absent-SSOT `ai_prompt`, numeric-calculus ULP, BOM/project parsing, and profile canon.
- `cargo check -p ddonirang-tool --offline`: PASS.
- Official WASM build then freshness manifest write and check: PASS.
- `git diff --check`: PASS before product commit.

## Mutation evidence

Fixed source blobs: core `4af60b0e5947be0fb36f5411abdd8069be0e2c00`, SHA-256
`AAA34D2FF483C395587BB2E5531CB858E39008A920BCD677A8C2E34A94DBB4F7`; tool
`008f4e8d98e47293a4177174641fc32efa12805b`, SHA-256
`CAB464BE83D9E3F6E73A7DFFBC56EFC34E21966603EEDACC47B26CA2813B0B2D`.

1. Mapping overflow to `DivisionByZero` made the core assertion RED
   (`Err(DivisionByZero)` versus `Err(Overflow)`); exact restore was GREEN.
2. Mapping runtime overflow to `EvalError::DivisionByZero` let the update
   return success; the runtime assertion was RED. Exact restore was GREEN.

The rematerialized WASM blob is `72a450f01bf612ef49d3516a0ddfa63e2e75128a`
with SHA-256 `4A47D259E1F130C7075FCA5548E377F7ED109E310B8369B188CFAC53E79F55F8`.
The manifest blob is `f713ec472c11baa2db9b01d8bb404ac796c4eb87`, SHA-256
`144DFCEE4C36A8F39D3B9E4452455B8641630ABDC876153B4FE1BCA8D5F166A4`.

## Review request and nonclaims

Review only this product target for checked unit-division diagnostic
preservation, runtime fail-closed behavior, and tracked-WASM freshness. It
does not claim all unit-conversion boundaries, full tool-suite green, V1
readiness, release, or Human PASS.
