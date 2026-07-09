# PROPOSAL_DECLARATIVE_CLOSURE_11AXIS — SSOT 적용 준비본 (사용자 적용용)

작성: 2026-07-09 KST, Claude Code
원본: `docs/context/proposals/PROPOSAL_DECLARATIVE_CLOSURE_11AXIS_SSOT_PATCH_V2_20260709.md`
성격: **이 문서 자체는 SSOT가 아니다.** 아래 4개 블록은 V2 제안서에 이미 있던 삽입 텍스트 그대로이며(내용 변경 없음), Claude는 `docs/ssot/**`를 직접 수정하지 않으므로 사용자가 그대로 복사해 반영할 수 있도록 목적지와 함께 재정리했다.

## 근거 인용 재확인 결과 (V2 "Current Evidence" 표)

V2가 인용한 9개 `file:line` 중 시간 경과로 6개가 밀려 있었다(SSOT가 git 미추적 상태로 계속 갱신되기 때문). 삽입할 텍스트 자체에는 이 인용들이 들어있지 않으므로 반영에는 영향 없지만, 검증용으로 정정한 현재 위치는 다음과 같다:

| 주장 | V2 인용(밀림) | 실제 현재 위치 |
|---|---|---|
| `세움값`은 영속 상태 저장 시 `state_hash`에 포함 | `SSOT_LANG:5747` | `SSOT_LANG_v24.12.9.md:5806` |
| `살피기/반례찾기/밝히기` 실행결과·진단은 `state_hash` 제외 | `SSOT_LANG:5755-5756` | `SSOT_LANG_v24.12.9.md:5807` |
| `될때/인 동안`은 이번 round도 full runtime 미승격 | `SSOT_DECISIONS:446,453,539` | `SSOT_DECISIONS_v24.12.9.md:553-554` |
| D-STRICT는 무작위/시계/외부 네트워크 직접 사용 금지 | `SSOT_LANG:4075,6589,6608` | `SSOT_LANG_v24.12.9.md:7021` |
| 단위식 `^` 지수는 컴파일타임 정수 리터럴만 허용 | `SSOT_LANG:3330,3173,6302` | `SSOT_LANG_v24.12.9.md:3225-3226` (예시: `:6319`) |
| 난수 시드는 `InputSnapshot.rng_seed` 기반 결정적 | `SSOT_LANG:6437,6449,6450` | `SSOT_LANG_v24.12.9.md:6500` |
| `SSOT_UPDATE_NOTES` 세움/prime/잇기 후보 문구 | `:16,17,19` | 그대로 정확함(변경 없음) |

## 반영 블록 1 — `docs/ssot/ssot/SSOT_UPDATE_NOTES_v24.12.9.md`

목적지: 파일 최상단, 기존 v24.12.9 note 앞에 새 섹션으로 삽입.

> 원문 그대로: V2 제안서 §"Proposed `SSOT_UPDATE_NOTES_v24.13.0-candidate` Entry" 블록 전체(`## v24.13.0-candidate 선언형 closure 11축 후보` ~ 마지막 줄까지 15개 항목).

## 반영 블록 2 — `docs/ssot/ssot/SSOT_OPEN_ISSUES_v24.12.9.md`

목적지: 언어/현재 후보 OI 클러스터 아래 추가.

> 원문 그대로: V2 제안서 §"Proposed `SSOT_OPEN_ISSUES` Updates"의 4개 OI 블록(`OI-UNIT-SCALAR-MIX-01`, `OI-SOLVEPLAN-ARTIFACT-SCHEMA-01`, `OI-SIM-CONSTRAINT-NAME-01`, `OI-RNG-PER-AGENT-STREAM-01`).

## 반영 블록 3 — `docs/ssot/ssot/SSOT_PLANS_v24.12.9.md`

목적지: 즉시 언어/시뮬레이션 계획 큐에 추가.

> 원문 그대로: V2 제안서 §"Proposed `SSOT_PLANS` Pack Queue" 표 20행 전체. 이 중 9개(`lang_seum_algebraic_v1`, `lang_seum_linear_v1`, `sim_seum_tick_phase_v1`, `lang_seum_diag_v1`, `lang_connect_lowering_v1`, `lang_connect_diag_v1`, `sim_circuit_series_v1`, `sim_econ_market_v1`, `sim_init_equation_v1`, `sim_ode_first_order_v1`, `sim_ode_second_order_v1`, `sim_ode_vector_v1`, `sim_ode_method_switch_v1`, `sim_unit_dimension_static_v1`—의 pack skeleton 부분)는 **이미 pack 파일이 존재**하고 golden PASS를 Claude가 직접 재확인했다(closure gate는 "product runtime + golden"이라 아직 미충족 — 지금은 `--solveplan-out` opt-in 도구 산출물 수준). 나머지(`sim_constraint_reaction_v1` 계열 4개, `sim_experiment_manifest_v1`, `sim_agent_rng_stream_v1`)는 pack 자체가 아직 없다.

## 반영 블록 4 — `docs/ssot/ssot/SSOT_DEMOS_v24.12.9.md`

목적지: 기존 선언형 `세움` 데모 뒤에 candidate 데모로 추가.

> 원문 그대로: V2 제안서 §"Proposed `SSOT_DEMOS` Additions"의 5개 `ddn` 코드 블록(S1 선형관계, S2 ODE, 단위 caret 지수, t=0 init solve, 훅 리셋).

## 반영 후 확인 사항

- 4개 블록 전부 "candidate / runtime landed claim: no"를 명시하고 있어 그대로 반영해도 구현 완료 주장이 되지 않는다.
- 반영 후 `python tests/run_ci_sanity_gate.py --profile core_lang` 재실행 권장(SSOT 텍스트 변경만으로는 실패할 이유가 없지만 습관적 확인).
- Codex가 이미 구현한 파서 확장(A7, `채비` 안 `세움` 중첩)은 Claude가 별도로 설계 검토 승인했다(2026-07-09) — 이 SSOT 반영이 그 승인을 사후적으로 문서화하는 것이지, 이 반영이 있어야 그 코드가 유효해지는 것은 아니다.
