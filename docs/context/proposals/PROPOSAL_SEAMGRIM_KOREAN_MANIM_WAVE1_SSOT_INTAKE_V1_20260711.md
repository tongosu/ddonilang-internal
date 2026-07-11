# 셈그림·한국어 Manim Wave 1 SSOT 인입 제안 V1

- 작성일: 2026-07-11
- 상태: SSOT 관리자 검토용 proposal
- 기준: local `v24.12.9-candidate` 파일군과 2026-07-11 Wave 1/1T 제품 증거
- 직접 반영: 금지. 이 문서는 `docs/ssot/**`를 수정하지 않는다.

## 1. 목적

7월 10일 SSOT는 한국어 Manim의 목표·비목표·공백을 이미 반영했다. 7월 11일 제품 구현은 그 공백 일부에 실제 증거를 만들었다. 이번 인입은 schema를 정본으로 승격하는 작업이 아니라 다음 세 상태를 정확히 기록하는 작업이다.

1. SSOT에 이미 반영된 방향
2. 대표 진자 1세계에서 실제로 동작하는 부분 증거
3. 여전히 미구현·미승인인 일반 계약

기준 장부는 `docs/context/reports/SEAMGRIM_KOREAN_MANIM_DECISION_LEDGER_V1_20260711.detjson`이다.

## 2. 핵심 판정

### 부분 증거로 올릴 수 있음

- 명시적 scene binding: 진자 observation anchor와 각도재기·graph cursor 결합
- 카메라: 고정·맞춤·따라가기 3정책의 진자 reference subset
- 봉인 observation trace 생성
- `zero_crossing`, `sign_change`, `extremum`, `tolerance_entry` 오프라인 평가
- `highlight`, `visibility`, `camera_focus` 재생
- `resolved_scene_trace` candidate sidecar와 scrub/replay 안정성

### 아직 올리면 안 됨

- `view_plan.v1` 전체 canonical schema 또는 canonical bytes
- live online reaction
- 세 시간의 정본 계약
- semantic cursor 전체
- 측정 부품 가족
- lesson plan schema
- formula transform, object morph, frame/mp4 export
- 한국어 Manim 완료

## 3. 대상 SSOT와 제안 변경

### 3.1 `SSOT_UPDATE_NOTES_v24.12.9.md`

관리자가 적절한 다음 번호에 아래 취지의 evidence section을 추가한다.

```text
2026-07-11 한국어 Manim Wave 1 제품 증거

- 대표 진자 1세계에서 explicit observation binding, angle measure,
  graph cursor, fixed/fit/follow view camera가 제품 UI/WASM frontdoor에 연결됐다.
- 봉인 observation trace를 대상으로 4개 조건을 평가하고
  highlight/visibility/camera_focus를 scrub/replay하는 offline 제품 경로가 있다.
- 위 증거는 OI-MANIM-SCENE-BINDING-01,
  OI-MANIM-CAMERA-LAYER-TRANSITION-01,
  OI-BOGAE-PLAN-SCHEMA-01, OI-412의 부분 증거다.
- live online reaction, general schema, formula transform, object morph,
  export는 여전히 OPEN이다.
- `state_hash` 산식, parser, world runtime 의미는 바뀌지 않는다.
```

증거:

- commits: `60cdb3a`, `9b3ebf7`, `b5b41ec`, `25c84eb`
- packs: `seamgrim_pendulum_view_plan_product_v1`, `seamgrim_sealed_observation_trace_v1`, `seamgrim_trace_predicate_evaluator_v1`, `seamgrim_sealed_trace_reaction_product_v1`

### 3.2 `SSOT_OPEN_ISSUES_v24.12.9.md`

새 OI를 먼저 만들지 말고 기존 OI에 evidence note를 붙인다.

| 기존 OI | 반영할 증거 | 닫히지 않은 이유 |
|---|---|---|
| `OI-MANIM-SCENE-BINDING-01` | 진자 explicit anchor binding | SolvePlan·수식 항·범용 schema 없음 |
| `OI-MANIM-CAMERA-LAYER-TRANSITION-01` | fixed/fit/follow subset | layer·transition·충돌 정본 없음 |
| `OI-BOGAE-PLAN-SCHEMA-01` | `view_plan.v1` reference payload | canonical bytes/hash/roundtrip 없음 |
| `OI-412` | sealed trace offline reaction | live online과 `보개마당` parser/runtime closure 없음 |
| `OI-411` | 4공간 셸 partial | 기존 3화면 기준과 새 IA의 최종 사용자 결정 필요 |

`resolved_scene_trace`, lesson plan, deployment profile은 이번에 새 OI로 증식시키지 않는다. 먼저 사용자 결정과 Wave 2A 제품 증거를 기다린다.

### 3.3 `SSOT_PLANS_v24.12.9.md`

Korean Manim completion order의 첫 단계에 아래 상태 주석을 제안한다.

```text
manim_ko_scene_binding_v1: 대표 진자 reference subset은 product evidence가 있다.
general binding closure는 OPEN.

manim_ko_scene_player_v1: sealed trace offline scrub/reaction subset은
product evidence가 있다. live player와 canonical scene player closure는 OPEN.
```

완료 순서 자체는 바꾸지 않는다. formula transform과 graph explain의 일반 구현은 계속 후속이다.

### 3.4 `SSOT_TERMS_v24.12.9.md`

이번 인입에서 새 정본 용어를 추가하지 않는다. `semantic_anchor`, `resolved_scene_trace`, `lesson_plan`, 측정 부품 가족은 사용자 승인 전 proposal 용어로 유지한다.

## 4. 위임된 방향 결정

사용자가 설계·검토 판단을 Codex에 위임한 범위에서 다음 다섯 방향을 **candidate 제품 원칙으로 채택**한다. exact schema와 canonical 승격은 계속 OPEN이다.

| 번호 | 결정 | 채택 범위 |
|---|---|---|
| D1 | 한국어 Manim을 `반응형 지식 장면`으로 설명 | 제품 설명 개념으로 채택, 언어 키워드 금지 |
| D2 | 세계 마디/장면 커서/출력 프레임 3분리 | candidate 원칙 채택 |
| D3 | `semantic_anchor`와 `resolved_scene_trace` 이름 | candidate artifact 이름 채택 |
| D4 | 셈그림 4공간과 역할=배포 구성 원칙 | 제품 IA 원칙 채택, deployment schema 보류 |
| D5 | lesson plan V0를 도구층 TOML/AST로 시작 | 구현 실험 채택, `수업{}` 문법 보류 |

이 결정은 SSOT 본문을 자동으로 바꾸지 않는다. SSOT 관리자는 candidate 반영 위치와 버전 표기만 검토한다.

## 5. 제품 영향

이 proposal 자체는 제품을 바꾸지 않는다. 관리자가 evidence를 반영해도 기존 제품의 parser/runtime/state_hash가 바뀌지 않는다. Wave 2A 구현은 별도 목표와 제품 검증을 따른다.

## 6. 검증

```text
python tests/run_seamgrim_korean_manim_decision_ledger_check.py
git diff --check
git status --short -- docs/ssot
```

## 7. 범위 밖

- SSOT 직접 수정
- local 파일명의 버전 번호 정리
- OI 닫기
- live online 완료 주장
- 한국어 Manim 전체 완료 주장
