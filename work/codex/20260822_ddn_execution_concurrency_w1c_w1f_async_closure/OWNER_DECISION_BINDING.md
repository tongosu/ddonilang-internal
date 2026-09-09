# DDN execution concurrency W1-C1 Owner 결정 결속

## 계보와 범위

```text
GOAL_ID: DDN_EXECUTION_CONCURRENCY_W1C_TO_W1F_ASYNC_CLOSURE_ULTRA_W1
W1B_PRODUCT_FIXED_HEAD: 7610e4bfda5c322e65cf6df9a5af45e58e0ab4bf
W1B_REVIEW_COMMIT: 0d8ca402e90cea2688f38641bfb872e91a041d0a
W1B_CLOSE_COMMIT: c61bdfef7a6eb1547f2d95807f946fb3c571fe43
OWNER_DECISION: DDN_EXECUTION_CONCURRENCY_W1C_OWNER_DECISION_APPROVED
IMPLEMENTATION_SCOPE: W1-C1
W1-C2_REACTION_PROVIDER_PUBLIC_SURFACE: OPEN
RD207_PUBLIC_STABLE_WIRE: OPEN
```

W1-C1은 sender-filter, exactly-one EndpointRoute, typed internal
`ProviderIdentity`와 route 이후 provider fan-out 실행 기반까지만 구현한다. 새로운 공개
ReactionProvider 선언 문법, stable wire와 public diagnostic authority는 추가하지 않는다.

## Exact sender-filter surface

```ddn
철수에게서 (받은수:수)를 받으면 { ... }.
```

- `에게서` 앞의 식은 exact sender identity predicate다.
- `(받은수:수)를 받으면 { ... }.`는 `ANY_SENDER` consuming route다.
- 생략형을 특정 sender나 current owner로 해석하지 않는다.
- 명시적 sender는 envelope에 보존한다.
- owner 안의 sender 생략 전송은 그 owner identity를 사용한다.
- owner 밖에서 sender를 확정할 수 없으면 fail-closed한다. `누리` fallback과 임의 identity
  생성은 금지한다.

## Route identity

`RouteIdentity`는 다음 canonical semantic material로 구조적으로 도출한다.

```text
receiver identity
message type
canonical sender predicate
payload predicate
owning module/owner identity
```

source span, declaration order, vector index와 worker order는 identity material이 아니다.
의미상 같은 consuming route가 여러 번 등록돼도 dedup하지 않으며 cardinality ambiguity다.

## Internal provider boundary

- `ProviderIdentity`는 canonical module/owner identity와 provider declaration의 stable
  semantic identity로 구성한다.
- provider key는 `ProviderIdentity`와 동일한 semantic key다.
- 같은 delivery occurrence에서 diamond 경로로 같은 key가 여러 번 도달하면 한 번만
  관찰한다.
- 서로 다른 key는 전부 관찰한다.
- nested delivery occurrence는 바깥 dedup set을 공유하지 않는다.
- provider 실행 순서는 언어 의미가 아니다. deterministic trace는
  `ProviderIdentity` canonical order로 정렬할 수 있다.

historical `~~>`와 기존 multi-handler corpus는 migration evidence로 보존하며 successor
route/provider로 자동 해석하거나 일괄 rewrite하지 않는다.

## Candidate diagnostic phase contract

W1-C1 진단은 product-local structured candidate다. `E_ASYNC_ENDPOINT_*`를 public
stable authority로 승격하지 않는다.

```text
parse
route: unhandled | ambiguity | sender-identity-failure
provider: provider-identity-failure
queue/wait: bounded full is WAIT, not success/drop/completion
```

제품 구현은 W1-B plain PASS 결속 뒤에만 허용된다. 이 결속은 완료됐지만 SSOT/SPEC,
UI, deploy, activation, outreach는 승인되지 않았다.
