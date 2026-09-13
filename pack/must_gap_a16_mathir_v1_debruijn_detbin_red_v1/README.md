# must_gap_a16_mathir_v1_debruijn_detbin_red_v1

§M1.5 MathIR v1 / De Bruijn / DetBin red conformance skeleton이다.

- evidence_tier: `docs_first`
- current_status: `designed`
- closure_claim: `no`

## 범위

- 목표: 수식 parser/evaluator와 formatter는 있으나 MathIR v1, De Bruijn index, MathIRDetBin 직렬화는 제품 경로에서 닫히지 않았다.
- 비범위: parser/runtime 구현, golden 갱신, 오류 코드 확정.

## 근거

- SSOT: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5339`
- 감사: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:60`
- deepdive: `docs/context/reports/MUST_GAP_DEEPDIVE_A16_mathir_v1_debruijn_detbin_V1.md`

## 기대 red

`cases/c01_bound_variable_alpha_equiv/input.ddn`은 현재 구현을 고치기 전까지 red 기준선이다. 이 pack은 실행용 golden이 아니며 `closure_claim: no`를 유지한다.
