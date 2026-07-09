# 20260709 Codex Declarative Closure 11-Axis Run2

## 결과 요약

- G0: 진행 중. Run2 범위는 G4~G6으로 제한한다.
- G4: 완료. `잇기` 문장형 surface를 `teul-cli run --solveplan-out` SolvePlan artifact의 `lowering.connect_desugar`로 기록한다.
- G5: 미착수.
- G6: 미착수.
- G7~G11: 이번 실행 범위 밖이라 착수하지 않는다.

## 경계

- 브랜치: `codex/queue-20260706`.
- `docs/ssot/**` 직접 수정 금지.
- `state_hash` 산식 변경 금지. `state_hash_inputs`는 SolvePlan manifest field로 유지한다.
- 새 core block 및 `잇기 {}` block 추가 금지.
- full physical/economic simulation runtime claim 금지. 이번 닫힘은 `teul-cli run --solveplan-out` artifact behavior 기준이다.
- 워킹트리의 기존 untracked 프롬프트/반영 파일은 입력 참고로만 두고 커밋하지 않는다.

## 시작 상태

- `git status --short --branch`: `codex/queue-20260706`.
- 기존 untracked:
  - `work/_session_deltas/20260709_codex_recent_proposals_reflection.md`
  - `또니랑/CLAUDECODE_PROMPT_지시문16_설계정교화.md`
  - `또니랑/CODEX_DEVGOALS_20260709_DECLARATIVE_CLOSURE_11AXIS.md`
  - `또니랑/CODEX_HANDOFF_20260709_11AXIS_PROPOSAL_V2_AND_G1G3_RESUME.md`
- `git status --short -- docs/ssot`: 변경 없음.

## 질문 큐

1. DR-179 기준으로 `state_hash_inputs.include`에 `source_hash`와 `lowering.phase.tick_order`를 필수 포함할지 결정 필요. 이번 실행에서는 산식 변경 없이 manifest field로만 유지한다.
2. `설정.셈 { 적분: ... }` method selection의 formal settings schema/AST field 연결 시점 결정 필요. 이번 실행에서는 Run1B의 최소 source 기반 선택을 넘지 않는다.

## 검증 로그

- G0 커밋 전: `git status --short -- docs/ssot` PASS(변경 없음).
- G4:
  - `python -m json.tool` on G4 contracts/expected artifact PASS.
  - `python -m py_compile tests/run_declarative_closure_g4_connect_check.py` PASS.
  - `python tests/run_pack_golden.py lang_connect_lowering_v1 sim_circuit_series_v1 sim_econ_market_v1 lang_connect_diag_v1` PASS.
  - `python tests/run_declarative_closure_g4_connect_check.py` PASS.
  - `cargo test --manifest-path tools/teul-cli/Cargo.toml solveplan -- --nocapture` PASS.
  - `git status --short -- docs/ssot` PASS(변경 없음).
