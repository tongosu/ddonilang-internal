# 공개 제품 예제 후보 matrix

| ID | 역할 | pre-V25 | V25 | 제안 | 권리 상태 |
|---|---|---:|---:|---|---|
| SPEC01~07 | public SPEC docs-first | 1/7 | 0/7 | 제품 예제로 자동 승격 금지 | 공개 중이나 최종 license OPEN |
| PC01 | Definition/Binding conformance | FAIL | PASS | Tier 0, targeted PASS+rights 뒤 후보 | Owner 확인 필요 |
| HELLO | 첫 실행·출력 | PASS | FAIL | Tier 1 migration | audit 필요 |
| GRID_CURRENT | Workbench current grid | PASS | FAIL | Tier 1 + native grid result | audit 필요 |
| TENSOR | Basic Tensor | PASS | FAIL | Tier 1, Tensor R1 contract 뒤 | audit 필요 |
| PROJECTILE | 물리 showcase | PASS | FAIL | Tier 2, core workflow 뒤 | Owner 확인 필요 |
| CONSOLE_VIEW | renderer parity | FAIL | FAIL | Tier 2 | audit 필요 |
| GRID2D_VIEW | renderer grid smoke | FAIL | FAIL | Tier 2 | audit 필요 |
| RICH_TEXT | text UI | PASS | FAIL | minimum first-run에서 defer | audit 필요 |

## 1차 후보를 고른 이유

- `PC01`: V25 Definition `:=`와 Binding `<-`의 가장 작은 제품 의미 증거다.
- `HELLO`: 설치·열기·실행·출력을 가장 짧게 보여준다.
- `GRID_CURRENT`: Workbench의 시각 제품 경로와 native canonical result를 검증한다.
- `TENSOR`: V1 REQUIRED인 Basic Tensor R1의 실제 자료 workflow를 대표한다.

네 후보는 migration 순서를 정하기 위한 제안이며 release membership이 아니다.

