# [독립검토] DDN-R-W1DF-01 W1-D~F 비동기 WAIT·Outbox 권위수렴 — 결과

## 0. 외부 AI 실행 기록

```text
TASK_TITLE:
[독립검토] DDN-R-W1DF-01 W1-D~F 비동기 WAIT·Outbox 권위수렴 독립검토

PURPOSE:
fixed-HEAD independent semantic, atomicity, parity and product review

INPUT_SCOPE:
local repository fixed commits and supplied handoff only

NETWORK_OR_EXTERNAL_DOWNLOAD:
NOT_AUTHORIZED — none performed. Real-Edge verification used a Playwright
1.44.0 copy already present in the local npm cache
(`C:\Users\ddongosu\AppData\Local\npm-cache\_npx\...\node_modules\playwright`,
version exactly matching `package.json`'s declared `1.44.0`) because the
project's own `node_modules/playwright` was absent in this environment at
review time. No `npm install`, no network fetch was executed.

CAPACITY_AND_COST:
Claude Sonnet 5 (claude-sonnet-5), single session, ~consumed the majority of
one long working session across lineage/code audit, isolated builds (native
CLI, two independent WASM release builds, nodejs WASM), 3 full Rust
regression suites, 65-case oracle reproduction, 8 real fault-injection
mutations with rebuild+retest cycles, and one real Microsoft Edge product
cycle. Exact token/dollar cost not exposed to this agent; UNKNOWN in that
sense.

EXPECTED_OUTPUT:
one independent report and one document-only review commit

RETURN_TO:
또니랑·셈그림 주 Chat / Control Tower
```

이 접두어와 실행 기록은 권위나 승인 자체가 아니다.

---

## 1. 결론 (VERDICT)

**VERDICT: PASS_WITH_FOLLOW_UP**

**정확한 판정 범위:**

```text
W1D_SHARED_LOGICAL_DELIVERY_FIFO_NO_REENTRY: PASS
W1E_BOUNDED_WAIT_AND_STAGED_OUTBOX: PASS
W1F_65_CASE_LOGICAL_ORACLE_AND_WORKER_MATRIX: PASS_WITH_FOLLOW_UP (분류 정직성 후속)
```

blocking finding은 0건이다. silent drop, first-match/first-provider fallback, WAIT 성공 위장, immediate re-entry, abort 뒤 publish, partial mutation, worker-dependent identity, harness-only product 위장, public surface 선점, protected resource 침범 — 이 중 어느 것도 실제 코드 감사·실행·실패주입·실제 Edge에서 재현되지 않았다. plain `PASS`가 아닌 이유는 아래 §6·§7·§14·§17에 기록한 비차단 후속 사항들 때문이며, 그중 가장 비중 있는 것은 65-case oracle runner가 제품을 전혀 실행하지 않는다는 사실이 오해될 수 있다는 분류 정직성 문제다.

---

## 2. 고정 좌표와 계보 (Section 4)

```text
BASELINE_W1C1_CLOSED:            eca2fbc50cd5cd50af299aad4fd87f33683c575a
PRODUCT_AND_TEST_FIXED_HEAD:     d8a4b2ab5b7c5fe68b1738f955d2d3d5b2b86ad1
FINAL_IMPLEMENTATION_HANDOFF:    42caa9a53cf85a3b638f85d45e0b564a1bbf92d9
EXPECTED_WASM_SIZE:              5482770
EXPECTED_WASM_SHA256:            fbccef544253e2ffe1c05abda1826ce34e785a4de193bfe59dec48d7898dde05
```

`git log --format='%H %P'`로 직접 확인한 선형 계보(모두 단일 부모, merge commit 0):

```
eca2fbc5  <- c8b0f3d4   (내 W1-C1 F1 targeted rereview plain PASS 커밋)
e46f653d  <- eca2fbc5   (feat: W1-D~F logical async delivery authority 결속)
e9647e2a  <- e46f653d   (fix: clean-detached WASM source path 재현성 고정)
d8a4b2ab  <- e9647e2a   (test: W1-F worker permutation oracle 실제 병렬 검증) ← FIXED HEAD
42caa9a5  <- d8a4b2ab   (docs: W1-D~F 구현 검증과 독립 검토 인계) ← HANDOFF
```

`BASELINE_W1C1_CLOSED`(eca2fbc5)가 내 이전 W1-C1 F1 targeted rereview plain PASS(`c8b0f3d4`)의 직접 자식임을 재확인했다 — 이번 W1-D~F는 이미 독립 검토를 통과한 정확한 기반 위에서만 작업했다. `git log --merges eca2fbc5..42caa9a5`는 빈 출력(병합 0).

**handoff commit(42caa9a5)은 문서 6개만 변경**(`git show --stat`로 확인): `docs/context/all/DEV_SUMMARY.md`, `docs/status/CHANGELOG.md`, `docs/status/PROJECT_STATUS.md`, `work/_session_deltas/...`, `work/codex/.../INDEPENDENT_REVIEW_REQUEST.md`, `work/codex/.../MIGRATION_MAP_AND_IMPLEMENTATION_HANDOFF.md`. 제품·테스트 diff 0.

**구현 변경 파일 전체 목록과 line count** (`git diff --stat eca2fbc5 d8a4b2ab`, 13 files / +1066 / -46):

```
lang/src/delivery.rs                                                | 350 ++++++++++++++
lang/src/lib.rs                                                     |   8 +-
pack/future_grammar_atlas_owner_closed_delta_r2_w1df/README.md      |  17 +
pack/future_grammar_atlas_owner_closed_delta_r2_w1df/build_oracle.mjs |140 ++++++
pack/future_grammar_atlas_owner_closed_delta_r2_w1df/logical_oracle.jsonl | 65 ++++
scripts/build_wasm_tool.ps1                                         |  13 +
solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson    |  24 +-
solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm (binary)    | 5467851 -> 5482770 bytes
tests/ddn_execution_concurrency_w1df_oracle_runner.mjs (신규)         | 180 +++++++
tool/src/ddn_runtime.rs                                             | 128 +++++-
tools/teul-cli/src/cli/run.rs                                       |   9 +-
tools/teul-cli/src/runtime/error.rs                                 |   6 +
tools/teul-cli/src/runtime/eval.rs                                  | 172 +++++++-
```

**예상 밖 경로: 0건.** `docs/ssot`, `publish/spec`, `solutions/seamgrim_ui_mvp/ui/workbench`, `solutions/seamgrim_ui_mvp/ui/index.html`, `pack/ddn_execution_concurrency_w1b*`, `pack/ddn_execution_concurrency_w1c1_sender_route_provider`, `tests/ddn_execution_concurrency_w1c1_sender_route_provider_runner.mjs`, `tests/ddn_workcostv1_standard_limits_w1_edge_runner.mjs`에 대해 개별 `git diff --stat`를 실행했고 전부 **빈 출력(diff 0)**이었다.

