# MUST_GAP_DEEPDIVE_A25_josa_canon_tilde_insertion_V1

## 대상

- Track A item: `A25`
- SSOT rule: `NAMING-LINT 3) 정본화`
- SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6994`
- Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER4_V1.md:57`
- 산출물 성격: red conformance 심화조사

## 현재 재검증

SSOT는 조사 접미사 자동 분리로 `S + J`가 판정되면 정본화기가 반드시 `S~J` 형태로 `~`를 삽입해야 한다고 정한다. 현재 `teul-cli` 경로는 명시 `~`가 있는 입력을 `TokenKind::Josa`로 처리하고 call arg suffix에 붙이는 경로는 있지만, `도로를` 같은 붙임형을 `도로~를`로 자동 canon 출력하는 경로는 확인되지 않는다.

## 근거

- SSOT 정본화 MUST: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6994`
- 자동 분리 시 `~` 삽입 요구: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6995`
- 붙임형 예시와 기대 정본: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:7003`
- 현재 lexer는 명시 `~`에서만 `read_josa`로 들어간다: `tools/teul-cli/src/lang/lexer.rs:356`
- `read_josa`는 dialect josa를 `TokenKind::Josa`로 만든다: `tools/teul-cli/src/lang/lexer.rs:614`, `tools/teul-cli/src/lang/lexer.rs:633`, `tools/teul-cli/src/lang/lexer.rs:635`
- parser의 call arg suffix는 이미 tokenized된 `TokenKind::Josa`만 소비한다: `tools/teul-cli/src/lang/parser.rs:5355`, `tools/teul-cli/src/lang/parser.rs:5374`, `tools/teul-cli/src/lang/parser.rs:5386`
- 감사 행은 자동 split 후 canon `~` 삽입 경로 부재로 미구현 판정했다: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER4_V1.md:57`

## 판정

- 현재 판정: red 유지
- 언어 커널 구현 변경: 없음
- 신규 red pack: `pack/must_gap_a25_josa_canon_tilde_insertion_red_v1`

## 결정 필요

- 자동 split을 lexer tokenization에서 수행할지, parser/name resolution 이후 canon 단계에서 수행할지 결정 필요.
- `T`와 `S`가 모두 유효한 경우 경고와 fatal의 경계를 lint 정책으로 확정해야 한다.
