# 2026-07-10 Codex Session Delta - Ganada Product Advancement W2-W3

## 목표
- Ganada Product Advancement Week2-3 계획을 실행한다.
- 우선순위는 마줄기 stale checker repair, 마줄기 제품 workflow 강화, 자줄기 Seulgi 실사용 workflow, 타줄기 registry v2 gate 확장 순서다.

## 시작 상태
- 브랜치: `codex/queue-20260706`.
- 시작 전 tracked dirty: `docs/context/all/DEV_SUMMARY.md`.
- 시작 전 untracked 참고 파일: `work/_session_deltas/20260709_codex_recent_proposals_reflection.md`, `work/_session_deltas/20260710_codex_gaji_forest_product_plan.md`, `work/_session_deltas/20260710_codex_korean_manim_ssot_reflection.md`, `work/_session_deltas/20260710_codex_ssot_g0_g8_evidence_reflection.md`, `또니랑/*.md`.
- 시작 전 `docs/ssot/**`: clean.
- 기존 dirty `DEV_SUMMARY.md` hunk와 untracked 참고 파일은 이번 batch 커밋에 섞지 않는다.

## 경계
- `docs/ssot/**` 직접 수정 금지.
- parser/runtime 문법, runtime `state_hash` 산식 변경 금지.
- 실제 AI model call, auto-apply, file write, runtime AST persistence claim 금지.
- publication은 local dry-run만 허용한다. 공개/업로드/릴리스 승인/외부 배포 claim 금지.
- LTS는 readiness/regression evidence만 허용한다. certification claim 금지.

## Day1 재현 로그
- `python tests/run_roadmap_v2_ma0_curriculum_catalog_check.py` FAIL: `matrix counts mismatch: rows=90 behavior=90 docs=0`.
- `python tests/run_roadmap_v2_ma1_lesson_first_run_reconciliation_check.py` FAIL: nested `tests/run_studio_lesson_authoring_run_integration_check.py`가 stale `DEV_SUMMARY.md` token 4개를 요구한다.
- `python tests/run_studio_public_lesson_publication_prep_check.py` FAIL: stale `DEV_SUMMARY.md` token 4개를 요구한다.

## 진행 로그
- GVC-W2-G0: 시작 상태, 경계, current failing legacy checker 3개를 기록했다.
- GVC-W2-MA-REPAIR: `마-0/마-1/마-4` stale checker를 execution evidence registry 기반으로 수리하고 `ganada_ma_closure_repair_v1`을 추가했다.
- GVC-W2-MA2-ASSESS: assessment panel에 `assessment-panel/run/result/feedback` selector를 추가하고 lesson-run source 기반 browser gate `ganada_ma_assessment_workflow_v1`을 추가했다.
- GVC-W2-MA3-CLASSROOM: classroom UI에 teacher/student/roster/result review/report export local dry-run workflow gate `ganada_ma_classroom_workflow_v1`을 추가했다.
- GVC-W2-MA4-PUBLICATION: publication review/local dry-run/artifact preview/boundary warning workflow gate `ganada_ma_publication_dryrun_workflow_v1`을 추가했다.
- GVC-W2-MA5-LTS: local runner matrix, operations report, no-certification regression gate `ganada_ma_lts_readiness_workflow_v1`을 추가했다.
- GVC-W3-JA-SEULGI-CONTEXT: Seulgi proposal/replay UI를 lesson/editor fixture context와 연결하고 `ganada_ja_seulgi_context_v1`을 추가했다.
- GVC-W3-JA-RECEIPTS: fixture proposal import, preview, approve/reject receipt, replay-safe provenance를 `ganada_ja_seulgi_local_workflow_v1`으로 묶었다.
- GVC-W3-TA-REGISTRY-V2: Week2-3 product evidence를 `ganada_execution_evidence_registry_v2`로 확장하고 docs-only behavior closure negative control을 유지했다.
- GVC-W3-JA-FIX: core sanity의 observer registry check가 UI 파일 내 `reset` substring을 금지해, Seulgi lesson context label을 `seamgrim_lesson_run_rail_v1`로 바꿨다.

## 결과 요약
- 완료: Day1~Day9 계획 항목 전부 처리.
- 마줄기: stale checker 3개 repair 완료, `마-2` assessment, `마-3` classroom, `마-4` publication dry-run, `마-5` LTS readiness product workflow gate 추가.
- 자줄기: Seulgi fixture import, preview, approve/reject receipt, replay-safe log workflow 추가.
- 타줄기: `ganada_execution_evidence_registry_v2`가 Week2-3 touched cells 증거를 기계적으로 추적하고 docs/status-only behavior closure를 reject.
- 닫힘 주장: 신규 장기 `닫힘-동작` 승격은 하지 않음. product/browser/checker PASS 증거만 누적.

## 검증
- PASS `python tests/run_ganada_ma_closure_repair_check.py`
- PASS `python tests/run_ganada_ma_assessment_workflow_check.py`
- PASS `python tests/run_ganada_ma_classroom_workflow_check.py`
- PASS `python tests/run_ganada_ma_publication_dryrun_check.py`
- PASS `python tests/run_ganada_ma_lts_readiness_check.py`
- PASS `python tests/run_ganada_ja_seulgi_context_check.py`
- PASS `python tests/run_ganada_ja_seulgi_local_workflow_check.py`
- PASS `python tests/run_ganada_execution_evidence_registry_v2_check.py`
- PASS `python tests/run_ganada_maru_verification_contract_check.py`
- PASS `python tests/run_pack_golden.py ganada_maru_verification_contract_v1 ganada_execution_evidence_registry_v1 ganada_execution_evidence_registry_v2`
- PASS `python tests/run_ci_sanity_gate.py --profile core_lang`
- PASS `cargo check` (기존 dead_code warnings)
- PASS `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS `git diff --check` (기존 dirty DEV_SUMMARY CRLF/LF 경고만 표시)
- PASS `git status --short -- docs/ssot`

## 경계 확인
- `docs/ssot/**` 변경 없음.
- parser/runtime 문법 변경 없음.
- runtime `state_hash` 산식 변경 없음.
- 실제 AI call, auto-apply, file write, runtime AST persistence claim 없음.
- publication은 local dry-run only, LTS는 readiness/regression only.

## 남은 워킹트리 주의
- 기존 dirty `docs/context/all/DEV_SUMMARY.md` hunk는 SSOT/Korean-Manim/용어 감사 내용이며 이번 batch 커밋에 포함하지 않았다.
- `docs/context/reports/INDEX.md` dirty hunk도 외부/기존 변경으로 간주해 포함하지 않았다.
- 기존 untracked 참고 파일과 `또니랑/*.md`도 커밋하지 않았다.
