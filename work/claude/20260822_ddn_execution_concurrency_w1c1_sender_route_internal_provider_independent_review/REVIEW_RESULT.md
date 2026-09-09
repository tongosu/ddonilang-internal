# CT-CLAUDE-DDN-EXECUTION-CONCURRENCY-W1C1-INDEPENDENT-REVIEW — 결과

## 0. 결론 (VERDICT)

**VERDICT: PASS_WITH_FOLLOW_UP**

W1-C1 "sender-route/internal-provider" 구현은 지시문의 Section 2~13 요구사항을 실측/실행/실패주입/실제 Edge 검증으로 독립 재현하여 확인했다. 차단(BLOCKER) 결함은 발견되지 않았다. 비차단(non-blocking) 후속 사항 2건을 기록한다(§9-F1, §11-F1). `PASS`가 아닌 `PASS_WITH_FOLLOW_UP`을 부여하는 이유는 이 두 후속 사항 때문이며, 둘 다 W1-C1의 핵심 의미론(센더 필터, 라우트 식별, 내부 provider 경계)에 대한 결함이 아니라 (a) 기존 CLI 출력 관례와 신규 파리티 러너 어서션 간의 문자열 비교 엄격도 불일치, (b) W1-C1 진단 코드가 아직 손대지 않은(out-of-scope) Workbench UI 계층까지는 전파되지 않는 사전 존재 UI 설계임을 확인했다.

---

## 1. 고정 좌표 및 계보 (Section 3)

```
PRODUCT_FIXED_HEAD:            da791953f51a38e9489d0b2a158eeb419645fd43
IMPLEMENTATION_HANDOFF_COMMIT: e613537706b45b184f3615a43cde824a78b71eb3
FINAL_REVIEW_REQUEST_COMMIT:   6d84137aa6aa560e958d2e9cf5046da569bc8d69
EXPECTED_PRODUCT_WASM_SHA256:  7106d312993408029404db967d100fdb6838192daef9e38bc45e2aa8acd7a6e7
```

계보 확인 (`git log --format='%H %P'`):

```
e613537706b45b184f3615a43cde824a78b71eb3  <- parent da791953f51a38e9489d0b2a158eeb419645fd43   (핸드오프, docs-only, 단일부모)
6d84137aa6aa560e958d2e9cf5046da569bc8d69  <- parent e613537706b45b184f3615a43cde824a78b71eb3   (최종 리뷰 요청, docs-only, 단일부모)
```

모두 단일 부모(병합 커밋 0). 리포트 브랜치는 `6d84137a...`를 부모로 하는 새 워크트리에서 생성했다(§8).

W1-C1 순수 구현 diff 범위(`57f3f5d3`→`da791953`, 6개 구현 커밋):

```
963c7c88 feat(lang): add semantic sender and route identities
d874dc0d feat(tool): enforce semantic sender endpoint routes
1a6c2932 feat(lang): add internal reaction provider occurrence authority
6bfbeee8 fix(tool): isolate successor routes from historical hooks
2ec750aa test(concurrency): add W1-C1 native WASM oracle
da791953 feat(tool): structure async candidate diagnostics
```

`57f3f5d3`는 W1-B 리뷰 체인(`c61bdfef → 0d8ca402 → 97fe787b → 7610e4bf`)을 포함한 사전 상태이며, W1-C1 diff와 명확히 분리했다.

변경 파일 인벤토리 (`git diff --stat 57f3f5d3 da791953`, 23 files / +1356 / -104):

```
lang/src/ast.rs                                              |   5 +
lang/src/delivery.rs (신규 타입 대부분)                       | 465 ++++++++++++++++++++-
lang/src/lexer.rs ("에게서" 조사 추가)                        |  44 +-
lang/src/lib.rs (재수출 + RD-203 possessive fix)              |  49 ++-
lang/src/normalizer.rs (canon 분기 + normalize_expression_identity) | 67 ++-
lang/src/parser.rs (sender-filter 파싱)                       | 153 ++++++-
pack/ddn_execution_concurrency_w1c1_sender_route_provider/00~09/input.ddn (10개) |  63 (합계)
pack/ddn_execution_concurrency_w1c1_sender_route_provider/README.md |   9 +
pack/ddn_execution_concurrency_w1c1_sender_route_provider/expected.jsonl |  10 +
solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson |  38 +-
solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm (바이너리) | 5439334 -> 5467851 bytes
tests/ddn_execution_concurrency_w1c1_sender_route_provider_runner.mjs (신규) | 145 +++++++
tool/src/ddn_runtime.rs (라우팅/센더/provider 배선)            | 409 +++++++++++++++---
tool/src/runtime_surface.rs (phase 필드 배선)                  |   3 +-
```

