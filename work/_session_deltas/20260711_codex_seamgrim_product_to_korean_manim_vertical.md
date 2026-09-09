# 2026-07-11 Codex Session Delta - Seamgrim Product to Korean Manim Vertical

## 결과 요약

- Stage A PASS: 기존 W1~W6/셈그림 기준선과 dirty 상태를 확인하고, `docs/ssot/**` 변경 없이 제품 경로만 사용했다.
- Stage B PASS: `배우기/실험실/만들기/배포` L0/L1 제품 셸, 데스크톱 DDN 22% 내외, 모바일 DDN 토글, runtime 역할 토글 숨김을 browser runner로 고정했다. 후속 감사에서 `수업 열기`와 `실험실에서 바꾸기`가 같은 경로였던 결함을 고쳐 각각 배우기/실험실 공간을 유지한다.
- Stage C PASS: 일차함수/포물선/수요공급세금 3대표 세계에 primary view 계약과 human observation payload를 제품 화면에 연결했다.
- Stage D PASS: 실험실 E1에서 조절값 변경, 재실행, `origin_hash`/`delta_ref` lineage, auto apply/file write false를 browser runner로 검증했다.
- Stage E/F/G PASS: 진자 lesson, explicit `view_plan.v1`, 의미 닻, 각도재기, same-tick graph cursor, fixed/fit/follow camera 정책을 제품 보개에 연결했다. 같은 lesson은 CLI frontdoor와 WASM/browser frontdoor 양쪽에서 실행한다.
- Stage H 제한 PASS: 미리 계산된 봉인 일정의 edge/level 발화 tick에서 highlight/visibility/camera_focus action을 제품 UI에 재생한다. `zero_crossing/sign_change/extremum/tolerance_entry`를 관찰 샘플에서 계산하는 evaluator와 live online reaction은 구현하지 않았다.

## Stage A 감사표

| 축 | 기존 근거/프로토타입 상태 | 이번 제품 상태 |
|---|---|---|
| L0 제품 셸 | UI V2 screen plan은 4공간 후보를 제시했지만 실제 셈그림 화면은 기존 탭/역할 문구가 남아 있었다. | `배우기/실험실/만들기/배포` 전역 nav와 browse/run/create/deploy 매핑을 실제 UI에 반영했다. |
| L1 수업 실행 | 대표 lesson runner는 있었지만 UI V2 셸과 직접 이어진 계약은 부족했다. | lesson catalog 선택, 수업 열기, WASM 실행, 결과/오류 표시를 `seamgrim_ui_v2_product_shell_v1`으로 묶었다. |
| DDN 편집면 | 데스크톱/모바일 DDN 노출 정책이 제품 화면에서 분리되지 않았다. | 데스크톱은 DDN 패널을 유지하고 모바일은 명시 toggle로만 연다. |
| Primary view | 세계별 보개 선택은 휴리스틱/화면 관례에 기대는 부분이 있었다. | 일차함수/포물선/수요공급세금에 `primary_view_rules.v1`과 `seamgrim.observation_payload.v1`을 붙였다. |
| 실험실 E1 | 조절값 변경과 lineage 비교가 제품 계약으로 고정되지 않았다. | DDN 조절값 변경, 재실행, `origin_hash`/`delta_ref` 비교 패널을 browser runner로 검증했다. |
| 한국어 Manim 최소 코어 | 진자 view plan과 봉인 trace reaction은 설계/proposal 단계였다. | `rep_phys_pendulum_wave1_v1`, explicit `view_plan.v1`, sealed trace reaction product runtime/checker를 추가했다. |

## 제품 동작

- DDN은 기존 셈그림 WASM 제품 frontdoor로 실행되고, 관찰값은 `seamgrim.observation_payload.v1` rows로 제품 UI에 표시된다.
- 진자 lesson은 `rep_phys_pendulum_wave1_v1`로 추가했다.
- `view_plan_runtime.js`는 observation에서 explicit anchor를 해석하고, `space2d`, angle measure, same-tick graph cursor, camera policy report를 생성한다.
- `trace_reaction_runtime.js`는 lesson-local sealed trace file만 읽고, 반응은 view layer에만 적용한다.
- trace reaction은 sealed trace schedule의 미리 계산된 발화 tick을 읽고 `seamgrim.resolved_scene_trace.v1`로 선택/억제 action을 기록한다. 암묵 LWW는 금지하고 충돌은 `E_TRACE_REACTION_CONFLICT`로 남긴다. 조건 evaluator는 아직 없다.
- 확인 URL: `http://127.0.0.1:4177/solutions/seamgrim_ui_mvp/ui/index.html?tab=studio&lesson=rep_phys_pendulum_wave1_v1` (local static server pid 35928).

