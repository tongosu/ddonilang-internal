# 2026-07-11 Codex Session Delta - Seamgrim Wave 2B Authoring Deploy Vertical

## 시작 상태

- Branch: `codex/queue-20260706`
- Start commit: `63f7637 fix(seamgrim): remove runtime role switch`
- Objective: `C:\Users\ddongosu\.codex\attachments\f61259f2-e83c-4afe-a8c3-da43995dc81c\goal-objective.md`
- Scope: Wave 2B G0~G8, Korean Manim authoring + deployment package configuration vertical.
- Boundary:
  - `docs/ssot/**` read-only.
  - No new DDN grammar/core block.
  - No runtime `state_hash` formula change.
  - No login/cloud/IDC deploy/cryptographic signature claim.
  - Preserve unrelated dirty/untracked files and do not stage them.

## 읽은 근거

- `AGENTS.md`
- `AGENT_WORKFLOW.md`
- `SSOT_POLICY.md`
- `ARTIFACT_POLICY.md`
- `docs/context/all/DEV_SUMMARY.md`
- `work/_session_deltas/20260711_codex_wave2a_runtime_role_boundary_fix.md`
- `work/_session_deltas/20260711_codex_wave2a_independent_audit_fix.md`
- `work/_session_deltas/20260711_codex_seamgrim_wave2a_live_semantic_lesson.md`
- `work/_session_deltas/20260711_codex_seamgrim_product_to_korean_manim_vertical.md`
- `docs/ssot/ssot/SSOT_INDEX_v24.12.9.md`
- `docs/ssot/walks/gogae8/gogae_seamgrim_ui_mvp/INDEX.md`
- `docs/ssot/ssot/SSOT_TOOLCHAIN_v24.12.9.md` relevant Seamgrim/Korean Manim/view-state boundary excerpts.
- `docs/ssot/ssot/SSOT_UPDATE_NOTES_v24.12.9.md` relevant Korean Manim/view-plan/state_hash boundary excerpts.

## 기존 dirty/untracked 보존 목록

- `docs/context/all/DEV_SUMMARY.md`
- `docs/context/reports/INDEX.md`
- `docs/reports/audit/INDEX.md`
- `tests/run_ganada_intake_ledger_v1_check.py`
- `tools/build_ganada_intake_ledger_v1.py`
- unrelated `work/_session_deltas/20260709_*`, `20260710_*`, unrelated `20260711_*`
- `work/codex/**`
- `또니랑/**`

## 관문별 결과

| Gate | Status | Notes |
|---|---|---|
| G0 | PASS | Baseline Wave1/Wave2A product checkers, pack golden, and `core_lang` sanity PASS. |
| G1 | PASS | `studio_classroom_mode_switch_v1` runner migrated to superseded/no-runtime-toggle guard; downstream export contract now bases on `STUDIO_CLASSROOM_MODE_V1`. |
| G2 | PASS | Publish workflow moved to independent `#screen-publish`; open/paste/copy/download actions rebound through `publishRoot`; browser isolation pack/checker PASS. |
| G3 | PASS | `deployment_profile.v0` product workflow added. Publish screen edits profile fields, package copy/save payload carries canonical profile hash and package hash, local package reopen shows read-only run profile, tamper detection emits Korean diagnostic, and runtime role switch stays absent. |
| G4 | PASS | Five view-only Korean Manim measurement component families are authored on existing `view_plan.v1`: angle, length, vector arrow, axes/ticks, and trajectory trail. Product toggles, units, accessibility names, view-hash candidates, and `state_hash` non-participation are browser-verified. |
| G5 | PASS | `만들기 > 수업 구성` now exposes product authoring controls for camera policy, measurement components, semantic anchor, four reaction conditions, three reaction actions, and explicit priority. Same anchor/property/priority conflicts emit `E_VIEW_AUTHOR_REACTION_CONFLICT` and implicit LWW stays disabled. |
| G6 | PASS | `lesson_plan.v0` now preserves activity-level scene, primary view, camera policy, measurement components, reaction rule refs, `view_authoring_hash`, and `view_plan_ref`; editor structure view and code view roundtrip to the same canonical TOML. |
| G7 | PASS | Representative pendulum/projectile/linear worlds now have product browser vertical evidence for DDN source, WASM state hash, primary view roles, observation keys, save/reopen source path, and lesson composition roundtrip. |
| G8 | PASS | Final quality gate pack/checker/browser runner, Wave1/Wave2A regression, Wave2B G3~G7 regression, cargo checks, core_lang sanity, diff check, and `docs/ssot/**` clean check PASS. |

