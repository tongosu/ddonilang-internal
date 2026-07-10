# 셈그림 current-line 대표 3세계 W2 구현 보고서

상태: `닫힘-동작` / 2026-07-10

## 세계

| 개념 | 제품 차시 | 첫 세계 주소값 | 핵심 조절값 | 주 보기 |
|---|---|---|---|---|
| 일차함수 | `rep_math_function_line_v1` | `linear-function` | 기울기, y 절편, x 간격 | `x/y` `graph_series` |
| 포물선 | `rep_phys_projectile_xy_v1` | `projectile` | 가로 속도, 세로 속도, 중력 | `x/y` `trajectory_trail` |
| 시장과 세금 | `rep_econ_supply_demand_tax_v1` | `market-tax` | 시작 가격, 세금, 수요 민감도 | `t/가격` `graph_series` |

세 세계는 모두 기존 대표 팩과 활성 제품 차시를 재사용한다. `physics_projectile`, `math_function_line`, `econ_supply_demand_tax` 별칭도 활성 ID로 정본화한다.

## 구현

- `first_delight` 주소를 세 세계 레지스트리로 확장했다.
- 첫 세계 CSS를 포물선 전용에서 모든 `data-first-delight` 세계 공통으로 바꿨다.
- 그래프 payload가 최신 점 하나만 줄 때 이전 보개 점열을 이어 그린다.
- 세계 메타의 `first_delight_graph_axes`로 교과 그래프 축을 고정한다.
- 일차함수 대표 원문에 팩 메타와 일치하는 `마디수: 24`를 넣어 계산 뒤 실행이 끝나게 했다.
- `graph_series`, `trajectory_trail`, `afterimage` 역할을 분리하고 상태 해시 밖에 유지했다.

화면 검수에서 단순 선분 개수만으로는 같은 점을 이은 무의미한 그래프를 잡지 못했다. 축 메타와 DOM 증거를 추가하고 browser runner가 세계별 축까지 확인하도록 강화했다.

## 증거

- 제품 묶음: `pack/seamgrim_current_line_three_worlds_v1/`
- 세계 manifest: `worlds.detjson`
- 브라우저 시험: `tests/seamgrim_current_line_three_worlds_runner.mjs`
- 통합 검사: `tests/run_seamgrim_current_line_three_worlds_check.py`

```text
node tests/seamgrim_current_line_three_worlds_runner.mjs
PASS seamgrim_current_line_three_worlds: ok

python tests/run_seamgrim_current_line_three_worlds_check.py
PASS [seamgrim-current-line-three-worlds-v1] OK behavior-closed
```

통합 검사는 세 세계의 데스크톱·모바일 배치, 비공백 그래프/궤적, 세 핵심 조절값, 별칭 정본화, 입력 변경에 따른 해시 변경, 같은 변경값의 같은 해시, 대표 원문의 CLI check/canon/run을 확인한다. 포물선은 W1의 run/pause/step/reset 검사도 다시 실행한다.

## 경계

- 온뭉치 수록 확정이 아니다. W2 manifest는 가등급 pilot 입력 후보다.
- `docs/ssot/**`, parser, runtime 의미론, state hash 산식 변경 없음.
- 선언형 `세움{}` 표현판과 자동 동등성 주장은 아직 없다.
