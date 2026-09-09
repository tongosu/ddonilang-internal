# 2026-07-11 Codex — 셈그림 다음 초장기 목표 설계

## 읽은 근거

- `AGENTS.md`
- `AGENT_WORKFLOW.md`
- `SSOT_POLICY.md`
- `CLAUDE.md`
- `docs/context/all/DEV_SUMMARY.md`
- `docs/context/proposals/PROPOSAL_KOREAN_MANIM_REACTIVE_KNOWLEDGE_SCENE_V2_20260711.md`
- `work/_session_deltas/20260710_codex_seamgrim_ui_v2_screen_plan.md`
- `work/_session_deltas/20260711_codex_korean_manim_reactive_knowledge_scene_v2.md`
- `work/_session_deltas/20260711_codex_seamgrim_product_to_korean_manim_vertical.md`
- Wave 1/1T 커밋 `60cdb3a`, `9b3ebf7`, `b5b41ec`, `25c84eb`

## 판정

- Wave 1T 오프라인 반응 이후 다음 제품 단위는 live만 단독으로 닫는 것보다 UI 역할 분리, 의미 커서, 수업계획 도구층을 포함한 사용자 수직 흐름이 적절하다.
- 새 DDN 문법, 마당 runtime, 수식 morph, 영상 export는 다음 목표에서 제외한다.
- 구현은 VS Code Codex가 장시간 수행하고, 설계·범위·완료 주장 감사는 Codex 앱이 맡는 분업이 적절하다.

## 산출물

- `docs/context/reports/SEAMGRIM_KOREAN_MANIM_NEXT_WAVE_DECISION_BRIEF_V1_20260711.md`
- `docs/context/roadmap/CODEX_SUPERLONG_GOAL_SEAMGRIM_LIVE_SEMANTIC_LESSON_V1_20260711.md`

## SSOT 경계

- `docs/ssot/**` 수정 없음.
- 본 문서의 계약은 제품 구현 지시용 candidate이며 SSOT 반영을 주장하지 않는다.

## 다음 착수점

VS Code Codex에 roadmap 목표 문서를 그대로 전달한다. 각 관문별 독립 커밋과 browser 제품 증거를 요구한다.
