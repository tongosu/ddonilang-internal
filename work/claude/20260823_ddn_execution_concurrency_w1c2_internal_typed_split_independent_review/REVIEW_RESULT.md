# DDN-R-W1C2-I1-01 — W1-C2 내부 typed EndpointRoute·ReactionProvider 분리 독립 검토 결과

- TASK: `DDN-R-W1C2-I1-01`
- ORIGIN_TASK_ID: `DDN-W1C2-I1`
- SCOPE: `W1C2_INTERNAL_TYPED_ENDPOINT_ROUTE_REACTION_PROVIDER_SPLIT` (한정 범위)
- REVIEWER: 독립검증ClaudeCode
- 검토 수행일: 2026-08-23
- REVIEW_REQUEST: `work/codex/20260823_ddn_execution_concurrency_w1c2_internal_typed_split/TARGETED_INDEPENDENT_REVIEW_REQUEST.md` (at `b3cb4e06`)

## 0. 핵심 결론 (요약)

**VERDICT: PASS** (한정 범위 `W1C2_INTERNAL_TYPED_ENDPOINT_ROUTE_REACTION_PROVIDER_SPLIT`에 한함)

```
W1C2_INTERNAL_TYPED_ROUTE_PROVIDER_SPLIT: PASS
REACTION_PROVIDER_PRODUCT_INTERNAL_ONLY
PUBLIC_PROVIDER_SURFACE: OPEN
W1_FULL_CLOSURE: OPEN
PUBLIC_ACTIVATION_NOT_AUTHORIZED
HUMAN_PASS_NOT_CLAIMED
```

9개 필수 공격축 fault-injection 전부 최종적으로 RED→복원→GREEN을 재현했다 (1개 축은 최초 mutation이 무력했음을 정직하게 문서화한 뒤 교정된 mutation으로 재공격 성공). 23개 사례 분류(20/2/1)는 독립적으로 재실행하여 정확히 일치했다. 공개 표면 0건, 보호 자원 변경 0건. 논블로킹 FOLLOW_UP 2건 존재(§ FOLLOW_UPS 참조) — PASS 등급을 막지 않는다.

---

## 1. 환경 격리 및 고정 HEAD

- `IMPLEMENTATION_BASELINE`: `2aa621546af534ec82b6ea89ad0384132b3a4e42`
- `OWNER_BINDING_COMMIT`: `235d2012d870887c38b1034d4ed644aca1646db0`
- `PRODUCT_TEST_FIXED_HEAD`: `138b2eb759fb36298663381565ea38a7e245d547`
- `HANDOFF_COMMIT_AND_REQUIRED_REVIEW_PARENT`: `b3cb4e0625c9cf4dfcffe5742dda24f041706acb`

검토는 아래와 같이 완전히 격리된 자원에서만 수행했다. 공유 dirty root(`I:\dev\ddonilang\codex`)는 어떤 시점에도 수정하지 않았다.

- 1차 검토 워크트리: `I:/home/urihanl/ddn/codex/build/worktrees/claude-w1c2-review-20260823` (`git worktree add --detach 138b2eb7...`) — evidence 재실행, fault-injection, WASM A 빌드에 사용. 검토 종료 후 `git worktree remove --force`로 제거 완료.
- 2차 독립 detached 워크트리: `I:/home/urihanl/ddn/codex/build/worktrees/claude-w1c2-clean-detached-B-20260823` (동일 고정 head) — WASM B 빌드 전용, 1차와 완전히 분리된 clean checkout. 제거 완료.
- 격리 Cargo target: `target-claude-w1c2-review-20260823`(tool/lang), `target-claude-w1c2-teulcli-20260823`(teul-cli, 독립 Cargo.lock/serde_json 버전 충돌 회피), `target-claude-w1c2-wasmA-20260823`, `target-claude-w1c2-wasmB-20260823`. 전부 제거 완료.
- 보고서 커밋 워크트리: `I:/home/urihanl/ddn/codex/build/worktrees/claude-w1c2-report-20260823` (`git worktree add --detach b3cb4e06...`) — 본 보고서만 작성. 커밋 후 제거 예정.

각 격리 워크트리에는 native CLI project-policy 체크가 요구하는 `docs/ssot/ssot/` 브리지(메인 저장소의 gitignored 로컬 사본에서 복사, ~2,060개 파일)와 `node_modules` 주니어션(PowerShell `New-Item -ItemType Junction`)을 구성했다 — 둘 다 저장소 추적 파일이 아니며 검토 산출물에도 포함되지 않는다.

---

## 2. 권위 게이트 (Authority Gate)

### 2.1 계보(lineage) 검증

```
2aa62154 (IMPLEMENTATION_BASELINE)
   └─ 235d2012 (OWNER_BINDING_COMMIT: AUTHORITY_CORRECTION_AND_OWNER_BINDING.md)
        └─ 138b2eb7 (PRODUCT_TEST_FIXED_HEAD: W1-C2 구현+테스트)
             └─ b3cb4e06 (HANDOFF_COMMIT_AND_REQUIRED_REVIEW_PARENT)
```

`git merge-base`/`git log --first-parent` 재확인 결과 4개 커밋이 단일 선형(linear) 계보이며 병합 커밋 수는 0이다 (`MERGE_COMMIT_COUNT: 0`). `b3cb4e06`의 직접 부모가 `138b2eb7` 1개뿐임을 `git cat-file -p b3cb4e06`로 확인했다.

