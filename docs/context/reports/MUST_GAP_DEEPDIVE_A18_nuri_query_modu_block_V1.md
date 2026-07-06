# MUST_GAP_DEEPDIVE_A18_nuri_query_modu_block_V1

    ## 대상

    - Track A item: `A18`
    - SSOT rule: 16.3 군집 실행 블록 `모두`
    - SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4356`
    - Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:32`
    - 산출물 성격: red conformance 심화조사

    ## 현재 재검증

    query 결과 대상 `모두`/`첫째`/`마지막`/`개수` 군집 실행 표면은 제품 parser/runtime에서 확인되지 않는다.

    ## 근거

    - SSOT group block anchor: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4356
- 일반 foreach/반복 파서는 있으나 query-group `모두` 전용이 아니다: tools/teul-cli/src/lang/parser.rs:513, tools/teul-cli/src/lang/parser.rs:529
- core query API는 존재하지만 언어 표면과 연결되지 않는다: core/src/platform.rs:129, core/src/platform.rs:615
- 감사 행은 query loop 표면 근거 없음으로 미구현 판정했다: docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:32
- 관련 대표 red pack: pack/must_gap_a17_nuri_query_imjadeul_surface_red_v1/README.md

    ## 판정

    - 현재 판정: red 유지 / A17 pack으로 대표
    - 언어 커널 구현 변경: 없음

- 관련 대표 red pack: `pack/must_gap_a17_nuri_query_imjadeul_surface_red_v1`


    ## 결정 필요

    - `모두 {}`를 기존 `~에 대해` sugar로 낮출지, query executor를 별도로 둘지 결정 필요.
