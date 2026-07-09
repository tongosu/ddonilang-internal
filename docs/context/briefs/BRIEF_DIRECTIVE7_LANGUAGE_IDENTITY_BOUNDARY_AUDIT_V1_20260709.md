# BRIEF: 지시문 7 실행 — 언어 정체성·교육·국제화·게임엔진 경계 감사

작성: 2026-07-09 KST
근거: `또니랑/CODEX_HANDOFF_20260706_설정헤더_정합_및_구제안_델타.md` §지시문 7 (원문 지시, 아직 미실행 확인됨)
성격: **AUDIT — 결정 아님.** parser/runtime 변경 0건, `docs/ssot/**` 수정 0건.

## 배경

또니랑은 "한국어로 결정적 세계를 정의하고 재현하는 언어"라는 정본 정체성을 갖고 있으며, 교육·누리짐·말힘누리·교착어권 표면으로 확장되는 제품선을 가진다. 다만 이를 "범용 프로그래밍 언어", "완성된 국제어", "풀스택 게임 엔진", "현대 언어 이론 전체 교육과정"으로 과잉 주장하면 SSOT·구현·검증 상태와 어긋난다.

## 작업

AUDIT 보고서 1건 작성 (결정 아님):

1. **네 역할별 주장-근거 매트릭스** 작성:
   - 선언적 시뮬레이션: `누리/마디/InputSnapshot/state_hash/replay`로 닫힌 부분과 `세움/잇기/될때/인 동안` 등 아직 열려 있는 부분 분리.
   - 교육/현대 언어 이론: 초심자 문법·세계 모델링·결정성·상태/입력/재연 교육에는 강점이 있으나, 타입 이론/증명론/효과 시스템/컴파일러 이론 전체 커리큘럼으로 닫지 않음.
   - 한국어 기반 교착어권 국제 표면: 한국어 정본 + `sym3` + 방언 후보의 방향성은 강점이지만, `ko-common` 및 T2 언어군은 native review·pack equivalence 전까지 "국제어 완성" 주장 금지.
   - 게임 엔진 역할: world kernel/game-logic engine/DrawList producer로는 주장 가능하나, 렌더링·에셋·오디오·네트워크·편집기까지 포함한 full game engine 주장은 금지.
2. 각 역할을 `closed / conditional / proposal / not-claim`로 분류하고, 문구 예시를 함께 제안한다.
3. 공개 문구 권고안을 작성한다:
   - 권장: "한국어 네이티브 결정적 세계 모델링 언어", "교육용 시뮬레이션 언어", "게임 월드 로직 커널", "교착어권 친화 표면을 목표로 하는 다언어 DSL".
   - 비권장: "범용 언어", "완성된 국제어", "완성형 게임 엔진", "현대 언어학/프로그래밍 언어 이론 전체를 대체하는 교육과정".
4. 다음 증빙 필요 목록을 만든다: 대표 교육 vertical slice, dialect native review 표, dialect pack equivalence, DrawList adapter smoke, 누리짐 consumer parity, 언어이론 학습 범위표.
5. 보고서는 `docs/reports/audit/LANGUAGE_IDENTITY_BOUNDARY_AUDIT_V1_20260709.md`에 두고 `docs/reports/audit/INDEX.md`를 갱신한다. SSOT 본문 변경이 필요하면 별도 PROPOSAL/OI로만 올린다.

## 참고 자료 (이번 감사가 참조할 기존 증빙)

- `docs/reports/audit/KO_COMMON_PROMOTION_READINESS_AUDIT_V1_20260707.md` — ko-common 4조건 중 2 미충족/2 부분충족 확인됨. 이 감사의 "국제어 완성 주장 금지" 판단에 직접 근거로 쓸 것.
- `docs/reports/audit/NURIGYM_CONSUMER_EVIDENCE_STATUS_V1.md` — 누리짐 consumer parity 현황.
- `docs/context/reports/SETTINGS_HEADER_T0_ALIGNMENT_AUDIT_V1.md` — 선언적 시뮬레이션 축의 기존 증빙.

## 공통 불변 경계 (MUST)

- `state_hash` 산식·입력 변경 금지.
- `docs/ssot/**` 직접 수정 금지.
- CLOSED 주장은 `golden_closed` pack PASS + SSOT status sync로만 계산.
- 신규 문법 도입 0건.
- `main` 직접 커밋 금지 — `codex/queue-20260706`에만.

## DoD

감사 보고서 1건 + 주장-근거 매트릭스 + 권장/비권장 문구표 + 증빙 gap 목록. parser/runtime 변경 0건, `docs/ssot/**` 수정 0건, closure 주장 없음.