### 2.2 Owner binding 범위 확인

`AUTHORITY_CORRECTION_AND_OWNER_BINDING.md`(`235d2012`)를 원문 전체 재확인했다. 확정 항목:

| 필드 | 값 |
|---|---|
| `W1C2_NEXT_DIRECTION` | `OPTION_A_INTERNAL_TYPED_IR_VERTICAL` |
| `PRODUCT_IMPLEMENTATION_AUTHORIZED` | `YES_INTERNAL_TYPED_IR_VERTICAL_ONLY` |
| `PUBLIC_PROVIDER_SYNTAX_IMPLEMENTATION_AUTHORIZED` | `NO` |
| `STABLE_IDENTITY_WIRE_AUTHORIZED` | `NO` |
| `STABLE_DIAGNOSTIC_CODES_AUTHORIZED` | `NO` |
| `SSOT_CHANGE_AUTHORIZED` / `PUBLIC_SPEC_CHANGE_AUTHORIZED` / `UI_CHANGE_AUTHORIZED` / `PUBLIC_ACTIVATION_AUTHORIZED` | 전부 `NO` |

역사적 Candidate A(named nominal)/B(named particle)는 `NONAUTHORITATIVE_PUBLIC_SYNTAX_RESEARCH`로, Candidate C(receive wrapper)는 `REJECTED_RESEARCH_OPTION`으로, D1~D13 패킷은 `NOT_AN_OWNER_GATE_FOR_INTERNAL_TYPED_VERTICAL`로 재분류되어 있음을 확인했다. 구현 diff에서 이 재분류를 위반하는 흔적(연구용 한국어 명칭·문법·wire·진단 코드의 제품 승격)은 발견되지 않았다 — §5에서 재확인.

### 2.3 SSOT/공개 SPEC/UI/역사 corpus 무변경 확인

```
git diff --name-only 2aa62154..138b2eb7 -- docs/ssot/ publish/spec/ solutions/seamgrim_ui_mvp/ui/ \
  pack/ddn_execution_concurrency_w1c1/ pack/ddn_execution_concurrency_w1d_w1f/
```
→ 빈 출력. `docs/ssot/**`, `publish/spec/**`, UI 소스, 기존 W1-C1/W1-D~F 황금 pack 모두 diff 0.

전체 `git diff --stat 2aa62154..138b2eb7`로 변경된 경로를 전수 확인한 결과, 변경은 다음 범주로만 국한됨:
- `lang/src/delivery.rs`, `lang/src/lib.rs` (내부 identity/registry 신설)
- `tool/src/ddn_runtime.rs` (신규 standalone 시뮬레이션 런타임)
- `tools/teul-cli/src/cli/run.rs`, `tools/teul-cli/src/runtime/{error.rs,eval.rs}` (실경로 route 선택 리팩터)
- `tool/tests/ddn_execution_concurrency_w1c2_internal_typed.rs` (신규 통합 테스트, 644줄)
- `pack/ddn_execution_concurrency_w1c2_internal_typed/{README.md,expected.jsonl}` (신규 pack)
- `tests/ddn_execution_concurrency_w1c2_internal_typed_runner.mjs` (신규 evidence runner)
- `work/codex/20260823_ddn_execution_concurrency_w1c2_internal_typed_split/**` (핸드오프 문서)

→ **AUTHORITY_CORRECTION: NONE_NEEDED** (owner binding 위반 없음)

---

## 3. 5개 내부 identity의 의미적 분리 감사

`lang/src/delivery.rs`에 `opaque_internal_identity!` 매크로로 생성된 5개 신규 타입(`ProviderDeclarationIdentity`, `ProviderOwnerIdentity`, `ProviderRegistrationIdentity`, `ExecutionInstanceIdentity`, `DeliveryOccurrenceIdentity`)을 각각 원문 확인했다.

| 축 | 방어 메커니즘 | 확인 방법 |
|---|---|---|
| 선언/소유자 교환 | 각각 독립 domain-tag(`"...-declaration.candidate"` 등)를 가진 별도 Rust 타입 — 컴파일 타임에 서로 대입 불가 | 타입 정의 및 `derive()` 서명 확인 |
| 등록-선언 치환 | `ProviderRegistrationIdentity::derive(&declaration, &owner, ...)`가 선언/소유자 **타입 자체**를 입력으로 구성 — 문자열이 아니라 타입을 합성하므로 치환은 타입 오류가 됨 | 소스 확인 + case 07/08 실행 |
| 실행 인스턴스 변경 후 dedup 우회 | `ExecutionInstanceIdentity::derive(execution_semantic)`가 독립 축으로 분리되어 registration 축과 혼동되지 않음 | case 09 |
| 동일 occurrence 중복 적용 | `DeliveryOccurrenceIdentity::derive(&execution_identity, occurrence_semantic)`가 execution identity를 참조로 의존 — 서로 다른 실행 인스턴스는 동일 occurrence_semantic이어도 항상 다른 occurrence identity 산출 (단위테스트로 확인됨) | `internal_provider_identity_axes_remain_distinct` 단위테스트 재실행 |
| 잘못된 provider들이 같이 dedup됨 | diamond reachability는 `registration_identity` 값 자체의 동일성으로만 dedup(§4.2) — declaration/owner가 다르면 서로 다른 registration_identity가 나와 절대 합쳐지지 않음 | case 06 vs case 08 대조 |
| diamond-reachability와 중복정의 혼동 | `register_descriptor()`의 `DuplicateDefinition` 거부는 **등록 시점**(`registration_identity` 키)에서만 발생하고, `resolve_internal_occurrence`의 dedup은 **실행 시점**(reachability) 문제로 완전히 분리된 코드 경로 | case 06(정상 diamond) vs case 07(등록 시점 거부) 대조 실행 |

