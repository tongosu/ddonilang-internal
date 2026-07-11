# CODEX 초장기 목표 2026-07-11

## 셈그림 Wave 2A: 라이브 반응·뜻 연결·수업 구성 수직 구현

이 문서를 VS Code Codex의 목표로 사용한다. 질문이 없어도 시작할 수 있도록 범위와 결정이 고정되어 있다.

## 0. 최종 목표

진자 대표 수업에서 다음 흐름이 제품 UI와 WASM 경로로 실제 동작하게 만든다.

```text
배우기에서 활동 시작
-> 진자 실행과 그래프·공간 장면 관찰
-> 실험실에서 줄 길이 또는 시작 각도 변경
-> InputSnapshot 기반 새 실행 계보 생성
-> committed observation 기반 라이브 반응
-> 그래프·추·각도재기·관찰값·DDN 원문의 뜻 연결
-> 만들기에서 활동 순서 편집
-> 저장한 수업계획을 다시 열어 같은 활동 흐름 실행
```

이 목표는 4~5시간 이상의 연속 개발을 허용하는 초장기 목표다. 시간을 채우기 위해 범위를 늘리지는 말고, 필수 관문의 제품 품질과 검증을 높인다.

North Star:

> 처음 보는 사용자가 설치 없이 진자 수업을 실행하고, 값을 바꾸고, 변화의 뜻을 확인하고, 자기 수업 흐름을 만들 수 있는가?

## 1. 시작 기준과 작업 경계

- 시작 브랜치: 현재 `codex/queue-20260706`
- 기준 커밋: `25c84eb`
- 선행 커밋: `60cdb3a`, `9b3ebf7`, `b5b41ec`, `25c84eb`
- 먼저 읽을 문서:
  - `AGENTS.md`
  - `AGENT_WORKFLOW.md`
  - `SSOT_POLICY.md`
  - `docs/context/all/DEV_SUMMARY.md`
  - `docs/context/reports/SEAMGRIM_KOREAN_MANIM_NEXT_WAVE_DECISION_BRIEF_V1_20260711.md`
  - `docs/context/proposals/PROPOSAL_KOREAN_MANIM_REACTIVE_KNOWLEDGE_SCENE_V2_20260711.md`
  - `work/_session_deltas/20260711_codex_seamgrim_product_to_korean_manim_vertical.md`

시작 즉시 `git status --short`를 기록한다. 기존 dirty/untracked 파일은 사용자 작업으로 간주하고 수정·stage·commit하지 않는다. 특히 기존 Ganada intake, `또니랑/**`, unrelated report/index, projectile lesson의 선행 변경을 건드리지 않는다.

`docs/ssot/**`는 읽기 전용이다. 변경·stage 0건을 각 관문과 마지막에 확인한다.

## 2. 고정 설계 결정

아래 사항은 재질문하지 않고 구현 기준으로 사용한다.

1. DDN/WASM이 세계 계산의 유일한 제품 진실이다. JS에서 진자 물리를 다시 계산하지 않는다.
2. 라이브 evaluator는 commit 뒤의 구조화 observation snapshot을 마디당 한 번 읽는다.
3. 보기 반응은 세계를 쓰지 않으며 `state_hash`에 참여하지 않는다.
4. 세계 hook runtime은 선행 조건이 아니다.
5. 오프라인과 라이브는 predicate core·벡터·충돌 규칙을 공유한다.
6. 의미 연결은 `anchor_id/source_ref`로만 한다. 변수명 휴리스틱을 금지한다.
7. 카메라는 DrawList를 바꾸지 않는 보기 정책이다. 월드 좌표 DrawList와 renderer profile 경계를 유지한다.
8. 수업 활동 전환은 도구층 lesson runner가 소유한다. `마당{}` runtime을 요구하지 않는다.
9. 수업계획 V0는 `lesson_plan.v0.toml` + 정규화 AST다. 새 DDN `수업{}` 문법을 만들지 않는다.
10. 학생/교사는 실행 중 역할 토글이 아니다. 배포 구성의 문제이며 이번 목표에서 새 역할 스위치를 만들지 않는다.
11. 현재 local 권위 기준은 `v24.12.9-candidate`다. 다른 candidate의 미반영 결정을 제품 전제로 삼지 않는다.

## 3. 금지 범위

- 새 core block, 예약어, DDN 문법
- 테스트 전용 lowering으로 제품 완료 주장
- JS 물리 시뮬레이터 또는 하드코딩된 진자 결과
- world state에 카메라·highlight·lesson state 쓰기
- 일반 DAE solver, 마당 runtime closure
- 일반 수식 morph, 문자열 기반 항 매칭
- deployment profile 완성 또는 보안 주장
- MP4/video export
- AI 자동 저작·자동 승인
- 전체 한국어 Manim 완료 주장
- unrelated 대규모 리팩터링

