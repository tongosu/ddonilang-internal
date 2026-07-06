# MUST_GAP_DEEPDIVE_A11_match_branch_binding_scope_V1

    ## 대상

    - Track A item: `A11`
    - SSOT rule: 27.1.1.2 바인딩/스코프 규칙
    - SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4712`
    - Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:45`
    - 산출물 성격: red conformance 심화조사

    ## 현재 재검증

    `~에 따라` AST/패턴 binding 자체가 없어 payload binding scope도 집행되지 않는다.

    ## 근거

    - SSOT binding/scope anchor: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4712
- 현재 구현된 유사 분기는 `고르기` statement다: tools/teul-cli/src/lang/parser.rs:4199
- `고르기` branch는 condition expr와 body block만 가진다: tools/teul-cli/src/lang/parser.rs:4278, tools/teul-cli/src/lang/parser.rs:4360
- 감사 행도 `~에 따라` AST/패턴 binding 부재를 근거로 미구현 판정했다: docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:45
- 관련 대표 red pack: pack/must_gap_a09_match_branch_e_ttara_red_v1/README.md

    ## 판정

    - 현재 판정: red 유지 / A09 pack으로 대표
    - 언어 커널 구현 변경: 없음

- 관련 대표 red pack: `pack/must_gap_a09_match_branch_e_ttara_red_v1`


    ## 결정 필요

    - 패턴 payload binding을 branch-local scope로 제한하는 symbol table 규칙 결정 필요.
