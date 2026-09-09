# must_gap_a09_match_branch_e_ttara_red_v1

27.1.1 갈래 분기 `~에 따라` red conformance skeleton이다.

- evidence_tier: `docs_first`
- current_status: `designed`
- closure_claim: `no`

## 범위

- 목표: `~에 따라` match expression은 제품 parser/runtime에서 찾지 못했다. 현재 유사 분기는 `고르기` statement이다.
- 비범위: parser/runtime 구현, golden 갱신, 오류 코드 확정.

## 근거

- SSOT: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4668`
- 감사: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:43`
- deepdive: `docs/context/reports/MUST_GAP_DEEPDIVE_A09_match_branch_e_ttara_V1.md`

## 기대 red

`cases/c01_e_ttara_match_surface/input.ddn`은 현재 구현을 고치기 전까지 red 기준선이다. 이 pack은 실행용 golden이 아니며 `closure_claim: no`를 유지한다.
