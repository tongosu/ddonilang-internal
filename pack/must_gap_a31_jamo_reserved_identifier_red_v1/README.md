# must_gap_a31_jamo_reserved_identifier_red_v1

시스템 예약 자음 식별자 red conformance skeleton이다.

- evidence_tier: `docs_first`
- current_status: `designed`
- closure_claim: `no`

## 범위

- 목표: 단자음/자음식별자를 사용자 정의 이름으로 쓰는 입력이 future diagnostic 대상임을 red 기준선으로 남긴다.
- 비범위: lexer/parser/lint 구현, SystemRootAlias 표 확정, golden 갱신.

## 근거

- SSOT: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1721`
- 감사: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:38`
- deepdive: `docs/context/reports/MUST_GAP_DEEPDIVE_A31_jamo_reserved_identifier_V1.md`

## 기대 red

`cases/c01_jamo_identifier_decl/input.ddn`은 현재 구현을 고치기 전까지 red 기준선이다. 이 pack은 실행용 golden이 아니며 `closure_claim: no`를 유지한다.
