# seamgrim_semantic_cursor_v1

셈그림 Wave 2A G4의 진자 뜻 커서를 고정하는 제품 검증 pack이다.

- 제품 lesson: `solutions/seamgrim_ui_mvp/lessons/rep_phys_pendulum_wave1_v1/lesson.ddn`
- anchor contract: `solutions/seamgrim_ui_mvp/lessons/rep_phys_pendulum_wave1_v1/view_plan.detjson`
- cursor runtime: `solutions/seamgrim_ui_mvp/ui/semantic_cursor_runtime.js`
- browser runner: `tests/seamgrim_semantic_cursor_runner.mjs`
- 범위: 관찰값, 그래프 축/현재점, 공간 객체 강조, DDN 원문 source span을 같은 anchor 선택으로 연결한다.
- 제외: 변수명 휴리스틱, AI 설명 직렬화, world state write, `state_hash` 참여, 새 DDN 문법.

이 pack의 golden은 실행 마커만 검증한다. 실제 제품 동작은 checker가 browser runner로 검증한다.
