# Q27_DELETION_REAUDIT_V2_EXECUTION_BASED_20260709

- 작성: 2026-07-09 KST, Codex
- 대상 삭제 커밋: `2e6a956 [Q27] 죽은 체크 삭제`
- 기준 소스: `git show 2e6a956^:<path>`
- 판정 기준: 코드 추적을 쓰지 않고, 복원한 체크 스크립트의 실제 실행 결과만 사용했다.
- 실행 방식: 삭제 직전 소스를 `work/_tmp_q27_reaudit_v2/<파일명>`에 복원한 뒤, 상대경로 호환을 위해 같은 내용을 `tests/__tmp_q27_reaudit_v2_<번호>_<파일명>`로 임시 복사해 `python`으로 실행하고 즉시 제거했다.
- 임시 디렉터리/파일 제거: `work/_tmp_q27_reaudit_v2` 제거 완료, `tests/__tmp_q27_reaudit_v2_*.py` 잔여 0건.

## 요약

- 전체 실행 행 수: 111
- 실행 결과: PASS 1 / FAIL 110 / 실행불가 0
- 최종분류: 정말죽음 110 / 실수삭제 1 / 실행불가 0
- V1 대비: 일치 27 / 불일치 84
- 전환: `실수삭제->실수삭제` 1, `실수삭제->정말죽음` 84, `정말죽음->정말죽음` 26
- 브리프 지목 15건: 15/15 정말죽음으로 정정 확인.

## 실행불가

- 0건.

## V1 대비 불일치