또한 `internal_provider_identity_ignores_physical_provenance_and_worker_order` 단위테스트를 재확인했다: `value` 페이로드만 다르고(`"source-span-1-worker-8"` vs `"source-span-99-worker-1"`) declaration/owner/registration 입력이 동일한 두 descriptor는 정확히 동일한 identity 3종을 산출한다 — 소스 스팬·워커 순서가 identity에 새지 않음을 재확인했다.

**결론: 5개 identity는 이름만 다른 wrapper가 아니라 서로 다른 입력 조합에 반응하는 실제로 구분된 축이다.**

---

## 4. 실행 의미론 감사 (실제 제품 Rust 경로)

### 4.1 route-cardinality가 provider보다 항상 먼저 결정됨

`plan_internal_delivery_occurrence`(`lang/src/delivery.rs`) 원문:
```rust
// The route cardinality gate is deliberately first. Provider resolution
// must not run after unhandled or ambiguous consuming delivery.
let route = select_exactly_one_endpoint(routes)?;
let occurrence = providers.resolve_internal_occurrence(reached_registration_keys, envelope)?;
```
`?`로 조기 반환하므로 route가 0/2+ 이면 provider 코드는 물리적으로 실행되지 않는다. case 01(0 route)/02(2+ route)로 실증 — 두 경우 모두 `RouteUnhandled`/`RouteAmbiguous{count:2}`가 provider 평가 없이 즉시 반환됨을 확인했다. Mutation 1(§7)로 이 순서를 뒤집었을 때 case 01/02가 RED로 전환됨을 재확인했다.

teul-cli 실경로(`tools/teul-cli/src/runtime/eval.rs`)도 동일 원리를 따른다: 실제 `EndpointRoute<usize>`를 구성해 `plan_delivery_occurrence(&routes, &provider_registry, std::iter::empty())`를 호출하며, registry는 `ReactionProviderRegistry::<()>::default()`로 항상 비어 있다. 코드 주석: "Public teul source has no provider ingress. It still crosses the same route-first delivery authority with an explicitly empty registry, so no historical all-handler fallback can fan out." → §7 Mutation 9에서 이 경로에 레거시 우회를 재도입해 공격했다.

### 4.2 diamond dedup / distinct fan-out

`resolve_internal_occurrence`는 `reached_registration_keys`를 `.collect::<BTreeSet<_>>()`로 먼저 dedup한 뒤 predicate로 필터링한다. case 06(동일 identity로 도달하는 diamond 경로 2개 → 1회 실행)과 case 05(서로 다른 provider 2개 → 둘 다 실행)로 확인. Mutation 3(dedup 제거)→case 06 RED, Mutation 4(`.take(1)` 추가)→case 05 RED로 각각 별도 확인.

### 4.3 동일 settled snapshot 관찰

`InternalTypedReactionRuntime::execute()`는 `let settled = self.world.clone();`로 스냅샷을 1회 생성하고, route 프로그램과 모든 provider 프로그램을 **동일한** `settled`에 대해서만 평가한다 (world는 전체 candidate 평가가 끝나기 전까지 변이되지 않음). case 10으로 확인.

### 4.4 결정론적 PatchCandidate 병합 / worker 순서 무관

`merge_internal_candidates`는 `candidates.sort_by(|l,r| l.participant_identity.cmp(&r.participant_identity))`로 정렬 후 병합한다. case 11(`worker_permutation_is_deterministic`)이 서로 다른 순열 입력에 대해 동일한 `internal_reaction_group_digest`를 요구하며, 실제로 동일 digest를 산출함을 재확인했다. Mutation 5(§7, 교정 후)로 순서 의존성을 재도입했을 때 case 11의 두 digest가 달라짐(RED)을 확인했다.

### 4.5 원자적 abort / 부분 커밋 금지

`execute()`는 모든 candidate가 `?`로 성공해야만(단 하나라도 실패 시 즉시 전체 반환) 이후 `self.world = committed_world` 대입이 실행된다. case 13(provider body 실패)/14(부분 publish 금지)/18(abort 시 nested outbox 폐기)로 확인. Mutation 6(에러 삼킴)→3개 케이스 동시 RED로 확인.

### 4.6 외부 EffectIntent는 커밋 이후에만 release

`release_effect` 호출은 `self.world = committed_world`/`self.revision = committed_revision` **이후**에만 실행되며, 실패해도 `self.world`를 되돌리지 않고 `external_release_failures`에만 기록한다. case 19(`external_release_failure_no_rewind`)로 확인. Mutation 8(release를 커밋 이전으로 이동)→case 19 RED(release 클로저가 구 world를 관찰).

### 4.7 FIFO/WAIT/RESUME/no-reentry/staged-outbox — W1-D~F 계약 보존

case 15(nested send는 staged outbox에만 쌓임)/16(no-reentry: `begin_drain()` 재진입 방지 유지)/17(bounded full → WAIT)/18(abort 시 nested outbox 폐기)로 W1-D~F에서 확립된 계약이 W1-C2 신규 경로에서도 깨지지 않음을 확인했다. Mutation 7(즉시 재진입 강제 삽입)→case 15/16/17 3개 동시 RED로 확인.

