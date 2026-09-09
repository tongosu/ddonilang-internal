# DDN-R-RELINT-PC01-01 — PC01 fresh fixed-HEAD 독립 검토 결과

- ORIGIN_TASK_ID: DDN-LONG-RELINT-PRODUCT-01
- EXECUTOR: 독립검증ClaudeCode
- RETURN_TO: Codex관리Work
- 검토일: 2026-08-26
- 검토 worktree: `build/worktrees/review-ddn-pc01-fresh-fixed-head-20260826` (git worktree, `review/ddn-pc01-fresh-fixed-head-20260826` 브랜치, main tree 비접촉)

## VERDICT: **PASS_WITH_FOLLOW_UP**

plain PASS 아님 — 아래 §D의 정밀한 단일 결함(안전성 훼손 없음, 진단 완성도 gap) 때문에
follow-up으로 낮춘다. PC01 release membership을 열지 않는다.

## 판정 근거 요약

봉인 5파일 팩과 mutation runner는 그대로 재실행했지만(직접 재현이 목적이므로), 그 결과만으로
끝내지 않고: (a) 실제 CLI/WASM/runtime/LSP 소비 지점을 소스에서 추적, (b) 팩이 다루지 않는
독자 반례 4건을 별도 임시 테스트 파일로 작성·실행·즉시삭제, (c) `a2e23fd4→fc09a1f4` 구간과
`f80c69b8→fc09a1f4` 구간을 raw diff로 직접 대조했다.

## 필수 검증 1~10 결과

| # | 항목 | 결과 | 근거 |
|---:|---|---|---|
| 1 | Definition/Binding AST·parser·canon identity 분리 | PASS | `Stmt::Definition`(ast.rs:144)과 `Stmt::Mutate`는 별개 variant. `parse_v25`는 `Parser::new_v25_with_mode`(전용 생성자)를 쓰고 `SourceEpoch::V25`를 명시적으로 붙인다. canon 출력은 `:=`/`<-`를 분리해 쓴다(normalizer.rs) |
| 2 | 옛 `=` Definition surface silent acceptance 0 | PASS (단, §D 참고) | top-level SeedDef `=`(parser.rs:227)와 local 무타입 `이름 = 값`(is_legacy_definition_stmt_start, parser.rs:1861-1862)은 `E_V25_DEFINITION_MIGRATION_REQUIRED`로 명시 거부. **어떤 경로로도 silent ACCEPT는 발견되지 않음** — 모든 옛 `=` 시도는 최소한 reject된다(§D의 typed-local 케이스도 reject는 되고, 진단 코드만 다르다) |
| 3 | Binding-as-Definition 오용 fail-closed 진단 | PASS | 채비 블록 이름 도입에서 `<-` 사용 시 `E_V25_DEFINITION_BINDING_CATEGORY`(parser.rs:1812-1816) — 팩의 `negative_binding_as_definition.ddn`으로 재현 확인 |
| 4 | parse→canon→parse category/symbol identity | PASS | 팩 테스트 `v25_parse_canon_parse_preserves_categories_and_symbols` 재실행 PASS. 독자 probe로 canon→parse→canon **2회 roundtrip**까지 확장해 고정점(fixed point)임을 추가 확인(§C-2) |
| 5 | runtime/LSP projection category collapse 0 | PASS | (a) runtime: `tool/src/ddn_runtime.rs`의 `DdnProgram::from_v25_source` → 실제 `DdnRunner::run_update` 실행까지 연결된 기존 단위 테스트 `v25_definition_then_rebinding_executes_as_distinct_local_operations`를 재실행 PASS(값이 1→2로 rebind된 뒤 "2"가 출력됨을 직접 확인). (b) LSP: `tool/src/lsp/server.rs`가 `Stmt::Definition`/`Stmt::Mutate`를 별개 match arm으로 처리(collapse 없음) |
| 6 | 5파일 팩 내부 일관성 + oracle 실제 소비 | PASS | `expected.jsonl` 3행이 `v25_definition_binding_pack_matches_oracle` 테스트에서 실제로 읽혀 case_count==3 assert까지 통과 |
| 7 | PC02 exact inverse 이후 hidden fallback 0 | PASS | `parse_v25`/`from_v25_source`는 `tool/src`, `tools/teul-cli/src`, `solutions/`(Workbench) 어디서도 CLI/WASM/Workbench 진입점으로 연결되지 않음(단위테스트 1곳 제외) — PC02(공유 frontdoor 스위치)가 아직 존재하지 않으므로 "hidden fallback"이 생길 배선 자체가 없다. 기본 `parse`/`from_source` 경로는 PC01 추가로 전혀 바뀌지 않음(순수 추가) |
| 8 | 현재 CLI/WASM/Workbench 조합이 PC01 계약을 훼손하지 않음 | PASS | `f80c69b8→fc09a1f4` 구간 diff는 `publish/spec/v0.5.0/*`(신규 파일만, 순수 추가) + `tests/run_ddn_public_specific_conformance_check.py`(신규) + `work/codex/**` 문서뿐. `lang/src`, `tool/src`, `tools/teul-cli/src`, `core/src` 변경 0 — PC01 관련 코드 자체가 이 구간에서 전혀 건드려지지 않았다 |
| 9 | Rust pack 직접 실행 3/3 | PASS | `cargo test -p ddonirang-lang --test v25_definition_binding_pack` → 3 passed; 0 failed (§B) |
| 10 | M1/M2/M3 GREEN→RED→exact restore→GREEN, residue 0 | PASS | `node tests/ddn_v25_pc01_definition_binding_mutation_runner.mjs` 재실행: baseline GREEN → M1/M2/M3 전부 RED → restored GREEN → `DDN_V25_PC01_MUTATION_RED_GREEN_PASS residue=0`. 이후 `git status --short` 완전 공백으로 재확인(§B) |

