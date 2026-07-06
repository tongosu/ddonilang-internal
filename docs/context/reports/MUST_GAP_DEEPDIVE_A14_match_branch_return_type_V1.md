# MUST_GAP_DEEPDIVE_A14_match_branch_return_type_V1

    ## 대상

    - Track A item: `A14`
    - SSOT rule: 27.1.1.5 반환 타입 규칙
    - SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4756`
    - Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:48`
    - 산출물 성격: red conformance 심화조사

    ## 현재 재검증

    `~에 따라` expression이 없어 branch result type unification도 없다.

    ## 근거

    - SSOT return type anchor: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4756
- `고르기`는 statement body를 실행하는 구조다: tools/teul-cli/src/lang/parser.rs:4300, tools/teul-cli/src/lang/parser.rs:4461
- runtime도 `고르기` branch body 실행 중심이다: tools/teul-cli/src/runtime/eval.rs:1030, tools/teul-cli/src/runtime/eval.rs:1047
- 감사 행은 `~에 따라` expression 부재로 return type unification도 없음으로 판정했다: docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:48
- 관련 대표 red pack: pack/must_gap_a09_match_branch_e_ttara_red_v1/README.md

    ## 판정

    - 현재 판정: red 유지 / A09 pack으로 대표
    - 언어 커널 구현 변경: 없음

- 관련 대표 red pack: `pack/must_gap_a09_match_branch_e_ttara_red_v1`


    ## 결정 필요

    - match를 expression으로 둘 때 branch 결과 타입 통합 규칙 결정 필요.
