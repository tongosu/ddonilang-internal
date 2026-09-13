# 2026-07-11 Codex Session Delta - Seamgrim Wave 2D First View Authoring

## 시작 상태

- Branch: `codex/queue-20260706`
- Start HEAD observed: `1f224d3 fix(governance): close archive reference gaps`
- Wave 2D roadmap baseline: `38f423b test(seamgrim): stabilize wave2c representative evidence`
- HEAD delta from roadmap baseline: `1f224d3`, governance/archive reference fix only; no Wave2D product files in that commit.
- Existing dirty/untracked preserved:
  - modified context/report/session files under `docs/context/**`, `docs/reports/audit/INDEX.md`, `work/_session_deltas/20260711_codex_seamgrim_next_superlong_goal.md`
  - unrelated untracked `work/_session_deltas/20260709_*`, `20260710_*`, `20260711_*`, `work/beta/**`, `work/claude/**`, `work/codex/**`, `또니랑/**`
- `docs/ssot/**`: clean at start.

## 읽은 근거

- `AGENTS.md`
- `AGENT_WORKFLOW.md`
- `SSOT_POLICY.md`
- `ARTIFACT_POLICY.md`
- `docs/context/all/DEV_SUMMARY.md`
- `docs/context/roadmap/CODEX_SUPERLONG_GOAL_SEAMGRIM_WAVE2D_FIRST_VIEW_AUTHORING_V1_20260711.md`
- `docs/reports/audit/SEAMGRIM_WAVE2C_INDEPENDENT_COMPLETION_AUDIT_V1_20260711.md`
- `work/_session_deltas/20260711_codex_seamgrim_wave2c_first_external_success.md`

## G0 기준선

- PASS: `python tests/run_seamgrim_wave2c_first_success_check.py`
- PASS: `python tests/run_seamgrim_wave2c_local_success_check.py`
- PASS: `python tests/run_seamgrim_wave2b_quality_gate_check.py`
- PASS: `python tests/run_seamgrim_wave2d_first_view_baseline_check.py`
- PASS: `git status --short -- docs/ssot`

## G0 baseline failure vectors

Captured by `pack/seamgrim_wave2d_first_view_baseline_v1/baseline_metrics.detjson`.

- `toolbar_command_group_missing`: desktop toolbars have no explicit command/view grouping.
- `toolbar_view_group_missing`: desktop view controls are not separated as a second group/menu.
- `tablet_ddn_before_visual`: at `1024x768`, DDN appears before the primary visual.
- `mobile_primary_visual_too_short`: at `390x844`, primary visual height is below 360px and below the product gate.
- `mobile_advanced_controls_not_collapsed`: mobile still exposes advanced measurement controls in the first toolbar.
- `card_preview_space_not_reserved`: representative card preview has no visible reserved box before hydration.
- `card_preview_hydration_timeout`: selected representative card preview did not hydrate within the measurement timeout.

Boundaries held:

- No `docs/ssot/**` changes.
- No product behavior change in G0.
- No new DDN syntax.
- No runtime `state_hash` formula change.

## G1 실행 도구막대 명령군 분리

- 구현:
  - `.run-control-bar` 내부를 `run-context-group`, `run-file-group`, `run-command-group`, `run-view-group`, `run-delivery-tool-group`으로 분리.
  - 기존 버튼 id, tooltip, aria, data-testid는 유지.
  - first-delight desktop에서는 실행 명령군과 보기 도구군을 보이고, context/file/delivery 군은 숨김.
  - mobile first-delight에서는 실행/일시정지/초기화와 DDN toggle만 전면 배치하고 step/status/측정/보기군은 전면에서 제외.
- 측정:
  - `node tests/seamgrim_wave2d_first_view_authoring_runner.mjs --mode=measure`
  - G0의 `toolbar_command_group_missing`, `toolbar_view_group_missing`, `mobile_advanced_controls_not_collapsed` failure vector가 사라짐.
- 검증:
  - PASS: `python tests/run_seamgrim_wave2c_first_success_check.py`
  - PASS: `python tests/run_seamgrim_wave2d_first_view_baseline_check.py`
  - PASS: `git diff --check -- solutions/seamgrim_ui_mvp/ui/index.html solutions/seamgrim_ui_mvp/ui/styles.css`
  - PASS: `git status --short -- docs/ssot`

## G2 주 시각화 우선 반응형 배치

- 구현:
  - `1024x768` first-delight에서 `.run-visual-column`을 grid row 1, DDN editor를 row 2로 배치해 주 시각화가 DDN보다 먼저 나오게 함.
  - tablet/mobile first-delight의 보개 frame/canvas 최소 높이를 360px로 고정.
  - mobile first-delight에서는 수업 설명 brief를 첫 화면 전면에서 숨겨 제목/실행/주 시각화 우선순위를 확보.
  - non-first-delight 실행바 group wrap에서 보기군이 실행 버튼 위를 덮지 않도록 flex wrapping과 semantic graph canvas 최소 높이를 보정.
