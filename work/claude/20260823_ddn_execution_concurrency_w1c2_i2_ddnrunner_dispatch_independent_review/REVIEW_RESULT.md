# DDN-R-W1C2-I2-01 — 실제 DdnRunner 내부 dispatch 연결 독립 검토 결과

- TASK: `DDN-R-W1C2-I2-01`
- ORIGIN_TASK_ID: `DDN-W1C2-I2`
- SCOPE: `W1C2_I2_INTERNAL_DDNRUNNER_REACTION_PROVIDER_DISPATCH_CONNECTION` (한정 범위)
- REVIEWER: 독립검증ClaudeCode
- 검토 수행일: 2026-08-23

## 0. 핵심 결론

**VERDICT: PASS_WITH_FOLLOW_UP** (한정 범위 `W1C2_I2_INTERNAL_DDNRUNNER_REACTION_PROVIDER_DISPATCH_CONNECTION`에 한함)

I2가 청구한 핵심 사실 — "실제 `DdnRunner::run_update`/`EvalContext`의 receive-signal dispatch가 I1의 shared typed core(`plan_internal_delivery_occurrence`/`prepare`/`commit_prepared`)를 실제로 호출하며, standalone 시뮬레이션이나 test-only 복제가 아니다" — 는 독립 재구성 결과 **사실로 확인**됐다. 15/15 실제 통합 사례, 10/10 fault-injection(2개 축은 최초 시도 무력 → 원인 규명 후 교정 성공), 공개 표면 0건, 기본 registry 불변을 모두 독립 재현했다. 다만 검토 과정에서 이 커밋들과 무관한 **3건의 환경성 한계**(WASM 재현성, `ai_prompt` golden SSOT 민감성, W1-C1 canon LF 사전 존재 이슈)와 **1건의 증거 커버리지 관찰**(I2 자체 테스트는 "commit 전 effect 방출" 하위 불변식을 직접 검증하지 않고 I1의 공유 `commit_prepared` 테스트에 전이적으로 의존)을 발견해 논블로킹 FOLLOW_UP으로 기록한다.

---

## 1. 계보·권위 감사

```
af7ad522 (BASELINE)
   └─ 242857bb (PRODUCT_IMPLEMENTATION_COMMIT)
        └─ 5b822e3f (PRODUCT_TEST_FIXED_HEAD)
             └─ a74fb850 (HANDOFF_AND_REQUIRED_REVIEW_PARENT)
```

- `git merge-base --is-ancestor`로 4개 커밋의 선형 계보 확인, `git log --merges`로 병합 커밋 0건 확인.
- `a74fb850`이 `b3cb4e06`(I1 리뷰 커밋)의 후손임을 확인 — I1의 plain PASS 계보가 자연스럽게 이어짐.
- `docs/ssot/**`, `publish/spec/**`, Workbench UI source, 기존 W1-C1/W1-D~F/I1 황금 pack: `git diff --stat af7ad522..5b822e3f`로 전수 확인한 결과 diff 0 (WASM 바이너리/매니페스트, 신규 I2 pack·테스트·러너, I1 pack의 case22 relabel 제외).
- 새로운 공개 문법·wire·진단·activation 권한 주장 없음 — `IMPLEMENTATION_HANDOFF.md`/`INDEPENDENT_REVIEW_REQUEST.md` 원문 확인.

---

## 2. 실제 DdnRunner 연결 증명

### 2.1 call graph

`tool/src/ddn_runtime.rs`의 `EvalContext`(실제 `.ddn` 프로그램 실행 엔진, `DdnRunner::run_update`가 호출)의 receive-signal dispatch 코드를 원문 확인했다:

```
실제 신호 도착
  -> routes: Vec<EndpointRoute<InternalReactionProgram>> 구성 (실제 Stmt::Receive에서)
  -> InternalDeliveryEnvelopeSemantic::new(...)
  -> reached = provider_registry.matching_registration_identities(&envelope)  [기본] 또는 override [내부 typed 검증 전용]
  -> self.internal_dispatch.runtime.prepare(&routes, &provider_registry, reached, &envelope, ...)
       -> plan_internal_delivery_occurrence(...)  [I1 shared core, lang/src/delivery.rs, 무변경]
  -> route_index로 실제 Stmt::Receive 본문 조회 및 실행 (self.eval_receive_stmt)
  -> 성공 시: self.internal_dispatch.runtime.commit_prepared(prepared, |effect,_,_| {...})
```