**Malhimnuri R2 ancestry 혼입 0**: `git merge-base --is-ancestor efe7fcf5ed1285eafb65ca95bac9f85824fafcb9 d8a4b2ab...` → `NOT_ANCESTOR`. Malhimnuri R2 연구 커밋은 이번 계보의 조상이 아님을 직접 확인했다(핸드오프의 주장을 신뢰하지 않고 재검증).

**주의(발견, blocking 아님)**: 이번 diff에서 `tools/teul-cli/**`가 처음으로 함께 변경됐다(W1-C1은 명시적으로 teul-cli를 건드리지 않았음). §5에서 teul-cli가 독립 의미를 재구현하지 않고 동일 shared authority(`lang/src/delivery.rs`)만 소비함을 직접 확인했다.

---

## 3. 운영·권위 문서와 live SSOT (Section 3)

작업 전 `AGENTS.md`, `CLAUDE.md`, `AGENT_WORKFLOW.md`, `SSOT_POLICY.md`, `90_프로젝트운영/공통운영_0.7.1~0.10.0_적용.md`, `90_프로젝트운영/AI_자원_라우팅.md`, `90_프로젝트운영/AI_업무지시_제목접두어.md`, `docs/context/all/DEV_SUMMARY.md`를 읽었다.

**live SSOT 직접 확인**: `docs/ssot/ssot/CURRENT.md`를 직접 열어 "현재 정본: v24.48.0 (./SSOT_ALL_MANIFEST_v24.48.0.md), owner 최종 승인: 2026-08-22"를 확인했다. `SSOT_INDEX_v24.48.0.md`, `SSOT_ALL_MANIFEST_v24.48.0.md`, `AGENTS.md`, `SSOT_POLICY.md`가 모두 v24.48.0을 일관되게 가리킨다.

**발견(비차단, 수정하지 않음)**: `AGENT_WORKFLOW.md`는 여전히 "1. `docs/ssot/ssot/*_v24.44.1.md` (live current...)"와 "`docs/ssot/ssot/SSOT_INDEX_v24.44.1.md`" 문구를 우선순위 1번·세션 체크 7번으로 갖고 있다 — 실제 live current(v24.48.0)와 4단계(24.44.1→24.46.1→24.47.0→24.48.0) 뒤처진 stale 문구다. 지시문의 경고대로 이 문구를 current authority로 쓰지 않았고, 직접 수정하지도 않았다. 후속 조치 제안: `AGENT_WORKFLOW.md`의 두 지점을 v24.48.0으로 동기화하는 별도 문서 세션.

---

## 4. 권위·비주장 감사 (Section 5)

`lang/src/delivery.rs` diff(350줄) 전체를 직접 읽고 다음을 확인했다:

- **`LogicalDeliveryPhase`**: `Admit/Wait/Resume/Start/Settle/Terminal/CleanupJoin/Preflight/Publish/Release` — product-local typed phase, 공개 wire 아님을 doc comment로 명시.
- **`WaitNodeIdentity::derive(queue_identity, operation_identity, logical_admission_ordinal)`**: `semantic_digest`로 도메인 분리된 canonical 문자열만 해싱. worker id, thread id, 소스 스팬, 벡터 인덱스를 전혀 입력받지 않음(시그니처 자체가 구조적으로 배제).
- **`enqueue_or_wait`**: `pending.len() < capacity && waiting.is_empty()`일 때만 직접 admit — waiter가 이미 있으면 capacity 여유가 있어도 새 도착이 waiter 뒤에 줄서도록(큐 잡아채기 방지) 설계됨을 확인.
- **`pop_front()`**: pending에서 pop한 뒤 waiting의 맨 앞(`waiting.pop_front()`)을 pending 뒤로(`push_back`) 승격 — capacity 회복 시 정확히 한 번, FIFO 순서로 resume.
- **`is_empty()`**: pending과 waiting 모두 빈 경우만 true — waiter가 남아있는데 "완료"로 오판하지 않음.
- **`cancel_waiter(identity)`**: 정확히 하나의 waiter만 제거, pending(이미 admit된 항목)은 건드리지 않음 — "authored cancellation은 stable wait identity 한 건만 제거"와 정확히 일치.
- **`StagedDeliveryOutbox`**: `Vec<Vec<E>>` 프레임 스택. `commit_frame()`은 부모 프레임이 있으면 병합 후 빈 Vec 반환(중첩 성공은 아직 publish 아님), 부모가 없으면(outermost) 커밋된 항목을 반환. `abort_frame()`은 해당 프레임을 그냥 버림(부모 무병합).
- **`canonical_provider_occurrences`**: `BTreeSet` 기반 dedup — 동일 `ProviderIdentity`는 occurrence당 1회, 서로 다른 identity는 모두 보존.

`tool/src/ddn_runtime.rs`(128줄)와 `tools/teul-cli/src/runtime/eval.rs`(172줄) diff를 대조하며 다음을 확인했다:

- 두 크레이트 모두 `ddonirang_lang`에서 `LogicalAsyncQueue`, `LogicalWaitReceipt`, `QueueAdmission`, `StagedDeliveryOutbox`를 **import**해서 쓸 뿐, 자체 FIFO/wait/outbox 타입을 재정의하지 않음(§5 상세는 아래 참고).
- 두 크레이트 모두 handler dispatch 직전 `outbox.begin_frame()`, 성공 시 `commit_frame()` → `admit_*_envelopes(published)`, 실패 시 `abort_frame()` + 기존 Gate0 계약 스냅샷 복원(state/locals/resources/patch_ops/trace/diagnostics/rng) 패턴이 대칭적으로 일치.
- `operation_identity` 포맷 문자열이 `"madi:{}:{}>{}:{}"`(tick/madi, sender, receiver, event_kind)로 두 크레이트에서 정확히 동일 — 별도 헬퍼 공유는 아니지만 완전히 동형(近-copy) 구현.
- `누리` 폴백 제거가 teul-cli에도 동일하게 적용됨: `.unwrap_or_else(|| "누리".to_string())` → `.ok_or(RuntimeError::AsyncSenderIdentityUnresolved { span })?`.

**W1C2/rendezvous/공개 WAIT wire/안정 진단코드/RD207 선점 없음**: `lexer.rs`/`parser.rs` diff는 **0**(이번 vertical에서 신규 문법 추가 없음, migration map 문서와 일치). `ReactionProviderRegistry`는 W1-C1과 동일하게 항상 빈 레지스트리로 인스턴스화됨(diff에 신규 provider 선언 문법 없음). 새 진단 코드는 모두 `_CANDIDATE` 접미사(`E_ASYNC_SENDER_IDENTITY_UNRESOLVED_CANDIDATE` 등 기존 유지, 신규 코드 추가 없이 phase만 재사용).

