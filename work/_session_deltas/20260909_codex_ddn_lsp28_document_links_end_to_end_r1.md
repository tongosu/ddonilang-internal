# DDN-LSP28 — Open-Document Document Links End-to-End Handoff

## Authority and custody

```makefile
AI_PROVIDER = OpenAI
AI_SURFACE = Codex Work
SESSION_NICKNAME = 또니LSP완결 Work
PROJECT_ROLE = DDN LSP Product Single Writer
RETURN_LABEL = [DDN LSP-0 전용 구현 -> 또니랑 개발 관리자 Work]
LIVE_AUTHORITY = existing v25.69.0 typed parser, Lexer, DocumentStore, and LSP position owners; SSOT/SPEC unchanged
BASE_PRODUCT = 591649789b02f374b3dbeb75fee2f427e98a8dbb
BASE_TREE = f32655166d7b4faac3b90cc4a8ec04b2dec2cf4c
PRODUCT_COMMIT = 47d6465db91cda5dca32ef16df4e2ac4a3433b41
PRODUCT_TREE = b4cb90d64e3bf8ffb784af6a3bd68ffb5e5a057d
PRODUCT_PARENT = 591649789b02f374b3dbeb75fee2f427e98a8dbb
MERGE_COUNT = 0
PRODUCT_PATHS = tool/src/lsp/document_link.rs, tool/src/lsp/mod.rs, tool/src/lsp/server.rs, tool/tests/lsp_open_document_navigation.rs
TOOL_SRC_LIB_RS_CHANGED = 0
NEW_DEPENDENCY = 0
FILESYSTEM_CRAWL = 0
REMOTE_DEPENDENCY = 0
SOURCE_UPLOAD = 0
PUBLIC_SPEC_CHANGE = 0
PUSH_PERFORMED = NO
```

LSP26 and LSP27 remain predecessor product units and were not rewritten or
retested as new implementations. LSP28 is the third unit in the autonomous
closure and is pending one independent review bound to its exact product and
handoff targets.

## LSP28 implementation

The selected safe candidate was document links using explicit current resource
targets. The implementation reuses the existing V25 parser/lexer admission,
`DocumentStore` current snapshot, and UTF-16 byte-range owner. A valid explicit
`@"relative/resource"` literal produces a `textDocument/documentLink` result;
comments, ordinary strings, malformed source, unsafe absolute/parent-traversal
paths, closed documents, and stale snapshots do not produce a link. The target
URI is derived from the current document URI without reading the filesystem.

Implemented behavior:

- initialize advertises `documentLinkProvider` with `resolveProvider=false`.
- only the open document named by the request is inspected.
- ranges cover the explicit `@"..."` source bytes and are serialized through
  the existing UTF-16 position conversion.
- relative resource path bytes are URI-encoded deterministically, including
  Korean and non-BMP characters.
- current didChange snapshots are used; didClose returns an empty result.
- version mismatch returns `-32801`; snapshot identity mismatch returns
  `-32802`; cancellation returns `-32800` without partial success.
- output is bounded at `MAX_DOCUMENT_LINKS = 1000`.
- no new parser, identity owner, registry, filesystem read, crawler, upload,
  dependency, packaging change, or `tool/src/lib.rs` change was made.

## Verification

```makefile
FOCUSED_TEST = cargo test -p ddonirang-tool --test lsp_open_document_navigation lsp28_document_links_are_typed_open_document_resource_targets = PASS
LSP27_NAVIGATION_REGRESSION = cargo test -p ddonirang-tool --test lsp_open_document_navigation = 11/11 PASS
LSP_REGRESSIONS = lsp_completion, lsp_definition, lsp_references, lsp_rename, lsp_document_symbol, lsp_diagnostics, lsp_semantic_tokens, lsp_signature_help, lsp_hover, lsp_document_highlight = PASS
BLACKBOX_BEFORE_EOF = python tests/run_lsp0_transport_document_sync_check.py = PASS
BLACKBOX_RESULT = LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS
CARGO_CHECK = cargo check -p ddonirang-tool --bin ddonirang-lsp --offline = PASS
DIFF_CHECK = git diff --check = PASS
PROCESS_RESIDUE = 0
```

The focused test covers capability advertisement, explicit resource link
range, Korean/non-BMP URI encoding, deterministic repeat, didChange refresh,
malformed source rejection, parent traversal rejection, stale version and
snapshot rejection, cancellation, and didClose removal. Existing transport
black-box coverage remains green for initialize, fragmentation, persistent
connection, and all previously supported LSP responses.

