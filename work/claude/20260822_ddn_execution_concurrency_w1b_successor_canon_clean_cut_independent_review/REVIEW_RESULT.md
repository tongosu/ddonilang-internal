# DDN execution concurrency W1-B successor canon clean-cut 독립 검토 결과

## 0. 판정

```text
PASS
SCOPE: W1B_SUCCESSOR_CANON_CLEAN_CUT_ONLY
```

fixed HEAD `7610e4bf...`의 successor canon clean-cut을 fresh detached worktree와 격리
Cargo target/WASM output에서 독립적으로 전부 재현했다. 계보·변경 범위·parser
identity·canon clean-cut·default runtime fail-closed·migration evidence 격리·13-case
D-PACK·native/WASM/Workbench parity·4건 fault injection·전체 회귀·보호 경계 전부
결함 0으로 확인했다. `PASS`로 판정하되 범위는 W1-B에만 한정하며 W1 전체 `PASS`나
`CLOSED`는 선언하지 않는다.

## 1. 검토 고정점과 환경

| 항목 | 값 |
|---|---|
| PRODUCT_FIXED_HEAD | `7610e4bfda5c322e65cf6df9a5af45e58e0ab4bf` |
| FIXED_HEAD_PARENT | `6e03e0cfcff64de8a578883cb8ccba15bdf17cee` |
| HANDOFF_COMMIT | `97fe787bb4cb4bdd80700c9c44a38085613b9105` |
| PREDECESSOR_PRODUCT_FIXED_HEAD | `aaf72e08498031feeabfabc6692316e42dcfdc42`(PASS, `W1_FIRST_SAFE_ASYNC_VERTICAL_ONLY`) |
| CURRENT_SSOT | v24.48.0 |
| PUBLIC_LANGUAGE_SPEC | v0.5.0 |
| 테스트 worktree | `claude-w1b-canon-review-20260822`(fixed HEAD detached, 종료 후 제거) |
| 보고서 commit worktree | `claude-w1b-report-commit-20260822`, 브랜치 `claude/ddn-execution-concurrency-w1b-successor-canon-clean-cut-independent-review-20260822`, parent `97fe787b` |
| 격리 Cargo target | `target-claude-w1b-canon-review-20260822`(tool/lang), `target-claude-w1b-teulcli-only-20260822`(teul-cli 전용, 종료 후 모두 삭제) |
| SSOT material bridge | 테스트 worktree 내부 `docs/ssot/ssot`(v24.44.1 12파일 raw-byte copy, 종료 후 worktree와 함께 제거) |

구현 worktree(`ddn-execution-concurrency-w1b-canon-clean-cut-20260822`)는 직접 수정하지
않았다.

## 2. 계보와 변경 범위

```bash
git log -1 --format="%H parent=%P" 7610e4bfda5c322e65cf6df9a5af45e58e0ab4bf   # parent=6e03e0c...
git log -1 --format="%H parent=%P" 97fe787bb4cb4bdd80700c9c44a38085613b9105   # parent=7610e4b...
git merge-base --is-ancestor 6e03e0cfcff64de8a578883cb8ccba15bdf17cee 97fe787bb4cb4bdd80700c9c44a38085613b9105   # YES
git log --merges 6e03e0c...97fe787b... --oneline | wc -l   # 0
```

3개 commit이 요청서의 `EXPECTED_LINEAGE`와 정확히 일치, merge commit 0.

```bash
git diff --stat 6e03e0cfcff64de8a578883cb8ccba15bdf17cee 7610e4bfda5c322e65cf6df9a5af45e58e0ab4bf
```

34 files changed, lang/src/{normalizer.rs, parser.rs}, `pack/future_grammar_atlas_owner_closed_delta_r2`의
9개 신규 case 디렉터리 + golden.jsonl/logical_oracle.jsonl(9행 추가, 13행 확정),
`solutions/seamgrim_ui_mvp/ui/wasm/*`(tracked WASM 산출물 4개 파일),
`tests/ddn_execution_concurrency_w1b_native_wasm_parity_runner.mjs`(신규),
`tool/src/{ddn_runtime.rs, runtime_surface.rs, wasm_api.rs}`,
`tools/teul-cli/src/{canon.rs, cli/frontdoor_parse.rs, cli/lang_mode.rs, lang/parser.rs,
lang/token.rs, main.rs, runtime/eval.rs}` — 전부 언어/런타임/CLI/WASM 경계 파일이다.

