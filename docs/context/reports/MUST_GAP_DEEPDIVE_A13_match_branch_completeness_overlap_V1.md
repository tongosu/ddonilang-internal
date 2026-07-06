# MUST_GAP_DEEPDIVE_A13_match_branch_completeness_overlap_V1

    ## 대상

    - Track A item: `A13`
    - SSOT rule: 27.1.1.4 완전성/중복 규칙
    - SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4740`
    - Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:47`
    - 산출물 성격: red conformance 심화조사

    ## 현재 재검증

    `고르기`의 completion marker 일부는 있으나 `~에 따라` variant exhaustiveness/overlap/order 검사는 없다.

    ## 근거

    - SSOT completeness anchor: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4740
- `고르기` completion marker parser는 존재한다: tools/teul-cli/src/lang/parser.rs:4244, tools/teul-cli/src/lang/parser.rs:4339
- `고르기` runtime은 첫 참 branch 실행 구조다: tools/teul-cli/src/runtime/eval.rs:1030, tools/teul-cli/src/runtime/eval.rs:1047
- 감사 행은 `~에 따라` variant completeness/overlap 검사 없음으로 판정했다: docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:47
- 관련 대표 red pack: pack/must_gap_a09_match_branch_e_ttara_red_v1/README.md

    ## 판정

    - 현재 판정: red 유지 / A09 pack으로 대표
    - 언어 커널 구현 변경: 없음

- 관련 대표 red pack: `pack/must_gap_a09_match_branch_e_ttara_red_v1`


    ## 결정 필요

    - 고름씨/옵션 variant exhaustiveness와 중복/순서 진단 정책 결정 필요.