The product-fixed full package validation was:

```makefile
COMMAND = cargo test -p ddonirang-tool --quiet
RESULT = 635 passed, 2 failed
FAILURES = ai_prompt::tests::ai_prompt_output_invariants_hold; ai_prompt::tests::ai_prompt_output_matches_golden
CLASS = NONBLOCKING_PREEXISTING_ENVIRONMENT_FAILURE
CAUSE = worktree docs/ssot directory is absent
PRODUCT_RELEVANCE = none; no LSP, AI-prompt, or SSOT path was changed
```

## Mutation evidence

Each mutation was applied alone, run against the existing focused test, restored
immediately, and followed by the restored GREEN test. No mutation was staged or
committed.

### M1 — parser/source validity guard removal

Target: `tool/src/lsp/document_link.rs`, `document_links_snapshot`.

Exact temporary diff:

```diff
-    if parse_v25(source, &snapshot.uri).is_err() {
+    if false && parse_v25(source, &snapshot.uri).is_err() {
```

RED: `lsp28_document_links_are_typed_open_document_resource_targets` returned
one link for malformed source `그림:글 := @"assets/broken.png" + .`, while the
focused assertion required `[]`.

Exact restore:

```makefile
RESTORE_SHA256 = 3E430053BB35CA18D4185D77817C26DD3A5FF297359AE2D62D0F104B60D82BC9
RESTORE_BLOB = 1d620ddef6b0a294c683c6d845ac115e8cb023b1
```

GREEN: the same focused test passed after restore.

### M2 — unsafe relative-resource guard removal

Target: `tool/src/lsp/document_link.rs`, safe relative resource admission.

Exact temporary diff:

```diff
-        if !matches!(at.kind, TokenKind::At) || !safe_relative_resource(resource_path) {
+        if !matches!(at.kind, TokenKind::At) {
```

RED: the focused test returned `file:///workspace/../secret.png` for
`@"../secret.png"`, while the fail-closed assertion required `[]`.

Exact restore:

```makefile
RESTORE_SHA256 = 3E430053BB35CA18D4185D77817C26DD3A5FF297359AE2D62D0F104B60D82BC9
RESTORE_BLOB = 1d620ddef6b0a294c683c6d845ac115e8cb023b1
```

GREEN: the same focused test passed after restore.

### M3 — stale-version guard removal

Target: `tool/src/lsp/server.rs`, `document_links` requested-version guard.

Exact temporary diff:

```diff
-            if requested_version != snapshot.version {
+            if false && requested_version != snapshot.version {
```

RED: the focused test accepted a request at version `1` after the document had
advanced to version `2`; the expected `-32801` response was absent.

Exact restore:

```makefile
RESTORE_SHA256 = 434AD78F48C9C8CF76FD1055FA17ACEE1FD7B0C2BB87C7DBB45789F9259CD948
RESTORE_BLOB = 5e3b6fcec54c906e977d698c46a6881fd21b0120
```

GREEN: the same focused test passed after restore.

## Handoff

```makefile
HANDOFF_FILE = work/_session_deltas/20260909_codex_ddn_lsp28_document_links_end_to_end_r1.md
HANDOFF_COMMIT = pending
HANDOFF_PARENT = 47d6465db91cda5dca32ef16df4e2ac4a3433b41
AUTHOR = tongosu <tongosu@myarts.kr>
COMMITTER = tongosu <tongosu@myarts.kr>
PROHIBITED_TRAILER_COUNT = 0
FOREIGN_DIRTY_TOUCHED = 0
PROTECTED_UNTRACKED_CHANGED = 0
```

LSP28 is `PRODUCT_FIXED_PENDING_REVIEW`. LSP26, LSP27, and LSP28 are the three
new product units fixed in this autonomous closure and are ready for one
independent review bound to their exact targets. No public push, VSIX rebuild,
packaging change, product promotion, or SSOT change was performed.

```makefile
READY_FOR_INDEPENDENT_REVIEW = LSP26, LSP27, LSP28 exact product/handoff targets
NEXT_AUTONOMOUS_UNIT = none; wait for the single independent review
GOAL_STATUS = PASS_THREE_NEW_LSP_PRODUCT_UNITS_FIXED_PENDING_REVIEW
```