```bash
git diff --exit-code 6e03e0cfcff64de8a578883cb8ccba15bdf17cee 7610e4bfda5c322e65cf6df9a5af45e58e0ab4bf -- 'solutions/seamgrim_ui_mvp/ui/*' ':!solutions/seamgrim_ui_mvp/ui/wasm'
# exit 0 — wasm 산출물 디렉터리를 제외한 UI source diff 0
git diff --stat 6e03e0c...97fe787b... -- docs/ssot/   # 0
git diff --stat 6e03e0c...97fe787b... -- publish/spec/ # 0
git diff --stat 7610e4b...97fe787b... -- ':!work' ':!docs'   # 0 (handoff는 문서 전용)
git diff --stat 6e03e0c...97fe787b... -- 'pack/*' ':!pack/future_grammar_atlas_owner_closed_delta_r2'   # 0
```

`solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.js`/`.d.ts`의 diff를 직접 열람해
wasm-bindgen이 생성한 바인딩 코드(`wasm_historical_async_migration_evidence_json` export
추가)뿐임을 확인했다 — 손으로 작성한 UI 동작 코드가 아니다.

## 3. 현행 권위 감사

```text
docs/ssot/CURRENT.md: 내부 current v24.48.0, 진입점 SSOT_INDEX_v24.48.0.md, 상태 live current
publish/spec/CURRENT.md: 현재 공개판 v0.5.0
```

`docs/ssot/ssot/SSOT_INDEX_v24.48.0.md`가 실재하고 `CURRENT.md`가 가리키는 진입점과
일치함을 직접 확인했다. v24.45.1~v24.48.0 사이 authority drift는 W1-B diff(§2의 34개
파일)와 겹치지 않으므로(모두 언어/런타임/CLI/WASM 경계 파일, SSOT/SPEC 파일 아님)
직접 충돌은 없다. SSOT current·제품 구현·public SPEC·independent PASS·runtime
activation을 분리해 판정했으며, 이 검토는 SSOT current나 public SPEC의 변경을 승인하지
않는다.

## 4. historical corpus 독립 집계

```bash
grep -rl '~~>' pack/ --include="*.ddn" | grep -v future_grammar_atlas_owner_closed_delta_r2 | wc -l   # 39
grep -ro '~~>' pack/ --include="*.ddn" | grep -v future_grammar_atlas_owner_closed_delta_r2 | wc -l   # 95
grep -rl '<<-' pack/ --include="*.ddn" | grep -v future_grammar_atlas_owner_closed_delta_r2 | wc -l   # 5
grep -ro '<<-' pack/ --include="*.ddn" | grep -v future_grammar_atlas_owner_closed_delta_r2 | wc -l   # 7
```

요청서·인계 문서가 주장한 39 files/95 occurrences(`~~>`), 5 files/7 occurrences(`<<-`)와
정확히 일치했고, 이 corpus의 source diff는 §2에서 이미 0으로 확인했다.

## 5. parser identity — 13-case 실측 (Section 6~7 겸함)

fresh 격리 빌드(native `ddonirang-tool.exe`, `teul-cli.exe`)로 successor D-PACK의 13개
case를 golden.jsonl과 대조하며 전부 개별 실행했다. teul-cli 빌드는 처음에
`cargo test --manifest-path tools/teul-cli/Cargo.toml`이 `serde_json` 두 버전
충돌(E0308/E0631/E0282)로 실패했는데, 원인을 추적한 결과 **내가 tool/과 teul-cli/를
같은 격리 `CARGO_TARGET_DIR`에서 빌드해 두 개의 독립적으로 lock된 그래프(루트
워크스페이스 Cargo.lock의 serde_json 1.0.147 vs teul-cli 자체 Cargo.lock의 1.0.149)가
빌드 캐시에서 충돌**한 것이었다 — teul-cli 전용 격리 target으로 분리하자 즉시
1,161/1,161 PASS로 재현됐다(§9). 제품 결함이 아니며 W1-B diff와 무관하다.

