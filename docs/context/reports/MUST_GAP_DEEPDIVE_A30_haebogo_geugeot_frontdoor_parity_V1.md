# MUST_GAP_DEEPDIVE_A30_haebogo_geugeot_frontdoor_parity_V1

## 대상

- Track A item: `A30`
- SSOT rule: `[V18-02] ~해보고: + 그것`
- SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1435`
- Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:30`
- 산출물 성격: red conformance 심화조사

## 현재 재검증

SSOT는 `〈동작〉 해보고:`가 동작을 1회 실행하고 결과를 `그것`에 바인딩하며, `그것`의 범위를 블록 내부로 제한한다고 정한다. 감사표의 “제품 lang/runtime 경로 no-match” 판정은 `tools/teul-cli` 내부 frontdoor 기준으로는 여전히 맞지만, 루트 `lang/`과 legacy `tool/`에는 `Stmt::Try`와 `그것` 바인딩 흔적이 있다. 따라서 이 항목은 “완전 부재”가 아니라 `teul-cli` 제품 frontdoor parity red / 재분류 필요로 기록한다.

## 근거

- SSOT V18-02 시작: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1435`
- `〈동작〉 해보고:` 문법: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1438`
- 결과를 `그것`에 바인딩하고 범위를 블록으로 제한한다는 요구: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1439`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1440`
- `teul-cli`는 루트 `ddonirang-lang` 의존성과 별도로 내부 `mod lang`을 가진다: `tools/teul-cli/Cargo.toml:19`, `tools/teul-cli/src/main.rs:12`
- 루트 `lang`에는 `KwHaebogo` token과 parser `Stmt::Try` 생성 경로가 있다: `lang/src/lexer.rs:45`, `lang/src/lexer.rs:1203`, `lang/src/parser.rs:489`, `lang/src/parser.rs:494`
- legacy `tool` runtime은 `Stmt::Try` 평가에서 `그것`을 locals에 바인딩한다: `tool/src/ddn_runtime.rs:3199`, `tool/src/ddn_runtime.rs:3201`, `tool/src/ddn_runtime.rs:3659`, `tool/src/ddn_runtime.rs:3661`
- 직접 검색: `rg -n 'KwHaebogo|해보고|Stmt::Try|그것' tools/teul-cli/src/lang tools/teul-cli/src/runtime/eval.rs` = NO_MATCH
- 감사 행은 `tools/teul-cli` lang/runtime 기준으로 해당 표면을 찾지 못해 미구현 판정했다: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:30`

## 판정

- 현재 판정: red 유지, 단 `재분류 필요` 표시
- red 범위: `tools/teul-cli` 제품 frontdoor parity
- 이미 확인된 부분 구현 흔적: 루트 `lang/` parser/AST, legacy `tool/` runtime
- 언어 커널 구현 변경: 없음
- 신규 red pack: `pack/must_gap_a30_haebogo_geugeot_frontdoor_red_v1`

## 결정 필요

- `tools/teul-cli`가 루트 `ddonirang-lang`의 `Stmt::Try`를 제품 frontdoor로 재사용할지, 내부 `tools/teul-cli/src/lang`에 별도 표면을 맞출지 결정 필요.
- root `lang`/legacy `tool` 구현을 현재 Gate0 제품 경로로 승격할 수 있는지 별도 parity 검증이 필요하다.
