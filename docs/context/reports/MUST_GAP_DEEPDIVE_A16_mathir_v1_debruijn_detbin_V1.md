# MUST_GAP_DEEPDIVE_A16_mathir_v1_debruijn_detbin_V1

    ## 대상

    - Track A item: `A16`
    - SSOT rule: §M1.5 MathIR v1 / De Bruijn / DetBin
    - SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5339`
    - Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:60`
    - 산출물 성격: red conformance 심화조사

    ## 현재 재검증

    수식 parser/evaluator와 formatter는 있으나 MathIR v1, De Bruijn index, MathIRDetBin 직렬화는 제품 경로에서 닫히지 않았다.

    ## 근거

    - SSOT MathIR anchor: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5339
- 제품 teul-cli formula 내부 AST는 FormulaAst다: tools/teul-cli/src/runtime/formula.rs:63
- format_formula_body는 FormulaAst를 text로 format한다: tools/teul-cli/src/runtime/formula.rs:68, tools/teul-cli/src/runtime/formula.rs:119
- parser는 #ascii/#ascii1 formula head만 제품 teul-cli 경로에서 직접 다룬다: tools/teul-cli/src/lang/parser.rs:5718, tools/teul-cli/src/lang/parser.rs:5795
- DetBin 언급은 state/bogae 쪽 일반 계약 근거이며 MathIRDetBin 구현 근거가 아니다: core/src/platform.rs:680

    ## 판정

    - 현재 판정: red 유지
    - 언어 커널 구현 변경: 없음

- 신규 red pack: `pack/must_gap_a16_mathir_v1_debruijn_detbin_red_v1`


    ## 결정 필요

    - MathIR node set, binder normalization, DetBin byte layout을 TOOLCHAIN/제품 경로 중 어디서 먼저 고정할지 결정 필요.
