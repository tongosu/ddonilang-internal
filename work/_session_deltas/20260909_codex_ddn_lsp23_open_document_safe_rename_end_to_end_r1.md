# DDN-LSP23 Open-Document Safe Rename — R1 Handoff

## Fixed lineage

```ini
IMPLEMENTATION_BASE = 894e47fb48dfd7b7c139f0bad040523da7f33cfa
PRODUCT_FIXED = 1d31bcc498b953f3bb8a2fe302a71af60f38cfaf
PRODUCT_TREE = 3cf7132f8851b36740a4ea8602c858099a68d318
PRODUCT_PARENT = 894e47fb48dfd7b7c139f0bad040523da7f33cfa
PRODUCT_MERGE_COUNT = 0
ACTIVE_UNIT = LSP23_OPEN_DOCUMENT_SAFE_RENAME
```

Product commit changed exactly four paths:

```text
tests/run_lsp0_transport_document_sync_check.py
tool/src/lsp/rename.rs
tool/src/lsp/server.rs
tool/tests/lsp_rename.rs
```

`tools/vscode-ddn/**` was unchanged. LSP22 VSIX was not rebuilt.

## Implemented behavior

```ini
PREPARE_RENAME = PASS
RENAME = PASS
SAME_DOCUMENT = PASS
OPEN_DOCUMENT_CROSS_FILE = PASS
IDENTITY_BINDING = PASS
UTF16_RANGE = PASS
VERSIONED_DOCUMENT_EDITS = PASS
DETERMINISTIC_ORDER = PASS
COLLISION_FAIL_CLOSED = PASS
UNSAFE_OPEN_DOCUMENT_FAIL_CLOSED = PASS
PARTIAL_EDIT_COUNT = 0
```

The server advertises `renameProvider.prepareProvider = true`. Rename reuses
the existing local `DefinitionIdentity` owner and returns versioned
`TextDocumentEdit` entries for currently open documents only. Closed documents
are excluded, malformed open DDN snapshots reject the complete rename, and the
existing collision, stale-snapshot, invalid-name, ambiguous, comment/string,
stdlib and non-local guards remain active. Responses arrive before EOF and the
server remains usable over a persistent connection.

## Verification

Focused rename:

```text
cargo test -p ddonirang-tool --test lsp_rename
PASS: 5 tests
```

Focused LSP regressions:

```text
cargo test -p ddonirang-tool --test lsp_definition
cargo test -p ddonirang-tool --test lsp_references
cargo test -p ddonirang-tool --test lsp_document_symbol
cargo test -p ddonirang-tool --test lsp_diagnostics
cargo test -p ddonirang-tool --test lsp_completion
cargo test -p ddonirang-tool --test lsp_signature_help
cargo test -p ddonirang-tool --test lsp_semantic_tokens
cargo test -p ddonirang-tool --test lsp_document_highlight
PASS: all commands
```

Persistent black-box:

```text
python tests/run_lsp0_transport_document_sync_check.py
LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS
SH16_BLACKBOX_RENAME_BEFORE_EOF=PASS
G12/S13/R14/SH15/HL17/ST18/ST19/ST20 regression checks=PASS
PROTOCOL_REPEAT=BYTE_STABLE
```

Clean validation:

```text
cargo check -p ddonirang-tool --bin ddonirang-lsp --offline = PASS
git diff --check = PASS
```

Complete package regression returned 635 passed and 2 failed. The only failures
were the pre-existing environment-sensitive tests
`ai_prompt::tests::ai_prompt_output_matches_golden` and
`ai_prompt::tests::ai_prompt_output_invariants_hold`, both because the
worktree-local `docs/ssot` path was unavailable. Classification:
`NONBLOCKING_PREEXISTING_ENVIRONMENT_FAILURE`. No product or prompt change was
made.

## Mutation evidence

Each mutation was applied alone, the focused test was run immediately, the
original bytes were restored, and the same test returned GREEN. No mutation was
staged or committed.

### M1 — UTF-16 range guard

```ini
TARGET = tool/src/lsp/server.rs
ORIGINAL_SHA256 = 6636A75A0BF30B6F33377FBED9DE25C01801A88B90A5D5FE5B986B89B729DD4B
ORIGINAL_BLOB = fa8ae4220d8c5177248a4e4d6c9bf40a226631ec
RESTORE_SHA256 = 6636A75A0BF30B6F33377FBED9DE25C01801A88B90A5D5FE5B986B89B729DD4B
RESTORE_BLOB = fa8ae4220d8c5177248a4e4d6c9bf40a226631ec
```

```diff
- let range = super::position::byte_range_to_lsp_range(source, range, encoding)
+ let range = super::position::byte_range_to_lsp_range(
+     source,
+     range,
+     PositionEncoding::Utf8,
+ )
```

