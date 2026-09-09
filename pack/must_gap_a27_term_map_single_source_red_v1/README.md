# must_gap_a27_term_map_single_source_red_v1

TERM-MAP 단일 소스/FATAL term lint red conformance skeleton이다.

- evidence_tier: `docs_first`
- current_status: `designed`
- closure_claim: `no`

## 범위

- 목표: SSOT TERM-MAP의 `fatal_terms`가 Gate0 lint/canon의 단일 근거여야 함을 red 기준선으로 남긴다.
- 비범위: SSOT 수정, extractor/codegen 구현, golden 갱신.

## 근거

- SSOT: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:935`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:937`
- 감사: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:26`
- deepdive: `docs/context/reports/MUST_GAP_DEEPDIVE_A27_term_map_single_source_V1.md`

## 기대 red

`cases/c01_fatal_term_asset/input.ddn`은 현재 구현을 고치기 전까지 red 기준선이다. 이 pack은 실행용 golden이 아니며 `closure_claim: no`를 유지한다.
