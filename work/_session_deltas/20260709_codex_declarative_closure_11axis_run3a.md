# 20260709 Codex Declarative Closure 11-Axis Run3A

## 결과 요약

- G0: 완료. Run3A 범위는 G7~G11 red/contract pack과 보고서로 제한한다.
- G7: 완료(`닫힘-문서`). `막음`/`막기` constraint reaction red pack과 umbrella/subpack/checker를 추가했다. parser/runtime landed claim은 `false`로 고정했다.
- G8: 완료(`닫힘-문서`). `sim_experiment_manifest_v1` candidate manifest와 checker를 추가했다. `state_hash_policy.formula_change=false`, `plan_hash_status=pending_canonical_bytes_decision`로 고정했다.
- G9: 완료(`닫힘-문서`). `sim_standard_parts_catalog_v1` catalog와 checker를 추가했다. 기존 증빙이 약한 part는 `candidate_only`로 유지했다.
- G10: 완료(`닫힘-문서`). `sim_agent_rng_stream_v1` proof fixture와 checker를 추가했다. derivation은 `(global_seed, agent_id, stream_name)`로 고정하고 runtime RNG 교체는 하지 않았다.
- G11: 완료(`닫힘-문서`). `SOLVEPLAN_PLAN_HASH_BOUNDARY_V1_20260709.md`와 checker를 추가했다. `state_hash_inputs`는 manifest field only, `plan_hash` canonical bytes는 pending으로 고정했다.

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
- G9:
  - `python -m json.tool pack/sim_standard_parts_catalog_v1/*.detjson` PASS(실행은 개별 detjson 전체).
  - `python -m py_compile tests/run_declarative_closure_g9_standard_parts_catalog_check.py` PASS.
  - `python tests/run_pack_golden.py sim_standard_parts_catalog_v1` PASS.
  - `python tests/run_declarative_closure_g9_standard_parts_catalog_check.py` PASS.
  - `git status --short -- docs/ssot` PASS(변경 없음).
- G10:
  - `python -m json.tool pack/sim_agent_rng_stream_v1/*.detjson` PASS(실행은 개별 detjson 전체).
  - `python -m py_compile tests/run_declarative_closure_g10_agent_rng_stream_red_check.py` PASS.
  - `python tests/run_pack_golden.py sim_agent_rng_stream_v1` PASS.
  - `python tests/run_declarative_closure_g10_agent_rng_stream_red_check.py` PASS.
  - `git status --short -- docs/ssot` PASS(변경 없음).
- G11:
  - `python -m py_compile tests/run_declarative_closure_g11_plan_hash_boundary_check.py` PASS.
  - `python tests/run_declarative_closure_g11_plan_hash_boundary_check.py` PASS.
  - `git status --short -- docs/ssot` PASS(변경 없음).

## 종합 검증

- 신규:
  - `python tests/run_declarative_closure_g7_constraint_red_check.py` PASS.
  - `python tests/run_declarative_closure_g8_experiment_manifest_check.py` PASS.
  - `python tests/run_declarative_closure_g9_standard_parts_catalog_check.py` PASS.
  - `python tests/run_declarative_closure_g10_agent_rng_stream_red_check.py` PASS.
  - `python tests/run_declarative_closure_g11_plan_hash_boundary_check.py` PASS.
- 회귀:
  - `python tests/run_declarative_closure_g4_connect_check.py` PASS.
  - `python tests/run_declarative_closure_g5_unit_check.py` PASS.
  - `python tests/run_declarative_closure_g6_init_vector_check.py` PASS.
  - `cargo check` PASS(기존 dead code warning만 발생).
  - `cargo check --manifest-path tools/teul-cli/Cargo.toml` PASS.
  - `python tests/run_ci_sanity_gate.py --profile core_lang` PASS.
  - `git status --short -- docs/ssot` PASS(변경 없음).

## 커밋

- `31cdc82 [DC-RUN3-G0] start declarative closure run3a`
- `5061778 [DC-G7-CONSTRAINT-RED] add constraint reaction red packs`
- `4b61119 [DC-G8-EXPERIMENT-MANIFEST] add experiment manifest fixture`
- `22d97b0 [DC-G9-STANDARD-PARTS] add standard parts catalog`
- `e50d63d [DC-G10-RNG-STREAM-RED] add per-agent rng stream proof fixtures`
- `53df9f8 [DC-G11-PLAN-HASH] document solveplan plan hash boundary`

## 운영 메모

- G8 커밋 직후 main ref가 queue 선행 커밋으로 fast-forward된 상태를 확인했다. `codex/queue-20260706`를 G8까지 fast-forward한 뒤, main ref는 reflog의 정상 복구점 `fd1132e`로 되돌렸다. 최종 작업 브랜치는 `codex/queue-20260706`이다.
- `python tests/run_ci_sanity_gate.py --profile core_lang` 실행 중 `pack/open_bundle_artifact/run_bundle/geoul.diag.jsonl`, `pack/open_end_to_end/open.log.jsonl`가 재생성됐고, 이번 작업 산출물이 아니므로 해당 두 tracked side effect만 복구했다.
- 기존 untracked 참고 파일은 커밋하지 않았다.