`docs/ssot/**`, `publish/spec/**`, `tools/teul-cli/**`, W1-B 히스토리컬 팩(`pack/ddn_execution_concurrency_w1b*`), Seamgrim Workbench UI 소스(`solutions/seamgrim_ui_mvp/ui/workbench/**`, `ui/index.html`)에 대해 개별 `git diff --stat`를 실행했고 전부 **0바이트 출력(변경 없음)**을 확인했다. 유일하게 변경된 UI 관련 파일은 추적 WASM 바이너리 자체(엔진 재빌드 산출물)와 그 manifest이며, 이는 새 문법이 브라우저에서 동작하려면 필연적으로 필요한 재빌드이지 UI 소스 변경이 아니다.

---

## 2. 선행 권위 게이트 (Section 2)

**(1) W1-B 독립 PASS 결속 확인**

`c61bdfef` (W1-B PASS 종료 결속 커밋)을 `git show`로 재확인. 인용된 나의 W1-B 리뷰 커밋 `0d8ca402e90cea2688f38641bfb872e91a041d0a`, 리포트 바이트 수 19,178, SHA-256 `3bf6db0ede1792497d3a3bbc19db60ef7cb74d24a3a018495c4543bc89818f9e`가 실제 리포트 파일과 정확히 일치함을 재검증했다(이번 세션 초반에 완료, 결과 불변). W1-B 고정 HEAD `7610e4bfda5c322e65cf6df9a5af45e58e0ab4bf`에 순수 PASS(조건부 아님)가 결속되어 있음을 확인했다. → 게이트 통과.

**(2) W1-C1 Owner 결정 결속과 구현 범위 일치**

`work/codex/20260822_ddn_execution_concurrency_w1c_w1f_async_closure/OWNER_DECISION_BINDING.md`(커밋 `57f3f5d3`)를 전문 대조했다. 명시된 W1-C1 범위(센더 필터 구문, `RouteIdentity` 5요소 구조, 내부 `ProviderIdentity`, `누리` 폴백 제거, 히스토리컬 훅 비간섭)와 실제 구현 diff가 1:1로 대응함을 §3의 파일별 코드 감사로 확인했다. `MIGRATION_OWNERSHIP_MAP.md`는 `tools/teul-cli/**` 비접촉을 명시했고 실제로도 diff 0. → 게이트 통과.

두 게이트 모두 통과했으므로 `REWORK / BLOCKER: W1B_INDEPENDENT_PLAIN_PASS_NOT_BOUND` 사유는 발생하지 않는다.

---

## 3. 센서-필터 의미론 (Section 4) — 코드 감사 + 실행 검증

