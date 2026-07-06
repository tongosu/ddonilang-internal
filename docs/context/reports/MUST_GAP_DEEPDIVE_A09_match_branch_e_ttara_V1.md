# MUST_GAP_DEEPDIVE_A09_match_branch_e_ttara_V1

    ## 대상

    - Track A item: `A09`
    - SSOT rule: 27.1.1 갈래 분기 `~에 따라`
    - SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4668`
    - Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:43`
    - 산출물 성격: red conformance 심화조사

    ## 현재 재검증

    `~에 따라` match expression은 제품 parser/runtime에서 찾지 못했다. 현재 유사 분기는 `고르기` statement이다.

    ## 근거

    - SSOT match anchor: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4668
- 현재 구현된 다중 분기는 `고르기` statement parser다: tools/teul-cli/src/lang/parser.rs:528, tools/teul-cli/src/lang/parser.rs:4199
- `고르기` branch parser는 조건식 기반이다: tools/teul-cli/src/lang/parser.rs:4278, tools/teul-cli/src/lang/parser.rs:4389
- runtime도 `고르기` 계열 테스트/실행만 갖고 match expression 근거는 없다: tools/teul-cli/src/runtime/eval.rs:17053
- inventory도 `~에 따라`는 절 반영/소거 docs-first로 따로 표시한다: docs/context/reports/SSOT_LANG_INVENTORY_V1.md:339

    ## 판정

    - 현재 판정: red 유지
    - 언어 커널 구현 변경: 없음

- 신규 red pack: `pack/must_gap_a09_match_branch_e_ttara_red_v1`


    ## 결정 필요

    - `고르기`와 별도 expression match로 둘지, sugar로 낮출지 결정 필요.