---

## 5. shared authority 감사와 우회 경로 공격 (Section 7)

```text
lang/src/currentline.rs  — diff 0, W1-D~F와 무관
tool/src/preprocess.rs   — diff 0 (파일 자체가 이번 diff에 없음)
tool/src/ddn_runtime.rs  — shared 타입만 소비, import 라인에서 직접 확인
tools/teul-cli/**        — shared 타입만 소비 (아래 상세)
tools/teul-cli/src/canon.rs — 검색했으나 이 파일 자체가 저장소에 없음(canon 로직은 cli/run.rs에 위치, diff 9줄뿐이며 진단 코드/라인/컬럼 매핑만 추가)
WASM frontdoor           — wasm_run_summary_json 등 W1-C1과 동일 경로, 신규 wasm API 추가 없음
```

`grep -n "begin_frame\|is_staging"` 결과 `tool/src/ddn_runtime.rs`에서 `is_staging()` 1곳, `begin_frame()` 1곳만 나타난다 — **실제 제품 배선에서는 프레임이 항상 깊이 1**이며, 진짜 중첩(nested-within-nested) 프레임은 현재 어떤 실행 경로로도 발생하지 않는다(§7-F1 참고).

- **currentline missing handler silent no-op**: 이번 diff가 `currentline.rs`를 건드리지 않으므로 해당 없음. 별도로 grep했으나 W1-D~F 관련 신규 코드 없음.
- **duplicate overwrite**: `ReactionProviderRegistry::register`는 여전히 W1-C1 그대로 `DuplicateRegistration` 오류로 fail-closed(diff 없음, 코드 재확인).
- **immediate re-entry**: `begin_drain()`의 `draining` 플래그 가드가 실제 방어층임을 실패주입 Mutation 3에서 직접 증명(§7).
- **preprocess의 정적 fan-out 선점**: `tool/src/preprocess.rs` 자체가 이번 diff와 무관하며 별도 fan-out 로직 추가 없음(grep 확인, 매치 0).
- **teul-cli 독립 queue/route 의미**: **0** — `tools/teul-cli/src/runtime/eval.rs`는 `LogicalAsyncQueue`/`StagedDeliveryOutbox`/`QueueAdmission`/`LogicalWaitReceipt`를 `ddonirang_lang`에서 직접 import하며, 자체 FIFO/큐 admission 로직을 재작성하지 않았다. teul-cli 고유의 `ContractFrame`/`NuriResetSnapshot`은 **teul-cli 자신의 기존(pre-existing) Gate0 계약 프레임 메커니즘**이며, 이번 diff는 그 스냅샷 구조체에 shared queue/outbox/wait-receipts 필드 3개를 추가해 **같은 스냅샷/복원 경로에 편입**시켰을 뿐 별도 의미 계층을 만들지 않았다.
- **JS/Python test-only semantic lowering**: `tests/ddn_execution_concurrency_w1df_oracle_runner.mjs`가 유일한 신규 JS 테스트이며, 이는 §6에서 자세히 다루듯 **제품을 전혀 실행하지 않는 로직 오라클** — "test-only lowering으로 제품 지원을 완료 처리"하는 패턴이 아니라(제품 완료 주장 자체를 그 파일이 하지 않음), 오히려 그 반대로 제품과 완전히 분리된 로지컬 fixture다. 제품 검증은 별도의 실제 Rust 유닛 테스트(`successor_async_*`)와 native CLI/WASM 실행이 담당한다(§6, §15에서 독립 재현).
- **기본 제품 경로가 shared authority를 우회하지 않음**: `send_message`(tool) / 대응 함수(teul-cli) 모두 `is_staging()` 분기 → `admit_*_envelopes` → `enqueue_or_wait` 단일 진입점을 거친다. legacy bypass 경로 없음(diff에 별도 fallback 분기 추가 없음).

---

## 6. 65-case 원장의 정직성 재분류 (Section 6)

**절대 65/65를 "product PASS"로 받아들이지 않았다.** `pack/future_grammar_atlas_owner_closed_delta_r2_w1df/logical_oracle.jsonl`을 직접 파싱하고, 그 생성기 `build_oracle.mjs`와 소비자 `tests/ddn_execution_concurrency_w1df_oracle_runner.mjs`를 전문 읽었다.

**재분류표:**

| 분류 | 건수 | 근거 |
|---|---:|---|
| `LOGICAL_ORACLE_ONLY` | 65/65 (오라클 러너가 실제로 실행/검증하는 범위) | 아래 §6-F1 |
| `PRODUCT_PASS`(오라클 자체 라벨) | 7 | FGA2-N10, N11, P09, P10, P11, X14, X20 |
| — 그중 실제 CLI/WASM 3-frontdoor 코퍼스(W1-C1)로 이미 독립 PASS된 것 | 4 (P09, P10, N10, X20) | route/sender/provider 의미는 W1-C1에서 변경 0, 이미 검증됨 |
| — 그중 신규 W1-E 동작, Rust in-process 유닛 테스트로만 검증(§15에서 직접 재실행) | 3 (P11, N11, X14) | `INTERNAL_TYPED_PRODUCT_CASE`(아래 §6-F2) |
| `PRODUCT_UNSUPPORTED` | 58 | `source_status: LOGICAL_CANDIDATE`, `product_status: PRODUCT_UNSUPPORTED` |
| `OWNER_DECISION_REQUIRED` | 0 | 모든 항목이 PASS 또는 UNSUPPORTED로 명확히 구분됨, 애매한 항목 없음 |

group cardinality 16/12/15/3/10/7/2(합 65), `PRODUCT_PASS=7`/`PRODUCT_UNSUPPORTED=58`을 러너 실행으로 직접 재확인했다(§15).

### §6-F1 (핵심 finding, 비차단이나 중요): 오라클 러너는 제품을 전혀 실행하지 않는다

`build_oracle.mjs`의 `digest(caseId, expectation)` 함수:

```js
function digest(caseId, expectation) {
  return `sha256:${crypto.createHash("sha256")
    .update(`fga2-w1df\0${caseId}\0${expectation}`, "utf8").digest("hex")}`;
}
```

