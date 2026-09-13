# must_gap_a02_call_tail_resolve_unresolved_red_v1

CALL-TAIL-RESOLVE-01 해석 규칙 red conformance skeleton이다.

- evidence_tier: `docs_first`
- current_status: `designed`
- closure_claim: `no`

## 범위

- 목표: call-tail 후보 수집과 ambiguous 오류는 현재 브랜치에 착지했지만, 0개 후보 전용 unresolved 진단은 아직 보이지 않는다.
- 비범위: parser/runtime 구현, golden 갱신, 오류 코드 확정.

## 근거

- SSOT: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:825`
- 감사: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:21`
- deepdive: `docs/context/reports/MUST_GAP_DEEPDIVE_A02_call_tail_resolve_unresolved_V1.md`

## 기대 red

`cases/c01_unresolved_tail_dedicated_diag/input.ddn`은 현재 구현을 고치기 전까지 red 기준선이다. 이 pack은 실행용 golden이 아니며 `closure_claim: no`를 유지한다.
