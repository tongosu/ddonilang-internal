# DDN-LSP39-READABLE-SYNTAX-AND-SEMANTIC-TOKENS-R1 — HANDOFF

## Scope

- Baseline: `0d411acfe457f59d350aa9f947bf2b7b36a89736`
- Product commit: `330280289af99319bb585b83ce86283ebcbb18ef`
- Product tree: `020266add9a141ff723c04914e60b470ac86e49d`
- Product parent: `0d411acfe457f59d350aa9f947bf2b7b36a89736`
- Product paths: `tool/src/lsp/semantic_tokens.rs`, `tool/src/lsp/server.rs`, `tool/tests/lsp_semantic_tokens.rs`, `tools/vscode-ddn/syntaxes/ddn.tmLanguage.json`
- Foreign dirty paths were not modified, staged, or restored.

## Product behavior

- Reuses lexer/parser `Token`, `SeedDef`, `ParamPin`, shared `symbol::declaration_range`, and the existing stdlib registry.
- Keeps the existing semantic token type order and adds the standard modifiers `declaration` and `defaultLibrary`.
- Emits declaration modifiers for AST-bound callable/type and parameter declaration ranges; references retain the existing function/type/parameter categories.
- TextMate grammar now exposes matching declaration, call-site, parameter, control, type, literal, and operator scopes for the four admitted extensions.
- Unsupported source profiles remain empty; line comments remain unclassified through the existing lexer/parser admission path.
- No user theme or global VS Code setting is changed.

## Mutation evidence

All mutations were one-at-a-time, followed immediately by source restoration and the same focused GREEN check. The pre-mutation `tool/src/lsp/semantic_tokens.rs` SHA-256 was:
`6142242D818B66683AE82B80C90B343124721B09B29F2966406FA36D292E294C`.

1. `M1_PARAMETER_DECLARATION_MODIFIER_GUARD`
   - Temporary diff: replaced `if parameter_declaration_ranges.contains(&range) { 1 } else { 0 }` with `modifiers: 0`.
   - RED: `lsp39_roles_use_ast_bound_declaration_modifiers_and_ignore_line_comments` failed because no parameter declaration token had modifier bit `1`.
   - Exact restore: restored the conditional hunk; SHA-256 returned to `6142242D818B66683AE82B80C90B343124721B09B29F2966406FA36D292E294C`.
   - GREEN: the same focused test passed.

2. `M2_UTF16_TO_UTF8_POSITION_DOWNGRADE`
   - Temporary diff: replaced the semantic-token conversion argument `encoding` with `PositionEncoding::Utf8`.
   - RED: `lsp9_full_tokens_use_lexer_categories_utf16_and_deterministic_delta` failed at the expected UTF-16 token position.
   - Exact restore: restored the `encoding` argument; SHA-256 returned to `6142242D818B66683AE82B80C90B343124721B09B29F2966406FA36D292E294C`.
   - GREEN: the same focused test passed.

3. `M3_UNSUPPORTED_SOURCE_ADMISSION_GUARD`
   - Temporary diff: replaced `if snapshot.language_id != "ddn"` with `if false`.
   - RED: `lsp39_unsupported_source_is_not_semantically_classified` returned semantic data for `file:///unsupported.txt` instead of `[]`.
   - Exact restore: restored the language-id guard; SHA-256 returned to `6142242D818B66683AE82B80C90B343124721B09B29F2966406FA36D292E294C`.
   - GREEN: the same focused test passed.

## Verification

- `cargo test -p ddonirang-tool --test lsp_semantic_tokens --offline`: 5 passed.
- `npm test --prefix tools/vscode-ddn`: PASS; package inventory 7 files, forbidden count 0.
- Node syntax and JSON parse checks: PASS.
- `cargo check -p ddonirang-tool --offline`: PASS.
- `git diff --check` for LSP39 paths: PASS.
- Persistent real VS Code host was not claimed here; LSP38 real-host status remains environment-blocked by the external updater/mutex packet.

## Custody

- Author/committer: `tongosu <tongosu@myarts.kr>`.
- Product commit is linear and has no prohibited trailer.
- This file is the LSP39 docs-only handoff; it does not change SSOT, public SPEC, or closed predecessor targets.
- Independent review status: `READY_FOR_INDEPENDENT_REVIEW = YES`.