- `lang/src/delivery.rs`: `SenderIdentityPredicate` = `AnySender | Exact(String)`. `canonical_material()` → `"ANY_SENDER"` / `"EXACT:{len}:{value}"`. 센더 필터 없는 수신은 항상 `AnySender`로 정규화됨을 코드와 유닛 테스트로 확인.
- `tool/src/ddn_runtime.rs`: 센더 신원은 배달 envelope/context에 보존되고 payload에 섞이지 않음(별도 필드로 전달, `EndpointRouteSemantic::new(receiver, message_type, sender_predicate, payload_predicate, owner_identity)` 시그니처가 5요소를 구조적으로 분리).
- **`누리` 폴백 제거 확인**: 과거 `.unwrap_or_else(|| "누리".to_string())` 패턴이 완전히 삭제되고 `.or_else(|| self.current_owner_identity.clone()).ok_or_else(|| E_ASYNC_SENDER_IDENTITY_UNRESOLVED_CANDIDATE)`로 대체됨을 diff에서 직접 확인. 즉 임자 컨텍스트 밖에서 센더를 해석할 수 없으면 임의 신원을 대입하지 않고 실패로 닫힌다(fail-closed).
- 표시 문자열/소스 스팬/선언 순서/벡터 인덱스가 센더 신원으로 쓰이지 않음을 `route_identity()` 구현(문자열 canonical_material만 해싱, span/NodeId 없음)에서 확인. `normalizer.rs`의 `normalize_expression_identity()` 독트스트링도 "Spans and NodeIds are deliberately absent"를 명시.
- **실행 재현**: 원 pack의 `04_top_level_sender_missing`(오너 컨텍스트 밖에서 센더 생략) 케이스가 `E_ASYNC_SENDER_IDENTITY_UNRESOLVED_CANDIDATE`로 실패함을 official parity runner를 통해 재확인(§9). `05_owner_context_sender_success`는 임자 본문 안에서 암묵적 센더로 성공함을 재확인.
- 같은 의미의 입력이 canon 이후 같은 typed identity로 수렴함을 `09_exact_surface_canon_roundtrip` 케이스로 재확인(§9의 case 09 논의 참고).

결함 없음.

---

## 4. EndpointRoute 조정 (Section 5) — 코드 감사 + 실행 검증 + 실패주입

`RouteIdentity`는 `lang/src/delivery.rs`의 `route_identity()`에서 정확히 5요소만을 `canonical_text()`로 NFC 정규화한 뒤 blake3 해시로 구성한다:

```
[receiver_identity, message_type, sender_predicate.canonical_material(), payload_predicate, owner_identity]
```

소스 스팬, 선언 순서, 벡터 인덱스는 입력에 포함되지 않는다. `select_exactly_one_endpoint`류 함수는 매칭된 라우트 **개수**로 0/1/2+를 판정하며, 동점 시 등록 순서로 첫 번째를 고르는 폴백이 없음을 코드에서 확인(2+ 매칭 시 명시적 ambiguity 오류로 귀결).

official 10-case corpus(§9)로 다음 카디널리티를 모두 실측했다:
- `00_any_sender_builtin_success` — 1-route, ANY_SENDER
- `01_exact_sender_success` — 1-route, EXACT 센더
- `02_sender_mismatch_unhandled` — 0-route(`E_ASYNC_ENDPOINT_UNHANDLED_CANDIDATE`)
- `03_sender_type_matrix_success` — 여러 타입 조합에서 정확한 1-route 선택
- `07_duplicate_route_ambiguity` — 의미적으로 동일한 두 소비 라우트 → 2+-route ambiguity 오류(첫 매치 성공으로 폴백하지 않음)

**실패주입 (Mutation 2 — route-ambiguity를 first-match 성공으로 변조)**: `lang/src/delivery.rs`의 ambiguity 판정 분기를 `if routes.len() >= 1 { Ok(routes[0]) }`류로 바꿔 `cargo test -p ddonirang-lang`을 재실행 → `equal_consuming_routes_remain_ambiguous` 등 유닛 테스트가 RED로 전환됨을 확인. 이후 `git checkout -- lang/src/delivery.rs`로 복구하고 SHA-256이 변조 전과 정확히 일치함을 확인, 재빌드 후 GREEN 재확인.

**실패주입 (Mutation 4 — 선언 순서/소스 스팬을 RouteIdentity에 혼입)**: 최초 시도로 `tool/src/ddn_runtime.rs`의 라우트 등록 호출부에서 반복 인덱스를 `owner_identity` 자리에 흘려보내는 변조를 가했으나 `tool --lib` 491/491 테스트가 그대로 통과하고 케이스 07 실측 결과도 무변화였다 — 이는 `select_exactly_one_endpoint`의 카디널리티 판정이 `Vec` 길이 기반이지 `RouteIdentity` 동등성 기반이 아니기 때문임을 근본 원인으로 특정했다. **교정된 변조**로 `lang/src/delivery.rs`의 `route_identity()` 자체에 정적 `AtomicU64` 호출-순서 카운터를 해시 입력에 섞어 넣었더니, `cargo test -p ddonirang-lang`에서 `route_identity_is_semantic_nfc_and_not_source_order`, `equal_consuming_routes_remain_ambiguous` 2건이 정확히 RED로 전환됨을 확인. `git checkout --`로 복구, SHA-256 일치 확인, 재빌드 GREEN 재확인.