| case | 명령 | 기대(golden.jsonl) | 실측 |
|---|---|---|---|
| c01 async left | `run` | stdout `7`, exit 0 | 일치 (state_hash `ea710335...`) |
| c02 async zero route | `run` | `E_ASYNC_ENDPOINT_UNHANDLED`, exit 1 | 일치 |
| c03 async multi route | `run` | `E_ASYNC_ENDPOINT_AMBIGUOUS`, exit 1 | 일치 |
| c04 nested FIFO tail | `run` | stdout `123`, exit 0 | 일치 |
| c05 async right | `run` | stdout `7`, exit 0 | 일치 (state_hash `ea710335...`, c01과 동일 — 좌/우 표기 의미 동등성 확인) |
| c06 rendezvous left | `run` | `E_RENDEZVOUS_PRODUCT_OPEN`, exit 1 | 일치 |
| c07 rendezvous right | `run` | `E_RENDEZVOUS_PRODUCT_OPEN`, exit 1 | 일치 |
| c08 historical migration | `historical-async-migration-evidence` | 정확한 evidence JSON | **바이트 단위 완전 일치** |
| c09 default old `~~>` reuse forbidden | `run` | `E_RENDEZVOUS_PRODUCT_OPEN`, exit 1 | **일치 — clean-cut 핵심 케이스, historical로 새지 않음** |
| c10 historical migration span(2건) | `historical-async-migration-evidence` | 정확한 evidence JSON(2 artifacts) | **바이트 단위 완전 일치** |
| c11 async canon roundtrip | `canon` | `~>`로 정본화 | 일치 |
| c12 rendezvous canon roundtrip | `canon` | `~~>`로 정본화(async와 구분) | 일치 |
| c13 native rendezvous boundary | `run` | `E_RENDEZVOUS_PRODUCT_OPEN`, exit 1 | 일치 |

**13/13 전부 golden.jsonl과 정확히 일치**함을 fresh 빌드로 직접 확인했다. c09가 이번
clean-cut의 핵심 검증이다 — default 모드의 구식 `~~>`가 절대 `HistoricalAsync`로 새지
않고 `E_RENDEZVOUS_PRODUCT_OPEN`으로 정확히 거부된다.

### legacy projection canon 분리

`tools/teul-cli/src/canon.rs` diff를 직접 열람했다. 이 별도(untyped) legacy
canonicalizer는 이전에는 `~~>`를 그냥 텍스트로 통과시켰으나, 이제는
`TokenKind::SignalArrow`가 있으면 무조건 `E_CANON_TYPED_TRANSFER_REQUIRES_SHARED_FRONTDOOR`로
거부하고 공통 typed frontdoor(§5의 c11/c12 canon 경로)로만 처리하도록 강제한다 —
일반 canon과 typed transfer canon의 진입점이 코드 레벨에서 분리됐다.

## 6. default runtime fail-closed — 코드 감사

`tools/teul-cli/src/runtime/eval.rs`의 `Stmt::Send` 디스패치를 직접 열람했다.

```rust
match transfer {
    MessageTransfer::HistoricalAsync(_) => self.dispatch_signal_send(...),  // legacy broadcast
    MessageTransfer::Async(_) => self.dispatch_async_send(...),             // successor async
    MessageTransfer::Rendezvous(_) => return Err(RuntimeError::RendezvousProductOpen { span }),
}
```

`transfer`는 파서가 이미 확정한 값이며(§5), default 모드에서 `~~>`는 파서 단계에서
`Rendezvous`로 고정되므로 이 match의 `HistoricalAsync`/`Async` 분기는 default 실행
경로에서 `~~>`에 대해 **도달 자체가 불가능**하다 — 즉시 `RendezvousProductOpen`
오류로 종료된다. `dispatch_signal_send`(historical 분기)는 오직 파서가
`HistoricalMigrationEvidence` 모드로 이미 태깅한 문장에서만 호출되므로, 이 함수
내부의 `historical_async_for_migration()` 하드코딩은 라우팅 결정이 아니라 상위에서
이미 확정된 태그를 그대로 전달하는 것뿐임을 확인했다.

