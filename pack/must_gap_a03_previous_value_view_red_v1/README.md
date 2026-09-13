# must_gap_a03_previous_value_view_red_v1

7.2 이전값보기 red conformance skeleton이다.

- evidence_tier: `docs_first`
- current_status: `designed`
- closure_claim: `no`

## 범위

- 목표: `이전값보기` 표면은 현재 제품 경로에서 찾지 못했다. 내부 rollback/edge detector용 prev_value 변수는 있으나 사용자 표면 구현이 아니다.
- 비범위: parser/runtime 구현, golden 갱신, 오류 코드 확정.

## 근거

- SSOT: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2970`
- 감사: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER2_V1.md:26`
- deepdive: `docs/context/reports/MUST_GAP_DEEPDIVE_A03_previous_value_view_V1.md`

## 기대 red

`cases/c01_previous_value_surface/input.ddn`은 현재 구현을 고치기 전까지 red 기준선이다. 이 pack은 실행용 golden이 아니며 `closure_claim: no`를 유지한다.
