# DDN-LSP19-OPEN-DOCUMENT-TYPE-DEFINITION-R1 — Handoff

## 상태

- `ACTIVE_PRODUCT_UNIT = textDocument/typeDefinition`
- `IMPLEMENTATION_BASE = 3b438441e2a2a30aa713c6fe77c2286566310144` (LSP18 handoff)
- `PRODUCT_FIXED = 12e9434d893ee402e26a03a3d7a75edfa1d79d9a`
- `PRODUCT_TREE = d1fcef91e3f62d21b415f54fdcb5f8ac7a4077dc`
- `PRODUCT_PARENT = 3b438441e2a2a30aa713c6fe77c2286566310144`
- `PUSH_PERFORMED = NO`

작성자·커미터는 모두 `tongosu <tongosu@myarts.kr>`이며 prohibited trailer는 0이다.

## 구현 경계

기존 `DocumentStore`와 `tool/src/lsp/symbol.rs`의 lexer/parser owner를 재사용했다. 열린 문서만 입력으로 사용하며 filesystem crawl, unopened source, remote/upload, 새 registry/parser, `tool/src/lib.rs`, dependency는 추가하지 않았다.

- `tool/src/lsp/symbol.rs`: `SeedKind::Imeumssi` 로컬 type declaration을 `type:local:<canonical_name>` identity로 수집하고, 기존 token/parser 결과에서 `name:TypeRef` 사용 위치를 찾는다. 열린 문서 전체에서 정확히 하나일 때만 반환하며 duplicate, callable-only 이름, unknown/stdlib-without-source는 null이다.
- `tool/src/lsp/server.rs`: initialize `typeDefinitionProvider`, `textDocument/typeDefinition` route, version `-32801`, snapshot `-32802`, target open-snapshot/range/data binding을 추가했다.
- `tool/tests/lsp_open_document_navigation.rs`: same/other open document, applied type, Korean/UTF-16, duplicate, callable-only, unknown, string, didClose, stale, repeat assertions를 추가했다.
- `tests/run_lsp0_transport_document_sync_check.py`: 기존 persistent transport runner에 type-definition before-EOF check를 추가했다.

## 검증

```text
cargo test -p ddonirang-tool --test lsp_open_document_navigation
  8 passed

cargo test -p ddonirang-tool --test lsp_definition --test lsp_references --test lsp_rename
  2 + 4 passed

cargo test -p ddonirang-tool --test lsp_document_symbol --test lsp_signature_help
  3 + 3 passed

cargo test -p ddonirang-tool --test lsp_completion --test lsp_hover --test lsp_diagnostics
  15 + 6 + 3 passed

cargo test -p ddonirang-tool --test lsp_semantic_tokens --test lsp_document_highlight --test lsp_formatting
  3 + 2 + 3 passed

python tests/run_lsp0_transport_document_sync_check.py
  ST23_BLACKBOX_TYPE_DEFINITION_BEFORE_EOF=PASS
  LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS

cargo check -p ddonirang-tool
  PASS (warnings only)

git diff --check
  PASS
```

black-box의 첫 별도 target build는 task-owned rustc가 20분 이상 산출물 없이 정지해 종료했고, 동일 runner를 현재 작업 target으로 재실행하여 PASS를 확보했다. runner/pack/검증 로직은 동일하다.

## Mutation evidence

각 mutation은 한 번에 하나만 적용하고 즉시 원복했다. 아래 hash는 mutation 직전과 원복 직후의 byte-exact hash이다.

### M1 — type-kind guard 제거

대상: `tool/src/lsp/symbol.rs`, `collect_local_type_definitions`의 다음 guard.

```diff
@@
             let TopLevelItem::SeedDef(seed) = item;
+            if !matches!(&seed.seed_kind, SeedKind::Imeumssi) {
+                return None;
+            }
             declaration_range(&tokens, seed).map(|range| {
```

임시 mutation은 위 2줄을 제거했다. callable-only `가짜:셈씨`를 type declaration으로 오수용하는 assertion이 RED가 됐다.

- 원복 전 원본 SHA-256: `AE092F72B0362FC3957CCE32742A05A2B1A462FD8EA9E1FA8B865C51DE1D7F9D`
- RED: `lsp19_type_definition_is_exact_open_document_bound_and_utf16_current` — callable-only input이 `type:local:가짜`로 잘못 반환되어 expected null assertion 실패
- 원복 SHA-256: `AE092F72B0362FC3957CCE32742A05A2B1A462FD8EA9E1FA8B865C51DE1D7F9D`
- 원복 후 GREEN: 동일 focused test PASS

### M2 — didClose removal 제거

대상: `tool/src/lsp/document_store.rs`, `DocumentStore::close`.

```diff
@@
         self.documents
-            .remove(uri)
+            .get(uri)
+            .cloned()
             .ok_or(DocumentStoreError::NotOpen)
```

- 원복 전 원본 SHA-256: `B2D1B815CFFBD609C1C8D01D55F9CAE3D7F62FE17156D661F846F203DE9BFA87`
- RED: close 후에도 `file:///a-type-declaration.ddn` type location이 반환되어 null assertion 실패
- 원복 SHA-256: `B2D1B815CFFBD609C1C8D01D55F9CAE3D7F62FE17156D661F846F203DE9BFA87`
- 원복 후 GREEN: 동일 focused test PASS

### M3 — stale snapshot guard 제거

대상: `tool/src/lsp/server.rs`, LSP19 `type_definition`의 snapshot identity guard.

```diff
@@
-            if requested_identity != snapshot.identity.as_str() {
+            if false && requested_identity != snapshot.identity.as_str() {
```

- 원복 전 원본 SHA-256: `56A928098463A0884046C0F8F50D4BED6E5946B50F4AA0ACB7860BBE6CAC2395`
- RED: forged `snapshot:forged` 요청이 `-32802`로 거부되지 않아 stale snapshot assertion 실패
- 원복 SHA-256: `56A928098463A0884046C0F8F50D4BED6E5946B50F4AA0ACB7860BBE6CAC2395`
- 원복 후 GREEN: 동일 focused test PASS

## custody

- product commit changed paths: 정확히 4개 위 LSP19 파일
- `tool/src/lib.rs` changed: 0
- `lang/**`, `core/**`, runtime/WASM/Workbench foreign dirty paths: touched 0, staged 0
- new dependency/pack/runner/meta-test: `0/0/0`
- public push: `NO`
- process residue after validation: task-owned cargo/rustc/LSP runner 0
- independent review readiness: `YES`

다음 작업은 동일 target의 독립검토이며, LSP20은 LSP19 review binding 이후 별도 successor로 시작한다.
