# TYPEAPP canonical round-trip and presentation correction — handoff

## Scope and authority

- Task: `TYPEAPP-PRODUCT-CANON-ROUNDTRIP-AND-PRESENTATION-CORRECTION-R1`
- Product worktree: `I:/home/urihanl/ddn/codex/build/worktrees/ddn-p-v1-project-ux-r2-census-r1-20260828`
- Branch: `codex/ddn-v1-p1a-core-supported-ingress-w1-20260829`
- Base: `277c325db79510b899379e17add199b0d9f09db1` / tree `8da771d692b0c80730d6dd7894cd5bfd685025b9`
- Product fixed: `895669fce6ea55e03157fa27e6c5cd6e82735064` / tree `8f5e6efdffdea3d48c907e5fb816c94eef86537e`
- Product parent: `277c325db79510b899379e17add199b0d9f09db1`; merge count `0`
- Live read-only authority: internal SSOT `v25.54.0 / RD-001~557`; public Language SPEC `v0.6.0`
- Fixed64 integrated: `NO`

## Correction

- `lang/src/normalizer.rs`: applied types now emit comma-separated arguments while preserving existing formatter spacing (`(글, 수) 짝맞춤`); nested types remain parse/normalize stable.
- `lang/src/frontdoor.rs`: applied-type diagnostic labels now use canonical source shape (`(글,(수)차림)짝맞춤`) rather than angle pseudo-source.
- `lang/src/stdlib.rs`: 60 signature occurrences were changed from angle pseudo-source to canonical applied-type source; runtime authority, generic identity, registration, and public spelling are unchanged.
- No new parser, AST, compatibility alias, tensor syntax, tool/core/runtime, B-01, SSOT, SPEC, UI, or Fixed64 changes.

## RED → restore → GREEN

- Normalizer predecessor separator mutation (`" "`) produced a parse failure at the normalized applied type; exact separator restoration returned focused GREEN.
- Frontdoor predecessor label mutation (`name<args>`) failed the canonical-label assertion; exact restoration returned GREEN.
- One stdlib predecessor angle signature mutation failed the no-angle census; exact restoration returned GREEN.
- Mutation residue `0`; no protected custody changed.

## Verification

- focused applied-type tests: `2/2 PASS`
- stdlib signature census test: `1/1 PASS`
- `cargo test -p ddonirang-lang`: `372` unit tests and `4` integration tests PASS; doc-tests `0`
- `cargo check -p ddonirang-lang`: PASS
- `git diff --check`: PASS
- new test artifacts: `0`; existing Rust test modules extended only; meta-test `0`
- parse → normalize → parse → normalize stability: single, multi, nested, and doubly nested applied types PASS

## Custody and nonclaims

- Target product diff is exactly the three leased `lang/src` files above; tracked/staged product diff outside them `0`.
- Four protected untracked session deltas remain byte/hash unchanged and unstaged.
- No cargo/rustc/ddonirang/teul process residue; merge `0`.
- `SEMANTIC_DELTA=0`, `SSOT_CHANGE=0`, `PUBLIC_SPEC_CHANGE=0`, `B01_PRODUCT_DIFF=0`.
- `READY_FOR_INDEPENDENT_REVIEW=YES`; `REVIEW_VERDICT=NOT_PERFORMED`.
- This handoff does not claim P0/P1/P4/VE03/V1 closure, readiness, release, activation, legal approval, or Human PASS.
