# 뜻 단위 변경 검토 W5 보고서

상태: 조절 규칙 toolchain `닫힘-동작` / 사람 검토 UI `닫힘-동작` / 전체 world diff 미완료

## 결과

- `teul-cli world-diff <baseline.ddn> <candidate.ddn>` 제품 명령을 추가했다.
- 두 원문을 공통 정본화 frontdoor로 읽고 매김 조절 계획을 구조적으로 비교한다.
- 같은 원문은 변경 0개, 포물선 중력 기본값 `9.8 -> 4.9`는 `control_init` 한 축만 검출한다.
- 선택한 마디 수로 두 원문을 실행해 CLI state/trace hash를 artifact에 기록한다.
- 셈그림은 `ddn.world_diff.v1`을 읽어 변경 뜻을 한국어로 보여주고, 사람이 `적용` 또는 `버리기`를 누르기 전에는 현재 세계를 바꾸지 않는다.
- 적용은 현재 브라우저 세션의 조절값만 바꾸며 원문 파일을 쓰지 않는다.

## 제품 경계

현재 착지한 축은 매김 조절의 기본값, 범위, 간격, 자료형, 추가·제거다. 다음은 아직 미착지다.

- 전체 정본 AST diff
- `설정`, `세움`, SolvePlan, `막음` 전용 diff
- 첫 state hash 분기 마디 계산
- CLI와 브라우저/WASM 상태 해시 산식의 동일성 주장
- 실제 외부 AI 호출

후보 artifact의 권한은 항상 `none`이다. 승인·거절은 `ddn.world_diff.review_event.v1` 로컬 이벤트이며, 승인 후 권한도 `local_session_only`다.

## 검증

```text
cargo test --manifest-path tools/teul-cli/Cargo.toml world_diff -- --nocapture
PASS 3 tests

node tests/seamgrim_world_diff_review_runner.mjs
PASS seamgrim_world_diff_review: ok

python tests/run_tool_world_diff_v1_check.py
PASS [tool-world-diff-v1] OK toolchain-behavior-closed review-behavior-closed ai-authority-none
```

통합 검사는 artifact 2회 바이트 결정성, 같은 원문 빈 diff, 한 조절값 한 축 diff, 승인/거절, pack golden, 슬기 gatekeeper, W4 비교판, 온뭉치 카드 회귀를 함께 확인한다.

## 시각 확인

- `I:/home/urihanl/ddn/codex/build/seamgrim_world_diff_review_desktop.png`
- `I:/home/urihanl/ddn/codex/build/seamgrim_world_diff_review_mobile.png`

해시와 내부 schema는 학습 화면에서 숨기고, 변경 뜻과 사람 결정만 노출했다. `docs/ssot/**`, parser 문법, runtime 의미론, state hash 산식 변경 없음.