두 실패주입 모두 "라우트가 등록 순서/벡터 인덱스로 폴백하지 않는다"는 요구사항이 실제 방어층에서 강제되고 있음을 실측으로 증명했다. Mutation 4의 최초 시도가 무효했던 사실과 그 이유, 교정 경로를 있는 그대로 기록한다(은폐하지 않음).

결함 없음.

---

## 5. 내부 ReactionProvider 경계 (Section 6) — 코드 감사

- `tool/src/ddn_runtime.rs`에서 `ReactionProviderRegistry::<()>::default()`로 항상 **빈 레지스트리**가 생성되고, `fan_out`은 no-op임을 확인. W1-C1은 공개 provider 선언 구문을 전혀 추가하지 않았다 — `lang/src/parser.rs`, `lang/src/ast.rs` diff 어디에도 새로운 공개 provider 선언 토큰/문법이 없다.
- `ProviderIdentity::derive(module_owner_identity, declaration_identity)`는 내부 전용 타입이며 공개 API로 재수출되지 않았다(`lang/src/lib.rs`의 재수출 목록에 없음).
- `canonical_provider_occurrences()`는 `BTreeSet` 기반으로 같은 `ProviderIdentity`의 다이아몬드 발견을 1회로 dedupe하고, 서로 다른 `ProviderIdentity`는 non-consuming fan-out으로 모두 실행되도록 설계되어 있다(코드 레벨 확인, 레지스트리가 항상 비어 있어 실행 시 실제로 관측되는 provider는 0개).
- `plan_delivery_occurrence()`가 라우트 카디널리티를 **먼저** 결정하고 provider 해석은 **그 다음**임을 함수 본문 순서로 확인 — 라우트 실패가 provider 실패보다 항상 선행한다.
- 역사적 receive 훅이 provider로 자동 승격되지 않음(§6 코드 경로가 `payload_type` 존재 여부로 완전히 분리되어 있어 자동 승격 지점 자체가 없음).
- W1-C1 diff 어디에도 provider 실행 순서를 사용자 관측 가능한 계약으로 노출하는 코드가 없다(내부 순서만 존재, 공개 API/출력에 노출 안 됨).

W1C2(공개 provider 표면)는 전혀 선점되지 않았다 — 결함 없음, `W1C2_REACTION_PROVIDER_PUBLIC_SURFACE`는 여전히 OPEN.

---

## 6. 히스토리컬 마이그레이션 비간섭 (Section 7) — 코드 감사 + 실행 검증

- `tool/src/ddn_runtime.rs`: `let Some(payload_type) = payload_type.as_deref() else { continue; };` — `payload_type`이 없는(레거시 `kind`/`binding`/`condition`-only) receive 문은 라우트 등록 자체에서 스킵됨을 확인. 자동 재작성 코드 없음.
- `pack/ddn_execution_concurrency_w1c1_sender_route_provider/06_historical_hook_not_successor`가 이를 정확히 실측 검증한다(§9에서 재실행, 결과 오라클과 일치).
- W1-B의 `<~/~>` 비동기 vs `<~~/~~>` rendezvous 클린컷 코드(§3에서 diff 0 확인된 W1-B 히스토리컬 팩과 함께)는 전혀 건드리지 않았다.
- W1-C1의 센서 라우트가 rendezvous나 historical-async 신원과 병합되는 코드 경로 없음(별도 타입 `MessageTransfer` variant 체계가 그대로 유지됨, diff에 `MessageTransfer` enum 변경 없음).

결함 없음.

---

## 7. 진단 계약 (Section 8) — 코드 감사 + 실행 검증

