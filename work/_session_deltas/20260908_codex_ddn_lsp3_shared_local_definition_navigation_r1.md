# DDN-LSP3-SHARED-LOCAL-DEFINITION-NAVIGATION-R1 — 결과

## 작업 계약

- 실행자: 현재 세션, single writer
- 선행 LSP2 handoff: `78e7d1fbf5f5cce5e14ad80d351c6ba205e5c30b`
- latest safe successor base: `21af229179096a29ded4abdfc7080406915041a1`
- successor tree: `e68f2bad374f67217a94f61df7a3848ff913da2f`
- successor parent: `78e7d1fbf5f5cce5e14ad80d351c6ba205e5c30b`
- successor 변경은 LSP 경로가 아닌 docs-only session/control 문서 2개뿐이며 LSP drift는 0이었다.
- 이번 제품 commit은 successor 위에서 시작했고, LSP task-owned 경로만 변경했다.
- cross-file index, network, remote source upload, WASM/UI, lang/core, SSOT/SPEC, pack, teul-cli는 범위 밖이다.

## 제품 결과

- product commit: `fe60fed73e129d9bfa8737dbe0b254c3b8e360ea`
- product tree: `0276166dcd9b8629f02062f06e11c486addb267d`
- product parent: `21af229179096a29ded4abdfc7080406915041a1`
- merge count: 0
- changed product paths:
  - `tests/run_lsp0_transport_document_sync_check.py`
  - `tool/src/hover.rs`
  - `tool/src/lsp/definition.rs`
  - `tool/src/lsp/mod.rs`
  - `tool/src/lsp/server.rs`
  - `tool/src/lsp/symbol.rs`
  - `tool/tests/lsp_definition.rs`
- unexpected paths: 0
- shared navigation/symbol owner: `tool/src/lsp/symbol.rs`
- hover and definition both reuse `resolve_symbol`; duplicate parser/registry/formatter/semantic owner count: 0
- new dependency/pack/runner/meta-test: 0/0/0/0

## G01–G12

- G01 PASS: initialize advertises `definitionProvider: true`.
- G02 PASS: local immutable value reference resolves to the same-document definition range.
- G03 PASS: local callable invocation/reference resolves to the callable declaration range.
- G04 PASS: declaration self-navigation returns its own exact declaration range.
- G05 PASS: returned URI is exactly the open document URI and range is declaration-name exact.
- G06 PASS: stdlib callable, unknown, whitespace, and punctuation return null.
- G07 PASS: Korean UTF-16 declaration and target ranges are exact.
- G08 PASS: emoji-preceded UTF-16 reference resolves to the correct declaration range.
- G09 PASS: current snapshot is used; stale version returns `-32801`, no stale location.
- G10 PASS: didClose returns null.
- G11 PASS: repeated definition result is byte-stable.
- G12 PASS: fragmented in-memory transport and black-box stdio return definition before EOF.

## Focused implementation

- `definition_snapshot` resolves the shared symbol owner and returns only local declaration ranges.
- stdlib and unresolved symbols have no source declaration range and therefore return null.
- definition response is a same-document LSP Location object:
  `{ "uri": <current URI>, "range": <declaration name range> }`.
- existing hover output remains stable after moving its lookup to the shared symbol owner.

## Mutation evidence

Final product baseline for `tool/src/lsp/server.rs`:

```text
SHA256=AB95C4835AD4D8F927AB471C8D2E2398814A8C9D3E40E460B601ECFFDC271C7C
```

Each mutation was applied alone, was not staged or committed, and was restored before the next mutation. Every exact restore returned the same baseline SHA-256 above.

### M-N1 — UTF-16 to UTF-8 position regression

Exact temporary diff:

```diff
-        let result =
-            definition_snapshot(snapshot, position, encoding).map_err(ServerError::Definition)?;
+        let result = definition_snapshot(snapshot, position, PositionEncoding::Utf8)
+            .map_err(ServerError::Definition)?;
```

