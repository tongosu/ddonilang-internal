# must_gap_a47_multi_dispatch_specificity_red_v1

다중 디스덧댐 specificity red conformance skeleton이다.

- evidence_tier: `docs_first`
- current_status: `designed`
- closure_claim: `no`

## 범위

- 목표: overload 후보 수집, 가장 구체적 타입 선택, 동률/비교 불가 오류가 제품 경로에 없음을 red 기준선으로 남긴다.
- 비범위: type lattice 구현, overload parser/runtime 구현, golden 갱신.

## 근거

- SSOT: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3979`
- 감사: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:18`
- deepdive: `docs/context/reports/MUST_GAP_DEEPDIVE_A47_multi_dispatch_specificity_V1.md`

## 기대 red

이 pack은 실행용 golden이 아니며 `closure_claim: no`를 유지한다. `cases/c01_specific_type_wins/input.ddn`은 구체 타입 우선 선택, `cases/c02_incomparable_tie_errors/input.ddn`은 비교 불가 후보 오류 기준선이다.