## §A. 계보 확인

```
REVIEW_PARENT = FIXED_INTEGRATION_HEAD = fc09a1f4c857c97db20194173b19e17a3b83f9aa (동일 커밋, 직접 확인)
fc09a1f4의 부모 = 375554bd35fdefc6c5a67f97a5413e268d54d57f (git log -1 --format="%H %P")
f80c69b8dc9363fe56f95e0467bc8ff1f791cf76 는 fc09a1f4의 조상(ancestor) 확인
merge commit 수, f80c69b8..fc09a1f4: 0 (git log --merges 공백)
```

**a2e23fd4 → fc09a1f4 구간 직접 확인(요청서의 명시적 요구)**:
`f80c69b8..fc09a1f4` diff = `publish/spec/v0.5.0/*`(신규 8개 문서 + 7개 예제 + manifest, 전부
`+`만 있는 순수 추가), `tests/run_ddn_public_specific_conformance_check.py`(신규),
`work/codex/20260826_ddn_long_relint_product_01/*` 문서 4개(신규) — 23 files changed,
1134 insertions(+), **삭제/수정 0**. `a2e23fd4`는 이 구간 안의 한 지점이므로 이 결과가 그대로
적용된다. **PC01 제품 의미를 바꾸는 변경 없음을 diff 자체로 확인**.

## §B. 직접 재현

```
$ CARGO_TARGET_DIR=I:/home/urihanl/ddn/codex/target_review_pc01 \
  cargo test -p ddonirang-lang --test v25_definition_binding_pack -- --nocapture
test pre_v25_reader_is_explicitly_separate_from_v25_reader ... ok
test v25_definition_binding_pack_matches_oracle ... ok
test v25_parse_canon_parse_preserves_categories_and_symbols ... ok
test result: ok. 3 passed; 0 failed

$ node tests/ddn_v25_pc01_definition_binding_mutation_runner.mjs
baseline: GREEN
M1_DEFINITION_TO_BINDING_COLLAPSE: RED
M2_OLD_EQUALS_SILENT_ALIAS: RED
M3_DEFINITION_CANON_BINDING_SYMBOL: RED
restored: GREEN
DDN_V25_PC01_MUTATION_RED_GREEN_PASS residue=0

$ git status --short   →  (공백)

$ cargo test --manifest-path tool/Cargo.toml v25_definition_then_rebinding_executes_as_distinct_local_operations -- --nocapture
test result: ok. 1 passed; 0 failed
```