## 기준선 검증

- PASS: `python tests/run_seamgrim_ui_v2_product_shell_check.py`
- PASS: `python tests/run_seamgrim_primary_view_contract_check.py`
- PASS: `python tests/run_seamgrim_lab_e1_minimal_check.py`
- PASS: `python tests/run_seamgrim_pendulum_view_plan_product_check.py`
- PASS: `python tests/run_seamgrim_sealed_trace_reaction_check.py`
- PASS: `python tests/run_seamgrim_wave2a_product_ia_check.py`
- PASS: `python tests/run_seamgrim_live_trace_reaction_check.py`
- PASS: `python tests/run_seamgrim_offline_live_reaction_parity_check.py`
- PASS: `python tests/run_seamgrim_semantic_cursor_check.py`
- PASS: `python tests/run_lesson_plan_roundtrip_v1_check.py`
- PASS after runner boundary fix: `python tests/run_seamgrim_responsive_lesson_workflow_check.py`
  - Initial failure: product dataset already contained `liveTraceReactionFiredActions=...highlight.theta_measure`, but `stepUntil` did not re-check the final sampled state before throwing.
  - Fix: final predicate check added in `tests/seamgrim_responsive_lesson_workflow_runner.mjs`.
- PASS: `python tests/run_pack_golden.py seamgrim_ui_v2_product_shell_v1 seamgrim_primary_view_contract_v1 seamgrim_lab_e1_minimal_v1 seamgrim_pendulum_view_plan_product_v1 seamgrim_sealed_trace_reaction_product_v1 seamgrim_wave2a_product_ia_v1 seamgrim_live_trace_reaction_v1 seamgrim_offline_live_reaction_parity_v1 seamgrim_semantic_cursor_v1 lesson_plan_roundtrip_v1 seamgrim_responsive_lesson_workflow_v1`
- PASS: `python tests/run_ci_sanity_gate.py --profile core_lang`
- Restored generated open-log artifacts after sanity gate:
  - `pack/open_bundle_artifact/run_bundle/geoul.diag.jsonl`
  - `pack/open_end_to_end/open.log.jsonl`

## 결정 / 경계

- Runtime student/teacher switch must not be restored. Deployment profile/package owns student/teacher differences.
- Historical classroom-mode packs may remain as `superseded` evidence, but cannot be used for current behavior closure.
- View/camera/measurement/reaction artifacts are view/tooling layer and must stay outside runtime `state_hash`.

## G1 legacy runtime-role 이관

- Updated `tests/studio_classroom_mode_switch_runner.mjs`:
  - no longer clicks a runtime `학생`/`교사` switch;
  - verifies `pack/studio_classroom_mode_switch_v1/contract.detjson` is `superseded`;
  - verifies Run screen has no `[data-classroom-mode-switch]`, no `[data-classroom-mode]`, no `window.__STUDIO_CLASSROOM_MODE_SWITCH__`, and no runtime role dataset after learn/lab entry.
- Updated `pack/studio_classroom_report_export_action_v1/contract.detjson`:
  - `based_on` changed from `STUDIO_CLASSROOM_MODE_SWITCH_V1` to `STUDIO_CLASSROOM_MODE_V1`.
- PASS: `node tests/studio_classroom_mode_switch_runner.mjs`
- PASS: `python tests/run_pack_golden.py studio_classroom_mode_switch_v1 studio_classroom_report_export_action_v1`
- PASS: `python tests/run_seamgrim_ui_v2_product_shell_check.py`
- PASS: `python tests/run_seamgrim_wave2a_product_ia_check.py`

