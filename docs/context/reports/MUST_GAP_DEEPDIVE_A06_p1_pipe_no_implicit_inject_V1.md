# MUST_GAP_DEEPDIVE_A06_p1_pipe_no_implicit_inject_V1

    ## 대상

    - Track A item: `A06`
    - SSOT rule: §P1.3 암묵 주입 금지
    - SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5960`
    - Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER4_V1.md:21`
    - 산출물 성격: red conformance 심화조사

    ## 현재 재검증

    일반 call arg binding은 있으나 `해서` 흐름값의 암묵 주입 금지 알고리즘은 제품 경로에 없다.

    ## 근거

    - SSOT PIPE-NO-IMPLICIT-INJECT anchor: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5960
- 일반 ArgBinding은 josa/pin/named argument를 보존한다: tools/teul-cli/src/lang/parser.rs:5255, tools/teul-cli/src/lang/parser.rs:5291
- named/pin arg 처리 자체는 존재한다: tools/teul-cli/src/lang/parser.rs:5330, tools/teul-cli/src/lang/parser.rs:5350
- 하지만 `해서` pipe stage가 없어 이 규칙을 적용할 대상 AST가 없다: docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER4_V1.md:21
- 관련 대표 red pack: pack/must_gap_a04_p1_pipe_surface_red_v1/README.md

    ## 판정

    - 현재 판정: red 유지 / A04 pack으로 대표
    - 언어 커널 구현 변경: 없음

- 관련 대표 red pack: `pack/must_gap_a04_p1_pipe_surface_red_v1`


    ## 결정 필요

    - flow value injection을 명시 pin 전용으로 닫을지, 위치 fallback을 허용할지 SSOT §P1.7과 함께 결정 필요.
