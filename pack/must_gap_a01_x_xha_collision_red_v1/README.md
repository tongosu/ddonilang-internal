# must_gap_a01_x_xha_collision_red_v1

V18-00D `X`/`X하` 이름 충돌 금지의 red conformance skeleton이다.

- evidence_tier: `docs_first`
- current_status: `designed`
- closure_claim: `no`

## 범위

- 목표: 같은 스코프에서 `계산`과 `계산하`를 별도 씨앗으로 정의하는 입력은 정의 시점에 거부되어야 한다.
- 현재 제품 경로: call-tail 호출 시점 ambiguity는 존재하지만 정의 시점 충돌 금지는 별도 구현 근거가 없다.
- 비범위: parser/runtime 구현, golden 갱신, 오류 코드 확정.

## 근거

- SSOT: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:875`
- 감사: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:22`
- 현재 call-tail ambiguity 구현: `tools/teul-cli/src/runtime/eval.rs:2421`, `tools/teul-cli/src/runtime/eval.rs:2435`
- 잔여 gap 보고서: `docs/context/reports/MUST_GAP_DEEPDIVE_A01_x_xha_collision_V1.md`

## 기대 red

`cases/c01_x_xha_same_scope/input.ddn`은 현재 구현을 고치기 전까지 red 기준선이다. 이 pack은 실행용 golden이 아니며, `closure_claim: no`를 유지한다.