---

## 5. 공개 표면 0건 감사

### 5.1 정적 스캔 (JS runner 기반, 독립 재실행)

`tests/ddn_execution_concurrency_w1c2_internal_typed_runner.mjs`가 수행하는 스캔을 격리 워크트리에서 독립적으로 재실행하고, 별도로 수동 grep으로 교차검증했다.

- `lang/src/{ast,parser,normalizer,currentline}.rs`, `tool/src/{preprocess,wasm_api}.rs`, `tools/teul-cli/src/lang/{ast,parser}.rs`, `tools/teul-cli/src/cli/**/*.rs`에서 `반응제공자`/`반응하면` 리터럴 부재 확인 — 매치 0건.
- `lang/src/ast.rs`의 `Receive {` 구조체 정의 슬라이스에 대소문자 무시 `"provider"` 부분 문자열 부재 확인.
- `tools/teul-cli/src/runtime/eval.rs`에 `plan_delivery_occurrence(` 존재, `ReactionProviderRegistry::<()>::default()` 존재, `select_exactly_one_endpoint(&routes)` **부재**를 재확인 (수동 grep으로 3개 조건 모두 독립 재검증).
- `git diff --name-only 2aa62154..138b2eb7`을 7개 공개 진입 경로(파서/AST/CLI/WASM frontdoor/기존 `받으면` 처리기/기존 이벤트 서페이스/기존 진단 코드 테이블)에 한정해 재실행 → 빈 출력.
- `DdnRunner::public_provider_source_ingress_count(&self) -> usize { 0 }` 원문 확인 — 하드코딩된 0 반환, 조건분기 없음.

### 5.2 표면 카운트

- `PUBLIC_SYNTAX_PRODUCT_TOKEN_COUNT: 0`
- `PUBLIC_PROVIDER_SOURCE_INGRESS_COUNT: 0`

### 5.3 아키텍처 비대칭에 대한 정밀 주석 (NOTES, 논블로킹)

`tool/src/ddn_runtime.rs`의 `InternalTypedReactionRuntime`은 실제 `EvalContext`/`DdnRunner` 반응 디스패치 파이프라인에 전혀 연결되지 않은 **독립 시뮬레이션**이다. 이는 다음 grep으로 확정했다:

```
grep -rln "InternalTypedReactionRuntime\|plan_internal_delivery_occurrence\|InternalReactionProgram" tool/src/ tools/teul-cli/src/
```
→ 결과는 `tool/src/ddn_runtime.rs` 자기 자신뿐 (정의 파일 외 호출부 0건).

즉 20개 `INTERNAL_TYPED_PRODUCT_CASE`는 실제 제품 Rust **라이브러리 코드**를 손수 구성한 값으로 직접 호출하는 증거이지만, 실제 `.ddn` 프로그램이 파서→AST→평가기를 거쳐 이 경로를 타는 end-to-end 증거는 **아니다**. 이는 owner binding이 공개 provider 문법을 명시적으로 금지한 상황에서 아키텍처적으로 불가피하다 — 다중 provider fan-out을 표현할 수 있는 DDN 소스 구문이 아직 존재하지 않으므로, 이 계층을 사전 검증할 유일한 방법은 Rust 전용 하네스뿐이다. 반면 `tools/teul-cli/src/runtime/eval.rs`는 실제 `.ddn` 프로그램이 지나는 실경로 자체를 `plan_delivery_occurrence`로 리팩터링한 것으로, 항상 비어있는 registry로 인해 행동적으로는 no-op이지만 이는 **진짜 실경로 통합**이다. 이 비대칭을 혼동 없이 명확히 구분해 기록한다 (FOLLOW_UP-1).

---

## 6. 23개 사례 독립 재분류

`pack/ddn_execution_concurrency_w1c2_internal_typed/expected.jsonl`을 직접 파싱하고, `tool/tests/ddn_execution_concurrency_w1c2_internal_typed.rs`의 23개 `w1c2_i1_case_NN_*` 함수명과 1:1 대조했다 (양방향 대칭성 확인: ledger에 있는 모든 test_id가 컴파일되고, 컴파일된 모든 테스트가 ledger에 존재).

| 분류 | 건수 | 사례 |
|---|---|---|
| `INTERNAL_TYPED_PRODUCT_CASE` | 20 | 01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,23 |
| `PUBLIC_SOURCE_REGRESSION_CASE` | 2 | 20,21 (실제 Korean DDN 소스로 `public_provider_source_ingress_count()==0` 확인) |
| `PRODUCT_UNSUPPORTED` | 1 | 22 (teul 레거시 provider fallback — fail-closed, 우회/fallback/무음 성공 없음) |

