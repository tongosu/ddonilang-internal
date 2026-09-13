# PG-CLI-03 indexed ResultFlow handoff

## Claim

- Product target: `9983a04276e252558f937da3d7e23e015a36c9f6`
- Tree: `c8b67b0b26ed938fdb3806e534a0044498b734f2`
- Parent: `343ab3f911c74ae193ef33a0bac393621f9c2eb5`

Current V25 `producer -> collection[index].` is retained as typed
`Stmt::ResultFlow`; it is not lowered to `Stmt::Mutate`. The producer is
evaluated first, then an immutable replacement candidate is validated before
the root binding is committed. A non-indexed destination is rejected with
`E_RESULT_FLOW_DESTINATION_PLACE_REQUIRED`.

PreV25 right-assignment custody is unchanged: only the V25 parser epoch
admits this ResultFlow category.

## Product paths

- `lang/examples/canon_ast_dump.rs`
- `lang/src/{ast,canonicalizer,execution_mode,migration,normalizer,parser}.rs`
- `lang/tests/pg_cli_result_flow.rs`
- `tool/src/{ddn_runtime,local_project,project_authoring,wasm_api,work_cost}.rs`
- `tool/src/lsp/{folding_range,selection_range,signature_help,symbol}.rs`
- `tool/tests/fixtures/pg_cli_result_flow.ddn`
- `tool/tests/lsp_open_document_navigation.rs`
- tracked `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_{bg.wasm,manifest.detjson}`

The direct AST-consumer expansion is limited to exhaustiveness and structural
child traversal. It creates neither a second parser nor a DefinitionIdentity.

## Primary gates

```text
cargo test -p ddonirang-lang --test pg_cli_result_flow --offline
cargo test -p ddonirang-tool pg_cli_result_flow_updates_a_selection_only_after_the_candidate_is_ready --lib --offline
cargo test -p ddonirang-lang --offline                         # 374 passed
cargo test -p ddonirang-tool --test lsp_open_document_navigation --offline # 9 passed
cargo check -p ddonirang-lang -p ddonirang-tool --offline
python tests/run_ddn_cli_wasm_freshness_check.py
```

All gates passed. Source-built `ddonilang`, `또니랑`, and `ddonirang` produced
byte-identical output for `tool/tests/fixtures/pg_cli_result_flow.ddn`.
The rebuilt tracked WASM ran the same source twice with the same result and
published `차림[1, 0]`.

Tracked artifact SHA-256: `D16D6D442AC84CF10EA5A0995C33C7002AE22172BF318E4B12A14D19940B1452`.
Manifest SHA-256: `E7471A84AEEB777951CAA771BAD2A9C8C62E4F221ABA0E80113819F8D4E54A35`.

## Mutation evidence

| Mutation | Observed RED | Exact restored fixed blob / SHA-256 | Green gate |
| --- | --- | --- | --- |
| M1: lower ResultFlow to Mutate | AST test reported `arrow statement must retain ResultFlow, not Mutate`; canon lost `1 -> 판[0].` | `lang/src/parser.rs` `0a159b24b816c707a6073b591ddb896714e1983e` / `D307FEDF271922B7A00B288FA58F2A34793BD101A0D88E1BF771C6B0D87DEE69` | `pg_cli_result_flow` |
| M2: accept non-selection destination | `1 -> 판.` parsed as `ResultFlow { destination: Var("판") }`; fail-closed test failed | same parser blob / SHA-256 | `pg_cli_result_flow` |
| M3: remove collection bounds guard | invalid index triggered a Rust bounds panic instead of `FATAL:CHARIM_INDEX_OUT_OF_RANGE` | `tool/src/ddn_runtime.rs` `41fe651b62d459c8a2f9fbdd3e552b74301b838b` / `8E07E04A5B52F6F813AB92B7EEBC9D52AA327AE628BC9DF65A06565AAC760253` | ResultFlow runtime test |

Each mutation was restored byte-exactly before its focused GREEN rerun.
`git diff --check` passed before the product commit.

## Review request and nonclaims

Review the exact target, V25/PreV25 separation, parser/canon roundtrip,
candidate-before-commit runtime behavior, LSP selection parent chain, three
CLI output equality, and tracked WASM freshness. This writer does not claim
independent PASS, official blocker-row closure, release/support, SSOT/public
SPEC transition, or completion of the full scripted Tetris workflow.
