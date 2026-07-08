# BRIEF: 통합후보 조치 실행 — 삭제 32건 + 보류 해제 2건

작성: 2026-07-08 KST
승인 근거: `docs/context/reports/CONSOLIDATION_ACTION_REVIEW_V1.md`(34행 심사표, 사용자 승인 완료), Claude 독립 재검증(표본 5건 실존/무참조 확인 완료)

## 배경

`CONSOLIDATION_ACTION_REVIEW_V1.md`의 34행(삭제 심사 32 + 보류 해제 검토 2)에 대해 사용자 승인이 났다. 이번 브리프는 그 실제 집행이다 — 새 판단 없음, 표에 이미 적힌 조치를 정확히 그대로 실행한다.

## 트랙 H1 — 파일 삭제 32건

### Outcome

- `CONSOLIDATION_ACTION_REVIEW_V1.md`의 `#1`~`#32`행(제안 액션 = "삭제 심사 대상") 각각의 "파일 경로" 열에 있는 32개 경로를 `git rm`으로 삭제한다.
- **삭제 직전 재검증(각 파일마다)**: (a) 파일이 여전히 존재하는지, (b) 저장소 전체(`tests/`, `tools/`, `solutions/`, `pack/`, `docs/`, CI 설정 파일 등, `docs/context/reports/` 제외)에서 파일명이 여전히 무참조 상태인지 다시 grep한다. 심사표 작성 이후 시간이 지났으므로 재확인은 생략하지 않는다.
- 재검증에서 참조가 새로 발견되거나 파일이 이미 없는 경우, 그 파일은 삭제하지 않고 "제외" 목록에 사유와 함께 남긴다 — 억지로 32개를 다 채우려 하지 않는다.
- 32개 경로 전부 `tests/*.mjs` 파일이다(다른 디렉터리 경로가 섞여 있지 않은지 실행 전에 한 번 확인한다).

### Verification

- 삭제 후 `git status`로 정확히 삭제된 파일 수를 확인하고 로그에 남긴다(재검증에서 제외된 게 있으면 32보다 적을 수 있다 — 그건 정상이다).
- 삭제 후 관련 테스트 스위트가 있다면(`tests/` 아래 Node/Playwright 러너를 부르는 상위 러너가 있는지 확인) 그 상위 러너 실행 결과가 삭제 전과 동일한지 확인한다. 없다면 "상위 러너 없음, 고아 파일 확인됨"이라고 기록한다.
- `cargo test --manifest-path tools/teul-cli/Cargo.toml` PASS 유지 확인(회귀 없음 — 원래 Rust 테스트와 무관하지만 사이드 이펙트 없음을 확인하는 차원).
- `python tests/run_ci_sanity_gate.py --profile core_lang` PASS 유지 확인.

## 트랙 H2 — 보류 해제 반영 2건

### Outcome

- 대상: `pack/lang_settings_header_closure_v1`, `pack/seamgrim_curriculum_batch_smoke_v1`.
- `docs/context/reports/CONSOLIDATION_ACTION_REVIEW_V1.md`의 `#33`, `#34`행 "제안 액션" 열을 "보류 해제/승격 검토"에서 "보류 해제 반영 완료(2026-07-08)"로 갱신한다.
- 실측 결과, 이 두 pack의 "보류" 상태는 문서상 분류일 뿐 어떤 러너/CI 설정에도 기계적 skip 처리로 연결되어 있지 않다(확인됨: `tests/_run_pack_golden_impl.py` 등에 이 두 pack ID에 대한 skip 로직 없음). 따라서 코드/설정 변경은 필요 없고, 문서 갱신만 한다.
- `docs/context/reports/CONSOLIDATION_CANDIDATE_DRAFT_V1.md`는 원본 스냅샷이므로 수정하지 않는다 — 대신 그 파일의 해당 2행 바로 아래에 각주 한 줄만 추가한다: "2026-07-08 재검증 결과 PASS로 보류 해제됨 — 상세: `CONSOLIDATION_ACTION_REVIEW_V1.md` #33/#34." 원본 표 내용/처분 값 자체는 손대지 않는다.

### Verification

- 두 pack을 각각 `python tests/run_pack_golden.py <pack_이름>` 재실행하고 PASS 확인, 실행 로그를 남긴다.
- 각주가 정확히 2곳(해당 행 바로 아래)에만 추가됐는지, 원본 표의 다른 행/값이 전혀 바뀌지 않았는지 `git diff`로 확인한다.

