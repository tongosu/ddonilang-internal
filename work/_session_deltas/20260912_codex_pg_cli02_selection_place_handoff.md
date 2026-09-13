# PG-CLI-02 SelectionPlace handoff

Product target: `921bd23005692e009212dccfcf9df1ebef479fae`

Parent: `61b26a70d669729056ded4525cccca6f72d6f332`

## Claim

`대상[index] <- 값.` now remains an `ExprKind::SelectionPlace` solely as a
`Stmt::Mutate` target. It is not a postfix value selection, callable, or a new
DefinitionIdentity. Runtime evaluates a candidate immutable replacement via the
existing `차림.바꾼값` owner and commits the root only after that candidate is
valid. Evaluation errors pass through the mutation snapshot restore.

## Product paths

- `lang/src/{ast,parser,canonicalizer,normalizer,execution_mode,migration,lib}.rs`
- `lang/examples/canon_ast_dump.rs`
- `lang/tests/pg_cli_selection_place.rs`
- `tool/src/ddn_runtime.rs`
- `tool/src/{project_authoring,work_cost}.rs`
- `tool/src/lsp/{selection_range,signature_help,symbol}.rs`
- `tool/tests/fixtures/pg_cli_selection_place.ddn`
- tracked WASM and `ddonirang_tool.manifest.detjson`

The direct exhaustive consumers only recurse structural children; the LSP paths
create no symbol, callable or token identity for SelectionPlace.

## Focused evidence

- `cargo test -p ddonirang-lang --test pg_cli_selection_place --offline` — 3/3 PASS.
- `cargo test -p ddonirang-tool --lib pg_cli_selection_place --offline` — 2/2 PASS.
- Existing PG-CLI-01 language tests — 3/3 PASS.
- Source-built `ddonilang`, `또니랑`, and `ddonirang` each accepted the exact
  fixture under `--source-profile v1-core-v25`, with the same revision identity.
- Official WASM build followed by freshness manifest generation and
  `python tests/run_ddn_cli_wasm_freshness_check.py` — PASS.
- `cargo test -p ddonirang-lang --offline` — PASS (374 unit tests plus integrations).
- `cargo check -p ddonirang-lang -p ddonirang-tool --offline` and `git diff --check` — PASS.

`cargo test -p ddonirang-tool --lib --offline` remains non-green in this
isolated worktree: 14 unrelated pre-existing failures include unavailable
`docs/ssot` for ai_prompt and existing project-authoring/runtime-surface
expectations. The PG-CLI focused runtime gates pass; this is a nonclaim, not a
full-tool regression PASS.

## Mutations

| Axis | Observed RED | exact restore |
| --- | --- | --- |
| M1 range guard | Replacing `if index >= items.len()` with `if false && ...` made the out-of-range focused test panic at `out[index]`. | `tool/src/ddn_runtime.rs` blob `708f117558f9acfb83488028cb7af50cc8bbc18b`; focused GREEN after restore. |
| M2 selection index binding | Replacing the SelectionPlace index with the root expression made the structural AST assertion fail because the index was not a literal. | `lang/src/parser.rs` blob `da0fddb7f9727c0251af91e47269d885ef5b7047`; focused GREEN after restore. |

Tracked post-build hashes:

- WASM: `37BD0588B55A9742A82C993A0B51E0ACA1F61B3749EC284C288F193F25A335DB`
- manifest: `246F630BB27AD049B8FC55BFF8B55F0E5ADC18B63DB3820301D0191EE4498254`
- L2 source fixture: `CCED99DDCAD904EC7C4B65DE6E851769E9777812A66FB105F4BDAAAB4C69EC7B`

## Review request / nonclaims

Review `921bd230…` for SelectionPlace category preservation, out-of-range
failure atomicity, three-name source-analysis parity and tracked-WASM freshness.
This handoff makes no independent PASS claim and does not claim the unavailable
immutable L0 seed was run in this worktree.
