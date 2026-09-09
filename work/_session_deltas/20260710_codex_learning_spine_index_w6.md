# Session Delta - 또니랑 배움길 연결 색인 W6

- Date: 2026-07-10
- Agent: Codex
- Status: Reflected
- Closure: connector index behavior-closed / curriculum completion open / owner decision required

## 변경

- 기존 교육 자산을 8단계로 잇는 `ddn.learning_spine_index.v1`을 추가했다.
- 셈그림 교과 화면에 배움길 탐색과 세계 실행 이동을 연결했다.
- `landed`, `mixed`, `gap_open`을 분리하고 열린 항목을 단계별로 기록했다.
- 교재·가이드, 구현 보고서, 승인 전 제안의 출처 종류와 source/reflection/implementation/owner 상태 축을 분리했다.
- 키보드 초점 복원과 landed 연결 세계 5개 실행 검증을 추가했다.
- overlay는 `learning_spine_index` 하나만 사용하고 7개 태그 어휘를 동결했다.
- Python/Rust/JavaScript/Modelica 대응 교과를 미완료로 유지하고 Modelica full DAE 비목표를 명시했다.

## 검증

- manifest의 모든 교재·팩·세계 참조 존재 확인 PASS.
- desktop/mobile browser runner PASS.
- landed 1~3단계의 단계 증거 관문과 연결 세계 5개 실행 PASS.
- pack golden PASS.
- W5 world diff와 W4/W3 회귀 PASS.
- `docs/ssot/**` 변경 없음.

## 독립 검토 반영

- P1 권한·상태 축 혼합: 수정 완료.
- P2 열기·닫기 초점 유실: 수정 완료.
- P2 landed 실행 근거 부족: 수정 완료.
- 강화 관문에서 발견한 포물선 모바일 조절 영역 축소 회귀: 수정 완료, W2/W5 browser runner 재통과.

## 열린 항목

- 일급 함수·제네릭·결과형의 승인된 세부 교과.
- 모듬·package·테스트·진단의 초심자 연결 차시.
- 세움 11축 선언형 runtime과 제한된 논리·증명 교범.
- full AST/SolvePlan world diff와 실제 AI 후보 출처.
- 네 언어 개념 ID·예제 대응표와 교착어 원어민 검토.

## 다음

- W7은 사용자 승인과 독립 검토를 거쳐 배움길의 source/reflection/implementation/owner 상태를 확정한다.
- 제품 작업은 10세계 중 다음 시각 효과가 큰 세계의 닫힘-동작으로 이어간다.
