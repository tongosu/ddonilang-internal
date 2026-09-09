# DDN-LSP25 open-document cross-file references — handoff R1

## Authority

```makefile
BASE_PRODUCT = 07d62f47fbaec5320e89cd568438b3538712cbbb
BASE_HANDOFF = 95b1471e6a9a5485b56185bb721dbe407632acec
LSP24_REVIEW = PASS_TARGET_BOUND
LSP24_STATUS = CLOSED_TARGET_BOUND
LSP25_STATUS = PRODUCT_FIXED_PENDING_REVIEW
LIVE_AUTHORITY = v25.69.0, no impact on LSP25
SHARED_SYMBOL_OWNER = tool/src/lsp/symbol.rs
OPEN_DOCUMENT_ONLY = YES
FILESYSTEM_CRAWL = 0
REMOTE_DEPENDENCY = 0
SOURCE_UPLOAD = 0
TOOL_SRC_LIB_RS_CHANGED = 0
NEW_DEPENDENCY = 0
```

The existing `DocumentStore`, `resolve_symbol_across_documents`, and local
reference owner are reused. No parser, regex semantic owner, workspace index,
filesystem fallback, or remote service was added.

## Product commit

```makefile
LSP25_PRODUCT_TARGET = 9f63ab7bbbfe49eaec166c9ea5b7989e1770ad8e
LSP25_PRODUCT_TREE = db59d513f67ebeb1c51acfdb64ceb44f6be27deb
LSP25_PRODUCT_PARENT = 95b1471e6a9a5485b56185bb721dbe407632acec
MERGE_COUNT = 0
PRODUCT_PATHS = tool/src/lsp/server.rs, tool/tests/lsp_references.rs
PRODUCT_PATH_COUNT = 2
UNEXPECTED_PATHS = 0
AUTHOR = tongosu <tongosu@myarts.kr>
COMMITTER = tongosu <tongosu@myarts.kr>
PROHIBITED_TRAILER_COUNT = 0
```

The product hunk adds bounded reference publication and cancellation checks.
Tests cover declaration inclusion, deterministic URI/source order,
Korean/emoji UTF-16 ranges, didChange snapshots, didClose removal, stale
version/snapshot identity rejection, unopened-file exclusion, duplicate
identity fail-closed behavior, deterministic repeat, and the 1000-location
bound.

## Validation

```makefile
CROSS_FILE_REFERENCES = PASS
INCLUDE_DECLARATION = PASS
DIDCHANGE_CURRENT_SNAPSHOT = PASS
DIDCLOSE_REMOVAL = PASS
STALE_VERSION = PASS, -32801
STALE_SNAPSHOT = PASS, -32802
IDENTITY_COLLISION = PASS, empty result
UTF16_RANGE = PASS
URI_AND_SOURCE_ORDER = PASS
RESULT_BOUND = PASS, 1000
CANCELLATION_ATOMICITY = PASS, -32800
FILESYSTEM_UNOPENED = PASS
```

```text
cargo test -p ddonirang-tool --test lsp_references
4 passed; 0 failed

lsp_references, lsp_definition, lsp_rename, lsp_document_symbol,
lsp_hover, lsp_diagnostics, lsp_completion regression = PASS

R14_BLACKBOX_REFERENCES_BEFORE_EOF = PASS
ST20_BLACKBOX_OPEN_DOCUMENT_NAVIGATION_BEFORE_EOF = PASS
LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK = PASS

cargo check -p ddonirang-tool --bin ddonirang-lsp --offline = PASS
git diff --check = PASS
```

## Mutation evidence

Final restored identities before product commit:

```makefile
SERVER_RESTORED_SHA256 = 56f9a7f7741d3a07844097f4c5d2764e8ef961a525e5391508772d565b4b8e96
SERVER_RESTORED_BLOB = 58fc6701032e1cb1cc727ff951fce4b8915b1de7
TEST_RESTORED_SHA256 = 76d0189ac8440aa05736a6bf640fef4cc1da69b39b81d9d7d8e10eb2911c913c
TEST_RESTORED_BLOB = 004fe619449220e4445ca37f62609a975e0ac2fc
```

### M1 — cross-document search regressed to same-document

Target: `tool/src/lsp/server.rs`, reference location loop.

```diff
-        for (target_uri, target) in self.documents.iter() {
+        for (target_uri, target) in self
+            .documents
+            .iter()
+            .filter(|(target_uri, _)| *target_uri == uri)
+        {
```

Command:

```text
cargo test -p ddonirang-tool --test lsp_references lsp25_open_document_cross_file_references_contract -- --exact --quiet
```

RED: URI list was `["file:///lsp25-b.ddn"]` instead of
`["file:///lsp25-a.ddn", "file:///lsp25-b.ddn", "file:///lsp25-c.ddn"]`.

```makefile
EXACT_RESTORE = PASS
RESTORE_SHA256 = 56f9a7f7741d3a07844097f4c5d2764e8ef961a525e5391508772d565b4b8e96
RESTORE_BLOB = 58fc6701032e1cb1cc727ff951fce4b8915b1de7
GREEN = lsp_references, 4 passed; 0 failed
RESIDUE = 0
```

### M2 — stale version guard removed

Target: `tool/src/lsp/server.rs`, references version guard.

```diff
-            if requested_version != snapshot.version {
+            if false {
```

Command:

```text
cargo test -p ddonirang-tool --test lsp_references i02_change_stale_malformed_and_close_empty -- --exact --quiet
```

RED: the existing stale request assertion for `-32801` failed because the
request entered the success path.

```makefile
EXACT_RESTORE = PASS
RESTORE_SHA256 = 56f9a7f7741d3a07844097f4c5d2764e8ef961a525e5391508772d565b4b8e96
RESTORE_BLOB = 58fc6701032e1cb1cc727ff951fce4b8915b1de7
GREEN = lsp_references, 4 passed; 0 failed
RESIDUE = 0
```

### M3 — UTF-16 range downgraded to UTF-8

Target: `tool/src/lsp/server.rs`, reference location range conversion.

```diff
-                let range = super::position::byte_range_to_lsp_range(source, range, encoding)
+                let range = super::position::byte_range_to_lsp_range(
+                    source,
+                    range,
+                    PositionEncoding::Utf8,
+                )
```

Command:

```text
cargo test -p ddonirang-tool --test lsp_references lsp25_open_document_cross_file_references_contract -- --exact --quiet
```

RED: emoji-bearing range became `56..68` instead of UTF-16 `32..36`.

```makefile
EXACT_RESTORE = PASS
RESTORE_SHA256 = 56f9a7f7741d3a07844097f4c5d2764e8ef961a525e5391508772d565b4b8e96
RESTORE_BLOB = 58fc6701032e1cb1cc727ff951fce4b8915b1de7
GREEN = lsp_references, 4 passed; 0 failed
RESIDUE = 0
```

## Final custody

```makefile
TASK_OWNED_DIRTY = 0 before handoff docs commit
STAGED = 0 after product commit
FOREIGN_DIRTY_TOUCHED = 0
PROTECTED_UNTRACKED_CHANGED = 0
PROCESS_RESIDUE = 0
PUSH = NO
READY_FOR_INDEPENDENT_REVIEW = YES
NEXT_AUTONOMOUS_UNIT = LSP26 call-hierarchy open-document completeness mapping only
```

LSP24 review PASS was bound to its exact target and was not rerun. Foreign
tracked/untracked changes remain untouched and were not staged, formatted,
reset, or committed.
