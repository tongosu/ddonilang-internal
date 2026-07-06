# MUST_GAP_DEEPDIVE_A37_word_ieumssi_operator_V1

## 대상

- Track A item: `A37`
- SSOT rule: `6.2.2 말 이음씨`
- SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2804`
- Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER2_V1.md:20`
- 산출물 성격: red conformance 심화조사

## 현재 재검증

SSOT는 식별자 이름을 연산자 자리로 쓰는 사용자 정의 말 이음씨를 언어 자체 기능으로 둔다. 현재 `teul-cli` 표현식 parser는 고정 precedence 함수 체인을 갖고 있으며, `이음씨` 정의/registry, word infix dispatch, 같은 스코프 이름 충돌 진단 경로는 확인되지 않는다.

## 근거

- SSOT 이음씨 정의 시작: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2780`
- 공통 정의 헤더 문법: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2796`
- 말 이음씨 시작과 설명: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2804`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2806`
- 말 이음씨 사용 예와 언어 자체 기능 선언: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2814`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2815`
- 같은 스코프 중복 정의는 모호성 오류여야 한다: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2816`
- 현재 parser는 `parse_logical_or`부터 `parse_postfix`까지 고정 precedence 함수 체인이다: `tools/teul-cli/src/lang/parser.rs:4777`, `tools/teul-cli/src/lang/parser.rs:4799`, `tools/teul-cli/src/lang/parser.rs:4821`, `tools/teul-cli/src/lang/parser.rs:4880`, `tools/teul-cli/src/lang/parser.rs:4902`, `tools/teul-cli/src/lang/parser.rs:4943`
- 직접 검색: `rg -n '이음씨|중위연산|operator registry|precedence registry' tools/teul-cli/src` = NO_MATCH
- 감사 행은 사용자 정의 이음씨/중위연산 선언을 찾지 못해 미구현 판정했다: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER2_V1.md:20`

## 판정

- 현재 판정: red 유지
- 언어 커널 구현 변경: 없음
- 신규 red pack: `pack/must_gap_a37_ieumssi_operator_red_v1`

## 결정 필요

- 사용자 정의 이음씨 registry를 parser symbol table에 둘지, type checker 이후 lowering 단계에 둘지 결정 필요.
- word operator와 기존 call-tail/bare call 해석의 충돌 우선순위를 확정해야 한다.
