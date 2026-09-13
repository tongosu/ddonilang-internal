# 2026-07-11 Codex Session Delta - Seamgrim Wave 1 Independent Audit

## 감사 판정

- 제품 UI/WASM 수직 구현의 핵심인 대표 세계, 관찰 payload, E1 lineage, 진자 explicit view plan, 각도재기, same-tick cursor, fixed/fit/follow camera는 실제 제품 runner로 확인했다.
- 최초 구현은 `수업 열기`와 `실험실에서 바꾸기`가 같은 콜백과 같은 화면 상태로 이어졌다. 두 진입을 각각 `learn`과 `lab` 공간으로 전달하도록 수정하고 browser test를 보강했다.
- FNV 후보값을 정본 `bogae_hash`로 노출하던 이름 충돌을 제거했다. 현재 이름은 `world_draw_payload_hash_candidate`이며 정본 `bogae_hash=blake3(detbin)`를 주장하지 않는다.
- 최초 H 구현은 네 조건을 계산하지 않고 전 구간에서 네 predicate를 모두 true로 두었다. 이를 미리 계산된 발화 tick에서만 action을 재생하는 경계로 수정하고 `condition_evaluation_claim=false`를 고정했다.
- 과거 tick을 scrub한 뒤 카메라나 각도 표시를 바꾸면 live tick으로 튀던 결함을 수정했다. view-only 설정 변경은 현재 장면 커서를 유지한다.

## 닫힘 범위

- 닫힘-동작: UI V2 4공간 셸과 배우기/실험실 진입 분리, 3대표 세계 primary view/관찰 payload, Lab E1 lineage, 진자 view plan과 카메라/각도재기, 미리 계산된 봉인 일정 재생.
- 미완료: 봉인 관찰 샘플에서 `zero_crossing`, `sign_change`, `extremum`, `tolerance_entry`를 계산하는 evaluator, live online reaction, 외부 trace ingestion/authoring UI.

## 안전 경계

- `docs/ssot/**`는 수정하지 않았다.
- parser/runtime 의미론과 `state_hash` 산식은 수정하지 않았다.
- 기존 unrelated 변경과 untracked 파일은 보존했다.

## 검증

- 신규 제품 checker 5종 PASS: UI V2 셸, primary view, Lab E1, 진자 view plan, precomputed sealed schedule replay.
- 진자 제품 checker를 병렬 3회 실행해 camera/angle 변경 경쟁 조건이 재발하지 않음을 확인했다.
- `cargo run --quiet --manifest-path tools/teul-cli/Cargo.toml -- run solutions/seamgrim_ui_mvp/lessons/rep_phys_pendulum_wave1_v1/lesson.ddn --madi 2` PASS.
- 신규 pack golden 5종 PASS.
- 기존 회귀 PASS: first delight projectile, current-line three worlds, world diff, learning spine 전체 집계와 browser runner.
- `cargo check`, `cargo check --manifest-path tools/teul-cli/Cargo.toml`, `python tests/run_ci_sanity_gate.py --profile core_lang` PASS.
- 실제 화면: 1440x900에서 캔버스 771x434, 3열 317/804/313px, 가로 넘침 없음. 390x844에서 캔버스 x=37..338, 300x169로 viewport 안에 표시됨.
- `git diff --check` PASS, `git status --short -- docs/ssot` clean.
