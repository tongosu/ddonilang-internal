# DDN-LSP1-SHARED-DIAGNOSTICS-PUBLISHING-R1 — handoff

## Authority and boundary

- `LIVE_AUTHORITY`: existing LSP0 transport/document-sync and completion targets already bound to the clean linear successor `446b359d3dfcde62c613e1231c5d742a14af582f`.
- `IMPLEMENTATION_BASE`: `446b359d3dfcde62c613e1231c5d742a14af582f`.
- Existing LSP0, completion Unit A, and completion Unit B target-bound results were reused; no re-review was performed.
- `REMOTE_SERVER_DEPENDENCY=0`; `SOURCE_UPLOAD=0`; no asynchronous worker or queue was added.
- Foreign dirty tracked files and protected untracked files in the product worktree were not modified, staged, or committed.

## Product commit

```ini
PRODUCT_FIXED_HEAD = e4adaa8404606a239911258cda52d1603738df0b
PRODUCT_FIXED_TREE = de66c43ecf4a5eb964bf202ac6f870ecc4df7eeb
PRODUCT_FIXED_PARENT = 446b359d3dfcde62c613e1231c5d742a14af582f
MERGE_COUNT = 0
PRODUCT_PATH_COUNT = 7
```

Changed task-owned paths:

```text
tests/run_lsp0_transport_document_sync_check.py
tool/src/diagnostics.rs
tool/src/lib.rs
tool/src/lsp/mod.rs
tool/src/lsp/server.rs
tool/tests/lsp_completion.rs
tool/tests/lsp_diagnostics.rs
```

The shared diagnostic owner reuses `parse_v25`, the existing parser error code/message, and the existing `validate_no_legacy_boim_surface` frontdoor identity. It emits deterministic diagnostics sorted by LSP range then code, with severity, stable message, UTF-16 range, document version, source profile, and snapshot identity. `didOpen` and `didChange` publish the current snapshot; `didClose` publishes an empty set. Version and snapshot identity guards reject stale publication requests.

## D01–D12

```ini
D01_VALID_V25_EMPTY = PASS
D02_LEGACY_EQUALS = PASS / E_V25_DEFINITION_MIGRATION_REQUIRED
D03_LEGACY_BOIM = PASS / E_BOIM_LEGACY_REMOVED frontdoor identity
D04_SYNTAX_ERROR = PASS / existing parser code and message
D05_KOREAN_UTF16 = PASS
D06_EMOJI_UTF16 = PASS
D07_CHANGE_FIXES_ERROR = PASS
D08_CHANGE_PUBLISHES_NEW_VERSION_ERROR = PASS
D09_DETERMINISTIC_ORDER = PASS
D10_DIDCLOSE_EMPTY = PASS
D11_STALE_VERSION_REJECTED = PASS
D12_FRAGMENTED_TRANSPORT = PASS
```

The current base did not require duplicating a later `채비` hardcut. D03 uses the existing frontdoor rejection when present.

## Mutation evidence

The pre-mutation SHA-256 of `tool/src/lsp/server.rs` was:

```text
7865aa2e81e5d1ac44d6dd0a0f3b73083c986019c8ccdee6ad33d37387bf692b
```

### M-D1 — UTF-16 to UTF-8 diagnostic range mutation

Target: `tool/src/lsp/server.rs`, `LspServer::diagnostics_event`.

Exact temporary diff:

```diff
-        let report = analyze_snapshot(snapshot, encoding).map_err(ServerError::Diagnostics)?;
+        let report = analyze_snapshot(snapshot, PositionEncoding::Utf8)
+            .map_err(ServerError::Diagnostics)?;
```

Command:

```text
$env:CARGO_TARGET_DIR='I:\home\urihanl\ddn\codex\build\targets\lsp1-diagnostics'; cargo test -p ddonirang-tool --test lsp_diagnostics d05_d06_utf16_ranges_cover_korean_and_non_bmp -- --nocapture
```

RED 핵심 출력:

```text
assertion `left == right` failed
left:  ... end character 3 ...
right: ... end character 1 ...
test d05_d06_utf16_ranges_cover_korean_and_non_bmp ... FAILED
```

The temporary hunk was removed immediately. Exact restore SHA-256:

```text
7865aa2e81e5d1ac44d6dd0a0f3b73083c986019c8ccdee6ad33d37387bf692b
```

The same focused test then returned `1 passed; 0 failed`.

### M-D2 — document-version binding mutation

