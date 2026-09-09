# DDN-LSP24 open-document workspace symbol — handoff R1

## Authority and custody

```makefile
IMPLEMENTATION_BASE = 011e4540237c642651c9b954f9899f2b0fdead9e
LSP23_PRODUCT = 1d31bcc498b953f3bb8a2fe302a71af60f38cfaf
LSP23_REVIEW_WAITING = YES
LSP24_STATUS = PRODUCT_FIXED_PENDING_REVIEW
PRODUCT_SCOPE = current DocumentStore open documents only
SHARED_SYMBOL_OWNER = tool/src/lsp/symbol.rs
FILESYSTEM_CRAWL = 0
REMOTE_DEPENDENCY = 0
SOURCE_UPLOAD = 0
TOOL_SRC_LIB_RS_CHANGED = 0
NEW_DEPENDENCY = 0
```

The existing `DocumentStore` and shared symbol owner remain the only semantic
owners. Results come from current open snapshots, in deterministic URI order
and source order, with a hard limit of 1000. Empty and whitespace-only
queries return an empty result. didChange uses the current snapshot, didClose
removes the document immediately, and cancellation returns `-32800` without a
success result.

## Product commit

```makefile
LSP24_PRODUCT_TARGET = 07d62f47fbaec5320e89cd568438b3538712cbbb
LSP24_PRODUCT_TREE = 3d12d34835644abd5f3a0bed3f2578279ed52b8e
LSP24_PRODUCT_PARENT = 011e4540237c642651c9b954f9899f2b0fdead9e
MERGE_COUNT = 0
PRODUCT_PATHS = tests/run_lsp0_transport_document_sync_check.py, tool/src/lsp/server.rs, tool/tests/lsp_document_symbol.rs
PRODUCT_PATH_COUNT = 3
AUTHOR = tongosu <tongosu@myarts.kr>
COMMITTER = tongosu <tongosu@myarts.kr>
PROHIBITED_TRAILER_COUNT = 0
```

Only the three product paths above changed. No `tools/vscode-ddn` path
changed.

## Behavior and validation

```makefile
WORKSPACE_SYMBOL_PROVIDER = PASS
OPEN_DOCUMENT_ONLY = PASS
DIDCHANGE_CURRENT_SNAPSHOT = PASS
DIDCLOSE_REMOVAL = PASS
UTF16_RANGE = PASS
DETERMINISTIC_ORDER = PASS
RESULT_LIMIT = PASS, 1000
CANCELLATION_ATOMICITY = PASS, -32800
UNKNOWN_PRIVATE_FALSE_SYMBOLS = PASS, existing shared symbol rules
```

Focused Rust tests:

```text
cargo test -p ddonirang-tool --test lsp_document_symbol
4 passed; 0 failed

Focused regression loop:
lsp_document_symbol, lsp_rename, lsp_references, lsp_definition,
lsp_hover, lsp_diagnostics, lsp_completion
LSP24_FOCUSED_REGRESSION=PASS
```

Coverage includes open-document value/function search, cross-document results,
Korean/emoji UTF-16 ranges, current snapshot/version binding, didClose
removal, empty/whitespace rejection, deterministic repeat, the 1000-result
boundary, and cancellation.

Persistent black-box:

```text
I1_INITIALIZE_BEFORE_EOF=PASS
I2_FRAGMENTED_HEADER=PASS
I3_FRAGMENTED_UTF8_BODY=PASS
I4_MULTI_FRAME_SINGLE_WRITE=PASS
I5_PERSISTENT_LIFECYCLE=PASS
WS21_BLACKBOX_WORKSPACE_SYMBOL_BEFORE_EOF=PASS
S13_BLACKBOX_DOCUMENT_SYMBOL_BEFORE_EOF=PASS
R14_BLACKBOX_REFERENCES_BEFORE_EOF=PASS
SH16_BLACKBOX_RENAME_BEFORE_EOF=PASS
ST20_BLACKBOX_OPEN_DOCUMENT_NAVIGATION_BEFORE_EOF=PASS
LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS
```

```text
cargo check -p ddonirang-tool --bin ddonirang-lsp --offline = PASS
git diff --check (owned paths and staged product diff) = PASS
tools/vscode-ddn npm test = PASS
VS Code package inventory = 7 files, forbidden file count = 0
```

The extension package was not modified or rebuilt by LSP24.

