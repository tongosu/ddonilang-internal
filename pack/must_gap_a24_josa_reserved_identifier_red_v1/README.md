# must_gap_a24_josa_reserved_identifier_red_v1

조사 단독 식별자 예약/금지 red conformance skeleton이다.

- evidence_tier: `docs_first`
- current_status: `designed`
- closure_claim: `no`

## 범위

- 목표: `을`, `를`, `이`, `가` 등 조사별칭 자체가 식별자로 사용될 때 future diagnostic 대상임을 red 기준선으로 남긴다.
- 비범위: lexer/parser/lint 구현, 금지 목록 확장, golden 갱신.

## 근거

- SSOT: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6976`
- 감사: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER4_V1.md:55`
- deepdive: `docs/context/reports/MUST_GAP_DEEPDIVE_A24_josa_reserved_identifier_V1.md`

## 기대 red

`cases/c01_bare_josa_identifier/input.ddn`은 현재 구현을 고치기 전까지 red 기준선이다. 이 pack은 실행용 golden이 아니며 `closure_claim: no`를 유지한다.