- 측정:
  - `node tests/seamgrim_wave2d_first_view_authoring_runner.mjs --mode=measure`
  - G1 후 남았던 `tablet_ddn_before_visual`, `mobile_primary_visual_too_short` failure vector가 사라짐.
  - 남은 failure vector: `card_preview_space_not_reserved`, `card_preview_hydration_timeout`.
- 검증:
  - PASS: `python tests/run_seamgrim_responsive_lesson_workflow_check.py`
  - PASS: `python tests/run_seamgrim_wave2c_first_success_check.py`
  - PASS: `git diff --check -- solutions/seamgrim_ui_mvp/ui/styles.css`
  - PASS: `git status --short -- docs/ssot`

## G3 저작 공간 확장과 실행 왕복

- 구현:
  - DDN 원문 preview 기본 최소 높이를 240px로 높여 모바일 토글 상태에서도 읽을 수 있는 원문 영역을 확보.
  - `#ddn-textarea` 저작 공간 최소 높이를 480px로 높여 1440px desktop에서 코드 편집 영역이 보조 패널처럼 작아지지 않게 조정.
  - Wave2D browser runner에 `--mode=workflow`를 추가해 카드 실행, 모바일 DDN toggle, 만들기 탭 이동, world-code/lesson-plan tab 왕복, 편집 후 실행을 독립 검증.
  - 실행 버튼은 auto-run 상태에서 disabled일 수 있으므로, 사용 가능할 때만 클릭하고 이미 실행 상태면 그대로 검증.
- 검증:
  - PASS: `node tests/seamgrim_wave2d_first_view_authoring_runner.mjs --mode=workflow`
  - PASS: `python tests/run_seamgrim_wave2c_first_success_check.py`
  - PASS: `python tests/run_seamgrim_responsive_lesson_workflow_check.py`
  - PASS: `git diff --check -- solutions/seamgrim_ui_mvp/ui/styles.css tests/seamgrim_wave2d_first_view_authoring_runner.mjs`
  - PASS: `git status --short -- docs/ssot`

## G4 대표 카드 preview 안정화

- 구현:
  - 대표 카드 preview를 `hidden` 상태로 만들지 않고, 처음부터 `data-preview-state="loading"` skeleton으로 렌더링해 비동기 로딩 전 공간을 예약.
  - `.card-structure-preview`에 고정 `aspect-ratio: 4 / 3`과 `min-height: 112px`를 적용하고, hydration 전후 외곽 높이 변화가 없도록 조정.
  - hydration 실패/미지원 preview도 컨테이너를 숨기지 않고 `data-preview-state="empty"` fallback을 유지.
  - 기본 카드에서 상세 결과/배포/준비/활동/목표/미션 텍스트를 시각적으로 숨기고, 제목/학년·교과/한 문장 목표/primary view/두 실행 명령만 전면 노출.
  - 패키지 증거용 legacy delivery token은 source-level 증거로만 유지하고, 기본 화면의 보이는 delivery 문구는 G7에서 역할 없는 `수업 열기 · 실험실 변경`으로 정리.
- 검증:
  - PASS: `node tests/seamgrim_wave2d_first_view_authoring_runner.mjs`
  - PASS: `python tests/run_seamgrim_wave2c_first_success_check.py`
  - PASS: `python tests/run_seamgrim_wave2d_first_view_baseline_check.py`
  - PASS: `git diff --check -- solutions/seamgrim_ui_mvp/ui/screens/browse.js solutions/seamgrim_ui_mvp/ui/styles.css tests/seamgrim_wave2d_first_view_authoring_runner.mjs`
  - PASS: `git status --short -- docs/ssot`
- 발견:
  - `node tests/studio_local_package_export_action_runner.mjs`는 카드 변경 후 delivery 정적 문자열 실패는 해소했지만, 기존 `active allowlist count mismatch: 16`에서 별도 실패.
  - `python tests/run_seamgrim_wave2c_local_success_check.py`는 240초 timeout. G7 최종 회귀에서 별도 원인 확인 필요.

## G5 로컬 검수 서버 no-store 계약

- 구현:
  - 기존 `solutions/seamgrim_ui_mvp/tools/ddn_exec_server.py`의 JSON API 응답에 `Cache-Control: no-store, max-age=0`을 추가.
  - OPTIONS와 favicon 204 응답에도 no-store를 명시.
  - 새 제품 서버를 만들지 않고, 기존 `ddn_exec_server.py`를 직접 띄우는 checker를 추가.
  - checker는 `/`, `/ui/app.js`, `/api/health`, `/api/lessons/inventory`의 no-store를 확인하고, 같은 `/build/reports/...` URL에서 파일 bytes를 v1->v2로 바꾼 뒤 같은 포트 재요청이 최신 bytes를 반환하는지 검증.
