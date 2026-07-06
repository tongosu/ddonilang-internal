# MUST_GAP_DEEPDIVE_A39_extended_operator_symbols_V1

## 대상

- Track A item: `A39`
- SSOT rule: `6.2.4 확장 이음기호 집합`
- SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2842`
- Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER2_V1.md:22`
- 산출물 성격: red conformance 심화조사

## 현재 재검증

SSOT는 EXT_OPCHAR 후보 문자 집합에서 1-3글자 조합의 확장 이음기호를 만들고, lexer가 최장 일치로 token화해야 한다고 정한다. 현재 `teul-cli` lexer/token에는 고정 token 분기만 있고, EXT_OPCHAR class, longest-match operator symbol scanner, 정의 전 “빈 기호” registry 경로는 확인되지 않는다.

## 근거

- SSOT 확장 이음기호 시작: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2842`
- 고정 후보 문자 집합/1-3글자/최장 일치 요구: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2845`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2847`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2848`
- 정의된 경우에만 의미가 있다는 요구: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2849`
- EXT_OPCHAR 목록: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2853`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2854`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2855`
- 예약 토큰 금지 목록: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2861`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2864`
- 현재 lexer는 `+`, `-`, `*`, `/`, `|`, 비교/화살표 등 고정 분기를 둔다: `tools/teul-cli/src/lang/lexer.rs:209`, `tools/teul-cli/src/lang/lexer.rs:229`, `tools/teul-cli/src/lang/lexer.rs:230`, `tools/teul-cli/src/lang/lexer.rs:252`, `tools/teul-cli/src/lang/lexer.rs:296`, `tools/teul-cli/src/lang/lexer.rs:323`
- 직접 검색: `rg -n 'EXT_OPCHAR|OperatorSymbol|extended operator|이음기호' tools/teul-cli/src` = NO_MATCH
- 감사 행은 확장 이음기호 token class 부재로 미구현 판정했다: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER2_V1.md:22`

## 판정

- 현재 판정: red 유지
- 언어 커널 구현 변경: 없음
- 관련 red pack: `pack/must_gap_a37_ieumssi_operator_red_v1`

## 결정 필요

- EXT_OPCHAR scanner가 기존 sym3/token dispatch보다 먼저 실행될지, reserved token을 먼저 차단할지 결정 필요.
- Unicode variation selector 정규화/오류 정책을 제품 진단으로 확정해야 한다.
