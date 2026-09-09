# DDN execution concurrency W1-C1 구현 인계

## 상태와 고정점

```text
GOAL_ID: DDN_EXECUTION_CONCURRENCY_W1C_TO_W1F_ASYNC_CLOSURE_ULTRA_W1
W1B_CLOSE_BASELINE: c61bdfef7a6eb1547f2d95807f946fb3c571fe43
W1C1_PRODUCT_FIXED_HEAD: da791953f51a38e9489d0b2a158eeb419645fd43
DDN_EXECUTION_CONCURRENCY_W1C1_SENDER_ROUTE_INTERNAL_PROVIDER_IMPLEMENTED_UNDER_REVIEW
W1C1_INDEPENDENT_PASS_NOT_YET_ISSUED
W1C2_REACTION_PROVIDER_PUBLIC_SURFACE_OPEN
RD207_PUBLIC_STABLE_WIRE_OPEN
W1_FULL_CLOSURE_OPEN
PUBLIC_ACTIVATION_NOT_AUTHORIZED
HUMAN_PASS_NOT_CLAIMED
```

## 2026-08-22 후속 독립 PASS 결속

이 문서의 위 상태는 원 구현 인계 시점 기록이다. F1 correction `2e080cdb...`와
targeted rereview request `53ec44bd...` 뒤 Claude review commit `c8b0f3d...`가 plain
`PASS`를 발행했고 successor branch에 `--ff-only`로 결속됐다. exact closure scope와
보호 경계는
`work/codex/20260822_ddn_execution_concurrency_w1c1_independent_pass_closure/W1C1_LIMITED_SCOPE_CLOSURE.md`가 소유한다. F2, W1-C2, W1 full closure는 OPEN이다.

기존 목표를 W1-B plain PASS 결속 뒤 이어서 수행했다. 새 목표나 의미 계보를 만들지
않았다. 이 문서는 Codex 구현·직접 검증 인계이며 독립 판정이 아니다.

## Owner 결정 반영

- exact sender-filter surface는
  `철수에게서 (받은수:수)를 받으면 { ... }.`이다.
- sender filter가 없는 `(받은수:수)를 받으면`은 `ANY_SENDER`다.
- 명시 sender는 기존 message sender surface `(철수)의 payload ~> receiver`로 envelope에
  보존된다.
- owner 문맥 안 omitted sender는 owner identity를 사용한다. owner 문맥 밖 omitted
  sender는 임의 identity나 `누리`를 만들지 않고 fail-closed한다.
- successor consuming route는 exact typed receive만 수집한다. historical receive hook과
  `~~>` corpus는 자동 successor route/provider로 승격하지 않았다.
- W1-C1에는 public ReactionProvider 선언 문법, stable wire, public diagnostic authority를
  추가하지 않았다.

## typed semantic authority

`lang/src/delivery.rs`가 다음 공통 구조를 소유한다.

- `RouteIdentity`, `EndpointRouteSemantic`, `EndpointRoute<T>`
- `SenderIdentityPredicate::{AnySender, Exact}`
- `ProviderIdentity`, `ReactionProvider<T>`, `ReactionProviderRegistry<T>`
- `DeliveryOccurrence`, `plan_delivery_occurrence`

RouteIdentity는 receiver, message type, canonical sender predicate, payload predicate,
module/owner identity를 domain-separated BLAKE3 material로 결합한다. source span,
declaration/vector/worker order는 identity material이 아니다. 동일 identity route 둘은
dedup하지 않아 ambiguity로 남는다.

ProviderIdentity는 canonical module/owner와 stable declaration semantic identity로
도출한다. registry duplicate/unknown key는 fail-closed한다. diamond reach key는 한
delivery occurrence 안에서 한 번만 resolve되고 distinct key는 모두 fan-out된다. nested
occurrence는 새 key set을 가진다. canonical order는 trace/검증 표현일 뿐 언어의 물리
실행 순서 보장이 아니다.

제품 runtime은 exact-one route를 결정한 뒤 빈 내부 provider registry라도 이 공통
occurrence planner를 반드시 통과한다. public provider declaration이 없으므로 W1-C1
DDN source에서 provider를 등록하는 경로는 없다.

