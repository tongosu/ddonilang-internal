# DDN-LSP20-PULL-DIAGNOSTICS-OPEN-DOCUMENTS-R1 — handoff

## Identity

- Previous LSP19 product: `12e9434d893ee402e26a03a3d7a75edfa1d79d9a`
- Previous LSP19 handoff: `fbf14a3ae6778a58115a51ab330611cffed8635a`
- LSP20 implementation base: `fbf14a3ae6778a58115a51ab330611cffed8635a`
- LSP20 product commit: `f0af222d` (full identity recorded after commit)
- LSP20 scope: open-document pull diagnostics only; existing push diagnostics remains the semantic owner.

## Product changes

- `tool/src/lsp/server.rs`
  - advertises LSP 3.17 `diagnosticProvider` with `identifier = ddonirang-v25`, inter-file and workspace diagnostics enabled;
  - routes `textDocument/diagnostic` and `workspace/diagnostic`;
  - returns full/unchanged document reports and workspace reports from current `DocumentStore` snapshots only;
  - derives deterministic result IDs from URI, version, snapshot identity, and the exact shared diagnostic payload;
  - keeps push `publishDiagnostics` and pull diagnostics on the same `diagnostic_values` owner;
  - rejects stale document version/snapshot identity, unknown documents, and cancelled requests without partial output.
- `tool/tests/lsp_diagnostics.rs`
  - adds capability, push/pull parity, result reuse, didChange refresh, stale rejection, workspace URI order, didClose exclusion, UTF-16 Korean/emoji, and cancellation coverage.
- `tests/run_lsp0_transport_document_sync_check.py`
  - extends the existing persistent transport black-box runner with pull/workspace diagnostics and response-before-EOF coverage.

No `tool/src/lib.rs`, `lang/**`, `core/**`, public CLI/WASM/UI, SSOT, SPEC, dependency, pack, or new runner was changed.

## Mutation evidence

Each mutation was applied alone, tested immediately, and byte-exactly restored before the next mutation.

### M1 — snapshot identity removed from result ID

- Target/hunk: `tool/src/lsp/server.rs`, `diagnostic_result_id`, the final `format!("sha256:{:x}:{}", ..., snapshot.identity.as_str())` binding.
- Pre-mutation SHA-256: `48AB7E45FD6C1D8D559F4189C52BEB8A780F2078F1705FDFA43A20B9B98A861F`
- Temporary mutation: result ID was reduced to `format!("sha256:{:x}", hasher.finalize())`.
- RED command: `cargo test -p ddonirang-tool --test lsp_diagnostics d13_pull_diagnostics_reuses_push_payload_and_result_id`
- RED: `assertion failed: result_id.ends_with(&format!(":{snapshot_identity}"))`.
- Restore: original final format restored; SHA-256 returned to `48AB7E45FD6C1D8D559F4189C52BEB8A780F2078F1705FDFA43A20B9B98A861F`.
- GREEN: same focused test passed.

### M2 — closed document retained

- Target/hunk: `tool/src/lsp/document_store.rs`, `DocumentStore::close`, `remove(uri)`.
- Pre-mutation SHA-256: `B2D1B815CFFBD609C1C8D01D55F9CAE3D7F62FE17156D661F846F203DE9BFA87`
- Temporary mutation: `remove(uri)` was changed to `get(uri).cloned()`.
- RED command: `cargo test -p ddonirang-tool --test lsp_diagnostics d15_workspace_pull_is_open_only_and_uri_deterministic`
- RED: expected one workspace item after close, observed two (`left: 2`, `right: 1`).
- Restore: `remove(uri)` restored; SHA-256 returned to `B2D1B815CFFBD609C1C8D01D55F9CAE3D7F62FE17156D661F846F203DE9BFA87`.
- GREEN: same focused test passed.

### M3 — push/pull diagnostic owner split

- Target/hunk: `tool/src/lsp/server.rs`, `diagnostics_notification` shared payload call.
- Pre-mutation SHA-256: `48AB7E45FD6C1D8D559F4189C52BEB8A780F2078F1705FDFA43A20B9B98A861F`
- Temporary mutation: push notification removed `source` from its first diagnostic after `diagnostic_values`, leaving pull on the shared payload.
- RED command: `cargo test -p ddonirang-tool --test lsp_diagnostics d13_pull_diagnostics_reuses_push_payload_and_result_id`
- RED: push/pull arrays differed because push lacked `source: "ddonirang-v25"`.
- Restore: notification returned to `let diagnostics = diagnostic_values(snapshot, report)`; SHA-256 returned to `48AB7E45FD6C1D8D559F4189C52BEB8A780F2078F1705FDFA43A20B9B98A861F`.
- GREEN: same focused test passed.

## Verification

- `cargo test -p ddonirang-tool --test lsp_diagnostics` — 10/10 PASS.
- `python -m py_compile tests/run_lsp0_transport_document_sync_check.py` — PASS.
- `python tests/run_lsp0_transport_document_sync_check.py` — PASS; includes `ST23_BLACKBOX_PULL_DIAGNOSTICS_BEFORE_EOF=PASS`, existing transport/LSP checks PASS, final `LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS`.
- `cargo check -p ddonirang-tool` — PASS.
- `git diff --check` — PASS.

## Boundary

- open-document source only; no filesystem crawl, closed-document cache, remote dependency, upload, or workspace index.
- product author/committer: `tongosu <tongosu@myarts.kr>`.
- prohibited AI/co-author trailers: 0.
- push performed: NO.
- foreign dirty paths were not touched or staged.

