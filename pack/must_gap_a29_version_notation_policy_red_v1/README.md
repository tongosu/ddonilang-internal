# must_gap_a29_version_notation_policy_red_v1

SSOT 버전 표기 정책 red conformance skeleton이다.

- evidence_tier: `docs_first`
- current_status: `designed`
- closure_claim: `no`

## 범위

- 목표: `r1/r2`식 revision 표기 대신 PATCH/MINOR/MAJOR 정책을 강제해야 함을 red 기준선으로 남긴다.
- 비범위: docs lint 구현, SSOT 수정, golden 갱신.

## 근거

- SSOT: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1355`
- 감사: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:28`
- deepdive: `docs/context/reports/MUST_GAP_DEEPDIVE_A29_version_notation_policy_V1.md`

## 기대 red

`cases/c01_revision_notation/input.md`는 현재 구현을 고치기 전까지 red 기준선이다. 이 pack은 실행용 golden이 아니며 `closure_claim: no`를 유지한다.
