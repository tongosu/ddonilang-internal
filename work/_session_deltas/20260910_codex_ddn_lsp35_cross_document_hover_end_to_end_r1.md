# DDN-LSP35 Cross-Open-Document Hover — Handoff

## Identity

- Base: `01d6aed66db07584c670d22be3543a6e28772abf`
- Product: `b5eb3a9f1e4f80c852b0f6ebc0c054838d515845`
- Product tree: `cf2b211f288084f8bed1c3cd424626d581fedc64`
- Product parent: `01d6aed66db07584c670d22be3543a6e28772abf`
- Review: `PRODUCT_FIXED_PENDING_REVIEW`
- Author/committer: `tongosu <tongosu@myarts.kr>`

## Scope

LSP35 extends `textDocument/hover` to resolve the same existing local
DefinitionIdentity across currently open DDN documents. It reuses
`DocumentStore` and `tool/src/lsp/symbol.rs`; it does not add a parser, index,
filesystem crawl, source upload, remote server, or semantic owner. URI and
source order remain deterministic. Closed and duplicate declarations return
null, stale version/snapshot requests fail closed, and the result range is
encoded as UTF-16 from the live reference snapshot.

Changed product paths:

- `tool/src/lsp/server.rs`
- `tool/tests/lsp_hover.rs`

Product blobs at the fixed target:

- `tool/src/lsp/server.rs`: `cb86c8ec7bd1d69277d050b6590f1f7912673326`
- `tool/tests/lsp_hover.rs`: `5a887230ea48967377bdf995d0c2b4c94ec6ad46`

## Focused and regression evidence

Focused command:

```text
cargo test -q -p ddonirang-tool --test lsp_hover
```

Result: `4 passed, 0 failed`.

Applicable LSP regression command covered hover, type definition, definition,
references, rename, document symbols, completion, signature help,
diagnostics, and semantic tokens. Result: all listed test binaries passed.

Persistent checker:

```text
python tests/run_lsp0_transport_document_sync_check.py
```

Result: `LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS`; H12 hover,
ST23 type-definition, G12 definition, R14 references, SH16 rename, and all
other reported before-EOF cases were `PASS`.

Other gates:

- `cargo check -q -p ddonirang-tool --bin ddonirang-lsp --offline`: PASS
- `git diff --check`: PASS
- package regression: `635 passed, 2 failed`

The two package failures are the known environment-only
`ai_prompt_output_matches_golden` and `ai_prompt_output_invariants_hold`
failures. Both fail before product assertions because this isolated worktree
does not contain `docs/ssot`; no product or SSOT change was made.

## Fresh mutation evidence

Each mutation was applied alone, then restored before the next mutation.

1. Cross-document collision guard removal in `tool/src/lsp/symbol.rs`:

```text
removed: if candidates.len() == 1 { ... } else if candidates.len() > 1 { ... }
applied: if !candidates.is_empty() { ... } else if candidates.len() > 1 { ... }
```

RED: the duplicate-open-document case returned a hover object instead of
`null`.

Exact restore: the exact one-candidate guard and explicit duplicate branch.

GREEN: `lsp_hover` returned `4 passed, 0 failed` after restore.

2. UTF-16 range downgrade in `tool/src/lsp/server.rs`:

```text
removed: result.reference_range, encoding
applied: result.reference_range, PositionEncoding::Utf8
```

RED: the emoji-prefix range expected character `18` and observed `28`.

Exact restore: `result.reference_range, encoding`.

GREEN: `lsp_hover` returned `4 passed, 0 failed` after restore.

3. Hover stale-version guard removal:

```text
removed: if requested_version != snapshot.version {
applied: if false && requested_version != snapshot.version {
```

RED: the stale hover test received a successful current result instead of
error `-32801`.

Exact restore: `if requested_version != snapshot.version`.

GREEN: `lsp_hover` returned `4 passed, 0 failed` after restore.

## LSP22C environment gate

The supplied VSIX was not rebuilt. Three read-only updater checks still found
`CodeSetup-stable-...` and its temporary companion process. No updater was
terminated, no installation was attempted, and no real Extension Host result
was claimed. Status: `HOLD_EXTERNAL_VSCODE_UPDATER_ONLY`.

## Nonclaims

This handoff does not claim independent review PASS, whole LSP/IDE closure,
public extension release, V1 readiness, release, or Human PASS.