- `EvalError::AsyncCandidate { code, phase, message, span }` variant가 신설되었고, phase는 `async_sender_identity` / `async_route` / `async_provider` / `async_queue_wait` 4종으로 분리됨을 diff에서 확인.
- `tool/src/runtime_surface.rs`: `error.diagnostic_phase()`가 외부 관측 가능한 `ExecutionDiagnostic.phase` JSON 필드로 배선됨을 3줄 diff에서 확인.
- 모든 신규 진단 코드가 `_CANDIDATE` 접미사를 사용함(`E_ASYNC_ENDPOINT_UNHANDLED_CANDIDATE`, `E_ASYNC_SENDER_IDENTITY_UNRESOLVED_CANDIDATE` 등) — house style에 따라 공개/안정 권위로 승격되지 않았음을 명명 자체가 신호한다.
- **실행 재현**: 리뷰 워크트리에서 직접 작성한 센더 불일치 소스(`(영희)의 7 ~> 관제탑`, 관제탑은 `철수`만 수신)를 `run` 서브커맨드로 실행 →

  ```
  {"code":"E_ASYNC_ENDPOINT_UNHANDLED_CANDIDATE","message":"matching route count is 0","phase":"async_route","source_span":{"start":129,"end":156},...}
  STATUS=1
  ```

  구조화된 JSON, 정확한 phase(`async_route`), 유효한 source_span(end>start)을 실측으로 확인. 이는 official parity runner의 `assertCandidateDiagnostic()`이 10-case corpus 전체에서 검증하는 것과 동일한 계약이다(§9).
- 진단 렌더러/메시지 표현 변경이 성공/실패 판정에 영향을 줄 수 있는지 확인: 판정은 `native.status`(프로세스 종료 코드) 및 WASM 쪽 `ok`/`error` boolean에 의해 결정되며 진단 문자열 내용과 독립적임을 러너 코드에서 확인 — 렌더링 문구를 바꿔도 성공/실패 판정 자체는 불변.

결함 없음.

---

## 8. 독립 실행 재현 (Section 9)

격리된 `git worktree --detach da791953f51a38e9489d0b2a158eeb419645fd43`와 두 개의 격리된 `CARGO_TARGET_DIR`(`target-claude-w1c1-review-20260822`: tool/lang 전용, `target-claude-w1c1-teulcli-20260822`: teul-cli 전용)를 처음부터 분리하여 시작, 이전 세션들에서 반복 발견된 serde_json 버전 충돌 링크 오류를 재현 없이 회피했다.

실측 결과:

| 항목 | 결과 |
|---|---|
| `cargo test -p ddonirang-lang` (전체) | 357 passed; 0 failed; 0 ignored (doc-tests 0) |
| `cargo test -p ddonirang-tool --lib` (전체) | 491 passed; 0 failed |
| `cargo test --manifest-path tools/teul-cli/Cargo.toml` (전체) | 1161 passed; 0 failed |
| `wasm-pack build --target web -- --features wasm` | 성공, `tool/pkg` 생성 |
| `wasm-pack build --target nodejs -- --features wasm` | 성공, `tool/pkg-nodejs` 생성 |
| `cargo check --target wasm32-unknown-unknown` | 통과 |
| W1-C1 10-case 오라클 + official parity runner | 아래 §9-F1 참고 |
| 소스 빌드 WASM ↔ 추적 Workbench WASM ↔ 네이티브 CLI 3-frontdoor 파리티 | 케이스 00~08 전건 일치(canon/summary/diagnostic 동일) |
| clean-detached WASM 바이트 신원 | `tool/pkg/ddonirang_tool_bg.wasm` SHA-256 = 추적 `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm` SHA-256 = `EXPECTED_PRODUCT_WASM_SHA256` = `7106d312993408029404db967d100fdb6838192daef9e38bc45e2aa8acd7a6e7` (5,467,851 bytes) — 3자 완전 일치 |
| 배포 산출물 최신성 | 추적 WASM이 리뷰 워크트리에서 clean-detached로 재빌드한 바이트와 정확히 동일 — 오래된 산출물 없음 |

**§9-F1 (비차단, 근본 원인 특정 완료): official parity runner의 case 09(`09_exact_surface_canon_roundtrip`, mode: canon)에서 `assert.equal(sourceBuilt.wasm_canon_ddn(source), native.stdout, ...)`가 실패했다.** 원인을 `tool/src/main.rs`의 `run_canon()`(W1-C1 diff에 포함되지 않은, 기존 CLI 코드)에 있는

