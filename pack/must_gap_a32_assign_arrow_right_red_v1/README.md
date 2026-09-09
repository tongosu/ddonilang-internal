# must_gap_a32_assign_arrow_right_red_v1

`->` 우향 대입 입력 설탕 red conformance skeleton이다.

- evidence_tier: `docs_first`
- current_status: `designed`
- closure_claim: `no`

## 범위

- 목표: `식 -> 자리.`를 입력으로 허용하고 정본은 `<-`로 출력해야 함을 red 기준선으로 남긴다.
- 비범위: lexer/parser/canon 구현, golden 갱신.

## 근거

- SSOT: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1908`
- 감사: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:42`
- deepdive: `docs/context/reports/MUST_GAP_DEEPDIVE_A32_assign_arrow_right_V1.md`

## 기대 red

`cases/c01_right_assignment/input.ddn`은 현재 구현을 고치기 전까지 red 기준선이다. 이 pack은 실행용 golden이 아니며 `closure_claim: no`를 유지한다.