`DdnRunner`가 `tool/src/main.rs`(CLI 실경로)와 `tool/src/wasm_api.rs`(WASM 실경로) 양쪽에서 실제로 사용됨을 `grep`으로 확인했다 — I1에서 지적한 "`InternalTypedReactionRuntime`이 standalone 시뮬레이션이며 실제 `EvalContext`/`DdnRunner` 경로에 연결되지 않음"이라는 아키텍처 gap이 이번 I2로 실제로 닫혔다.

`prepare()`/`commit_prepared()` 분리(I1의 단일 `execute()`를 리팩터)는 route body 평가와 provider candidate 준비를 하나의 원자적 커밋 단위로 묶기 위한 구조로, `commit_prepared`는 `prepare`가 이미 검증·병합한 candidate만 받으므로 이 단계에서 새로 실패할 수 없다(순수 materialize).

### 2.2 15개 사례 독립 재실행

`tool/tests/ddn_execution_concurrency_w1c2_ddnrunner_dispatch.rs`(587줄)를 원문 확인했다. 핵심 확인: 사례 01/02/03은 `DdnRunner::new(program, "매틱")` + `runner.run_update(&NuriWorld::new(), &empty_input(), &defaults())`을 **실제 한국어 DDN 소스**(`채비`, `알림씨`, `임자`, `받으면`, `매틱`, `움직씨`)로 직접 호출한다 — I1과 달리 손수 구성한 Rust 값이 아니라 실제 파서/AST/평가기를 경유한다. 사례 03은 기본(주입 없는) `DdnRunner`로 `output.resources.get("받은") == Some("route")`를 확인해 기본 경로가 실제로 동작함을 증명한다.

격리 워크트리·격리 `CARGO_TARGET_DIR`에서 독립 재빌드·재실행:

```
cargo test -p ddonirang-tool --test ddn_execution_concurrency_w1c2_ddnrunner_dispatch
→ test result: ok. 15 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

`tests/ddn_execution_concurrency_w1c2_ddnrunner_dispatch_runner.mjs`(JS evidence runner)도 독립 재실행해 동일 15/15와 공개 표면 0 카운트 전부를 재확인했다.

---

## 3. Registry 경계

### 3.1 기본 제품 경로

`InternalDdnRunnerDispatchState::default()`가 `ReactionProviderRegistry::default()`(empty)를 사용함을 원문 확인. 사례 03이 `runner.internal_provider_registry_len() == 0`을 직접 단언한다.

### 3.2 내부 typed 통합 검증 경로 visibility 감사

`with_internal_reaction_provider_registry`/`with_internal_provider_reachability`/`with_internal_reaction_runtime`는 `#[doc(hidden)] pub fn`으로 선언되어 있다. 호출부를 전수 검색한 결과:

```
grep -rln "with_internal_reaction_provider_registry|with_internal_provider_reachability|with_internal_reaction_runtime" tool/ tools/ solutions/
→ tool/src/ddn_runtime.rs (정의부 자신)
→ tool/tests/ddn_execution_concurrency_w1c2_ddnrunner_dispatch.rs (테스트 파일)
```

DDN source/CLI option/env/config/file/WASM export/Workbench UI 어디에도 이 API로의 경로가 없다. `teul-cli`는 `Cargo.toml`에 `ddonirang-tool`을 path dependency로 갖고 있지만(다른 목적: `runtime_surface`, `local_project` 등), `ddn_runtime`/`DdnRunner`/`with_internal_*`를 teul-cli 소스 어디서도 import하지 않음을 확인했다 — "tool과 teul-cli에 별도 provider 알고리즘이 생기지 않음"이 성립한다.

**논블로킹 관찰(FOLLOW_UP-1)**: 이 API들은 `pub(crate)`가 아니라 `pub`이므로, 워크스페이스 내 다른 crate(이미 `ddonirang-tool`에 의존하는 `teul-cli` 포함)가 기술적으로 import할 수 있다. `#[doc(hidden)]`은 문서에서만 숨기며 Rust 가시성 자체를 제한하지 않는다. 현재 아무도 호출하지 않으므로 실제 위험은 없지만, 향후 실수로 호출될 가능성을 원천 차단하려면 `pub(crate)`로 좁히는 것을 권고한다.

