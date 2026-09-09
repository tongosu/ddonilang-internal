# DDN-LSP2-SHARED-HOVER-IDENTITY-R1 — 결과

## 작업 계약

- 작업면: 현재 LSP single writer
- base: `e3c4cf24c4226bda6dd6319dffed55036941a503`
- base tree: `2a44865b92a6513492416b84a1616f2718b30284`
- 제품 범위: `tool/src/**`의 shared hover owner와 기존 LSP server wiring, focused test, 기존 black-box checker extension
- 금지 범위: `lang/**`, `core/**`, WASM/UI, SSOT/SPEC, pack, teul-cli, foreign dirty
- LSP0 transport/document sync, completion, diagnostics는 재구현하지 않고 회귀만 확인했다.

## 제품 결과

- product commit: `ef34c931c447ff768a602276dbe5e5fd8d7f7678`
- product tree: `1788cf054726a7148241d68e2a64909091a44b31`
- product parent: `e3c4cf24c4226bda6dd6319dffed55036941a503`
- merge count: 0
- changed paths:
  - `tests/run_lsp0_transport_document_sync_check.py`
  - `tool/src/hover.rs`
  - `tool/src/lib.rs`
  - `tool/src/lsp/mod.rs`
  - `tool/src/lsp/server.rs`
  - `tool/tests/lsp_hover.rs`
- unexpected product paths: 0
- duplicate parser/registry/formatter implementations: 0
- new dependency/pack/runner/meta-test: 0/0/0/0

## H01–H12

- H01 PASS: initialize capability advertises `hoverProvider: true`.
- H02 PASS: local immutable definition hover returns `definition:local:<name>`.
- H03 PASS: local callable reference resolves to the same local identity.
- H04 PASS: registered stdlib callable hover returns `definition:stdlib:<name>`.
- H05 PASS: v25 canonical signature/source profile is returned; pseudo-source `<...>` is absent.
- H06 PASS: whitespace, unknown, and punctuation return JSON null.
- H07 PASS: Korean UTF-16 position/range is exact.
- H08 PASS: emoji-preceded non-BMP UTF-16 position/range is exact.
- H09 PASS: didChange uses the current snapshot and stale version `-32801` is rejected.
- H10 PASS: didClose clears hover and returns JSON null.
- H11 PASS: repeated identical hover responses are byte-stable.
- H12 PASS: fragmented transport processes initialize before EOF and returns hover before EOF.

## Mutation evidence

Final product baseline for each mutation:

- target: `tool/src/lsp/server.rs`
- restore SHA-256: `58f2636249673a4dbe943eff9f394f33c986eec1723e1729ded5b3cdf17096b9`
- each mutation was applied alone, not staged or committed; the exact restore hash was checked before the next mutation.

### M-H1 — UTF-16 to UTF-8 position regression

Exact temporary diff:

```diff
-        let result = hover_snapshot(snapshot, position, encoding).map_err(ServerError::Hover)?;
+        let result = hover_snapshot(snapshot, position, PositionEncoding::Utf8)
+            .map_err(ServerError::Hover)?;
```

Command:

```text
cargo test -p ddonirang-tool --test lsp_hover h01_h08_initialize_and_shared_local_stdlib_hover -- --nocapture
```

Expected/actual RED:

```text
called \`Result::unwrap()\` on an \`Err\` value:
Hover(InvalidPosition(ContinuationByte))
test h01_h08_initialize_and_shared_local_stdlib_hover ... FAILED
```

Exact restore:

```text
restore server.rs; SHA256=58F2636249673A4DBE943EFF9F394F33C986EEC1723E1729DED5B3CDF17096B9
```

GREEN after restore: the same focused test passed, 1/1.

### M-H2 — stale version guard removal

Exact temporary diff:

```diff
-        if let Some(requested_version) = document.get("version").and_then(Value::as_i64) {
-            if requested_version != snapshot.version {
-                return Ok(error_event(
-                    id,
-                    RpcError::with_data(
-                        -32801,
-                        "hover document version이 stale합니다",
-                        json!({
-                            "requestedVersion": requested_version,
-                            "currentVersion": snapshot.version,
-                            "snapshotIdentity": snapshot.identity.as_str(),
-                        }),
-                    ),
-                ));
-            }
-        }
```

Command:

```text
cargo test -p ddonirang-tool --test lsp_hover h09_h11_live_snapshot_close_and_byte_stability -- --nocapture
```

Expected/actual RED:

```text
stale hover must be rejected: ServerEvent { responses: [Response {
  result: Ok(... documentVersion: 2 ...)
}] }
test h09_h11_live_snapshot_close_and_byte_stability ... FAILED
```

Exact restore:

```text
restore server.rs; SHA256=58F2636249673A4DBE943EFF9F394F33C986EEC1723E1729DED5B3CDF17096B9
```

GREEN after restore: the same focused test passed, 1/1.

### M-H3 — hover capability advertisement removal

Exact temporary diff:

```diff
-                    "completionProvider": {"resolveProvider": false},
-                    "hoverProvider": true
+                    "completionProvider": {"resolveProvider": false}
```

Command:

```text
cargo test -p ddonirang-tool --test lsp_hover h01_h08_initialize_and_shared_local_stdlib_hover -- --nocapture
```

Expected/actual RED:

```text
assertion failed:
initialized.responses[0].clone_response().unwrap()["capabilities"]["hoverProvider"] == true
test h01_h08_initialize_and_shared_local_stdlib_hover ... FAILED
```

Exact restore:

```text
restore server.rs; SHA256=58F2636249673A4DBE943EFF9F394F33C986EEC1723E1729DED5B3CDF17096B9
```

GREEN after restore: the complete focused hover suite passed, 3/3.

## Verification

- focused hover: PASS, 3/3
- diagnostics regression: PASS, 6/6
- completion regression: PASS, 15/15
- transport/document-sync regression: PASS, 22/22
- existing black-box checker, with `H12_BLACKBOX_HOVER_BEFORE_EOF` extension: PASS
  - I1–I8 PASS/FAIL_CLOSED
  - RB06/RB08 FAIL_CLOSED
  - H12 hover before EOF PASS
  - final `LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS`
- `git diff --check`: PASS
- `cargo check -p ddonirang-tool --bin ddonirang-lsp`: blocked by pre-existing foreign dirty language files, not by this task:
  - `lang/src/model.rs:3953–3959`: missing `UnitDim::AXIS_COUNT/exponents/from_exponents`
  - `lang/src/parser.rs:2595`: missing `Fixed64::parse_decimal_exact`
  - foreign dirty paths were `lang/src/model.rs`, `lang/src/parser.rs`, `lang/src/runtime.rs`, `lang/src/stdlib.rs`
  - no LSP task file overlaps those paths; they were not modified, staged, or repaired.

## Custody and non-claims

- foreign tracked dirty and protected untracked files were not touched.
- no push, force-push, tag, release, history rewrite, or new worktree/branch/reviewer.
- no product change outside the six listed task-owned paths.
- no full semantic IDE, go-to-definition, rename, references, VSCode extension release, Seamgrim, P0–P6, V1, public, release, or Human PASS claim.
- status: `LSP_HOVER_STATUS=PRODUCT_IMPLEMENTED_PENDING_REVIEW`
- `READY_FOR_INDEPENDENT_REVIEW=YES`
- reviewer should bind the same review to product target `ef34c931c447ff768a602276dbe5e5fd8d7f7678`.
