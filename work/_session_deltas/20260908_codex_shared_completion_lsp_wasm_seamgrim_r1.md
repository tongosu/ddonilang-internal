# DDN-SHARED-COMPLETION-LSP-WASM-SEAMGRIM-R1 — handoff

## 작업 계약

- AI_PROVIDER: OpenAI
- AI_SURFACE: Codex VSCode Work
- SESSION_NICKNAME: 자동완성 Work
- PROJECT_ROLE: SINGLE_WRITER
- DEEP_RESEARCH_CHECK: NOT_USE
- PUSH: NO
- SSOT_CHANGE: 0
- PUBLIC_SPEC_CHANGE: 0
- NEW_DEPENDENCY: 0

## 기준과 커밋

- implementation base 포함 기준: `54070b7362dd48f9c977ef835bb0f36fc478641d`
- worktree: `I:\home\urihanl\ddn\codex\build\worktrees\ddn-p-v1-project-ux-r2-census-r1-20260828`
- branch: `codex/ddn-v1-p1a-core-supported-ingress-w1-20260829`
- Unit A product commit: `a07e0059bc88090620adf54a64a9205ecc0b5ccc`
- Unit A parent/tree: `a51005f3eac05051ceac3c681c7a9cad40e621e3` / `f4aa77062af031cc34a44436185ab1a9a763c5f5`
- Unit B product commit: `f3b966fcc01ad7053d46029242d1035a9b086bc6`
- Unit B parent/tree: `a07e0059bc88090620adf54a64a9205ecc0b5ccc` / `504a920ed4a6ad6d0ea4b9f182f075078d6c7603`
- Unit A/B author and committer: `tongosu <tongosu@myarts.kr>`
- product commits have no trailers and were not pushed.

## 구현

`tool/src/completion.rs`가 DocumentStore snapshot, version, UTF-8/UTF-16/UTF-32 position, current DDN parser/stdlib registry를 결속하는 단일 deterministic owner다. local top-level definition과 current registered stdlib callable만 제안하며 string/comment/number/type-schema/legacy/불확실 문맥은 빈 목록으로 닫는다. 정렬 key는 candidate kind, UTF-8 label bytes, definition identity다.

LSP는 `textDocument/completion`에서 이 결과를 그대로 `CompletionItem`으로 감싼다. WASM은 기존 `wasm_project_authoring_completion_json` frontdoor의 `ddonilang.completion.v1-candidate` schema 분기로 같은 owner 결과를 structured projection한다. Workbench JS는 새 semantic engine을 두지 않고 기존 runtime bridge와 textarea를 사용해 120ms debounce, version/generation stale discard, listbox option, ArrowUp/ArrowDown, Enter/Tab, Escape, click, exact replacement range를 제공한다. completion은 runtime/state/receipt를 변경하지 않는다.

## 검증

- `cargo test --offline -p ddonirang-tool --test lsp_completion`: 15 passed
- `cargo test --offline -p ddonirang-tool --test lsp0_transport_document_sync`: 22 passed
- existing `python tests/run_lsp0_transport_document_sync_check.py` with current target: PASS (I1~I8/RB06/RB08)
- aligned validation snapshot `cargo check --offline -p ddonirang-tool --bin ddonirang-lsp`: PASS
- aligned validation snapshot `cargo check --offline -p ddonirang-tool --features wasm`: PASS
- `node --check` runtime bridge/workbench: PASS
- regenerated tracked WASM direct Node load and `wasm_project_authoring_completion_json` structured response: PASS
- `git diff --check`: PASS
- existing Workbench Playwright runner: ENVIRONMENT_BLOCKED (`Cannot find package 'playwright'`); no dependency download or workaround performed.

The direct product-worktree `cargo check -p ddonirang-tool --bin ddonirang-lsp` remains blocked by pre-existing foreign dirty `lang/src/model.rs`, `lang/src/parser.rs`, `lang/src/runtime.rs`, and `lang/src/stdlib.rs` API mismatch. Those files were not changed, staged, or committed.

## Mutation evidence

### Unit A

- M-A1: `tool/src/completion.rs` deterministic label comparator reversed. RED: `c_a10_repeat_is_byte_stable`; exact restore hash `4482FBE5A977FC868F7BB4948495D6D721579BF35EB43A8CCA1D33998D0EFB00`; same test GREEN.
- M-A2: completion adapter used `PositionEncoding::Utf8` instead of negotiated encoding in `tool/src/lsp/server.rs`. RED: `c_a05_lsp_replacement_range_is_exact` (`left: Null`, `right: "첫함수"`); exact source restore; same test GREEN.
- M-A3: removed `in_comment` guard in `tool/src/completion.rs`. RED: `c_a06_string_and_comment_contexts_are_empty`; exact restore hash `4482FBE5A977FC868F7BB4948495D6D721579BF35EB43A8CCA1D33998D0EFB00`; same test GREEN.

### Unit B

- M-B1: structured projection inserted `.skip(1)` and dropped one candidate. RED: `c_b01_structured_wasm_projection_matches_lsp_candidates`; exact restore to completion source hash `A2C6BFBC8500CAFB79C9E3ACF2C2D9CB62FFF287EEC514B56767F6FE5FD81E20`; same test GREEN.
- M-B3: structured projection changed replacement range start to byte zero. RED: same parity test; exact restore to the same source hash; same test GREEN.
- M-B2 UI stale-result mutation was not claimed because the existing browser runner could not load without the preinstalled Playwright package. The production guard remains present and is covered by source inspection plus the non-browser Rust parity tests.

## custody

- `tool/src/wasm_api.rs` had no pre-existing dirty hunk and no active wasm writer/process was observed before Unit B admission.
- Product commits staged only owned paths. Foreign tracked dirty lang files and four protected pre-existing untracked session deltas remain untouched.
- No new runner, pack, meta-test, dependency, branch, worktree, reviewer, tag, force push, or history rewrite was created.