## G2 publish screen 독립화

- Added independent product screen/container:
  - `solutions/seamgrim_ui_mvp/ui/index.html`: `#screen-publish`, `#publish-panel`, local package open/paste/copy/download controls moved out of `#screen-browse`.
  - `solutions/seamgrim_ui_mvp/ui/app.js`: `MAIN_TAB_PUBLISH`, `setScreen("publish")`, route sync, and shell tab handling.
  - `solutions/seamgrim_ui_mvp/ui/screens/browse.js`: package workflow controls are bound through `publishRoot`.
  - `solutions/seamgrim_ui_mvp/ui/styles.css`: removed `browse-space-publish` state styling; publish has its own screen.
- Added pack/checker/browser runner:
  - `pack/seamgrim_publish_screen_isolation_v1`
  - `tests/seamgrim_publish_screen_isolation_runner.mjs`
  - `tests/run_seamgrim_publish_screen_isolation_check.py`
- PASS: `python tests/run_seamgrim_publish_screen_isolation_check.py`
- PASS: `python tests/run_seamgrim_wave2a_product_ia_check.py`
- PASS: `python tests/run_seamgrim_responsive_lesson_workflow_check.py`
- PASS: `python tests/run_pack_golden.py seamgrim_publish_screen_isolation_v1 seamgrim_wave2a_product_ia_v1 seamgrim_responsive_lesson_workflow_v1`
- PASS: `python tests/run_seamgrim_ui_v2_product_shell_check.py`

## G3 deployment_profile.v0 제품 수직

- Applied preserved WIP from `stash@{0}: seamgrim-wave2b-deployment-profile-wip` without dropping the stash.
  - This Git version does not support `git stash apply --include-untracked`; tracked changes were applied with `git stash apply 'stash@{0}'`, and the stash apply restored the untracked pack/checker/runner files into the worktree.
- Added product profile model and deterministic candidate hashes:
  - `solutions/seamgrim_ui_mvp/ui/studio_local_share_package.js`
  - `buildDeploymentProfileV0`, `profile_hash`, `deployment_profile_hash`, `package_hash_inputs`, `package_hash`.
  - Package hash includes `deployment_profile`.
  - `state_hash` formula and cryptographic signature claims remain unchanged/false.
- Added publish screen profile editor:
  - `preset_ref`
  - allowed control name/min/max/step
  - answer/explanation display policy
  - default/allowed views
  - run/restart policy
  - live profile hash preview
- Added product roundtrip:
  - package copy/export includes `deployment_profile`.
  - local package paste/open validates profile hash and package hash.
  - run screen displays read-only profile summary and stores profile/package hash in run dataset.
  - tampered profile emits `studio_local_package_deployment_profile_hash_mismatch` and Korean message: `배포 프로필 해시가 맞지 않습니다...`.
- Added route repair:
  - initial `?tab=publish` now opens `#screen-publish` instead of falling back to browse. This preserves G2's URL compatibility claim and is used by the G3 tamper workflow.
- Added pack/checker/browser runner:
  - `pack/seamgrim_deployment_profile_v0_v1`
  - `tests/seamgrim_deployment_profile_v0_runner.mjs`
  - `tests/run_seamgrim_deployment_profile_v0_check.py`
- PASS: `python tests/run_seamgrim_deployment_profile_v0_check.py`
- PASS: `python tests/run_seamgrim_publish_screen_isolation_check.py`
- PASS: `python tests/run_seamgrim_wave2a_product_ia_check.py`
- PASS: `python tests/run_pack_golden.py seamgrim_deployment_profile_v0_v1 seamgrim_publish_screen_isolation_v1 seamgrim_wave2a_product_ia_v1`
- PASS: `node --check solutions/seamgrim_ui_mvp/ui/app.js`
- PASS: `node --check solutions/seamgrim_ui_mvp/ui/studio_local_share_package.js`
- PASS: `node --check solutions/seamgrim_ui_mvp/ui/screens/browse.js`
- PASS: `node --check solutions/seamgrim_ui_mvp/ui/screens/run.js`
- PASS: `node --check tests/seamgrim_deployment_profile_v0_runner.mjs`

