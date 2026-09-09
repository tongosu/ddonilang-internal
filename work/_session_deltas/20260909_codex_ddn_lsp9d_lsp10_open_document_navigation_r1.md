# DDN-LSP9D-SEMANTIC-TOKENS-DELTA-AND-OPEN-DOCUMENT-NAVIGATION-R1

## Checkpoint

- 작업 기준 HEAD: `0cf0737806b7a32034e30ee4aa00503b195f5a75`
- 작업 기준 tree: `07b99d09ea06ed0a3cd52dc4d08f0a26c2adafed`
- 제품 fixed commit: `e6f015868acf425b3eb11cff3fe4c09e3f0e40b6`
- 제품 tree: `e5e12bf50a548e670d75d3b495166b4c1c989248`
- 제품 parent: `0cf0737806b7a32034e30ee4aa00503b195f5a75`
- Unit A/B는 `tool/src/lsp/server.rs`와 `tool/src/lsp/symbol.rs`의 공유 owner hunk가 겹친다. 이미 focused/regression/mutation 검증을 마친 변경을 두 commit으로 인위적으로 분리하지 않고 하나의 coherent product commit으로 고정했다. 이 문서는 별도 docs-only handoff다.

## Product scope

변경된 제품 경로는 다음 6개뿐이다.

```text
tests/run_lsp0_transport_document_sync_check.py
tool/src/lsp/semantic_tokens.rs
tool/src/lsp/server.rs
tool/src/lsp/symbol.rs
tool/tests/lsp_open_document_navigation.rs
tool/tests/lsp_semantic_tokens.rs
```

- LSP9D: deterministic `resultId`, `textDocument/semanticTokens/full/delta`, current snapshot binding, unknown/expired/foreign `previousResultId`의 current full fallback, didClose cache clear, URI별 열린 문서 cache 1개, token data bounded limit `100_000`.
- LSP10: 현재 `didOpen` 상태인 문서만 대상으로 definition/references를 조회한다. 기존 `DocumentStore`와 `symbol.rs` owner를 재사용하며, URI lexical order와 문서 내 source order를 보존하고 duplicate identity는 fail-closed한다.
- UTF-16 위치, Korean/emoji/multibyte 범위, didChange current snapshot, stale version `-32801`, stale snapshot `-32802`, didClose 제외, before-EOF 응답을 검증했다.
- filesystem crawl/read, hidden index, remote dependency, source upload, 새 parser/symbol owner, `tool/src/lib.rs` 변경, dependency/pack/runner/meta-test 추가는 없다.

## Mutation evidence

각 mutation은 한 번에 하나만 적용하고 즉시 byte-exact 복원했다. 모든 RED 뒤 동일 focused test를 GREEN으로 재실행했다.

### M1 — resultId document identity binding

- 대상: `tool/src/lsp/semantic_tokens.rs`, `result_id` hash hunk.
- 원본 hunk:

```rust
hasher.update((snapshot.uri.len() as u64).to_le_bytes());
hasher.update(snapshot.uri.as_bytes());
hasher.update(snapshot.version.to_le_bytes());
hasher.update(snapshot.identity.as_str().as_bytes());
```

- 임시 mutation: URI length/URI bytes/snapshot identity hash input을 제거하고 version/data만 hash하도록 변경.
- 실행: `cargo test -p ddonirang-tool --test lsp_semantic_tokens --offline --quiet`
- 기대/실제 RED: `lsp9d_delta_is_deterministic_bounded_and_reconstructs_current_stream` 실패. 다른 URI의 `resultId`가 달라야 하는 assertion에서 두 ID가 동일하여 `assert_ne!(other_id, first_result_id)`가 실패.
- 복원: 위 세 hash input을 원본대로 복원.
- 원본/복원 SHA-256: `32A97EFAAC5909288378ABA0CB7724DDEA7F531D2EF4CC0B71B9FEF51FD72B99`.
- 복원 후 GREEN: semantic-token focused tests `3 passed`.

### M2 — didClose semantic-token cache clear

- 대상: `tool/src/lsp/server.rs`, `did_close` hunk.
- 원본 hunk:

```rust
self.documents.close(uri).map_err(ServerError::Document)?;
self.semantic_tokens_cache.remove(uri);
Ok(uri.to_string())
```

- 임시 mutation: `self.semantic_tokens_cache.remove(uri);` 한 줄 제거.
- 실행: `cargo test -p ddonirang-tool --test lsp_semantic_tokens --offline --quiet`
- 기대/실제 RED: `lsp9d_delta_is_deterministic_bounded_and_reconstructs_current_stream` 실패. close/reopen 뒤 이전 result ID가 수용되어 full fallback 대신 delta가 반환되고 `reopened["data"].is_array()`가 false.
- 복원: `self.semantic_tokens_cache.remove(uri);`를 byte-exact 복원.
- 원본/복원 SHA-256: `4493889B37BD13795D21736813EA822A51066CAD3D8506CF2478D472864786E9`.
- 복원 후 GREEN: semantic-token focused tests `3 passed`.

### M3 — UTF-16 token range conversion

- 대상: `tool/src/lsp/semantic_tokens.rs`, token range conversion hunk.
- 원본 hunk:

```rust
            encoding,
```

- 임시 mutation: 위 `encoding`을 `PositionEncoding::Utf8`로 강등.
- 실행: `cargo test -p ddonirang-tool --test lsp_semantic_tokens --offline --quiet`
- 기대/실제 RED: Korean/emoji UTF-16 token position assertion에서 expected decoded function token `(1, 19, 3, 0)`이 없어져 실패.
- 복원: `PositionEncoding::Utf8`를 원래 request `encoding`으로 byte-exact 복원.
- 원본/복원 SHA-256: `32A97EFAAC5909288378ABA0CB7724DDEA7F531D2EF4CC0B71B9FEF51FD72B99`.
- 복원 후 GREEN: semantic-token focused tests `3 passed`.

## Validation

- LSP9D focused: `cargo test -p ddonirang-tool --test lsp_semantic_tokens --offline --quiet` — `3 passed`.
- LSP10 focused: `cargo test -p ddonirang-tool --test lsp_open_document_navigation --offline --quiet` — `2 passed`.
- LSP4~LSP10 regression: `cargo test -p ddonirang-tool --test lsp_semantic_tokens --test lsp_open_document_navigation --test lsp_document_highlight --test lsp_rename --test lsp_signature_help --test lsp_references --test lsp_document_symbol --test lsp_definition --test lsp_hover --test lsp_diagnostics --test lsp_completion --offline --quiet` — PASS.
- persistent transport black-box: `tests/run_lsp0_transport_document_sync_check.py` — `ST18_BLACKBOX_SEMANTIC_TOKENS_BEFORE_EOF=PASS`, `ST19_BLACKBOX_SEMANTIC_TOKENS_DELTA_BEFORE_EOF=PASS`, `ST20_BLACKBOX_OPEN_DOCUMENT_NAVIGATION_BEFORE_EOF=PASS`, final `LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS`.
- clean fixed snapshot: `cargo check --manifest-path I:/home/urihanl/ddn/codex/build/lsp9d-lsp10-clean-snapshot-r1/tool/Cargo.toml --offline` — exit `0`; existing warnings only.
- diff check: task-owned product diff clean; no format residue.
- author/committer: `tongosu <tongosu@myarts.kr>`.
- prohibited trailer count: `0`.
- push: `NO`.

## Boundary state

- `tool/src/lib.rs` changed: `0`.
- new dependency: `0`.
- source upload: `0`.
- remote dependency: `0`.
- filesystem crawl: `0`.
- cache bound: one current semantic-token resolution per open URI; no previous generations retained.
- foreign dirty paths: untouched and unstaged.
- task-owned dirty paths after product commit: `0`.
- staged paths before handoff commit: `0`.
- process residue: `0`.
- LSP6/LSP7/LSP8/LSP9 review state remains pending as supplied; no review verdict was inferred or changed.

## Next gate

Product fixed and handoff documentation are ready for independent review. No product promotion or push was performed. A subsequent LSP unit requires an explicit next-unit dispatch; this checkpoint does not invent or start another semantic owner.