```text
RED:
cargo test -p ddonirang-tool --test lsp_rename lsp7_prepare_and_rename_reuses_local_identity_and_utf16_ranges -- --exact
FAIL: Korean UTF-16 range; actual 36..45, expected 20..23
EXACT RESTORE: SHA-256 and Git blob matched the original values
GREEN: same command PASS
```

### M2 — closed-document exclusion

```ini
TARGET = tool/src/lsp/server.rs
ORIGINAL_SHA256 = 6636A75A0BF30B6F33377FBED9DE25C01801A88B90A5D5FE5B986B89B729DD4B
ORIGINAL_BLOB = fa8ae4220d8c5177248a4e4d6c9bf40a226631ec
RESTORE_SHA256 = 6636A75A0BF30B6F33377FBED9DE25C01801A88B90A5D5FE5B986B89B729DD4B
RESTORE_BLOB = fa8ae4220d8c5177248a4e4d6c9bf40a226631ec
```

```diff
- self.documents.close(uri).map_err(ServerError::Document)?;
+ let _ = self.documents.get(uri);
```

```text
RED:
cargo test -p ddonirang-tool --test lsp_rename lsp11_cross_open_document_rename_is_atomic_versioned_and_deterministic -- --exact
FAIL: returned URI list included file:///c.ddn; expected only file:///a.ddn and file:///b.ddn
EXACT RESTORE: SHA-256 and Git blob matched the original values
GREEN: same command PASS
```

### M3 — identity binding guard

```ini
TARGET = tool/src/lsp/rename.rs
ORIGINAL_SHA256 = CCA28D388C96F0EBF5C654D8AFC20225820F25C2724C4B971CE349898DAB0281
ORIGINAL_BLOB = 03616394c5fb2cd1a35c65ad880c960a57c2bf8a
RESTORE_SHA256 = CCA28D388C96F0EBF5C654D8AFC20225820F25C2724C4B971CE349898DAB0281
RESTORE_BLOB = 03616394c5fb2cd1a35c65ad880c960a57c2bf8a
```

```diff
- let ranges = collect_local_references_for_identity(document, &symbol.identity, true)?;
+ let ranges = collect_local_references_for_identity(
+     document,
+     &format!("definition:local:{}", new_name),
+     true,
+ )?;
```

```text
RED:
cargo test -p ddonirang-tool --test lsp_rename lsp11_cross_open_document_rename_is_atomic_versioned_and_deterministic -- --exact
FAIL: rename result was None and the test panicked at the result unwrap
EXACT RESTORE: SHA-256 and Git blob matched the original values
GREEN: same command PASS
```

### M4 — collision guard

```ini
TARGET = tool/src/lsp/rename.rs
ORIGINAL_SHA256 = CCA28D388C96F0EBF5C654D8AFC20225820F25C2724C4B971CE349898DAB0281
ORIGINAL_BLOB = 03616394c5fb2cd1a35c65ad880c960a57c2bf8a
RESTORE_SHA256 = CCA28D388C96F0EBF5C654D8AFC20225820F25C2724C4B971CE349898DAB0281
RESTORE_BLOB = 03616394c5fb2cd1a35c65ad880c960a57c2bf8a
```

```diff
- if documents.iter().any(|document| {
+ if false && documents.iter().any(|document| {
      collect_document_symbols(document)
```

```text
RED:
cargo test -p ddonirang-tool --test lsp_rename lsp7_change_stale_collision_invalid_nonlocal_and_close_fail_closed -- --exact
FAIL: WorkspaceEdit with newText="둘함수" returned; expected null for collision
EXACT RESTORE: SHA-256 and Git blob matched the original values
GREEN: same command PASS
```

## Scope and handoff state

```ini
LSP22_REAL_HOST_SMOKE = BLOCKED_ENVIRONMENT
LSP22_VSIX_REBUILT = NO
SOURCE_UPLOAD = 0
REMOTE_DEPENDENCY = 0
FILESYSTEM_CRAWL = 0
FOREIGN_DIRTY_TOUCHED = 0
PROTECTED_UNTRACKED_CHANGED = 0
PRODUCT_PACKAGING_CHANGED = 0
PUSH_PERFORMED = NO
PROCESS_RESIDUE = 0
READY_FOR_INDEPENDENT_REVIEW = YES
LSP23_STATUS = PRODUCT_FIXED_PENDING_REVIEW
NEXT_EXACT_ACTION = independent review bound to PRODUCT_FIXED 1d31bcc498b953f3bb8a2fe302a71af60f38cfaf
```

The LSP22 host gate remains a separate environment blocker and was not
retested or treated as an LSP23 product defect. The worktree still has
pre-existing foreign tracked changes outside this task's four product paths;
none were formatted, staged, reset, or committed.