| 파일명 | V1 | V2 실행결과 | V2 최종분류 | FAIL 이유 excerpt |
|---|---|---|---|---|
| `tests/run_constraint_solve_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | constraint_solve_rebase_check: FAIL: missing required path: CONSTRAINT_SOLVE_REBASE_V1.md |
| `tests/run_lang_blocked_ssot_track_parking_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | lang_blocked_ssot_track_parking_rebase_check: FAIL: missing required path: LANG_BLOCKED_SSOT_TRACK_PARKING_REBASE_V1.md |
| `tests/run_lang_flow_history_ssot_acceptance_request_check.py` | `실수삭제` | `FAIL` | `정말죽음` | lang_flow_history_ssot_acceptance_request_check: FAIL: missing required path: LANG_FLOW_HISTORY_SSOT_ACCEPTANCE_REQUEST_V1.md |
| `tests/run_lang_non_ssot_track_resume_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | lang_non_ssot_track_resume_rebase_check: FAIL: missing required path: LANG_NON_SSOT_TRACK_RESUME_REBASE_V1.md |
| `tests/run_lang_pack_checker_stability_sweep_check.py` | `실수삭제` | `FAIL` | `정말죽음` | lang_pack_checker_stability_sweep_check: FAIL: missing required path: LANG_PACK_CHECKER_STABILITY_SWEEP_V1.md |
| `tests/run_lang_post_ssot_landing_product_gate_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | lang_post_ssot_landing_product_gate_rebase_check: FAIL: missing required path: LANG_POST_SSOT_LANDING_PRODUCT_GATE_REBASE_V1.md |
| `tests/run_lang_prime_ssot_acceptance_request_check.py` | `실수삭제` | `FAIL` | `정말죽음` | lang_prime_ssot_acceptance_request_check: FAIL: missing required path: LANG_PRIME_SSOT_ACCEPTANCE_REQUEST_V1.md |
| `tests/run_lang_product_path_transition_closure_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | lang_product_path_transition_closure_rebase_check: FAIL: missing required path: LANG_PRODUCT_PATH_TRANSITION_CLOSURE_REBASE_V1.md |
| `tests/run_lang_ssot_acceptance_request_closure_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | lang_ssot_acceptance_request_closure_rebase_check: FAIL: missing required path: LANG_SSOT_ACCEPTANCE_REQUEST_CLOSURE_REBASE_V1.md |
| `tests/run_lang_ssot_landing_coordination_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | lang_ssot_landing_coordination_rebase_check: FAIL: missing required path: LANG_SSOT_LANDING_COORDINATION_REBASE_V1.md |
| `tests/run_lang_ssot_landing_wait_state_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | lang_ssot_landing_wait_state_rebase_check: FAIL: missing required path: LANG_SSOT_LANDING_WAIT_STATE_REBASE_V1.md |
| `tests/run_lang_ssot_owner_landing_audit_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | lang_ssot_owner_landing_audit_rebase_check: FAIL: missing required path: LANG_SSOT_OWNER_LANDING_AUDIT_REBASE_V1.md |
| `tests/run_lang_ssot_owner_landing_handoff_check.py` | `실수삭제` | `FAIL` | `정말죽음` | lang_ssot_owner_landing_handoff_check: FAIL: missing required path: LANG_SSOT_OWNER_LANDING_HANDOFF_V1.md |
| `tests/run_lang_tuck_ssot_acceptance_handoff_check.py` | `실수삭제` | `FAIL` | `정말죽음` | lang_tuck_ssot_acceptance_handoff_check: FAIL: missing required path: LANG_TUCK_SSOT_ACCEPTANCE_HANDOFF_V1.md |
| `tests/run_lang_tuck_ssot_acceptance_request_check.py` | `실수삭제` | `FAIL` | `정말죽음` | lang_tuck_ssot_acceptance_request_check: FAIL: missing required path: LANG_TUCK_SSOT_ACCEPTANCE_REQUEST_V1.md |
| `tests/run_roadmap_v2_ba0_free_lab_seed_reassessment_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-ba0-free-lab-seed-reassessment] FAIL: missing file: BA0_FREE_LAB_SEED_REASSESSMENT_V1.md |
| `tests/run_roadmap_v2_ba0_free_lab_seed_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-ba0-free-lab-seed] FAIL: missing file: BA0_FREE_LAB_SEED_REBASE_V1.md |
| `tests/run_roadmap_v2_cha0_rpg_seed_reassessment_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-cha0-rpg-seed-reassessment] FAIL: missing file: CHA0_RPG_SEED_REASSESSMENT_V1.md |
| `tests/run_roadmap_v2_cha0_rpg_seed_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-cha0-rpg-seed] FAIL: missing file: CHA0_RPG_SEED_REBASE_V1.md |
| `tests/run_roadmap_v2_cha1_rpg_phrase_action_smoke_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-cha1-rpg-phrase-action] FAIL: missing file: CHA1_RPG_PHRASE_ACTION_SMOKE_V1.md |
| `tests/run_roadmap_v2_cha2_rpg_story_pack_closure_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-cha2-rpg-story-pack] FAIL: missing file: CHA2_RPG_STORY_PACK_CLOSURE_V1.md |
| `tests/run_roadmap_v2_cha3_rpg_box_authoring_ui_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-cha3-rpg-box-authoring-ui] FAIL: missing file: CHA3_RPG_BOX_NURIMAKER_AUTHORING_UI_V1.md |
| `tests/run_roadmap_v2_cha4_rpg_story_package_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-cha4-rpg-story-package] FAIL: missing file: CHA4_RPG_STORY_PACKAGE_V1.md |
| `tests/run_roadmap_v2_cha5_rpg_engine_adapter_lts_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-cha5-rpg-engine-adapter-lts] FAIL: missing file: CHA5_RPG_ENGINE_ADAPTER_LTS_V1.md |
| `tests/run_roadmap_v2_da1_math_first_run_frontier_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-da1-math-first-run-frontier-rebase] FAIL: missing file: ROADMAP_V2_DA1_MATH_FIRST_RUN_FRONTIER_REBASE_V1.md |
| `tests/run_roadmap_v2_da2_symbolic_solve_proof_frontier_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-da2-symbolic-solve-proof-frontier-rebase] FAIL: missing file: ROADMAP_V2_DA2_SYMBOLIC_SOLVE_PROOF_FRONTIER_REBASE_V1.md |
| `tests/run_roadmap_v2_da3_seamgrim_math_view_frontier_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-da3-seamgrim-math-view-frontier-rebase] FAIL: missing file: ROADMAP_V2_DA3_SEAMGRIM_MATH_VIEW_FRONTIER_REBASE_V1.md |
| `tests/run_roadmap_v2_da4_math_package_share_frontier_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-da4-math-package-share-frontier-rebase] FAIL: missing file: ROADMAP_V2_DA4_MATH_PACKAGE_SHARE_FRONTIER_REBASE_V1.md |
| `tests/run_roadmap_v2_da5_math_lts_frontier_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-da5-math-lts-frontier-rebase] FAIL: missing file: ROADMAP_V2_DA5_MATH_LTS_FRONTIER_REBASE_V1.md |
| `tests/run_roadmap_v2_ga0_current_line_ledger_matrix_reconciliation_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-ga0-reconciliation] FAIL: missing file: ROADMAP_V2_GA0_CURRENT_LINE_LEDGER_MATRIX_RECONCILIATION_V1.md |
| `tests/run_roadmap_v2_ga1_core_smoke_matrix_reconciliation_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-ga1-reconciliation] FAIL: missing file: ROADMAP_V2_GA1_CORE_SMOKE_MATRIX_RECONCILIATION_V1.md |
| `tests/run_roadmap_v2_ga2_matrix_status_reconciliation_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-ga2-reconciliation] FAIL: missing file: GA2_MATRIX_STATUS_RECONCILIATION_V1.md |
| `tests/run_roadmap_v2_ga5_release_gate_blocker_audit.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-ga5-release-gate-blocker-audit] FAIL: missing file: GA5_RELEASE_GATE_BLOCKER_AUDIT_V1.md |
| `tests/run_roadmap_v2_geo0_ai_question_card_seed_reconciliation_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-geo0-question-card-reconciliation] FAIL: missing file: GEO0_AI_QUESTION_CARD_SEED_RECONCILIATION_V1.md |
| `tests/run_roadmap_v2_geo1_question_card_smoke_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-geo1-question-card-smoke] FAIL: missing file: GEO1_QUESTION_CARD_SMOKE_V1.md |
| `tests/run_roadmap_v2_geo2_ai_output_validation_pack_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-geo2-ai-output-validation] FAIL: missing file: GEO2_AI_OUTPUT_VALIDATION_PACK_V1.md |
| `tests/run_roadmap_v2_geo3_dev_assist_ui_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-geo3-dev-assist-ui] FAIL: missing file: GEO3_DEV_ASSIST_UI_V1.md |
| `tests/run_roadmap_v2_geo4_author_tool_share_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-geo4-author-tool-share] FAIL: missing file: GEO4_AUTHOR_TOOL_SHARE_V1.md |
| `tests/run_roadmap_v2_geo5_ai_workflow_hardening_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-geo5-ai-workflow-hardening] FAIL: missing file: GEO5_AI_WORKFLOW_HARDENING_V1.md |
| `tests/run_roadmap_v2_ha3_classroom_ui_pack_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-ha3-education-classroom-ui-pack] FAIL: command failed: C:\\Users\\ddongosu\\AppData\\Local\\Programs\\Python\\Python313\\python.exe tests/run_roadmap_v2_ha2_education_assessment_pack_check.py / C:\\Users\\ddongosu\\AppData\\Local\\Programs\\Python\\Python313\\pyt… |
| `tests/run_roadmap_v2_ha4_public_course_publication_pack_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-ha4-public-course-publication-pack] FAIL: solutions\\seamgrim_ui_mvp\\ui\\styles.css missing ['.education-publication-pack', '.education-publication-artifacts', '.education-publication-preview'] |
| `tests/run_roadmap_v2_ha5_education_operations_lts_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-ha5-education-operations-lts] FAIL: solutions\\seamgrim_ui_mvp\\ui\\styles.css missing ['.education-operations-lts', '.education-operations-artifacts', '.education-operations-preview'] |
| `tests/run_roadmap_v2_ka0_platform_charter_matrix_reconciliation_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-ka0-reconciliation] FAIL: missing file: ROADMAP_V2_KA0_PLATFORM_CHARTER_MATRIX_RECONCILIATION_V1.md |
| `tests/run_roadmap_v2_ka1_server_mvp_matrix_reconciliation_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-ka1-reconciliation] FAIL: missing file: ROADMAP_V2_KA1_SERVER_MVP_MATRIX_RECONCILIATION_V1.md |
| `tests/run_roadmap_v2_ka2_publication_read_api_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-ka2-publication-read-api] FAIL: missing file: KA2_PUBLICATION_READ_API_CLOSURE_V1.md |
| `tests/run_roadmap_v2_ka3_project_share_ui_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-ka3-project-share-ui] FAIL: missing file: KA3_PROJECT_SHARE_UI_V1.md |
| `tests/run_roadmap_v2_ka4_public_registry_seed_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-ka4-public-registry-seed] FAIL: missing file: KA4_PUBLIC_REGISTRY_SEED_V1.md |
| `tests/run_roadmap_v2_ka5_platform_hardening_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-ka5-platform-hardening] FAIL: missing file: KA5_PLATFORM_HARDENING_V1.md |
| `tests/run_roadmap_v2_la2_matrix_status_reconciliation_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-la2-reconciliation] FAIL: missing file: LA2_MATRIX_STATUS_RECONCILIATION_V1.md |
| `tests/run_roadmap_v2_ma2_seamgrim_curriculum_2_pack_closure_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-ma2-curriculum-2-closure] FAIL: missing file: MA2_SEAMGRIM_CURRICULUM_2_PACK_CLOSURE_V1.md |
| `tests/run_roadmap_v2_ma2_studio_prereq_unlock_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-ma2-prereq-unlock] FAIL: missing file: MA2_STUDIO_PREREQ_UNLOCK_V1.md |
| `tests/run_roadmap_v2_ma3_seamgrim_curriculum_3_classroom_ui_pack_closure_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-ma3-classroom-ui-closure] FAIL: missing file: MA3_SEAMGRIM_CURRICULUM_3_CLASSROOM_UI_PACK_CLOSURE_V1.md |
| `tests/run_roadmap_v2_ma3_studio_classroom_workbench_prereq_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-ma3-prereq-rebase] FAIL: missing file: MA3_STUDIO_CLASSROOM_WORKBENCH_PREREQ_REBASE_V1.md |
| `tests/run_roadmap_v2_ma4_public_lesson_publication_prereq_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-ma4-prereq-rebase] FAIL: missing file: MA4_PUBLIC_LESSON_PUBLICATION_PREREQ_REBASE_V1.md |
| `tests/run_roadmap_v2_ma4_seamgrim_curriculum_4_publication_pack_closure_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-ma4-publication-closure] FAIL: missing file: MA4_SEAMGRIM_CURRICULUM_4_PUBLICATION_PACK_CLOSURE_V1.md |
| `tests/run_roadmap_v2_ma5_curriculum_lts_prereq_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-ma5-prereq-rebase] FAIL: missing file: MA5_CURRICULUM_LTS_PREREQ_REBASE_V1.md |
| `tests/run_roadmap_v2_ma5_seamgrim_curriculum_5_lts_pack_closure_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-ma5-lts-closure] FAIL: missing file: MA5_SEAMGRIM_CURRICULUM_5_LTS_PACK_CLOSURE_V1.md |
| `tests/run_roadmap_v2_na3_matrix_status_reconciliation_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-na3-reconciliation] FAIL: missing file: ROADMAP_V2_NA3_MATRIX_STATUS_RECONCILIATION_V1.md |
| `tests/run_roadmap_v2_na3_resource_network_policy_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-na3-rebase] FAIL: missing file: ROADMAP_V2_NA3_RESOURCE_NETWORK_POLICY_REBASE_V1.md |
| `tests/run_roadmap_v2_pa2_social_bridge_pack_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-pa2-social-bridge-pack] FAIL: missing file: PA2_SOCIAL_BRIDGE_PACK_V1.md |
| `tests/run_roadmap_v2_pa3_policy_ghost_ui_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-pa3-policy-ghost-ui] FAIL: missing file: PA3_POLICY_GHOST_UI_V1.md |
| `tests/run_roadmap_v2_pa4_social_template_registry_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-pa4-social-template-registry] FAIL: missing file: PA4_SOCIAL_TEMPLATE_REGISTRY_V1.md |
| `tests/run_roadmap_v2_pa5_social_world_lts_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-pa5-social-world-lts] FAIL: missing file: PA5_SOCIAL_WORLD_LTS_V1.md |
| `tests/run_roadmap_v2_post_da5_frontier_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-post-da5-frontier-rebase] FAIL: missing file: ROADMAP_V2_POST_DA5_FRONTIER_REBASE_V1.md |
| `tests/run_roadmap_v2_post_ga0_frontier_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-post-ga0-frontier-rebase] FAIL: missing file: ROADMAP_V2_POST_GA0_FRONTIER_REBASE_V1.md |
| `tests/run_roadmap_v2_post_ga1_frontier_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-post-ga1-frontier-rebase] FAIL: missing file: ROADMAP_V2_POST_GA1_FRONTIER_REBASE_V1.md |
| `tests/run_roadmap_v2_post_ka0_frontier_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-post-ka0-frontier-rebase] FAIL: missing file: ROADMAP_V2_POST_KA0_FRONTIER_REBASE_V1.md |
| `tests/run_roadmap_v2_post_ka1_frontier_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-post-ka1-frontier-rebase] FAIL: missing file: ROADMAP_V2_POST_KA1_FRONTIER_REBASE_V1.md |
| `tests/run_roadmap_v2_post_la2_frontier_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-post-la2-frontier-rebase] FAIL: missing file: ROADMAP_V2_POST_LA2_FRONTIER_REBASE_V1.md |
| `tests/run_roadmap_v2_post_na3_frontier_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-post-na3-frontier-rebase] FAIL: missing file: ROADMAP_V2_POST_NA3_FRONTIER_REBASE_V1.md |
| `tests/run_roadmap_v2_post_ta0_frontier_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-post-ta0-frontier-rebase] FAIL: missing file: ROADMAP_V2_POST_TA0_FRONTIER_REBASE_V1.md |
| `tests/run_roadmap_v2_post_ta1_frontier_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-post-ta1-frontier-rebase] FAIL: missing file: ROADMAP_V2_POST_TA1_FRONTIER_REBASE_V1.md |
| `tests/run_roadmap_v2_post_ta2_frontier_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-post-ta2-frontier-rebase] FAIL: missing file: ROADMAP_V2_POST_TA2_FRONTIER_REBASE_V1.md |
| `tests/run_roadmap_v2_ta0_pack_checker_skeleton_matrix_reconciliation_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-ta0-reconciliation] FAIL: missing file: ROADMAP_V2_TA0_PACK_CHECKER_SKELETON_MATRIX_RECONCILIATION_V1.md |
| `tests/run_roadmap_v2_ta1_pack_runner_basis_matrix_reconciliation_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-ta1-reconciliation] FAIL: missing file: ROADMAP_V2_TA1_PACK_RUNNER_BASIS_MATRIX_RECONCILIATION_V1.md |
| `tests/run_roadmap_v2_ta2_guide_status_reconciliation_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [roadmap-v2-ta2-guide-reconciliation] FAIL: missing file: ROADMAP_V2_TA2_GUIDE_STATUS_RECONCILIATION_V1.md |
| `tests/run_seamgrim_baseline_stabilization_closure_rebase_check.py` | `실수삭제` | `FAIL` | `정말죽음` | seamgrim_baseline_stabilization_closure_rebase_check: FAIL: missing required path: SEAMGRIM_BASELINE_STABILIZATION_CLOSURE_REBASE_V1.md |
| `tests/run_seamgrim_cli_warning_parity_repair_check.py` | `실수삭제` | `FAIL` | `정말죽음` | seamgrim_cli_warning_parity_repair_check: FAIL: missing required path: SEAMGRIM_CLI_WARNING_PARITY_REPAIR_V1.md |
| `tests/run_seamgrim_runtime_5min_baseline_repair_check.py` | `실수삭제` | `FAIL` | `정말죽음` | seamgrim_runtime_5min_baseline_repair_check: FAIL: missing required path: SEAMGRIM_RUNTIME_5MIN_BASELINE_REPAIR_V1.md |
| `tests/run_seamgrim_wasm_tool_golden_baseline_repair_check.py` | `실수삭제` | `FAIL` | `정말죽음` | seamgrim_wasm_tool_golden_baseline_repair_check: FAIL: missing required path: SEAMGRIM_WASM_TOOL_GOLDEN_BASELINE_REPAIR_V1.md |
| `tests/run_std_resource_network_policy_minimum_check.py` | `실수삭제` | `FAIL` | `정말죽음` | [std-resource-network-policy-minimum] FAIL: missing file: STD_RESOURCE_NETWORK_POLICY_MINIMUM_V1.md |
| `tests/run_studio_classroom_mode_switch_check.py` | `실수삭제` | `FAIL` | `정말죽음` | studio_classroom_mode_switch_check: FAIL: missing required path: STUDIO_CLASSROOM_MODE_SWITCH_V1.md |
| `tests/run_studio_classroom_report_export_action_check.py` | `실수삭제` | `FAIL` | `정말죽음` | studio_classroom_report_export_action_check: FAIL: missing required path: STUDIO_CLASSROOM_REPORT_EXPORT_ACTION_V1.md |
| `tests/run_studio_diagnostic_fixit_editor_apply_check.py` | `실수삭제` | `FAIL` | `정말죽음` | studio_diagnostic_fixit_editor_apply_check: FAIL: missing required path: STUDIO_DIAGNOSTIC_FIXIT_EDITOR_APPLY_V1.md |