`expectation`은 **영어/한국어 자유 서술 문자열**(예: `"bounded-full async send WAITs then resumes FIFO"`)이다. `expected_semantic_digests.workers_1/2/8`은 모두 이 **같은 정적 문자열을 같은 함수로 3번 해싱**한 값이며, DDN 소스나 Rust 런타임을 전혀 거치지 않는다. `tests/ddn_execution_concurrency_w1df_oracle_runner.mjs`의 worker matrix는 **실제 Node `worker_threads`를 진짜로 spawn**하지만(9회, `[1,2,8] × [forward,reverse,shuffled]`), 각 worker가 하는 일은 동일한 `recomputeSemanticDigest(row)`(정적 텍스트 해싱)뿐이다. 정적 텍스트의 순수 해시가 어떤 스레드에서 계산되든 같다는 것은 **거의 동어반복적으로 자명**하며, 이것이 제품의 실제 async delivery/WAIT/outbox 로직이 worker 순서에 무관하다는 증거가 되지 않는다.

- **expected digest는 구현 결과에서 사후 생성된 self-oracle인가**: 그렇다. `digest()`가 오라클 파일 생성 시점에 **자기 자신의 case_id/expectation 문자열**로부터 산출한다 — 실행 결과를 캡처한 것이 아니다.
- **실패 case가 정확한 원인으로 실패하는가**: 이 오라클 러너의 "실패"는 스키마/cardinality/텍스트-해시 불일치에 대한 실패이지 제품 실패가 아니다. 러너의 검증 항목(65 unique, cardinality, PRODUCT_PASS 집합, worker matrix 수렴)은 모두 **JSON 메타데이터 자체의 자기 일관성**이다.
- **harness-only lowering 여부**: 정확히는 "harness-only lowering"보다 더 근본적으로 **harness가 제품에 전혀 도달하지 않는다** — lowering할 대상(DDN 소스)조차 이 특정 러너 안에는 없다.

이것을 blocking으로 판정하지 않은 이유: (1) `README.md`와 handoff/DEV_SUMMARY/PROJECT_STATUS/CHANGELOG가 일관되게 "logical" fixture, "58 PRODUCT_UNSUPPORTED"라고 명시하며 제품 실행 결과라고 문장으로 주장하지 않는다. (2) PASS/OPEN matrix가 이를 "LOGICAL_ORACLE PASS"로 별도 항목화해 실제 Rust 테스트 카운트(14/4/6)와 분리 기재한다. (3) `product_status: PRODUCT_PASS` 라벨이 가리키는 7개 시나리오의 실제 제품 증거는 **다른 곳(Rust 유닛 테스트)에 진짜로 존재**하며 내가 직접 재현했다(§15). 다만 이 라벨과 실제 검증 테스트 사이에 **기계적 추적 연결이 없다** — 누군가 `successor_async_bounded_full_wait_resumes_fifo_without_drop`을 미래에 실수로 지워도 이 오라클 러너는 계속 GREEN이다. **후속 제안**: 오라클 러너가 각 `PRODUCT_PASS` 행에 대해 대응하는 cargo 테스트 이름을 명시적으로 참조하고 그 테스트의 존재(`cargo test <name> --list` 등)를 assert하도록 강화.

### §6-F2: bounded-WAIT는 현재 어떤 공개 프런트도어로도 도달 불가능

`grep -rln "async_queue_capacity" tool/src/` → `ddn_runtime.rs` 단 1개 파일에서만 매치된다. `with_async_queue_capacity()`는 CLI(`main.rs`), WASM(`runtime_surface.rs`) 어디에도 배선되어 있지 않다. 기본 용량은 `DEFAULT_ASYNC_QUEUE_CAPACITY = 100_000`이다. 즉 **일반 사용자가 작성한 DDN 프로그램은 CLI/WASM/Workbench 어떤 경로로도 bounded-full/WAIT/resume 조건을 실질적으로 관측할 수 없다** — 이 값을 재정의하는 것은 오직 Rust 내부 API(`#[test]` 함수)뿐이다.

이것은 owner의 migration map이 이미 "공개 capacity contract/wire"를 OPEN으로 남겨둔 것과 정확히 일치하므로 은폐된 과장은 아니지만, **P11("bounded-full async send WAITs then resumes FIFO")과 N11("bounded-full async silently drops")을 정확히 분류하면 `PUBLIC_SOURCE_PRODUCT_CASE`가 아니라 `INTERNAL_TYPED_PRODUCT_CASE`**(실제 DDN 소스 텍스트 + 실제 공유 런타임이지만, 트리거하려면 Rust 레벨 API 후크가 필요)다. §15에서 이 분류의 정확성을 재확인하기 위해 native CLI로 기본 용량(100,000) 아래에서 3개 중첩 전송을 보내는 프로그램을 직접 실행해, bounded-WAIT가 트리거되지 않고(예상대로) 정상 순차 전달만 일어남을 확인했다.

---

## 7. bounded FIFO와 WAIT 직접 실행 (Section 8)

Rust 유닛 테스트(§15에서 독립 재현) 외에, **내가 직접 작성한 DDN 프로그램**을 native CLI로 실행해 다음을 확인했다:

- capacity 기본값(100,000) 아래에서 **한 핸들러가 3개의 nested send(둘,셋,넷)를 동시에 staging**하는 프로그램을 실행 → `순서 = 234`(FIFO: 둘→셋→넷). 이는 §14 Mutation 2의 GREEN 기준선이자, tool/teul-cli의 기존 capacity=1 유닛 테스트가 놓치는 "동시에 2개 이상 pending" 시나리오를 내가 독립적으로 구성해 실제 native CLI로 검증한 것이다.
- Rust 유닛 테스트(lang) `bounded_full_wait_is_fifo_and_resumes_without_drop`(capacity=2), `wait_nodes_are_occurrence_unique_and_graph_classifies_progress`, `sealed_wait_graph_distinguishes_closed_deadlock_from_open_external`을 격리 빌드에서 재실행 — capacity 1/2 이상, multiple waiter의 결정적 순서, cancelled waiter 제거, sealed internal deadlock vs open external wait 구분을 모두 코드와 실행으로 확인했다.
- **cancelled waiter 제거·aborted waiter 부활 0**: `cancel_waiter`는 정확히 지정된 identity 하나만 제거하고 재호출 시 `false`를 반환(멱등, 재부활 없음) — 유닛 테스트로 확인.
- **wall-clock·thread scheduling 비의존**: `WaitNodeIdentity`/`RouteIdentity` 어디에도 시간·스레드 정보가 입력되지 않음(시그니처 감사 + Mutation 7로 실증).
- **WAIT가 receipt/결과에서 완료로 위장되지 않는지**: `QueueAdmission::Waiting(receipt)`는 `Enqueued`와 명확히 다른 variant이며, `admit_async_envelopes`는 이를 구분해 `async_wait_receipts`에 별도 기록한다(성공 경로와 혼동 없음).

