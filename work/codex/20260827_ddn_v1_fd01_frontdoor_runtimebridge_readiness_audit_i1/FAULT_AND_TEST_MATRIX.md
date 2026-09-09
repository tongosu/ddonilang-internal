# FD01 감사·후속 fault/test matrix

## 이번 감사에서 실행한 근거

| ID | 실행 | 결과 | 의미 |
|---|---|---|---|
| T1 | RuntimeBridge T1 runner | PASS | bridge 기본 계약 |
| T2 | source analysis T4 | PASS | 정적 연결 |
| T3 | T4 + tracked WASM | PASS | 실제 WASM 분석 경로 |
| T4 | observation manifest T4D | PASS | native manifest contract |
| T5 | observation channel T4F | PASS | fallback 0, fail-closed |
| T6 | T5F four-family + tracked WASM | EXPECTED RED | grid native result 누락 |
| T7 | current grid successor audit | OWNER DECISION REQUIRED | source 수용/result null |
| T8 | current CLI + PC01 V25 source | EXPECTED RED | `E_SHARED_CANONICAL` |
| T9 | 557 lesson dual-parser inventory | PASS | V25 0, pre-only 127, neither 430 |

## 후속 구현 필수 반례

1. source analysis만 V25, execution은 pre-V25인 mismatch
2. execution만 V25, source analysis는 pre-V25인 mismatch
3. epoch metadata 누락
4. 알 수 없는 epoch identity
5. source text 수정 뒤 stale analysis 재사용
6. V25 실패 뒤 pre-V25 silent retry
7. pre-V25 실패 뒤 V25 silent retry
8. content sniffing으로 parser 선택
9. JS가 Rust 실패를 성공 observation으로 합성
10. 실패 뒤 partial state/revision/output/effect 발생
11. 같은 source/revision에 서로 다른 epoch receipt 결속
12. historical source가 암묵적으로 V25로 승격
13. current grid 결과를 JS에서만 생성
14. tracked WASM과 source build drift

각 mutation은 원제품 GREEN → 실제 source mutation RED → exact restore → GREEN을 남긴다.
정적 grep만으로 fault injection을 대체하지 않는다.

