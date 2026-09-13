# PG-CLI-04 named single-expression pure callable — handoff

## Claim

- Product target: `604717bb29102b70a05e64809b29908b8ace32de`
- Tree: `97753f06a3a97984c5f48a980fc8010a366a7f78`
- Parent: `e8d228e2049a1e55fa4ac5c6fe72f85af5dde393`
- Surface: `이름 (받는자리:타입, ... --> 결과타입) := 식.`

The shared V25 parser retains this as a named `SeedKind::ValueFunc` with a
declared result type. It is not lowered to a binding, lambda, or ordinary
`움직씨`. Canonical output retains the same surface; the runtime checks the
declared result type before successful call completion.

## Product paths

- `lang/src/ast.rs`
- `lang/src/parser.rs`
- `lang/src/canonicalizer.rs`
- `lang/src/normalizer.rs`
- `lang/tests/pg_cli_pure_callable.rs`
- `tool/src/ddn_runtime.rs`
- `tool/tests/fixtures/pg_cli_pure_callable.ddn`

## Primary gates

```text
cargo test -p ddonirang-lang --test pg_cli_pure_callable --offline
cargo test -p ddonirang-tool pg_cli_rd406_named_single_expression_callable_runs_and_checks_its_result_type --lib --offline -- --nocapture
cargo test -p ddonirang-lang --offline
cargo check -p ddonirang-lang --offline
```

All listed gates passed. The three source-built binaries `ddonilang`, `또니랑`,
and `ddonirang` ran `tool/tests/fixtures/pg_cli_pure_callable.ddn` with
`--source-profile v1-core-v25`; each produced `output_log_texts=["34"]` and
the same stdout SHA-256:

```text
7C42163CEA998E969C8DA58D505B97217FE38FEFE70978D6F5906A8A16E6D21A
```

## Mutation evidence

| Mutation | Observed RED | Fixed blob / exact restore | Green gate |
| --- | --- | --- | --- |
| M1: direct header uses `Semssi` instead of `ValueFunc` | AST assertion reported `left: Semssi`, `right: ValueFunc` | `lang/src/parser.rs` blob `94ca8fa7cbf14f10a9f25aca7e17bd89a6f6b0a0` | PG-CLI-04 parser test |
| M2: result type check removed | runtime test failed: `wrong typed callable result must fail closed` | `tool/src/ddn_runtime.rs` blob `9bae39feb2239602b63bd0d823f24cd7c27ebdac` | PG-CLI-04 runtime test |

`git diff --check` passed before the product commit. This handoff does not
claim independent review, V1 release/support, public-SPEC change, WASM
freshness, or a complete Tetris workflow.

## Review request

Verify exact target, direct-surface parse/canon/reparse behavior, result-type
failure atomicity, and the two mutations above. A review verdict must be bound
to this product target; this writer makes no independent PASS claim.
