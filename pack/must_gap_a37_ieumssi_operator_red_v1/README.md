# must_gap_a37_ieumssi_operator_red_v1

사용자 정의 이음씨/중위연산 red conformance skeleton이다.

- evidence_tier: `docs_first`
- current_status: `designed`
- closure_claim: `no`

## 범위

- 목표: 말 이음씨, 기호 이음씨, 확장 이음기호, 사용자 우선순위 registry가 제품 경로에 없음을 red 기준선으로 남긴다.
- 비범위: lexer/parser/type/runtime 구현, precedence registry 설계 확정, golden 갱신.

## 근거

- SSOT: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2780`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2804`
- 감사: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER2_V1.md:20`
- deepdive: `docs/context/reports/MUST_GAP_DEEPDIVE_A37_word_ieumssi_operator_V1.md`

## 기대 red

`cases/c01_word_ieumssi/input.ddn`은 현재 구현을 고치기 전까지 red 기준선이다. 이 pack은 실행용 golden이 아니며 `closure_claim: no`를 유지한다.