```rust
if !output_body.ends_with('\n') { output_body.push('\n'); }
```

로 정확히 특정했다. 이는 파일 출력과 stdout 표시 모두에 적용되는, W1-C1 이전부터 존재하던 CLI 표시 관례다. 독립 Node 스크립트로 `native.stdout === wasm_output + "\n"`이 정확히 성립함을 실측 확인 — 즉 **정본 텍스트는 바이트 단위로 완전히 동일**하고, 러너의 문자열 비교(trim 없는 `assert.equal`)가 이 표시상의 개행 관례보다 더 엄격했을 뿐이다. case 00~08(센더 필터/라우트/진단 관련 실질 검증)은 case 09보다 먼저 순서대로 통과했으므로 이 실패는 제품/의미론 회귀가 아니라 신규 테스트 하네스의 어서션이 기존의 무관한 CLI 관례와 부딪힌 것이다. **후속 조치 제안**: 러너의 canon 비교에 trailing-newline 정규화(혹은 `.trimEnd()`)를 추가하거나, `run_canon()`의 개행 강제 로직을 exit 전용으로 분리.

---

## 9. 실제 Microsoft Edge 검증 (Section 11)

전용 W1-C1 Edge 러너가 저장소에 없어, 이미 검증된 `tests/ddn_workcostv1_standard_limits_w1_edge_runner.mjs`(원본 SHA-256 `c0721401c36aa3bb30e9d099643541155a6fb39e281b27e4fea70d5df721b712`, 이 리뷰 내내 원본 자체는 변경하지 않음)의 흐름을 **일회용 사본**(`tests/_claude_w1c1_edge_verification_disposable.mjs`, 추적 원본과 완전 분리, 사용 후 삭제·git status 클린 재확인)으로 이식했다. DDN 소스만 W1-C1 센더-필터 프로그램으로 교체하고, 브라우저 연결부만 `chromium.launchPersistentContext({channel:"msedge",...})` → 격리 CDP 연결(`chromium.connectOverCDP(...)`)로 교체했다.

**실제 Edge 인스턴스**: PowerShell `Start-Process msedge.exe`로 격리 프로필(`%TEMP%\claude_edge_w1c1_profile`)·격리 포트(47901, 보호 포트 8787과 무관)에서 headless 실행, `/json/version`으로 `Edg/151.0.4129.86` 확인(진짜 Edge, Chromium 대체 아님).

실측 결과(스크립트 자체 출력 JSON, `ok: true`, `errors: []`):

| 확인 항목 | 결과 |
|---|---|
| WASM 신원/영수증 | `wasm_sha256 = 7106d312...a6e7` (EXPECTED와 일치), `wasm_bytes = 5467851`, `deterministic_rerun: true` |
| 정상 센서-필터 실행 결과 `7` | `first_run.result = 7` ✅ |
| 성공 뒤 state_hash | `blake3:352bd266...` (두 성공 실행에서 동일 — 이유는 아래 참고) |
| 구조화된 mismatch diagnostic | `failure_atomicity.lifecycle = "failed"`, `diagnostic_code = "E_PRIMARY_VIEW_DECISION_MISSING"`, `severity = "warning"` — §11-F1 참고 |
| 실패 뒤 partial state mutation | `activeFrame === null`, `stale_result_count: 0`, 캔버스/결과 표면 잔존 0건 |
| 수정 뒤 실행 결과 `10` | `repaired_run.result = 10` ✅ |
| PID 교체 뒤 동일 결과 | `old_pid 72888 → new_pid 36852`, `exact_revision: true`, `result: 10` (재개 후 정확한 리비전) ✅ |
| 이식/오프라인 가져오기 | `source_exact: true`, `result: 10`, mobile overflow 0/0 |
| console/page/network 오류 | `errors: []` (전 구간 0건) ✅ |
| 보호 자원 | `protected_port_8787_used: false`, `official_store_writes: 0` |

