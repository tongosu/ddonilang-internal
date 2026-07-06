# MUST_GAP_DEEPDIVE_A04_p1_pipe_surface_V1

    ## 대상

    - Track A item: `A04`
    - SSOT rule: §P1 파이프(해서)
    - SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5947`
    - Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER4_V1.md:19`
    - 산출물 성격: red conformance 심화조사

    ## 현재 재검증

    `해서` 파이프 표면/AST/runtime은 제품 경로에서 확인되지 않는다. 현재 `Pipe` token은 `|`이고 seed literal parameter에만 쓰인다.

    ## 근거

    - SSOT §P1 시작: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5947
- Pipe token은 `|`이다: tools/teul-cli/src/lang/token.rs:77, tools/teul-cli/src/lang/lexer.rs:252
- parser의 Pipe 사용은 seed literal args 쪽이다: tools/teul-cli/src/lang/parser.rs:5212, tools/teul-cli/src/lang/parser.rs:5246
- audit도 제품 parser/runtime에서 `해서` pipe AST/평가 경로를 찾지 못했다: docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER4_V1.md:19
- inventory의 landed 표기는 별도 inventory drift 후보로 보이며 제품 file:line은 canon helper만 가리킨다: docs/context/reports/SSOT_LANG_INVENTORY_V1.md:385

    ## 판정

    - 현재 판정: red 유지
    - 언어 커널 구현 변경: 없음

- 신규 red pack: `pack/must_gap_a04_p1_pipe_surface_red_v1`


    ## 결정 필요

    - 파이프 표면을 call-tail/흐름값 규칙과 어느 계층에서 통합할지 결정 필요.
