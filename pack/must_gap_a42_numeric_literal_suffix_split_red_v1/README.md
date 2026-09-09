# must_gap_a42_numeric_literal_suffix_split_red_v1

숫자 리터럴 접미 분리 red conformance skeleton이다.

- evidence_tier: `docs_first`
- current_status: `designed`
- closure_claim: `no`

## 범위

- 목표: `100cm를` 같은 숫자 리터럴 뒤 단위/조사 접미 분리 알고리즘이 제품 경로에 없음을 red 기준선으로 남긴다.
- 비범위: lexer/parser suffix-chain 구현, 단위 registry 확장, golden 갱신.

## 근거

- SSOT: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3291`
- 감사: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER2_V1.md:39`
- deepdive: `docs/context/reports/MUST_GAP_DEEPDIVE_A42_numeric_literal_suffix_split_V1.md`

## 기대 red

`cases/c01_numeric_unit_josa_suffix/input.ddn`은 현재 구현을 고치기 전까지 red 기준선이다. 이 pack은 실행용 golden이 아니며 `closure_claim: no`를 유지한다.