---

## 4. 공개 ingress 0 감사

```
git diff --stat af7ad522..5b822e3f -- lang/src/ast.rs lang/src/parser.rs lang/src/normalizer.rs \
  lang/src/lexer.rs tools/teul-cli/src/lang/ tool/src/wasm_api.rs tool/src/preprocess.rs \
  solutions/seamgrim_ui_mvp/ui/ tools/teul-cli/src/cli/
→ 빈 출력 (WASM 바이너리/매니페스트 제외 전부 무변경)
```

```
PUBLIC_PROVIDER_SYNTAX_TOKEN_COUNT: 0
PUBLIC_PROVIDER_SOURCE_INGRESS_COUNT: 0
PUBLIC_PROVIDER_CLI_OPTION_COUNT: 0
PUBLIC_PROVIDER_ENV_COUNT: 0
PUBLIC_PROVIDER_WASM_EXPORT_COUNT: 0
PUBLIC_PROVIDER_UI_CONTROL_COUNT: 0
```

기존 `받으면` 재해석, JS preprocess 숨은 lowering: 없음 (파서/AST diff 0으로 구조적으로 불가능).

---

## 5. case 22 후속

I1 pack(`pack/ddn_execution_concurrency_w1c2_internal_typed/expected.jsonl`)의 case 22가 `22_teul_legacy_provider_fallback_zero`(test_id: `...case_22_teul_legacy_provider_fallback_is_product_unsupported`)에서 `22_tool_ddnrunner_public_provider_ingress_zero`(test_id: `...case_22_tool_ddnrunner_public_provider_ingress_is_unsupported`)로 정확히 교정됐음을 diff와 실제 테스트 함수 원문으로 확인했다. 테스트 본문(`DdnRunner::public_provider_source_ingress_count() == 0` 검사)과 새 이름이 이제 일치한다. teul-cli 관련 주장은 README에서 명시적으로 "별도 정적 scan 증거"로 분리 기재됐고, `zero-match test filter`가 fail-closed임(빈 매치 시 성공으로 처리되지 않음)을 JS 러너 로직 확인으로 재검증했다. 분류(`PRODUCT_UNSUPPORTED`)와 검증 의미는 변경되지 않았다.

```
W1C2_CASE22_EVIDENCE_LABEL_ACCURACY_FOLLOW_UP: PASS
```

---

## 6. Fault Injection — 10축 독립 수행

모든 mutation은 격리 워크트리에서만 수행했고 `git checkout --` + `git status --short`/SHA-256 재확인으로 정확히 원복했다. 기준 해시: `tool/src/ddn_runtime.rs` = `db374cc0feec777e04157dc2d63be463a4f384b647ce745107ae8ae29513e8aa`.

