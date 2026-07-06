# MUST_GAP_DEEPDIVE_A24_josa_reserved_identifier_V1

## 대상

- Track A item: `A24`
- SSOT rule: `NAMING-LINT 1) 금지(예약)`
- SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6976`
- Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER4_V1.md:55`
- 산출물 성격: red conformance 심화조사

## 현재 재검증

SSOT는 `이, 가, 을, 를, ...` 같은 조사별칭 자체를 식별자로 사용할 수 없다고 정한다. 현재 `teul-cli` lexer는 명시 `~`를 만났을 때만 조사 후보를 읽고 `TokenKind::Josa`로 canonicalize한다. bare 조사 단독 identifier를 예약어로 막는 lint/parse diagnostic 경로는 확인되지 않는다.

## 근거

- SSOT NAMING-LINT 시작: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6971`
- 조사 단독 금지 MUST: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6976`
- 금지 대상 기본 목록: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6977`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6978`
- 현재 lexer는 `~` 입력에서만 `read_josa`로 진입한다: `tools/teul-cli/src/lang/lexer.rs:356`
- `read_josa`는 `~` 뒤의 text가 dialect josa이면 `TokenKind::Josa`를 만든다: `tools/teul-cli/src/lang/lexer.rs:614`, `tools/teul-cli/src/lang/lexer.rs:633`, `tools/teul-cli/src/lang/lexer.rs:635`
- AST에는 josa list/argument suffix는 있지만 bare identifier 예약 금지 전용 진단은 확인되지 않는다: `tools/teul-cli/src/lang/ast.rs:60`, `tools/teul-cli/src/lang/ast.rs:367`
- 감사 행은 bare 조사 단독 identifier 금지 진단 부재로 미구현 판정했다: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER4_V1.md:55`

## 판정

- 현재 판정: red 유지
- 언어 커널 구현 변경: 없음
- 신규 red pack: `pack/must_gap_a24_josa_reserved_identifier_red_v1`

## 결정 필요

- bare 조사 단독 금지를 lexer 단계 fatal로 둘지, parser/lint 단계 diagnostic으로 둘지 결정 필요.
- 금지 목록 확장 시 Minor만 허용한다는 SSOT 정책을 제품 config/registry에 어떻게 반영할지 결정 필요.
