# MUST_GAP_DEEPDIVE_A35_goreumssi_tag_union_V1

## 대상

- Track A item: `A35`
- SSOT rule: `고름씨 정의`
- SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2649`
- Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:58`
- 산출물 성격: red conformance 심화조사

## 현재 재검증

SSOT는 `고름씨`를 유한/닫힌 태그 집합으로 정의하고, 모든 variant와 field type이 컴파일 타임에 확정되어야 한다고 정한다. 현재 `teul-cli`에는 `#atom` expression과 context tag 중복 일부 검사는 있지만, `고름씨` type declaration, closed variant registry, `(고름씨ID, 변형Index)` 런타임 표현 경로는 확인되지 않는다.

## 근거

- SSOT 고름씨 정의 시작: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2649`
- 고름씨는 유한/닫힌 tag union이다: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2651`
- variant와 field type compile-time 확정 요구: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2652`
- 현재 `SeedKind::from_name` 정본 kind는 `셈씨/움직씨`만 인식한다: `tools/teul-cli/src/lang/ast.rs:23`, `tools/teul-cli/src/lang/ast.rs:26`, `tools/teul-cli/src/lang/ast.rs:27`
- 현재 atom 값은 lexer/parser/AST에 있다: `tools/teul-cli/src/lang/token.rs:10`, `tools/teul-cli/src/lang/lexer.rs:514`, `tools/teul-cli/src/lang/ast.rs:304`, `tools/teul-cli/src/lang/parser.rs:5107`
- runtime은 `Expr::Atom`을 문자열 값으로 평가한다: `tools/teul-cli/src/runtime/eval.rs:2115`
- 감사 행은 `#atom`은 있으나 `고름씨` 타입 surface가 없어 미구현 판정했다: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:58`

## 판정

- 현재 판정: red 유지
- 언어 커널 구현 변경: 없음
- 신규 red pack: `pack/must_gap_a35_goreumssi_tag_union_red_v1`

## 결정 필요

- `고름씨` runtime 표현을 문자열 atom으로 유지할지, SSOT의 `(고름씨ID, 변형Index)` 정수쌍 표현으로 전환할지 결정 필요.
- 기존 context tag 중복 검사와 closed union registry의 책임 경계를 확정해야 한다.