`lang/src/delivery.rs`: `HistoricalAsyncSend` struct는 비공개 필드
(`_migration_evidence_only: ()`)를 가져 구조체 리터럴로 외부에서 직접 생성할 수
없고, `historical_async_for_migration()`은 명명된 단일 constructor다. 저장소 전체
`*.rs`에서 이 함수의 호출처를 검색해 `lang/src/parser.rs`(migration 모드 분기),
`tools/teul-cli/src/lang/parser.rs`(동일 패턴, 자체 파서 사본), 그리고 이미 historical
태그가 확정된 상태에서 값을 전달하는 런타임 내부 지점들뿐임을 확인했다 — 새 진입점은
없다.

## 7. migration evidence 격리 — 이중 방어 확인

- 파서 레벨: `ParseMode::HistoricalMigrationEvidence`가 아니면 default `~~>`는
  `Rendezvous`로 고정(§5, §6).
- **런타임 레벨의 독립된 두 번째 방어층을 발견**: `tool/src/ddn_runtime.rs`의
  `DdnProgram::from_source_with_mode`가 `mode == HistoricalMigrationEvidence`이면
  파싱 자체를 시작하기 전에 `E_HISTORICAL_ASYNC_MIGRATION_EXECUTION_FORBIDDEN`으로
  즉시 거부한다. 즉 설령 mode 선택 로직이 잘못되어 migration mode가 default 실행
  경로에 흘러들어와도, 이 별도 guard가 독립적으로 제품 실행 진입을 차단한다(§8
  fault injection mutation 2가 바로 이 이중 방어를 실측했다).
- 파일명·pack 경로·handler 종류로 mode를 추측하는 코드는 검색 결과 없다 — mode는
  항상 명시적 인자로 위에서 아래로 전달된다(`ParseMode` enum 값 하나로 귀결).
- historical → successor 변환 표면은 c08/c10의 `successor_replacement` 필드
  (`"값 ~~> 대상." → "값 ~> 대상."`)로 정확히 제공되며, 요청서가 명시한 old/successor
  치환 형태와 일치한다.

## 8. 4건 fault injection — RED 확인 후 원복

| # | 변이 | 대상 파일 | RED 결과 | 원복 확인 |
|---|---|---|---|---|
| 1 | default `~~>`를 `HistoricalAsyncSend`로 강제(mode 분기 제거) | `lang/src/parser.rs` | `cargo test -p ddonirang-lang`: 5건 실패(`successor_default_owns_double_arrow_as_rendezvous` 등) | SHA-256 `8bcc3055...` 원본과 일치 |
| 2 | migration mode를 default run에서 자동 활성화(`default_parse_mode()`가 항상 `HistoricalMigrationEvidence` 반환) | `tool/src/ddn_runtime.rs` | c01(이전에는 성공)이 `E_HISTORICAL_ASYNC_MIGRATION_EXECUTION_FORBIDDEN`으로 실패 — §7의 독립 실행-금지 guard가 실제로 작동함을 실측 확인 | SHA-256 `2fca9d18...` 원본과 일치 |
| 3 | `<~~`를 `AsyncSend`로 lowering | `lang/src/parser.rs` | `cargo test -p ddonirang-lang`: 1건 실패(`successor_direction_pairs_keep_distinct_typed_identities`) | SHA-256 `8bcc3055...` 원본과 일치 |
| 4 | historical migration artifact에서 identity tag 제거(canon 출력을 rendezvous와 동일 `~~>`로 되돌림) | `lang/src/normalizer.rs` | `cargo test -p ddonirang-lang`: 1건 실패(`explicit_migration_mode_emits_distinct_evidence`) | SHA-256 `cb979522...` 원본과 일치 |

시도 1(`Parser::new()`의 기본 mode 변경)과 시도 2(`lib.rs::parse()`의 기본 mode 변경)는
실제 `run` 실행 경로에 영향이 없어 mutation 2로 채택하지 않았다 — 두 함수 모두 default
`run` 경로에서 실제로 사용되지 않는 대체 진입점이었다(직접 실행 대조로 확인). 최종
채택한 `default_parse_mode()`가 실제 `run` 경로가 참조하는 지점임을 코드 추적으로
확인한 뒤 그 지점을 변이했다.

