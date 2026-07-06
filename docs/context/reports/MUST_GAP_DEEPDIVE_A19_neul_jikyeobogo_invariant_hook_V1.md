# MUST_GAP_DEEPDIVE_A19_neul_jikyeobogo_invariant_hook_V1

    ## 대상

    - Track A item: `A19`
    - SSOT rule: 16.2 `늘지켜보고` 문법
    - SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4039`
    - Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:22`
    - 산출물 성격: red conformance 심화조사

    ## 현재 재검증

    계약/rollback 시스템은 있으나 commit 직전 invariant hook `늘지켜보고` 표면은 제품 경로에 없다.

    ## 근거

    - SSOT invariant hook anchor: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4039
- SSOT commit 직전 stage 설명: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4054
- 기존 계약 parser는 별도 contract stmt다: tools/teul-cli/src/lang/parser.rs:4615, tools/teul-cli/src/lang/parser.rs:4738
- 기존 contract frame rollback/commit은 runtime에 있다: tools/teul-cli/src/runtime/eval.rs:1861, tools/teul-cli/src/runtime/eval.rs:1889
- 감사 행은 `늘지켜보고` token/parser 분기 없음으로 미구현 판정했다: docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:22

    ## 판정

    - 현재 판정: red 유지
    - 언어 커널 구현 변경: 없음

- 신규 red pack: `pack/must_gap_a19_neul_jikyeobogo_invariant_hook_red_v1`


    ## 결정 필요

    - `늘지켜보고`를 계약 시스템에 낮출지 별도 commit-stage hook으로 둘지 결정 필요. `덧댐거부` 감사 이벤트도 별도 결정 필요.
