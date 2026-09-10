# DDN-LSP32-SAFE-FULL-DOCUMENT-FORMATTING-R1 — 결과

## 기준과 결속

```ini
ACTIVE_UNIT = LSP32_SAFE_FULL_DOCUMENT_FORMATTING
BASE_HANDOFF = 1fa26d707208e30eb01b56fd059f0e0b99f1ec5b
PRODUCT_FIXED = 985fea19ad7aa3f33cffe43021ff6d9e5d19a65f
PRODUCT_TREE = dbeb2b0eb30cb174abfcb7738c0e45534a8167fd
PRODUCT_PARENT = 1fa26d707208e30eb01b56fd059f0e0b99f1ec5b
MERGE_COUNT = 0
```

이 문서는 LSP32 product commit의 별도 handoff다. LSP30 이전 commit은 amend/rebase/revert하지 않았다. 현재 checkout의 foreign dirty tracked paths와 보호된 untracked session delta는 읽기·수정·stage하지 않았다.

## 제품 변경

변경한 파일은 다음 두 개뿐이다.

```text
tool/src/lsp/server.rs
tool/tests/lsp_formatting.rs
```

`tool/src/lsp/server.rs`의 최종 blob은 `f859c6271fa2915fd54faef0a36d2a6373b1e674`이고, `tool/tests/lsp_formatting.rs`의 최종 blob은 `0f7f3f84c0999569f4d9318109ad4f1e868cf460`이다.

구현 계약:

- ordinary `.ddn`은 기존 `parse_v25` → `canonicalize` → `normalize(N1)` owner를 사용한다.
- `.ddl`/`.옮김`은 기존 `parse_ddl_wave1` → `canonicalize_ddl_wave1` owner만 사용한다.
- 두 표면 모두 canonical 결과를 다시 parse/canonicalize하고, 결과가 byte-identical하지 않으면 edit를 게시하지 않는다.
- DDL은 2차 parse에서 DefinitionIdentity/TypeIdentity 배열이 원본과 다르면 edit를 게시하지 않는다.
- current open `DocumentStore` snapshot, version, snapshot identity만 사용한다. unknown/closed/stale/invalid/legacy/migration-required input은 `[]`이다.
- source byte bound는 `1_000_000` bytes이며, 초과 source는 `[]`이다.
- 변경 문서는 UTF-16 negotiated encoding으로 시작 `(0,0)`부터 source 전체 끝까지를 가리키는 단일 full-document `TextEdit`만 받는다.
- request cancellation은 parse/canonicalize 전후와 publish 직전에 확인하며, 취소된 request는 `-32800`으로 종료하고 edit를 게시하지 않는다.
- initialize의 기존 `documentFormattingProvider = true`와 기존 `textDocument/formatting` wire를 유지한다.

새 parser, grammar, semantic owner, dependency, `tool/src/lib.rs` 변경, filesystem access, remote dependency, source upload, range/on-type formatting은 추가하지 않았다.

## 검증

Focused:

```text
cargo test -p ddonirang-tool --test lsp_formatting
4 passed, 0 failed
```

LSP 회귀:

```text
lsp_completion          15 passed
lsp_definition           3 passed
lsp_diagnostics         11 passed
lsp_document_highlight   4 passed
lsp_document_symbol      4 passed
lsp_formatting           4 passed
lsp_hover                 3 passed
lsp_open_document_navigation 11 passed
lsp_references            4 passed
lsp_rename                5 passed
lsp_semantic_tokens       3 passed
lsp_signature_help        3 passed
FAILED_BINARIES = 0
```

Persistent transport checker:

```text
python tests/run_lsp0_transport_document_sync_check.py
F13_BLACKBOX_FORMATTING_BEFORE_EOF = PASS
LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK = PASS
```

지정 추가 검증:

```text
cargo check -p ddonirang-tool --bin ddonirang-lsp --offline = PASS
git diff --check = PASS
```

## Mutation evidence

Mutation 전 product source 기준 hash:

```ini
TARGET = tool/src/lsp/server.rs
BASE_SHA256 = FADEEB6E9252639B902D389EEED3E7E7A849450E2E3A929E6C657DE4F79F0404
```

각 mutation은 한 번에 하나만 적용했다. 각 restore 직후 `server.rs` hash는 위 `BASE_SHA256`와 byte-exact 일치했고, focused formatting suite는 다시 `4 passed, 0 failed`였다.

### M1 — second parse/canon stability guard 훼손

Exact diff:

```diff
-        if stable != canonical {
+        if stable == canonical {
```

RED:

