# C1-L11 strict current frontdoor handoff

## Fixed target

- Product commit: `269460066f1f7030e0552437bf003423a1a1613b`
- Product tree: `1a7748f4dbf6309b67010e7791d18ea9920a858a`
- Parent: `6c3a9c973af2052508fe22d8023a52978baec9c9`
- Scope: `lang/src/parser.rs`, `lang/tests/v25_definition_binding_pack.rs`

## Behavior

The V25 parser now rejects brace-form legacy `쓰임 {}`, `드러냄 {}`, and
`공개 {}` before AST admission with
`E_V25_DEFINITION_MIGRATION_REQUIRED`.  The check operates on lexer tokens,
so text inside a string literal is not classified as a legacy directive.
Parenthesized RD-457 directives remain covered by the existing shared
frontdoor regression.

## Evidence

- `cargo test -p ddonirang-lang --test v25_definition_binding_pack -- --nocapture`: 5/5 PASS
- `cargo test -p ddonirang-lang --test rd457_module_directive_roundtrip -- --nocapture`: 6/6 PASS
- `cargo test -p ddonirang-lang --offline`: 374/374 PASS
- `cargo check -p ddonirang-lang --offline`: PASS
- `git diff --check`: PASS
- Mutation M1: disabling the guard made the strict V25 assertion RED; the
  parser was restored byte-exactly to blob
  `6259b2607a66df20a0294665ad6d617060e1fcf7` and SHA-256
  `7fc55a8d5f33bbf5919fa5b312260ecf8ceed5242e4c68ba7c0312ef4d0dd956`,
  then the focused gate was GREEN.

## Nonclaims

This is `PRODUCT_FIXED_PENDING_REVIEW` for the strict L11 current-frontdoor
slice only. It does not close C1-L11 producer dependency-zero, P0-P6, V1
readiness, release, activation, legal, or Human PASS.