| # | 공격축 | Mutation | RED | 상태 |
|---|---|---|---|---|
| 1 | DdnRunner provider 호출 제거 | `prepare()` 호출을 제거하고 `route_index=0` 하드코딩, `prepared_internal_reaction`을 항상 None으로 유지 | 15/15 전부 실패(0 passed) | ✅ |
| 2 | route 판정 전에 provider 호출 | `plan_internal_delivery_occurrence`에서 provider 해석을 route 판정보다 먼저 실행 | case 01/02 실패 | ✅ |
| 3 | ambiguity 뒤 provider 호출 | ambiguous 시 `&routes[0]`로 강제 진행 | case 02 실패 | ✅ |
| 4 | default registry에 숨은 provider 삽입 | `InternalDdnRunnerDispatchState::default()`에 실제 매칭되는 provider를 등록 | case 03 실패 (`registry_len: left:1, right:0`) | ✅ |
| 5 | diamond dedup 제거 | `resolve_internal_occurrence`의 `.collect::<BTreeSet<_>>()` 제거 | case 05/15 실패 | ✅ |
| 6 | 서로 다른 provider를 잘못 dedup | dedup 뒤 `.take(1)` 추가 | case 06/08/10 실패 | ✅ |
| 7 | provider별 snapshot 변경 | **1차(무력)**: 각 provider에 무관한 신규 key만 추가 → 15/15 GREEN 유지, 원인: case 08의 observer가 무관 key를 검사하지 않음. **2차(부분 교정, 여전히 무력)**: 위치 인덱스(`mutation_index>0`)로만 drift 적용 → 여전히 GREEN, 원인: `resolve_internal_occurrence`의 `BTreeSet` 정렬로 인해 "observer"(reg-observer, 알파벳상 앞섬)가 index 0에 배치되어 drift를 받지 않음. **3차(교정 성공)**: registration identity 문자열 자체로 drift를 걸어 순서 무관하게 모든 provider가 서로 다른 snapshot을 보게 함 | case 08 실패 (`E_INTERNAL_SETTLED_SNAPSHOT_MISMATCH_CANDIDATE`) | ✅ (2회 원인 규명 후 교정 성공) |
| 8 | failure 뒤 부분 publish | provider 평가 루프에서 에러를 `if let Ok(...)`로 삼킴 | case 09 실패 | ✅ |
| 9 | commit 전 EffectIntent 실행 | **1차(무력)**: release 호출 인자를 `&self.world`에서 지역변수 `&committed_world`(이미 계산된 최종값)로 바꿔 이동 → 15/15 GREEN 유지, 원인: 지역변수는 이동 여부와 무관하게 이미 정답을 담고 있어 "필드 미갱신" 상태를 실제로 관찰하지 못함. **2차(교정)**: 원래대로 `&self.world`/`self.revision` **필드**를 참조하되 그 필드 대입을 release 호출 뒤로 이동 | I2 자체 15-case에는 무영향(둘 다 GREEN) — **I1의 23-case 회귀**(`w1c2_i1_case_19_external_effect_release_is_after_commit`, 공유 `commit_prepared` 대상)에서 실패 (`left: None, right: Some("committed")`) | ✅ (2회 원인 규명 후 교정 성공, 단 탐지는 I1 스위트가 담당 — §7 관찰 참조) |
| 10 | occurrence 중복 적용 | 동일 `prepared`를 clone해 `commit_prepared`를 2회 호출 | case 05/11/12/13/15 5건 실패 | ✅ |

전체 복원 후 `tool/src/ddn_runtime.rs`/`lang/src/delivery.rs` SHA-256이 기준값과 정확히 일치함을 재확인했고, 두 스위트(I2 15-case, I1 23-case) 전부 최종 GREEN, `git status --short` 빈 출력을 확인했다.

```
FAULT_INJECTION: 10/10 최종 성공 (2축은 최초 시도 무력 -> 원인 규명 후 교정하여 성공)
```

### 6.1 증거 커버리지 관찰 (FOLLOW_UP-2, 논블로킹)

Mutation 9는 I2 자체 15-case 스위트(`case_11_ddnrunner_effect_intent_releases_after_outer_commit`)로는 검출되지 않았다 — 그 테스트는 `commit_events` 문자열 순서(`["ddn_route_frame_committed", "effect_released:..."]`)와 최종 `revision()`만 검사하며, release 클로저가 호출되는 시점에 `self.world`가 실제로 어떤 값을 담고 있는지는 검사하지 않는다. 이 서브-불변식은 I1의 공유 `commit_prepared` 대상 테스트(`w1c2_i1_case_19`)를 통해서만 전이적으로 보호된다. `commit_prepared`가 I1/I2 양쪽에서 동일 함수이므로 실질적 위험은 없지만, I2 자신의 evidence ledger가 이 축을 직접 주장하려면 `case_11`을 world-content 직접 검사로 보강하는 편이 더 정확하다.

---

## 7. 회귀