- 검증:
  - PASS: `python -m py_compile tests/run_seamgrim_wave2d_local_review_server_check.py solutions/seamgrim_ui_mvp/tools/ddn_exec_server.py`
  - PASS: `python tests/run_seamgrim_wave2d_local_review_server_check.py`
  - PASS: `node tests/seamgrim_wave2d_first_view_authoring_runner.mjs`
  - PASS: `python tests/run_seamgrim_wave2c_first_success_check.py`
  - PASS: `git diff --check -- solutions/seamgrim_ui_mvp/tools/ddn_exec_server.py tests/run_seamgrim_wave2d_local_review_server_check.py`
  - PASS: `git status --short -- docs/ssot`

## G6 Wave2D pack/checker 통합

- 구현:
  - `pack/seamgrim_wave2d_first_view_authoring_v1` 추가.
  - pack contract에 G1~G5 product checks, 네 viewport, no-store/latest-byte smoke, SSOT/state_hash/DDN 문법 경계를 기록.
  - `tests/run_seamgrim_wave2d_first_view_authoring_check.py` 추가.
  - checker가 product token, local review server checker, browser runner, pack golden, `docs/ssot/**` clean 상태를 한 번에 검증.
- 검증:
  - PASS: `python -m py_compile tests/run_seamgrim_wave2d_first_view_authoring_check.py`
  - PASS: `python tests/run_seamgrim_wave2d_first_view_authoring_check.py`
  - PASS: `python tests/run_pack_golden.py seamgrim_wave2d_first_view_authoring_v1`
  - PASS: `python tests/run_seamgrim_wave2c_first_success_check.py`
  - PASS: `python tests/run_seamgrim_wave2d_local_review_server_check.py`
  - PASS: `git diff --check -- pack/seamgrim_wave2d_first_view_authoring_v1 tests/run_seamgrim_wave2d_first_view_authoring_check.py`
  - PASS: `git status --short -- docs/ssot`

## G7 최종 검증과 회귀 수리

- 구현:
  - `buildCourseDeliveryText()`의 보이는 문구를 `학생 실행 · 교사용 배포`에서 `수업 열기 · 실험실 변경`으로 되돌려 기본 UI에서 legacy role entry가 노출되지 않게 함.
  - 정적 packaging evidence token은 `browse.js` source 내부에만 남겨 기존 package runner의 source-level 경계는 유지.
  - semantic cursor가 pause/재렌더 중 값 없는 중간 observation을 받으면 직전 정상 anchor 값을 보존하도록 `syncSemanticCursorView()`에 carried-forward 경로 추가.
  - 이 보존 경로는 view-only UI state이며 `state_hash` 산식이나 world state를 변경하지 않음.
- 검증:
  - PASS: `python tests/run_seamgrim_wave2d_first_view_authoring_check.py`
  - PASS: `node tests/seamgrim_wave2d_first_view_authoring_runner.mjs`
  - PASS: `python tests/run_seamgrim_wave2c_first_success_check.py`
  - PASS: `python tests/run_seamgrim_wave2c_local_success_check.py`
  - PASS: `python tests/run_seamgrim_pendulum_view_plan_product_check.py`
  - PASS: `python tests/run_seamgrim_wave2b_representative_worlds_check.py`
  - PASS: `python tests/run_pack_golden.py seamgrim_wave2d_first_view_authoring_v1 seamgrim_wave2c_local_success_v1 seamgrim_wave2b_representative_worlds_v1 seamgrim_wave2b_quality_gate_v1 seamgrim_pendulum_view_plan_product_v1`
  - PASS: `python tests/run_seamgrim_semantic_cursor_check.py`
  - PASS: `python tests/run_seamgrim_ui_v2_product_shell_check.py`
  - PASS: `python tests/run_seamgrim_wave2b_quality_gate_check.py`
  - PASS via quality gate: `cargo check`
  - PASS via quality gate: `cargo check --manifest-path tools/teul-cli/Cargo.toml`
  - PASS via quality gate: `python tests/run_ci_sanity_gate.py --profile core_lang`
  - PASS via quality gate: `git diff --check`
  - PASS via quality gate: `git status --short -- docs/ssot`
- 부산물:
  - sanity gate가 갱신한 `pack/open_bundle_artifact/run_bundle/geoul.diag.jsonl`, `pack/open_end_to_end/open.log.jsonl`는 검증 부산물로 복원.
