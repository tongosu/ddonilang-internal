# DDN-LSP12 Open-Document Workspace Symbol — Handoff R1

## Binding

- Unit: `LSP12_OPEN_DOCUMENT_WORKSPACE_SYMBOL`
- Implementation base: `26445d7f4f372d59f323eb7c2eb930e4ea22ffb4`
- LSP11 predecessor: product `48886c30e032a98e46bb4a71edfe4628a9b54386`, runner correction `fe333ffe875375d4bcc94cb325fbc685cfc360ba`, handoff `26445d7f4f372d59f323eb7c2eb930e4ea22ffb4`
- Product commit: `cb4aafef7f4f9bc32522b1708e4eabc684f1f9f1`
- Product tree: `b29e75c85de184941bcb9abd290d1f4fe118b359`
- Product parent: `26445d7f4f372d59f323eb7c2eb930e4ea22ffb4`
- Review state: `IMPLEMENTED_PENDING_REVIEW`; no LSP12 independent PASS is claimed.

## Product scope

Changed exactly these three task-owned paths:

1. `tool/src/lsp/server.rs`
   - Added `workspaceSymbolProvider: true` to initialize capabilities.
   - Routed `workspace/symbol` to a server method.
   - Reused `DocumentStore` open-document snapshots and `document_symbols_snapshot`.
   - Closed, malformed, stale version, or stale snapshot metadata returns `[]`.
   - Enumerated the `BTreeMap` open-document owner in lexical URI order; symbol order remains existing source order.
   - Reused existing negotiated-position range conversion.
   - Preserved symbol identity, current document version, snapshot identity, and source profile in result data.
   - Enforced `MAX_WORKSPACE_SYMBOLS = 1000`.
2. `tool/tests/lsp_document_symbol.rs`
   - Added multi-URI workspace-symbol coverage for capability, query, repeat stability, current version after didChange, duplicate identities, didClose exclusion, and stale/closed snapshot metadata.
3. `tests/run_lsp0_transport_document_sync_check.py`
   - Extended the existing runner with `WS21_BLACKBOX_WORKSPACE_SYMBOL_BEFORE_EOF`.
   - No new runner or dependency was created.

No `tool/src/lib.rs`, language, runtime, WASM, Workbench, or foreign dirty path was changed.

## Exact mutation evidence

All mutations were applied one at a time, never staged, and restored immediately.

### M1 — closed-document retention guard

Target hunk in `tool/src/lsp/server.rs`:

```diff
                 let Some(snapshot) = self.documents.get(uri) else {
-                    return Ok(success_event(id, json!([])));
+                    continue;
                 };
```

Command:

```text
cargo test -p ddonirang-tool --test lsp_document_symbol lsp12_workspace_symbol_is_open_document_bounded_and_snapshot_bound --offline --quiet
```

RED 핵심 출력:

```text
assertion `left == right` failed
left: [workspace-a symbol]
right: []
```

Exact restore: the original `return Ok(success_event(id, json!([])));` hunk was restored. `server.rs` SHA-256 returned to `0EE9BD07E0889B0563B95B519AAD98D57FB2F34B860B650B5478445B6027016A`.

GREEN: `1 passed; 0 failed`.

### M2 — nondeterministic URI order

Target hunk in `tool/src/lsp/server.rs`:

```diff
-        for (uri, snapshot) in self.documents.iter() {
+        let mut documents = self.documents.iter().collect::<Vec<_>>();
+        documents.reverse();
+        for (uri, snapshot) in documents {
```

Command: same focused workspace-symbol command above.

RED 핵심 출력:

```text
assertion `left == right` failed
left: "file:///workspace-b.ddn"
right: "file:///workspace-a.ddn"
```

Exact restore: the original `for (uri, snapshot) in self.documents.iter()` hunk was restored. `server.rs` SHA-256 returned to `0EE9BD07E0889B0563B95B519AAD98D57FB2F34B860B650B5478445B6027016A`.

GREEN: `1 passed; 0 failed`.

### M3 — stale snapshot guard bypass

Target hunk in `tool/src/lsp/server.rs`:

```diff
-                if requested.get("version").and_then(Value::as_i64) != Some(snapshot.version)
-                    || requested.get("snapshotIdentity").and_then(Value::as_str)
-                        != Some(snapshot.identity.as_str())
-                {
+                if false {
```

Command: same focused workspace-symbol command above.

RED 핵심 출력:

```text
assertion `left == right` failed
left: [current symbols for A and B]
right: []
```

Exact restore: the original version and snapshot-identity comparisons were restored. `server.rs` SHA-256 returned to `0EE9BD07E0889B0563B95B519AAD98D57FB2F34B860B650B5478445B6027016A`.

GREEN: `1 passed; 0 failed`.

## Verification

Focused workspace-symbol test:

```text
cargo test -p ddonirang-tool --test lsp_document_symbol lsp12_workspace_symbol_is_open_document_bounded_and_snapshot_bound --offline --quiet
1 passed; 0 failed
```

Existing LSP regression group:

```text
cargo test -p ddonirang-tool --test lsp_document_symbol --test lsp_open_document_navigation --test lsp_rename --test lsp_definition --test lsp_references --test lsp_document_highlight --test lsp_signature_help --test lsp_semantic_tokens --test lsp_hover --test lsp_diagnostics --test lsp_completion --offline --quiet
all listed test groups passed
```

Persistent transport / black-box checker:

```text
python tests/run_lsp0_transport_document_sync_check.py
WS21_BLACKBOX_WORKSPACE_SYMBOL_BEFORE_EOF=PASS
LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS
```

Clean validation snapshot:

```text
git archive cb4aafef -- Cargo.toml Cargo.lock .cargo core lang numeric proof symbolic tool tests
cargo check --manifest-path I:\home\urihanl\ddn\codex\build\lsp12-clean-snapshot-r1\tool\Cargo.toml --bin ddonirang-lsp --offline
Finished `dev` profile
```

```text
git diff --check -- tool/src/lsp/server.rs tool/tests/lsp_document_symbol.rs tests/run_lsp0_transport_document_sync_check.py
PASS
```

Final task-file SHA-256:

```text
tool/src/lsp/server.rs = 0EE9BD07E0889B0563B95B519AAD98D57FB2F34B860B650B5478445B6027016A
tool/tests/lsp_document_symbol.rs = 98B0E4E870F25246AFD5A5B2C1C7FCB1B1156668ACE2B2FDE52D14CF75487B3F
tests/run_lsp0_transport_document_sync_check.py = 6DF00117B9B24C2D96A0C3562FFEE0EE148EDF01E7BCD2DCDD5281D1678686A2
```

## Custody

- New dependency: `0`
- New pack: `0`
- New runner: `0`; existing runner extended
- Filesystem crawl: `0`
- Source upload / remote dependency: `0 / 0`
- Foreign dirty touched: `0`
- Protected untracked changed: `0`
- Push: `NO` at this handoff stage
- Author and committer: `tongosu <tongosu@myarts.kr>`
- Prohibited trailer count: `0`

Next safe unit remains deferred until the LSP12 review boundary is recorded; no LSP13 implementation was started in this unit.