## 공통 경계 (절대 준수)

1. 위 34행 표에 없는 파일은 삭제하지 않는다.
2. 재검증에서 의심스러우면(참조 발견, 파일 부재 등) 삭제하지 말고 "제외"로 기록 — 억지로 진행하지 않는다.
3. `docs/ssot/**` 수정 금지.
4. `docs/context/reports/CONSOLIDATION_CANDIDATE_DRAFT_V1.md`의 기존 표 내용/값 변경 금지 — 각주 추가만 허용.
5. `golden.jsonl`/`contract.detjson` 정정 금지(H2는 문서 각주만, pack 파일 자체는 건드리지 않는다).
6. `main` 직접 커밋 금지 — `codex/queue-20260706`에만 커밋한다. 삭제(H1)와 보류해제(H2)는 각각 별도 커밋으로 남긴다(리뷰 편의).
7. push 금지, 네트워크 금지.

## 실행 로그

(트랙 완료 시 `[CAE-H1]`/`[CAE-H2]` 태그로 기록, 삭제/제외 목록과 검증 결과 포함)

### [CAE-H1] 파일 삭제 실행 로그 — 2026-07-09 KST

- 실행 브랜치: `codex/queue-20260706`.
- 삭제 직전 재검증:
  - 전체 대상: 32개, 모두 `tests/*.mjs` 확인.
  - 재검증 산출물:
    - `I:/home/urihanl/ddn/codex/build/consolidation_action_execute_v1/h1_predelete_reverify.detjson`
    - `I:/home/urihanl/ddn/codex/build/consolidation_action_execute_v1/h1_predelete_reverify.tsv`
  - 기준: 파일 존재 확인 + `docs/context/reports/**`, `target/**`, `build/**`, `out/**`, `.git/**`, 자기 자신 제외 후 파일명 정적 검색.
- `git rm` 삭제 18개:
  - `tests/seamgrim_editor_selection_runner.mjs`
  - `tests/seamgrim_formula_sugar_runner.mjs`
  - `tests/seamgrim_input_registry_runner.mjs`
  - `tests/seamgrim_inspector_contract_runner.mjs`
  - `tests/seamgrim_legacy_warning_guide_runner.mjs`
  - `tests/seamgrim_play_output_contract_runner.mjs`
  - `tests/seamgrim_play_source_contract_runner.mjs`
  - `tests/seamgrim_preview_component_runner.mjs`
  - `tests/seamgrim_preview_payload_loader_runner.mjs`
  - `tests/seamgrim_preview_result_contract_runner.mjs`
  - `tests/seamgrim_preview_session_runner.mjs`
  - `tests/seamgrim_preview_view_model_runner.mjs`
  - `tests/seamgrim_range_split_runner.mjs`
  - `tests/seamgrim_runtime_view_stack_runner.mjs`
  - `tests/seamgrim_scene_summary_runner.mjs`
  - `tests/seamgrim_update_tick_runner.mjs`
  - `tests/seamgrim_view_dock_time_runner.mjs`
  - `tests/seamgrim_wasm_loader_diag_runner.mjs`