## runtime과 진단

- exact builtin payload type과 user-defined `알림씨` envelope type을 구분한다.
- sender/type mismatch는 candidate 집합에서 제외한다.
- 0 route는 `E_ASYNC_ENDPOINT_UNHANDLED_CANDIDATE`다.
- 2+ route는 `E_ASYNC_ENDPOINT_AMBIGUOUS_CANDIDATE`다.
- sender identity 불명은 `E_ASYNC_SENDER_IDENTITY_UNRESOLVED_CANDIDATE`다.
- provider identity 오류는 `E_ASYNC_PROVIDER_IDENTITY_CANDIDATE`다.
- bounded full은 `E_ASYNC_QUEUE_WAIT_REQUIRED_CANDIDATE`이며 성공/drop으로 바꾸지 않는다.
- candidate JSON은 `async_sender_identity`, `async_route`, `async_provider`,
  `async_queue_wait` phase와 non-empty send source span을 가진다.

이 code/phase는 product-local candidate다. W1-C2 public diagnostic authority나 stable
wire를 닫지 않는다.

## 선형 commit 계보

```text
c61bdfef W1-B independent PASS close
57f3f5d3 W1-C1 Owner decision and migration map
963c7c88 typed sender/route/provider identities
d874dc0d semantic sender EndpointRoute runtime
1a6c2932 internal ReactionProvider occurrence authority
6bfbeee8 historical hook/successor exact-route separation
2ec750aa W1-C1 native/WASM oracle and tracked runtime
da791953 structured async candidate diagnostics
```

`c61bdfef..da791953` merge commit은 0이다.

## 검증 결과

| 검증 | 결과 |
|---|---:|
| `cargo test -p ddonirang-lang -q` | 357/357 PASS |
| `cargo test -p ddonirang-tool --lib -q` | 491/491 PASS |
| teul-cli 독립 manifest source build | PASS |
| W1-C1 oracle | 10/10, 성공 6·실패 4 PASS |
| native/source node WASM/tracked Workbench full summary·diagnostic parity | PASS |
| expected oracle mutation RED→원복→GREEN | PASS |
| tracked WASM freshness manifest | PASS |
| actual Microsoft Edge Workbench tracked WASM | PASS |
| clean-detached lang/tool/teul/native/WASM | PASS |
| clean-detached source-built web/tracked WASM raw bytes | identical |

최종 tracked/browser/clean-detached WASM:

```text
bytes: 5,467,851
SHA-256: 7106d312993408029404db967d100fdb6838192daef9e38bc45e2aa8acd7a6e7
```

실제 Edge에서 success output `7`, mismatch code
`E_ASYNC_ENDPOINT_UNHANDLED_CANDIDATE`, phase `async_route`, span `104..131`을 확인했다.
검증 서버/Edge profile은 격리했으며 서버 listener는 종료했다.

## 보호 경계

- `docs/ssot/**` diff 0
- `publish/spec/**` diff 0
- W1-B predecessor pack diff 0
- Graph W1·RD-204 R3 ancestry 병합 0
- UI source/behavior diff 0; tracked common-Rust WASM artifact만 currentize
- official store write 0, activation call 0
- 공식 DB 573,440 bytes, SHA-256
  `3fbf028e852dd3a13c3b84f812254de30c55113140f2b7869ff81a2a3b2b65f0`
- PID `53196`, start `2026-08-08T12:27:21.8634297+09:00`, port `8787` 유지

## OPEN

```text
W1C1_INDEPENDENT_PLAIN_PASS: PENDING
W1C2_REACTION_PROVIDER_PUBLIC_SURFACE: OPEN
RD207_PUBLIC_STABLE_WIRE: OPEN
W1D_SHARED_LOGICAL_DELIVERY_FULL_CONVERGENCE: NOT_CLAIMED
W1E_WAIT_STAGED_OUTBOX: NOT_CLAIMED
W1F_65_CASE_ORACLE_AND_WORKER_PERMUTATION: NOT_CLAIMED
RENDEZVOUS_RUNTIME: OPEN
PUBLIC_ACTIVATION_NOT_AUTHORIZED
HUMAN_PASS_NOT_CLAIMED
```
