# must_gap_a35_goreumssi_tag_union_red_v1

`고름씨` closed tag union red conformance skeleton이다.

- evidence_tier: `docs_first`
- current_status: `designed`
- closure_claim: `no`

## 범위

- 목표: `고름씨`가 닫힌 variant/type registry를 가져야 함을 red 기준선으로 남긴다.
- 비범위: parser/type/runtime 구현, atom representation 변경, golden 갱신.

## 근거

- SSOT: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2649`
- 감사: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:58`
- deepdive: `docs/context/reports/MUST_GAP_DEEPDIVE_A35_goreumssi_tag_union_V1.md`

## 기대 red

`cases/c01_goreumssi_definition/input.ddn`은 현재 구현을 고치기 전까지 red 기준선이다. 이 pack은 실행용 golden이 아니며 `closure_claim: no`를 유지한다.