## §C. 독립 추가 반례(팩과 별개, 임시 파일 작성→실행→즉시삭제)

임시 파일 `lang/tests/zz_independent_review_probe_pc01.rs`, `lang/tests/zz_probe2_typed_vs_untyped.rs`를
worktree에 만들어 실행한 뒤 **커밋 없이 즉시 삭제**하고 `git status --short` 공백을 재확인했다(§E).

**C-1. local 문에서 옛 `=` (무타입)**: `값 = 1.` → `E_V25_DEFINITION_MIGRATION_REQUIRED` 정확히 발화. PASS.

**C-2. 2회 roundtrip 고정점**: `parse_v25 → canon → normalize → parse_v25 → canon → normalize`를
연쇄해 `canon1 == canon2`, `(definitions, bindings) == (1, 1)` 유지 확인. PASS — 팩의 단일 roundtrip
검증을 한 단계 더 공격했지만 안정적.

**C-3. 재정의(같은 이름을 `:=`로 두 번)**: `값:수 := 1.` 다음 `값:수 := 2.` — 두 문 모두
`Stmt::Definition`으로 남아 있고(즉 두 번째가 `Stmt::Mutate`로 조용히 collapse되지 않음) 확인. PASS.

**C-4. `source_epoch` 필드 직접 확인**: `parse_v25` 결과의 `program.source_epoch == SourceEpoch::V25`. PASS.

## §D. 발견 사항 (PASS_WITH_FOLLOW_UP 사유)

**typed-local 옛 `=`가 fail-closed는 하지만 전용 진단 코드를 받지 못한다.**

```
소스: 값:수 = 1.   (채비 블록도 top-level SeedDef도 아닌, 타입 주석이 붙은 local 문)
결과: Err(...) — reject는 된다(안전성 유지, silent accept 아님)
그러나 err.message == ":="  (일반 "expected token" 오류, E_V25_DEFINITION_MIGRATION_REQUIRED 아님)

비교:
소스: 값 = 1.       (무타입 local 문) → err.message에 E_V25_DEFINITION_MIGRATION_REQUIRED 포함 — 의도대로 동작
```

원인: `is_legacy_definition_stmt_start()`(parser.rs:1861-1862)가 `ident` 바로 다음 토큰이
`Equals`인지만 검사한다. 타입 주석(`:수`)이 끼면 이 판별식이 거짓이 되어 대신
`is_definition_stmt_start()`(Colon 다음 토큰이 `Define`이거나 `Colon`이면 참)가 걸려
`parse_definition_stmt()`로 진입하고, 거기서 `self.expect(&TokenKind::Define, ":=")`가
그냥 범용 "expected :=" 오류를 낸다.

**영향 범위 판단**: 봉인 5파일 팩의 두 negative 케이스(`negative_old_equals.ddn`은 top-level
SeedDef 형태만, `negative_binding_as_definition.ddn`은 채비 블록 `<-` 형태만) 어느 것도 이
typed-local 형태를 포함하지 않으므로 **팩 자체는 100% 정상**이고 이 발견은 팩 범위 밖의
추가 반례에서 나왔다. 항목 2("silent acceptance 0")는 여전히 성립한다 — 이 케이스도
분명히 REJECT되며, 사용자가 V25로 잘못 넘어가는 경로가 아니다. 다만 항목 3/9가 요구하는
"the intended product-local diagnostic"과는 다른, 일반화된 오류가 나가므로 진단 완성도
gap으로 기록하고 PASS_WITH_FOLLOW_UP 사유로 삼는다.

