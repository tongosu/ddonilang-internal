# DDN-LSP29 OPEN-DOCUMENT-DOCUMENT-HIGHLIGHT-R1 — HANDOFF

## Target and custody

```ini
ACTIVE_UNIT = LSP29_OPEN_DOCUMENT_DOCUMENT_HIGHLIGHT
BASE_PRODUCT = a49355918d38f3d8bbdcb1934b60afca6ab2b8c7
PRODUCT_FIXED = 5519dde3334606fc17866adc6d87090e47404406
PRODUCT_TREE = 8966f09524842c40d22bbe8f815a18821ccdc4f0
PRODUCT_PARENT = a49355918d38f3d8bbdcb1934b60afca6ab2b8c7
PRODUCT_PATHS = tool/src/lsp/document_highlight.rs, tool/src/lsp/server.rs, tool/tests/lsp_document_highlight.rs
TOOL_SRC_LIB_RS_CHANGED = 0
NEW_DEPENDENCY = 0
PUBLIC_WIRE_CHANGE = 0
FILESYSTEM_CRAWL = 0
SOURCE_UPLOAD = 0
REMOTE_DEPENDENCY = 0
```

The product commit is the first commit after the LSP28 docs handoff. Previous LSP26/LSP27/LSP28 commits were not amended or rewritten.

## Implemented behavior

- `textDocument/documentHighlight` uses the existing `DocumentStore` snapshot and `symbol.rs` local `DefinitionIdentity` owner.
- Declaration and same-document typed references are returned in source order; non-local/stdlib, ambiguous, comment, string, whitespace, punctuation, closed-document, stale-version, and stale-snapshot cases fail closed.
- Existing UTF-16 conversion is retained for Korean and non-BMP-offset contexts.
- `MAX_DOCUMENT_HIGHLIGHTS = 1_000` bounds the result.
- Cancellation is checked before publication and after range materialization; a cancelled request publishes an error and no success result.
- Existing didChange, didClose, initialize capability, and persistent response-before-EOF paths remain active.

## Exact mutation evidence

All mutations were applied one at a time and restored before the next mutation.

### M1 — typed identity filter removal

Target: `tool/src/lsp/document_highlight.rs`, `document_highlights_snapshot`, local identity guard.

Exact diff:

```diff
-    if !symbol.identity.starts_with("definition:local:") {
+    if false {
```

Original restored file SHA-256: `61851B6AA647EAD497C081212512AA8BC12EE1E63C55EA03FDADF998CF2960F5`

Original restored blob: `6e9de3692697ccd7af8b59bd48b9d8357641bfa8`

RED command:

```text
cargo test -p ddonirang-tool --test lsp_document_highlight
```

RED core output:

```text
assertion failed: document_highlights_snapshot(...).unwrap().is_none()
at tool/tests/lsp_document_highlight.rs:232
test result: FAILED. 3 passed; 1 failed
```

Exact restore: PASS; the file returned to the SHA-256 and blob above.

GREEN after restore: `4 passed; 0 failed`.

### M2 — UTF-16 range downgraded to UTF-8

Target: `tool/src/lsp/server.rs`, document-highlight byte-range conversion.

Exact diff:

```diff
-                    super::position::byte_range_to_lsp_range(source, highlight.range, encoding)
+                    super::position::byte_range_to_lsp_range(
+                        source,
+                        highlight.range,
+                        PositionEncoding::Utf8,
+                    )
```

Original restored file SHA-256: `6E00F1305CF2CBFE81AF59E0B0F35DE3DA98AEB15560F038AB33C195C27D2551`

Original restored blob: `e22d64516568ef91f3cbf2ad1d2e98b6807d1893`

RED command:

```text
cargo test -p ddonirang-tool --test lsp_document_highlight
```

RED core output:

```text
assertion `left == right` failed
left:  start character 31, end character 40
right: start character 19, end character 22
at tool/tests/lsp_document_highlight.rs:94
test result: FAILED. 3 passed; 1 failed
```

Exact restore: PASS; the file returned to the SHA-256 and blob above.

GREEN after restore: `4 passed; 0 failed`.

### M3 — stale-version guard removal

Target: `tool/src/lsp/server.rs`, `document_highlights` requested-version guard.

Exact diff:

```diff
-            if requested_version != snapshot.version {
+            if false && requested_version != snapshot.version {
```

Original restored file SHA-256: `6E00F1305CF2CBFE81AF59E0B0F35DE3DA98AEB15560F038AB33C195C27D2551`

Original restored blob: `e22d64516568ef91f3cbf2ad1d2e98b6807d1893`

RED command:

```text
cargo test -p ddonirang-tool --test lsp_document_highlight
```

RED core output:

```text
assertion failed: stale response did not return error code -32801
at tool/tests/lsp_document_highlight.rs:157
test result: FAILED. 3 passed; 1 failed
```

Exact restore: PASS; the file returned to the SHA-256 and blob above.

GREEN after restore: `4 passed; 0 failed`.

## Verification

```ini
FOCUSED = cargo test -p ddonirang-tool --test lsp_document_highlight = PASS (4/4)
LSP_REGRESSION = completion, definition, diagnostics, document_symbol, hover, open_document_navigation, references, rename, semantic_tokens, signature_help = PASS
BLACKBOX_BEFORE_EOF = python tests/run_lsp0_transport_document_sync_check.py = PASS
OFFLINE_CARGO_CHECK = cargo check -p ddonirang-tool --bin ddonirang-lsp --offline = PASS
DIFF_CHECK = git diff --check = PASS
```

Full package validation ran once before product fixation: `635 passed, 2 failed, 637 total`. The only failures were the pre-existing environment-dependent `ai_prompt_output_matches_golden` and `ai_prompt_output_invariants_hold`, caused by the unavailable `I:\home\urihanl\ddn\codex\docs\ssot` path. They are `NONBLOCKING_PREEXISTING_ENVIRONMENT_FAILURE`, not LSP29 findings.

## Review and next custody

```ini
LSP26_STATUS = CLOSED_TARGET_BOUND
LSP27_STATUS = PRODUCT_FIXED_PENDING_REVIEW
LSP28_STATUS = PRODUCT_FIXED_PENDING_REVIEW
LSP29_STATUS = PRODUCT_FIXED_PENDING_REVIEW
READY_FOR_INDEPENDENT_REVIEW = YES
PUSH_PERFORMED = NO
FOREIGN_DIRTY_TOUCHED = 0
PROTECTED_UNTRACKED_CHANGED = 0
```

The next autonomous unit is not started in this handoff. Git/backup Work must snapshot the exact LSP29 product and handoff identities before any successor unit begins.

```ini
GIT_AUTHOR = tongosu <tongosu@myarts.kr>
GIT_COMMITTER = tongosu <tongosu@myarts.kr>
PROHIBITED_TRAILER_COUNT = 0
```
