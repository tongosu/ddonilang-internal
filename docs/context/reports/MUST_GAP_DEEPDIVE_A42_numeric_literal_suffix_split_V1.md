# MUST_GAP_DEEPDIVE_A42_numeric_literal_suffix_split_V1

## 대상

- Track A item: `A42`
- SSOT rule: `10.4.1 숫자 리터럴 접미 분리`
- SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3291`
- Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER2_V1.md:39`
- 산출물 성격: red conformance 심화조사

## 현재 재검증

SSOT는 `100cm를`처럼 숫자 리터럴 뒤 접미가 공백 없이 붙는 경우 단위 접미를 먼저 분리하고, 단위가 아니면 조사 분리를 시도해야 한다고 정한다. 현재 `teul-cli` lexer는 숫자 뒤 식별자 시작 문자가 오면 `마디`만 주기 훅 예외로 허용하고 나머지는 `BadIdentStart`로 거부한다. parser의 단위 postfix도 `100@cm`처럼 명시 `@`가 있는 경로에 한정되어, SSOT의 일반 숫자 리터럴 접미 분리 알고리즘은 제품 경로에 확인되지 않는다.

## 근거

- SSOT 숫자 리터럴 접미 분리 시작: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3291`
- SSOT 예시 `100을`, `100cm를`: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3294`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3295`
- SSOT 알고리즘: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3299`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3300`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3301`
- 감사 행은 일반 숫자 접미 분리/진단 구현 근거 부재로 미구현 판정했다: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER2_V1.md:39`
- 현재 숫자 lexer 시작: `tools/teul-cli/src/lang/lexer.rs:407`
- 현재 숫자 뒤 식별자 접미는 `마디`만 예외로 허용한다: `tools/teul-cli/src/lang/lexer.rs:435`, `tools/teul-cli/src/lang/lexer.rs:436`, `tools/teul-cli/src/lang/lexer.rs:437`
- 그 외 숫자 뒤 식별자 시작은 `BadIdentStart`로 거부된다: `tools/teul-cli/src/lang/lexer.rs:439`
- 현재 number literal parser는 `parse_unit_postfix`만 연결한다: `tools/teul-cli/src/lang/parser.rs:5066`, `tools/teul-cli/src/lang/parser.rs:5070`
- 현재 unit postfix는 명시 `@` 토큰이 없으면 종료한다: `tools/teul-cli/src/lang/parser.rs:5918`, `tools/teul-cli/src/lang/parser.rs:5919`, `tools/teul-cli/src/lang/parser.rs:5922`

## 판정

- 현재 판정: red 유지
- 언어 커널 구현 변경: 없음
- 신규 red pack: `pack/must_gap_a42_numeric_literal_suffix_split_red_v1`

## 결정 필요

- 숫자 뒤 ASCII 단위(`cm`, `m`, `s`)와 한글 조사(`를`, `을` 등)를 lexer token 내부에서 분해할지, parser suffix-chain 단계에서 원문 span을 재분석할지 결정 필요.
- `100cm를`의 정본을 `100@cm~를`처럼 explicit 접착자로 canonicalize할지, AST에 원접미 chain을 보존할지 결정 필요.
- 단위 후보가 스코프 식별자와 충돌할 때의 오류 코드와 QuickFix 문구가 필요하다.