실제 Microsoft Edge에서는 capacity가 도달 불가능하므로(§6-F2) full→WAIT 전이 자체는 재현하지 않았고, 대신 **nested no-reentry + FIFO 순서**(실제 도달 가능한 W1-D 핵심 동작)를 실제 제품 UI로 검증했다(§16).

---

## 8. OutboxCandidate와 원자성 (Section 9)

`tool/src/ddn_runtime.rs`의 handler dispatch 함수를 전문 추적했다:

```
frame_snapshot 캡처 (locals/resources/patch_ops/guard/const_scopes/factor_*/public_observations)
+ previous_aborted/rng_state/flow_stack/wait_receipts_len 캡처
→ outbox.begin_frame()
→ handler body 실행 (모든 nested send는 stage()로 리다이렉트)
→ Ok(()): outbox.commit_frame() → admit_async_envelopes(published)
→ Err(_): outbox.abort_frame() + frame_snapshot 복원 + aborted/rng/flow_stack 복원
         + wait_receipts.truncate(previous_len)
```

이 스냅샷/복원 메커니즘은 **W1-D~F가 새로 만든 것이 아니라 이미 baseline(eca2fbc5)에 존재하던 Gate0 계약(DR-178) 롤백 인프라를 재사용**한 것임을 `git show eca2fbc5:tool/src/ddn_runtime.rs`로 확인했다(`EvalFrameSnapshot`/`capture_frame_snapshot`/`restore_frame_snapshot`가 이미 있었음). teul-cli도 동형으로 자신의 기존 `ContractFrame`/`rollback_contract_frame`을 재사용한다.

각 실패 유형(parse/type failure, runtime failure, WorkCost/resource rejection, abort, cancel, commit failure)은 모두 동일한 `Result<(), EvalError>` 반환 경로로 수렴하므로, **실패 종류별로 별도 처리 분기가 없다** — 단일 초크포인트에서 모든 실패가 동일하게 처리되어 특정 실패 유형만 롤백을 누락할 위험이 구조적으로 배제된다.

teul-cli의 신규 유닛 테스트 `successor_async_handler_failure_rolls_back_state_and_staged_outbox`를 재실행해 다음을 직접 확인했다: 핸들러가 `순서<-7` 실행 → nested send 스테이징 → `1/0` 실패 → **`관제탑.순서`가 정확히 `0`으로 원복**(7이 아님) 그리고 **`trace.events`가 비어있음**(스테이징된 nested 메시지가 실제로 전달되지 않았다는 증거).

실제 Edge에서는 §16의 abort 시나리오로 다음을 확인했다: `발가된 목표알림.순서=1)` 핸들러가 **한 번도 실행되지 않음**(`staged_outbox_target_delivered: false`), 실패 뒤 `activeFrame === null`, stale result 0, canvas 0.

**"기존 sequential Patch 경로를 이름만 바꿔 atomic이라 부르는지"** 확인: 아니다 — staging(`begin_frame`/`stage`)·preflight(핸들러 body 전체 실행 완료까지 대기)·single logical publish(`commit_frame()`이 반환한 리스트를 한 번에 `admit_async_envelopes`)가 실제 3단계로 구현되어 있고, 실패 시 이 3단계 중 어느 지점에서 멈추든 이미 admit된 큐 상태에는 어떤 영향도 주지 않는다(핸들러 실행 중에는 큐 자체가 전혀 mutate되지 않기 때문).

---

## 9. internal ReactionProvider 경계 (Section 10)

W1-C1에서 이미 검증된 `plan_delivery_occurrence`(route 먼저, provider 나중)와 `canonical_provider_occurrences`(BTreeSet dedup, 서로 다른 identity 모두 보존)가 이번 diff에서 **변경되지 않았음**을 diff 자체로 확인했다(delivery.rs의 provider 관련 코드는 diff 범위 밖). `ReactionProviderRegistry`는 이번에도 항상 빈 상태로 인스턴스화되며(§4), 새 public provider 문법은 0(lexer/parser diff 0). Mutation 5·6(§14)으로 dedup과 fan-out 방어가 실제로 작동함을 재확인했다.

nested occurrence의 별도 dedup 집합 여부는 W1-C1 범위이며 이번 diff가 건드리지 않아 변경 없음 — internal typed evidence를 public source support로 승격하는 문구는 handoff·DEV_SUMMARY 어디에도 없음을 확인했다(§3 grep).

---

## 10. worker·permutation 결정성 (Section 11)

구현자의 digest를 복사하지 않고 `node tests/ddn_execution_concurrency_w1df_oracle_runner.mjs`를 처음부터 다시 실행해 **독립적으로 재계산**했다:

```json
{"cases":65,"groups":{"FGA2-G01":16,"FGA2-G02":12,"FGA2-G03":15,"FGA2-G04":3,"FGA2-G05":10,"FGA2-G06":7,"FGA2-G07":2},"product_bounded_cases":7,"oracle_open_cases":58,"workers":[1,2,8],"same_tag_permutations":["forward","reverse","shuffled"],"worker_matrix_runs":9,"worker_matrix_digest":"8d5160b13ad4726cbad895cf313a750cf2bd4337d3326e7bf811d5903ee8ac6c","oracle_sha256":"73b2ee48dd12033c1e5ed45d7052979fdfc35a6017cc12599e521afd3f8ae8d3", ...}
```

handoff가 인용한 `worker_matrix_digest`/`oracle_sha256`과 정확히 일치했다(재현 가능). **다만 §6-F1에서 밝혔듯 이 수렴은 정적 텍스트 해시의 수렴이지 제품 실행의 수렴이 아니다.** worker completion order/vector index/pointer/thread id/wall-clock이 semantic identity에 섞이지 않는지에 대한 **제품 레벨** 증거는 §4(`WaitNodeIdentity`/`RouteIdentity` 시그니처 감사)와 §14 Mutation 7(call-order 오염 실패주입)에서 별도로 확보했다 — 65-case worker matrix가 아니라 이 두 곳이 실제 근거다.

---

## 11. WorkCost·resource 경계 (Section 12)

`grep -n "work_cost\|WorkCost" tool/src/ddn_runtime.rs`를 async/wait/outbox/admit/enqueue 키워드와 교차 검색한 결과 **매치 0** — 새 admission/WAIT 코드는 `WorkCostMeter`를 전혀 건드리지 않는다. 이는 다음을 함의한다:

