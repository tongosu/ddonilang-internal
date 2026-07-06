# MUST_GAP_DEEPDIVE_A21_nuance_54_rules_V1

## 대상

- Track A item: `A21`
- SSOT rule: `5.4 규칙` 말결 없음/중복/부정 결합
- SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6359`
- Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER4_V1.md:32`
- 산출물 성격: red conformance 심화조사

## 현재 재검증

SSOT는 말결 토큰이 없을 때 기본값 0.5, 여러 말결 토큰이 있을 때 마지막 토큰 적용, 부정어 결합 시 부호 반전을 요구한다. 현재 `teul-cli` 제품 경로에는 문자열 builtin `말결값`과 논리 builtin `아님`은 있지만, `$...` 말결 token sequence를 문장 단위로 수집해 5.4 규칙을 적용하는 lexer/parser/runtime 경로는 확인되지 않는다.

## 근거

- SSOT 5.4 규칙 시작: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6359`
- 기본 0.5/마지막 token/부정 결합 요구: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6361`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6362`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6363`
- 현재 runtime builtin은 문자열 입력의 `말결값`이다: `tools/teul-cli/src/runtime/eval.rs:5235`
- builtin 허용 목록에는 `말결값`과 `아님`/`아니다`가 분리되어 있다: `tools/teul-cli/src/runtime/eval.rs:5969`, `tools/teul-cli/src/runtime/eval.rs:5995`
- `$` 말결 token 전용 lexer/parser 분기는 확인되지 않는다. 현재 단일 문자 dispatch는 `|`, `(`, `[`, `{`, `:` 등만 직접 token화한다: `tools/teul-cli/src/lang/lexer.rs:209`, `tools/teul-cli/src/lang/lexer.rs:252`, `tools/teul-cli/src/lang/lexer.rs:355`
- 감사 행은 5.4 규칙을 미구현으로 판정했다: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER4_V1.md:32`

## 판정

- 현재 판정: red 유지
- 언어 커널 구현 변경: 없음
- 관련 red pack: `pack/must_gap_a20_nuance_token_combination_red_v1`

## 결정 필요

- `$...`를 lexer token으로 승격할지, 기존 `말결값(문자열)` builtin과 별도 계층으로 병존시킬지 결정 필요.
- 부정 결합의 “부호 반전”이 weight 부호인지, valence 축 반전인지, 논리 결과의 confidence 반전인지 런타임 의미를 확정해야 한다.
