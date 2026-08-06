# 결정론 계약 — Language SPEC v0.4.0 후보

> 상태: `public candidate / not current / docs-first / product-open`
> trace: Language SPEC `v0.4.0` candidate ← internal live SSOT `v24.22.1`
> 현 공개판: Language SPEC `v0.3.0` (고정판, 불변)
> 권위: 충돌하면 internal live SSOT가 우선한다.
> 제품 경계: 문서 정본과 parser/runtime/default-product 지원을 분리한다.

## 이름형과 위치형 값꾸러미

- 위치형은 위치와 값이 equality·stable typed-meaning hash에 참여한다.
- 이름형은 같은 semantic kind와 필드 이름·값이면 작성 순서와 무관하게 같다.
- 이름형 hash는 NFC field-name UTF-8 bytes 오름차순으로 계산한다.
- schema record 정본은 선언 순서, 열린 record 정본은 field-name 순서다.
- 관찰·표·범례의 표시 순서는 별도 `field_order`로 보존한다.
- parser 혼합 유실·중복 이름·필드 수 유실은 금지 계약이지만 제품 P1은
  아직 `NOT FIXED`다.

## 수 반올림

명시 반올림, exact→`셈수`, Fixed64 곱셈·나눗셈, 단위 환산, solver
입출력 양자화는 `roundTiesToEven`을 사용한다. 0 분모와 overflow는 실패다.
일부 경계만 구현한 상태를 전체 계약 완료라고 부르지 않는다.

## 글·자료·증거

- 글은 자동 NFC를 하지 않으며 normalization은 명시 API다.
- BOM은 data이고 자동 인코딩 감지·locale fallback·BOM 제거를 금지한다.
- dataset hash와 evidence hash는 별도로 계산해 binding identity에 함께 묶는다.
- 공개 식별자는 허용된 exact field만 쓰고 import·실행·표시 중 자동 fetch하지 않는다.
- present·gap·missing·pruned와 run failure를 분리한다.

## 함수·순환·실행

- 함수 graph·갈무리·효과·씨맞춤을 봉인할 수 없으면 직렬화·replay를 금지한다.
- 정적으로 완전히 아는 세움·매마디 순환은 canon에서 거부한다.
- 동적 경계만 runtime guard를 쓰며 숨은 고정점 반복·재시도·선언 순서
  타이브레이크를 하지 않는다.
- 세계 마디, solver 내부 step, 출력 schedule, renderer frame을 분리한다.
- accepted commit 전 표본 공개와 silent solver fallback을 금지한다.

## 관문과 완료 주장

관문 PASS는 다음 단계 진입 자격이다. runtime landed, behavior-closed,
운영 실증, corpus 완료, 외부 사용자 성공을 서로 대신하지 않는다.
