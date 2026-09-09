# must_gap_a26_semsi_result_slot_red_v1

SEMSI-RESULT-01 셈씨 결과칸 red conformance skeleton이다.

- evidence_tier: `docs_first`
- current_status: `designed`
- closure_claim: `no`

## 범위

- 목표: 셈씨 이름을 암묵 결과칸으로 취급하고 마지막 대입을 반환값으로 삼아야 함을 red 기준선으로 남긴다.
- 비범위: parser/runtime 구현, `돌려주기` 정책 변경, golden 갱신.

## 근거

- SSOT: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:7057`
- 감사: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER4_V1.md:58`
- deepdive: `docs/context/reports/MUST_GAP_DEEPDIVE_A26_semsi_result_slot_V1.md`

## 기대 red

`cases/c01_result_slot_assignment/input.ddn`은 현재 구현을 고치기 전까지 red 기준선이다. 이 pack은 실행용 golden이 아니며 `closure_claim: no`를 유지한다.