**state_hash가 결과 7과 10 사이에서 동일한 이유(결함 아님)**: 두 실행 모두 `(받은수: 받은수) 보임.`(순수 관측/Bogae 출력)만 수행하고 영속 Nuri 상태를 갱신하지 않는 DDN 프로그램이었다. CLAUDE.md에 명시된 state_hash 경계 규칙(DR-152/DR-178: "포함 — 영속 상태만 / 제외 — view/debug/diag/보개 전용 키")에 정확히 부합하는 결과이며, 오히려 이 경계가 실제로 올바르게 지켜지고 있다는 긍정적 증거로 판단한다.

**§11-F1 (비차단, 근본 원인 특정 완료, W1-C1 diff 범위 밖): Workbench UI가 표시한 mismatch 진단 코드는 런타임이 실제로 낸 `E_ASYNC_ENDPOINT_UNHANDLED_CANDIDATE`(phase: `async_route`)가 아니라 일반화된 `E_PRIMARY_VIEW_DECISION_MISSING`("실행은 끝났지만 ... 실제 보기 결과가 없습니다")이었다.** 근본 원인을 직접 추적했다: 동일한 소스를 리뷰 워크트리의 네이티브 CLI로 `run` 서브커맨드로 실행하면 `status=1`과 함께 정확한 `E_ASYNC_ENDPOINT_UNHANDLED_CANDIDATE` 구조화 진단이 즉시 나온다(§7에서 실측 인용) — 즉 **런타임/WASM 경계의 진단 계약 자체는 정확하다.** Workbench UI(`solutions/seamgrim_ui_mvp/ui/workbench/workbench.js`)는 W1-C1 diff에 전혀 포함되지 않은 사전 존재 코드이며(§3에서 diff 0 확인), 이 UI는 "실행이 끝났지만 보임 결과가 없다"를 일반화된 severity `"warning"` 메시지로 표시하도록 이미 설계되어 있다(신규 route-specific 코드를 UI 레벨까지 배선하는 부분은 W1-C1 범위에 없음, W1-C1 diff는 UI를 건드리지 않았으므로 당연한 결과). 따라서 이는 W1-C1이 도입한 회귀가 아니라, UI 계층이 아직 신규 phase-분리 진단을 표면화하지 않는 기존 상태이며, W1-C1의 핵심 요구사항인 "런타임이 구조화된 product-local 후보 진단을 낸다"는 §7·§9에서 이미 별도로 충족을 확인했다. **후속 조치 제안(비차단, UI 트랙)**: Workbench가 `state.diagnostics[]`의 최신 항목 code/phase를 그대로 노출하거나, `async_route`/`async_sender_identity` phase를 감지해 더 구체적인 메시지로 매핑하는 것은 W1-C2 이후 UI 트랙에서 검토할 사항으로 남긴다.

일회용 파일은 사용 직후 삭제했고 `git status --short`가 클린함을 재확인했다.

---

## 10. 보호 자원 전/후 (Section 12)

| 자원 | 값 | 상태 |
|---|---|---|
| 보호 PID 53196 | PID 53196, StartTime `2026-08-08T12:27:21.8634297+09:00` | 리뷰 시작~종료 동안 동일 프로세스(재시작/종료 없음) |
| `127.0.0.1:8787` 소유자 | PID 53196 (python), 동일 StartTime | 변경 없음 |
| 공식 프로젝트 DB (`build/seamgrim_project_data/seamgrim_projects.sqlite3`) | SHA-256 `c8fdd4d47e20f7ad7ce4f095389991859432d5af0a87aa1f7b0b06e90fe44228`, 마지막 수정 `2026-08-02 15:25:18` (리뷰 시작 20일 전) | 리뷰 활동 기간 동안 mtime 불변 — 미접촉 |
| 공식 스토어 쓰기 | 0건 | 일회용 Edge 러너는 `os.tmpdir()` 기반 격리 `dataDir`/`profileDir`/`offlineProfileDir`만 사용(원본 WorkCostV1 템플릿의 검증된 격리 설계 그대로 상속), `protected_port_8787_used: false`·`official_store_writes: 0`을 스크립트 자체가 실측 보고 |
| 활성화 엔드포인트 호출 | 0건 | 리뷰 전 구간에서 격리 임시 서버(포트 47901 Edge, 임의 임시 포트의 exec 서버)만 사용, 보호 8787에 연결 시도 없음 |
| 외부 접촉 | 0건 | 네트워크 접근은 로컬 격리 서버/브라우저 CDP뿐 |
| 잔존 Edge/프로세스/소켓/프로필/임시DB | 0건 | 리뷰용 Edge PID(202500, 203948) 종료 확인, 프로필 디렉터리 삭제 확인, 포트 47901 해제 확인 |

