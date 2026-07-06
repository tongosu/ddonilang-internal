# MUST_GAP_DEEPDIVE_A20_nuance_token_combination_V1

    ## 대상

    - Track A item: `A20`
    - SSOT rule: 17.5 말결 결합 규칙
    - SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4137`
    - Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:27`
    - 산출물 성격: red conformance 심화조사

    ## 현재 재검증

    `말결값` builtin은 있지만 `$...` token sequence, 기본 0.5, 다중 token 마지막 적용, 부정어 반전 결합은 없다.

    ## 근거

    - SSOT nuance combination anchor: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4137
- 현재 builtin은 `말결값`이다: tools/teul-cli/src/runtime/eval.rs:5235, tools/teul-cli/src/runtime/eval.rs:5969
- 현재 weight mapping은 함수 하나로 닫혀 있다: tools/teul-cli/src/runtime/eval.rs:15617
- 기존 pack은 `말결값(문자열)` 결과를 검증한다: pack/gogae4_w39_nuance_weight/README.md:4, pack/gogae4_w39_nuance_weight/input.ddn:2
- 감사 행은 `$` 말결 token sequence/부정어 결합 부재로 미구현 판정했다: docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:27

    ## 판정

    - 현재 판정: red 유지
    - 언어 커널 구현 변경: 없음

- 신규 red pack: `pack/must_gap_a20_nuance_token_combination_red_v1`


    ## 결정 필요

    - 말결을 lexer token으로 둘지, builtin 함수 계층에 머물게 할지 결정 필요. 부정어 결합의 부호/스케일 정책도 필요하다.
