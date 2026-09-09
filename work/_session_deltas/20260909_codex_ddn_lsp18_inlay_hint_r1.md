# DDN-LSP18-CALLABLE-PARAMETER-INLAY-HINTS-R1 handoff

## Authority and custody

- Active unit: `textDocument/inlayHint` callable parameter inlay hints.
- Predecessor LSP17 product: `a29b4a53361a513622cf6f350278a116e66832ef`.
- Predecessor LSP17 handoff: `3c9c7420de5808fe3f6d121c6821b0ed44777393`.
- LSP18 product fixed: `d2046cefd854698327097ccbf4f6f813e479aac8`.
- LSP18 product tree: `0042862044ed70f4ff5db5d4f1457059341fa59a`.
- LSP18 product parent: `3c9c7420de5808fe3f6d121c6821b0ed44777393`.
- No push was performed. No `tool/src/lib.rs`, lang/core, runtime, WASM, SSOT, SPEC, or foreign dirty path was modified or staged.

## Product change

Changed exactly these four paths in the product commit:

```text
tool/src/lsp/signature_help.rs
tool/src/lsp/server.rs
tool/tests/lsp_signature_help.rs
tests/run_lsp0_transport_document_sync_check.py
```

The implementation reuses `DocumentStore` snapshots, existing `collect_body_calls`, parser `BindingReason::Positional`, local callable `ParamPin` identity, and existing UTF-16 position conversion. It emits only resolved positional arguments of a local callable; explicit named/relation arguments, unresolved/ambiguous/malformed calls, strings, comments, unknown documents, and closed documents produce no hints.

The server declares `inlayHintProvider`, handles `textDocument/inlayHint`, binds every result to document version/snapshot identity/source profile, and returns `-32801` or `-32802` for stale version/snapshot. Results are sorted by UTF-16 source position and ParamPin identity. The existing persistent transport checker now verifies response-before-EOF, repeat stability, live snapshot, stale version/snapshot, and didClose empty behavior.

## Verification

Focused command:

```text
cargo test -p ddonirang-tool --test lsp_signature_help --offline -- --nocapture
PASS: 3 passed, 0 failed
```

Persistent transport / black-box command:

```text
$env:CARGO_TARGET_DIR='I:\\home\\urihanl\\ddn\\codex\\build\\lsp18-blackbox-target-20260909'
python tests/run_lsp0_transport_document_sync_check.py
PASS: IH23_BLACKBOX_INLAY_HINT_BEFORE_EOF=PASS
PASS: LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS
```

The complete LSP regression command passed all selected definition, references, rename, document-symbol, open-document-navigation, signature-help, semantic-token, hover, diagnostics, completion, formatting, and document-highlight tests.

Clean snapshot check:

```text
$env:CARGO_TARGET_DIR='I:\\home\\urihanl\\ddn\\codex\\build\\lsp18-clean-target-r1-20260909-02'
cargo check -p ddonirang-tool --offline
PASS: Finished dev profile
```

`git diff --check` passed for all four product paths. The clean snapshot was extracted from the committed LSP17 tree and received only the four current LSP18 paths before the check. Windows tar emitted pre-existing Unicode-path extraction warnings, but the Cargo check completed successfully.

## Mutation evidence

Each mutation was applied alone, tested, restored byte-exactly, and tested GREEN before the next mutation.

### M1 — positional ParamPin swap

Target: `tool/src/lsp/signature_help.rs`, inlay result construction label hunk.

Exact mutation:

```diff
-                label: format!("{}:", param.pin_name),
+                label: format!("{}:", seed.params[1].pin_name),
```

Command:

```text
cargo test -p ddonirang-tool --test lsp_signature_help --offline -- --nocapture
```

RED core output:

```text
assertion `left == right` failed
left: String("오른:")
right: "왼:"
```

Exact restore:

```diff
-                label: format!("{}:", seed.params[1].pin_name),
+                label: format!("{}:", param.pin_name),
```

Restored SHA-256: `955f13fa0cd49c5017a7bca7ec6db656325b86c4c72811dc077f798b91a00d65`.

Restore GREEN: focused test `3 passed, 0 failed`.

### M2 — callable binding removed

Target: `tool/src/lsp/signature_help.rs`, local callable lookup hunk.

Exact mutation:

```diff
-            (seed.canonical_name == candidate.func).then_some(seed)
+            (seed.canonical_name == candidate.func && seed.canonical_name == "not-a-name")
+                .then_some(seed)
```

Command:

```text
cargo test -p ddonirang-tool --test lsp_signature_help --offline -- --nocapture
```

RED core output:

```text
assertion `left == right` failed
left: 0
right: 2
```

Exact restore:

```diff
-            (seed.canonical_name == candidate.func && seed.canonical_name == "not-a-name")
-                .then_some(seed)
+            (seed.canonical_name == candidate.func).then_some(seed)
```

Restored SHA-256: `955f13fa0cd49c5017a7bca7ec6db656325b86c4c72811dc077f798b91a00d65`.

Restore GREEN: focused test `3 passed, 0 failed`.

### M3 — stale snapshot guard removed

Target: `tool/src/lsp/server.rs`, only the `inlay_hints` snapshot identity guard.

Exact mutation:

```diff
-            if requested_identity != snapshot.identity.as_str() {
+            if false && requested_identity != snapshot.identity.as_str() {
```

Command:

```text
cargo test -p ddonirang-tool --test lsp_signature_help --offline -- --nocapture
```

RED core output:

```text
assertion failed: matches!(&stale_snapshot.responses[0], ... error.code == -32802)
```

Exact restore:

```diff
-            if false && requested_identity != snapshot.identity.as_str() {
+            if requested_identity != snapshot.identity.as_str() {
```

Restored SHA-256: `d6c730f798b75a0fc54cd4d8743481c16b535bfc7d17f4aefc603be2fe8f6ff`.

Restore GREEN: focused test `3 passed, 0 failed`.

## Final custody

```makefile
PRODUCT_COMMIT = d2046cefd854698327097ccbf4f6f813e479aac8
PRODUCT_TREE = 0042862044ed70f4ff5db5d4f1457059341fa59a
PRODUCT_PARENT = 3c9c7420de5808fe3f6d121c6821b0ed44777393
AUTHOR = tongosu <tongosu@myarts.kr>
COMMITTER = tongosu <tongosu@myarts.kr>
PROHIBITED_TRAILER_COUNT = 0
NEW_DEPENDENCY = 0
NEW_RUNNER = 0
NEW_META_TEST = 0
SOURCE_UPLOAD = 0
REMOTE_DEPENDENCY = 0
FILESYSTEM_CRAWL = 0
PUSH_PERFORMED = NO
```

Foreign tracked and untracked changes pre-existed in the worktree and were not touched or staged. This handoff is docs-only and is committed separately after the product commit.
