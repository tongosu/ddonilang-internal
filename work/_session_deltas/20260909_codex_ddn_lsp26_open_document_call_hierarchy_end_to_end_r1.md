# DDN-LSP26 OPEN-DOCUMENT CALL HIERARCHY — HANDOFF R1

## Authority and target

- `CURRENT_UNIT = LSP26_OPEN_DOCUMENT_CALL_HIERARCHY`
- `BASE_PRODUCT = 9f63ab7bbbfe49eaec166c9ea5b7989e1770ad8e`
- `BASE_HANDOFF = 56a818adca5d7d958973cf7817f2e177a4d7c264`
- `LSP25_REVIEW = PASS_TARGET_BOUND`
- `LSP25_STATUS = CLOSED_TARGET_BOUND`
- `PRODUCT_COMMIT = f41fe8bc14ba81212be286d91dee0e65c4321df0`
- `PRODUCT_TREE = 6d1978202b874f5139ba9acb68d0bd89ccd393ba`
- `PRODUCT_PARENT = 56a818adca5d7d958973cf7817f2e177a4d7c264`

## Product behavior

The existing `DocumentStore` and `tool/src/lsp/symbol.rs` callable/symbol owner remain authoritative. The server now provides bounded and cancellation-aware call hierarchy traversal for open documents only.

- `textDocument/prepareCallHierarchy`, `callHierarchy/incomingCalls`, and `callHierarchy/outgoingCalls` remain advertised and wired.
- Same-document and cross-open-document caller/callee edges use existing `DefinitionIdentity` resolution.
- `didChange` uses the current snapshot; stale version and stale snapshot payloads fail closed; `didClose` removes the document from traversal.
- Existing source-order and URI ordering are preserved, including Korean and emoji UTF-16 ranges.
- Call hierarchy result ranges are bounded to 1,000 and edge traversal is bounded to 10,000.
- Cancellation checks reject the request with `-32800` before a success response; no partial success is published.
- Filesystem crawl/read, remote dependency, source upload, hidden workspace index, and duplicate semantic owner remain absent.

Changed product paths:

```text
tool/src/lsp/server.rs
tool/tests/lsp_open_document_navigation.rs
```

## Verification

Focused call hierarchy:

```text
cargo test -p ddonirang-tool --test lsp_open_document_navigation
9 passed, 0 failed
```

The focused suite covers capability, same-document and cross-document incoming/outgoing calls, deterministic repeat, duplicate identity rejection, current snapshot lifecycle, Korean/emoji UTF-16 ranges, bounded ranges, stale prepare `-32801`, and cancellation `-32800`.

Selected LSP regressions:

```text
lsp_signature_help       3 passed
lsp_definition           3 passed
lsp_references           4 passed
lsp_rename               5 passed
lsp_document_symbol      4 passed
lsp_completion          15 passed
lsp_diagnostics         10 passed
lsp_semantic_tokens      3 passed
```

Persistent transport:

```text
python tests/run_lsp0_transport_document_sync_check.py
ST20_BLACKBOX_OPEN_DOCUMENT_NAVIGATION_BEFORE_EOF=PASS
LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS
```

Offline build and formatting checks:

```text
cargo check -p ddonirang-tool --bin ddonirang-lsp --offline = PASS
git diff --check = PASS
```

## Mutation evidence

All mutations were applied one at a time to the product source, were not staged or committed, and were immediately restored.

### M1 — cross-file edge regressed to same-document only

Exact temporary diff in `tool/src/lsp/server.rs`:

```diff
                 let Some(callee) = unique.get(&callee_identity) else {
                     continue;
                 };
+                if callee.uri != snapshot.uri {
+                    continue;
+                }
                 edges.push((caller.clone(), callee.clone(), call.range));
```

Command:

```text
cargo test -p ddonirang-tool --test lsp_open_document_navigation lsp15_call_hierarchy_is_open_document_bound_and_deterministic -- --exact --quiet
```

Expected/actual RED:

```text
assertion failed: incoming result count
left: 1
right: 2
```

Exact restore:

```text
restore SHA-256 = a142d38bf1a3fddb7b06bcce49f45611aca5decb0e72c65e56d8e12ee9142e86
restore blob     = 563fc66335481dde515b9514b8d6604593653f00
```

Restore GREEN: full focused call-hierarchy suite `9 passed, 0 failed`.

### M2 — stale prepare version guard removed

Exact temporary diff in `tool/src/lsp/server.rs`:

```diff
         if let Some(requested_version) = document.get("version").and_then(Value::as_i64) {
-            if requested_version != snapshot.version {
+            if false && requested_version != snapshot.version {
```

Command:

```text
cargo test -p ddonirang-tool --test lsp_open_document_navigation lsp26_call_hierarchy_is_bounded_and_cancellable -- --exact --quiet
```

Expected/actual RED:

```text
assertion failed: stale_prepare error code
```

Exact restore:

```text
restore SHA-256 = a142d38bf1a3fddb7b06bcce49f45611aca5decb0e72c65e56d8e12ee9142e86
restore blob     = 563fc66335481dde515b9514b8d6604593653f00
```

Restore GREEN: full focused call-hierarchy suite `9 passed, 0 failed`.

### M3 — UTF-16 call range calculation downgraded to UTF-8

Exact temporary diff in `tool/src/lsp/server.rs`:

```diff
     let range =
-        super::position::byte_range_to_lsp_range(source, range, encoding).map_err(|error| {
+        super::position::byte_range_to_lsp_range(source, range, PositionEncoding::Utf8).map_err(|error| {
```

Command:

```text
cargo test -p ddonirang-tool --test lsp_open_document_navigation lsp15_call_hierarchy_is_open_document_bound_and_deterministic -- --exact --quiet
```

Expected/actual RED:

```text
assertion failed: emoji UTF-16 call range
left: Number(34)
right: 20
```

Exact restore:

```text
restore SHA-256 = a142d38bf1a3fddb7b06bcce49f45611aca5decb0e72c65e56d8e12ee9142e86
restore blob     = 563fc66335481dde515b9514b8d6604593653f00
```

Restore GREEN: full focused call-hierarchy suite `9 passed, 0 failed`.

## Custody

```makefile
TOOL_SRC_LIB_RS_CHANGED = 0
PUBLIC_LANGUAGE_CHANGED = 0
CLI_WASM_CHANGED = 0
VSCODE_PACKAGING_CHANGED = 0
FILESYSTEM_CRAWL = 0
REMOTE_DEPENDENCY = 0
SOURCE_UPLOAD = 0
PUSH = NO
AUTHOR = tongosu <tongosu@myarts.kr>
COMMITTER = tongosu <tongosu@myarts.kr>
PROHIBITED_TRAILER_COUNT = 0
```

Foreign tracked dirty paths and protected untracked material were not modified, formatted, staged, or committed. No server process residue was left by the verification run.

## Next safe unit

LSP26 is fixed and ready for one independent review. The next unit should be selected only from an already typed, shared-owner LSP workflow; no LSP24 or LSP25 reimplementation is required.