The one full package regression requested before fixing ran once:

```text
cargo test -p ddonirang-tool
635 passed; 2 failed
```

The two failures are pre-existing environment failures, not LSP24 findings:

```text
ai_prompt::tests::ai_prompt_output_matches_golden
ai_prompt::tests::ai_prompt_output_invariants_hold
reason: worktree-local docs/ssot path is absent
classification: NONBLOCKING_PREEXISTING_ENVIRONMENT_FAILURE
```

## Mutation evidence

The pre-mutation `tool/src/lsp/server.rs` identity used for all restore checks:

```makefile
SERVER_PRE_MUTATION_SHA256 = 7b33d0f7cc22729361f5e04e631ba2dd76ff7033b44324365e59d0fb2607138f
SERVER_PRE_MUTATION_BLOB = 0245e518586b80d14cf3c3c05a615c5db537d4ed
```

### M1 — retain closed document after didClose

Target: `tool/src/lsp/server.rs`, `did_close`.

Exact temporary diff:

```diff
-        self.documents.close(uri).map_err(ServerError::Document)?;
+        let _ = self.documents.get(uri);
```

Command:

```text
cargo test -p ddonirang-tool --test lsp_document_symbol lsp12_workspace_symbol_is_open_document_bounded_and_snapshot_bound -- --exact
```

RED: assertion at line 306 reported `left: 2`, `right: 1`; the closed URI
remained in workspace-symbol results.

```makefile
EXACT_RESTORE = PASS
RESTORE_SHA256 = 7b33d0f7cc22729361f5e04e631ba2dd76ff7033b44324365e59d0fb2607138f
RESTORE_BLOB = 0245e518586b80d14cf3c3c05a615c5db537d4ed
GREEN = same focused test, 1 passed; 0 failed
RESIDUE = 0
```

### M2 — calculate workspace-symbol range as UTF-8

Target: `tool/src/lsp/server.rs`, workspace-symbol selection range.

Exact temporary diff:

```diff
                 let range = super::position::byte_range_to_lsp_range(
                     source,
                     symbol.selection_range,
-                    encoding,
+                    PositionEncoding::Utf8,
                 )
```

Command:

```text
cargo test -p ddonirang-tool --test lsp_document_symbol lsp12_workspace_symbol_is_open_document_bounded_and_snapshot_bound -- --exact
```

RED: assertion at line 238 reported start/end `31..40` instead of the
UTF-16 `19..22` range for the emoji-bearing source.

```makefile
EXACT_RESTORE = PASS
RESTORE_SHA256 = 7b33d0f7cc22729361f5e04e631ba2dd76ff7033b44324365e59d0fb2607138f
RESTORE_BLOB = 0245e518586b80d14cf3c3c05a615c5db537d4ed
GREEN = same focused test, 1 passed; 0 failed
RESIDUE = 0
```

### M3 — remove result limit

Target: `tool/src/lsp/server.rs`, `MAX_WORKSPACE_SYMBOLS` guard.

Exact temporary diff:

```diff
-                if results.len() >= MAX_WORKSPACE_SYMBOLS {
-                    return Ok(success_event(id, json!(results)));
-                }
```

Command:

```text
cargo test -p ddonirang-tool --test lsp_document_symbol lsp24_workspace_symbol_query_limit_and_cancellation_contract -- --exact
```

RED: assertion at line 339 reported `left: 1001`, `right: 1000`.

```makefile
EXACT_RESTORE = PASS
RESTORE_SHA256 = 7b33d0f7cc22729361f5e04e631ba2dd76ff7033b44324365e59d0fb2607138f
RESTORE_BLOB = 0245e518586b80d14cf3c3c05a615c5db537d4ed
GREEN = same focused test, 1 passed; 0 failed
RESIDUE = 0
```

## Final custody

```makefile
TASK_OWNED_DIRTY = 0
STAGED = 0 after product commit
FOREIGN_DIRTY_TOUCHED = 0
PROTECTED_UNTRACKED_CHANGED = 0
PROCESS_RESIDUE = 0
PUSH_PERFORMED = NO
LSP22_VSIX_REBUILT = NO
READY_FOR_INDEPENDENT_REVIEW = YES
NEXT_AUTONOMOUS_UNIT = successor selection after review dispatch
```

Foreign pre-existing tracked changes remain outside the LSP24 owned paths and
were not staged, formatted, reset, or committed.
