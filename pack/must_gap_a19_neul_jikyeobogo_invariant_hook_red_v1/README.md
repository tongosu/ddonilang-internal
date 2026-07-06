# must_gap_a19_neul_jikyeobogo_invariant_hook_red_v1

16.2 `늘지켜보고` 문법 red conformance skeleton이다.

- evidence_tier: `docs_first`
- current_status: `designed`
- closure_claim: `no`

## 범위

- 목표: 계약/rollback 시스템은 있으나 commit 직전 invariant hook `늘지켜보고` 표면은 제품 경로에 없다.
- 비범위: parser/runtime 구현, golden 갱신, 오류 코드 확정.

## 근거

- SSOT: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4039`
- 감사: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:22`
- deepdive: `docs/context/reports/MUST_GAP_DEEPDIVE_A19_neul_jikyeobogo_invariant_hook_V1.md`

## 기대 red

`cases/c01_invariant_hook_surface/input.ddn`은 현재 구현을 고치기 전까지 red 기준선이다. 이 pack은 실행용 golden이 아니며 `closure_claim: no`를 유지한다.
