# 2026-07-10 Codex Session Delta - Ganada Product Advancement W1

## 목표
- Ganada Product Advancement Week 1 계획을 실행한다.
- 우선순위는 마줄기 실행 재감사, 마줄기 lesson 제품 실행 수리, 마줄기 UI/workbench 연결, 자줄기 슬기 UI 연결, 타줄기 evidence gate hardening 순서다.

## 시작 상태
- 브랜치: `codex/queue-20260706`.
- 시작 전 tracked dirty: `docs/context/all/DEV_SUMMARY.md`.
- 시작 전 untracked 참고 파일: `work/_session_deltas/20260709_codex_recent_proposals_reflection.md`, `work/_session_deltas/20260710_codex_gaji_forest_product_plan.md`, `work/_session_deltas/20260710_codex_korean_manim_ssot_reflection.md`, `또니랑/*.md`.
- 시작 전 dirty `DEV_SUMMARY.md`는 Korean-Manim/SSOT addendum 관련 기존 hunk로 확인했다. 이번 작업 커밋에는 별도 staging으로 섞지 않는다.

## 경계
- `docs/ssot/**` 직접 수정 금지.
- 언어 parser/runtime 문법, runtime `state_hash` 산식 변경 금지.
- 실제 모델 호출 금지. 슬기/AI 증거는 deterministic fixture/provenance 기반으로만 둔다.
- `닫힘-동작`은 제품 실행 PASS와 재현 가능한 pack/checker PASS가 있을 때만 제안한다.
- 기존 untracked 참고 파일은 커밋하지 않는다.

## 진행 로그
- GVC-W1-G0: 시작 상태와 경계를 기록했다.
- GVC-W1-MA-REAUDIT: `ganada_ma_branch_execution_reaudit_v1` pack/checker를 추가했다. `마-0`~`마-5`는 실제 명령 기반으로 재감사했고, legacy claim gate 실패 3건은 repair queue로 남겼다.
- GVC-W1-MA-LESSON: `ganada_ma_representative_lessons_v1` pack/checker를 추가했다. 대표 lesson 4종은 math/physics/econ/science로 고정했고, science는 `rep_science_phase_change_timeline_v1` 제품 실행 hash를 새 smoke로 기록했다.
- GVC-W1-MA-UI: lesson catalog/preset/run/result/error 안정 selector를 추가하고 `seamgrim_lesson_run_preset_rail_runner.mjs`가 실제 catalog 선택 후 제품 실행 결과와 `blake3:` state hash를 확인하도록 보강했다.
- GVC-W1-JA-UI: 슬기 proposal/replay UI에 `seulgi-proposal-panel`, `seulgi-approve`, `seulgi-reject`, `seulgi-boundary-warning`, `seulgi-replay-log` selector를 추가했다. runner는 fixture/provenance 기반 UI만 검증하며 AI 호출/auto-apply/file write/runtime claim은 false로 유지한다.
- GVC-W1-TA-GATE: `ganada_execution_evidence_registry_v1` pack/checker를 추가했다. Week1 touched cell 8개(`마-0`~`마-5`, `자-3`, `자-5`)의 실행 명령, runner, PASS marker, file:line 근거를 추적하고 docs-only behavior close negative control을 reject로 고정했다.

## 커밋
- `e06f2de [GVC-W1-G0] start ganada product advancement week`
- `be39c47 [GVC-W1-MA-REAUDIT] add ma branch execution reaudit gate`
- `7117440 [GVC-W1-MA-LESSON] add representative lesson product gate`
- `d0845e6 [GVC-W1-MA-UI] wire lesson workflow selectors`
- `1078437 [GVC-W1-JA-UI] harden seulgi workflow selectors`
- `bb80456 [GVC-W1-TA-GATE] add ganada execution evidence registry`

## 결과 요약
- Day 1 마줄기 실행 재감사: 완료. 6칸 전체 실제 명령 기반 재감사 완료, 상태 승격 없음, repair queue 명시.
- Day 2 대표 lesson 제품 실행 수리: 완료. 4종 대표 lesson product smoke/golden PASS.
- Day 3 마줄기 UI/workbench 연결: 완료. catalog -> preset -> 제품 실행 결과 workflow browser PASS.
- Day 4 자줄기 슬기 UI 배선: 완료. proposal approve/reject, boundary warning, replay-safe log browser PASS.
- Day 5 타줄기 gate hardening: 완료. evidence registry checker가 docs-only behavior closure를 거부하고 strong execution evidence를 요구.
- `docs/ssot/**`: 변경 없음.
- parser/runtime/state_hash: 변경 없음.

## 결정 필요 / Repair Queue
- `마-0`: legacy matrix checker가 stale 90/90 status count에 묶여 있어 product evidence와 분리 필요.
- `마-1`: legacy reconciliation checker가 stale `DEV_SUMMARY.md` token에 의존한다.
- `마-4`: publication prep/review status check가 stale `DEV_SUMMARY.md` token에 의존한다.
- `마-2`/`마-3`/`마-5`: 제품 실행 증거는 기록됐지만 기존 prereq contract가 not-closed 경계를 유지하므로 별도 재판정 필요.
- `자-3`/`자-5`: 제품 UI runner PASS 증거는 갱신됐지만 행렬 상태 재판정은 이번 배치 범위 밖이다.

## 검증
- `python tests/run_ganada_ma_branch_execution_reaudit_check.py` PASS.
- `python tests/run_pack_golden.py ganada_ma_branch_execution_reaudit_v1 ganada_ma_representative_lessons_v1 ganada_maru_verification_contract_v1 ganada_execution_evidence_registry_v1` PASS.
- `python tests/run_ganada_ma_representative_lessons_check.py` PASS.
- `python tests/run_ganada_execution_evidence_registry_check.py` PASS.
- `python tests/run_ganada_maru_verification_contract_check.py` PASS.
- `python tests/run_roadmap_v2_ja_seulgi_boundary_reconciliation_check.py` PASS.
- `python tests/run_roadmap_v2_ja3_seulgi_proposal_ui_check.py` PASS.
- `python tests/run_roadmap_v2_ja5_replay_safe_ai_workflow_check.py` PASS.
- `node tests/seamgrim_lesson_run_preset_rail_runner.mjs` PASS.
- `node tests/seamgrim_lesson_authoring_flow_browser_runner.mjs` PASS.
- `node tests/studio_lesson_authoring_run_integration_runner.mjs` PASS.
- `node tests/seulgi_proposal_ui_runner.mjs` PASS.
- `node tests/seulgi_replay_safe_workflow_runner.mjs` PASS.
- `python tests/run_ci_sanity_gate.py --profile core_lang` PASS.
- `cargo check` PASS, 기존 dead-code warning 출력.
- `git diff --check` PASS, `docs/context/all/DEV_SUMMARY.md` CRLF/LF 경고만 출력.
- `git status --short -- docs/ssot` clean.