## 111건 실행 기반 감사표

| 파일명 | 실행결과(PASS/FAIL/실행불가) | FAIL 이유 excerpt | 최종분류 | V1 분류 일치여부 |
|---|---:|---|---|---|
| `tests/run_age5_ci_frontier_recheck.py` | FAIL | E_AGE5_CI_FRONTIER_RECHECK_MISSING: ['AGE5_CI_FRONTIER_RECHECK_V1.md', 'NEXT_WORK_QUEUE_AFTER_CONNECT_V1.md', 'CONNECT_ENDPOINT_SOLVE_RANGE_CASE_SUITE_CHECK_RUNNER_V1V.md', 'STD_EVENT_MINIMUM_CLOSURE_V1.md'] | `정말죽음` | 일치 |
| `tests/run_block_editor_roundtrip_expected_refresh_check.py` | FAIL | E_BLOCK_EDITOR_ROUNDTRIP_REFRESH_MISSING: ['BLOCK_EDITOR_ROUNDTRIP_EXPECTED_REFRESH_V1.md', 'ROADMAP_V2_LA2_SUBSET_ROUNDTRIP_REBASE_V1.md', 'NEXT_WORK_QUEUE_AFTER_CONNECT_V1.md'] | `정말죽음` | 일치 |
| `tests/run_constraint_solve_rebase_check.py` | FAIL | constraint_solve_rebase_check: FAIL: missing required path: CONSTRAINT_SOLVE_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_lang_blocked_ssot_track_parking_rebase_check.py` | FAIL | lang_blocked_ssot_track_parking_rebase_check: FAIL: missing required path: LANG_BLOCKED_SSOT_TRACK_PARKING_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_lang_flow_history_ssot_acceptance_request_check.py` | FAIL | lang_flow_history_ssot_acceptance_request_check: FAIL: missing required path: LANG_FLOW_HISTORY_SSOT_ACCEPTANCE_REQUEST_V1.md | `정말죽음` | 불일치 |
| `tests/run_lang_non_ssot_track_resume_rebase_check.py` | FAIL | lang_non_ssot_track_resume_rebase_check: FAIL: missing required path: LANG_NON_SSOT_TRACK_RESUME_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_lang_pack_checker_stability_sweep_check.py` | FAIL | lang_pack_checker_stability_sweep_check: FAIL: missing required path: LANG_PACK_CHECKER_STABILITY_SWEEP_V1.md | `정말죽음` | 불일치 |
| `tests/run_lang_post_ssot_landing_product_gate_rebase_check.py` | FAIL | lang_post_ssot_landing_product_gate_rebase_check: FAIL: missing required path: LANG_POST_SSOT_LANDING_PRODUCT_GATE_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_lang_prime_ssot_acceptance_request_check.py` | FAIL | lang_prime_ssot_acceptance_request_check: FAIL: missing required path: LANG_PRIME_SSOT_ACCEPTANCE_REQUEST_V1.md | `정말죽음` | 불일치 |
| `tests/run_lang_product_path_transition_closure_rebase_check.py` | FAIL | lang_product_path_transition_closure_rebase_check: FAIL: missing required path: LANG_PRODUCT_PATH_TRANSITION_CLOSURE_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_lang_ssot_acceptance_request_closure_rebase_check.py` | FAIL | lang_ssot_acceptance_request_closure_rebase_check: FAIL: missing required path: LANG_SSOT_ACCEPTANCE_REQUEST_CLOSURE_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_lang_ssot_landing_coordination_rebase_check.py` | FAIL | lang_ssot_landing_coordination_rebase_check: FAIL: missing required path: LANG_SSOT_LANDING_COORDINATION_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_lang_ssot_landing_wait_state_rebase_check.py` | FAIL | lang_ssot_landing_wait_state_rebase_check: FAIL: missing required path: LANG_SSOT_LANDING_WAIT_STATE_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_lang_ssot_owner_landing_audit_rebase_check.py` | FAIL | lang_ssot_owner_landing_audit_rebase_check: FAIL: missing required path: LANG_SSOT_OWNER_LANDING_AUDIT_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_lang_ssot_owner_landing_handoff_check.py` | FAIL | lang_ssot_owner_landing_handoff_check: FAIL: missing required path: LANG_SSOT_OWNER_LANDING_HANDOFF_V1.md | `정말죽음` | 불일치 |
| `tests/run_lang_tuck_ssot_acceptance_handoff_check.py` | FAIL | lang_tuck_ssot_acceptance_handoff_check: FAIL: missing required path: LANG_TUCK_SSOT_ACCEPTANCE_HANDOFF_V1.md | `정말죽음` | 불일치 |
| `tests/run_lang_tuck_ssot_acceptance_request_check.py` | FAIL | lang_tuck_ssot_acceptance_request_check: FAIL: missing required path: LANG_TUCK_SSOT_ACCEPTANCE_REQUEST_V1.md | `정말죽음` | 불일치 |
| `tests/run_math_calculus_computed_output_refresh_check.py` | FAIL | E_MATH_CALCULUS_COMPUTED_REFRESH_MISSING: ['MATH_CALCULUS_COMPUTED_OUTPUT_REFRESH_V1.md', 'ROADMAP_V2_DA1_MATH_REBASE_V1.md', 'NEXT_WORK_QUEUE_AFTER_CONNECT_V1.md'] | `정말죽음` | 일치 |
| `tests/run_math_vector_minimum_first_run_check.py` | FAIL | E_MATH_VECTOR_MINIMUM_FIRST_RUN_MISSING: ['MATH_VECTOR_MINIMUM_FIRST_RUN_V1.md', 'ROADMAP_V2_DA1_MATH_CLOSURE_V1.md', 'NEXT_WORK_QUEUE_AFTER_CONNECT_V1.md'] | `정말죽음` | 일치 |
| `tests/run_numeric_solver_capability_rebase_check.py` | FAIL | E_NUMERIC_SOLVER_REBASE_MISSING: ['NUMERIC_SOLVER_LONG_HORIZON_ROADMAP_V1.md', 'NUMERIC_SOLVER_CAPABILITY_REBASE_V1.md'] | `정말죽음` | 일치 |
| `tests/run_ode_method_comparison_check.py` | FAIL | E_ODE_METHOD_COMPARISON_MISSING: ['ODE_METHOD_COMPARISON_V1.md', 'ODE_TICK_LOOP_LESSON_BASELINE_V1.md', 'NUMERIC_SOLVER_LONG_HORIZON_ROADMAP_V1.md', 'tests\\\\run_ode_tick_loop_lesson_baseline_check.py'] | `정말죽음` | 일치 |
| `tests/run_ode_tick_loop_lesson_baseline_check.py` | FAIL | E_ODE_TICK_LOOP_BASELINE_MISSING: ['ODE_TICK_LOOP_LESSON_BASELINE_V1.md', 'NUMERIC_SOLVER_CAPABILITY_REBASE_V1.md', 'NUMERIC_SOLVER_LONG_HORIZON_ROADMAP_V1.md'] | `정말죽음` | 일치 |
| `tests/run_roadmap_v2_ba0_free_lab_seed_reassessment_check.py` | FAIL | [roadmap-v2-ba0-free-lab-seed-reassessment] FAIL: missing file: BA0_FREE_LAB_SEED_REASSESSMENT_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_ba0_free_lab_seed_rebase_check.py` | FAIL | [roadmap-v2-ba0-free-lab-seed] FAIL: missing file: BA0_FREE_LAB_SEED_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_cha0_rpg_seed_reassessment_check.py` | FAIL | [roadmap-v2-cha0-rpg-seed-reassessment] FAIL: missing file: CHA0_RPG_SEED_REASSESSMENT_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_cha0_rpg_seed_rebase_check.py` | FAIL | [roadmap-v2-cha0-rpg-seed] FAIL: missing file: CHA0_RPG_SEED_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_cha1_rpg_phrase_action_smoke_check.py` | FAIL | [roadmap-v2-cha1-rpg-phrase-action] FAIL: missing file: CHA1_RPG_PHRASE_ACTION_SMOKE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_cha2_rpg_story_pack_closure_check.py` | FAIL | [roadmap-v2-cha2-rpg-story-pack] FAIL: missing file: CHA2_RPG_STORY_PACK_CLOSURE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_cha3_rpg_box_authoring_ui_check.py` | FAIL | [roadmap-v2-cha3-rpg-box-authoring-ui] FAIL: missing file: CHA3_RPG_BOX_NURIMAKER_AUTHORING_UI_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_cha4_rpg_story_package_check.py` | FAIL | [roadmap-v2-cha4-rpg-story-package] FAIL: missing file: CHA4_RPG_STORY_PACKAGE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_cha5_rpg_engine_adapter_lts_check.py` | FAIL | [roadmap-v2-cha5-rpg-engine-adapter-lts] FAIL: missing file: CHA5_RPG_ENGINE_ADAPTER_LTS_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_da1_final_closure_check.py` | FAIL | E_ROADMAP_V2_DA1_FINAL_CLOSURE_MISSING: ['ROADMAP_V2_DA1_FINAL_CLOSURE_V1.md', 'ROADMAP_V2_DA1_MATH_CLOSURE_V1.md', 'MATH_VECTOR_MINIMUM_FIRST_RUN_V1.md', 'NEXT_WORK_QUEUE_AFTER_CONNECT_V1.md'] | `정말죽음` | 일치 |
| `tests/run_roadmap_v2_da1_math_closure_check.py` | FAIL | E_ROADMAP_V2_DA1_MATH_CLOSURE_MISSING: ['ROADMAP_V2_DA1_MATH_CLOSURE_V1.md', 'ROADMAP_V2_DA1_MATH_REBASE_V1.md', 'MATH_CALCULUS_COMPUTED_OUTPUT_REFRESH_V1.md', 'MATH_VECTOR_MINIMUM_FIRST_RUN_V1.md', 'NEXT_WORK_QUEUE_AFTER_CONNECT_V1.md'] | `정말죽음` | 일치 |
| `tests/run_roadmap_v2_da1_math_first_run_frontier_rebase_check.py` | FAIL | [roadmap-v2-da1-math-first-run-frontier-rebase] FAIL: missing file: ROADMAP_V2_DA1_MATH_FIRST_RUN_FRONTIER_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_da1_math_rebase_check.py` | FAIL | E_ROADMAP_V2_DA1_MATH_REBASE_MISSING: ['ROADMAP_V2_DA1_MATH_REBASE_V1.md', 'NEXT_WORK_QUEUE_AFTER_CONNECT_V1.md', 'ROADMAP_V2_FOLLOWON_REBASE_V1.md', 'MATH_CALCULUS_COMPUTED_OUTPUT_REFRESH_V1.md'] | `정말죽음` | 일치 |
| `tests/run_roadmap_v2_da2_symbolic_solve_proof_frontier_rebase_check.py` | FAIL | [roadmap-v2-da2-symbolic-solve-proof-frontier-rebase] FAIL: missing file: ROADMAP_V2_DA2_SYMBOLIC_SOLVE_PROOF_FRONTIER_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_da3_seamgrim_math_view_frontier_rebase_check.py` | FAIL | [roadmap-v2-da3-seamgrim-math-view-frontier-rebase] FAIL: missing file: ROADMAP_V2_DA3_SEAMGRIM_MATH_VIEW_FRONTIER_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_da4_math_package_share_frontier_rebase_check.py` | FAIL | [roadmap-v2-da4-math-package-share-frontier-rebase] FAIL: missing file: ROADMAP_V2_DA4_MATH_PACKAGE_SHARE_FRONTIER_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_da5_math_lts_frontier_rebase_check.py` | FAIL | [roadmap-v2-da5-math-lts-frontier-rebase] FAIL: missing file: ROADMAP_V2_DA5_MATH_LTS_FRONTIER_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_followon_rebase_check.py` | FAIL | E_ROADMAP_V2_FOLLOWON_REBASE_MISSING: ['ROADMAP_V2_FOLLOWON_REBASE_V1.md', 'NEXT_WORK_QUEUE_AFTER_CONNECT_V1.md', 'AGE5_CI_FRONTIER_RECHECK_V1.md', 'ROADMAP_V2_SA1_REBASE_V1.md', 'ROADMAP_V2_NA2_UNIT_RANDOM_EVENT_REBASE_V1.md', 'STD_EVENT_MINIMUM_CLOSURE_V1.m… | `정말죽음` | 일치 |
| `tests/run_roadmap_v2_ga0_current_line_ledger_matrix_reconciliation_check.py` | FAIL | [roadmap-v2-ga0-reconciliation] FAIL: missing file: ROADMAP_V2_GA0_CURRENT_LINE_LEDGER_MATRIX_RECONCILIATION_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_ga1_core_smoke_matrix_reconciliation_check.py` | FAIL | [roadmap-v2-ga1-reconciliation] FAIL: missing file: ROADMAP_V2_GA1_CORE_SMOKE_MATRIX_RECONCILIATION_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_ga2_matrix_status_reconciliation_check.py` | FAIL | [roadmap-v2-ga2-reconciliation] FAIL: missing file: GA2_MATRIX_STATUS_RECONCILIATION_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_ga5_release_gate_blocker_audit.py` | FAIL | [roadmap-v2-ga5-release-gate-blocker-audit] FAIL: missing file: GA5_RELEASE_GATE_BLOCKER_AUDIT_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_geo0_ai_question_card_seed_reconciliation_check.py` | FAIL | [roadmap-v2-geo0-question-card-reconciliation] FAIL: missing file: GEO0_AI_QUESTION_CARD_SEED_RECONCILIATION_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_geo1_question_card_smoke_check.py` | FAIL | [roadmap-v2-geo1-question-card-smoke] FAIL: missing file: GEO1_QUESTION_CARD_SMOKE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_geo2_ai_output_validation_pack_check.py` | FAIL | [roadmap-v2-geo2-ai-output-validation] FAIL: missing file: GEO2_AI_OUTPUT_VALIDATION_PACK_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_geo3_dev_assist_ui_check.py` | FAIL | [roadmap-v2-geo3-dev-assist-ui] FAIL: missing file: GEO3_DEV_ASSIST_UI_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_geo4_author_tool_share_check.py` | FAIL | [roadmap-v2-geo4-author-tool-share] FAIL: missing file: GEO4_AUTHOR_TOOL_SHARE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_geo5_ai_workflow_hardening_check.py` | FAIL | [roadmap-v2-geo5-ai-workflow-hardening] FAIL: missing file: GEO5_AI_WORKFLOW_HARDENING_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_ha2_education_assessment_pack_check.py` | PASS |  | `실수삭제` | 일치 |
| `tests/run_roadmap_v2_ha3_classroom_ui_pack_check.py` | FAIL | [roadmap-v2-ha3-education-classroom-ui-pack] FAIL: command failed: C:\\Users\\ddongosu\\AppData\\Local\\Programs\\Python\\Python313\\python.exe tests/run_roadmap_v2_ha2_education_assessment_pack_check.py / C:\\Users\\ddongosu\\AppData\\Local\\Programs\\Python\\Python313\\pyt… | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_ha4_public_course_publication_pack_check.py` | FAIL | [roadmap-v2-ha4-public-course-publication-pack] FAIL: solutions\\seamgrim_ui_mvp\\ui\\styles.css missing ['.education-publication-pack', '.education-publication-artifacts', '.education-publication-preview'] | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_ha5_education_operations_lts_check.py` | FAIL | [roadmap-v2-ha5-education-operations-lts] FAIL: solutions\\seamgrim_ui_mvp\\ui\\styles.css missing ['.education-operations-lts', '.education-operations-artifacts', '.education-operations-preview'] | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_ka0_platform_charter_matrix_reconciliation_check.py` | FAIL | [roadmap-v2-ka0-reconciliation] FAIL: missing file: ROADMAP_V2_KA0_PLATFORM_CHARTER_MATRIX_RECONCILIATION_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_ka1_server_mvp_matrix_reconciliation_check.py` | FAIL | [roadmap-v2-ka1-reconciliation] FAIL: missing file: ROADMAP_V2_KA1_SERVER_MVP_MATRIX_RECONCILIATION_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_ka2_publication_read_api_check.py` | FAIL | [roadmap-v2-ka2-publication-read-api] FAIL: missing file: KA2_PUBLICATION_READ_API_CLOSURE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_ka3_project_share_ui_check.py` | FAIL | [roadmap-v2-ka3-project-share-ui] FAIL: missing file: KA3_PROJECT_SHARE_UI_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_ka4_public_registry_seed_check.py` | FAIL | [roadmap-v2-ka4-public-registry-seed] FAIL: missing file: KA4_PUBLIC_REGISTRY_SEED_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_ka5_platform_hardening_check.py` | FAIL | [roadmap-v2-ka5-platform-hardening] FAIL: missing file: KA5_PLATFORM_HARDENING_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_la2_final_closure_check.py` | FAIL | E_ROADMAP_V2_LA2_FINAL_MISSING: ['ROADMAP_V2_LA2_FINAL_CLOSURE_V1.md', 'SEAMGRIM_MALBLOCK_ROUNDTRIP_SUBSET_V1.md', 'BLOCK_EDITOR_ROUNDTRIP_EXPECTED_REFRESH_V1.md', 'NEXT_WORK_QUEUE_AFTER_CONNECT_V1.md'] | `정말죽음` | 일치 |
| `tests/run_roadmap_v2_la2_matrix_status_reconciliation_check.py` | FAIL | [roadmap-v2-la2-reconciliation] FAIL: missing file: LA2_MATRIX_STATUS_RECONCILIATION_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_la2_subset_roundtrip_rebase_check.py` | FAIL | E_ROADMAP_V2_LA2_REBASE_MISSING: ['ROADMAP_V2_LA2_SUBSET_ROUNDTRIP_REBASE_V1.md', 'ROADMAP_V2_GA2_FINAL_CLOSURE_V1.md', 'LANG_CORE_2_REPRESENTATIVE_GRAMMAR_PACK_V1.md', 'NEXT_WORK_QUEUE_AFTER_CONNECT_V1.md'] | `정말죽음` | 일치 |
| `tests/run_roadmap_v2_ma2_seamgrim_curriculum_2_pack_closure_check.py` | FAIL | [roadmap-v2-ma2-curriculum-2-closure] FAIL: missing file: MA2_SEAMGRIM_CURRICULUM_2_PACK_CLOSURE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_ma2_studio_prereq_unlock_check.py` | FAIL | [roadmap-v2-ma2-prereq-unlock] FAIL: missing file: MA2_STUDIO_PREREQ_UNLOCK_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_ma3_seamgrim_curriculum_3_classroom_ui_pack_closure_check.py` | FAIL | [roadmap-v2-ma3-classroom-ui-closure] FAIL: missing file: MA3_SEAMGRIM_CURRICULUM_3_CLASSROOM_UI_PACK_CLOSURE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_ma3_studio_classroom_workbench_prereq_rebase_check.py` | FAIL | [roadmap-v2-ma3-prereq-rebase] FAIL: missing file: MA3_STUDIO_CLASSROOM_WORKBENCH_PREREQ_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_ma4_public_lesson_publication_prereq_rebase_check.py` | FAIL | [roadmap-v2-ma4-prereq-rebase] FAIL: missing file: MA4_PUBLIC_LESSON_PUBLICATION_PREREQ_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_ma4_seamgrim_curriculum_4_publication_pack_closure_check.py` | FAIL | [roadmap-v2-ma4-publication-closure] FAIL: missing file: MA4_SEAMGRIM_CURRICULUM_4_PUBLICATION_PACK_CLOSURE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_ma5_curriculum_lts_prereq_rebase_check.py` | FAIL | [roadmap-v2-ma5-prereq-rebase] FAIL: missing file: MA5_CURRICULUM_LTS_PREREQ_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_ma5_seamgrim_curriculum_5_lts_pack_closure_check.py` | FAIL | [roadmap-v2-ma5-lts-closure] FAIL: missing file: MA5_SEAMGRIM_CURRICULUM_5_LTS_PACK_CLOSURE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_na3_matrix_status_reconciliation_check.py` | FAIL | [roadmap-v2-na3-reconciliation] FAIL: missing file: ROADMAP_V2_NA3_MATRIX_STATUS_RECONCILIATION_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_na3_resource_network_policy_rebase_check.py` | FAIL | [roadmap-v2-na3-rebase] FAIL: missing file: ROADMAP_V2_NA3_RESOURCE_NETWORK_POLICY_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_pa2_social_bridge_pack_check.py` | FAIL | [roadmap-v2-pa2-social-bridge-pack] FAIL: missing file: PA2_SOCIAL_BRIDGE_PACK_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_pa3_policy_ghost_ui_check.py` | FAIL | [roadmap-v2-pa3-policy-ghost-ui] FAIL: missing file: PA3_POLICY_GHOST_UI_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_pa4_social_template_registry_check.py` | FAIL | [roadmap-v2-pa4-social-template-registry] FAIL: missing file: PA4_SOCIAL_TEMPLATE_REGISTRY_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_pa5_social_world_lts_check.py` | FAIL | [roadmap-v2-pa5-social-world-lts] FAIL: missing file: PA5_SOCIAL_WORLD_LTS_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_post_da5_frontier_rebase_check.py` | FAIL | [roadmap-v2-post-da5-frontier-rebase] FAIL: missing file: ROADMAP_V2_POST_DA5_FRONTIER_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_post_ga0_frontier_rebase_check.py` | FAIL | [roadmap-v2-post-ga0-frontier-rebase] FAIL: missing file: ROADMAP_V2_POST_GA0_FRONTIER_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_post_ga1_frontier_rebase_check.py` | FAIL | [roadmap-v2-post-ga1-frontier-rebase] FAIL: missing file: ROADMAP_V2_POST_GA1_FRONTIER_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_post_ka0_frontier_rebase_check.py` | FAIL | [roadmap-v2-post-ka0-frontier-rebase] FAIL: missing file: ROADMAP_V2_POST_KA0_FRONTIER_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_post_ka1_frontier_rebase_check.py` | FAIL | [roadmap-v2-post-ka1-frontier-rebase] FAIL: missing file: ROADMAP_V2_POST_KA1_FRONTIER_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_post_la2_frontier_rebase_check.py` | FAIL | [roadmap-v2-post-la2-frontier-rebase] FAIL: missing file: ROADMAP_V2_POST_LA2_FRONTIER_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_post_na3_frontier_rebase_check.py` | FAIL | [roadmap-v2-post-na3-frontier-rebase] FAIL: missing file: ROADMAP_V2_POST_NA3_FRONTIER_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_post_priority_rebase_check.py` | FAIL | E_ROADMAP_V2_POST_PRIORITY_REBASE_MISSING: ['ROADMAP_V2_POST_PRIORITY_REBASE_V1.md', 'ROADMAP_V2_DA1_FINAL_CLOSURE_V1.md', 'ROADMAP_V2_GA2_REPRESENTATIVE_GRAMMAR_REBASE_V1.md', 'NEXT_WORK_QUEUE_AFTER_CONNECT_V1.md'] | `정말죽음` | 일치 |
| `tests/run_roadmap_v2_post_ta0_frontier_rebase_check.py` | FAIL | [roadmap-v2-post-ta0-frontier-rebase] FAIL: missing file: ROADMAP_V2_POST_TA0_FRONTIER_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_post_ta1_frontier_rebase_check.py` | FAIL | [roadmap-v2-post-ta1-frontier-rebase] FAIL: missing file: ROADMAP_V2_POST_TA1_FRONTIER_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_post_ta2_frontier_rebase_check.py` | FAIL | [roadmap-v2-post-ta2-frontier-rebase] FAIL: missing file: ROADMAP_V2_POST_TA2_FRONTIER_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_ta0_pack_checker_skeleton_matrix_reconciliation_check.py` | FAIL | [roadmap-v2-ta0-reconciliation] FAIL: missing file: ROADMAP_V2_TA0_PACK_CHECKER_SKELETON_MATRIX_RECONCILIATION_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_ta1_pack_runner_basis_matrix_reconciliation_check.py` | FAIL | [roadmap-v2-ta1-reconciliation] FAIL: missing file: ROADMAP_V2_TA1_PACK_RUNNER_BASIS_MATRIX_RECONCILIATION_V1.md | `정말죽음` | 불일치 |
| `tests/run_roadmap_v2_ta2_guide_status_reconciliation_check.py` | FAIL | [roadmap-v2-ta2-guide-reconciliation] FAIL: missing file: ROADMAP_V2_TA2_GUIDE_STATUS_RECONCILIATION_V1.md | `정말죽음` | 불일치 |
| `tests/run_seamgrim_baseline_stabilization_closure_rebase_check.py` | FAIL | seamgrim_baseline_stabilization_closure_rebase_check: FAIL: missing required path: SEAMGRIM_BASELINE_STABILIZATION_CLOSURE_REBASE_V1.md | `정말죽음` | 불일치 |
| `tests/run_seamgrim_cli_warning_parity_repair_check.py` | FAIL | seamgrim_cli_warning_parity_repair_check: FAIL: missing required path: SEAMGRIM_CLI_WARNING_PARITY_REPAIR_V1.md | `정말죽음` | 불일치 |
| `tests/run_seamgrim_malblock_roundtrip_subset_queue_guard_repair_check.py` | FAIL | [seamgrim-malblock-roundtrip-subset-queue-guard-repair] FAIL: missing file: SEAMGRIM_MALBLOCK_ROUNDTRIP_SUBSET_QUEUE_GUARD_REPAIR_V1.md | `정말죽음` | 일치 |
| `tests/run_seamgrim_private_productization_consolidation_audit.py` | FAIL | seamgrim_private_productization_consolidation_audit: FAIL: missing required paths: ['SEAMGRIM_PRIVATE_PRODUCTIZATION_CONSOLIDATION_AUDIT_V1.md'] | `정말죽음` | 일치 |
| `tests/run_seamgrim_private_productization_next_queue_recheck.py` | FAIL | seamgrim_private_productization_next_queue_recheck: FAIL: missing required paths: ['SEAMGRIM_PRIVATE_PRODUCTIZATION_NEXT_QUEUE_RECHECK_V1.md', 'SEAMGRIM_WORKBENCH_POLISH_V2.md', 'SEAMGRIM_LESSON_LIBRARY_CURATION_V1.md', 'SEAMGRIM_LESSON_RUN_PRESET_RAIL_V1.md'… | `정말죽음` | 일치 |
| `tests/run_seamgrim_run_history_export_summary_followup_recheck.py` | FAIL | seamgrim_run_history_export_summary_followup_recheck: FAIL: missing required paths: ['SEAMGRIM_RUN_HISTORY_EXPORT_SUMMARY_FOLLOWUP_RECHECK_V1.md', 'SEAMGRIM_RUN_HISTORY_EXPORT_SUMMARY_V1.md'] | `정말죽음` | 일치 |
| `tests/run_seamgrim_runtime_5min_baseline_repair_check.py` | FAIL | seamgrim_runtime_5min_baseline_repair_check: FAIL: missing required path: SEAMGRIM_RUNTIME_5MIN_BASELINE_REPAIR_V1.md | `정말죽음` | 불일치 |
| `tests/run_seamgrim_wasm_tool_golden_baseline_repair_check.py` | FAIL | seamgrim_wasm_tool_golden_baseline_repair_check: FAIL: missing required path: SEAMGRIM_WASM_TOOL_GOLDEN_BASELINE_REPAIR_V1.md | `정말죽음` | 불일치 |
| `tests/run_std_resource_network_policy_minimum_check.py` | FAIL | [std-resource-network-policy-minimum] FAIL: missing file: STD_RESOURCE_NETWORK_POLICY_MINIMUM_V1.md | `정말죽음` | 불일치 |
| `tests/run_studio_classroom_mode_switch_check.py` | FAIL | studio_classroom_mode_switch_check: FAIL: missing required path: STUDIO_CLASSROOM_MODE_SWITCH_V1.md | `정말죽음` | 불일치 |
| `tests/run_studio_classroom_report_export_action_check.py` | FAIL | studio_classroom_report_export_action_check: FAIL: missing required path: STUDIO_CLASSROOM_REPORT_EXPORT_ACTION_V1.md | `정말죽음` | 불일치 |
| `tests/run_studio_diagnostic_fixit_editor_apply_check.py` | FAIL | studio_diagnostic_fixit_editor_apply_check: FAIL: missing required path: STUDIO_DIAGNOSTIC_FIXIT_EDITOR_APPLY_V1.md | `정말죽음` | 불일치 |
| `tests/run_studio_historical_progress_ledger_reconciliation_check.py` | FAIL | studio_historical_progress_ledger_reconciliation_check: FAIL: missing required paths: ['STUDIO_HISTORICAL_PROGRESS_LEDGER_RECONCILIATION_V1.md'] | `정말죽음` | 일치 |
| `tests/run_studio_long_horizon_completion_audit_check.py` | FAIL | studio_long_horizon_completion_audit_check: FAIL: missing required paths: ['STUDIO_LONG_HORIZON_COMPLETION_AUDIT_V1.md'] | `정말죽음` | 일치 |
| `tests/run_studio_long_horizon_next_jit_reconciliation_check.py` | FAIL | studio_long_horizon_next_jit_reconciliation_check: FAIL: missing required paths: ['STUDIO_LONG_HORIZON_NEXT_JIT_RECONCILIATION_V1.md'] | `정말죽음` | 일치 |
| `tests/run_studio_progress_claim_boundary_audit_check.py` | FAIL | studio_progress_claim_boundary_audit_check: FAIL: missing required paths: ['STUDIO_PROGRESS_CLAIM_BOUNDARY_AUDIT_V1.md'] | `정말죽음` | 일치 |
| `tests/run_studio_public_release_execution_check.py` | FAIL | studio_public_release_execution: FAIL: missing required paths: ['I:\\\\dev\\\\ddonilang\\\\codex\\\\STUDIO_PUBLIC_RELEASE_EXECUTION_V1.md'] | `정말죽음` | 일치 |
| `tests/run_studio_public_release_external_publish_handoff_check.py` | FAIL | studio_public_release_external_publish_handoff: FAIL: missing required paths: ['I:\\\\dev\\\\ddonilang\\\\codex\\\\STUDIO_PUBLIC_RELEASE_EXTERNAL_PUBLISH_HANDOFF_V1.md'] | `정말죽음` | 일치 |
| `tests/run_studio_release_approval_gate_status_recheck.py` | FAIL | studio_release_approval_gate_status_recheck: FAIL: missing required paths: ['STUDIO_RELEASE_APPROVAL_GATE_STATUS_RECHECK_V1.md', 'SEAMGRIM_PRIVATE_PRODUCTIZATION_CONSOLIDATION_AUDIT_V1.md'] | `정말죽음` | 일치 |
| `tests/run_studio_safe_continuation_queue_recheck.py` | FAIL | studio_safe_continuation_queue_recheck: FAIL: missing required paths: ['STUDIO_SAFE_CONTINUATION_QUEUE_RECHECK_V1.md'] | `정말죽음` | 일치 |

## 검증

- 111행 전부 실행결과 기록: 111 == 111.
- 실행불가: 0건.
- 임시 작업 디렉터리 제거: True.
- tests 임시 사본 잔여: 0건.
- `docs/ssot/**` 수정 없음.
- 삭제된 체크 파일은 저장소에 되살리지 않음.
