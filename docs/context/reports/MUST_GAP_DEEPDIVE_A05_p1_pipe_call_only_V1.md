# MUST_GAP_DEEPDIVE_A05_p1_pipe_call_only_V1

    ## 대상

    - Track A item: `A05`
    - SSOT rule: §P1.2 호출식만 허용
    - SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5955`
    - Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER4_V1.md:20`
    - 산출물 성격: red conformance 심화조사

    ## 현재 재검증

    파이프 표면이 없으므로 stage를 호출식으로 제한하는 검사도 집행할 수 없다.

    ## 근거

    - SSOT PIPE-CALL-ONLY anchor: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5955
- 제품 Pipe token은 seed literal args에 쓰인다: tools/teul-cli/src/lang/parser.rs:5212, tools/teul-cli/src/lang/parser.rs:5246
- 일반 call arg parser는 존재하지만 파이프 stage 검사와 연결되지 않는다: tools/teul-cli/src/lang/parser.rs:5255, tools/teul-cli/src/lang/parser.rs:5350
- 관련 대표 red pack: pack/must_gap_a04_p1_pipe_surface_red_v1/README.md

    ## 판정

    - 현재 판정: red 유지 / A04 pack으로 대표
    - 언어 커널 구현 변경: 없음

- 관련 대표 red pack: `pack/must_gap_a04_p1_pipe_surface_red_v1`


    ## 결정 필요

    - stage 문법을 호출식으로만 제한할 진단 코드 이름 결정 필요.
