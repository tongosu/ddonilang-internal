# 2026-07-11 Codex 세션 델타 - Wave 2A 실행 역할 경계 교정

## 발견

- 최신 HEAD는 기존 수업 모드 전환을 항상 숨기고 있었으므로, 배포 파일 실행에서 토글이 눈에 보인다는 주장은 재현되지 않았다.
- 그러나 감사의 핵심은 유효했다. 실행 화면에 역할 전환 DOM, 이벤트 처리, 전환 함수, 브라우저 계측, 과거 동작 팩이 남아 있었다.
- G1 검사는 실제 DOM과 제품 상태가 아니라 이미 사라진 문구만 검사하고 있었다.

## 수정

- 제품에서 `data-classroom-mode-switch`와 `data-classroom-mode` DOM을 제거했다.
- 전환 이벤트, `applyClassroomModeSwitch`, `classroomModeAccess`, `__STUDIO_CLASSROOM_MODE_SWITCH__` 제품 경로를 제거했다.
- 실행 진입 시 적용되는 배포 profile은 유지했다. 이는 실행 중 역할 전환이 아니라 배포 시점 구성이다.
- 과거 역할별 탐색 실행 종류는 작업 중심 `browse_select`로 정규화했다.
- `studio_classroom_mode_switch_v1`은 `superseded`로 낮췄다.
- Wave 2A G1과 UI V2 셸 검사가 DOM, 제품 JS, CSS, dataset 상태, 브라우저 artifact의 재유입을 거부하도록 강화했다.

## 검증

- Wave 2A, UI V2 셸, primary view, live reaction, offline/live parity, 뜻 커서, 수업계획 왕복, 반응형 수업 workflow 제품 checker PASS.
- 관련 팩 golden PASS.
- 변경 JavaScript 구문 검사 PASS.
- `cargo check`, `cargo check --manifest-path tools/teul-cli/Cargo.toml` PASS.
- `python tests/run_ci_sanity_gate.py --profile core_lang` PASS.
- `git diff --check` PASS, `docs/ssot/**` 변경 없음.

## 닫힘 경계

- G1 실행 중 역할 토글 부재: 검사된 제품 셸 범위에서 `닫힘-동작`.
- 배포 꾸러미의 profile 의미론은 배포 공간의 별도 계약으로 남는다.
- `docs/ssot/**`, DDN parser/runtime 의미론, `state_hash` 산식은 변경하지 않았다.
- 제거된 역할별 카탈로그 선택자를 요구하는 과거 교육·배포 runner는 현행 완료 근거가 아닌 legacy-test debt다.
- 배포 공간의 `screen-browse` 컨테이너 재사용은 이번 결함과 별개인 후속 구조 개선 후보다.
