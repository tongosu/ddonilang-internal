# DDN execution concurrency W1-C Owner 결정 패킷

## 상태

```text
PACKET_ID: DDN_EXECUTION_CONCURRENCY_W1C_SENDER_FILTER_AND_REACTION_PROVIDER_OWNER_DECISION_PACKET
STATUS: OWNER_DECISION_REQUIRED_BEFORE_W1C
W1C_NOT_STARTED
NO_PUBLIC_SURFACE_ADDED_BY_W1B
```

W1-B 구현에는 sender-filter 또는 ReactionProvider public surface 결정이 필요하지 않았고
어떤 후보 surface도 제품에 추가하지 않았다. 이 문서는 후속 owner 판단의 경계를
보존하기 위한 패킷이다.

## 결정이 필요한 항목

| 영역 | owner가 확정할 것 | W1-B에서 보존한 불변식 |
|---|---|---|
| semantic identity | consuming EndpointRoute sender-filter와 non-consuming ReactionProvider 구분 | provider는 EndpointRoute 이후 별도 fan-out |
| candidate surface | sender/filter/provider의 정확한 DDN 문형 | filename/path/handler 추측 금지 |
| parser ambiguity | 기존 받으면 문형과의 충돌 해소 | source/declaration order를 우선순위로 사용 금지 |
| provider key | kind/sender/receiver/payload 중 exact identity | physical ordering은 의미 순서가 아님 |
| dedup | 동일 provider 등록과 중첩 registration 규칙 | consuming route cardinality 0/1/>1 불변 |
| fan-out observation | order를 public 의미로 노출할지 여부 | fan-out order 비의미성 유지 |
| migration | historical receive handler의 명시적 변환 경계 | automatic compatibility alias 금지 |
| parity | native/CLI/WASM/Workbench exact artifact | 공통 Rust frontdoor owner 유지 |
| authority | SSOT/public SPEC change 필요 여부 | W1-B는 둘 다 변경 0 |

Owner 결정 전 W1-C parser/runtime/public wire 구현을 시작하지 않는다.
