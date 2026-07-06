# MUST_GAP_DEEPDIVE_A10_match_branch_syntax_V1

    ## 대상

    - Track A item: `A10`
    - SSOT rule: 27.1.1.1 `E에 따라 { ... }` 문법
    - SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4675`
    - Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:44`
    - 산출물 성격: red conformance 심화조사

    ## 현재 재검증

    `E에 따라 { 패턴이면 몸 ... }` 문법은 별도 parser branch가 없다. 현재 `고르기:`는 조건문 statement 계열이다.

    ## 근거

    - SSOT syntax anchor: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4675
- `고르기` parser entry: tools/teul-cli/src/lang/parser.rs:4199
- `고르기` branch는 condition expr를 파싱한다: tools/teul-cli/src/lang/parser.rs:4278, tools/teul-cli/src/lang/parser.rs:4389
- match syntax 감사 행은 `~에 따라` AST/패턴 문법 없음으로 판정했다: docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:44
- 관련 대표 red pack: pack/must_gap_a09_match_branch_e_ttara_red_v1/README.md

    ## 판정

    - 현재 판정: red 유지 / A09 pack으로 대표
    - 언어 커널 구현 변경: 없음

- 관련 대표 red pack: `pack/must_gap_a09_match_branch_e_ttara_red_v1`


    ## 결정 필요

    - 패턴 문법과 branch body expression/statement 형태를 확정해야 한다.
