# MUST_GAP_DEEPDIVE_A38_symbol_ieumssi_operator_V1

## 대상

- Track A item: `A38`
- SSOT rule: `6.2.3 기호 이음씨`
- SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2818`
- Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER2_V1.md:21`
- 산출물 성격: red conformance 심화조사

## 현재 재검증

SSOT는 기호를 operator 자리로 쓰는 사용자 정의 기호 이음씨와 정의 헤더 전용 말별칭을 허용한다. 현재 `teul-cli`에는 builtin 기호 토큰과 산술/비교 precedence parser는 있지만, 사용자 정의 기호 이음씨 선언, alias metadata, expression dispatch registry는 확인되지 않는다.

## 근거

- SSOT 기호 이음씨 시작: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2818`
- OperatorSymbol 설명: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2820`
- 기호 이음씨 정의 예시: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2823`
- 말별칭 정의 헤더 예시: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2831`
- `+~더하기`는 정의 헤더에서만 허용되고 canon 출력에서 제거되어야 한다: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2836`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2838`
- 현재 token enum/lexer는 고정 토큰 집합을 가진다: `tools/teul-cli/src/lang/token.rs:74`, `tools/teul-cli/src/lang/lexer.rs:209`, `tools/teul-cli/src/lang/lexer.rs:230`
- 현재 parser는 고정 additive/multiplicative precedence로 `+`, `*` 등을 처리한다: `tools/teul-cli/src/lang/parser.rs:4880`, `tools/teul-cli/src/lang/parser.rs:4884`, `tools/teul-cli/src/lang/parser.rs:4902`, `tools/teul-cli/src/lang/parser.rs:4906`
- 감사 행은 사용자 정의 기호 이음씨 registry 부재로 미구현 판정했다: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER2_V1.md:21`

## 판정

- 현재 판정: red 유지
- 언어 커널 구현 변경: 없음
- 관련 red pack: `pack/must_gap_a37_ieumssi_operator_red_v1`

## 결정 필요

- builtin 기호와 사용자 정의 기호의 shadowing/override 허용 범위를 결정해야 한다.
- `+~더하기` alias metadata를 canon artifact에 보존할지, type registry에만 보존할지 결정 필요.
