# 또니랑 V1 언어 안내 — PRE_RELEASE

이 문서는 V1-Core 후보의 사용자 관점 목차다. SSOT나 Language SPEC을 대체하지 않으며, 아래 항목의 제품 지원을 선언하지 않는다.

## V1-Core 후보 18축

| ID | 사용자 관점 영역 | 현재 문서 상태 |
|---|---|---|
| VC01 | 한국어 기본 원문 | `V1_PLANNED` |
| VC02 | Definition `:=` | `V1_PLANNED` |
| VC03 | Binding/Rebinding `<-` | `V1_PLANNED` |
| VC04 | 기본 값·씨·identity | `V1_PLANNED` |
| VC05 | 정확수·기본 결정적 수치 | `V1_PLANNED` |
| VC06 | 글·바이트·NFC | `V1_PLANNED` |
| VC07 | Product | `V1_PLANNED` |
| VC08 | Sum·optional·typed result | `V1_PLANNED` |
| VC09 | named callable | `V1_PLANNED` |
| VC10 | ResultPlace | `V1_PLANNED` |
| VC11 | 조건·반복 | `V1_PLANNED` |
| VC12 | 기본 collection | `V1_PLANNED` |
| VC13 | typed Selection | `V1_PLANNED` |
| VC14 | Basic Tensor R1 | `V1_PLANNED` |
| VC15 | 한국어 활용형 | `V1_PLANNED` |
| VC16 | closed multisurface·canon | `V1_PLANNED` |
| VC17 | 기본 stdlib | `V1_PLANNED` — exact membership 미확정 |
| VC18 | 기본 diagnostics | `V1_PLANNED` |

각 축에는 일부 구현이나 제한된 제품 증거가 있을 수 있다. 그러나 축 전체의 V1 membership과 fixed-target 제품 PASS가 없으므로 `SUPPORTED_FOR_V1`로 올리지 않는다.

## 축별 안내 확장 틀

각 축이 V1 membership과 required product evidence를 얻으면 다음 순서로 사용자 안내를
확장한다.

1. 무엇인가
2. 언제 쓰나
3. verified syntax/example
4. 핵심 규칙
5. 대표 diagnostic
6. 관련 surface

현재 verified public example은 0개다. 위 제목은 문서 구조만 준비하며, 실행 근거가 생기기
전에는 syntax나 예제를 추측해 채우지 않는다.

## V1에서 자동 지원하지 않는 영역

다음은 기존 연구·구현·증거를 폐기한다는 뜻이 아니라, V1-Core 지원범위로 자동 편입하지 않는다는 뜻이다.

- anonymous callable
- recursion
- generic·구실
- Regex
- Proof
- State Machine
- AI collaboration
- advanced model·solver·graph
- self-hosting
- 2D observation/creation

현재 상태는 모두 `UNSUPPORTED_IN_V1`이다. 후속 공개판에서 별도 membership과 제품 근거가 생기면 재판정한다.

recursion은 최초 V1-Core에서 공식 지원하지 않는다. bounded/direct/mutual recursion의 세부
의미를 이 안내서가 추가하지 않으며, 제품은 silent host-stack failure 대신 명시적 unsupported
diagnostic으로 거부하는 방향이다. 이 diagnostic의 제품 착지와 독립 PASS는 아직 OPEN이다.

## 예제 정책

현재 이 안내서에 승인된 코드 예제는 없다. 예제는 원문 그대로 공식 제품 frontdoor에서 실행되고 canon·diagnostic까지 고정 검증된 뒤에만 추가한다.