**참고(관련 없음으로 확인)**: `채비` 블록 아이템에서 `=`가 나오면 `DeclKind::Butbak`이라는
완전히 별개의 기존 AST 종류로 파싱되고(parser.rs:1824-1827), normalizer도 이를 항상 `" = "`로
되돌린다(normalizer.rs:216) — epoch에 무관한, PC01과 무관한 기존 기능이다. 처음엔 "옛
`=`가 채비 블록에서 조용히 허용되는 것 아닌가" 의심했으나, 이는 Definition과 무관한 별도
`DeclItem` 카테고리이므로 PC01 범위 밖으로 확인했다.

## §E. 안전 경계 확인

- main working tree에 쓰기 0건. 모든 작업은 격리 worktree(`build/worktrees/review-ddn-pc01-fresh-fixed-head-20260826`)에서 수행했고, cargo 빌드도 `CARGO_TARGET_DIR=I:/home/urihanl/ddn/codex/target_review_pc01`(worktree 밖)로 분리했다.
- mutation runner가 건드린 `lang/src/parser.rs`/`normalizer.rs`는 스크립트 자체의 restore + 이 세션의 `git status --short` 재확인(공백)으로 residue 0 확인.
- 독립 probe 임시 파일 2개는 실행 후 즉시 삭제, `git status --short` 재확인(공백).
- `docs/ssot/**`, public SPEC, tracked WASM, 공식 DB, protected process/socket, activation 상태: 이 검토 세션에서 어느 것도 열거나 쓰지 않았다(읽기조차 하지 않음 — PC01 검토 범위가 이들과 직접 상호작용하지 않는다). `f80c69b8..fc09a1f4` 구간 자체의 diff에는 `publish/spec/v0.5.0/*` 신규 파일 추가가 있으나 전부 순수 추가이고 PC01 Definition/Binding 표면과는 겹치지 않는다(§A).
- Rights/license/공개 복사/activation/Human PASS: 판단하지 않았고 승인하지 않는다.

## 반환 스키마

```
VERDICT: PASS_WITH_FOLLOW_UP
SCOPE: PC01 Definition/Binding semantic distinction, fresh fixed-HEAD targeted review
FIXED_INTEGRATION_HEAD: fc09a1f4c857c97db20194173b19e17a3b83f9aa
FIXED_PRODUCT_SOURCE_HEAD: f80c69b8dc9363fe56f95e0467bc8ff1f791cf76
REVIEW_PARENT: fc09a1f4c857c97db20194173b19e17a3b83f9aa
REVIEW_COMMIT: (이 보고서 커밋 시 채움, 아래 커밋 로그 참조)
REVIEW_BRANCH: review/ddn-pc01-fresh-fixed-head-20260826
REPORT_PATH: work/claude/20260826_ddn_pc01_fresh_fixed_head_independent_review/REVIEW_RESULT.md
REPORT_BYTES: (커밋 후 파일 크기, 아래 참조)
REPORT_SHA256: (커밋 후 재계산, 아래 참조)
MERGE_COMMIT_COUNT: 0
PRODUCT_DIFF: 0 (lang/src, tool/src, tools/teul-cli/src, core/src 무변경 in f80c69b8..fc09a1f4)
SSOT_DIFF: 0 (review 세션이 docs/ssot/** 미접촉)
PUBLIC_SPEC_DIFF: f80c69b8..fc09a1f4 구간에 publish/spec/v0.5.0/* 신규 파일 추가(순수 추가, PC01과 무관); review 세션 자체는 0
TRACKED_WASM_DIFF: 0
MUTATION_RESULT: M1/M2/M3 3/3 GREEN→RED→restore GREEN, residue 0
RESIDUE_COUNT: 0
PROTECTED_RESOURCE_CUSTODY: 미접촉(불변) — 공식 DB/protected process·socket/activation 상태 이 검토에서 열거나 쓴 적 없음
FINAL_STATUS: PASS_WITH_FOLLOW_UP — plain PASS 아님, PC01 release membership 미개방. follow-up: `is_legacy_definition_stmt_start()`을 타입 주석 유무와 무관하게 판별하도록 넓혀 typed-local 옛 `=`도 E_V25_DEFINITION_MIGRATION_REQUIRED를 받게 하는 좁은 진단 정밀화 권고(안전성 자체는 이미 확보됨)
```
