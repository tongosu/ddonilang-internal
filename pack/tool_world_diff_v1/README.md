# tool_world_diff_v1

`teul-cli world-diff`의 첫 제품 단위를 검증한다.

- 같은 원문 두 개: 뜻 단위 변경 0개.
- 중력 기본값 하나 변경: `control_init` 1개.
- 같은 마디 실행: baseline/candidate state·trace hash를 artifact에 기록.
- 후보 권한: `none`.
- 자동 적용, 파일 쓰기, full AST/SolvePlan/첫 분기 마디 claim: 금지.