```text
lsp32_formatting_supports_authoritative_ddl_and_closes_open_snapshot ... FAILED
lsp13_formatting_uses_shared_canonical_owner_and_live_snapshot ... FAILED
test result: FAILED. 2 passed; 2 failed
```

Restore:

```diff
-        if stable == canonical {
+        if stable != canonical {
```

`RESTORE_SHA256 = FADEEB6E9252639B902D389EEED3E7E7A849450E2E3A929E6C657DE4F79F0404`

GREEN: `cargo test -p ddonirang-tool --test lsp_formatting` — `4 passed, 0 failed`.

### M2 — UTF-16 end range를 UTF-8 range로 강등

Exact diff:

```diff
-            encoding,
+            PositionEncoding::Utf8,
```

RED:

```text
lsp13_formatting_uses_shared_canonical_owner_and_live_snapshot ... FAILED
assertion `left == right` failed at tool/tests/lsp_formatting.rs:117:5
test result: FAILED. 3 passed; 1 failed
```

Restore:

```diff
-            PositionEncoding::Utf8,
+            encoding,
```

`RESTORE_SHA256 = FADEEB6E9252639B902D389EEED3E7E7A849450E2E3A929E6C657DE4F79F0404`

GREEN: `cargo test -p ddonirang-tool --test lsp_formatting` — `4 passed, 0 failed`.

### M3 — migration-required 입력에 partial edit 게시

먼저 legacy validation guard만 삭제하는 mutation을 시도했으나, 기존 `parse_v25`가 그 입력을 뒤에서 독립적으로 reject하여 RED가 관측되지 않았다. 그 시도는 성공 증거로 채택하지 않았다.

실제 채택 mutation은 같은 fail-closed guard의 반환을 partial edit로 바꾼 것이다.

Exact diff:

```diff
         if !is_ddl && validate_no_legacy_boim_surface(source).is_err() {
-            return Ok(success_event(id, json!([])));
+            return Ok(success_event(
+                id,
+                json!([{
+                    "range": {
+                        "start": {"line": 0, "character": 0},
+                        "end": {"line": 0, "character": 0},
+                    },
+                    "newText": "",
+                }]),
+            ));
         }
```

RED:

```text
lsp13_formatting_fails_closed_for_stale_and_legacy_input ... FAILED
assertion `left == right` failed at tool/tests/lsp_formatting.rs:197:5
test result: FAILED. 3 passed; 1 failed
```

Restore:

```diff
-            return Ok(success_event(
-                id,
-                json!([{
-                    "range": {
-                        "start": {"line": 0, "character": 0},
-                        "end": {"line": 0, "character": 0},
-                    },
-                    "newText": "",
-                }]),
-            ));
+            return Ok(success_event(id, json!([])));
```

`RESTORE_SHA256 = FADEEB6E9252639B902D389EEED3E7E7A849450E2E3A929E6C657DE4F79F0404`

GREEN: `cargo test -p ddonirang-tool --test lsp_formatting` — `4 passed, 0 failed`.

Mutation residue는 남기지 않았다. 최종 product source는 M1/M2/M3 모두 restore 상태다.

## Git custody

```ini
PRODUCT_COMMIT = 985fea19ad7aa3f33cffe43021ff6d9e5d19a65f
PRODUCT_TREE = dbeb2b0eb30cb174abfcb7738c0e45534a8167fd
PRODUCT_PARENT = 1fa26d707208e30eb01b56fd059f0e0b99f1ec5b
AUTHOR = tongosu <tongosu@myarts.kr>
COMMITTER = tongosu <tongosu@myarts.kr>
PROHIBITED_TRAILER_COUNT = 0
PUSH_PERFORMED = NO
NEW_DEPENDENCY = 0
NEW_PACK_RUNNER_META_TEST = 0/0/0
```

이 handoff 문서는 product commit 다음에 별도 docs-only commit으로 봉인한다. 독립검토 상태는 `PRODUCT_FIXED_PENDING_REVIEW`이며, 이 문서는 동일 product target에 결속된 LSP32 review 입력이다.

## 현재 custody와 다음 단계

```ini
FOREIGN_DIRTY_TOUCHED = 0
PROTECTED_UNTRACKED_CHANGED = 0
TASK_OWNED_DIRTY_BEFORE_HANDOFF = 0
STAGED_PRODUCT_PATHS = 0
PROCESS_RESIDUE = 0
READY_FOR_INDEPENDENT_REVIEW = YES
NEXT_AUTONOMOUS_UNIT = MANAGER_SELECTION_REQUIRED
```

제품 승격, public push, VSIX 재생성, LSP22 host gate 재실행, 다음 LSP 기능 구현은 이 handoff 범위에 포함하지 않는다.
