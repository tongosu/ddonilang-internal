# 또니랑 배움길 연결 색인 W6 보고서

상태: 연결 색인·셈그림 탐색 UI `닫힘-동작` / 교육과정 전체 완성 미완료 / 승격은 사용자 결정 필요

## 결과

- 기존 교재, 셈그림 세계, 검증 팩, 가나다 좌표를 8단계 배움길로 잇는 `ddn.learning_spine_index.v1`을 추가했다.
- 단계 순서는 `값·식·단위`에서 시작해 `Python·Rust·JS·Modelica 대응 교과`로 이어진다.
- 셈그림 교과 화면의 `배움길`에서 8단계를 탐색하고 각 단계의 연결 세계를 바로 실행할 수 있다.
- `landed`, `mixed`, `gap_open` 상태를 분리해 현재 구현 근거와 열린 설계를 같은 색으로 표시하지 않는다.
- 교재·가이드, 구현 보고서, 승인 전 제안을 `source_kind`로 분리하고 source/reflection/implementation/owner 네 상태 축을 기록한다.
- 패널을 열면 닫기 버튼으로, 닫으면 배움길 버튼으로 키보드 초점을 복원한다.
- `landed` 1~3단계의 연결 세계 5개를 모두 제품 화면에서 열고 실제 마디 진행 또는 완료를 확인한다.
- 모바일은 정식 단계명을 본문에 유지하면서 탐색부에 짧은 이름을 사용한다.

## 제품 경계

이 색인은 새 교육과정이나 새 로드맵이 아니다. 기존 자산의 연결 위치와 부족한 자리를 보여주는 색인이다.

- 1~3단계: 현재 교재·세계·팩을 연결한 실행 가능 경로
- 4~7단계: 함수값, 모듬, 선언형 모델, AI diff의 착지 근거와 열린 세부 계약을 함께 표시
- 8단계: 네 언어 대응 교과의 씨앗과 비교 경계만 표시
- Modelica: acausal-lite 교육 모델링 비교 후보이며 full DAE·일반 해석기 완성을 주장하지 않음
- Python/Rust/JavaScript: 소비자·구현 언어 대응 씨앗이며 일대일 교과 완성을 주장하지 않음
- SSOT 반영과 색인 승격: 자동 권한 없음, 사용자 결정 필요

## 검증

```text
node tests/seamgrim_learning_spine_index_runner.mjs
PASS seamgrim_learning_spine_index: ok

python tests/run_learning_spine_index_v1_check.py
PASS [learning-spine-index-v1] OK connector-index-behavior-closed curriculum-completion-open owner-decision-required
```

통합 검사는 8단계 순서와 네 상태 축, 출처 종류, 모든 교재·팩·세계 참조 존재, landed 단계 증거 관문, 연결 세계 5개 실행, 키보드 초점 복원, overlay·태그 동결, Modelica 비목표, 데스크톱·모바일 넘침, pack golden, W5 회귀를 확인한다.

## 독립 검토

독립 Codex 검토에서 3건을 발견해 반영했다.

- 제안·구현 보고서·교재가 한 목록에 섞인 문제: 출처 종류와 네 상태 축으로 분리
- 열기·닫기 뒤 키보드 초점 유실: 닫기 버튼/배움길 버튼 간 초점 이동 추가
- `landed`가 파일 존재만으로 유지된 문제: 단계 증거 관문과 연결 세계 전수 실행 추가

강화된 LS01 증거 관문은 포물선 모바일 조절 영역이 W4/W5 패널에 눌려 20px로 줄어든 회귀도 발견했다. 첫 기쁨 모바일 subpanel 높이를 보정한 뒤 3세계와 world_diff 브라우저 검사를 모두 재통과했다.

## 시각 확인

- `I:/home/urihanl/ddn/codex/build/seamgrim_learning_spine_desktop.png`
- `I:/home/urihanl/ddn/codex/build/seamgrim_learning_spine_mobile_final.png`
- `I:/home/urihanl/ddn/codex/build/seamgrim_learning_spine_ls08_desktop.png`
- `I:/home/urihanl/ddn/codex/build/seamgrim_learning_spine_ls08_mobile.png`
- `I:/home/urihanl/ddn/codex/build/projectile_controls_mobile_restored.png`

`docs/ssot/**`, parser 문법, runtime 의미론, state hash 산식 변경 없음.
