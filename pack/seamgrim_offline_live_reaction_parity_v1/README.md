# seamgrim_offline_live_reaction_parity_v1

셈그림 Wave 2A G3의 offline/live reaction parity를 고정하는 제품 검증 pack이다.

- offline 경로: `solutions/seamgrim_ui_mvp/ui/trace_reaction_runtime.js`
- live 경로: `solutions/seamgrim_ui_mvp/ui/live_trace_reaction_runtime.js`
- runner: `tests/seamgrim_offline_live_reaction_parity_runner.mjs`
- 비교 대상: 발화 tick, rule id, predicate result, selected actions, suppressed actions, diagnostics, camera policy
- 필수 fixture: 정상 순차 입력, 동일 payload 중복, 다른 payload 중복, 역순 tick, tick gap, lineage 전환, 같은 속성 충돌, 명시 priority 해결
- 경계: `resolved_scene_trace`는 `view_plan` 적용 sidecar이며 새 plan layer가 아니다. `state_hash`에는 참여하지 않는다.

이 pack의 golden은 실행 마커만 검증한다. 실제 parity와 오류 fixture는 checker가 제품 runtime runner로 검증한다.
