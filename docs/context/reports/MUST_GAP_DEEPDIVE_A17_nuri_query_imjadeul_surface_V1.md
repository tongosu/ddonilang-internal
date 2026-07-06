# MUST_GAP_DEEPDIVE_A17_nuri_query_imjadeul_surface_V1

    ## 대상

    - Track A item: `A17`
    - SSOT rule: 16.2 쿼리 표현식과 필터 `임자들`
    - SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4339`
    - Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:31`
    - 산출물 성격: red conformance 심화조사

    ## 현재 재검증

    core archetype/query API는 있으나 DDN 표면 `(조건...) 임자들` parser/runtime 연결은 없다.

    ## 근거

    - SSOT query expression anchor: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4339
- core archetype 구조는 존재한다: core/src/platform.rs:23, core/src/platform.rs:69
- core query API는 tag 기반 Vec<EntityId> 반환이다: core/src/platform.rs:129, core/src/platform.rs:615
- gogae3 내부는 core query API를 직접 호출한다: core/src/gogae3.rs:179, core/src/gogae3.rs:192
- 제품 parser/runtime에서 `임자들` 표면 근거는 감사 행 기준 없음: docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:31

    ## 판정

    - 현재 판정: red 유지
    - 언어 커널 구현 변경: 없음

- 신규 red pack: `pack/must_gap_a17_nuri_query_imjadeul_surface_red_v1`


    ## 결정 필요

    - 언어 표면 query를 core archetype API에 연결할지, 먼저 pack/spec로 더 나눌지 결정 필요.
