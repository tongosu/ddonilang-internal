# 세션 델타: 셈그림 네이티브 다중 파일 창작

- 목표: `WORKBENCH_NATIVE_MULTIFILE_AUTHORING_CLOSED`
- START_HEAD: `143cf2e37bcf6031060fa4e7631544f1c0f87a3c`
- 기준선: 요청된 브랜치/HEAD 일치, 조상 검사 PASS
- G0: 기존 기반 재사용 가능, native creation/edit-plan 부재로 미폐쇄 판정
- G1: 제품 계약을 `docs/context/briefs/BRIEF_SEAMGRIM_NATIVE_PROJECT_AUTHORING_CONTRACT_V1_20260717.md`에 기록
- unrelated dirty/untracked: 보존 중
- docs/ssot 변경: 없음
- 외부 사용자 성공: 0

## 다음

G2 Rust/WASM project edit-plan 1차를 구현했다.

- `rename_file`은 before hash, 영향 파일/참조, patch, after hash, 변경 후 source,
  atomic apply 가능 여부와 lock stale 경계를 반환한다.
- lexer token span과 `프로젝트`/`쓰임` 구조 블록만 사용해 일반 문자열·주석은 바꾸지 않는다.
- stale hash, `뿌리.ddn` rename, 중복 목표 경로를 적용 전에 거부한다.
- 검증: local-project 8 tests PASS, wasm feature cargo check PASS.

G2 2차 확장:

- 같은 edit-plan/WASM 계약에 `add_file`, `add_module`, `duplicate_file`, `delete_file`,
  `set_entry`를 추가했다.
- 참조 중 모듈, 현재 entry, `뿌리.ddn` 삭제를 적용 전에 거부한다.
- set-entry는 source entry와 `뿌리.ddn` 첫글/목표 참조를 함께 변경한다.
- 검증: local-project 11 tests PASS, wasm feature cargo check PASS.

다음은 G3 UI 생성 흐름과 G4 파일 작업/되돌리기에 연결한다.

## G3

- `새 프로젝트` 대화상자에서 이름과 빈 DDN/물리 실험 시작본을 선택한다.
- import 없이 실제 `뿌리.ddn`, `app/main.ddn`, 물리 시작본의 `lib/힘.ddn`을 만든다.
- 같은 local project payload를 편집, local recovery, 내 작업, portable/server 경로가 사용한다.
- 브라우저에서 생성 3파일 확인, reload, 내 작업 재열기, 가로 overflow 없음 PASS.
- 기존 승인 Workbench shell 브라우저 회귀 PASS.

## G4–G5 구조 편집

- 파일 추가, 모듈 시작본, 복제, 삭제, rename, entry 변경을 제품 WASM edit-plan에 연결했다.
- 적용 전 patch 미리보기를 표시하고 현재 source hash가 before hash와 같을 때만 적용한다.
- 최근 구조 변경 undo와 local recovery를 제공한다.
- 브라우저에서 rename 구조 참조 갱신, 일반 문자열/주석 보존, 참조 삭제 거부/트리 무변경,
  undo, add, duplicate, entry/root 동시 변경, reload 재열기 PASS.
- WASM bundle/manifest를 재봉인했고 freshness PASS.

## G6

- 기존 파일 서랍의 접이식 정보 영역에 entry, local module, import 방향, 가지, lock 상태를 표시한다.
- graph/symbol 진단은 문제·위치·고침 안내를 제공하고 존재하는 파일 위치는 선택 가능하다.
- 실제 브라우저에서 `app/main.ddn —힘→ lib/힘.ddn` import edge 확인 PASS.
- 문장 끝 `dt.`와 다음 줄의 `위치 보여주기`를 모듈 참조로 오인하던 token fallback을
  같은 줄 제한으로 수정하고 Rust negative regression PASS.

## G7–G8 물리 수직

- 물리 시작본은 `lib/힘.ddn`에서 중력을 드러내고 `app/main.ddn`이 이를 쓰며 위치·속도를
  마디별 계산한다.
- 실제 브라우저/WASM에서 4마디 실행 PASS.
- 모듈 rename 후 같은 4마디의 runtime state hash와 canvas pixel signature 동일 PASS.
- 중력값 9.8→4.9 변경 후 state hash, observation trace hash, canvas pixel signature 변화 PASS.
- 보개 상단 표시는 구조 경로가 섞인 trace hash 대신 bounded state hash를 사용해 의미 보존
  rename이 픽셀을 바꾸지 않도록 했다.
- 브라우저 step 완료를 madi 증가로 동기화하고 전체 물리 수직을 연속 5회 PASS했다.

## G9–G11 durable/share/my-work

- 네이티브 생성 프로젝트의 서버 최초 저장과 append-only 두 번째 revision PASS.
- 서버 재시작 뒤 edit capability로 3파일 재열기 및 같은 4마디 state hash 재현 PASS.
- view capability에서 원문 편집과 실행 제어를 제품 UI가 거부하도록 보정하고 PASS.
- view에서 clone 후 별도 project id/edit capability 및 독립 revision 저장 PASS.
- portable download를 깨끗한 브라우저 컨텍스트에서 import해 같은 3파일과 state hash 재현 PASS.
- 내 작업 제목 검색, 로컬 전용/서버 저장/받은 프로젝트 및 편집 가능/보기 전용 라벨을 추가했다.
- durable 수직 브라우저 검사를 연속 3회 PASS했다.

## G12–G14 공격·viewport·회귀

- source hash 충돌을 브라우저에서 주입해 rename 부분 적용 없음 PASS.
- 생성 취소, 참조 삭제 공격, 구조 undo, 경로/중복/root 보호 Rust negative controls PASS.
- 네이티브 생성 흐름을 1440×900, 1024×768, 778×912, 390×844에서 키보드 생성·파일
  선택, editor/primary view 최소 크기, icon accessible name/tooltip, 가로 overflow 없음으로 확인했다.
- 기존 종합 Workbench 4 viewport/server conflict/lock/lifecycle 관문 PASS.
- local-project multifile, boundary matrix, portable roundtrip, CLI/WASM parity 관문 PASS.

## G15–G16 promotion

- 물리 run 관찰값에 위치(m), 속도(m/s), 중력(m/s²) 이름·값·단위를 표시한다.
- 서버 중단 상태에서도 현재 local recovery에서 portable export PASS.
- promotion checker가 제품 marker, Rust lexer edit, WASM export와 12개 negative control 증거를
  확인하고 고의 marker 제거 mutation 6종을 모두 탐지한다.
- `python tests/run_seamgrim_native_multifile_authoring_promotion_check.py --full` PASS.
- 최종 lock 감사에서 edit-plan stale 표시와 적용 시 WASM lock atomic regeneration을 보정했다.
