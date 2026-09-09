# seamgrim_primary_view_contract_v1

세 대표 세계의 primary view 선택을 휴리스틱이 아니라 lesson 선언과 version-pinned 규칙표로 고정하는 검증 pack이다.

- 일차함수: `graph`
- 포물선: `space2d`
- 시장세금: `graph`

제품 runner는 `?tab=studio&lesson=...` 경로로 실제 DDN/WASM 실행을 열고, `schema_id`, `schema_version`, `ruleset_hash`, `lesson_declaration_hash`, `heuristic_selection=false`를 DOM dataset에서 확인한다.

이 pack의 golden은 실행 마커만 검증한다. 실제 제품 행동은 checker가 browser runner로 검증한다.
