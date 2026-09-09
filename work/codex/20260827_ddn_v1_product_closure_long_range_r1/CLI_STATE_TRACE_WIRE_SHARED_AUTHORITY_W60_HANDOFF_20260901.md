# CLI state/trace wire 공유 권위 W60 인계

## 계보와 범위

- goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` ACTIVE
- authority: internal SSOT v25.47.0 / RD-001~543, public SPEC v0.6.0
- baseline: `0f3fcf68d0c69b07f23b162bdbe8a2acb9e590c2`
- product fixed: `21a8662a58b0a593150a5c56378757950e3e3f12`
- fixed tree: `c3fdaceeb8f897ef5981bd3433bfef62d043bd66`
- direct parent exact, merge count 0

`DDN_STATE_V1` canonical-entry byte wire와 `DDN_TRACE_V1` source/output byte wire를 `ddonirang-tool::state_trace_wire`의 shared authority로 이동했다. teul `core/detbin.rs`는 private `State`/`TraceEvent`를 canonical entry/output iterator로 투영하는 adapter만 유지한다. header, key order, separators, seed formatting과 backslash/LF/CR/tab escaping은 기존 bytes를 보존한다.

## 변경 경로와 검증

1. `tool/src/state_trace_wire.rs`
2. `tool/src/lib.rs`
3. `tools/teul-cli/src/core/detbin.rs`

- shared exact byte contract: 1/1 PASS
- existing teul run consumer: 1/1 PASS
- teul offline cargo check: PASS
- teul full regression: 1043 PASS / 기존 동일 9 FAIL; new drift 0
- newline escape bypass mutation: actual RED exit 101, 0/1
- exact restore SHA-256: `169e42fe0eb9ad27d1d04e2edec558433c672d5a93e194fa29530d241cf9d722`
- restore GREEN: shared 1/1 + existing consumer 1/1
- mutation residue 0, partial publish change 0, `git diff --check` PASS
- new pack/runner/framework/meta-test/reviewer/worktree/branch 0
- tracked WASM/UI/SSOT/SPEC/public command or membership diff 0

## gate 영향과 남은 경계

- USER_WORKFLOW_CHANGED_OR_UNBLOCKED: run/docset/repl/Geoul이 소비하는 state hash와 trace bytes가 private teul wire encoder가 아니라 shared product authority에서 생성된다.
- DUPLICATE_AUTHORITY_ELIMINATED: teul-private state/trace byte framing and escaping family 1.
- remaining teul semantic custody: `State`, `Value::canon`, Fixed64/unit/value/runtime와 Bogae adapter. 이들의 의미를 existing code만으로 shared authority로 승격하지 않는다.
- REVIEW_BUNDLE_TARGET: W53~W60 coherent internal/deferred CLI authority convergence.

Status is `IMPLEMENTED_PENDING_REVIEW`. Whole teul authority/dependency 0, public retirement, V1 closure/readiness/release/activation/Human PASS를 주장하지 않는다.