- 제외 14개:
  - `tests/education_assessment_pack_runner.mjs` — `pack/education_curriculum_2_v1/contract.detjson` 참조 발견.
  - `tests/education_classroom_ui_pack_runner.mjs` — `pack/education_curriculum_3_v1/contract.detjson` 참조 발견.
  - `tests/education_operations_lts_runner.mjs` — `pack/education_curriculum_5_v1/README.md`, `pack/education_curriculum_5_v1/contract.detjson` 참조 발견.
  - `tests/education_publication_pack_runner.mjs` — `pack/education_curriculum_4_v1/contract.detjson` 참조 발견.
  - `tests/rpg_box_authoring_ui_runner.mjs` — `pack/malhim_rpg_3_v1/README.md`, `pack/malhim_rpg_3_v1/contract.detjson` 참조 발견.
  - `tests/rpg_engine_adapter_lts_runner.mjs` — `pack/malhim_rpg_5_v1/README.md`, `pack/malhim_rpg_5_v1/contract.detjson` 참조 발견.
  - `tests/rpg_story_package_runner.mjs` — `pack/malhim_rpg_4_v1/README.md`, `pack/malhim_rpg_4_v1/contract.detjson` 참조 발견.
  - `tests/studio_classroom_mode_switch_runner.mjs` — `pack/studio_classroom_mode_switch_v1/contract.detjson` 참조 발견.
  - `tests/studio_classroom_report_export_action_runner.mjs` — `pack/studio_classroom_report_export_action_v1/contract.detjson` 참조 발견.
  - `tests/studio_diagnostic_fixit_editor_apply_runner.mjs` — `pack/studio_diagnostic_fixit_editor_apply_v1/contract.detjson` 참조 발견.
  - `tests/ttonimaru_platform_hardening_runner.mjs` — `pack/ttonimaru_registry_5_v1/README.md`, `pack/ttonimaru_registry_5_v1/contract.detjson` 참조 발견.
  - `tests/ttonimaru_project_share_ui_runner.mjs` — `pack/ttonimaru_registry_3_v1/README.md`, `pack/ttonimaru_registry_3_v1/contract.detjson` 참조 발견.
  - `tests/ttonimaru_public_registry_seed_runner.mjs` — `pack/ttonimaru_registry_4_v1/README.md`, `pack/ttonimaru_registry_4_v1/contract.detjson` 참조 발견.
  - `tests/ttonimaru_publication_read_api_runner.mjs` — `pack/ttonimaru_registry_2_v1/README.md`, `pack/ttonimaru_registry_2_v1/contract.detjson` 참조 발견.
- 삭제 후 상태:
  - `git diff --name-only --cached --diff-filter=D -- tests/*.mjs` = 18개.
  - 관련 상위 러너: 삭제 18개는 재검증 검색에서 참조 0건이라 상위 러너 없음, 고아 파일 확인됨.
- 검증:
  - `cargo test --manifest-path tools/teul-cli/Cargo.toml` PASS (`1109 passed; 0 failed`).
  - `python tests/run_ci_sanity_gate.py --profile core_lang` PASS (`ci_sanity_status=pass code=OK step=all profile=core_lang`).
  - `git status --short -- docs/ssot` 출력 없음.
  - `git status --short -- lang core tool tools/teul-cli/src` 출력 없음.
  - sanity 실행 중 `pack/open_bundle_artifact/run_bundle/geoul.diag.jsonl`, `pack/open_end_to_end/open.log.jsonl`가 일시 갱신됐으나 이번 산출물이 아니므로 diff가 없도록 복구.

### [CAE-H2] 보류 해제 반영 로그 — 2026-07-09 KST

- 실행 브랜치: `codex/queue-20260706`.
- 대상:
  - `pack/lang_settings_header_closure_v1`
  - `pack/seamgrim_curriculum_batch_smoke_v1`
- 재검증:
  - `python tests/run_pack_golden.py lang_settings_header_closure_v1` PASS. 로그: `I:/home/urihanl/ddn/codex/build/consolidation_action_execute_v1/h2_lang_settings_header_closure_v1.log`.
  - `python tests/run_pack_golden.py seamgrim_curriculum_batch_smoke_v1` PASS. 로그: `I:/home/urihanl/ddn/codex/build/consolidation_action_execute_v1/h2_seamgrim_curriculum_batch_smoke_v1.log`.
  - `tests/_run_pack_golden_impl.py`의 `seamgrim_curriculum_batch_smoke_v1` 언급은 특수러너 pack 목록 등록이며 skip 로직이 아님.
  - `lang_settings_header_closure_v1`은 `tests/run_lang_settings_header_closure_pack_check.py` 참조만 확인됨.
- 문서 반영:
  - `docs/context/reports/CONSOLIDATION_ACTION_REVIEW_V1.md` #33/#34의 제안 액션을 `보류 해제 반영 완료(2026-07-08)`로 갱신.
  - `docs/context/reports/CONSOLIDATION_CANDIDATE_DRAFT_V1.md`는 원본 표 행/값을 유지하고 해당 두 행 바로 아래에 각주 2줄만 추가.
- 검증:
  - `Select-String ... '각주: 2026-07-08 재검증 결과 PASS로 보류 해제됨'` = 2.
  - `git diff -- docs/context/reports/CONSOLIDATION_ACTION_REVIEW_V1.md docs/context/reports/CONSOLIDATION_CANDIDATE_DRAFT_V1.md` 확인: review #33/#34 액션 값 변경 2건 + draft 각주 추가 2건만 포함.
  - `golden.jsonl`/`contract.detjson` 변경 없음.