## 4. 커밋 규율

각 관문을 검증한 뒤 바로 독립 커밋한다. 마지막 한 번에 몰아서 커밋하지 않는다.

권장 커밋:

1. `refactor(seamgrim): separate four product spaces`
2. `feat(seamgrim): evaluate live view reactions`
3. `test(seamgrim): prove offline live reaction parity`
4. `feat(seamgrim): connect semantic lesson cursor`
5. `feat(seamgrim): add lesson plan authoring vertical`
6. `test(seamgrim): close responsive lesson workflow`

커밋 전에는 목표 파일만 stage됐는지 확인한다. 기존 dirty 파일을 정리하거나 되돌리지 않는다.

## G0. 기준선과 세션 기록

다음 파일을 만든다.

`work/_session_deltas/20260711_codex_seamgrim_wave2a_live_semantic_lesson.md`

필수 절:

- 시작 상태
- 관문별 결과
- 닫힘-문서/닫힘-동작
- 질문 큐
- 부분 구현
- 검증
- 커밋 목록

기존 Wave 1 제품 checker와 관련 pack을 먼저 실행한다. 기준선 실패가 있으면 원인을 분리해 기록하고 새 기능으로 덮지 않는다.

## G1. 4공간 제품 IA를 실제 행동으로 분리

현재 셸의 이름만 바꾼 상태를 넘어서 각 공간의 주 작업을 코드와 화면에서 분리한다.

### 배우기

- 대표 교과/샘플 교과/검색은 탐색 분류로 유지한다.
- 배포 열기·붙여넣기·묶음 복사·저장·교과 만들기를 같은 탐색 탭 줄에서 제거한다.
- 수업을 열면 학습 활동 runner로 진입한다.
- 학생/교사 선택을 보이지 않는다.

### 실험실

- 현재 세계의 허용 조절값, 실행, 재생, 비교, 계보를 주 작업으로 둔다.
- 교사용 배포 준비 동작을 주 실행 막대에서 제거한다.
- 조절값 변경은 기존 InputSnapshot/lineage 경로를 사용한다.

### 만들기

- `세계 코드`와 `수업 구성`을 동등한 상위 탭으로 둔다.
- 세계 코드 편집기는 실제 코딩이 가능한 높이를 확보한다. 데스크톱 기본 최소 높이 420px, 전체화면/확장 명령을 제공한다.
- 작은 보조 패널 안에 DDN 편집기를 가두지 않는다.

### 배포

- 배포 열기, 묶음 복사·저장, 교사용 준비는 배포 공간으로 모은다.
- deployment profile은 후속임을 명확히 하되 기존 배포 기능을 깨지 않는다.

### 공통

- 설명은 하나의 `정보` 서랍으로 연다. 상단 버튼이 별도 하단 탭을 대신 선택하는 이중 진입 구조를 없앤다.
- 그래프 수업은 그래프가 primary view다. 기본 숫자 표는 의미 관찰값 보조 영역으로 내린다.
- 데스크톱 주 시각 영역은 가용 세로 공간의 절반 이상을 사용한다.
- DDN은 배우기/실험실에서 접을 수 있어도 찾을 수 있어야 하고, 만들기에서는 항상 명시적이다.
- 텍스트 버튼 대신 익숙한 명령은 기존 아이콘 체계와 tooltip을 사용한다.

### G1 합격 기준

- 네 공간의 주 작업과 URL/상태 전이가 runner로 검증된다.
- 학생/교사 런타임 토글이 새 흐름에 노출되지 않는다.
- 대표 교과/샘플/검색과 배포 명령이 같은 동급 탭으로 렌더되지 않는다.
- 설명 진입점이 하나다.
- 기존 배포·교과 열기 기능은 해당 공간에서 계속 동작한다.
- desktop/mobile browser smoke PASS.

## G2. Wave 1L 라이브 반응 evaluator

오프라인 evaluator를 복사해 두 번째 의미론을 만들지 않는다. predicate core를 공유 가능한 제품 모듈로 정리하고 offline/online adapter가 사용하게 한다.

온라인 입력 최소 계약:

```text
lineage_id
run_id
tick
committed_observation
ruleset_ref
```

필수 동작:

1. commit 뒤 같은 마디를 정확히 한 번 평가한다.
2. 같은 계보·마디·동일 payload 재전달은 멱등이며 동작을 중복 발화하지 않는다.
3. 같은 계보·마디의 다른 payload는 `E_VIEW_LIVE_DUPLICATE_TICK_MISMATCH` 후보 진단이다.
4. 이전 마디보다 작은 tick은 `E_VIEW_LIVE_OUT_OF_ORDER` 후보 진단이다.
5. tick 누락은 `W_VIEW_LIVE_TICK_GAP` 후보로 기록하고 조용히 완전 재현을 주장하지 않는다.
6. lineage가 바뀌면 edge/level 기억, 마지막 tick, 임시 장면 효과를 초기화한다.
7. `zero_crossing`, `sign_change`, `extremum`, `tolerance_entry`를 지원한다.
8. `highlight`, `visibility`, `camera_focus`를 실제 제품 화면에 적용한다.
9. 같은 대상·같은 속성의 같은 우선순위 충돌은 `E_VIEW_REACTION_CONFLICT`다.
10. 명시 priority가 다르면 높은 쪽을 선택하고 억제된 동작과 이유를 결과 trace에 남긴다.