보호 자원 전/후 완전 일치. 침해 없음.

---

## 11. 정리 완료 (Section 14 선행 조건)

- 리뷰용 Cargo 타깃 디렉터리 2개(`target-claude-w1c1-review-20260822`, `target-claude-w1c1-teulcli-20260822`) 삭제 완료.
- 리뷰 워크트리(`I:/home/urihanl/ddn/codex/build/worktrees/claude-w1c1-review-20260822`, `node_modules` 정션·`docs/ssot/ssot` v24.44.1 브리지 포함)를 `git worktree remove --force`로 제거 완료.
- 일회용 Edge 검증 파일 삭제 및 `git status --short` 클린 재확인 완료.
- 리뷰용 Edge 프로세스/프로필/포트 정리 완료.
- 리포트 커밋용 워크트리는 `6d84137aa6aa560e958d2e9cf5046da569bc8d69`를 부모로 새로 생성했다(별도 detached worktree, product 코드 변경 없음, 이 문서 1개 파일만 추가).

---

## 12. 승인 범위 명시 (비승인 항목)

이 리뷰는 다음을 승인하지 **않는다**:

- `W1C2_REACTION_PROVIDER_PUBLIC_SURFACE` (여전히 OPEN, 미착수)
- `W1_FULL_CLOSURE`
- `RD207_PUBLIC_STABLE_WIRE`
- `PUBLIC_ACTIVATION`
- `DEPLOYMENT`
- `EXTERNAL_OUTREACH`
- `HUMAN_PASS`

이 리뷰가 승인하는 범위는 정확히 `W1C1_SENDER_ROUTE_INTERNAL_PROVIDER_ONLY`(위 6개 구현 커밋, `57f3f5d3`→`da791953`)이다.

---

## 부록 A — 실패주입 4건 요약

| # | 변조 대상 | 방법 | 결과 |
|---|---|---|---|
| 1 | 센서 predicate 검사 비활성화 | `SenderIdentityPredicate` 매칭 분기를 항상 true로 변조 | RED(센서 불일치 케이스가 성공으로 오판) → 복구 → GREEN |
| 2 | route-ambiguity → first-match 성공 | ambiguity 판정 분기를 `routes[0]` 반환으로 변조 | RED(`equal_consuming_routes_remain_ambiguous` 등 실패) → 복구 → GREEN |
| 3 | 미해결 센더에 임의 기본값 할당 | `E_ASYNC_SENDER_IDENTITY_UNRESOLVED_CANDIDATE` 실패 지점에 고정 문자열 대입 | RED(fail-closed 계약 위반 테스트 실패) → 복구 → GREEN |
| 4 | 선언 순서/소스 스팬을 RouteIdentity에 혼입 | (1차, 무효) 등록 호출부 인덱스 혼입 → 무변화 확인, 근본원인 특정(카디널리티는 Vec 길이 기반, identity 기반 아님) → (2차, 유효) `route_identity()` 해시 입력에 `AtomicU64` 호출-순서 카운터 혼입 | RED(`route_identity_is_semantic_nfc_and_not_source_order`, `equal_consuming_routes_remain_ambiguous`) → 복구 → GREEN |

모든 변조는 `git checkout -- <file>` 복구 후 SHA-256 완전 일치를 확인했고, 최종 전체 재빌드+재테스트로 GREEN 및 `git status --short` 클린을 재확인했다.

---

## 부록 B — 이 보고서 자체의 메타데이터

이 섹션을 추가하기 직전까지의 본문 바이트 수와 SHA-256(자기 참조 불가능성으로 인해 이 메타데이터 문단 자체는 해시 계산 대상에서 제외):

```
바이트 수: 26683
SHA-256:   5be291f0524baf9d9ada929977926eaf6c8c7925b86af0282bce69fb4d9b2e92
```
