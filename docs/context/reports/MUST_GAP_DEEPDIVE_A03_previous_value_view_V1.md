# MUST_GAP_DEEPDIVE_A03_previous_value_view_V1

    ## 대상

    - Track A item: `A03`
    - SSOT rule: 7.2 이전값보기
    - SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2970`
    - Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER2_V1.md:26`
    - 산출물 성격: red conformance 심화조사

    ## 현재 재검증

    `이전값보기` 표면은 현재 제품 경로에서 찾지 못했다. 내부 rollback/edge detector용 prev_value 변수는 있으나 사용자 표면 구현이 아니다.

    ## 근거

    - SSOT 표면 예시: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2978, docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2981
- 제품 검색 결과는 internal previous-state 변수뿐이다: tools/teul-cli/src/runtime/eval.rs:752, tools/teul-cli/src/runtime/eval.rs:804
- 계약 rollback/open rollback prev_value는 사용자 표면이 아니다: tools/teul-cli/src/runtime/eval.rs:1192, tools/teul-cli/src/runtime/eval.rs:6735
- D55 설계 방향은 proposal에만 있다: docs/context/proposals/PROPOSAL_FLOW_HOOK_IMPLEMENTATION_DECISIONS_D51_D58_20260706.md:31

    ## 판정

    - 현재 판정: red 유지
    - 언어 커널 구현 변경: 없음

- 신규 red pack: `pack/must_gap_a03_previous_value_view_red_v1`


    ## 결정 필요

    - D55처럼 참조된 대상만 저장하는 스냅샷 범위를 제품 경로에 넣을지 결정 필요. 이번 작업에서는 구현하지 않는다.