## G4 한국어 Manim 측정 부품 가족

- Added five measurement component families on the existing `seamgrim.view_plan.v1` path without new DDN syntax:
  - angle measure: existing `obs.theta` arc/baseline/current/label.
  - length measure: deterministic pivot-to-bob length line/ticks/label.
  - vector arrow: tangent velocity arrow from bob, using `obs.speed` and `obs.angular_velocity`.
  - axes/ticks: deterministic x/y axes and fixed tick step.
  - trajectory trail: deterministic bob arc polyline from current pendulum state.
- Added run-screen product controls:
  - `lesson-angle-measure-toggle`
  - `lesson-length-measure-toggle`
  - `lesson-vector-measure-toggle`
  - `lesson-axes-measure-toggle`
  - `lesson-trail-measure-toggle`
- Runtime/report boundary:
  - each component emits unit, semantic label, object ids, accessibility name, and `state_hash_participation: false`.
  - `view_plan_hash` and `world_draw_payload_hash_candidate` remain view/artifact candidates only.
  - `state_hash` formula is unchanged and world state does not store view objects.
- Added pack/checker/browser runner:
  - `pack/seamgrim_measurement_components_v1`
  - `tests/seamgrim_measurement_components_runner.mjs`
  - `tests/run_seamgrim_measurement_components_check.py`
- PASS: `python tests/run_seamgrim_measurement_components_check.py`
- PASS: `python tests/run_seamgrim_pendulum_view_plan_product_check.py`
- PASS: `python tests/run_pack_golden.py seamgrim_measurement_components_v1 seamgrim_pendulum_view_plan_product_v1`
- PASS: `node --check solutions/seamgrim_ui_mvp/ui/view_plan_runtime.js`
- PASS: `node --check solutions/seamgrim_ui_mvp/ui/screens/run.js`
- PASS: `node --check tests/seamgrim_measurement_components_runner.mjs`

## G5 카메라·반응 연출 저작 UI

- Added product authoring panel inside `만들기 > 수업 구성`:
  - camera policies: `fixed`, `fit`, `follow`
  - measurement components: `angle`, `length`, `vector`, `axes`, `trail`
  - semantic anchors: `obs.theta`, `obs.angular_velocity`, `obs.speed`, `obs.pivot`, `obs.bob`, `obs.time`
  - condition kinds: `zero_crossing`, `sign_change`, `extremum`, `tolerance_entry`
  - reaction actions: `highlight`, `visibility`, `camera_focus`
  - explicit numeric `priority`
- Added deterministic UI artifact:
  - schema: `seamgrim.view_reaction_authoring.v1`
  - `artifact_hash`: `candidate:fnv1a32:view_reaction_authoring:*`
  - `implicit_lww_allowed: false`
  - `state_hash_participation: false`
  - `live_online_reaction_claim: false`
  - `sealed_trace_replay_scope: true`
- Added conflict guard:
  - same semantic anchor + same target property + same priority emits `E_VIEW_AUTHOR_REACTION_CONFLICT`.
  - no implicit last-write-wins resolution is applied.
- Added pack/checker/browser runner:
  - `pack/seamgrim_view_reaction_authoring_v1`
  - `tests/seamgrim_view_reaction_authoring_runner.mjs`
  - `tests/run_seamgrim_view_reaction_authoring_check.py`
- PASS: `python tests/run_seamgrim_view_reaction_authoring_check.py`
- PASS: `node tests/seamgrim_view_reaction_authoring_runner.mjs`
- PASS: `python tests/run_pack_golden.py seamgrim_view_reaction_authoring_v1`
- PASS: `node --check solutions/seamgrim_ui_mvp/ui/screens/editor.js`
- PASS: `node --check tests/seamgrim_view_reaction_authoring_runner.mjs`
- PASS: `python -m py_compile tests/run_seamgrim_view_reaction_authoring_check.py`

## G6 수업계획/view_plan 통합 왕복