Target: `tool/src/lsp/server.rs`, `LspServer::publish_diagnostic_request`.

Exact temporary diff:

```diff
         let snapshot = self
             .documents
             .get(&request.uri)
             .ok_or(PublishRejection::DocumentClosed)?;
-        if snapshot.version != request.version {
-            return Err(PublishRejection::VersionMismatch);
-        }
         if snapshot.identity != request.snapshot_identity {
```

Command:

```text
$env:CARGO_TARGET_DIR='I:\home\urihanl\ddn\codex\build\targets\lsp1-diagnostics'; cargo test -p ddonirang-tool --test lsp_diagnostics d10_close_clears_diagnostics_and_d11_rejects_stale_result -- --nocapture
```

RED 핵심 출력:

```text
assertion `left == right` failed
left: Ok(ServerEvent { ... documentVersion: 2 ... })
right: Err(VersionMismatch)
test d10_close_clears_diagnostics_and_d11_rejects_stale_result ... FAILED
```

The temporary guard removal was restored immediately. Exact restore SHA-256:

```text
7865aa2e81e5d1ac44d6dd0a0f3b73083c986019c8ccdee6ad33d37387bf692b
```

The same focused test then returned `1 passed; 0 failed`.

### M-D3 — didClose empty-publication mutation

Target: `tool/src/lsp/server.rs`, `textDocument/didClose` notification branch.

Exact temporary diff:

```diff
             "textDocument/didClose" => {
                 let uri = self.did_close(params)?;
-                Ok(empty_diagnostics_event(&uri))
+                let _ = uri;
+                Ok(ServerEvent::empty())
             }
```

Command:

```text
$env:CARGO_TARGET_DIR='I:\home\urihanl\ddn\codex\build\targets\lsp1-diagnostics'; cargo test -p ddonirang-tool --test lsp_diagnostics d10_close_clears_diagnostics_and_d11_rejects_stale_result -- --nocapture
```

RED 핵심 출력:

```text
assertion `left == right` failed
left: 0
right: 1
test d10_close_clears_diagnostics_and_d11_rejects_stale_result ... FAILED
```

The temporary branch mutation was restored immediately. Exact restore SHA-256:

```text
7865aa2e81e5d1ac44d6dd0a0f3b73083c986019c8ccdee6ad33d37387bf692b
```

The complete focused diagnostics suite then returned `6 passed; 0 failed`.

## Final verification

```text
cargo test -p ddonirang-tool --test lsp_diagnostics
  6 passed; 0 failed

cargo test -p ddonirang-tool --test lsp0_transport_document_sync
  22 passed; 0 failed

cargo test -p ddonirang-tool --test lsp_completion
  15 passed; 0 failed

python tests/run_lsp0_transport_document_sync_check.py
  LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS
  PROTOCOL_REPEAT=BYTE_STABLE

cargo check -p ddonirang-tool --bin ddonirang-lsp
  Finished `dev` profile

git diff --check
  PASS
```

The existing completion child-process checker and LSP0 black-box checker were updated only to consume and assert the new required `publishDiagnostics` notifications. No parser, runtime, WASM, SSOT, public SPEC, or product semantic path outside the declared owner was changed.

```ini
STALE_PUBLICATION_COUNT = 0
PARTIAL_DOCUMENT_RESULT = 0
DIAGNOSTIC_AFTER_CLOSE = 0
REMOTE_SERVER_DEPENDENCY = 0
SOURCE_UPLOAD = 0
NEW_DEPENDENCY = 0
PROCESS_RESIDUE = 0
PUSH_PERFORMED = NO
```

## Handoff state

```ini
TASK_OWNED_DIRTY = NO after product commit; handoff file is the only new task-owned change
STAGED = handoff file only, before docs-only handoff commit
FOREIGN_DIRTY_TOUCHED = 0
PROTECTED_UNTRACKED_CHANGED = 0
GIT_AUTHOR = tongosu <tongosu@myarts.kr>
GIT_COMMITTER = tongosu <tongosu@myarts.kr>
PROHIBITED_TRAILER_COUNT = 0
PUSH_PERFORMED = NO
READY_FOR_ONE_INDEPENDENT_REVIEW = YES
```

Requested review boundary: bind the single final product target `e4adaa8404606a239911258cda52d1603738df0b` to the evidence in this handoff. This handoff does not claim a full semantic IDE, VSCode extension release, Seamgrim browser behavior, V1 readiness, public support, release, or Human PASS.
