# 20260709 Codex Declarative Closure 11-Axis Run3A

## 결과 요약

- G0: 완료. Run3A 범위는 G7~G11 red/contract pack과 보고서로 제한한다.
- G7: 완료(`닫힘-문서`). `막음`/`막기` constraint reaction red pack과 umbrella/subpack/checker를 추가했다. parser/runtime landed claim은 `false`로 고정했다.
- G8: 완료(`닫힘-문서`). `sim_experiment_manifest_v1` candidate manifest와 checker를 추가했다. `state_hash_policy.formula_change=false`, `plan_hash_status=pending_canonical_bytes_decision`로 고정했다.
- G9: 미착수.
- G10: 미착수.
- G11: 미착수.

## 경계

- 브랜치: `codex/queue-20260706`.
- `docs/ssot/**` 직접 수정 금지.
- parser/runtime 문법 확장 금지. 새 core block 또는 새 language block 추가 금지.
- `state_hash` 산식 변경 금지. `state_hash_inputs`는 manifest field로 유지한다.
- 닫힘은 `닫힘-문서` 또는 fixture/checker 기준으로만 주장한다.
- 워킹트리의 기존 untracked prompt/session 파일은 입력 참고로만 두고 커밋하지 않는다.

## 시작 상태

- `git branch --show-current`: `codex/queue-20260706`.
- 추적 변경 없음.
- 기존 untracked:
  - `work/_session_deltas/20260709_codex_recent_proposals_reflection.md`
  - `또니랑/CLAUDECODE_PROMPT_지시문16_설계정교화.md`
  - `또니랑/CODEX_DAYRUN_20260708_목표지시서.md`
  - `또니랑/CODEX_DEVGOALS_20260709_DECLARATIVE_CLOSURE_11AXIS.md`
  - `또니랑/CODEX_HANDOFF_20260709_11AXIS_PROPOSAL_V2_AND_G1G3_RESUME.md`
- `git status --short -- docs/ssot`: 변경 없음.

## 질문 큐

1. `plan_hash` canonical byte format은 아직 미결이다. 이번 실행에서는 보고서와 checker로 경계만 고정한다.
2. `막음/막기` runtime 표면은 미착수다. 이번 실행에서는 red/contract fixture만 추가한다.
3. per-agent RNG stream은 proof fixture만 추가한다. 제품 runtime RNG 교체는 하지 않는다.

## 검증 로그

- G0 커밋 전: `git status --short -- docs/ssot` PASS(변경 없음).
- G7:
  - `python -m json.tool pack/*mageum*/*.detjson` PASS(실행은 개별 G7 detjson 전체).
  - `python -m py_compile tests/run_declarative_closure_g7_constraint_red_check.py` PASS.
  - `python tests/run_pack_golden.py sim_constraint_reaction_v1 sim_mageum_floor_v1 sim_mageum_box_v1 sim_mageum_chain_v1 lang_mageum_diag_v1` PASS.
  - `python tests/run_declarative_closure_g7_constraint_red_check.py` PASS.
  - `git status --short -- docs/ssot` PASS(변경 없음).
- G8:
  - `python -m json.tool pack/sim_experiment_manifest_v1/*.detjson` PASS(실행은 개별 detjson 전체).
  - `python -m py_compile tests/run_declarative_closure_g8_experiment_manifest_check.py` PASS.
  - `python tests/run_pack_golden.py sim_experiment_manifest_v1` PASS.
  - `python tests/run_declarative_closure_g8_experiment_manifest_check.py` PASS.
  - `git status --short -- docs/ssot` PASS(변경 없음).
