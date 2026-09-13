# DDN execution concurrency W1-C1 독립 검토 요청서

## fixed HEAD와 판정 경계

```text
GOAL_ID: DDN_EXECUTION_CONCURRENCY_W1C_TO_W1F_ASYNC_CLOSURE_ULTRA_W1
W1B_CLOSE_BASELINE: c61bdfef7a6eb1547f2d95807f946fb3c571fe43
PRODUCT_FIXED_HEAD: da791953f51a38e9489d0b2a158eeb419645fd43
REVIEW_FIXED_HEAD: e613537706b45b184f3615a43cde824a78b71eb3
REVIEW_MODE: FIXED_HEAD_READ_ONLY
ALLOWED_VERDICT: PASS / PASS_WITH_FOLLOW_UP / REWORK
```

검토자는 `REVIEW_FIXED_HEAD`를 격리된 clean-detached worktree에서 읽기 전용으로
재현한다. 제품 코드, pack, oracle, 기대값과 기존 구현 보고서를 수정하지 않는다.
Codex의 구현 보고는 독립 판정이 아니다.

## 검토 범위

1. W1-B plain PASS 결속 commit `c61bdfef...`이 구현 계보의 ancestor이고
   `c61bdfef..e6135377` merge commit이 0인지 확인한다.
2. exact surface `철수에게서 (받은수:수)를 받으면 { ... }.`가 sender predicate이며,
   sender-filter 없는 exact typed receive가 `ANY_SENDER`인지 직접 재현한다.
3. explicit sender가 envelope에 보존되고 owner 문맥 omitted sender는 owner identity를
   사용하며, top-level omitted sender는 `누리` 또는 임의 identity 없이 fail-closed하는지
   확인한다.
4. RouteIdentity가 receiver/message type/canonical sender predicate/payload predicate/
   module-owner identity로 도출되고 source span/declaration order/vector/worker order를
   포함하지 않는지 확인한다. 동일 consuming route 2+는 dedup이 아니라 ambiguity여야 한다.
5. successor consuming route가 exact typed receive만 수집하며 historical receive hook,
   `~~>`와 기존 corpus를 successor route/provider로 자동 해석하거나 일괄 rewrite하지
   않았는지 확인한다.
6. 내부 ProviderIdentity/registry/occurrence authority가 diamond once-per-occurrence,
   distinct provider fan-out, nested fresh dedup set과 route-first gate를 지키는지 확인한다.
   public ReactionProvider 선언 문법이나 stable wire가 추가되지 않아야 한다.
7. unhandled, ambiguity, sender-identity, provider-identity, bounded WAIT가 구조화된
   product-local candidate code/phase/source span으로 구분되는지 확인한다. 이 candidate를
   public stable diagnostic authority로 승격하지 않았는지도 확인한다.
8. lang 357, tool 491, teul-cli shared runtime, 10-case native/source-WASM/tracked-WASM
   exact parity와 failure atomicity를 clean-detached에서 직접 재현한다.
9. oracle mutation이 RED를 만들고 원복 뒤 GREEN인지, source-built/tracked/browser WASM이
   5,467,851 bytes와 SHA-256
   `7106d312993408029404db967d100fdb6838192daef9e38bc45e2aa8acd7a6e7`로 수렴하는지 확인한다.
10. 가능한 독립 실제 Edge 순환으로 success output, mismatch candidate code/phase/span과
    tracked WASM identity를 확인한다.
11. `docs/ssot/**`, public SPEC, W1-B predecessor pack, Graph W1, RD-204 R3, UI source,
    공식 store와 activation endpoint가 보호되었는지 확인한다.

## 필수 재현 명령

격리 target과 WASM staging 경로를 사용한다.

```text
cargo test -p ddonirang-lang -q
cargo test -p ddonirang-tool --lib -q
node tests/ddn_execution_concurrency_w1c1_sender_route_provider_runner.mjs
node tests/check_wasm_runtime_freshness.mjs
git diff --check
```

runner가 요구하는 source-built CLI/WASM 준비 절차와 expected oracle mutation 검증도
요청서 및 pack README에 따라 별도로 재현한다. 테스트를 통과시키기 위한 expectation,
진단, runtime 의미 완화는 허용하지 않는다.

## 보호 상태와 결과물

공식 DB의 기준은 573,440 bytes, SHA-256
`3fbf028e852dd3a13c3b84f812254de30c55113140f2b7869ff81a2a3b2b65f0`이다. 보호 PID
`53196`, start `2026-08-08T12:27:21.8634297+09:00`, `127.0.0.1:8787`을 침범하지
않는다. 공식 store write와 activation call은 0이어야 한다.

독립 결과는 새 `work/claude/.../REVIEW_RESULT.md`에 직접 재현 근거와 함께 기록하고
별도 review commit으로 결속한다. `PASS_WITH_FOLLOW_UP` 또는 `REWORK`이면 우회하지 않고
즉시 해당 상태에서 중단한다. plain `PASS` 전에는 다음 상태를 유지한다.

```text
DDN_EXECUTION_CONCURRENCY_W1C1_SENDER_ROUTE_INTERNAL_PROVIDER_IMPLEMENTED_UNDER_REVIEW
W1C1_INDEPENDENT_PASS_NOT_YET_ISSUED
W1C2_REACTION_PROVIDER_PUBLIC_SURFACE_OPEN
RD207_PUBLIC_STABLE_WIRE_OPEN
W1_FULL_CLOSURE_OPEN
PUBLIC_ACTIVATION_NOT_AUTHORIZED
HUMAN_PASS_NOT_CLAIMED
```
