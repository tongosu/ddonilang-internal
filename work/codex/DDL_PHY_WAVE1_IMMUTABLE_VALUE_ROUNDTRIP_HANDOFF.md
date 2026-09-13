# DDL PHY Wave 1 immutable value round-trip handoff

## Fixed target

- Product fixed: `2809a7a1b0489d164bf6a418c8cbf5de59c6dfb9`
- Parent: `a843d50f8404af693878f82dd30f61b56c76f70f`
- Tree: `0f35fa5a1b2e22deafbd2d3dbe51c3ed6ee380e8`
- Merge count: `0`
- Author and committer: `tongosu <tongosu@myarts.kr>`

## Implemented Wave 1 boundary

`.ddl` and `.옮김` now admit only exact `#!한국어` and `#!日本語` headers,
with exactly two top-level sections and one registry-owned immutable public
value projection each.  The two localized surfaces bind the same internal
`DefinitionIdentity` and `TypeIdentity`; no path, source order, localized
spelling, locale, or automatic alias has identity authority.

The DDL-only `:={...}` omission maps to `OmittedPayload::ValueInitializer`.
It has no executable body, runtime value, synthetic initializer, CLI, WASM,
wire, or IDE/LSP effect.  Canon preserves source section order as presentation,
uses LF, and stabilizes parse -> canon -> parse -> canon.

The Japanese declaration is exact-registry admitted because the existing
shared lexer currently does not tokenize Japanese identifiers.  This is not a
fallback parser, locale fallback, or generalized Japanese DDN route.

## Changed paths

```text
lang/src/ddl.rs
lang/src/ast.rs
lang/src/canonicalizer.rs
lang/src/lib.rs
lang/tests/ddl_physical_first_vertical.rs
```

## Verification

- focused DDL integration: 7/7 PASS
- `cargo test -p ddonirang-lang`: 372 unit + 7 DDL integration + 4 existing
  V25 integration PASS
- `cargo check -p ddonirang-lang`: PASS
- `git diff --check`: PASS before fixed commit

Mutation proof, each against `lang/src/ddl.rs` raw SHA-256
`5bd461c6934a18549151efc876513d31e6252ba11d506f6a723548c810a5f9a9`:

| Mutation | RED signal | Exact restore + focused GREEN |
|---|---|---|
| M1 remove `.옮김` admission | `.옮김` positive rejected as unsupported | PASS |
| M2 ignore nested block depth at header scan | nested `#!` test changed failure mode | PASS |
| M3 admit generic `#!qu` | generic-Quechua rejection test changed failure mode | PASS |
| M4 split localized DefinitionIdentity | positive shared-identity parse rejected | PASS |

No mutation residue was committed.  Final `lang/src/ddl.rs` working-tree
SHA-256 is `e5685b2a5f1399e6b9dbe4ad36745859940964ffea959d37869bf7c9766542a6`.

## Custody and nonclaims

- SSOT change: 0; public SPEC change: 0
- runtime/CLI/WASM/wire/IDE-LSP change: 0
- new dependency: 0; new pack/runner/meta-test: 0/0/0
- The pre-existing foreign tracked changes in `lang/src/model.rs`,
  `lang/src/parser.rs`, `lang/src/runtime.rs`, and `lang/src/stdlib.rs` were
  neither staged nor modified by this unit.  The four protected untracked
  session-delta files remain untouched.

Status: `DDL_WAVE1_PRODUCT_IMPLEMENTED=YES`,
`DDL_WAVE1_CLOSURE_CANDIDATE_READY=YES`,
`READY_FOR_INDEPENDENT_REVIEW=YES`.

This does not claim full DDL, public DDL support, 17-language support,
callable/type projection, V1 readiness, release, or Human PASS.
