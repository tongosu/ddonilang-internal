# MUST_GAP_DEEPDIVE_A12_match_branch_type_rules_V1

    ## 대상

    - Track A item: `A12`
    - SSOT rule: 27.1.1.3 타입 규칙
    - SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4727`
    - Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:46`
    - 산출물 성격: red conformance 심화조사

    ## 현재 재검증

    `~에 따라` 대상 갈래형/type checker가 없어 불가능 패턴 오류도 집행되지 않는다.

    ## 근거

    - SSOT type rule anchor: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4727
- 값 모델에는 None/Atom이 있으나 match type checker와 연결되지 않는다: tools/teul-cli/src/core/value.rs:255, tools/teul-cli/src/lang/ast.rs:298
- `고르기` parser는 조건식 기반 statement라 갈래형 pattern matching이 아니다: tools/teul-cli/src/lang/parser.rs:4278, tools/teul-cli/src/lang/parser.rs:4389
- 감사 행은 `~에 따라` type check 경로 없음으로 판정했다: docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:46
- 관련 대표 red pack: pack/must_gap_a09_match_branch_e_ttara_red_v1/README.md

    ## 판정

    - 현재 판정: red 유지 / A09 pack으로 대표
    - 언어 커널 구현 변경: 없음

- 관련 대표 red pack: `pack/must_gap_a09_match_branch_e_ttara_red_v1`


    ## 결정 필요

    - 옵션/참거짓/고름씨 match 대상 타입 집합과 불가능 패턴 진단을 확정해야 한다.
