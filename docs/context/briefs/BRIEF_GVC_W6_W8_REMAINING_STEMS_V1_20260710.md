# BRIEF: GVC W6~W8 — 나머지 6줄기(다/사/아/차/파/거) 제품 증거 배치

작성: 2026-07-10 KST
근거: `docs/context/roadmap/GANADA_MARU_VERIFICATION_CONTRACT_V1_20260710.md`(닫힘등급 계약), W1~W5 성공 패턴 그대로 반복(마/자/라/카 완료).
성격: W1~W5와 동일한 규율. **90칸 상태 재판정 없음. 신규 `닫힘-동작` 매트릭스 승격 주장 없음.** 실행 증거 축적 + registry 확장만.

## 배경

GVC W1~W5가 15줄기 중 마(교과)/자(AI슬기)/라(말블록)/카(또니마루) 4개 줄기를 처리했다. 남은 6개 줄기(다/사/아/차/파/거)를 같은 방식으로 처리한다. 각 줄기의 6개 마루(milestone) 성격은 `GANADA_REVERIFICATION_TIER1~3_V1.md`에서 확인:

| 줄기 | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| 다(수학) | math library proposal | math smoke pack | symbolic/proof pack | seamgrim math view pack | registry pack | math LTS suite |
| 사(보개/게임) | bogae schema docs | bogae smoke pack | sprite/grid pack | game preview pack | asset registry pack | renderer LTS |
| 아(누리짐) | nurigym schema docs | smoke pack | dataset hash pack | parity pack | dataset publish pack | training workflow suite |
| 차(RPG) | proposal/schema | smoke pack | story pack | authoring UI pack | package pack | adapter LTS |
| 파(경제사회) | case schema | AGE4 case smoke | bridge report pack | policy ghost pack | social template pack | social-world LTS |
| 거(AI개발보조) | question card schema | toolchain smoke | AI validation pack | authoring UI pack | tool registry | AI workflow LTS |

각 줄기마다 실제 제품 코드/pack이 이미 존재하는지 먼저 확인하고(예: `pack/econ_agent_*`, `pack/sim_econ_market_v1`, `pack/nuri_gym_*`, `core/src/nurigym/*`, `pack/game_maker_*`, `pack/malhim_rpg_*`, `pack/ttonimaru_*`, `pack/question_card_*` 등 기존 산출물), **새로 지어내지 말고 기존 실제 동작 증거를 gate로 연결하는 것을 우선**한다.

## 작업 (W1~W5와 동일 구조 반복)

각 줄기(다/사/아/차/파/거)마다:

1. **`ganada_{stem}_branch_execution_reaudit_v1` pack/checker**: 6개 마루를 실제 명령(체커/러너/`teul-cli run`)으로 재감사한다. legacy checker가 stale 문서 토큰에 걸려 FAIL하는 것과 실제 제품이 안 되는 것을 구분해서 기록한다(W1~W5와 동일 방법론).
2. **대표 제품 증거 pack 2~4개**: 각 줄기에서 이미 실제로 동작하는 기존 pack/코드를 찾아 gate로 연결한다. 예시:
   - 다줄기: `symbolic_minimum_v1`, `numeric_exact_numbers_smoke_v1`, `math_vector_minimum_first_run_v1`, `proof_runtime_smoke_v1`(Q33에서 이미 실제 동작 확인됨) 연결.
   - 사줄기: `std_bogae_grid2d_v1` 등 지시문 8 표준 보개팩, 기존 `bogae_*` pack 연결.
   - 아줄기: `core/src/nurigym/{bandit,cartpole,gridmaze,pendulum}.rs`, `nuri_gym_*` pack, 이번 세션에서 검증한 step_record v0.2 연결.
   - 차줄기: `malhim_rpg_*` pack(1~5, W4/W5에서 확인한 실제 존재).
   - 파줄기: `econ_agent_*`, `sim_econ_market_v1`, `social_world_econ_*` pack(Q33에서 실제 동작 확인됨) 연결.
   - 거줄기: `question_card_*` pack(1~5, 이전 세션에서 실제 존재/PASS 확인됨) 연결.
3. **`ganada_execution_evidence_registry_v4`**: v3의 17개 추적 셀에 이번 6줄기 신규 추적 셀을 누적 추가한다. `behavior_closed_claim=false`, `matrix_upgrade_claim=false` 유지, docs/status-only negative control 유지.

## 보너스 항목 (여유 있으면, 필수 아님)

- W4/W5가 남긴 "다음 추천": 라-5 편집환경 안정화 runner 강화, 카-5 platform hardening runner를 pack/checker로 승격, 라줄기 stale checker 3건(`run_malblock_authoring_ui_check.py`, `run_studio_malblock_workbench_integration_check.py`, `run_seamgrim_malblock_roundtrip_subset_check.py`) 수리 — 마줄기 stale checker 수리(W2-MA-REPAIR)와 동일 방법으로.

## 경계 (W1~W5와 동일, 절대 준수)

1. `docs/ssot/**` 직접 수정 금지.
2. parser/runtime 문법, `state_hash` 산식 변경 금지.
3. 실제 AI model call, 외부 업로드/배포/계정 시스템 claim 금지.
4. **90칸 매트릭스 상태 재판정 금지** — 새 `닫힘-동작` 승격 주장 없음. 이번 배치는 증거 축적/게이트 확장만.
5. 기존 untracked 참고 파일, 기존 dirty `DEV_SUMMARY.md`/`docs/context/reports/INDEX.md` hunk는 커밋에 섞지 않는다.
6. `main` 직접 커밋 금지 — `codex/queue-20260706`에만. (지난 배치처럼 실수로 main에 커밋되면 즉시 교정하고 보고서에 명시.)
7. 판단이 막히면(예: 어떤 줄기의 milestone에 대응하는 실제 제품이 전혀 없음) "결정 필요"로 남기고 억지로 pack을 만들지 않는다.

## DoD

- 6개 줄기 × (reaudit pack 1 + 대표 증거 pack 2~4) = 최소 18개 신규 pack/checker.
- `ganada_execution_evidence_registry_v4` — 누적 셀 수 = v3(17) + 이번 배치 신규 추적 셀.
- 각 신규 checker/pack golden 직접 실행 PASS.
- `cargo check`, `python tests/run_ci_sanity_gate.py --profile core_lang` PASS.
- 세션 델타에 결과 요약 + "결정 필요" 목록(있으면) 기록.
