# RD-457 module-directive final handoff

## Fixed lineage

- Product implementation: `48d3aa34d4ceb06e8990495870c4151e0a5f5781`
- P5 UTF-8-span correction: `173160424364f091e2a3bccf513895c4c84aa130`
- Product implementation parent: `b8a54e74efe4bafd88ea569d3663b0b039669b20`
- Correction scope: `lang/tests/rd457_module_directive_roundtrip.rs` only.

## P5 correction result

The UTF-8 assertion uses the existing registry target `./lib/😀` inside a string
literal. It does not admit emoji identifiers. The test proves that the first
directive byte slice is exact and that the following export span starts at the
actual UTF-8 byte offset. It also proves parse/canon/parse/canon byte stability
and LF canonical output.

`lang/src/module_directive.rs` remains blob
`2d2345106bbb47f5dbaa07690f4d85e2a24d5c31`; therefore the product-side M1,
M2, and M3 RED → exact restore → GREEN evidence remains applicable.

## Validation

- Focused RD-457 tests: PASS (3/3).
- `cargo test -p ddonirang-lang`: PASS.
- `cargo check -p ddonirang-lang --offline`: PASS.
- `git diff --check`: PASS.
- Product implementation, lexer, runtime, CLI, WASM, Workbench, SSOT, and
  public SPEC changes in the P5 correction: 0.

## Custody and next action

The isolated worktree is clean after this handoff. The orphaned writer worktree
and its `parser.rs`, local-project, project-authoring, and tool-runtime WIP are
not modified, staged, reset, or adopted here.

The next C1-L11 preparation is read-only: convert the currently observed
Workbench generator forms `쓰임 { 힘: \"./lib/힘\". }` and `드러냄 { 중력. }` to
the approved static-directive forms `(힘=\"./lib/힘\") 쓰임.` and
`(중력=중력) 드러냄.` only after that producer path receives its own clean lease.

## Disposition

`RD457_STATUS=PRODUCT_FIXED_READY_FOR_INDEPENDENT_REVIEW`.
`READY_FOR_INDEPENDENT_REVIEW=YES` means that an immutable review target is
available; it is not an independent PASS or a V1 closure, readiness, release,
or Human-PASS claim.
