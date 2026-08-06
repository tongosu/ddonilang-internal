# 호환성·비주장 정책 — Language SPEC v0.3.0

> 상태: current public pre-release draft / owner-approved 2026-07-26
> trace: Language SPEC `v0.3.0` ← internal current SSOT `v24.17.1`
> 권위: 충돌하면 설치된 internal current SSOT가 우선한다.
> 구현 경계: docs-first canonical과 parser/runtime 제품 상태를 구분한다.

## v0.x clean break

- 외부 사용자와 보존할 사용자 자료가 0인 현재 잘못된 표면을 호환 자산으로 만들지 않는다.
- `보임 {}`는 제거됐다. deprecated alias나 dual canonical output을 제공하지 않는다.
- `project.obs.N`, `output_N` 같은 합성 정체성을 공개 의미로 사용하지 않는다.
- `묶음`·`pack`을 값꾸러미의 사용자 정본 별칭으로 제공하지 않는다.
- v0.2.1과 이전 공개판은 역사판으로 제자리 보존한다.

## 비주장

이 공개판은 parser/runtime/renderer, 한국어 Manim, 표준 선반 runtime,
외부 사용자 성공을 완료로 주장하지 않는다. `space2d`, `space3d`, `PinSpec`,
영문 schema field는 wire·구현 이름이며 한국어 의미 정체성을 대신하지 않는다.
