# MUST_GAP_DEEPDIVE_A02_call_tail_resolve_unresolved_V1

    ## 대상

    - Track A item: `A02`
    - SSOT rule: CALL-TAIL-RESOLVE-01 해석 규칙
    - SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:825`
    - Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:21`
    - 산출물 성격: red conformance 심화조사

    ## 현재 재검증

    call-tail 후보 수집과 ambiguous 오류는 현재 브랜치에 착지했지만, 0개 후보 전용 unresolved 진단은 아직 보이지 않는다.

    ## 근거

    - CALL_TAILS 후보 집합: tools/teul-cli/src/lang/parser.rs:14, tools/teul-cli/src/runtime/eval.rs:30
- bare call-tail statement lowering: tools/teul-cli/src/lang/parser.rs:886, tools/teul-cli/src/lang/parser.rs:932
- runtime 후보 수집/ambiguous 분기: tools/teul-cli/src/runtime/eval.rs:2422, tools/teul-cli/src/runtime/eval.rs:2436
- 0개 후보는 전용 오류가 아니라 TypeMismatch로 떨어진다: tools/teul-cli/src/runtime/eval.rs:2442, tools/teul-cli/src/runtime/error.rs:221
- 기존 conformance pack은 ambiguous만 고정한다: pack/lang_kernel_v1_conformance/README.md:9, pack/lang_kernel_v1_conformance/golden.jsonl:2

    ## 판정

    - 현재 판정: 부분 해소 / unresolved red 유지
    - 언어 커널 구현 변경: 없음

- 신규 red pack: `pack/must_gap_a02_call_tail_resolve_unresolved_red_v1`


    ## 결정 필요

    - 0개 후보를 E_CALL_TAIL_UNRESOLVED로 고정할지, 현재 E_RUNTIME_TYPE_MISMATCH fallback을 유지할지 결정 필요.
