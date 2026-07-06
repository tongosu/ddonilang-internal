# MUST_GAP_DEEPDIVE_A07_p1_block_tail_pipe_V1

    ## 대상

    - Track A item: `A07`
    - SSOT rule: §P1.6 `{ ... }해서` 파이프 꼬리
    - SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5982`
    - Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER4_V1.md:22`
    - 산출물 성격: red conformance 심화조사

    ## 현재 재검증

    block tail `}해서` parser/runtime 분기는 확인되지 않는다.

    ## 근거

    - SSOT block tail anchor: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5982
- 현재 Pipe token은 `|`뿐이다: tools/teul-cli/src/lang/token.rs:77, tools/teul-cli/src/lang/lexer.rs:252
- parser Pipe 사용 지점은 seed literal args다: tools/teul-cli/src/lang/parser.rs:5212, tools/teul-cli/src/lang/parser.rs:5246
- audit도 block tail `해서` parser/runtime 분기를 찾지 못했다: docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER4_V1.md:22
- 관련 대표 red pack: pack/must_gap_a04_p1_pipe_surface_red_v1/README.md

    ## 판정

    - 현재 판정: red 유지 / A04 pack으로 대표
    - 언어 커널 구현 변경: 없음

- 관련 대표 red pack: `pack/must_gap_a04_p1_pipe_surface_red_v1`


    ## 결정 필요

    - 토막 꼬리 `}해서`를 `}하고`/계약 표면과 같은 계층에서 처리할지 결정 필요.
