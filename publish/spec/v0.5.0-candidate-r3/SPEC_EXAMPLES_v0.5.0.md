# 정본 예제 — Language SPEC v0.5.0 후보

> 상태: `public candidate / independent review required / not current / docs-first / product-open`
> trace: Language SPEC `v0.5.0` candidate ← internal live SSOT `v24.24.1`
> 현 공개판: Language SPEC `v0.4.0` (고정판, 불변)
> 권위: 충돌하면 internal live SSOT가 우선한다.
> 제품 경계: 문서 후보와 parser/runtime/default-product 지원을 분리한다.

모든 예제 파일은 `docs-first / product-open`이다. 현재 기본 parser/runtime
실행 성공을 주장하지 않는다.

## 예제 목록

- [`01_result_and_optional.ddn`](./examples/01_result_and_optional.ddn)
- [`02_generic_static_header.ddn`](./examples/02_generic_static_header.ddn)
- [`03_bytes_and_exact_number.ddn`](./examples/03_bytes_and_exact_number.ddn)
- [`04_function_and_optional_map.ddn`](./examples/04_function_and_optional_map.ddn)
- [`05_pack_kinds.ddn`](./examples/05_pack_kinds.ddn)
- [`06_observation_and_mol.ddn`](./examples/06_observation_and_mol.ddn)
- [`07_common_model.ddn`](./examples/07_common_model.ddn)
  - `모형 {}`·`모형값`·닫힌 `::`·초기화와 출력 권한의 docs-first 예제.

## 읽는 순서

맺음과 `없음`을 먼저 구분하고, `두고`로 정적 머리와 실행 입력을 나눈다.
그 뒤 함수값·선택값 연산, 값꾸러미 두 종류, 공개 관찰과 단위를 읽고
마지막으로 공통 모형 선언을 읽는다.

exact graph module/export, `얼개 {}` migration, 새 구실 짧은 syntax와 제품
solver 수직은 OPEN이므로 실행 성공 예제로 주장하지 않는다.
