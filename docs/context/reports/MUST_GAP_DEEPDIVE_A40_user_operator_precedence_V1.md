# MUST_GAP_DEEPDIVE_A40_user_operator_precedence_V1

## 대상

- Track A item: `A40`
- SSOT rule: `6.2.5 사용자 정의 이음씨 우선순위`
- SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2868`
- Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER2_V1.md:23`
- 산출물 성격: red conformance 심화조사

## 현재 재검증

SSOT는 사용자 정의 이음씨가 기본 우선순위 5를 갖고, 정의 헤더 앞의 `우선순위(N)`로 3..13 범위 안에서 명시 우선순위를 선언할 수 있다고 정한다. 현재 `teul-cli` 표현식 parser는 builtin operator를 고정 precedence 함수 체인으로 처리하며, 사용자 precedence registry, `우선순위(N)` 정의 헤더 parser, 범위 검증은 확인되지 않는다.

## 근거

- SSOT 사용자 우선순위 시작: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2868`
- 기본 우선순위와 명시 문법: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2870`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2871`
- 허용 범위 3..13: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2872`
- 명시 우선순위 예시: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2877`
- 현재 parser fixed chain: `tools/teul-cli/src/lang/parser.rs:4777`, `tools/teul-cli/src/lang/parser.rs:4799`, `tools/teul-cli/src/lang/parser.rs:4821`, `tools/teul-cli/src/lang/parser.rs:4880`, `tools/teul-cli/src/lang/parser.rs:4902`, `tools/teul-cli/src/lang/parser.rs:4925`, `tools/teul-cli/src/lang/parser.rs:4943`
- 직접 검색: `rg -n 'precedence registry|operator registry|우선순위|이음씨' tools/teul-cli/src` = NO_MATCH
- 감사 행은 사용자 precedence registry 부재로 미구현 판정했다: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER2_V1.md:23`

## 판정

- 현재 판정: red 유지
- 언어 커널 구현 변경: 없음
- 관련 red pack: `pack/must_gap_a37_ieumssi_operator_red_v1`

## 결정 필요

- 사용자 operator precedence를 parse-time에 반영할지, parse 후 Pratt/precedence 재구성 단계로 둘지 결정 필요.
- 같은 우선순위/결합성 기본값과 충돌 diagnostic을 확정해야 한다.
