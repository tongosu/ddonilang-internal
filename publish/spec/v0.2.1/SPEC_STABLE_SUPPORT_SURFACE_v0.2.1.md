# 지원 범위 — Language SPEC v0.2.1

> 상태: current public pre-release draft / consistency-cleaned 2026-07-17
> trace: Language SPEC `v0.2.1` ← installed current SSOT `v24.15.1`
> 권위: 충돌하면 설치된 internal current SSOT가 우선한다.
> 구현 경계: G7과 함수 타입 `-->`는 설계 확정, K0~K7·A1 제품 증거는 아직 OPEN이다.


| 표면 | 설계 상태 | 제품 상태 |
|---|---|---|
| 한글 씨자리와 적용 타입 | canonical docs-first | K0~K2 OPEN |
| `(된씨)맺음`, `#잘됨/#안됨`, `이유:글` | canonical docs-first | 기존 제품 표면과 parity 재검증 필요 |
| 구실 정의·요구·구현·채택 | canonical docs-first | K0·K3 OPEN |
| 입력 기반 generic 추론 | canonical docs-first | K2 OPEN |
| 정적 dispatch | canonical docs-first | K4 OPEN |
| `보기만/누리바꿈`, D-STRICT, open=deny | canonical docs-first | K5 OPEN |
| 씨맞춤·profile·artifact·replay | canonical docs-first | K6 OPEN |
| CLI/WASM/교재 동일 표면 | required gate | K7 OPEN |
| 함수 타입 `-->` | canonical docs-first | A1 제품 세로줄 OPEN |
| M3-실험 0 제한 사용자 씨앗지음 | approved experimental plan | unavailable; W0~W4 OPEN |

## 현재 비지원 V1 기능

- 호출부 명시 타입 인자와 output-only generic.
- receiver 없는 구실 요구.
- blanket/conditional 맡음, specialization, negative impl.
- associated type, default member, 구실 상속.
- runtime 구실 값, vtable, box, downcast, dynamic dispatch.
- 다형 재귀, variance/subtyping, HKT/dependent/rank-2+.
- runtime reflection과 instance별 맡음.

이 목록은 “연구 누락”이 아니라 의도된 V1 절단이다. SSOT에 적힌 재개 조건을 충족한
항목만 별도 결정으로 다시 연다.

## build profile

`generic-kusil-v1`은 씨맞춤 4096, 씨맞춤 깊이 64, 적용 타입 깊이 32, generic 요구
32, 구실 member 64를 상한으로 둔다. 각 상한의 N-1과 N은 통과, N+1은 CLI/WASM에서
같은 진단 code·span·payload로 실패해야 한다. 이 parity는 K6/K7 제품 관문이다.
