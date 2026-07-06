# MUST_GAP_DEEPDIVE_A43_binding_ambiguity_lsp_quickfix_V1

## 대상

- Track A item: `A43`
- SSOT rule: `10.5.2 바인딩 모호성 진단 + LSP QuickFix`
- SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3430`
- Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER2_V1.md:42`
- 산출물 성격: red conformance 심화조사

## 현재 재검증

SSOT는 핀 후보가 2개 이상이면 추측하지 않고 `PIN_AMBIGUOUS` 오류와 `:핀`/`~조사`/문장 재작성 QuickFix를 제공해야 한다고 정한다. 현재 `teul-cli` parser는 `:핀`과 `~조사`를 `ArgBinding`에 보존하지만, 제품 AST의 `BindingReason`에는 ambiguous 상태가 없다. `tool/src/lsp`에는 `AmbiguousPin`, `QuickFix`, rebind action 골격이 있으나 `check_pin_ambiguity`는 빈 함수이고, 위치 탐색과 원문 추출도 stub이다. `@` 오용 진단도 `InvalidSuffix`를 만들지만 fixes는 비어 있다.

따라서 현재 제품 경로는 접미 분해/보존 일부만 있고, SSOT의 바인딩 후보 산출, 모호성 오류, QuickFix 우선순위 집행은 red로 남는다.

## 근거

- SSOT 10.5.2 시작: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3430`
- 후보가 2개 이상이면 `PIN_AMBIGUOUS`와 QuickFix 필요: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3442`
- LSP QuickFix 우선순위: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3444`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3445`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3446`
- SSOT 예시 후보 2개/QuickFix: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3450`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3451`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3452`
- `@` 오용 QuickFix 요구: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3454`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3457`
- 감사 행은 일반 QuickFix 골격만 있고 조사/핀 모호성 전용 구현은 없다고 판정했다: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER2_V1.md:42`
- 현재 `teul-cli` `ArgBinding`은 josa/resolved_pin을 보존한다: `tools/teul-cli/src/lang/ast.rs:365`, `tools/teul-cli/src/lang/ast.rs:367`, `tools/teul-cli/src/lang/ast.rs:368`
- 현재 `teul-cli` `BindingReason`은 `Dictionary`, `Positional`, `UserFixed`뿐이다: `tools/teul-cli/src/lang/ast.rs:376`
- 현재 `parse_arg_suffix`는 `:핀`과 `Josa`를 분리한다: `tools/teul-cli/src/lang/parser.rs:5353`, `tools/teul-cli/src/lang/parser.rs:5376`, `tools/teul-cli/src/lang/parser.rs:5380`
- 현재 named/fixed pin은 `resolved_pin`으로 들어간다: `tools/teul-cli/src/lang/parser.rs:5410`, `tools/teul-cli/src/lang/parser.rs:5414`
- LSP diagnostic code 골격: `tool/src/lsp/server.rs:366`
- LSP quickfix kind 골격: `tool/src/lsp/server.rs:386`
- LSP diagnose는 pin ambiguity check를 호출하지만 구현은 빈 함수다: `tool/src/lsp/server.rs:411`, `tool/src/lsp/server.rs:420`
- LSP rebind action은 ambiguous binding일 때만 동작하도록 되어 있다: `tool/src/lsp/server.rs:763`, `tool/src/lsp/server.rs:765`
- 위치 탐색은 항상 `None`이다: `tool/src/lsp/server.rs:772`
- 원문 추출은 빈 문자열이다: `tool/src/lsp/server.rs:803`
- `@` 오용 진단은 fixes를 비워 둔다: `tool/src/lsp/server.rs:469`, `tool/src/lsp/server.rs:475`

## 판정

- 현재 판정: red 유지
- 언어 커널 구현 변경: 없음
- 신규 red pack: `pack/must_gap_a43_binding_ambiguity_lsp_quickfix_red_v1`

## 결정 필요

- 제품 `tools/teul-cli` AST에 ambiguous candidate list를 보존할지, LSP 전용 분석기가 별도 symbol table에서 후보를 계산할지 결정 필요.
- `PIN_AMBIGUOUS` 오류 코드의 계층이 parser/runtime/LSP 중 어디에 속하는지 확정해야 한다.
- `@` 오용 QuickFix의 자동 치환 범위가 `@대상` 전체인지, 뒤따르는 `~조사`까지 포함한 접미 chain 전체인지 결정 필요.
