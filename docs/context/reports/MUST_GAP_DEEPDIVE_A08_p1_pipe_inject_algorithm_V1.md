# MUST_GAP_DEEPDIVE_A08_p1_pipe_inject_algorithm_V1

    ## 대상

    - Track A item: `A08`
    - SSOT rule: §P1.7 흐름값 주입 알고리즘
    - SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5991`
    - Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER4_V1.md:23`
    - 산출물 성격: red conformance 심화조사

    ## 현재 재검증

    흐름값 명시 pin/첫 미채움 필수핀/모호성 오류 알고리즘은 제품 pipe AST 부재 때문에 집행되지 않는다.

    ## 근거

    - SSOT PIPE-INJECT anchor: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5991
- SSOT injection fallback rule: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5996
- 일반 call arg parser는 pin/named/josa를 처리한다: tools/teul-cli/src/lang/parser.rs:5291, tools/teul-cli/src/lang/parser.rs:5350
- pipe stage AST/runtime이 없어 주입 알고리즘 적용 지점이 없다: docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER4_V1.md:23
- 관련 대표 red pack: pack/must_gap_a04_p1_pipe_surface_red_v1/README.md

    ## 판정

    - 현재 판정: red 유지 / A04 pack으로 대표
    - 언어 커널 구현 변경: 없음

- 관련 대표 red pack: `pack/must_gap_a04_p1_pipe_surface_red_v1`


    ## 결정 필요

    - 모호성 오류와 기본 주입 순서를 제품 PinSpec과 통합할지 결정 필요.
