# DDN-LSP30 OPEN-DOCUMENT-PULL-DIAGNOSTICS-R1 — HANDOFF

## Target and custody

```ini
ACTIVE_UNIT = LSP30_OPEN_DOCUMENT_PULL_DIAGNOSTICS
BASE_PRODUCT = f75e31dff9933e20f4654be25417d2efb7534a08
PRODUCT_FIXED = a70f26631560b878ee6d2cdc8b495f8f90faf865
PRODUCT_TREE = c6d7d7b5b7ac86e7364c490ef86828457cd33bca
PRODUCT_PARENT = f75e31dff9933e20f4654be25417d2efb7534a08
PRODUCT_PATHS = tool/src/lsp/server.rs, tool/tests/lsp_diagnostics.rs
UNEXPECTED_PATHS = 0
TOOL_SRC_LIB_RS_CHANGED = 0
NEW_DEPENDENCY = 0
PUBLIC_DDN_WIRE_CHANGE = 0
FILESYSTEM_CRAWL = 0
REMOTE_DEPENDENCY = 0
SOURCE_UPLOAD = 0
```

The LSP29 product and handoff commits were preserved. LSP30 is a direct successor and does not amend, rewrite, revert, or merge prior commits.

## Pull diagnostic behavior

```ini
SHARED_DIAGNOSTIC_OWNER = diagnostics::analyze_snapshot
DOCUMENT_SOURCE = current open DocumentStore snapshot only
DIAGNOSTIC_PROVIDER = identifier ddonirang-v25; interFileDependencies=true; workspaceDiagnostics=true
FULL_REPORT = kind=full, items, deterministic resultId
UNCHANGED_REPORT = only when previousResultId exactly equals current resultId
RESULT_ID_BINDING = URI + version + snapshot identity + serialized diagnostic content
RESULT_BOUND = 1000 diagnostics
UTF16 = existing shared PositionEncoding conversion retained
LIFECYCLE = didChange refreshes; didClose/unknown returns existing explicit -32602 error
STALE = existing -32801 version and -32802 snapshot taxonomy retained
CANCELLATION = no success payload after cancellation checks
ORDER = existing deterministic diagnostic ordering retained
RESPONSE_BEFORE_EOF = existing persistent transport contract retained
```

The existing `tests/run_lsp0_transport_document_sync_check.py` already contained the pull-diagnostics before-EOF case (`ST23_BLACKBOX_PULL_DIAGNOSTICS_BEFORE_EOF`), so no new runner or pack was created.

## Exact mutation evidence

All counted mutations were applied one at a time. The fixed `server.rs` restore identity after every mutation was:

```ini
SHA256 = 1F056E11DAD0F429563C5972075B6A1AA9DDF49B076D593DD5A9E3770EF1ABF2
GIT_BLOB = 4a1f002134046748568563709919624457b4e59b
```

### M1 — snapshot identity removed from resultId

Target: `tool/src/lsp/server.rs`, `diagnostic_result_id`.

Exact diff:

```diff
-        "sha256:{:x}:{}",
+        "sha256:{:x}",
         hasher.finalize(),
-        snapshot.identity.as_str()
```

RED command:

```text
cargo test -p ddonirang-tool --test lsp_diagnostics
```

RED core output:

```text
assertion failed: result_id.ends_with(&format!(":{snapshot_identity}"))
at tool/tests/lsp_diagnostics.rs:366
test result: FAILED. 10 passed; 1 failed
```

Exact restore: PASS; SHA-256 and Git blob returned to the identities above.

GREEN after restore: `11 passed; 0 failed`.

### M2 — previousResultId accepted without equality

Target: `tool/src/lsp/server.rs`, `text_document_diagnostic` report selection.

Exact diff:

```diff
-        let result = if previous_result_id == Some(result_id.as_str()) {
+        let result = if previous_result_id.is_some() {
```

RED command:

```text
cargo test -p ddonirang-tool --test lsp_diagnostics
```

RED core output:

```text
assertion `left == right` failed
left: String("unchanged")
right: "full"
at tool/tests/lsp_diagnostics.rs:384
test result: FAILED; 10 passed; 1 failed
```

Exact restore: PASS; SHA-256 and Git blob returned to the identities above.

GREEN after restore: `11 passed; 0 failed`.

### M3 — UTF-16 diagnostic range downgraded to UTF-8

Target: `tool/src/lsp/server.rs`, `text_document_diagnostic` analysis call.

Exact diff:

```diff
-        let report = analyze_snapshot(snapshot, encoding).map_err(ServerError::Diagnostics)?;
+        let report = analyze_snapshot(snapshot, PositionEncoding::Utf8)
+            .map_err(ServerError::Diagnostics)?;
```

RED command:

```text
cargo test -p ddonirang-tool --test lsp_diagnostics
```

RED core output:

```text
assertion `left == right` failed
left: diagnostic end character 4
right: diagnostic end character 2
at tool/tests/lsp_diagnostics.rs:356
test result: FAILED; 10 passed; 1 failed
```

Exact restore: PASS; SHA-256 and Git blob returned to the identities above.

GREEN after restore: `11 passed; 0 failed`.

An initial URI-only hash-removal probe was discarded because the existing snapshot identity transitively includes URI; it did not produce a RED and is not counted as mutation evidence.

## Verification

```ini
FOCUSED = cargo test -p ddonirang-tool --test lsp_diagnostics = PASS (11/11)
LSP_REGRESSION = completion 15, definition 3, document_highlight 4, document_symbol 4, open_document_navigation 11, references 4, rename 5, semantic_tokens 3, signature_help 3 = PASS
BLACKBOX_BEFORE_EOF = python tests/run_lsp0_transport_document_sync_check.py = PASS
  ST23_BLACKBOX_PULL_DIAGNOSTICS_BEFORE_EOF = PASS
OFFLINE_CARGO_CHECK = cargo check -p ddonirang-tool --bin ddonirang-lsp --offline = PASS
DIFF_CHECK = git diff --check = PASS
```

The full package `ai_prompt` environment failures were not repeated, per the LSP30 instruction. The immediately preceding fixed validation recorded the same pre-existing pair: `ai_prompt_output_matches_golden` and `ai_prompt_output_invariants_hold`, caused by the unavailable `I:\home\urihanl\ddn\codex\docs\ssot` path. They remain `NONBLOCKING_PREEXISTING_ENVIRONMENT_FAILURE`.

## Review and successor custody

```ini
LSP26_STATUS = CLOSED_TARGET_BOUND
LSP27_STATUS = PRODUCT_FIXED_PENDING_REVIEW
LSP28_STATUS = PRODUCT_FIXED_PENDING_REVIEW
LSP29_STATUS = PRODUCT_FIXED_PENDING_REVIEW
LSP30_STATUS = PRODUCT_FIXED_PENDING_REVIEW
READY_FOR_INDEPENDENT_REVIEW = YES
PUSH = NO
FOREIGN_DIRTY_TOUCHED = 0
PROTECTED_UNTRACKED_CHANGED = 0
TASK_OWNED_DIRTY = 0
STAGED = 0
PROCESS_RESIDUE = 0
NEXT_AUTONOMOUS_UNIT = LSP31 open-document-only workspace/diagnostic, after Git/backup exact snapshot
```

```ini
GIT_AUTHOR = tongosu <tongosu@myarts.kr>
GIT_COMMITTER = tongosu <tongosu@myarts.kr>
PROHIBITED_TRAILER_COUNT = 0
```