- **WAIT retry의 무비용 무한 반복**: 해당 없음 — WAIT는 폴링/재시도 루프가 아니라 `waiting` VecDeque에 그냥 앉아 capacity 해제를 기다리는 수동적 상태이며, 대기 중 CPU 비용이 전혀 발생하지 않는다(busy-loop 없음).
- **full queue를 resource error로 변조**: 없음 — full은 `QueueAdmission::Waiting`을 낳지 `E_...RESOURCE_...` 류 오류를 만들지 않음(코드 확인).
- **aborted outbox의 성공 비용 receipt**: `EvalFrameSnapshot`에 `work_cost` 필드가 없다 — 실패 시 상태는 롤백되지만 WorkCostMeter는 롤백되지 않는다. 이는 handoff가 명시한 "실제 실행된 work prefix 비용은 되돌리지 않는다"는 **의도된, 문서화된 설계**이며, 이미 baseline의 Gate0 계약 실패 처리와 동일한 정책(리소스 미터는 실측 실행량을 반영, 의미 상태만 롤백)임을 `EvalFrameSnapshot` 필드 목록(§8)으로 확인했다. 이것이 "성공 비용 receipt"로 위장되는 것은 아니다 — 실패 자체는 여전히 정확히 실패로 보고된다.
- **provider diamond cost 중복/누락**: provider 레지스트리가 항상 비어 있어(§4) 현재 관측 가능한 provider 실행 자체가 없다 — 해당 없음.
- **RD-206 resource capability 임의 활성화**: `rd206_resource_capability: false`가 native/WASM 영수증과 실제 Edge 영수증(§16) 모두에서 재확인됨.

---

## 12. replay·receipt 정직성 (Section 13)

```text
허용 주장: result_and_identity_verified, sealed_identical_input, deterministic_internal_queue_outbox_evolution
금지 주장(grep 결과 0건): checkpoint_restored, continuation_present(참: 값 자체는 false로 보고), n_slice_equivalence_claimed, external_provider_replay, network replay
```

`git show 42caa9a5 | grep -iE "checkpoint_restored|continuation_present|n_slice_equivalence|external_provider_replay|network replay"`와 pack/runner 파일 자체를 별도로 grep한 결과 **금지 주장 문자열 0건**을 확인했다(`continuation_present`는 영수증 필드로서 매 실행마다 `false` 값으로 정직하게 보고되는 것이지, 문서가 그 기능이 있다고 주장하는 것이 아니다). WASM `deterministic_rerun` 체크(같은 입력 2회 실행 → 동일 raw JSON)는 native/실제 Edge 양쪽에서 재확인했다(§15, §16). replay 중 숨은 provider/network/wall-clock lookup은 없음 — provider 레지스트리가 항상 비어 있고 새 네트워크 코드가 diff에 없다.

---

## 13. 독립 실행 재현 (Section 15)

격리 worktree(`d8a4b2ab` fixed HEAD, 별도 `docs/ssot/ssot` v24.44.1 read-only bridge, `node_modules` junction)와 3개의 격리 `CARGO_TARGET_DIR`(tool/lang용, teul-cli 전용, WASM 빌드 A/B 각각 별도)를 사용했다.

| 검증 | 결과 |
|---|---|
| `cargo test -p ddonirang-lang delivery --lib` | **14 PASS** (handoff 주장과 정확히 일치) |
| `cargo test -p ddonirang-tool successor_async --lib` | **4 PASS** |
| `cargo test --manifest-path tools/teul-cli/Cargo.toml successor_async`(별도 격리 target) | **6 PASS** |
| `cargo test -p ddonirang-lang -q`(전체) | **361 passed**(W1-C1-F1 시점 357에서 +4, 신규 delivery 테스트와 일치) |
| `cargo test -p ddonirang-tool --lib -q`(전체) | **492 passed**(+1) |
| `cargo test --manifest-path tools/teul-cli/Cargo.toml -q`(전체) | **1164 passed**(+3) |
| `node tests/ddn_execution_concurrency_w1df_oracle_runner.mjs` | §10과 동일 JSON, 재현 성공 |
| W1-C1 native/source-WASM/tracked-WASM parity(`ddn_execution_concurrency_w1c1_sender_route_provider_runner.mjs`) | **10/10**, success 6/failure 4 — 회귀 없음 |
| `python tests/run_ddn_cli_wasm_freshness_check.py` | `[ddn-cli-wasm-freshness] PASS` |
| `python tests/run_seamgrim_deploy_artifacts_check.py` | `seamgrim deploy artifacts check ok` |
| `git diff --check` | PASS(클린) |

**source WASM A/B 독립 clean-detached 빌드**: `scripts/build_wasm_tool.ps1`(`--remap-path-prefix=<repo>=/ddn-src` 고정 소스 경로 리맵 포함)을 **서로 다른 두 개의 독립 detached worktree**(경로 자체가 다름)에서 각각 실행했다:

```
build A (claude-w1df-review-20260822 worktree):  5,482,770 bytes, SHA-256 fbccef54...dde05
build B (claude-w1df-clean-detached-B-20260822 worktree, 완전히 별도 checkout): 5,482,770 bytes, SHA-256 fbccef54...dde05 (A와 완전 동일)
tracked (solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm): 5,482,770 bytes, SHA-256 fbccef54...dde05 (동일)
EXPECTED: 5,482,770 / fbccef54...dde05 — 4자 완전 일치
```

`tests/run_ddn_wasm_source_tracked_byte_identity_check.py --fresh-a <A> --fresh-b <B> --tracked <tracked>`를 실행해 `"status": "PASS"`를 확인했다 — clean-detached WASM source path 재현성 교정(`e9647e2a`)이 실제로 작동함을 서로 다른 절대경로의 두 worktree로 증명했다. 예상 hash와 다르지 않았으므로 원인 규명이나 기대값 갱신은 필요 없었다.

---

## 14. 실제 결함 주입 — 8종 (Section 14)

모든 변이는 `sha256sum`으로 원복 확인, 최종 전체 재빌드+재테스트로 GREEN 재확인했다. 최종 확인: lang 361/361, tool 492/492, teul-cli 1164/1164, `git status --short` 클린.

