# must_gap_a43_binding_ambiguity_lsp_quickfix_red_v1

바인딩 모호성 진단과 LSP QuickFix red conformance skeleton이다.

- evidence_tier: `docs_first`
- current_status: `designed`
- closure_claim: `no`

## 범위

- 목표: 후보 핀 2개 이상에서 `PIN_AMBIGUOUS`와 `:핀` QuickFix가 제품 경로에 닫히지 않았음을 red 기준선으로 남긴다.
- 비범위: LSP 구현, parser/type checker candidate solver, golden 갱신.

## 근거

- SSOT: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3430`
- 감사: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER2_V1.md:42`
- deepdive: `docs/context/reports/MUST_GAP_DEEPDIVE_A43_binding_ambiguity_lsp_quickfix_V1.md`

## 기대 red

이 pack은 실행용 golden이 아니며 `closure_claim: no`를 유지한다. `cases/c01_pin_ambiguous/input.ddn`은 후보 핀 2개 케이스, `cases/c02_at_misuse_pin_quickfix/input.ddn`은 `@` 오용 QuickFix 케이스다.
