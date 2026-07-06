# MUST_GAP_DEEPDIVE_A31_jamo_reserved_identifier_V1

## 대상

- Track A item: `A31`
- SSOT rule: `시스템 예약 자음 식별자`
- SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1721`
- Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:38`
- 산출물 성격: red conformance 심화조사

## 현재 재검증

SSOT는 단자음/자음식별자를 시스템 root alias 용도로 예약하고, 사용자가 씨앗/그릇/타입/핀 이름으로 정의하는 것을 금지한다. 현재 `teul-cli` lexer/parser/runtime에서 자음식별자 예약 검사, SystemRootAlias 표, `E_IDENT_JAMO_RESERVED` 진단 경로는 확인되지 않는다.

## 근거

- SSOT 자음 식별자 규칙 시작: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1721`
- 자음식별자 정의와 문자 목록: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1726`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1727`
- 사용자 정의 금지와 예시 진단: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1728`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1729`
- 허용 위치는 `.` 접근점 + SystemRootAlias 등록 둘 다 필요하다: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1730`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1731`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1732`
- 현재 lexer identifier 판정은 alphabetic/numeric 기반이며 자음 예약 분기를 갖지 않는다: `tools/teul-cli/src/lang/lexer.rs:1082`, `tools/teul-cli/src/lang/lexer.rs:1086`
- 직접 검색: `rg -n 'Jamo|jamo|자음|단자음|E_IDENT_JAMO|SystemRootAlias' tools/teul-cli/src/lang tools/teul-cli/src/runtime` = NO_MATCH
- 감사 행은 자음 예약 검사를 찾지 못해 미구현 판정했다: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:38`

## 판정

- 현재 판정: red 유지
- 언어 커널 구현 변경: 없음
- 신규 red pack: `pack/must_gap_a31_jamo_reserved_identifier_red_v1`

## 결정 필요

- 자음식별자 금지를 lexer fatal로 둘지, parser/lint 단계에서 이름 선언 위치별로 집행할지 결정 필요.
- SystemRootAlias 표의 소유 위치와 확장 정책을 TERM-MAP/NAME-LINT와 어떻게 연결할지 결정해야 한다.