4건 전부 같은 검토 worktree에서 적용→RED 확인→즉시 `git checkout --`로 원복했다.
최종 재빌드 후 `cargo test -p ddonirang-lang` 347/347 PASS, `git status --short` 빈
결과로 mutation RED → restore GREEN → worktree clean을 확인했다.

## 9. successor D-PACK 원 runner 실행

```bash
python tests/run_pack_golden.py future_grammar_atlas_owner_closed_delta_r2
```

```text
pack golden ok
```

golden.jsonl은 정확히 13행이며 §5에서 13개 case 전부를 개별적으로도 재확인했다.

## 10. native/WASM/Workbench parity

fresh source-built teul-cli(격리 전용 target), fresh `--target nodejs` WASM
(`tool/pkg-nodejs`), tracked Workbench WASM(`solutions/seamgrim_ui_mvp/ui/wasm`)을
사용해 요청서 지정 env var로 원 parity runner를 실행했다.

```bash
DDN_W1B_CLI=<fresh teul-cli.exe>
DDN_W1B_WASM_DIR=<fresh nodejs wasm-pack dir>
DDN_W1B_TRACKED_WASM_DIR=<tracked ui/wasm dir>
node tests/ddn_execution_concurrency_w1b_native_wasm_parity_runner.mjs
```

```json
{"schema":"ddn.execution_concurrency.w1b.native_wasm_parity.v1","canon_cases":2,
 "migration_cases":2,"rendezvous_fail_closed_cases":1,
 "diagnostic":"E_RENDEZVOUS_PRODUCT_OPEN","failure_atomicity":true,
 "tracked_workbench_wasm":true}
```

실제 Microsoft Edge 러너: W1-B 전용 테스트 파일을 저장소 전체에서 검색한 결과
`ddn_execution_concurrency_w1b_native_wasm_parity_runner.mjs` 1개뿐이며 이는 순수
Node 기반(Playwright/Edge 의존 없음)이다. 이 범위를 검증하는 기존 실제 Edge runner는
제공돼 있지 않다 — `UI_CHANGED_0` 주장과 정합(브라우저 UI 표면 자체가 변경되지 않았으므로
전용 Edge smoke가 없는 것이 합리적이다). UI behavior 변경은 주장하지 않으며 이 검토도
주장하지 않는다.

## 11. WASM identity

```text
fresh source-built (--target web):  8be23053b6a6fbf74d2d1337f685dd8b2381f7b36932535fd0b69d7206db337d (5,439,334 bytes)
tracked (solutions/.../ui/wasm):    8be23053b6a6fbf74d2d1337f685dd8b2381f7b36932535fd0b69d7206db337d (동일)
구현자 주장값:                       8be23053b6a6fbf74d2d1337f685dd8b2381f7b36932535fd0b69d7206db337d / 5,439,334 bytes
```

세 값이 정확히 일치한다. native CLI metadata 변경으로 인한 WASM drift는 없다.

## 12. 전체 회귀

| 명령 | 결과 |
|---|---|
| `cargo test -p ddonirang-lang` | PASS — 347/347 |
| `cargo test -p ddonirang-tool --lib` | PASS — 485/485 |
| `cargo test --manifest-path tools/teul-cli/Cargo.toml`(teul-cli 전용 격리 target) | PASS — 1,161/1,161 |
| `cargo check -p ddonirang-tool --target wasm32-unknown-unknown --lib --features wasm` | PASS |
| `python tests/run_pack_golden.py future_grammar_atlas_owner_closed_delta_r2` | PASS — 13/13(§9) |
| `python tests/run_ddn_cli_wasm_freshness_check.py` | PASS |

개수는 인계 문서의 주장(347/485/1,161)과 정확히 일치한다. teul-cli 테스트가 처음
실패했던 원인(§5의 `CARGO_TARGET_DIR` 공유 아티팩트)은 검토 환경 설정 문제였고
W1-B diff의 회귀가 아님을 명확히 구분했다 — teul-cli 전용 격리 target으로 재실행해
1,161/1,161을 확인했다.

