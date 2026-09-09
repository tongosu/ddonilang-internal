# 20260709 Codex Declarative Closure 11-Axis

## 상태

- G0: 완료.
- Part A: 완료(SSOT 직접 편집 대신 proposal-ready 패치 후보 작성).
- G1: 부분. SolvePlan S0/S1 제품 런타임 미구현.
- G2: 부분. 세움 solve/write tick phase 제품 런타임 미구현.
- G3: 부분. prime parser 수용과 stdlib 적분기는 있으나 derivative-slot-to-integrator lowering 미구현.
- G4+: 지시서의 1차 실행 범위 밖이라 착수하지 않음.

## 읽은 문서

- `AGENTS.md`
- `SSOT_POLICY.md`
- `docs/context/all/DEV_SUMMARY.md`
- `docs/ssot/ssot/SSOT_UPDATE_NOTES_v24.12.9.md`
- `docs/ssot/ssot/SSOT_DECISIONS_v24.12.9.md`
- `docs/ssot/ssot/SSOT_OPEN_ISSUES_v24.12.9.md`
- `docs/ssot/ssot/SSOT_PLANS_v24.12.9.md`
- `docs/ssot/ssot/SSOT_DEMOS_v24.12.9.md`

## 경계 판정

- `docs/ssot/**` 직접 수정은 금지되어 있어 Part A는 `docs/context/proposals/PROPOSAL_DECLARATIVE_CLOSURE_11AXIS_SSOT_PATCH_V1_20260709.md`로 우회했다.
- runtime landed claim은 하지 않는다.
- `= / <- / =:=` 의미 변경 없음.
- 새 core block 없음.
- 언어 커널/런타임 구현은 이번 커밋에서 변경하지 않는다.
- `state_hash` 산식 변경 없음.

## Part A 반영 위치

| Axis | 위치 | 산출물 |
|---|---|---|
| A1 SolvePlan | `SSOT_DECISIONS`, `SSOT_LANG §R1A`, `SSOT_PLANS` 후보 | proposal §A1 |
| A2 prime | `SSOT_LANG`, `SSOT_DEMOS` 후보 | proposal §A2 |
| A3 `잇기` | `SSOT_DECISIONS`, `SSOT_DEMOS` 후보 | proposal §A3 |
| A4 hooks | `SSOT_DECISIONS`, `SSOT_LANG` hook matrix 후보 | proposal §A4 |
| A5 constraints | `SSOT_OPEN_ISSUES`, `SSOT_PLANS` 후보 | proposal §A5 |
| A6 units | `SSOT_LANG` unit sections, new OI | proposal §A6, `OI-UNIT-SCALAR-MIX-01` |
| A7 inner `채비` | `SSOT_LANG §R1A`, `SSOT_DECISIONS` candidate | proposal §A7 |
| A8 vector prime | `SSOT_LANG` vector/math candidate | proposal §A8 |
| A9 experiment manifest | `SSOT_TOOLCHAIN`, `SSOT_PLANS` candidate | proposal §A9 |
| A10 standard parts | `SSOT_PLANS`, `SSOT_DEMOS` candidate | proposal §A10 |
| A11 per-agent RNG | `SSOT_LANG` RNG, `SSOT_PLATFORM` multi-agent ordering candidate | proposal §A11 |

## 부분 구현

- G1: 기존 `방정식풀기`/relation solve and `세움` assertion check pieces exist, but no named SolvePlan S0/S1 product pipeline.
- G2: existing proof guard can run every tick, but no seum-derived value solve/write phase.
- G3: prime lexer/parser support and standalone integrators exist, but no derivative slot lowering.
- 상세 근거: `docs/reports/impl/DECLARATIVE_CLOSURE_G1_G3_IMPLEMENTATION_GAP_V1_20260709.md`.

## 질문 큐

1. `OI-UNIT-SCALAR-MIX-01`: scalar와 unit value 혼합을 dimensionless scalar로 허용할지, 명시 단위 없는 혼합을 전부 `E_UNIT_MISMATCH`로 막을지 결정 필요.
2. `OI-SOLVEPLAN-ARTIFACT-SCHEMA-01`: SolvePlan public detjson field set과 `state_hash_inputs` 위치 결정 필요.
3. `OI-CONSTRAINT-SURFACE-NAME-01`: `막음`/`막기`/`턱`/`제약` 중 canonical surface 결정 필요.
4. `OI-RNG-PER-AGENT-STREAM-01`: per-agent RNG stream derivation formula와 stream namespace 결정 필요.
5. `채비 {}` inside `세움{}`를 지금 candidate로 받을지, SolvePlan S0/S1 landing 뒤로 미룰지 결정 필요.
6. SSOT 직접 반영은 Codex 금지 영역이므로 SSOT 오너 적용 필요.

## 검증

- `git status --short --branch` initial: `codex/queue-20260706`, pre-existing untracked `또니랑/CODEX_DEVGOALS_20260709_DECLARATIVE_CLOSURE_11AXIS.md`.
- `cargo check`: PASS. 기존 `tool/src/ddn_runtime.rs` dead code warning만 발생.
- `python tests/run_ci_sanity_gate.py --profile core_lang`: PASS.
- sanity gate가 `pack/open_bundle_artifact/run_bundle/geoul.diag.jsonl`, `pack/open_end_to_end/open.log.jsonl`를 실행 로그로 갱신했으나 이번 작업 산출물이 아니어서 diff 범위만 원복했다.
- `git status --short -- docs/ssot lang core tool tools/teul-cli/src`: PASS(변경 없음).
- 최종 커밋 전 status에는 이번 문서 변경과 pre-existing untracked `또니랑/CODEX_DEVGOALS_20260709_DECLARATIVE_CLOSURE_11AXIS.md`만 남김.

## 산출물

- `docs/context/proposals/PROPOSAL_DECLARATIVE_CLOSURE_11AXIS_SSOT_PATCH_V1_20260709.md`
- `docs/reports/impl/DECLARATIVE_CLOSURE_G1_G3_IMPLEMENTATION_GAP_V1_20260709.md`
- `work/_session_deltas/20260709_codex_declarative_closure_11axis.md`