evaluation은 render loop, `requestAnimationFrame`, 임의 timer가 아니라 WASM commit 전달 지점에 연결한다.

### G2 합격 기준

- 실제 진자 실행 중 0 통과·극값·허용오차 진입이 화면 반응으로 보인다.
- pause/resume/step/reset에서 중복 발화가 없다.
- 수동 scrub은 라이브 evaluator를 오염시키지 않고 offline replay 결과를 사용한다.
- 조절 변경 후 새 lineage의 첫 마디부터 올바르게 다시 평가한다.
- live claim은 제품 runner와 browser smoke가 PASS한 범위에서만 true다.

## G3. 오프라인/라이브 parity와 resolved scene trace

같은 봉인 observation trace를 두 경로에 넣어 결과를 비교하는 제품 pack을 만든다.

비교 대상:

- 발화 tick
- rule id
- predicate result
- selected actions
- suppressed actions
- diagnostics
- camera policy 선택

`resolved_scene_trace`는 새 계획 계층이 아니라 `view_plan` 적용 결과 sidecar다. `state_hash` 참여는 false다.

필수 fixture:

- 정상 순차 입력
- 같은 tick 동일 payload 중복
- 같은 tick 다른 payload 중복
- 역순 tick
- tick gap
- lineage 전환
- 같은 속성 충돌
- 명시 priority 해결

### G3 합격 기준

- 정상 trace에서 offline/online 결과가 byte-stable 정규형으로 일치한다.
- 오류 fixture의 한국어 진단이 무엇이/어디서/어떻게 고칠지 3층을 갖는다.
- replay/scrub을 반복해도 결과가 바뀌지 않는다.

## G4. 진자 뜻 커서 수직 구현

진자의 다음 anchor를 명시적으로 등록한다.

- 각도
- 각속도
- 추 위치
- 속도
- 위치에너지
- 운동에너지

하나의 anchor를 선택하거나 현재 활동이 가리키면 다음 표현이 함께 반응한다.

- 의미 관찰값 행
- 그래프 계열과 현재점
- 공간 장면 객체
- 각도재기/벡터/에너지 표현
- 명시적 source_ref가 있는 경우 DDN 원문 위치

규칙:

- DOM 문자열이나 변수명으로 대상을 찾지 않는다.
- 단위와 label은 구조화 observation/anchor에서 읽는다.
- 사람용 문장은 별도 presenter가 만든다. AI 직렬화 계약을 이번에 확정하지 않는다.
- 선택과 강조는 view 상태이며 `state_hash`를 바꾸지 않는다.
- keyboard focus와 screen reader 이름을 제공한다.

### G4 합격 기준

- 그래프 범례, 관찰값, 공간 객체 중 어느 진입점에서 선택해도 같은 anchor가 선택된다.
- 선택된 세계 마디가 그래프 현재점과 공간 장면에서 일치한다.
- DDN source_ref가 없는 anchor는 추측해서 이동하지 않고 이유를 진단한다.
- 모바일에서 선택 표시가 그래프·재생 막대·각도 라벨을 가리지 않는다.

## G5. 수업계획 V0 제품 loader·runner·저작 UI

### 소유권

수업계획은 활동 순서와 학습 행위만 소유한다. 세계 계산, 카메라 좌표, 렌더 primitive는 소유하지 않는다.

V0 필드:

```text
schema
lesson_id
title
activities[]
  activity_id
  kind = observe | change | compare | explain
  title
  prompt
  preset_ref?
  allowed_controls[]?
  question?
  check_ref?
  view_plan_ref?
  anchor_refs[]?
```

저작 원본은 `lesson_plan.v0.toml`이다. 제품 loader가 파싱해 정규화 AST를 만들며 테스트 harness 전용 변환을 금지한다. 브라우저가 직접 여는 제품 경로에서도 동작해야 한다.

### 배우기 runner

- 이전/다음 활동, 현재 활동, 전체 진행을 표시한다.
- 활동 전환은 세계 마당을 전환하지 않는다.
- `observe`는 지정 anchor와 primary view를 연다.
- `change`는 allowed control만 노출한다.
- `compare`는 기존 lineage/world_diff 자산으로 baseline과 variant를 보여 준다.
- `explain`은 질문과 의미 관찰값을 보여 준다.

