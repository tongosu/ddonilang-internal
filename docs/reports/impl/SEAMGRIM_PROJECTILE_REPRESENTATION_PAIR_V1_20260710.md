# 셈그림 포물선 표현판 비교 W4 보고서

상태: 비교 UI `닫힘-동작` / 선언형 runtime 미착지

## 결과

- 포물선 운동 한 세계를 `마디별 계산`과 `세움 선언` 두 판으로 나란히 보여준다.
- 명시적 판은 브라우저/WASM에서 실제 실행되며 기존 결정적 `state_hash`를 재현한다.
- 선언형 판은 제품 `teul-cli run --solveplan-out`이 생성한 S2 SolvePlan artifact까지 착지했다.
- 두 판의 관측 동등성, 동일 TickPlan, 동일 state hash는 주장하지 않는다.
- 모바일에서는 비교판 내부의 이중 스크롤을 없애 두 표현과 경계 문구를 한 흐름으로 읽게 했다.

## 산출물

- `solutions/seamgrim_ui_mvp/lessons/rep_phys_projectile_xy_v1/projectile_seum_s2.ddn`
- `solutions/seamgrim_ui_mvp/lessons/rep_phys_projectile_xy_v1/projectile_seum_s2.solveplan.detjson`
- `solutions/seamgrim_ui_mvp/lessons/rep_phys_projectile_xy_v1/representation_pair.detjson`
- `pack/seamgrim_projectile_representation_pair_v1/`
- `tests/seamgrim_projectile_representation_pair_runner.mjs`
- `tests/run_seamgrim_projectile_representation_pair_check.py`

## 검증

```text
node tests/seamgrim_projectile_representation_pair_runner.mjs
PASS seamgrim_projectile_representation_pair: ok

python tests/run_seamgrim_projectile_representation_pair_check.py
PASS [seamgrim-projectile-representation-pair-v1] OK comparison-behavior-closed declarative-runtime-open
```

전체 검사는 SolvePlan 2회 바이트 결정성, 명시적 포물선 2회 state hash 일치, pack golden, G3 S2 closure checker, 데스크톱 2열/모바일 1열 UI를 함께 확인한다.

## 경계

- `equivalence_class=teaching_pair`, `equivalence_status=not_asserted`다.
- `state_hash_integration`은 `manifest_field_only_pending_tonni_confirmation`이다.
- 선언형 판은 아직 세계를 실행하지 않으며 자동 승격하지 않는다.
- `docs/ssot/**`, parser 문법, runtime 의미론, state hash 산식 변경 없음.
