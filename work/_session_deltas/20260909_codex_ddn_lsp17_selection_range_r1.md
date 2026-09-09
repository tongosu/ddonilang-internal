# DDN-LSP17 현재 문서 selectionRange R1 — 결과 및 인계

## 권위와 predecessor 결속

- LSP16 product fixed: `a7b991a4e65c7faa403b61478a91f2e9f6dcfae7`
  - tree: `236cc037617963f65979d218ac28ef4b155ebbd9`
  - parent: `0523fbc5e41d391735b5266b6420e48da8f94278`
- LSP16 handoff: `6d6bfe20579045efd025a5daec3025e6cd1f411d`
  - tree: `f3657ede1288ceccc23e8c0dd9fce96bb271dffc`
  - parent: `a7b991a4e65c7faa403b61478a91f2e9f6dcfae7`
- LSP17 product fixed: `a29b4a53361a513622cf6f350278a116e66832ef`
  - tree: `6ec21f71fcf55fd37a789a09dbc08b58dd600822`
  - parent: `6d6bfe20579045efd025a5daec3025e6cd1f411d`

LSP17은 현재 열린 `DocumentStore` snapshot만 사용한다. lexer token boundary와 V25 parser/AST span을 기존 LSP position conversion으로 UTF-16 range에 투영하며, invalid/stale/closed 입력은 fail-closed한다. `initialize` capability는 `selectionRangeProvider: true`이다.

## 제품 변경

변경 경로는 다음 5개뿐이다.

- `tool/src/lsp/selection_range.rs`
- `tool/src/lsp/mod.rs`
- `tool/src/lsp/server.rs`
- `tool/tests/lsp_open_document_navigation.rs`
- `tests/run_lsp0_transport_document_sync_check.py`

구현된 동작:

- 식별자·literal token에서 AST expression/statement/body/seed의 바깥 부모 chain 생성
- 입력 positions 순서 유지, 동일 입력 반복 시 byte-stable 응답
- Korean/non-BMP UTF-16 변환과 string 내부 boundary 처리
- punctuation/whitespace/invalid/parse failure는 null
- didChange current version 반영, stale version `-32801`, stale snapshot `-32802`
- didClose 또는 unknown URI는 빈 배열
- response를 EOF 전에 반환하는 기존 persistent transport 유지
- crossing selection ranges는 parent containment 검증으로 거부

## 검증

Focused:

```text
cargo test -p ddonirang-tool --test lsp_open_document_navigation --offline -- --nocapture
6 passed; 0 failed
```

Black-box:

```text
python tests/run_lsp0_transport_document_sync_check.py
ST22_BLACKBOX_SELECTION_RANGE_BEFORE_EOF=PASS
LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS
```

기존 LSP definition/references/rename/documentSymbol/open-document/signatureHelp/semanticTokens/hover/diagnostics/completion/formatting/documentHighlight 회귀를 한 번에 실행해 모두 PASS했다. 전체 실행 결과는 각 test target `test result: ... 0 failed`이다.

Clean snapshot:

```text
cargo check -p ddonirang-tool --offline
Finished `dev` profile ...
```

검증 snapshot과 target은 Git worktree 밖 `I:\home\urihanl\ddn\codex\build\lsp17-clean-snapshot-r1-20260909-02` 및 `I:\home\urihanl\ddn\codex\build\lsp17-clean-target-r1-20260909-02`에 두었다. 제품 tree에는 포함하지 않는다.

## Mutation evidence

기준 파일 SHA-256은 mutation 전 최종 제품 상태에서 수집했다.

### M1 — UTF-8 position 강등

대상: `tool/src/lsp/selection_range.rs`

Exact diff:

```diff
-    let cursor = position_to_byte_offset(source, position, encoding).ok()?;
+    let cursor = position_to_byte_offset(source, position, PositionEncoding::Utf8).ok()?;
```

명령:

```text
cargo test -p ddonirang-tool --test lsp_open_document_navigation lsp17_selection_ranges_are_ordered_ast_parent_chains_and_current --offline -- --nocapture
```

RED 핵심: `test lsp17_selection_ranges_are_ordered_ast_parent_chains_and_current ... FAILED`, `test result: FAILED. 0 passed; 1 failed`.

복원 전 기준/복원 후 SHA-256: `6FEB1EE983EAADDFE60B544ADDB5D575516EBE2E0E3E0026500211A410B868D2`.

복원 후 동일 명령: `1 passed; 0 failed`.

### M2 — parent containment validation 제거

대상: `tool/src/lsp/selection_range.rs`, `validate_selection_chain`.

Exact diff:

```diff
-    selected
-        .windows(2)
-        .all(|pair| pair[1].start <= pair[0].start && pair[0].end <= pair[1].end)
+    let _ = selected;
+    true
```

명령:

```text
cargo test -p ddonirang-tool --lib lsp::selection_range::tests::rejects_crossing_selection_ranges --offline -- --nocapture
```

RED 핵심: `assertion failed: !validate_selection_chain(&crossing)`, `test result: FAILED. 0 passed; 1 failed`.

복원 전 기준/복원 후 SHA-256: `6FEB1EE983EAADDFE60B544ADDB5D575516EBE2E3E0026500211A410B868D2`.

복원 후 동일 명령: `1 passed; 0 failed`.

### M3 — stale snapshot guard 제거

대상: `tool/src/lsp/server.rs`, `textDocument/selectionRange` snapshot identity guard.

Exact diff:

```diff
-            if requested_identity != snapshot.identity.as_str() {
+            if false && requested_identity != snapshot.identity.as_str() {
```

명령:

```text
cargo test -p ddonirang-tool --test lsp_open_document_navigation lsp17_selection_ranges_are_ordered_ast_parent_chains_and_current --offline -- --nocapture
```

RED 핵심: `assertion failed: matches!(... error.code == -32802)`, `test result: FAILED. 0 passed; 1 failed`.

복원 전 기준/복원 후 SHA-256: `6AE454A03E3E821A69B66E89DAC716E2F101C29EB60C47FF9D0F6E3B07AEAF3D`.

복원 후 동일 명령: `1 passed; 0 failed`.

세 mutation 모두 한 번에 하나만 적용했고, 다음 mutation 전에 exact restore hash를 확인했다. mutation residue는 없다.

## custody

- `tool/src/lib.rs` 변경: 0
- 새 dependency/pack/runner/meta-test/worktree/task: 0/0/0/0/0
- push: 수행하지 않음
- author/committer: `tongosu <tongosu@myarts.kr>`
- prohibited trailer: 0
- foreign dirty path: 수정·format·stage하지 않음
- product fixed commit은 LSP16 handoff 위에만 추가되었다.

## 다음 owner

동일 target에 대한 독립검토를 요청할 수 있다. 다음 자동 진행 후보는 기존 shared owner와 의미 authority가 이미 있는 LSP 후속 기능 중 하나를 별도 atomic unit으로 선택하며, LSP17 correction이 반환되면 successor finalization보다 LSP17 correction을 우선한다.