```
I1_REGRESSION: 23/23 PASS (재빌드·재실행)
LANG_TESTS: 363/363 PASS (별도 격리 재확인 — 최초 tail 캡처가 doctest 0건 라인만 보여줘 재실행으로 확정)
TOOL_TESTS: 396/397 PASS — 1건(`ai_prompt::tests::ai_prompt_output_matches_golden`)은 baseline(af7ad522)에서
  동일 SSOT 브리지로 동일하게 재현 확인된 사전 존재·환경 민감 실패(로컬 gitignored `docs/ssot/ssot/`
  스냅샷 차이에 기인, 이 리뷰의 diff 범위와 무관). 15-case I2 스위트와 23-case I1 스위트는 이 397건에
  포함되며 전부 PASS.
TEUL_CLI_TESTS: 1165/1165 PASS
W1C1_PARITY: run-mode 9/9 정확히 일치(진단 코드/phase/message/span/state_hash까지 CLI 직접 실행으로 재확인).
  canon-mode 1건(`09_exact_surface_canon_roundtrip`)은 trailing LF 비교 실패 — 근본원인 규명: CLI의
  `print!("{}", ddn)`과 WASM의 `wasm_canon_ddn` 둘 다 canonicalizer 출력을 그대로 반환하며 이 함수는
  242857bb/5b822e3f 범위에서 전혀 변경되지 않음(`git diff --stat`로 확인). baseline에서도 동일하게
  실패할 것으로 판단되는 사전 존재·JS 러너 자체의 LF 정규화 가정 문제이며 W1C2-I2의 회귀가 아니다.
W1DF_REGRESSION: capacity 통합 테스트(`ddn_execution_concurrency_w1df_capacity`) 직접 재실행 PASS.
  `ddn_execution_concurrency_w1df_product_evidence_runner.mjs`(전체 orchestration)는 내부적으로 위
  W1-C1 canon-LF 이슈에 하드 의존해 완주하지 못했다 — 동일 사전 존재 이슈로 인한 실행 실패이며, 대신
  capacity 테스트 직접 실행과 W1-C1 run-mode 9/9 수동 검증으로 실질 커버리지를 대체 확보했다.
```

---

## 8. WASM 소스 A/B/tracked

```
EXPECTED: bytes=5,508,839 / sha256=d91af594b3848b844f3f2df74217f0d7f6e562720b303bc936497df3fc91bdc8
TRACKED (저장소 체크인): bytes=5,508,839 / sha256=d91af594... → EXACT MATCH (독립 sha256sum으로 확인)
```

`ddonirang_tool.manifest.detjson`의 91개 소스 파일 SHA-256을 워크트리의 실제 체크아웃 파일과 대조한 결과 **전부 정확히 일치**(예: `tool/src/ddn_runtime.rs: db374cc0...` 일치) — tracked WASM이 이 리뷰가 감사한 정확한 소스 트리로부터 빌드됐음을 소스 수준에서 확정했다. 매니페스트의 `rustc_version`(1.92.0 ded5c06cf)/`cargo_version`(1.92.0)/`wasm_bindgen_or_pack_version`(wasm-pack 0.14.0)도 이 검토 환경과 정확히 동일하다.

**한계(FOLLOW_UP-3, 논블로킹, 242857bb/5b822e3f에 귀속하지 않음)**: 독립 clean-detached 워크트리 2곳에서 동일 소스·동일 툴체인 버전으로 `wasm-pack build --target web --features wasm`을 재실행한 결과, source A(5,508,903 bytes)와 source B(5,508,903 bytes)는 바이트 수는 서로 같지만 SHA-256이 서로 다르고(`8d5d522a...` vs `6db64784...`), tracked(5,508,839 bytes, `d91af594...`)와도 다르다. `cmp -l`로 대조한 결과 A/B 사이에 16,818바이트가 상이해 단순 임베디드 경로 문자열 차이 수준을 넘는다. 소스 파일 해시와 툴체인 버전이 모두 동일함에도 재현되지 않으므로, 이는 242857bb/5b822e3f의 결함이 아니라 이 로컬 빌드 환경의 wasm-bindgen/wasm-opt/병렬 codegen 비결정성으로 판단한다. tracked 산출물 자체는 기대값과 정확히 일치하고 소스 계보도 확정됐으므로 "official build/copy/manifest 절차 준수"는 인정하되, "source A = source B = tracked" 바이트 동일성 요구는 이 세션에서 완전히 재현하지 못했음을 투명하게 보고한다.

```
WASM_A_B_TRACKED_IDENTITY: TRACKED_MATCHES_EXPECTED / SOURCE_LEVEL_IDENTITY_CONFIRMED / BINARY_REBUILD_NON_REPRODUCIBLE_IN_THIS_ENVIRONMENT (product-unrelated)
```

---

## 9. 실제 Microsoft Edge