| # | 변이 | 대상 | 결과 |
|---|---|---|---|
| 1 | full queue를 success로 변경(`enqueue_or_wait`의 admit 조건을 `true`로) | `lang/src/delivery.rs` | lang 테스트 **RED**(2건: `bounded_full_wait_is_fifo_and_resumes_without_drop`, `wait_nodes_are_occurrence_unique_...`). **주의**: tool의 `successor_async_bounded_full_wait_resumes_fifo_without_drop`는 GREEN 유지 — capacity=1 시나리오에서 최종 집계값(1234)이 WAIT 경유 여부와 무관하게 동일하기 때문(사실 기록, 방어 자체는 lang 레벨에서 정확히 작동함을 확인했으므로 별도 교정 변이 불필요) |
| 2 | FIFO를 LIFO로(`pop_front()`에서 `pending.pop_front()`→`pop_back()`) | `lang/src/delivery.rs` | lang 테스트 **RED**(2건). tool/teul-cli의 capacity=1 유닛 테스트는 GREEN 유지(pending이 동시에 1개 이상 못 갖는 구조적 이유, §14-F1). **독립 검증**: 직접 작성한 "1개 핸들러가 3개 nested send를 동시 staging"하는 DDN 프로그램을 native CLI로 재빌드 실행 → 결과 `432`(역순, 결함 관측) vs 정상 `234`. 원복 뒤 재실행 → `234`(정상) 재확인 |
| 3 | nested send immediate re-entry 허용(`is_staging()` 체크를 `false`로 우회) | `tool/src/ddn_runtime.rs` | **1차 시도 무효**: `begin_drain()`의 독립적인 `draining` 재진입 가드가 여전히 막아 GREEN 유지(사실 기록). **교정 변이**: `begin_drain()` 자체도 항상 `true` 반환하도록 동시 변조 → lang **RED**(1건), tool **RED**(2건: `successor_async_bounded_full_wait_resumes_fifo_without_drop`, `successor_async_nested_send_runs_at_queue_tail_without_reentry`) |
| 4 | aborted OutboxCandidate publish 허용(`abort_frame()`이 부모에 병합) | `lang/src/delivery.rs` | lang **RED**(`staged_outbox_commits_nested_fifo_and_aborts_without_leak`, `[1,2,99,3]` vs `[1,2,3]`). teul-cli의 실패-롤백 테스트는 GREEN 유지 — **원인 규명**: `grep -c begin_frame tool/src/ddn_runtime.rs` = 1곳뿐, 현재 제품 배선에서 진짜 중첩 프레임은 결코 발생하지 않으며, outermost 실패는 caller가 무조건 `Vec::new()`로 덮어써 abort_frame() 내부 동작과 무관하게 이미 이중 방어됨(§7-F1과 동일 근거) |
| 5 | ProviderIdentity diamond dedup 제거(`canonical_provider_occurrences`가 BTreeSet 없이 원본 반환) | `lang/src/delivery.rs` | **RED**(2건: `provider_diamond_dedup_is_per_occurrence_and_canonical`, `delivery_occurrence_gates_provider_resolution_and_fans_out_distinct_keys`, `left: 3, right: 2`) |
| 6 | distinct provider 중 첫 provider만 실행(`resolve_occurrence`에 `.take(1)`) | `lang/src/delivery.rs` | **RED**(`delivery_occurrence_gates_provider_resolution_and_fans_out_distinct_keys`, `left: 1, right: 2`) |
| 7 | WaitEdge identity에 call-order 혼입(`WaitNodeIdentity::derive`에 정적 `AtomicU64` 카운터 추가) | `lang/src/delivery.rs` | 먼저 call-order-independence를 검증하는 임시 테스트를 추가해 baseline GREEN 확인 → 변이 적용 후 **RED**(동일 논리 입력 두 번 호출이 다른 해시 산출) → 변이와 임시 테스트 모두 원복해 정확한 원본 SHA-256 재확인 |
| 8 | failed commit 뒤 state hash 전진 허용(rollback 대신 commit 호출) | `tools/teul-cli/src/runtime/eval.rs` | **RED**(`successor_async_handler_failure_rolls_back_state_and_staged_outbox`, `left: Fixed64{7}, right: Fixed64{0}` — 실패에도 순서=7이 유지되어 롤백 누락이 정확히 드러남) |

**§14-F1**: Mutation 1·2가 tool/teul-cli 자체 테스트에서 무효였던 것은 그 테스트들이 모두 `capacity=1`만 사용하기 때문이다(pending이 동시에 1개 이상을 못 가지므로 pop_front/pop_back이 관측적으로 동일). 이는 실제 방어의 결함이 아니라 **tool/teul-cli 테스트 커버리지의 좁음**이며, 근본 방어(lang/src/delivery.rs)는 정확히 캐치했다. 후속 제안: tool/teul-cli의 `successor_async_*` 테스트 스위트에 capacity≥2, 동시-다중-pending 시나리오를 최소 1개 추가.

---

## 15. 실제 Microsoft Edge (Section 16)

전용 W1-D~F Edge 러너가 없어 이미 검증된 `tests/ddn_workcostv1_standard_limits_w1_edge_runner.mjs`(원본 SHA-256 `c0721401c36aa3bb30e9d099643541155a6fb39e281b27e4fea70d5df721b712`, 미변경) 흐름을 **일회용 사본**(`tests/_claude_w1df_edge_verification_disposable.mjs`, 사용 후 삭제·`git status --short` 클린 재확인)으로 이식했다. 소스만 아래 3개 W1-D~F 전용 DDN 프로그램으로 교체했고, 브라우저 연결부만 `chromium.connectOverCDP(...)` 격리 CDP 연결로 교체했다(원본 미변경).

**실제 Edge**: PowerShell `Start-Process msedge.exe --remote-debugging-port=48213`(임시 격리 프로필·포트, 보호 8787과 무관) → `/json/version`에서 `Edg/151.0.4129.86` 확인(Chromium 대체 아님).

**환경 참고(NETWORK_OR_EXTERNAL_DOWNLOAD 섹션에도 기록)**: 이 환경의 `node_modules/playwright`가 검토 시점에 물리적으로 없어(패키지는 `package.json`에 `1.44.0`으로 선언돼 있으나 설치 폴더 부재), 로컬 npm 캐시에 이미 존재하던 정확히 동일 버전(1.44.0)의 npx 캐시 사본을 `DDN_PLAYWRIGHT_MODULE`로 직접 지정해 사용했다. 네트워크 요청이나 `npm install`은 수행하지 않았다.

| 확인 항목 | 결과 |
|---|---|
| WASM 신원/영수증 | `wasm_sha256 = fbccef54...dde05`(EXPECTED와 일치), `wasm_bytes = 5482770`, `deterministic_rerun: true` |
| **W1-D nested no-reentry + FIFO**(첫알림 핸들러가 둘알림·셋알림을 동시 nested send) | `first_run.result = 23`(FIFO 순서: 둘→셋) ✅ — 실제 제품 UI에서 처음 검증 |
| **W1-E abort discards staged outbox**(트리거 핸들러가 목표알림을 staging한 뒤 1/0으로 실패) | `failure_atomicity.staged_outbox_target_delivered: false`(목표알림 핸들러가 전혀 실행되지 않음), `activeFrame: null`, stale result 0, canvas 0 ✅ |
| 구조화된 mismatch/failure diagnostic | `diagnostic_code: "E_PRIMARY_VIEW_DECISION_MISSING"`, severity `"warning"` — §15-F1 참고 |
| 성공 뒤 exact reopen | `restart_reopen.exact_revision: true`, 소스 텍스트 일치 |
| PID 교체 뒤 동일 결과 | `old_pid 151964 → new_pid 194360`, `result: 1`(트리거 수정 후 목표알림이 정상 전달된 결과) |
| offline import | `source_exact: true`, `result: 1`, mobile overflow 0/0 |
| console/page/network 오류 | `errors: []`(전 구간 0건) ✅ |
| 보호 자원 | `protected_port_8787_used: false`, `official_store_writes: 0` |