## 경계

- `docs/ssot/**` 변경 없음.
- parser/runtime 의미론 변경 없음.
- runtime `state_hash` 산식 변경 없음.
- H는 precomputed sealed schedule replay only다. 관찰 trace 기반 조건 계산, live online reaction, 외부 trace ingestion, authoring UI는 범위 밖이다.
- `view_plan_hash`와 `reaction_frame_hash`는 candidate view/report 해시다. runtime state hash 입력으로 편입하지 않았다.
- 카메라 선택과 trace reaction UI 선택은 `state_hash`에 참여하지 않는다. 월드 좌표 draw payload의 FNV 후보 해시는 정본 `bogae_hash=blake3(detbin)`와 구분한다.
- 각도재기 표시 toggle도 view-only이며 state hash 입력으로 편입하지 않았다.

## 검증

- `python tests/run_seamgrim_ui_v2_product_shell_check.py` PASS.
- `python tests/run_seamgrim_primary_view_contract_check.py` PASS.
- `python tests/run_seamgrim_lab_e1_minimal_check.py` PASS.
- `python tests/run_seamgrim_pendulum_view_plan_product_check.py` PASS.
- `python tests/run_seamgrim_sealed_trace_reaction_check.py` PASS.
- `cargo run --manifest-path tools/teul-cli/Cargo.toml -- run solutions/seamgrim_ui_mvp/lessons/rep_phys_pendulum_wave1_v1/lesson.ddn --madi 2` PASS.
- `python tests/run_seamgrim_first_delight_projectile_check.py` PASS.
- `python tests/run_seamgrim_current_line_three_worlds_check.py` PASS.
- `python tests/run_tool_world_diff_v1_check.py` PASS.
- `python tests/run_learning_spine_index_v1_check.py` PASS.
- `python tests/run_pack_golden.py seamgrim_ui_v2_product_shell_v1 seamgrim_primary_view_contract_v1 seamgrim_lab_e1_minimal_v1 seamgrim_pendulum_view_plan_product_v1 seamgrim_sealed_trace_reaction_product_v1` PASS.
- `node --check solutions/seamgrim_ui_mvp/ui/app.js` PASS.
- `node --check solutions/seamgrim_ui_mvp/ui/screens/run.js` PASS.
- `node --check solutions/seamgrim_ui_mvp/ui/screens/browse.js` PASS.
- `node --check solutions/seamgrim_ui_mvp/ui/view_plan_runtime.js` PASS.
- `node --check solutions/seamgrim_ui_mvp/ui/trace_reaction_runtime.js` PASS.
- `cargo check` PASS with existing warnings.
- `cargo check --manifest-path tools/teul-cli/Cargo.toml` PASS.
- `python tests/run_ci_sanity_gate.py --profile core_lang` PASS.
- `git diff --check` PASS.
- `git status --short -- docs/ssot` clean.

## 산출물

- New packs: `seamgrim_ui_v2_product_shell_v1`, `seamgrim_primary_view_contract_v1`, `seamgrim_lab_e1_minimal_v1`, `seamgrim_pendulum_view_plan_product_v1`, `seamgrim_sealed_trace_reaction_product_v1`.
- New browser runners/checkers under `tests/` for the five product gates above.
- New product modules: `solutions/seamgrim_ui_mvp/ui/view_plan_runtime.js`, `solutions/seamgrim_ui_mvp/ui/trace_reaction_runtime.js`.
- New lesson: `solutions/seamgrim_ui_mvp/lessons/rep_phys_pendulum_wave1_v1/`.

## 남은 항목

- live online reaction runtime은 아직 구현하지 않았다.
- `zero_crossing/sign_change/extremum/tolerance_entry`를 봉인 관찰 샘플에서 계산하는 evaluator는 아직 구현하지 않았다.
- sealed trace authoring/import UI는 아직 없다.
- matrix 장기 상태 재판정 또는 진짜닫힘 승격은 하지 않았다.
- 현재 워킹트리에는 이번 작업 전부터 존재한 unrelated/untracked 참고 파일이 남아 있다.