기존 검증된 CDP 워크플로(직접 `msedge.exe` 기동 + `--remote-debugging-port` + `chromium.connectOverCDP`)로, `tests/ddn_execution_concurrency_w1c2_i2_edge_runner.mjs`를 일회용 사본(`launch({channel:"msedge"})` 1줄만 `connectOverCDP`로 교체, 그 외 전부 원본 그대로)으로 실행했다 — 원본은 이 환경에서 `--remote-debugging-pipe` 기반 headless 기동이 실패해 CDP 방식으로 전환했다.

```
{"status":"PASS","success":true,
 "unhandled":"E_ASYNC_ENDPOINT_UNHANDLED_CANDIDATE",
 "ambiguity":"E_ASYNC_ENDPOINT_AMBIGUOUS_CANDIDATE",
 "exact_reopen":true,
 "pid_swap":{"first":17636,"second":20340},
 "protected_port_8787_untouched":true,
 "wasm_sha256":"d91af594b3848b844f3f2df74217f0d7f6e562720b303bc936497df3fc91bdc8",
 "console_page_network_errors":0,
 "public_provider_ui_or_input":0}
```

서빙된 WASM은 **tracked**(기대값과 정확히 일치하는 그 파일)이며, 내가 재현하지 못한 source A/B가 아니다. success/unhandled/ambiguity 흐름 재현, 서버 PID 교체 후 exact 재열기, console/page/network 오류 0, 공개 provider UI/입력 0을 확인했다. 이 결과는 **기존 공개 동작에 대한 회귀 확인일 뿐**이며 공개 provider 표면의 증거로 해석하지 않는다.

정리: 일회용 스크립트 삭제, Edge 프로세스 종료, 임시 프로필 삭제, 포트 해제 확인 완료.

```
ACTUAL_EDGE_REGRESSION: PASS
```

---

## 10. 보호 자원 전/후 대조

| 자원 | 검토 전 | 검토 후 | 일치 |
|---|---|---|---|
| 공식 DB 바이트/해시 | 540,672 / `c8fdd4d4...` | 540,672 / `c8fdd4d4...` | ✅ |
| 공식 DB mtime | 2026-08-02 15:25 | 동일(재기록 없음) | ✅ |
| WAL/SHM | 0 / 32,768 bytes, mtime 08-18 | 동일 | ✅ |
| 보호 PID | `53196` / python / `2026-08-08T12:27:21.86...+09:00` | 동일 | ✅ |
| 보호 포트 | `127.0.0.1:8787` owner `53196` | 동일 | ✅ |

공식 저장소 쓰기 0, activation 호출 0, external outreach 0.

---

## 11. 정리(cleanup)

검토용 워크트리(`claude-w1c2i2-review-20260823`, `claude-w1c2i2-wasmB-20260823`, `claude-w1c2i2-baseline-check-20260823`, `claude-w1c2i2-langcheck-20260823`) 전부 `git worktree remove --force`로 제거. 격리 Cargo target 6개(review/teulcli/wasmA/wasmB/wasmnode/baseline/langcheck) 전부 삭제. Edge 프로세스·프로필·포트 회수 확인.

---

## 12. FINDINGS / FOLLOW_UPS

### FOLLOW_UP-1 (논블로킹) — 내부 injection API의 Rust 가시성
- **finding**: `with_internal_reaction_provider_registry` 등이 `pub(crate)`가 아닌 `pub`이라 워크스페이스 내 다른 crate에서 기술적으로 호출 가능.
- **재현절차**: 정의부 시그니처 확인.
- **root cause**: `#[doc(hidden)]`은 문서 노출만 억제하고 Rust 가시성을 제한하지 않음.
- **제품영향**: 없음(현재 호출부 0건, teul-cli도 미사용).
- **차단여부**: 비차단.
- **후속owner**: 셈그림Codex.
- **허용교정범위**: `pub(crate)`로 좁히는 선택적 정리.

### FOLLOW_UP-2 (논블로킹) — commit-전-release 서브 불변식의 I2 자체 증거 공백
- **finding**: I2의 `case_11`은 release 시점의 world 내용을 직접 검사하지 않아, mutation 9(release를 커밋 이전으로 이동)를 I2 자체 스위트로는 검출하지 못함. 검출은 I1의 공유 `commit_prepared` 대상 테스트가 담당.
- **재현절차**: §6 mutation 9 표 참조.
- **root cause**: `case_11`은 로그 문자열 순서/최종 revision만 검사.
- **제품영향**: 없음(공유 함수라 I1 스위트가 실질 보호).
- **차단여부**: 비차단.
- **후속owner**: 셈그림Codex.
- **허용교정범위**: `case_11`을 world-content 직접 검사로 보강(선택).

