# DDN-LSP9 Semantic Tokens Full R1

## 작업 계약

```ini
AI_PROVIDER = Codex
AI_SURFACE = Work
PROJECT_ROLE = LSP product single writer
CURRENT_LSP_UNIT = LSP9_SEMANTIC_TOKENS_FULL
PUSH_PERFORMED = NO
GIT_AUTHOR = tongosu <tongosu@myarts.kr>
GIT_COMMITTER = tongosu <tongosu@myarts.kr>
```

LSP4와 LSP5의 기존 fixed target 및 검토 상태는 변경하지 않았다. 공유 root와 foreign dirty 경로는 수정·stage하지 않았다.

## 기준점

```ini
START_HEAD = 7181699c959558bda6baa921fa83714023fcd5b0
START_TREE = 312eb75b16496f5a99a9eace1d10f3a5bad49d5b
START_PARENT = fe0f745064c11b756ad336caf58dc5bbf1eaf513
```

## 구현

변경한 task-owned 경로는 다음 5개다.

```text
tests/run_lsp0_transport_document_sync_check.py
tool/src/lsp/mod.rs
tool/src/lsp/server.rs
tool/src/lsp/semantic_tokens.rs
tool/tests/lsp_semantic_tokens.rs
```

`semanticTokensProvider.full`과 기존 lexer/parser/stdlib registry를 사용하는 `textDocument/semanticTokens/full`을 추가했다. token legend는 function, type, variable, parameter, keyword, string, number, operator, atom, josa 순서이며, 결과는 UTF-16 negotiated position encoding과 source-order delta encoding을 사용한다. 현재 snapshot version과 snapshot identity를 응답에 결속하고 stale version/snapshot, malformed source, unknown/closed document은 fail-closed한다. 새 semantic identity, parser, registry, dependency는 추가하지 않았다.

## Mutation evidence

각 mutation은 한 번에 하나만 적용하고 focused test 후 원본을 즉시 byte-exact 복원했다.

### M1 — delta line state 제거

```diff
-let delta_line = range.start.line.saturating_sub(previous_line);
+let delta_line = 0;
```

RED:

```text
lsp9_full_tokens_use_lexer_categories_utf16_and_deterministic_delta ... FAILED
expected function token (1,19,3,0) was absent
```

복원 후 `tool/src/lsp/semantic_tokens.rs` SHA-256:

```text
8A673ECA6312F9783692184572579371B907A921E10AA29550F60DD0C6E7ACB3
```

복원 GREEN: focused LSP9 tests 2/2.

### M2 — UTF-16 range를 UTF-8 encoding으로 강등

```diff
-byte_range_to_lsp_range(source, range, encoding)
+byte_range_to_lsp_range(source, range, PositionEncoding::Utf8)
```

RED:

```text
lsp9_full_tokens_use_lexer_categories_utf16_and_deterministic_delta ... FAILED
expected function token (1,19,3,0) was absent
```

복원 후 semantic token source SHA-256:

```text
8A673ECA6312F9783692184572579371B907A921E10AA29550F60DD0C6E7ACB3
```

복원 GREEN: focused LSP9 tests 2/2.

### M3 — stale version guard 제거

```diff
-if requested_version != snapshot.version {
+if requested_version == snapshot.version {
```

RED:

```text
lsp9_full_tokens_use_lexer_categories_utf16_and_deterministic_delta ... FAILED
called Option::unwrap() on a None value
lsp9_full_tokens_stale_change_malformed_and_close_fail_closed ... FAILED
expected stale error -32801
```

복원 직후 `tool/src/lsp/server.rs` SHA-256:

```text
FEEE18470FECE9445E1A9945EF593AAA54368E46D53401850D0D4778955CD28
```

이후 task-owned 파일만 rustfmt를 적용했으며 최종 server SHA-256은 다음이다.

```text
F51A0BE0ED4F086902D37194CA9CF7924D3A7A48B9979CA4370C4AF73C655900
```

복원 GREEN: focused LSP9 tests 2/2.

## 검증

```ini
FOCUSED_TESTS = PASS 2/2
COMBINED_LSP_REGRESSION = PASS (39 tests)
BLACKBOX = PASS
ST18_BLACKBOX_SEMANTIC_TOKENS_BEFORE_EOF = PASS
LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK = PASS
RUSTFMT_CHECK = PASS
GIT_DIFF_CHECK = PASS
EXACT_RESTORE = PASS
```

현재 worktree의 `cargo check`는 LSP9 변경과 무관한 foreign `lang/**` dirty API mismatch(`UnitDim::AXIS_COUNT`, `UnitDim::exponents`, `UnitDim::from_exponents`, `Fixed64::parse_decimal_exact`)로 기존부터 차단되어 있다. 이 경로는 수정하지 않았다.

## 다음 단위

LSP10 cross-file navigation은 다음 authority가 fixed/reviewed 되기 전까지 시작하지 않는다.

```ini
LOCAL_PROJECT_DOCUMENT_REGISTRY = NOT_AVAILABLE
PROJECT_IDENTITY_OWNER = NOT_AVAILABLE
SAVE_REOPEN_SNAPSHOT_IDENTITY = NOT_AVAILABLE
NEXT_AUTONOMOUS_UNIT = BLOCKED_BY_PROJECT_INDEX_AUTHORITY
```

full semantic IDE, public extension release, V1 release 또는 Human PASS는 주장하지 않는다.
