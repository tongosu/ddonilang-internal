# seamgrim_lesson_view_plan_roundtrip_v1

Wave 2B G6의 `lesson_plan.v0` + `view_plan.v1` 통합 왕복 workflow를 검증하는 pack이다.

범위:

- `만들기 > 수업 구성` 구조 편집에서 활동별 scene, primary view, camera, measurement, reaction refs를 편집한다.
- G5의 view/reaction authoring artifact hash를 선택 활동에 연결한다.
- 코드 보기 TOML과 구조 입력이 같은 canonical 결과로 왕복한다.
- 보존하지 않는 항목은 UI transient state로만 계약에 남긴다.

테스트 전용 JSON 변환을 제품 loader에 하드코딩하지 않고, 제품 `lesson_plan_v0.js` parser/serializer가 필드를 보존한다.
