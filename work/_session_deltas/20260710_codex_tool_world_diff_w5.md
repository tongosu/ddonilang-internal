# Session Delta - 뜻 단위 변경 검토 W5

- Date: 2026-07-10
- Agent: Codex
- Status: Reflected
- Closure: control-diff toolchain behavior-closed / review behavior-closed / full world diff open

## 변경

- `teul-cli world-diff` 제품 명령과 `ddn.world_diff.v1` artifact를 추가했다.
- 포물선 중력 4.9 후보를 baseline 9.8과 구조적으로 비교하고 240마디 CLI 실행 증거를 연결했다.
- 셈그림에 권한 없는 후보, 변경 뜻, 적용/버리기 사람 결정을 구현했다.
- 승인 전 자동 적용, 파일 쓰기, runtime AST 저장을 금지했다.
- 온뭉치 포물선 카드에 `world_diff_ref`를 연결했다.

## 검증

- Rust 단위 검사 3 PASS.
- world diff browser runner PASS.
- W5 통합 checker PASS.
- desktop/mobile 시각 확인 PASS.

## 열린 항목

- AST, 설정, 세움, SolvePlan, 막음 diff.
- 첫 state hash 분기 마디.
- CLI/browser hash parity 결정.
- 외부 AI 호출과 승인 artifact 영구 저장.

## 다음

- W6는 새 교과과정을 만들지 않고 기존 교재, exposure level, 가나다 좌표, pack, 셈그림 세계를 잇는 `learning_spine_index`로 진행한다.