historical pack의 원문 변경 0은 §2·§4에서 이미 확인했다. `lang_consistency_v1` 등
predecessor부터 존재하던 기존 실패는 이번 검토 범위(fresh build·D-PACK·parity·fault
injection·보호 경계)에 포함되지 않았고, W1-B가 그 실패들을 성공으로 재포장하지
않았음은 §2의 diff 범위(그 pack들이 diff에 없음)로 방증된다.

## 13. 보호 경계

| 항목 | 검토 시작 | 검토 종료 |
|---|---|---|
| official_db_sha256 | `3fbf028e852dd3a13c3b84f812254de30c55113140f2b7869ff81a2a3b2b65f0` | 동일(불변) |
| protected_pid_53196 | python, StartTime 2026-08-08 12:27:21 | 동일 PID·동일 StartTime |
| protected_port_127.0.0.1_8787 | LISTEN, OwningProcess 53196 | 동일 |
| official_store_write_count | 0 | 0 |
| activation_endpoint_call_count | 0 | 0 |

보호 PID·port를 사용하거나 종료하지 않았다.

## 14. 참고 — 범위 밖 기존 관찰 사항(신규 아님)

native CLI `run` 서브커맨드의 project-policy 검사(`ddn.project.json`의
`ssot_requires: "24.44.1"`)는 현재 SSOT current(v24.48.0)보다 낡아 있다. 이는 W1-B
diff(§2의 34개 파일)에 `ddn.project.json`/`tool/src/project_meta.rs`가 포함되지 않아
W1-B가 만든 문제가 아니며, 이미 별도 검토(직전 세션)에서 발견·기록된 사전 존재
항목이다. 이번 검토는 authoritative v24.44.1 12파일을 검토 worktree 내부에
raw-byte로 bridge해 `run` 경로를 재현했고(§1), authoritative 원본에는 쓰지 않았다.
W1-B 제품 표면(언어/파서/canon/런타임/WASM)에는 영향이 없으므로 이 검토의 판정을
바꾸지 않는다.

## 15. 정리 상태

- 격리 Cargo target 2개(`target-claude-w1b-canon-review-20260822`,
  `target-claude-w1b-teulcli-only-20260822`) 삭제 확인.
- `node_modules` junction 삭제 확인(원본 무영향).
- 테스트 worktree(SSOT material bridge 포함) `git worktree remove --force`로 제거.
- 4건 fault injection 전부 즉시 원복, 최종 `git status --short` 빈 결과 확인(§8).
- 이번 검토는 실제 Edge 프로세스나 프로필을 생성하지 않았다(§10).
- review-owned residual process/socket/temp DB: 0.
- 구현 worktree는 직접 수정하지 않았다.

## 16. 종료 경계

이 판정은 다음을 승인하지 않는다.

```text
W1_FULL_CLOSURE
W1C
RENDEZVOUS_RUNTIME
SSOT_CHANGE
PUBLIC_SPEC_CHANGE
DEPLOYMENT
ACTIVATION
HUMAN_PASS
```

## 17. 이 문서 자체의 크기·해시

이 줄 바로 위까지("## 17. 이 문서 자체의 크기·해시" 섹션 헤더 포함, 그 이하 내용
제외)를 기준으로 계산한다.

```text
report_byte_count: 18783
report_sha256: 3e715bca1c4feb5899486db8ecabb25b2c4fe3260d513f39e676cc21dbec1490
```

```text
W1B_SUCCESSOR_CANON_CLEAN_CUT_INDEPENDENT_REVIEW_COMPLETED
W1_FULL_CLOSURE_OPEN
W1C_NOT_STARTED
RENDEZVOUS_RUNTIME_PRODUCT_OPEN
SSOT_CHANGE_NOT_AUTHORIZED
PUBLIC_SPEC_CHANGE_NOT_AUTHORIZED
DEPLOYMENT_NOT_AUTHORIZED
ACTIVATION_NOT_AUTHORIZED
HUMAN_PASS_NOT_CLAIMED
```
