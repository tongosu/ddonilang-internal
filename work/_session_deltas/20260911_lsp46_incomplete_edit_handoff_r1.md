# DDN-LSP46 — incomplete-edit semantic token handoff R1

## Scope and custody

- Unit: `DDN-LSP46-INCOMPLETE-EDIT-SEMANTIC-HIGHLIGHTING-R1`
- Baseline: `a9664d0d49569aba88f10f74b31edb176a78b3f3`
- Product commit: `76a54c972cbc6e13efa7a3df53803506100ff0f3`
- Product tree: `c300226df2430dce0ec009f91da317f00b9c5be9`
- Product parent: `a9664d0d49569aba88f10f74b31edb176a78b3f3`
- Product paths: `tool/src/lsp/semantic_tokens.rs`, `tool/tests/lsp_semantic_tokens.rs`
- Author and committer: `tongosu <tongosu@myarts.kr>`
- No SSOT, public SPEC, dependency, VSIX, extension, or foreign dirty path was changed.

## Behavior

When the current source cannot be parsed, the existing lexer is used only for a
bounded safe fallback: strings, numbers, exact keyword tokens, and operators /
punctuation. Identifiers, josa, variables, definitions, types, parameters, and
references are not inferred from incomplete text. Lexer failure returns an empty
stream. The fallback uses the existing UTF-16 encoder, deterministic token
ordering and size bound. Result IDs remain bound to the current document
snapshot; existing version, snapshot, cancellation, full/delta and didClose
guards remain in force. A repaired source returns the AST-bound identity stream
again; an invalid current snapshot never reuses the prior result.

## Verification

- `cargo test -p ddonirang-tool --test lsp_semantic_tokens --offline`: 6 passed.
- `cargo test -p ddonirang-tool --test lsp0_transport_document_sync --test lsp_semantic_tokens --offline`: 23 + 6 passed.
- `cargo check -p ddonirang-tool --bin ddonirang-lsp --offline`: passed.
- `git diff --check`: passed.
- A separate `CARGO_TARGET_DIR` was used for the final validation snapshot.

## Mutation evidence

Each mutant was applied one at a time and restored from the product commit
before the next mutation. The listed restore blob is the exact fixed blob.

### M1 — stale result reuse after current empty result

- Mutation: in `server.rs`, replace an empty current result with the cached URI
  result before insertion.
- Mutant blob (`tool/src/lsp/server.rs`):
  `46a01d41defab79296b047bb2fbb8657359bd9c2`
- RED: `lsp46_incomplete_source_keeps_bounded_lexical_roles_without_stale_identity_tokens` failed because the malformed current result returned the prior token array instead of empty/safe current data.
- Restore: `git restore --source=HEAD -- tool/src/lsp/server.rs`
- Restored blob: `fb855fdcfa14daa56a0917c5168801d5c515a7cd`
- GREEN: 6 semantic-token tests passed.

### M2 — identifier inference in lexical fallback

- Mutation: classify `TokenKind::Ident(_)` as semantic token type `2`.
- Mutant blob (`tool/src/lsp/semantic_tokens.rs`):
  `d745d36bcb5dab603d124aef66e0ca0bcbeebdce`
- RED: `lsp46_incomplete_source_keeps_bounded_lexical_roles_without_stale_identity_tokens` and `lsp9_full_tokens_stale_change_malformed_and_close_fail_closed` failed because incomplete text gained identity-class token types `0..=3`.
- Restore: `git restore --source=HEAD -- tool/src/lsp/semantic_tokens.rs`
- Restored blob: `854eb5e3820973c4b77019ffed2436d95bebc014`
- GREEN: 6 semantic-token tests passed.

### M3 — string role damage

- Mutation: classify `TokenKind::StringLit(_)` as keyword/operator type `4` instead of string type `5`.
- Mutant blob (`tool/src/lsp/semantic_tokens.rs`):
  `cdd1ef8b80e186556ca454ee4ccbe218918323f2`
- RED: `lsp46_incomplete_source_keeps_bounded_lexical_roles_without_stale_identity_tokens` failed because no fallback string token type `5` remained.
- Restore: `git restore --source=HEAD -- tool/src/lsp/semantic_tokens.rs`
- Restored blob: `854eb5e3820973c4b77019ffed2436d95bebc014`
- GREEN: 6 semantic-token tests passed.

## LSP45 disposition

`LSP45_COMPOSITE_KOREAN_PHRASE_HIGHLIGHTING = HOLD_OWNER_SEMANTIC_AUTHORITY`.
The requested `결과에 따라` / `전력결과에 따라` surface is recognized by a
runtime `currentline.rs` regex handler, but the ordinary `parse_v25` path used by
LSP semantic tokens rejects it. The lexer emits `에` as josa and `따라` as an
identifier; no shared parser/AST composite node or approved semantic token owner
was found. No LSP mini-parser, raw substring rule, or runtime-only surface was
promoted. An Owner/grammar decision is required before LSP45 can be implemented.

## Environment and next gate

- Real VS Code host: `HOLD_EXTERNAL_VSCODE_UPDATER_ONLY`; no updater process was
  terminated and no retry loop was run.
- Existing non-task `ddonirang-lsp.exe` process was not touched.
- Product status: `PRODUCT_FIXED_PENDING_REVIEW`.
- This handoff is docs-only and must be committed separately from the product
  commit. Independent review is required; this file does not issue a PASS.
