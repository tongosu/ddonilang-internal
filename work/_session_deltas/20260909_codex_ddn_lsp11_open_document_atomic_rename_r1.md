# DDN-LSP11-OPEN-DOCUMENT-ATOMIC-RENAME-R1

## Fixed lineage

- predecessor product: `e6f015868acf425b3eb11cff3fe4c09e3f0e40b6`
- predecessor handoff: `ab24f3e8c59bbd284e8c192335a1968f63064edc`
- LSP11 implementation commit: `48886c30e032a98e46bb4a71edfe4628a9b54386`
- implementation tree: `26a164ff3532f2ed1cc1bcc4ce307ec8f735b530`
- implementation parent: `ab24f3e8c59bbd284e8c192335a1968f63064edc`
- validation correction commit: `fe333ffe875375d4bcc94cb325fbc685cfc360ba`
- current fixed tree: `0616abe0582996c8c058801dea6114c5c6319f0c`
- correction parent: `48886c30e032a98e46bb4a71edfe4628a9b54386`

The correction commit only binds the existing black-box runner to its fresh Cargo target directory and updates its LSP11 multi-document coordinate. It does not change product rename semantics.

## Scope and behavior

Changed paths:

```text
tests/run_lsp0_transport_document_sync_check.py
tool/src/lsp/rename.rs
tool/src/lsp/server.rs
tool/src/lsp/symbol.rs
tool/tests/lsp_rename.rs
```

- `textDocument/prepareRename` and `textDocument/rename` reuse the existing `DocumentStore` and shared symbol owner.
- Only currently open documents participate; filesystem crawl, unopened read, hidden index, remote server, source upload, new parser, and new identity owner are all zero.
- Rename resolves one unique local `DefinitionIdentity` across open documents. Duplicate definitions are rejected.
- All target ranges are collected and validated before `documentChanges` are constructed. The result is versioned `TextDocumentEdit` entries in deterministic URI lexical order.
- Each edit document is bound to its current document version and snapshot identity in response data.
- Invalid/empty names, stale version/snapshot, closed documents, nonlocal symbols, malformed source, comments, strings, punctuation, and unrelated symbols fail closed or remain unchanged.
- Korean and emoji UTF-16 ranges, didChange current snapshot, didClose exclusion, deterministic repeated response, and response before EOF are covered.

## Mutation evidence

Each mutation was applied alone. The same focused test was run for RED, then the original hunk was restored byte-exactly and the test was GREEN.

### M1 — partial WorkspaceEdit publication

- Target: `tool/src/lsp/rename.rs`, workspace target collection loop.
- Original hunk:

```rust
for document in documents {
    let ranges = collect_local_references_for_identity(document, &symbol.identity, true)?;
```

- Mutation hunk:

```rust
for document in documents.iter().take(1) {
    let ranges = collect_local_references_for_identity(document, &symbol.identity, true)?;
```

- Command: `cargo test -p ddonirang-tool --test lsp_rename lsp11_cross_open_document_rename_is_atomic_versioned_and_deterministic --offline --quiet`
- RED: URI list was `["file:///a.ddn"]`, not `["file:///a.ddn", "file:///b.ddn", "file:///c.ddn"]`.
- Mutation SHA-256: `88436C6D00C428C5794F8485EC6E8F02951E0E435348DDC31CC046959F0DF971`.
- Exact restore SHA-256 before final formatting: `8D450B46390BFB3D20132F46946D1694B9AFAB5846670F3ED36EF930A0521995`.
- Final formatted file SHA-256: `3890B88CBBFC7AC315E5ED02C2E524890185734D489F1CDA5ECC1676048CF984`.
- GREEN: focused rename suite `4 passed`.

### M2 — lexical false-positive in string token content

- Target: `tool/src/lsp/symbol.rs`, identity reference token filter.
- Original hunk: `.filter(|token| token_name(token) == Some(name))`
- Mutation hunk: `.filter(|token| token_name(token) == Some(name) || token.raw.contains(name))`
- Command: `cargo test -p ddonirang-tool --test lsp_rename lsp7_prepare_and_rename_reuses_local_identity_and_utf16_ranges --offline --quiet`
- RED: rename edit count became `4` instead of `3`; the string occurrence was included.
- Mutation SHA-256: `651E6F435929C2AE7175CF84433963594A63854E02DAB4CC8C95F4A700E1B23C`.
- Exact restore/final SHA-256: `A900229269F6E255CEA981C1089A4D833B36E6038ABC3ECAF510522EA815526C`.
- GREEN: focused rename suite `4 passed`.

### M3 — stale-version guard removal

- Target: `tool/src/lsp/server.rs`, `textDocument/rename` request guard.
- Original guard rejects `requested_version != snapshot.version` with `-32801`.
- Mutation: removed that rejection block from `rename` only.
- Command: `cargo test -p ddonirang-tool --test lsp_rename lsp7_change_stale_collision_invalid_nonlocal_and_close_fail_closed --offline --quiet`
- RED: stale request no longer returned error code `-32801`; stale assertion failed.
- Mutation SHA-256: `C0FFEBD903A1E5CC1B252B95164B441A0F0F956C51382B66A2A84BE2BA913865`.
- Exact restore SHA-256 before final formatting: `840DE270496F7577872CCD478F364C5C37688066AF13F9ECCB8891CA4F0D9179`.
- Final formatted file SHA-256: `7DAC42763503A530E5D5AEF100B4A1610E7588316A85791E2D4599E8C154B875`.
- GREEN: focused rename suite `4 passed`.

## Validation

- Focused: `cargo test -p ddonirang-tool --test lsp_rename --offline --quiet` — `4 passed`.
- Applicable LSP regression: rename, open-document navigation, definition, references, document symbols, document highlight, signature help, semantic tokens, hover, diagnostics, completion — all groups passed.
- Persistent black-box runner: all transport cases, `SH16_BLACKBOX_RENAME_BEFORE_EOF`, `ST18`, `ST19`, and `ST20` passed; final `LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS`.
- Clean snapshot: minimal Git archive of `fe333ffe` with workspace Cargo files and `core/lang/numeric/proof/symbolic/tool/tests`; `cargo check --manifest-path .../tool/Cargo.toml --bin ddonirang-lsp --offline` exited `0`.
- Direct dirty-worktree cargo check was not treated as a product failure: it hit pre-existing foreign `lang/**` changes against the shared `core` path. The clean fixed snapshot passed.
- `git diff --check`: PASS for owned product paths.

## Custody

- Product semantic paths: `tool/src/lsp/rename.rs`, `tool/src/lsp/server.rs`, `tool/src/lsp/symbol.rs`.
- Existing test/checker paths: `tool/tests/lsp_rename.rs`, `tests/run_lsp0_transport_document_sync_check.py`.
- `tool/src/lib.rs`: unchanged.
- New dependency/pack/runner/meta-test: `0`.
- Foreign dirty paths: untouched and unstaged.
- Public push: `NO`.
- Author/committer: `tongosu <tongosu@myarts.kr>`.
- Prohibited trailer count: `0`.
- LSP9D/LSP10 review: `PASS_TARGET_BOUND`, preserved and not replayed.
- Ready for independent LSP11 review; no later unit was started.