- Extended product `lesson_plan.v0` parser/serializer activity fields:
  - `scene_ref`
  - `primary_view`
  - `camera_policy`
  - `measurement_components`
  - `reaction_rule_refs`
  - `view_authoring_hash`
  - `view_plan_ref`
- Connected G5 authoring artifact to the selected lesson activity:
  - camera policy copies from the authoring artifact.
  - selected measurement components copy from the authoring artifact.
  - reaction rule ids copy from the authoring artifact.
  - `view_authoring_hash` links to `seamgrim.view_reaction_authoring.v1`.
  - default `view_plan_ref` is `view_plan.v1`.
- Preserved code/structure workflow:
  - structure fields update the canonical TOML.
  - code apply reparses TOML and keeps structure fields identical.
  - byte-stable and semantic-stable roundtrip uses product `lesson_plan_v0.js`.
- Explicit non-preserved/transient items are only documented in the pack contract:
  - selected activity index
  - panel expanded state
  - diagnostics HTML text
  - temporary control focus
- Added pack/checker/browser runner:
  - `pack/seamgrim_lesson_view_plan_roundtrip_v1`
  - `tests/seamgrim_lesson_view_plan_roundtrip_runner.mjs`
  - `tests/run_seamgrim_lesson_view_plan_roundtrip_check.py`
- PASS: `python tests/run_seamgrim_lesson_view_plan_roundtrip_check.py`
- PASS: `python tests/run_pack_golden.py seamgrim_lesson_view_plan_roundtrip_v1 lesson_plan_roundtrip_v1`
- PASS: `node --check solutions/seamgrim_ui_mvp/ui/lesson_plan_v0.js`
- PASS: `node --check solutions/seamgrim_ui_mvp/ui/screens/editor.js`
- PASS: `node --check tests/seamgrim_lesson_view_plan_roundtrip_runner.mjs`
- PASS: `python -m py_compile tests/run_seamgrim_lesson_view_plan_roundtrip_check.py`

## G7 대표 세계 3종 수직 검증

- Added/verified representative world verticals:
  - `rep_phys_pendulum_wave1_v1`: angle/length/vector/trail roles, follow camera, extremum reaction rule ref.
  - `rep_phys_projectile_xy_v1`: trajectory trail, velocity vector, fit camera.
  - `rep_math_function_line_v1`: graph series, axes/ticks, graph point, slope measure, graph primary view.
- Product view additions:
  - Run screen exposes `window.__SEAMGRIM_MAIN_VISUAL__` for current rendered main visual instrumentation.
  - Projectile static `space2d.json` now declares view roles and view-only trajectory/vector shapes.
  - Observation fallback view decoration adds projectile `vector_arrow`/`fit_camera` roles and linear `axis_ticks`/`graph_point`/`slope_measure` roles.
- Browser workflow evidence:
  - each world opens by first-delight route and canonical lesson id.
  - DDN source token is accessible in `#run-ddn-preview`.
  - WASM state hash appears through the run mirror.
  - canvas is nonblank.
  - source can be reopened through direct DDN route and re-run.
  - representative lesson composition with three activities roundtrips through product `lesson_plan_v0.js`.
- Added pack/checker/browser runner:
  - `pack/seamgrim_wave2b_representative_worlds_v1`
  - `tests/seamgrim_wave2b_representative_worlds_runner.mjs`
  - `tests/run_seamgrim_wave2b_representative_worlds_check.py`
- PASS: `node tests/seamgrim_wave2b_representative_worlds_runner.mjs`
- PASS: `python tests/run_seamgrim_wave2b_representative_worlds_check.py`
- PASS via checker: `python tests/run_seamgrim_pendulum_view_plan_product_check.py`
- PASS via checker: `python tests/run_seamgrim_first_delight_projectile_check.py`
- PASS via checker: `python tests/run_seamgrim_current_line_three_worlds_check.py`
- PASS via checker: `python tests/run_pack_golden.py seamgrim_wave2b_representative_worlds_v1`
- PASS: `node --check solutions/seamgrim_ui_mvp/ui/screens/run.js`
- PASS: `node --check tests/seamgrim_wave2b_representative_worlds_runner.mjs`
- PASS: `python -m py_compile tests/run_seamgrim_wave2b_representative_worlds_check.py`
- PASS: `python -m py_compile tests/run_seamgrim_measurement_components_check.py`

