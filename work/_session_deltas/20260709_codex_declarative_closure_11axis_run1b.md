# 20260709 Codex Declarative Closure 11-Axis Run1B

## 결과 요약

- Proposal V2: 완료. V1은 superseded로 남기고 `docs/context/proposals/PROPOSAL_DECLARATIVE_CLOSURE_11AXIS_SSOT_PATCH_V2_20260709.md`를 재발행했다.
- G1 `[DC-G1-RED]`/`[DC-G1-CORE]`: 완료. `teul-cli run --solveplan-out` 제품 경로에서 S0/S1 `ddn.solveplan.v1` artifact를 생성한다.
- G2 `[DC-G2-PHASE]`: 완료. SolvePlan artifact에 `seum_solve` phase와 세움 진단 5종을 기록한다.
- G3 `[DC-G3-S2]`: 완료. prime derivative slot을 S2 SolvePlan으로 낮추고 기존 stdlib 적분기 표면 `적분.오일러`/`적분.반암시적오일러` 선택을 기록한다.
- G4~G6: 2차 실행 범위라 착수하지 않음.

## Proposal V2 Diff 요약

| Drift | V2 반영 위치 | 확인 |
|---|---|---|
| P1 A7 방향 반전 | V2 lines 24, 62, 78 | `채비 {}` top-level 유지, `채비 {}` 안 `세움 {}` = t=0 1회 solve candidate. |
| P2 S0 정의 복원 | V2 lines 25, 53, 72 | S0 = 명시적 대수 + 결정적 인과화(이분 매칭, 위상정렬, 소스 선언 순서 tie-break). |
| P3 A4 계약 2 복원 | V2 lines 57-58 | hook `<-` 쓰기 next segment start, 선언 순서, last write wins, SolvePlan 기록. |
| P4 A5 결정 재개방 철회 | V2 lines 27, 60, 76, 107 | `막음`/`막기` 확정, 반응 `멈춤`/`튕김(e)`/`조임`/`감쌈` 복원. |
| P5 pack queue 보충 | V2 lines 122-140 | connect/circuit/econ/init/vector 신규 pack queue와 `sim_constraint_reaction_v1` 하위 실행 단위 명시. |

## Questions 반영 확인

- Q1 `OI-UNIT-SCALAR-MIX-01`: 기본값 B 승인으로 기록했다. V2 lines 89-95, 192.
- Q2 `OI-SOLVEPLAN-ARTIFACT-SCHEMA-01`: 최소 field set과 `state_hash_inputs` manifest field 유지 기록. V2 lines 99-101, 193.
- Q3 constraint 이름: `막음`/`막기` 확정, 신규 OI 없음. V2 lines 107, 194.
- Q4 per-agent RNG: `(global_seed, agent_id, stream_name)` 승인 기록. V2 lines 111-116, 195.
- Q5 채비/세움 중첩: 질문 무효, `채비 {}` 안 `세움 {}` candidate 등록. V2 lines 62, 78, 196.
- 세움 밖 prime 절충: 현 단계 warning+identifier, 다음 major `E_PRIME_OUTSIDE_SEUM` 승격 조건 기록. V2 lines 180-186.

## 구현 증빙

| Commit | 항목 | 주요 근거 |
|---|---|---|
| `626a054 [DC-A-02]` | Proposal V2 | V2 drift P1~P5, Questions 1~5 반영. |
| `3d69be1 [DC-G1-RED]` | S0/S1 red pack | `pack/lang_seum_algebraic_v1`, `pack/lang_seum_linear_v1`, `tests/run_declarative_closure_g1_red_check.py`. |
| `9fff3a3 [DC-G1-CORE]` | S0/S1 product planner | `tools/teul-cli/src/cli/solveplan.rs:55`, `tools/teul-cli/src/cli/run.rs:3857`, `tests/run_declarative_closure_g1_core_check.py:109`. |
| `727d4b7 [DC-G2-PHASE]` | 세움 phase/진단 | `tools/teul-cli/src/cli/solveplan.rs:268`, `tools/teul-cli/src/cli/solveplan.rs:433`, `tests/run_declarative_closure_g2_phase_diag_check.py:125`. |
| `8b40374 [DC-G3-S2]` | prime slot S2 lowering | `tools/teul-cli/src/cli/solveplan.rs:487`, `tools/teul-cli/src/cli/solveplan.rs:518`, `tests/run_declarative_closure_g3_s2_check.py:126`. |

## State Hash 통합 설계 노트

- 이번 실행은 `state_hash` 산식과 runtime state hash 입력을 변경하지 않았다.
- SolvePlan의 `state_hash_inputs`는 artifact manifest field로만 유지했다.
- 현재 manifest include 후보는 `schema`, `source_hash`, `stage`, `method`, `relations`, `unknowns`, `lowering`이다.
- 현재 manifest exclude 후보는 `diagnostics`, `execution_results`다.
- DR-179 적용 시 "정의물 포함 / 실행 결과 제외"의 실제 경계를 `state_hash` 산식에 넣기 전 또니 확인이 필요하다.

## 질문 큐

1. DR-179 기준으로 `state_hash_inputs.include`에 `source_hash`와 `lowering.phase.tick_order`를 필수 포함할지 결정 필요.
2. `설정.셈 { 적분: ... }` method selection은 이번에 raw source 기반으로 최소 배선했다. formal settings schema/AST field 연결 시점 결정 필요.

## 검증

- `cargo check`: PASS. 기존 `tool/src/ddn_runtime.rs` dead code warning만 출력.
- `cargo check --manifest-path tools/teul-cli/Cargo.toml`: PASS.
- `python tests/run_pack_golden.py lang_seum_algebraic_v1 lang_seum_linear_v1 sim_seum_tick_phase_v1 lang_seum_diag_v1 sim_ode_first_order_v1 sim_ode_second_order_v1 sim_ode_method_switch_v1 sim_ode_vector_v1`: PASS.
- `python tests/run_declarative_closure_g1_red_check.py`: PASS.
- `python tests/run_declarative_closure_g1_core_check.py`: PASS.
- `python tests/run_declarative_closure_g2_phase_diag_check.py`: PASS.
- `python tests/run_declarative_closure_g3_s2_check.py`: PASS.
- `python tests/run_ci_sanity_gate.py --profile core_lang`: PASS, 최종 `ci_sanity_status=pass code=OK`.
- `git status --short -- docs/ssot`: PASS, 변경 없음.

## 경계

- `docs/ssot/**` 직접 수정 없음.
- `main` 직접 커밋/push 없음.
- G4~G6 착수 없음.
- `state_hash` 산식 변경 없음.
- full simulation runtime state write closure 주장은 하지 않는다. 이번 닫힘은 `teul-cli run --solveplan-out` SolvePlan artifact behavior 범위다.
