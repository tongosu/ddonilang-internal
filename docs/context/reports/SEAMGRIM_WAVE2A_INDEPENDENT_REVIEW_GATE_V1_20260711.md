# 셈그림 Wave 2A 독립 검수 관문 V1

- 작성일: 2026-07-11
- 대상 목표: `CODEX_SUPERLONG_GOAL_SEAMGRIM_LIVE_SEMANTIC_LESSON_V1_20260711.md`
- 역할: 구현자와 분리된 Codex/Claude 검수자가 사용
- 권위: 검수 절차이며 SSOT가 아니다.

## 1. 검수 원칙

1. 커밋 메시지나 완료 보고가 아니라 제품 행동을 본다.
2. grep/token checker만으로 닫힘-동작을 승인하지 않는다.
3. fixture 입력과 실제 WASM committed observation 경로를 구분한다.
4. offline PASS를 live PASS로 확장하지 않는다.
5. UI가 숨겼다는 사실과 책임 경계가 제거됐다는 사실을 구분한다.
6. candidate schema 구현과 SSOT canonical 승격을 구분한다.
7. 작성자와 검수자는 달라야 하며 불일치는 사용자에게 올린다.

## 2. 필수 입력

- 구현 커밋 목록
- 관문별 세션 델타
- 변경 파일 목록
- 신규·기존 pack 결과
- browser smoke 기록과 viewport
- 제품 확인 URL
- `docs/ssot/**` 무변경 증거
- 기존 dirty 파일 보존 목록

하나라도 없으면 즉시 실패시키지 않고 `증거 부족`으로 분류한다. 구현 실패와 증거 실패를 섞지 않는다.

## R0. 격리와 커밋

- 기준 `670e636` 이후 구현 커밋이 관문별로 분리됐는가.
- unrelated dirty/untracked 파일이 commit에 섞이지 않았는가.
- `docs/ssot/**` 변경·stage가 0건인가.
- 기존 Wave 1 pack이 회귀 없이 PASS하는가.

합격: 변경 파일과 커밋의 소유 범위가 설명 가능하다.

## R1. 4공간 IA

실제 화면에서 확인한다.

- 배우기: 대표/샘플/검색과 수업 진행이 주 작업인가.
- 실험실: 조절·실행·비교·계보가 주 작업인가.
- 만들기: 세계 코드와 수업 구성이 충분한 편집 공간을 갖는가.
- 배포: 열기·묶음·준비 동작이 모였는가.
- 학생/교사 런타임 토글이 새 흐름에 노출되지 않는가.
- 설명 진입점이 하나인가.
- 그래프 수업의 primary view가 숫자 표보다 앞서는가.

실패 예:

- 기존 버튼을 CSS로만 숨기고 keyboard/route에서 계속 주 동작으로 남김
- 네 공간 이름은 있으나 모두 같은 studio 화면을 열고 상태만 바꿈
- 코드 편집기가 보조 패널 크기에 머묾

## R2. 라이브 반응 의미론

다음은 실제 WASM 실행에서 확인한다.

- evaluation 입력이 commit 뒤 observation인가.
- tick당 한 번만 평가되는가.
- pause/resume/step/reset에서 중복 발화가 없는가.
- 같은 tick 동일 payload는 멱등인가.
- 같은 tick 다른 payload, 역순, gap이 각각 진단되는가.
- lineage 변경 시 edge/level 기억이 초기화되는가.
- world state write가 없는가.

라이브 화면에서 반응이 보이더라도 JS가 진자 값을 다시 계산하면 실패다.

## R3. Offline/Live parity

같은 sealed observation trace를 두 evaluator에 넣는다.

비교:

- fired ticks
- rule ids
- selected/suppressed actions
- diagnostics
- camera selections
- normalized resolved scene trace bytes

정상 순차 입력에서 byte-stable 정규형이 같아야 한다. 오류 fixture는 같은 오류일 필요는 없지만 경계 차이가 문서화돼야 한다.

## R4. 뜻 커서

진자 anchor 하나를 그래프 범례, 관찰값, 공간 객체에서 각각 선택한다.

- 모든 진입점이 같은 anchor id를 가리키는가.
- 그래프 현재점과 공간 장면이 같은 tick인가.
- 단위와 label이 구조화 payload에서 오는가.
- source_ref가 없을 때 변수명으로 추측하지 않는가.
- 선택이 state_hash를 바꾸지 않는가.
- keyboard와 screen reader로 같은 동작이 가능한가.

## R5. 수업계획 V0

- 제품 loader가 `lesson_plan.v0.toml`을 직접 읽는가.
- 테스트에서만 JSON으로 변환해 제품에는 하드코딩하지 않았는가.
- 목록과 계획 코드가 같은 AST를 쓰는가.
- 추가, 삭제, 이동, 종류·prompt 편집이 실제 저장되는가.
- 저장 후 재열기에서 의미가 같은가.
- observe/change/compare/explain 네 활동을 끝까지 진행할 수 있는가.
- 활동 전환이 world `마당{}` runtime을 요구하지 않는가.

왕복은 공백·주석 byte 보존이 아니라 정규화된 의미 보존으로 판정한다. 보존하지 않는 표현 정보는 명시한다.

## R6. 화면 품질

viewport:

- 1440×900
- 1024×768
- 390×844

확인:

- canvas nonblank pixel
- 그래프·공간 장면 framing
- 각도 라벨·재생 막대·활동 진행·DDN 겹침 없음
- 긴 한국어 label overflow 없음
- 코드 편집 가능 높이
- primary view가 가용 세로 공간의 절반 이상
- 모바일에서 DDN과 보기 전환 가능

스크린샷만 보지 말고 실행·조절·활동 전환 뒤 다시 확인한다.

## R7. 닫힘 주장

허용:

- `Wave 2A 닫힘-동작`: R0~R6이 모두 PASS한 목표 범위
- `부분`: 독립 관문만 PASS
- `증거 부족`: 행동은 있을 수 있으나 검수 자료 부족

금지:

- 한국어 Manim 완료
- lesson plan canonical
- deployment profile 완료
- formula transform 완료
- deterministic video export 완료
- live parity를 한 정상 fixture만으로 일반화

## 3. 검증 배터리

구현자가 보고한 명령을 그대로 믿지 않고 검수자가 핵심을 재실행한다.

```text
python tests/run_seamgrim_korean_manim_decision_ledger_check.py
신규 Wave 2A product checker
기존 Wave 1 Seamgrim product checker
pendulum CLI frontdoor
cargo check
cargo check --manifest-path tools/teul-cli/Cargo.toml
python tests/run_ci_sanity_gate.py --profile core_lang
browser desktop/tablet/mobile smoke
git diff --check
git status --short -- docs/ssot
```

## 4. 검수 결과 형식

```text
R0 격리: PASS/FAIL/증거 부족 — 근거
R1 IA: PASS/FAIL/증거 부족 — 근거
R2 live: PASS/FAIL/증거 부족 — 근거
R3 parity: PASS/FAIL/증거 부족 — 근거
R4 뜻 커서: PASS/FAIL/증거 부족 — 근거
R5 lesson plan: PASS/FAIL/증거 부족 — 근거
R6 화면 품질: PASS/FAIL/증거 부족 — 근거
R7 주장 경계: PASS/FAIL — 근거

중대 불일치:
사용자 결정 요청:
허용 닫힘 문구:
남은 위험:
```