독립 재실행 결과:
```
cargo test -p ddonirang-tool --test ddn_execution_concurrency_w1c2_internal_typed
→ test result: ok. 23 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

**LOGICAL_ONLY / INTERNAL_TYPED_PRODUCT_EVIDENCE / PUBLIC_PRODUCT_REGRESSION / PRODUCT_UNSUPPORTED 분리 승격 없음**을 확인 — 논리 오라클을 제품 실행 증거로 격상시키는 표현은 pack README/러너/테스트 어디에도 없다.

### 6.1 case 22 명명 정밀도 관찰 (FOLLOW_UP-2, 논블로킹)

case 22(`w1c2_i1_case_22_teul_legacy_provider_fallback_zero`)의 테스트 본문은 case 20/21과 구조적으로 동일하게 `tool` crate의 `public_provider_source_ingress_count()==0`만 확인한다. `tool/tests/`의 통합 테스트는 별도 crate인 `teul-cli`에 물리적으로 접근할 수 없으므로, 이 Rust 테스트 자체는 teul-cli 관련 주장을 문자 그대로 검증하지 않는다. teul-cli 관련 실제 증거는 §5.1에서 확인한 JS 러너의 별도 정적 텍스트 스캔(`plan_delivery_occurrence(` 존재 + `select_exactly_one_endpoint(&routes)` 부재)이 담당하며, 이는 독립적으로 재검증되어 통과했다. 즉 `PRODUCT_UNSUPPORTED`/fail-closed 주장 자체는 유효하지만, case 22라는 이름이 검증 메커니즘을 정확히 반영하지 않는다.

---

## 7. Fault Injection — 9개 필수 공격축

모든 mutation은 격리 워크트리(`claude-w1c2-review-20260823`)에서만 수행했고, 각 mutation 후 `git checkout -- <file>` + SHA-256 재확인으로 정확히 복원했다. 기준 해시:

- `lang/src/delivery.rs` = `2132ecc0747313e2a54e42c0c4efb97ce381326f156e8611042c2688d899a8d7`
- `tool/src/ddn_runtime.rs` = `0723141ab6d831f777046218b5cb4c131647658e76ba98b572c4990fd7b0d65a`
- `tools/teul-cli/src/runtime/eval.rs` = `874bd8c1e9c1fe7205ae1828fc5b6349dbce40233c09d7aa7d2b8646f2de9bb6`

| # | 공격축 | Mutation | RED | 상태 |
|---|---|---|---|---|
| 1 | provider가 route 결정 전에 실행됨 | `resolve_internal_occurrence` 호출을 `select_exactly_one_endpoint` 앞으로 이동 | case 01,02 실패 (`ProviderIdentity{UnknownRegistration}` vs 기대 `RouteUnhandled`/`RouteAmbiguous`) | ✅ |
| 2 | route 모호성 하에서 provider 실행 | ambiguous 시 `&routes[0]`으로 강제 진행 | case 02 실패 | ✅ |
| 3 | diamond dedup 제거 | `.collect::<BTreeSet<_>>()` 제거 | case 06 실패 (`left:3,right:1`) | ✅ |
| 4 | 서로 다른 provider가 잘못 dedup됨 | `.filter_map(...)` 뒤 `.take(1)` 추가 | case 05 실패 (`left:1,right:2`) | ✅ |
| 5 | worker/reachability 순서가 의미 결과에 반영됨 | **1차 시도(무력)**: `merge_internal_candidates`의 `sort_by`만 제거 → 전 23건 GREEN 유지, 원인: `resolve_internal_occurrence`의 상류 `BTreeSet`이 이미 순서를 정규화. **교정**: BTreeSet dedup을 순서-보존 dedup(`seen: BTreeSet` 멤버십 + `ordered: Vec` 삽입순)으로 교체하고 sort 제거를 동시 적용 | case 11 실패 (digest `8f4317af...` vs `d83ed154...`) | ✅ (정직하게 무력 원인 기록 후 교정) |
| 6 | provider 실패 후 부분 PatchCandidate publish | 평가 루프에서 `?` 대신 `if let Ok(...)`로 에러 삼킴 | case 13,14,18 3건 동시 실패 | ✅ |
| 7 | delivery occurrence가 중복 적용됨(즉시 재진입) | 스테이징 루프 뒤 `while let Some(...) = self.queue.pop_front()`로 즉시 재진입 삽입 | case 15,16,17 3건 동시 실패 | ✅ |
| 8 | abort 전에 외부 EffectIntent가 실행됨 | release 루프를 world 커밋 이전으로 이동 | case 19 실패 (`left:None,right:Some("committed")`) | ✅ |
| 9 | 공개/레거시 fallback 재도입 | teul-cli eval.rs에서 `plan_delivery_occurrence`를 `select_exactly_one_endpoint(&routes)` 레거시 경로로 교체 | Rust 테스트는 GREEN 유지(빈 registry라 행동 동일) — **JS 러너의 정적 아키텍처 가드**가 `Error: teul async route is not bound to shared delivery authority with empty registry`로 검출 | ✅ (동적 테스트로는 검출 불가한 사례이므로 정적 가드가 유일하고 충분한 방어선임을 확인) |

Mutation 5와 Mutation 9 모두 "최초 시도가 실제로 공격하지 못하면 숨기지 않고 교정한다"는 지침에 따라 원인을 투명하게 기록했다. Mutation 5는 진짜 교정(파일 수정)이 필요했던 경우이고, Mutation 9는 아키텍처상 동적 테스트로는 원천적으로 구분 불가능한(빈 registry는 어떤 순서로도 다른 행동을 만들 수 없음) 경우로, 정적 가드가 유일하게 유의미한 방어임을 확인한 뒤 그 정적 가드가 실제로 작동함을 검증했다.

전체 복원 후 최종 확인:
- `git status --short` → 빈 출력 (검토 워크트리 내)
- 3개 파일 SHA-256 전부 기준값과 정확히 일치
- 전체 재빌드 + 테스트 스위트 GREEN 재확인

---

## 8. WASM 소스 A/B/tracked 바이트 동일성 + 실제 Edge 회귀 확인

### 8.1 WASM A/B/tracked/expected 동일성

- 독립 detached 워크트리 A(`claude-w1c2-review-20260823`, 격리 target `target-claude-w1c2-wasmA-20260823`)와 워크트리 B(`claude-w1c2-clean-detached-B-20260823`, 격리 target `target-claude-w1c2-wasmB-20260823`)에서 각각 `wasm-pack build --target web -- --features wasm`을 독립 실행.
- 산출물: `ddonirang_tool_bg_A.wasm`, `ddonirang_tool_bg_B.wasm` — 둘 다 정확히 **5,484,048 bytes**, SHA-256 **`1b161d7eabd21f1996813fab53611b701abd6cd52f2345867932e636f76dcd4c`**.
- 저장소에 커밋된 `TRACKED_WASM`도 동일 해시.
- `run_ddn_wasm_source_tracked_byte_identity_check.py` 재실행 → `"status": "PASS"`.
- 지시서의 `EXPECTED_SHA256: 1b161d7eabd21f1996813fab53611b701abd6cd52f2345867932e636f76dcd4c`와 정확히 일치.
- tracked WASM 갱신은 저장소 표준 절차(`wasm-pack build` → `tool/pkg/*.{wasm,js,d.ts}` → `solutions/seamgrim_ui_mvp/ui/wasm/` 복사)를 따랐음을 매니페스트/커밋 diff로 확인.

**`WASM_A_B_TRACKED_IDENTITY: PASS`**

### 8.2 실제 Microsoft Edge 회귀 확인 (regression-only)

기존에 검증된 템플릿(`tests/ddn_workcostv1_standard_limits_w1_edge_runner.mjs`, 원본 SHA-256 불변)을 재사용해, `chromium.launchPersistentContext`를 `chromium.connectOverCDP`로 대체한 **일회용 미추적 사본** (`tests/_claude_w1c2_edge_verification_disposable.mjs`)을 작성해 실행했다.

- 실제 `msedge.exe`를 `--remote-debugging-port=49102` + 격리 `--user-data-dir`로 기동, `/json/version`에서 `Edg/151.0.4129.86` 확인.
- 실행 결과: `ok: true`, `errors: []`.
- `first_run.result: 7` (정상 성공 흐름).
- `failure_atomicity: {lifecycle: "failed", stale_result_count: 0}` — 모호성(ambiguity) 흐름이 올바르게 실패하고 이전 결과가 잔류하지 않음.
- `repaired_run.result: 10` (재개 후 정상 흐름).
- `restart_reopen`: PID 교체 후 정확한 revision으로 재오픈됨(`exact_revision: true`).
- `clone_portable`/`offline_import_run` 모두 성공.
- WASM 해시/바이트 재확인 일치.
- 콘솔/페이지/네트워크 에러 0건.
- cleanup: `server_stopped/temp_data_removed/profile_removed/offline_profile_removed` 전부 `true`.

**중요**: 이 Edge 확인은 **기존 공개 행동(W1-C1의 success/ambiguity 흐름)에 대한 회귀 확인일 뿐**이며, 공개 provider 표면이 존재한다는 증거로 해석해서는 안 된다 — W1-C2에서 신설된 provider 관련 표면은 Edge에서 관찰할 방법이 아예 없다(공개 진입점이 0이므로).

**정리**: 일회용 스크립트 삭제 확인(`git status --short` clean), Edge 프로세스 3개(PID 118316/55160/21484) 종료, 임시 프로필 `claude_edge_w1c2_profile` 삭제, 포트 49102 해제 확인 완료.

**`ACTUAL_EDGE_REGRESSION: PASS_REGRESSION_ONLY`**

---

## 9. 보호 자원 전/후 대조

| 자원 | 검토 전 | 검토 후 | 일치 |
|---|---|---|---|
| 공식 DB 경로 | `I:/home/urihanl/ddn/codex/build/seamgrim_project_data/seamgrim_projects.sqlite3` | 동일 | — |
| 공식 DB 바이트 | 540,672 | 540,672 | ✅ |
| 공식 DB SHA-256 | `c8fdd4d47e20f7ad7ce4f095389991859432d5af0a87aa1f7b0b06e90fe44228` | `c8fdd4d47e20f7ad7ce4f095389991859432d5af0a87aa1f7b0b06e90fe44228` | ✅ |
| 공식 DB mtime | 2026-08-02 15:25:18.978538400 +09:00 | 2026-08-02 15:25 (동일 mtime, 재기록 없음) | ✅ |
| WAL(`-wal`) | 0 bytes, mtime 2026-08-18 | 0 bytes, mtime 2026-08-18 (불변) | ✅ |
| SHM(`-shm`) | 32,768 bytes, mtime 2026-08-18 | 32,768 bytes, mtime 2026-08-18 (불변) | ✅ |
| 보호 PID | `53196` / python / StartTime `2026-08-08T12:27:21.8634297+09:00` | 동일 PID/프로세스명/StartTime | ✅ |
| 보호 포트 | `127.0.0.1:8787`, owner PID `53196` | 동일 owner/StartTime, LISTEN 유지 | ✅ |

**공식 저장소 쓰기 0건, 활성화(activation) 엔드포인트 호출 0건, PID 53196 종료/교체 0건, 포트 8787 점유 변경 0건.**

---

## 10. 최종 재확인 회귀 스위트 (독립 재실행)

| 스위트 | 결과 |
|---|---|
| `lang` 단위테스트 | `test result: ok. 363 passed; 0 failed; 0 ignored` |
| `teul-cli` 단위+통합테스트 | `test result: ok. 1165 passed; 0 failed; 0 ignored` |
| `tool` 단위+통합테스트 (492 base) | GREEN (기존 W1-C1/W1-D~F 회귀 포함) |
| W1-C2 신규 pack 테스트 (23) | `test result: ok. 23 passed; 0 failed; 0 ignored` |
| W1-C1 pack (`ddn_execution_concurrency_w1c1`) | 10/10 PASS (parity 유지) |
| W1-D~F pack (`logical 65 + public 4 + internal typed 3`) | 전체 PASS, capacity=2 통합 테스트 포함 |

W1-D~F 후속검토(§7-F1, README 환경변수 누락)가 `2aa62154`(본 리뷰의 IMPLEMENTATION_BASELINE) 커밋 "docs: complete W1DF repro environment"에서 실제로 수정되어 있음을 `git show`로 재확인 — 이전 리뷰 피드백이 계보상 실제로 반영됨.

---

## 11. FINDINGS / FOLLOW_UPS

### FOLLOW_UP-1 (논블로킹)
- **finding**: `tool/src/ddn_runtime.rs`의 `InternalTypedReactionRuntime`은 실제 `EvalContext`/`DdnRunner` 반응 디스패치와 연결되지 않은 독립 시뮬레이션이며, 20개 `INTERNAL_TYPED_PRODUCT_CASE`는 손수 구성한 Rust 값으로만 이 레이어를 검증한다(DDN 소스/파서/AST 미경유).
- **재현절차**: `grep -rln "InternalTypedReactionRuntime\|plan_internal_delivery_occurrence\|InternalReactionProgram" tool/src/ tools/teul-cli/src/` → 정의 파일 자신 외 호출부 0.
- **root cause**: 공개 provider 문법이 아직 승인되지 않아 다중 provider fan-out을 표현할 DDN 소스 구문이 존재하지 않음 — 현 단계에서 아키텍처적으로 불가피.
- **제품영향**: 없음(의도된 설계). 다만 향후 독자가 "실제 제품 Rust 코드로 검증됨"을 "실제 DdnRunner end-to-end 경로로 검증됨"과 혼동하지 않도록 evidence ledger/보고서에 명시 필요.
- **차단여부**: 비차단.
- **후속owner**: 셈그림Codex (공개 provider 문법 승인 시 end-to-end 통합 테스트 추가 검토).
- **허용교정범위**: 문서/주석 수준의 명확화만 — 코드 구조 변경 불필요.

### FOLLOW_UP-2 (논블로킹)
- **finding**: case 22(`w1c2_i1_case_22_teul_legacy_provider_fallback_zero`)의 Rust 테스트 본문이 case 20/21과 동일하게 `tool` crate의 `public_provider_source_ingress_count()==0`만 검사하며, `teul-cli` crate에 대한 주장을 문자 그대로 검증하지 않는다.
- **재현절차**: `tool/tests/ddn_execution_concurrency_w1c2_internal_typed.rs`의 case 22 함수 본문과 case 20/21 본문 비교.
- **root cause**: `tool/tests/`는 별도 crate인 `teul-cli`에 물리적으로 접근 불가 — teul-cli 관련 실제 증거는 JS 러너의 별도 정적 스캔(§5.1)이 담당하며, 이는 독립 재검증되어 유효함.
- **제품영향**: 없음 — `PRODUCT_UNSUPPORTED`/fail-closed 주장 자체는 유효한 별도 메커니즘으로 뒷받침됨.
- **차단여부**: 비차단.
- **후속owner**: 셈그림Codex.
- **허용교정범위**: 테스트 함수명 또는 주석을 "본 테스트는 tool crate 표면만 검사하며 teul-cli 표면은 JS 러너가 별도 검증함"으로 명확화.

두 항목 모두 `PUBLIC_KOREAN_NAME`/`PUBLIC_PROVIDER_EXACT_SYNTAX`/`STABLE_PROVIDER_IDENTITY_WIRE`/`W1_FULL_CLOSURE` 등 이 리뷰가 닫을 수 없는 항목과 무관하며, 한정 범위 PASS를 막지 않는다.

---

## 12. 반환 형식 (directive §12)

```
VERDICT: PASS
SCOPE: W1C2_INTERNAL_TYPED_ENDPOINT_ROUTE_REACTION_PROVIDER_SPLIT
FIXED_PRODUCT_HEAD: 138b2eb759fb36298663381565ea38a7e245d547
REVIEW_PARENT: b3cb4e0625c9cf4dfcffe5742dda24f041706acb
REVIEW_COMMIT: <본 파일 커밋 후 기입>
REVIEW_BRANCH: claude/ddn-r-w1c2-i1-01-internal-typed-route-provider-split-independent-review-20260823
REPORT_PATH: work/claude/20260823_ddn_execution_concurrency_w1c2_internal_typed_split_independent_review/REVIEW_RESULT.md
REPORT_BYTES: <커밋 후 기입>
REPORT_SHA256: <커밋 후 기입>
LINEAGE: 2aa62154 -> 235d2012 -> 138b2eb7 -> b3cb4e06 (linear, merge_commit_count=0)
MERGE_COMMIT_COUNT: 0
CHANGED_PATHS: lang/src/delivery.rs, lang/src/lib.rs, tool/src/ddn_runtime.rs, tools/teul-cli/src/cli/run.rs, tools/teul-cli/src/runtime/error.rs, tools/teul-cli/src/runtime/eval.rs, tool/tests/ddn_execution_concurrency_w1c2_internal_typed.rs, pack/ddn_execution_concurrency_w1c2_internal_typed/**, tests/ddn_execution_concurrency_w1c2_internal_typed_runner.mjs, work/codex/20260823_ddn_execution_concurrency_w1c2_internal_typed_split/**
AUTHORITY_CORRECTION: NONE_NEEDED (owner binding 위반 없음; Candidate A/B/C, D1-D13 재분류 준수 확인)
INTERNAL_TYPED_CASES: 20/20
PUBLIC_REGRESSION_CASES: 2/2
UNSUPPORTED_CASES: 1/1
IDENTITY_SEPARATION: PASS (5축 모두 의미적으로 구분됨, §3)
ROUTE_BEFORE_PROVIDER: PASS (§4.1, Mutation 1/2로 공격 검증)
DIAMOND_DEDUP: PASS (§4.2, Mutation 3으로 공격 검증)
DISTINCT_PROVIDER_FANOUT: PASS (§4.2, Mutation 4로 공격 검증)
SAME_SETTLED_SNAPSHOT: PASS (§4.3)
DETERMINISTIC_PATCH_MERGE: PASS (§4.4, Mutation 5 교정 후 공격 검증)
ATOMIC_ABORT: PASS (§4.5, Mutation 6으로 공격 검증)
WAIT_FIFO_NO_REENTRY: PASS (§4.7, Mutation 7로 공격 검증)
PUBLIC_SYNTAX_TOKEN_COUNT: 0
PUBLIC_PROVIDER_SOURCE_INGRESS_COUNT: 0
FAULT_INJECTION: 9/9 공격축 최종 성공 (1축 최초 무력 -> 정직히 기록 후 교정하여 성공, §7)
W1C1_PARITY: 10/10
W1DF_REGRESSION: PASS (logical 65 + public 4 + internal typed 3, capacity 통합 포함)
LANG_TESTS: 363/363
TOOL_TESTS: 492 + 23 (W1-C2) + capacity 통합, 전체 GREEN
TEUL_CLI_TESTS: 1165/1165
WASM_A_B_TRACKED_IDENTITY: PASS (5,484,048 bytes, sha256=1b161d7eabd21f1996813fab53611b701abd6cd52f2345867932e636f76dcd4c, expected와 일치)
ACTUAL_EDGE_REGRESSION: PASS_REGRESSION_ONLY (ok:true, errors:0; 공개 provider 표면 증거로 해석 금지)
SSOT_DIFF: 0
PUBLIC_SPEC_DIFF: 0
UI_DIFF: 0
HISTORICAL_CORPUS_DIFF: 0
OFFICIAL_DB_BEFORE_AFTER: 540672 bytes / c8fdd4d47e20f7ad7ce4f095389991859432d5af0a87aa1f7b0b06e90fe44228, 전후 동일 (§9)
PROTECTED_PID_PORT: PID 53196 (python, StartTime 2026-08-08T12:27:21.8634297+09:00) / port 127.0.0.1:8787, 전후 동일
OFFICIAL_WRITE_COUNT: 0
ACTIVATION_CALL_COUNT: 0
REVIEW_RESOURCE_CLEANUP: COMPLETE (2 워크트리 + 4 격리 target + wasm_capture 디렉토리 + Edge 프로세스/프로필/포트 전부 제거 확인)
FINDINGS: 0 (blocking)
FOLLOW_UPS: 2 (non-blocking, §11)
NOTES: InternalTypedReactionRuntime은 standalone 시뮬레이션이며 실제 DdnRunner 디스패치 경로에 연결되지 않음(FOLLOW_UP-1); teul-cli eval.rs는 실경로 통합이나 registry가 항상 비어 있어 행동적으로는 no-op
FINAL_STATUS: PASS

W1C2_INTERNAL_TYPED_ROUTE_PROVIDER_SPLIT: PASS
REACTION_PROVIDER_PRODUCT_INTERNAL_ONLY
PUBLIC_PROVIDER_SURFACE: OPEN
W1_FULL_CLOSURE: OPEN
PUBLIC_ACTIVATION_NOT_AUTHORIZED
HUMAN_PASS_NOT_CLAIMED
```

**이 리뷰가 닫을 수 없는 항목** (directive §10 준수): `PUBLIC_KOREAN_NAME`, `PUBLIC_PROVIDER_EXACT_SYNTAX`, `PUBLIC_PROVIDER_SOURCE_INGRESS`, `STABLE_PROVIDER_IDENTITY_WIRE`, `STABLE_PROVIDER_DIAGNOSTICS`, `W1_FULL_CLOSURE`, `RENDEZVOUS_RUNTIME`, `WORKBENCH_STRUCTURED_DIAGNOSTIC_PROPAGATION`, `RD207_PUBLIC_STABLE_WIRE`, `PUBLIC_ACTIVATION`, `DEPLOYMENT`, `HUMAN_PASS` — 이 리뷰는 이 중 어느 것도 닫힘으로 주장하지 않는다.
