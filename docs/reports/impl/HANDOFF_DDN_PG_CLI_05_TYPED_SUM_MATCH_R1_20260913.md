# PG-CLI-05 Typed Sum/Match R1 handoff

## Fixed target

- Product commit: `f4feea01cbf15ff6d9e7d04942d05024d2150335`
- Product tree: `a75df8dd4527d6515769d9e31c791aed5798a004`
- Product parent: `6b3285f1b74a866c8b0cda657b62a994ad5ccbe0`
- Claim: `PRODUCT_FIXED_PENDING_INDEPENDENT_REVIEW`

## Product scope

The shared language path admits typed sum declarations, exact qualified branch
construction, and statement-only `에 따라` dispatch. The runtime keeps branch
values lexical when first bound with `<-`; it does not introduce a resource
wire or serialize a new public value representation.

Changed product paths are `lang/src/{ast,lexer,parser,canonicalizer,normalizer,
execution_mode,migration,runtime}.rs`, `lang/tests/pg_cli_typed_sum_match.rs`,
and direct tool runtime/LSP traversal consumers.

## Primary gates

```text
cargo test -p ddonirang-lang --test pg_cli_typed_sum_match --offline
cargo test -p ddonirang-tool pg_cli_typed_sum_match_executes_exact_branch_and_fails_before_publication --lib --offline -- --nocapture
cargo check -p ddonirang-tool --lib --offline
cargo check -p ddonirang-tool --lib --features wasm --target wasm32-unknown-unknown --offline
git diff --check
```

The focused language gate covers canonical LF/reparse stability, exact owner
binding, duplicate and incomplete arms, bare branches, and dollar text. The
runtime gate covers payload dispatch and failure-before-output publication.

## Mutation and restore evidence

- `M1_EXHAUSTIVENESS`: temporarily bypassing the no-default exhaustiveness
  guard makes the negative focused test RED.
- Fixed parser blob after restore: `e6ea6a97d10773d3784c518d8c9ba15597eb8316`
- Fixed parser SHA-256 after restore:
  `708938760FC3BE22E564B83942CA5D484E6A857B23AEAF9FECA36E635E6EF03C`
- Restore result: the full focused language gate GREEN.

## Review boundary and nonclaims

Review the shared lexer-to-runtime path, exact-match and atomicity guards, and
Native/WASM compile parity. This handoff does not claim expression-valued
match, a new public wire/diagnostic identity, tracked UI-WASM rematerialization,
V1 readiness, release, support, or Human PASS.
