# 지원 범위 — Language SPEC v0.3.0

> 상태: current public pre-release draft / owner-approved 2026-07-26
> trace: Language SPEC `v0.3.0` ← internal current SSOT `v24.17.1`
> 권위: 충돌하면 설치된 internal current SSOT가 우선한다.
> 구현 경계: docs-first canonical과 parser/runtime 제품 상태를 구분한다.

| 표면 | 설계 상태 | 제품 상태 |
|---|---|---|
| 한글 씨자리와 적용 갈래 | canonical docs-first | 기존 범위별 확인 |
| `(된씨)맺음` | canonical | clean-cut parser/lock/hash migration OPEN |
| `(이름: 값, ...) 보임.` | canonical docs-first | parser/runtime/CLI/WASM OPEN |
| 이름씨 `(자리...)인 이름` | canonical docs-first | parser/canon/golden OPEN |
| 짧은 계약문 | canonical docs-first | Gate0 parity OPEN |
| 구실·정적 dispatch | canonical docs-first | K0~K7 OPEN |
| 표준 보기 12종 | canonical docs-first | Rust/browser/golden OPEN |
| 평면·입체 모양 선반 | canonical docs-first | common composition OPEN |
| 완성 장면틀 8종 | canonical docs-first | content/runtime OPEN |
| bounded SolvePlan | canonical direction | implementation OPEN |
| OI-KM-07 효과 | meaning gate OPEN | unavailable |
| OI-KM-10 입력 | meaning gate OPEN | unavailable |

## 표준 보기 12종

현재값, 시간선, 비교선, 좌표선, 흩어진점, 막대, 결과표, 위치자취,
벡터화살표, 장면그래프곁, 장면값겹, 분포막대를 공개 이름으로 사용한다.

제품 지원은 테스트 전용 변환기가 아니라 원문을 받는 parser/frontdoor, Rust owner,
CLI/WASM parity, browser와 golden 증거로 판단한다.