**§15-F1(비차단, 이미 W1-C1 리뷰에서 근본 원인 특정 완료, 이번에도 재확인)**: Workbench UI가 보인 진단 코드는 런타임이 실제로 낸 route-specific candidate 코드가 아니라 일반화된 `E_PRIMARY_VIEW_DECISION_MISSING`이다. 이는 Workbench UI(`solutions/seamgrim_ui_mvp/ui/workbench/**`)가 이번 diff에서 **전혀 변경되지 않았음**(§2에서 diff 0 확인)을 감안하면 당연한 결과이며, W1-C1 리뷰에서 이미 동일하게 발견·기록한 F2(Workbench 구조화 진단 전파) OPEN 상태와 정확히 일치한다. 새로운 회귀가 아니다.

**ambiguity 개별 재확인은 생략했다** — route/ambiguity 의미는 이번 diff에서 변경 0(§2, §4)이며 이미 W1-C1 F1 targeted rereview(plain PASS, `c8b0f3d4`)에서 실제 Edge로 검증되었다. capacity full→WAIT/resume은 §6-F2에 따라 실제 Edge에서 재현 불가능함을 확인하고 시도하지 않았다(대신 native CLI 직접 실행으로 대체 검증, §7).

---

## 16. 보호 자원 전/후 (Section 17)

| 자원 | 검토 전 | 검토 후 | 상태 |
|---|---|---|---|
| PID `53196` | `53196`, `2026-08-08T12:27:21.8634297+09:00` | 동일 | 불변 |
| `127.0.0.1:8787` owner | PID 53196(python), 동일 StartTime | 동일 | 불변 |
| 공식 DB(`build/seamgrim_project_data/seamgrim_projects.sqlite3`) | SHA-256 `c8fdd4d47e20f7ad7ce4f095389991859432d5af0a87aa1f7b0b06e90fe44228`, 540,672 bytes, mtime `2026-08-02 15:25:18` | 완전 동일 | 미접촉 |
| 공식 store write / activation call | — | 0 / 0 | |
| 외부 network/download | — | 0(§15 환경 참고) | |
| 임시 Edge·profile·port | 종료 시 정리 | PID 킬 확인, 프로필 삭제 확인, 포트 해제 확인 | |
| Cargo target(4개: tool/lang, teul-cli, wasmA, wasmB) | — | 전부 삭제 확인 | |
| review worktree(2개: 본 검토, clean-detached B) | — | `git worktree remove --force` 확인 | |
| node_modules/junction | — | worktree 제거와 함께 소거 | |
| temp DB/socket | — | 0 잔존 | |

**§16-F1 (finding, 비차단)**: `MIGRATION_MAP_AND_IMPLEMENTATION_HANDOFF.md`가 인용한 "공식 DB: 573440 bytes, SHA-256 `3fbf028e852dd3a13c3b84f812254de30c55113140f2b7869ff81a2a3b2b65f0`"는 **실제 현재 파일과 다르다**. `git log --all -S"3fbf028e..."`로 추적한 결과 이 값은 이 저장소의 오래된 여러 커밋(예: 내 자신의 과거 W1-B 리뷰 `0d8ca402`)에서 반복 인용되어온 **오래된(stale) 값**이며, 실제 파일은 `2026-08-02`에 mtime이 찍힌 채로 `c8fdd4d47e...`/540,672 bytes 상태를 유지하고 있다 — 이는 오늘 진행한 나의 이전 두 독립검토(W1-C1, W1-C1-F1)에서도 동일하게 관측된 값이다. 즉 **실제 무결성은 훼손되지 않았다**(mtime이 이번 세션들보다 훨씬 이전이므로 어떤 세션도 이 파일을 쓰지 않았음이 확인됨) — 다만 handoff 문서가 재검증 없이 오래된 값을 그대로 인용한 **문서 정확성 문제**다. blocking으로 처리하지 않았다(실제 쓰기 없음, 무결성 실제 확인됨).

---

## 17. 판정 근거 요약과 승인 범위

**plain `PASS`가 아닌 이유**: §6-F1(오라클 러너가 제품을 실행하지 않는다는 사실이 표현상 오인되기 쉬움), §14-F1(mutation 1·2에 대한 tool/teul-cli 자체 테스트 커버리지 좁음), §16-F1(handoff의 공식 DB 해시 인용이 stale) — 이 세 가지는 모두 제품 의미·원자성·권위·재현성에 영향을 주지 않는 비차단 사항이다.

**blocking finding: 0건.** silent drop, first-match/first-provider fallback, WAIT 성공 위장, immediate re-entry, abort 뒤 publish, partial mutation, worker-dependent identity, harness-only product 위장, public surface 선점, protected resource 침범 — 모두 실측으로 부재를 확인했다.

이 판정은 다음을 승인한다:

```text
W1D_SHARED_LOGICAL_DELIVERY_FIFO_NO_REENTRY: PASS
W1E_BOUNDED_WAIT_AND_STAGED_OUTBOX: PASS
W1F_65_CASE_LOGICAL_ORACLE_AND_WORKER_MATRIX: PASS_WITH_FOLLOW_UP
```

이 판정은 다음을 승인하지 않는다:

```text
W1C2_REACTION_PROVIDER_PUBLIC_SURFACE
RENDEZVOUS_RUNTIME
WORKBENCH_STRUCTURED_DIAGNOSTIC_PROPAGATION
RD207_PUBLIC_STABLE_WIRE
W1_FULL_CLOSURE
SSOT_CHANGE
PUBLIC_SPEC_CHANGE
PUBLIC_ACTIVATION
DEPLOYMENT
EXTERNAL_OUTREACH
HUMAN_PASS
```

---

## 부록 — 이 보고서 자체의 메타데이터

이 섹션을 추가하기 직전까지의 본문 바이트 수와 SHA-256(자기 참조 불가능성으로 인해 이 메타데이터 문단 자체는 해시 계산 대상에서 제외):

```
바이트 수: 43948
SHA-256:   8615a42f38e9dec79a6e87a6a89506095a8bd166a7e28cddd401aab0abafde47
```
