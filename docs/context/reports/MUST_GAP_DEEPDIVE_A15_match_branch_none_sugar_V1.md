# MUST_GAP_DEEPDIVE_A15_match_branch_none_sugar_V1

    ## 대상

    - Track A item: `A15`
    - SSOT rule: 27.1.1.6 `없으면` sugar
    - SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4771`
    - Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:49`
    - 산출물 성격: red conformance 심화조사

    ## 현재 재검증

    `X 없으면 Y` option coalesce sugar는 제품 lang/runtime에서 확인되지 않는다.

    ## 근거

    - SSOT none sugar anchor: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4771
- SSOT sugar 설명: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4774
- 값 모델의 None은 존재한다: tools/teul-cli/src/core/value.rs:255
- 하지만 `없으면`/Coalesce parser/runtime 구현 근거는 감사 행 기준 없음: docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:49
- 관련 대표 red pack input이 `없으면`도 포함한다: pack/must_gap_a09_match_branch_e_ttara_red_v1/cases/c01_e_ttara_match_surface/input.ddn

    ## 판정

    - 현재 판정: red 유지 / A09 pack으로 대표
    - 언어 커널 구현 변경: 없음

- 관련 대표 red pack: `pack/must_gap_a09_match_branch_e_ttara_red_v1`


    ## 결정 필요

    - `없으면`을 match sugar로 낮출지 독립 coalesce operator로 둘지 결정 필요.
