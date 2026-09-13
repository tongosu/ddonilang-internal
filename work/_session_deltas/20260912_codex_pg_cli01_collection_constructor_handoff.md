# PG-CLI-01 CollectionConstructor handoff — 2026-09-12

## Fixed target

- Product: `f9261848bd90c6554952e80a1ffb1dcbed24158e`
- Tree: `caf1a8f777d48efb52d6ec46980a98030632810a`
- Parent: `a6fe774f4c3e062802ec7fcd334b94d554f3ba3f`
- Claim: current V25 `차림[...]` is a typed `ExprKind::CollectionConstructor`, distinct from postfix selection and calls. `(T)차림` remains an applied element type.

## Product scope

The parser, AST, canonicalizer, normalizer, runtime, LSP structural consumers and exhaustive traversal consumers preserve the constructor and its authored element order. Runtime rejects mixed runtime categories before state/output publication. Signature help traverses nested calls but never publishes the constructor itself as a callable.

The compiler-required direct exhaustive-consumer extensions were `lang/examples/canon_ast_dump.rs`, `lang/src/execution_mode.rs`, `lang/src/migration.rs`, `tool/src/project_authoring.rs`, and `tool/src/work_cost.rs`. WASM binary and manifest were rematerialized because shared `lang/src` and `tool/src` source changed.

## Evidence

- Focused language test: `cargo test -p ddonirang-lang --test pg_cli_collection_constructor --offline` — 3/3 PASS.
- Focused runtime tests: `cargo test -p ddonirang-tool --lib pg_cli_collection_constructor --offline` — 2/2 PASS.
- Focused LSP behavior: `cargo test -p ddonirang-tool --lib collection_constructor_is_not_published --offline` — PASS.
- Native three-name source-built checks of `tool/tests/fixtures/pg_cli_collection_constructor.ddn` — `ddonilang`, `또니랑`, `ddonirang` all ACCEPTED.
- Full `cargo test -p ddonirang-lang --offline` — 374 unit + integration suites PASS.
- Full `cargo test -p ddonirang-tool --lib --offline` and `cargo check -p ddonirang-lang -p ddonirang-tool --offline` — PASS.
- Official WASM builder, manifest writer and `python tests/run_ddn_cli_wasm_freshness_check.py` — PASS.
- `git diff --check` — PASS. The immutable L0 source seed was absent from this clean worktree and remains unmodified.

## Mutation / exact restore

| Axis | RED result | Restore |
| --- | --- | --- |
| M1 parser category | Changing `차림` recognition to `묶음` made the AST focused test fail at parse with `]`. | `lang/src/parser.rs` blob `8ac8962f532909c82fb73d1b1d8607c0f8993809`, SHA-256 `F234F4C572C57DE56F6578DA6D579BFD3563E5F324D8F51AA9C0DE1023AC35E0`; focused GREEN. |
| M2 mixed-element guard | Suppressing the category mismatch guard made the atomicity focused test fail because the mixed collection succeeded. | `tool/src/ddn_runtime.rs` blob `527d06e22013a60c43422107906b65ccd171a05f`, SHA-256 `D98F43450E1ECB2419B375C21DD5F2ECA34E131E39DAA81F5FCE1D8814BDBED3`; focused GREEN. |

Tracked artifact SHA-256: `ddonirang_tool_bg.wasm` `37BD0588B55A9742A82C993A0B51E0ACA1F61B3749EC284C288F193F25A335DB`; manifest `A252CDF8F6D2ACF85D95DF1333FCA6052E50AB0854645020BF1112D4D55C013D`.

## Review request / nonclaims

Review the exact product target above for parser category separation, mixed-element failure atomicity, LSP non-call publication, and tracked-WASM freshness. This writer does not issue an independent PASS. No SSOT, public SPEC, public wire, new semantic identity, legacy lowering, or public-release claim is made.

Next exact action: independent review of `f9261848…`, then implement PG-CLI-02 as a separate successor vertical.
