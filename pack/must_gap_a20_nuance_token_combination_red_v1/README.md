# must_gap_a20_nuance_token_combination_red_v1

17.5 말결 결합 규칙 red conformance skeleton이다.

- evidence_tier: `docs_first`
- current_status: `designed`
- closure_claim: `no`

## 범위

- 목표: `말결값` builtin은 있지만 `$...` token sequence, 기본 0.5, 다중 token 마지막 적용, 부정어 반전 결합은 없다.
- 비범위: parser/runtime 구현, golden 갱신, 오류 코드 확정.

## 근거

- SSOT: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4137`
- 감사: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:27`
- deepdive: `docs/context/reports/MUST_GAP_DEEPDIVE_A20_nuance_token_combination_V1.md`

## 기대 red

`cases/c01_dollar_nuance_combination/input.ddn`은 현재 구현을 고치기 전까지 red 기준선이다. 이 pack은 실행용 golden이 아니며 `closure_claim: no`를 유지한다.
