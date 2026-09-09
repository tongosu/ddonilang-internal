# must_gap_a30_haebogo_geugeot_frontdoor_red_v1

`~해보고:` + `그것` teul-cli frontdoor parity red conformance skeleton이다.

- evidence_tier: `docs_first`
- current_status: `designed`
- closure_claim: `no`

## 범위

- 목표: `tools/teul-cli` 제품 frontdoor에서 `해보고`/`그것`이 원문 표면으로 닫히지 않은 상태를 red 기준선으로 남긴다.
- 비범위: root `lang`/legacy `tool` 구현 승격, parser/runtime 구현, golden 갱신.

## 근거

- SSOT: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1435`
- 감사: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:30`
- deepdive: `docs/context/reports/MUST_GAP_DEEPDIVE_A30_haebogo_geugeot_frontdoor_parity_V1.md`

## 기대 red

`cases/c01_haebogo_geugeot_frontdoor/input.ddn`은 `teul-cli` 제품 frontdoor parity가 닫히기 전까지 red 기준선이다. 이 pack은 실행용 golden이 아니며 `closure_claim: no`를 유지한다.