### 만들기 저작 UI

- `수업 구성` 탭에 활동 목록과 활동 편집기를 제공한다.
- 활동 추가, 삭제, 위/아래 이동, 종류 변경, 제목·prompt·참조 편집이 실제 동작한다.
- `목록`과 `계획 코드`는 같은 AST를 본다.
- 계획 코드 편집기는 충분한 높이와 확장 명령을 가진다.
- 목록 편집 -> 코드 -> 목록 왕복과 코드 -> 목록 -> 코드 왕복이 의미상 무손실이다.
- 오류는 해당 활동과 필드를 가리키는 한국어 진단으로 표시한다.

### 첫 진자 수업계획

1. 진자의 각도와 에너지 관찰
2. 시작 각도 변경
3. 원본과 변경 실행 비교
4. 0 통과와 최고점의 에너지 관계 설명

### G5 합격 기준

- lesson plan 파일을 열어 네 활동을 끝까지 진행할 수 있다.
- 새 활동 추가·재정렬·편집 후 저장하고 다시 열어 동일하다.
- `lesson_plan_roundtrip_v1` golden PASS.
- loader/runner/editor가 실제 제품 UI 경로에 연결된다.
- `마당{}` runtime 또는 새 DDN 문법이 추가되지 않는다.

## G6. 제품 품질과 반응형 검수

필수 viewport:

- 1440×900
- 1024×768
- 390×844

각 viewport에서 다음을 직접 검증한다.

1. 진자 수업 열기
2. 첫 실행
3. 그래프·공간 장면·각도 라벨 확인
4. 한 단계 실행과 pause/resume
5. 조절값 변경과 새 lineage 확인
6. 라이브 반응 확인
7. 뜻 커서 선택
8. 네 활동 진행
9. 만들기에서 수업 구성 편집과 왕복
10. 배포 공간 이동 후 기존 배포 기능 확인

canvas는 단순 DOM 존재가 아니라 nonblank pixel과 올바른 framing을 확인한다. 그래프·코드·관찰값·재생 막대가 겹치지 않아야 한다. 긴 한국어 label이 컨테이너 밖으로 넘치지 않아야 한다.

첫 기쁨 기록:

- 첫 수업 선택 -> 첫 실행
- 첫 실행 -> 첫 조절 변경
- 첫 조절 변경 -> 첫 비교/뜻 확인

자동 측정 기반이 없으면 수동 smoke 절차와 실제 시간을 기록하되 성능 수치를 과장하지 않는다.

## G7. 검증 배터리

최소 검증:

```text
신규 product checker 전부
신규 pack golden 전부
기존 Wave 1 Seamgrim checker
pendulum CLI frontdoor
cargo check
cargo check --manifest-path tools/teul-cli/Cargo.toml
python tests/run_ci_sanity_gate.py --profile core_lang
Playwright/browser desktop+tablet+mobile smoke
git diff --check
git status --short -- docs/ssot
```

테스트가 만든 open log 부산물은 시작 기준과 비교해 복원하되 사용자 파일은 건드리지 않는다.

## 5. 중단 관문

다음 경우 해당 관문을 부분으로 기록하고 다음 독립 관문으로 이동한다.

- 실제 WASM committed observation 연결 없이 fixture만으로 live를 흉내 내야 하는 경우
- InputSnapshot 계보를 우회해야 하는 경우
- 새 언어 문법이 필요한 경우
- `docs/ssot/**` 수정이 필요한 경우
- 일반 수식 morph나 마당 runtime이 필요해지는 경우

질문 큐에 근거 파일과 최소 선택지를 남긴다. 막힘을 감추기 위해 fallback simulation을 만들지 않는다.

## 6. 최종 보고

최종 답변과 세션 델타에 다음을 남긴다.

- 관문별 완료/부분/미착수
- 닫힘-동작과 닫힘-문서 분리
- 실제 변경 파일
- 커밋 해시와 제목
- 실행한 검증과 PASS/FAIL
- browser 확인 URL
- `docs/ssot/**` 변경/stage 0건 확인
- 기존 dirty/untracked 파일 보존 목록
- live online, 수업계획, 뜻 커서 각각의 남은 한계

## 7. 성공 정의

이 목표의 성공은 기능 파일 수가 아니다.

```text
진자 세계의 실제 DDN/WASM 결과가
라이브 장면과 그래프에 뜻으로 연결되고,
사용자가 그 흐름을 네 활동짜리 수업으로 구성해
다시 열고 실행할 수 있으며,
같은 trace에서 offline/live 반응이 일치하는 것.
```

이 범위가 제품 runner와 브라우저 증거로 닫힐 때만 `셈그림 Wave 2A 닫힘-동작`을 주장한다. 한국어 Manim 전체 완료는 주장하지 않는다.
