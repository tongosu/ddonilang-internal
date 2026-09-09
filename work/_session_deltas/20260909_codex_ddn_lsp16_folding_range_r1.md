# DDN-LSP16-CURRENT-DOCUMENT-STRUCTURAL-FOLDING-R1

## 기준점과 commit

- LSP15 product: `9e3574b5cb99dad171d212d3aa813c0e87a14054`
- LSP15 docs handoff: `0523fbc5e41d391735b5266b6420e48da8f94278`
- LSP16 product: `a7b991a4e65c7faa403b61478a91f2e9f6dcfae7`
- LSP16 product tree: `236cc037617963f65979d218ac28ef4b155ebbd9`
- LSP16 product parent: `0523fbc5e41d391735b5266b6420e48da8f94278`
- author/committer: `tongosu <tongosu@myarts.kr>`
- prohibited trailer count: `0`

LSP15 target identity는 변경하지 않았고, LSP16은 그 successor에서만 구현했다.

## product paths

다음 5개만 product commit `a7b991a4`에 포함됐다.

```text
tests/run_lsp0_transport_document_sync_check.py
tool/src/lsp/folding_range.rs
tool/src/lsp/mod.rs
tool/src/lsp/server.rs
tool/tests/lsp_open_document_navigation.rs
```

`tool/src/lib.rs`, `lang/**`, `core/**`, WASM/CLI/UI, SSOT/SPEC, foreign dirty path는 변경하지 않았다.

## 구현 결과

- `initialize`에 `foldingRangeProvider = true`를 선언했다.
- 현재 open `DocumentSnapshot`만 대상으로 `textDocument/foldingRange`를 처리한다.
- parser/AST의 definition, callable body, compound statement span만 사용한다.
- UTF-16 LSP range를 기존 position owner로 변환한다.
- single-line/empty range는 제외한다.
- source order와 outer-before-inner 순서를 deterministic하게 정규화한다.
- proper nesting이 아닌 overlap은 fail-closed 한다.
- didChange의 current version/snapshot만 허용하며 stale version은 `-32801`, stale snapshot은 `-32802`다.
- didClose 또는 unknown URI는 빈 결과다.
- filesystem crawl, unopened document 접근, lexical brace matching, remote/source upload은 없다.

## 검증

Focused:

```text
cargo test -p ddonirang-tool --test lsp_open_document_navigation --offline
  5 passed
cargo test -p ddonirang-tool folding_range --offline
  nested ordering unit passed
```

새 open-document test는 initialize capability, deterministic repeat, current document, stale version/snapshot, malformed fail-closed, didClose empty를 검증한다.

Persistent transport:

```text
python tests/run_lsp0_transport_document_sync_check.py
ST21_BLACKBOX_FOLDING_RANGE_BEFORE_EOF=PASS
LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS
```

Applicable LSP regression:

```text
lsp_definition=PASS
lsp_references=PASS
lsp_rename=PASS
lsp_document_symbol=PASS
lsp_open_document_navigation=PASS
lsp_signature_help=PASS
lsp_semantic_tokens=PASS
lsp_hover=PASS
lsp_diagnostics=PASS
lsp_completion=PASS
lsp_formatting=PASS
lsp_document_highlight=PASS
```

```text
rustfmt --edition 2021 --check <owned LSP files> = PASS
git diff --check = PASS
clean snapshot cargo check --manifest-path tool/Cargo.toml --bin ddonirang-lsp --offline = PASS
```

Clean snapshot check는 `lsp16-clean-snapshot-r1-20260909`에서 foreign dirty 변경 없이 수행했다. 현재 dirty root의 직접 cargo check는 LSP16 원인이 아닌 기존 foreign `lang/core` API mismatch 때문에 clean snapshot 검증으로 분리했다.

## mutation evidence

각 mutation은 한 번에 하나만 적용하고 즉시 원본으로 복원했다. mutation 전 folding file hash는 `19d943bc39a514ccfb38bc6d8cd3749640bab26d7f5eee250e20636e1dc72669`, server file hash는 `ad2078fc5e25d3553e3cd595844f2f5db8167802d04d51c1132a02ef5d998121`이었다.

### M1 lexical brace guessing

Target: `tool/src/lsp/folding_range.rs`, `folding_ranges_snapshot`의 AST candidate 수집 직후.

Exact temporary diff:

```diff
+    for (start, _) in source.match_indices('{') {
+        candidates.push(Candidate {
+            range: ByteRange {
+                start,
+                end: source.len(),
+            },
+            kind: FoldingKind::Compound,
+        });
+    }
```

Command:

```text
cargo test -p ddonirang-tool --test lsp_open_document_navigation lsp16_folding_ranges_are_ast_bound_utf16_deterministic_and_current --offline -- --nocapture
```

RED 핵심 출력:

```text
thread 'lsp16_folding_ranges_are_ast_bound_utf16_deterministic_and_current' ... panicked
```

AST 결과에 lexical candidate가 더해져 server의 invalid/proper-overlap 경로가 노출됐다. 해당 temporary hunk 제거 후 hash는 다시 `19d943bc39a514ccfb38bc6d8cd3749640bab26d7f5eee250e20636e1dc72669`였고 동일 command가 `1 passed`로 GREEN이었다.

### M2 nested ordering reversal

Target: `tool/src/lsp/folding_range.rs`, `normalize_candidates` sort.

Exact temporary diff:

```diff
             .start
             .cmp(&right.byte_range.start)
+            .reverse()
             .then(right.byte_range.end.cmp(&left.byte_range.end))
```

Command:

```text
cargo test -p ddonirang-tool lsp::folding_range::tests::nested_ranges_are_outer_before_inner_and_source_ordered --offline -- --nocapture
```

RED 핵심 출력:

```text
left:  [ByteRange { start: 6, end: 16 }, ByteRange { start: 0, end: 16 }]
right: [ByteRange { start: 0, end: 16 }, ByteRange { start: 6, end: 16 }]
```

`.reverse()` 제거 후 folding file hash는 다시 `19d943bc39a514ccfb38bc6d8cd3749640bab26d7f5eee250e20636e1dc72669`였고 동일 command가 `1 passed`로 GREEN이었다.

### M3 stale snapshot guard removal

Target: `tool/src/lsp/server.rs`, `folding_ranges`의 snapshot identity guard.

Exact temporary diff:

```diff
-            if requested_identity != snapshot.identity.as_str() {
+            if false && requested_identity != snapshot.identity.as_str() {
```

Command:

```text
cargo test -p ddonirang-tool --test lsp_open_document_navigation lsp16_folding_ranges_are_ast_bound_utf16_deterministic_and_current --offline -- --nocapture
```

RED 핵심 출력:

```text
thread 'lsp16_folding_ranges_are_ast_bound_utf16_deterministic_and_current' ... panicked
```

기대 `-32802` stale response 대신 정상 result가 반환되어 test helper가 실패했다. guard를 exact restore한 뒤 server hash는 다시 `ad2078fc5e25d3553e3cd595844f2f5db8167802d04d51c1132a02ef5d998121`였고 동일 command가 `1 passed`로 GREEN이었다.

## custody

```makefile
PRODUCT_FILE_CHANGE = LSP16 owned paths only
TOOL_SRC_LIB_RS_CHANGED = 0
NEW_DEPENDENCY = 0
NEW_PACK/RUNNER/META_TEST = 0/0/0
PUSH = NO
FOREIGN_DIRTY_TOUCHED = 0
PROCESS_RESIDUE = 0
```

기존 foreign tracked 변경과 기존 untracked session delta는 stage/commit하지 않았다. LSP16 product commit은 docs-only handoff와 분리한다.