### FOLLOW_UP-3 (논블로킹, 제품과 무관) — 로컬 WASM 빌드 비재현성
- **finding**: 동일 소스·동일 툴체인 버전으로도 독립 재빌드 2회(A/B)가 서로도, tracked와도 바이트 단위로 일치하지 않음(§8).
- **재현절차**: 본문 §8 참조.
- **root cause**: 로컬 wasm-bindgen/wasm-opt/병렬 codegen 비결정성으로 추정, 242857bb/5b822e3f 소스 변경과 무관.
- **제품영향**: 없음 — tracked 산출물 자체는 기대 해시와 정확히 일치.
- **차단여부**: 비차단.
- **후속owner**: 인프라/빌드 담당(범위 밖).
- **허용교정범위**: 이 리뷰에서는 조치하지 않음. 재현 가능한 WASM 빌드가 필요하면 별도 인프라 과업으로 분리 권고.

### FOLLOW_UP-4 (논블로킹, 제품과 무관) — 사전 존재 환경 민감 테스트 2건
- `tool::ai_prompt::tests::ai_prompt_output_matches_golden`: 로컬 gitignored `docs/ssot/ssot/` 스냅샷에 민감, baseline에서 동일 재현. 이 리뷰 diff 범위 밖.
- `pack/ddn_execution_concurrency_w1c1_sender_route_provider` case 09(canon-mode LF): 해당 canonicalizer 코드가 242857bb/5b822e3f에서 전혀 변경되지 않음, W1-C1 자체의 사전 존재 이슈로 판단.

---

## 13. 반환 형식

