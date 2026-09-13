# 20260710 Codex GVC W9 Stale Checker Repair

## 결과 요약

- 상태: 완료.
- 브랜치: `codex/queue-20260706`.
- 범위: W8 완료 후 별도 수리 후보로 남은 stale checker 4건을 제품/pack/runner evidence 기준으로 수리.
- 비범위: 90칸 매트릭스 재판정, 새 `닫힘-동작` 주장, `docs/ssot/**` 수정, parser/runtime/state_hash 변경.

## 시작 상태

- `git branch --show-current`: `codex/queue-20260706`.
- `git status --short -- docs/ssot`: 변경 없음.
- 기존 dirty/untracked 항목은 W9 범위 밖으로 유지:
  - `docs/context/all/DEV_SUMMARY.md`
  - `docs/context/reports/INDEX.md`
  - `docs/reports/audit/INDEX.md`
  - `docs/reports/impl/INDEX.md`
  - `solutions/seamgrim_ui_mvp/**`
  - `pack/seamgrim_first_delight_projectile_v1/`
  - 기타 `work/_session_deltas/**`, `또니랑/**` 참고 파일

## Baseline 재현

- `python tests/run_roadmap_v2_a3_nurigym_python_web_parity_check.py`
  - 이전 실패: `matrix counts mismatch: rows=90 behavior=90 docs=0`
- `python tests/run_roadmap_v2_a5_nurigym_training_workflow_check.py`
  - 이전 실패: `matrix counts mismatch: rows=90 behavior=90 docs=0`
- `python tests/run_std_grid_game_bogae_browser_dom_smoke_check.py`
  - 이전 실패: `missing file: NEXT_DEV_ROADMAP_AFTER_VIEWER_JS_DOM_V2.md`
- `python tests/run_std_grid_game_bogae_web_playback_controls_check.py`
  - 이전 실패: `missing file: STD_GRID_GAME_BOGAE_WEB_SHOWCASE_7DAY_V1.md`

## 변경

- `tests/run_roadmap_v2_a3_nurigym_python_web_parity_check.py`
  - 오래된 Ganada matrix count / `DEV_SUMMARY` token 의존 제거.
  - `nurigym_python_web_parity_v1` pack, NuriGym source packs, Web parity runner, UI module evidence 기준으로 검증.
- `tests/run_roadmap_v2_a5_nurigym_training_workflow_check.py`
  - 오래된 Ganada matrix count / status token 의존 제거.
  - `nurigym_training_workflow_v1`, dataset registry, A3 parity, `run_v25_first_ai_production_path_pack_check.py` 기준으로 검증.
  - 참고: `v25_first_ai_production_path_v1`의 직접 `run_pack_golden.py` 기대 hash는 현재 A5 gate 기준으로 쓰지 않고, 전용 pack checker를 제품 evidence로 사용한다.
- `tests/run_std_grid_game_bogae_browser_dom_smoke_check.py`
  - 누락된 root markdown 요구 제거.
  - live web assets pack, generated assets, Playwright smoke runner, browser DOM smoke pack 기준으로 검증.
- `tests/run_std_grid_game_bogae_web_playback_controls_check.py`
  - 누락된 root markdown 요구 제거.
  - playback assets/controls/closure packs, generated viewer asset/manifest/control evidence 기준으로 검증.
- 신규 pack/checker:
  - `pack/ganada_stale_checker_repair_w9_v1/`
  - `tests/run_ganada_stale_checker_repair_w9_check.py`
  - 수리된 4건을 다시 실행하고, 제거 대상 legacy token이 checker 본문에 남아 있지 않은지 확인.

## 증거

- `python -m py_compile tests/run_roadmap_v2_a3_nurigym_python_web_parity_check.py tests/run_roadmap_v2_a5_nurigym_training_workflow_check.py tests/run_std_grid_game_bogae_browser_dom_smoke_check.py tests/run_std_grid_game_bogae_web_playback_controls_check.py tests/run_ganada_stale_checker_repair_w9_check.py` PASS.
- `python -m json.tool pack/ganada_stale_checker_repair_w9_v1/repair.detjson` PASS.
- `python tests/run_pack_golden.py ganada_stale_checker_repair_w9_v1` PASS.
- `python tests/run_ganada_stale_checker_repair_w9_check.py` PASS.
- `python tests/run_roadmap_v2_a3_nurigym_python_web_parity_check.py` PASS.
- `python tests/run_roadmap_v2_a5_nurigym_training_workflow_check.py` PASS.
- `python tests/run_std_grid_game_bogae_browser_dom_smoke_check.py` PASS.
- `python tests/run_std_grid_game_bogae_web_playback_controls_check.py` PASS.
- `python tests/run_ganada_execution_evidence_registry_v4_check.py` PASS.
- `python tests/run_ganada_maru_verification_contract_check.py` PASS.
- `python tests/run_pack_golden.py ganada_maru_verification_contract_v1 ganada_execution_evidence_registry_v4 ganada_stale_checker_repair_w9_v1` PASS.
- `cargo check` PASS with existing warnings.
- `cargo check --manifest-path tools/teul-cli/Cargo.toml` PASS.
- `python tests/run_ci_sanity_gate.py --profile core_lang` PASS.
- `git diff --check` PASS. CRLF warnings only.
- `git status --short -- docs/ssot` clean.

## 정리

- sanity gate 실행 중 생성된 `pack/open_bundle_artifact/run_bundle/geoul.diag.jsonl`, `pack/open_end_to_end/open.log.jsonl` 변경은 검증 부산물이라 되돌렸다.
- `docs/context/all/DEV_SUMMARY.md`는 기존 dirty hunk가 있어 이번 W9 커밋에 섞지 않았다.

## 다음 후보

- 이제 stale checker 4건은 별도 repair 후보에서 제거 가능하다.
- 다음 큰 작업은 `ganada_execution_evidence_registry_v4`와 GVC contract 기준으로 90칸 전체 상태를 재판정하는 dry-run 보고서다. 이때도 `닫힘-문서` / `닫힘-동작` / `실패`를 분리하고, 이번 W9는 matrix 승격 근거가 아니라 stale gate 수리 근거로만 사용한다.
