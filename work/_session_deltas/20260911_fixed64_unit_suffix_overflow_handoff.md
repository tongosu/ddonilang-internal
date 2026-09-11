# Fixed64 unit-suffix overflow handoff — 2026-09-11

## Immutable product target

- Product: `4c5fceb984af83bec80a457b3f928b56eab24cab`
- Tree: `26238ce17d6f43b4bdc720cc70300c83ffef72e0`
- Parent: `9d88b2758636236991b4235ec8be176094130f74`
- Product paths: `core/src/units.rs`, `tool/src/ddn_runtime.rs`,
  `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`, and
  `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`.

## Claim

The current V25 typed unit-suffix path now routes source values through
checked Q31.32 conversion before a unit result or resource patch can be
published. `2147483647@C == 0@K` now returns the existing typed
`E_RUNTIME_ARITH_OVERFLOW` rather than silently saturating and succeeding.
Checked conversion is also used before a unit-tagged resource patch is queued.

## Evidence

- Baseline RED: the source-level unit-suffix test observed a successful update
  for the overflowing Celsius literal.
- Fixed focused gate `fixed64_unit_suffix_overflow_rejects_before_publication`: PASS.
- Core temperature conversion regression: PASS.
- `cargo test -p ddonirang-core --lib --offline`: 138 passed.
- `cargo test -p ddonirang-tool --lib --offline`: 671 passed; the same five
  inherited isolated-worktree failures remain (two absent-SSOT `ai_prompt`,
  numeric-calculus ULP, BOM/project parsing, profile canon).
- `cargo check -p ddonirang-tool --offline`: PASS.
- Official WASM build, then existing freshness manifest write/check: PASS.
- `git diff --check`: PASS before the product commit.

## Mutation evidence

Fixed source blobs: core `b9c2a8f6584097bdc13d51aafd6388197a6260d2`, SHA-256
`650484575C3F728B2119BC25B1789ED5EE641C186B8C1EA1032622BE096487EB`; tool
`8091567ad70fc3f6b57386213c8e5ee7ff3a25e8`, SHA-256
`99F4C59F3B46689AD500B9571A1FB78DFC558E10289B3E57D58131E17193F6D2`.

1. Replacing the shared suffix call with infallible `from_spec` made the
   overflowing source succeed: focused RED. Exact restore: GREEN.
2. Replacing Celsius checked addition with saturating operator addition made
   the same source succeed: focused RED. Exact restore: GREEN.

The rematerialized WASM blob is `f5c49ae1efd299e393f7e2f5da876e1f2d153f0c`
with SHA-256 `A793258DC3B0B32D602A40226DB72AE194653263FC062977A0B6AB373C693573`.
The manifest blob is `c91d0ca077612fefd9a0b302b8be5752f8b5531c`, SHA-256
`67259CC92339F606D539BFDE9266DCC2AE8E0DAF8B8F0CC32ECEEDFD8B78F360`.

## Review request and nonclaims

Review this target for current V25 unit-suffix admission, pre-patch failure
atomicity, checked temperature conversion, and tracked-WASM freshness. It does
not claim every historical infallible unit helper, all unit arithmetic, V1
readiness, release, or Human PASS.