Command:

```text
cargo test -p ddonirang-tool --test lsp_definition g01_g08_local_definition_identity_and_utf16_range -- --nocapture
```

RED:

```text
called \`Result::unwrap()\` on an \`Err\` value:
Definition(InvalidPosition(ContinuationByte))
test g01_g08_local_definition_identity_and_utf16_range ... FAILED
```

Restore and GREEN:

```text
SHA256=AB95C4835AD4D8F927AB471C8D2E2398814A8C9D3E40E460B601ECFFDC271C7C
test g01_g08_local_definition_identity_and_utf16_range ... ok
```

### M-N2 — definition version guard removal

Exact temporary diff:

```diff
-        if let Some(requested_version) = document.get("version").and_then(Value::as_i64) {
-            if requested_version != snapshot.version {
-                return Ok(error_event(
-                    id,
-                    RpcError::with_data(
-                        -32801,
-                        "definition document version이 stale합니다",
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
cargo test -p ddonirang-tool --test lsp_definition g06_g11_null_stale_close_and_stable -- --nocapture
```

RED:

```text
assertion failed: stale response did not match error code -32801
test g06_g11_null_stale_close_and_stable ... FAILED
```

Restore and GREEN:

```text
SHA256=AB95C4835AD4D8F927AB471C8D2E2398814A8C9D3E40E460B601ECFFDC271C7C
test g06_g11_null_stale_close_and_stable ... ok
```

### M-N3 — definitionProvider advertisement removal

Exact temporary diff:

```diff
-                    "definitionProvider": true,
```

Command:

```text
cargo test -p ddonirang-tool --test lsp_definition g01_g08_local_definition_identity_and_utf16_range -- --nocapture
```

RED:

```text
left: Null
right: true
test g01_g08_local_definition_identity_and_utf16_range ... FAILED
```

Restore and GREEN:

```text
SHA256=AB95C4835AD4D8F927AB471C8D2E2398814A8C9D3E40E460B601ECFFDC271C7C
definition focused suite: 3 passed, 0 failed
```

## Verification

- focused definition: PASS, 3/3
- hover regression: PASS, 3/3
- diagnostics regression: PASS, 6/6
- completion regression: PASS, 15/15
- transport/document-sync regression: PASS, 22/22
- existing black-box checker extended with definition behavior: PASS
  - I1–I6 PASS
  - I7/I8 FAIL_CLOSED
  - RB06/RB08 FAIL_CLOSED
  - H12 hover before EOF PASS
  - G12 definition before EOF PASS
  - final `LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS`
- `git diff --check`: PASS
- `cargo check -p ddonirang-tool --bin ddonirang-lsp`: pre-existing foreign failure, not changed by this task:
  - `lang/src/model.rs:3953–3959`: missing `UnitDim::AXIS_COUNT`, `exponents`, `from_exponents`
  - `lang/src/parser.rs:2595`: missing `Fixed64::parse_decimal_exact`
  - foreign dirty files: `lang/src/model.rs`, `lang/src/parser.rs`, `lang/src/runtime.rs`, `lang/src/stdlib.rs`
  - no overlap with the seven LSP product paths; no foreign file was modified, staged, or repaired.

## Custody and non-claims

- foreign tracked dirty and protected untracked files were preserved.
- no push, force-push, tag, release, history rewrite, new worktree, new branch, or new reviewer.
- no new dependency, pack, runner, or meta-test.
- no cross-file go-to-definition, workspace index, rename, references, full semantic IDE, VS Code extension release, Seamgrim browser, P0–P6/V1 closure, public support, release, or Human PASS claim.
- product status: `LSP_DEFINITION_STATUS=PRODUCT_IMPLEMENTED_PENDING_REVIEW`
- `READY_FOR_INDEPENDENT_REVIEW=YES`
- reviewer must bind the same review to product target `fe60fed73e129d9bfa8737dbe0b254c3b8e360ea`.