## G8 제품 품질 관문

- Added `seamgrim_wave2b_quality_gate_v1` as the Wave 2B final quality gate pack.
- Added product browser runner coverage:
  - viewports: `1440x900`, `1280x720`, `1024x768`, `390x844`.
  - nonblank main canvas and sufficient visible canvas height.
  - DDN source access, including mobile DDN toggle.
  - no horizontal overflow at tested viewports.
  - icon button tooltip/accessibility names for reset/run/step.
  - keyboard activation for primary run controls.
- Product fixes made for the quality gate:
  - tablet first-delight canvas keeps a stable visible height.
  - mobile DDN toggle can reveal the DDN source panel after canvas validation.
  - run/pause/reset/step buttons support Enter/Space activation.
- The resolved-scene trace stability check is delegated to the existing sealed trace/reaction checker; this does not claim a new general hook runtime.
- Added quality wrapper:
  - `tests/seamgrim_wave2b_quality_gate_runner.mjs`
  - `tests/run_seamgrim_wave2b_quality_gate_check.py`
- PASS: `node --check tests/seamgrim_wave2b_quality_gate_runner.mjs`
- PASS: `node tests/seamgrim_wave2b_quality_gate_runner.mjs`
- PASS: `python tests/run_seamgrim_ui_v2_product_shell_check.py`
- PASS: `python tests/run_seamgrim_primary_view_contract_check.py`
- PASS: `python tests/run_seamgrim_lab_e1_minimal_check.py`
- PASS: `python tests/run_seamgrim_pendulum_view_plan_product_check.py`
- PASS: `python tests/run_seamgrim_sealed_trace_reaction_check.py`
- PASS: `python tests/run_seamgrim_wave2a_product_ia_check.py`
- PASS: `python tests/run_seamgrim_live_trace_reaction_check.py`
- PASS: `python tests/run_seamgrim_offline_live_reaction_parity_check.py`
- PASS: `python tests/run_seamgrim_semantic_cursor_check.py`
- PASS: `python tests/run_lesson_plan_roundtrip_v1_check.py`
- PASS: `python tests/run_seamgrim_responsive_lesson_workflow_check.py`
- PASS: `python tests/run_seamgrim_deployment_profile_v0_check.py`
- PASS: `python tests/run_seamgrim_measurement_components_check.py`
- PASS: `python tests/run_seamgrim_view_reaction_authoring_check.py`
- PASS: `python tests/run_seamgrim_lesson_view_plan_roundtrip_check.py`
- PASS: `python tests/run_seamgrim_wave2b_representative_worlds_check.py`
- PASS: `python tests/run_pack_golden.py seamgrim_deployment_profile_v0_v1 seamgrim_measurement_components_v1 seamgrim_view_reaction_authoring_v1 seamgrim_lesson_view_plan_roundtrip_v1 seamgrim_wave2b_representative_worlds_v1 seamgrim_wave2b_quality_gate_v1`
- PASS: `cargo check`
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- PASS: `python tests/run_ci_sanity_gate.py --profile core_lang`
- PASS: `git diff --check`
- PASS: `git status --short -- docs/ssot`

## 질문 큐

- None.

## 커밋 목록

- `96bd108 test(seamgrim): stabilize wave2b baseline runner`
- `486db72 test(seamgrim): retire runtime role switch evidence`
- `cdf6441 feat(seamgrim): isolate publish product screen`
- `6e81b83 feat(seamgrim): add deployment profile workflow`
- `41c3280 feat(seamgrim): author measurement view components`
- `90d1759 feat(seamgrim): author camera and scene reactions`
- `56c8d74 feat(seamgrim): roundtrip lesson and view plans`
- `a90d69a test(seamgrim): close wave2b representative worlds`
- `ad7a10f chore(seamgrim): record wave2b quality gate`
- `5015759 docs(seamgrim): record wave2b verification`
