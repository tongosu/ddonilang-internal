# 또니랑 V1 제품 지원표 — PRE_RELEASE

```text
PRODUCT_RELEASED=NO
EXTERNAL_USER_COUNT=0
SUPPORTED_FOR_V1_COUNT=0
PRODUCT_PASS_MEMBERSHIP_PENDING_COUNT=0
```

## 상태 뜻

| 상태 | 뜻 |
|---|---|
| `V1_PLANNED` | V1 후보 범위이나 membership·제품 폐쇄가 아직 없음 |
| `PRODUCT_IMPLEMENTED_UNDER_REVIEW` | 제품 구현 slice가 있으나 fixed-target 독립 PASS 또는 V1 편입이 미완료 |
| `PRODUCT_PASS_MEMBERSHIP_PENDING` | 해당 공개 행의 required product gate에 대한 fixed-target 독립 PASS는 있으나 V1 membership이 아직 승인되지 않음. 공식 지원은 아님 |
| `SUPPORTED_FOR_V1` | 승인된 V1 membership과 독립 제품 PASS를 모두 가진 공식 지원 표면 |
| `UNSUPPORTED_IN_V1` | V1 지원범위에 포함하지 않음. 역사·후속 연구를 폐기한다는 뜻은 아님 |
| `DEFERRED` | 후속 버전 또는 별도 capability gate로 미룸 |

public Language SPEC v0.6.0에 존재한다는 사실만으로 `SUPPORTED_FOR_V1`이 되지 않는다.

지원 상태와 제품 근거는 서로 다른 축이다. 제한된 구현·독립 PASS를 가진 하위 slice가 있어도
공개 행 전체의 required gate가 닫히지 않았다면 그 행을
`PRODUCT_PASS_MEMBERSHIP_PENDING`으로 올리지 않는다. 현재 이 상태의 행은 0개다.

## V1-Core surface

| ID | surface | 상태 | 제품 지원 판정 근거 |
|---|---|---|---|
| VC01 | 한국어 기본 원문 | `V1_PLANNED` | P1 fixed-target census 대기 |
| VC02 | Definition `:=` | `V1_PLANNED` | internal partial evidence는 membership이 아님 |
| VC03 | Binding/Rebinding `<-` | `V1_PLANNED` | multi-path partial evidence 재검토 필요 |
| VC04 | 기본 값·씨·identity | `V1_PLANNED` | authoritative subset 미확정 |
| VC05 | 정확수·기본 결정적 수치 | `V1_PLANNED` | numeric product profile 미확정 |
| VC06 | 글·바이트·NFC | `V1_PLANNED` | exact product boundary 미확정 |
| VC07 | Product | `V1_PLANNED` | physical 조각과 V1 support를 분리 |
| VC08 | Sum·optional·typed result | `V1_PLANNED` | physical 조각과 V1 support를 분리 |
| VC09 | named callable | `V1_PLANNED` | ResultPlace·callable vertical 재검토 필요 |
| VC10 | ResultPlace | `V1_PLANNED` | definite-result·publish 제품 폐쇄 대기 |
| VC11 | 조건·반복 | `V1_PLANNED` | 제한된 scoped PASS는 전체 축 PASS가 아님 |
| VC12 | 기본 collection | `V1_PLANNED` | exact V1 collection subset 미확정 |
| VC13 | typed Selection | `V1_PLANNED` | strict/safe 제품 계약 검증 대기 |
| VC14 | Basic Tensor R1 | `V1_PLANNED` | shared product vertical 없음 |
| VC15 | 한국어 활용형 | `V1_PLANNED` | current morphology 제품 근거 rebase 필요 |
| VC16 | closed multisurface·canon | `V1_PLANNED` | shared canon authority 폐쇄 대기 |
| VC17 | 기본 stdlib | `V1_PLANNED` | exact membership은 census+Owner gate 뒤 결정 |
| VC18 | 기본 diagnostics | `V1_PLANNED` | public diagnostic contract 미확정 |

## 현재 결속된 제품 근거의 범위

다음 표는 실제 근거를 숨기지 않기 위한 evidence projection이며 V1 support status가 아니다.

| ID | 결속된 근거 | 검증된 범위 | 아직 부족한 것 |
|---|---|---|---|
| VC01 | Wave0 census, FD01A internal route, FD01B hidden candidate route | 일부 source-epoch·candidate ingress | public/default V1 ingress와 required frontdoor 전체 재결속 |
| VC02 | FD01A internal typed core independent PASS | internal native/WASM adapter의 Definition slice | default/public/Workbench editable ingress |
| VC03 | G14 제한 parity와 assignment 역사 근거 | 일부 Binding/Rebinding 경로 | current public/default·official CLI 전수와 행 전체 독립 PASS |
| VC09 | parser/AST/runtime source census | 이름 있는 callable 구현 조각 | current ResultPlace·definite result·atomic publish 전 제품 수직 |
| VC18 | structured diagnostic·Workbench/Edge의 제한 보고 근거 | 일부 진단·표시 slice | 전체 surface의 span·cause·frontdoor parity와 행 전체 독립 PASS |

위 다섯 행은 근거가 0인 행으로 축소하지 않지만, required gate 전체의 fixed-target PASS가
아니므로 계속 `V1_PLANNED`다.

## 실행계약

| ID | 계약 | 상태 | 제품 지원 판정 근거 |
|---|---|---|---|
| VE01 | deterministic execution | `V1_PLANNED` | 공식 경로 전수 검증 대기 |
| VE02 | state/result identity | `V1_PLANNED` | shared identity·receipt 폐쇄 대기 |
| VE03 | internal receipt/replay | `V1_PLANNED` | capability-relative 제품 근거 대기 |
| VE04 | fail-closed·no silent fallback·partial publish 0 | `V1_PLANNED` | 공식 frontdoor 합성 검증 대기 |

## V1-Core 자동 제외

| capability | 상태 |
|---|---|
| anonymous callable | `UNSUPPORTED_IN_V1` |
| recursion | `UNSUPPORTED_IN_V1` |
| generic·구실 | `UNSUPPORTED_IN_V1` |
| Regex | `UNSUPPORTED_IN_V1` |
| Proof | `UNSUPPORTED_IN_V1` |
| State Machine | `UNSUPPORTED_IN_V1` |
| AI collaboration | `UNSUPPORTED_IN_V1` |
| advanced model·solver·graph | `UNSUPPORTED_IN_V1` |
| self-hosting | `UNSUPPORTED_IN_V1` |
| 2D observation/creation | `UNSUPPORTED_IN_V1` |

최초 V1에서 recursion은 공식 지원하지 않는다. bounded/direct/mutual recursion의 새 의미를 이
문서가 정하지 않으며, 공식 ingress는 recursion을 silent host-stack failure로 흘리지 않고
명시적 unsupported diagnostic으로 거부하는 방향을 따른다. 그 diagnostic의 제품 착지와 독립
PASS는 아직 OPEN이다.

## 승격 규칙

한 행을 `SUPPORTED_FOR_V1`로 바꾸려면 최소한 다음을 고정한다.

1. Owner 승인 V1 membership
2. required target profile과 closure gate
3. implementation commit 또는 release artifact identity
4. 원문 기반 focused test와 회귀 검증
5. 필요한 frontdoor parity
6. fixed-target independent product PASS
