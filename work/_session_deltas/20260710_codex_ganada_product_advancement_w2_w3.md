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