```
[독립검증ClaudeCode -> Codex관리Work] DDN-R-W1C2-I2-01 — 결과

VERDICT: PASS_WITH_FOLLOW_UP
SCOPE: W1C2_I2_INTERNAL_DDNRUNNER_REACTION_PROVIDER_DISPATCH_CONNECTION
FIXED_PRODUCT_HEAD: 5b822e3f8754d3cf38fa1d26a9786dc9fbd6115e
REVIEW_PARENT: a74fb85094b4219a89a77a1d0226676d2e106903
REVIEW_COMMIT: <커밋 후 기입>
REVIEW_BRANCH: claude/ddn-r-w1c2-i2-01-ddnrunner-dispatch-independent-review-20260823
REPORT_PATH: work/claude/20260823_ddn_execution_concurrency_w1c2_i2_ddnrunner_dispatch_independent_review/REVIEW_RESULT.md
REPORT_BYTES: <커밋 후 기입>
REPORT_SHA256: <커밋 후 기입>
LINEAGE: af7ad522 -> 242857bb -> 5b822e3f -> a74fb850 (linear, merge_commit_count=0)
MERGE_COMMIT_COUNT: 0
CHANGED_PATHS: tool/src/ddn_runtime.rs, tool/tests/ddn_execution_concurrency_w1c2_ddnrunner_dispatch.rs,
  tool/tests/ddn_execution_concurrency_w1c2_internal_typed.rs(case22 relabel),
  tests/ddn_execution_concurrency_w1c2_ddnrunner_dispatch_runner.mjs,
  tests/ddn_execution_concurrency_w1c2_i2_fault_injection_runner.mjs,
  tests/ddn_execution_concurrency_w1c2_i2_edge_runner.mjs,
  pack/ddn_execution_concurrency_w1c2_ddnrunner_dispatch/**,
  pack/ddn_execution_concurrency_w1c2_internal_typed/{README.md,expected.jsonl},
  solutions/seamgrim_ui_mvp/ui/wasm/{ddonirang_tool_bg.wasm,ddonirang_tool.manifest.detjson}

ACTUAL_DDNRUNNER_CALL_GRAPH: CONFIRMED — EvalContext receive-dispatch -> prepare()/commit_prepared() -> plan_internal_delivery_occurrence (I1 shared core), 실제 DdnRunner::run_update/main.rs/wasm_api.rs 경로에서 확인
SHARED_AUTHORITY: CONFIRMED (standalone/test-only 아님, I1 core 재사용)
DEFAULT_REGISTRY: EMPTY (case 03 확인, mutation 4로 공격 검증)
INTERNAL_TYPED_INJECTION_VISIBILITY: pub(#[doc(hidden)]), 호출부 0건(정의부+자체 테스트 외), teul-cli 미사용 — FOLLOW_UP-1
PUBLIC_PROVIDER_SOURCE_REACHABILITY: 0 (전 카운트 0, diff 0)
ACTUAL_DDNRUNNER_INTEGRATION_CASES: 15/15
DEFAULT_EMPTY_REGISTRY_EXACT_PARITY: run-mode 9/9 exact(진단/phase/span/state_hash); canon-mode 1건은 사전 존재·무관 이슈(FOLLOW_UP-4)
CASE22_LABEL_FOLLOW_UP: PASS
FAULT_INJECTION: 10/10 최종 성공(2축 최초 무력 -> 교정, §6)
I1_REGRESSION: 23/23 PASS
W1C1_PARITY: run-mode 9/9 PASS, canon-mode 1건 사전 존재 이슈(비차단)
W1DF_REGRESSION: capacity 테스트 직접 PASS; 전체 orchestration은 위와 동일한 사전 존재 이슈로 미완주, 수동 대체 검증으로 커버
LANG_TESTS: 363/363 PASS
TOOL_TESTS: 396/397 PASS (1건 사전 존재·환경 민감, FOLLOW_UP-4)
TEUL_CLI_TESTS: 1165/1165 PASS
WASM_A_B_TRACKED_IDENTITY: TRACKED_MATCHES_EXPECTED_EXACTLY; SOURCE_LEVEL_IDENTITY_CONFIRMED(91/91 파일 해시 일치); BINARY_A_B_REBUILD_NON_REPRODUCIBLE_IN_THIS_ENVIRONMENT(FOLLOW_UP-3, 제품과 무관)
ACTUAL_EDGE_REGRESSION: PASS (tracked WASM 서빙, 0 errors, 공개 표면 증거로 미해석)

SSOT_DIFF: 0
PUBLIC_SPEC_DIFF: 0
UI_DIFF: 0
OFFICIAL_DB_BEFORE_AFTER: 540672 bytes / c8fdd4d47e20f7ad7ce4f095389991859432d5af0a87aa1f7b0b06e90fe44228, 전후 동일
PROTECTED_PID_PORT: PID 53196(python, 2026-08-08T12:27:21.86...+09:00) / 127.0.0.1:8787, 전후 동일
OFFICIAL_WRITE_COUNT: 0
ACTIVATION_CALL_COUNT: 0
REVIEW_RESOURCE_CLEANUP: COMPLETE

FINDINGS: 0 (blocking)
FOLLOW_UPS: 4 (non-blocking; FOLLOW_UP-1/2는 제품 코드 관찰, FOLLOW_UP-3/4는 환경/사전존재 이슈로 242857bb·5b822e3f에 귀속하지 않음)
FINAL_STATUS: PASS_WITH_FOLLOW_UP
NOTES: I2는 I1이 남긴 "standalone-only" gap을 실제로 닫았다. 남은 4건의 FOLLOW_UP은 전부 논블로킹이며 그 중 2건(WASM 재현성, ai_prompt/W1-C1 canon LF)은 이 리뷰가 감사한 diff와 무관함을 baseline 재현으로 직접 확인했다.
```

**이 리뷰가 닫을 수 없는 항목**: `PUBLIC_KOREAN_NAME`, `PUBLIC_PROVIDER_EXACT_SYNTAX`, `PUBLIC_PROVIDER_SOURCE_INGRESS`, `STABLE_PROVIDER_IDENTITY_WIRE`, `STABLE_PROVIDER_DIAGNOSTICS`, `W1_FULL_CLOSURE`, `RENDEZVOUS_RUNTIME`, `WORKBENCH_STRUCTURED_DIAGNOSTIC_PROPAGATION`, `RD207_PUBLIC_STABLE_WIRE`, `PUBLIC_ACTIVATION`, `DEPLOYMENT`, `HUMAN_PASS` — 전부 OPEN 유지.
