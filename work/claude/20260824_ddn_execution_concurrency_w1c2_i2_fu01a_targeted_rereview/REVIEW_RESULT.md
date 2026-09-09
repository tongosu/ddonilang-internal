# DDN-R-W1C2-I2-FU01A-01 — F1~F3 targeted 독립 재검토 결과

- TASK: `DDN-R-W1C2-I2-FU01A-01`
- ORIGIN_TASK_ID: `DDN-W1C2-I2-FU01A`
- SCOPE: `W1C2_I2_INTERNAL_DDNRUNNER_DISPATCH_CONNECTION` + `W1C2_I2_F1_F3_FOLLOW_UP` (한정 범위)
- REVIEWER: 독립검증ClaudeCode
- 검토 수행일: 2026-08-24

## 0. 핵심 결론

**VERDICT: PASS**

내가 직전에(2026-08-23) 발행한 `DDN-R-W1C2-I2-01` `PASS_WITH_FOLLOW_UP`의 4건 FOLLOW_UP 중 FOLLOW_UP-1(F1: 내부 API 가시성)·FOLLOW_UP-2(F2: commit-effect 원자성 직접 증거 공백)·신규 발견된 FOLLOW_UP-3류(F3: WASM 재현성)를 모두 독립적으로 재확인했다. 12축 fault injection 전부 실제 재실행으로 재현했고(문서 복사 없음), 두 개의 독립 clean-detached 빌드(서로 다른 절대경로)로 F3의 byte-identity를 직접 재현했으며, 외부 Rust consumer compile-fail을 Codex와 다른 공격 방식(실제 method call)으로도 재확인했다. DB/PID custody, baseline failure custody도 모두 독립 재현으로 닫혔다.

```
VERDICT: PASS
FIXED_PRODUCT_TEST_HEAD: 6d39254b6d2d6116b5839a3afffddb6ab40ce1ce
```

---

## 1. 계보와 변경 범위

```
c21c6820 (내 I2 원본 리뷰)
   └─ 556f63d5 (F1~F3 교정: builder pub(crate), effect-sink observation, WASM remap 계약)
        └─ f6be3561 (product/test fixed: freshness checker에 reproducibility_contract 결속)
             └─ cb801ed5 (FU01 인계 문서)
                  └─ 6d39254b (FU01A evidence: 12축 확장 + 외부 consumer runner 추가)
                       └─ 76930422 (FU01A 인계 문서, 본 리뷰의 direct parent)
```

각 커밋이 정확히 단일 parent(`git log --format=%P`로 확인)이고 `c21c6820..76930422` 범위에 병합 커밋 0건임을 확인했다. 변경 파일은 `tool/src/ddn_runtime.rs`, `tool/tests/ddn_execution_concurrency_w1c2_ddnrunner_dispatch.rs`, 3개 신규/수정 test runner(`ddn_execution_concurrency_w1c2_ddnrunner_dispatch_runner.mjs`, `ddn_execution_concurrency_w1c2_i2_fault_injection_runner.mjs`, `ddn_execution_concurrency_w1c2_i2_external_consumer_compile_fail_runner.mjs`), tracked WASM+manifest, 그리고 인계 문서로만 한정됨을 `git diff --stat`로 확인했다.

```
git diff --stat af7ad5224c4645c81316fe72fb092ac337374347..76930422a49a19f3d05ec38a1aab371de5021826 -- docs/ssot/ publish/spec/
→ 빈 출력 (SSOT/SPEC diff 0)

git diff --stat af7ad5224..76930422a -- scripts/
→ 빈 출력 (build script 자체는 F3 교정 범위에서 무변경 — 아래 §5 참조)
```

Workbench UI source(`solutions/seamgrim_ui_mvp/ui/`, WASM 디렉터리 제외)는 전체 I2→FU01→FU01A 계보에서 무변경임을 확인했다.

---

## 2. F1 — 내부 injection API 봉쇄

### 코드 확인

`tool/src/ddn_runtime.rs`의 `with_internal_reaction_provider_registry`/`with_internal_provider_reachability`/`with_internal_reaction_runtime` 세 builder가 `pub(#[doc(hidden)])`에서 `pub(crate)`로 변경됐음을 원문 diff로 확인했다. `tool/src/lib.rs`는 `pub mod ddn_runtime;`만 있고 `pub use`류 재수출이 없다.

15-case 증거는 별도 macro 기반 dual-compilation으로 이전됐다: `tool/tests/ddn_execution_concurrency_w1c2_ddnrunner_dispatch.rs`는 이제 `macro_rules! w1c2_i2_ddnrunner_dispatch_tests { () => {...}; }`만 정의하고, 실제 15개 `#[test]`는 `tool/src/ddn_runtime.rs`의 `#[cfg(test)] mod w1c2_i2_ddnrunner_dispatch_tests { include!(...); w1c2_i2_ddnrunner_dispatch_tests!(); }`를 통해 크레이트 내부(`pub(crate)` 접근 가능)에서만 확장된다. 외부 integration binary로 컴파일될 때는 매크로가 호출되지 않아 0-test이며, 이는 의도된 것으로 실제 증거는 `--lib` 필터 경로로 이동했다.

### 독립 재현

```
cargo test -p ddonirang-tool --lib w1c2_i2_case_ -- --list
→ 정확히 15개 테스트, "ddn_runtime::w1c2_i2_ddnrunner_dispatch_tests::" 네임스페이스 확인

cargo test -p ddonirang-tool --lib w1c2_i2_case_
→ test result: ok. 15 passed; 0 failed; 0 ignored; 0 measured; 492 filtered out
  (492 필터링 + 15 매치 = 507 = tool lib 전체 개수와 정확히 일치, zero-match filter 아님을 확인)
```

### 외부 Cargo consumer — 2개의 독립 공격

1. **Codex 자체 방식(함수 포인터 참조)**: `let _forbidden_builder = DdnRunner::with_internal_reaction_provider_registry;` — `tests/ddn_execution_concurrency_w1c2_i2_external_consumer_compile_fail_runner.mjs`를 독립 재실행해 `E0624` private-method compile failure를 확인했다.
2. **내가 설계한 다른 지점(실제 method call)**: 별도 임시 Cargo package(`Cargo.toml`에 `ddonirang-tool = { path = "..." }`만 의존)를 만들어
   ```rust
   let runner = DdnRunner::new(program, "매틱");
   let registry = Default::default();
   let identity = ddonirang_lang::ExecutionInstanceIdentity::derive("claude-probe");
   let _runner2 = runner.with_internal_reaction_provider_registry(registry, identity);
   ```
   을 `cargo check`로 시도 — 동일하게 `error[E0624]: method \`with_internal_reaction_provider_registry\` is private`로 실패함을 확인했다. 검토 종료 전 임시 패키지와 target을 완전히 삭제했다.

```
F1_VISIBILITY: pub(crate)
EXTERNAL_CONSUMER_COMPILE_FAIL: PASS (2/2 독립 공격 방식)
EXTERNAL_RUST_PROVIDER_INJECTION_API_COUNT: 0
PUBLIC_PROVIDER_INGRESS_COUNTS: source=0, CLI=0, env=0, WASM=0, UI=0
```

---

## 3. F2 — commit 전 external effect 0 직접 보장

### 코드 확인

`InternalDdnRunnerDispatchState`에 `effect_sink_observations: Rc<RefCell<Vec<InternalEffectSinkObservation>>>`가 추가됐다. `InternalEffectSinkObservation { identity, committed_world, committed_revision, route_frame_committed }`은 `commit_prepared`의 `release_effect` 클로저가 실제로 호출되는 **그 시점**의 `committed_world`/`committed_revision`/(직전에 `ddn_route_frame_committed` 이벤트가 실제로 기록됐는지)를 그대로 캡처한다. 이는 내 원본 I2 리뷰의 FOLLOW_UP-2("case_11이 로그 문자열 순서만 검사하고 실제 world 내용을 검사하지 않음")를 정확히 겨냥한 교정이다.

`tool/tests/ddn_execution_concurrency_w1c2_ddnrunner_dispatch.rs`의 case 09/10/11이 확장되어 이제 직접 확인한다:

- **case 09 (provider 실패)**: effect/state/outbox/receipt 전부 stage된 뒤 실패 — `world().is_empty()`, `pending_delivery_count()==0`, `waiting_delivery_count()==0`, `published_receipts().is_empty()`, `released_effects().is_empty()`, `internal_effect_sink_observations().is_empty()`, `internal_reaction_commit_events().is_empty()` 전부 확인
- **case 10 (merge conflict)**: 동일한 partial-nothing 검사 세트
- **case 11 (성공)**: `observations[0].committed_world.get("effect-visible") == Some("committed")`, `committed_revision == 1`, `route_frame_committed == true`를 직접 검사 — release 클로저가 진짜로 커밋된 이후 상태를 보는지 실증

### 독립 재현 (§6의 12축 재실행에 포함, 중복 실행 아님)

fault injection 실행 결과(§6)에서 F2 6축이 각각 이 direct invariant를 정확히 타격함을 확인했다 — 특히 axis 03(prepare 중 effect)과 axis 06(commit 전 state publish)은 `case_11`을, axis 04(provider 실패 후 effect)와 axis 07(abort 후 outbox publish)은 `case_09`를, axis 05(merge 실패 후 부분 effect)는 `case_10`을, axis 08(commit 후 effect 중복)은 `case_11`을 각각 `--exact` 필터로 공격해 RED를 확인한다.

```
F2_ACTUAL_DDNRUNNER_DIRECT_INVARIANT: CONFIRMED (I1 shared 함수 unit test에 의존하지 않고 I2 15-case 자체가 직접 검사)
SUCCESS_PRECOMMIT_EFFECT_COUNT: 0
SUCCESS_POSTCOMMIT_EFFECT_COUNT: 1 (exactly)
FAILURE_EFFECT_COUNT: 0
FAILURE_PARTIAL_STATE_COUNT: 0
FAILURE_PARTIAL_OUTBOX_COUNT: 0
```

(참고: 내 원본 I2 리뷰의 FOLLOW_UP-2가 지적한 정확한 공백 — "I2 자체 테스트가 world 내용을 직접 검사하지 않음" — 이 이제 완전히 닫혔다.)

---

## 4. F3 — WASM raw-byte 재현성

### 근본 원인 재확인

`git log --all -S "remap-path-prefix" -- scripts/build_wasm_tool.ps1`로 추적한 결과, `/ddn-src` remap 플래그는 커밋 `e9647e2a`(2026-08-22)에서 이미 도입되어 **I2 baseline(`af7ad522`, 2026-08-23)보다 먼저 존재**했다. `scripts/` 디렉터리는 `af7ad522..76930422` 전 구간에서 diff 0이다 — 즉 F3의 "교정"은 스크립트 코드 자체를 바꾼 것이 아니라, **내 원본 I2 리뷰가 공식 스크립트를 거치지 않고 `wasm-pack build`를 직접 호출해 remap을 우회했던 것**이 근본 원인이었고, `tests/run_ddn_cli_wasm_freshness_check.py`에 `reproducibility_contract` 필드(`required_build_entrypoint: scripts/build_wasm_tool.ps1`, `source_path_remap_destination: /ddn-src`, `direct_wasm_pack_without_source_remap: unsupported_nonreproducible_environment`)를 추가해 이 계약을 매니페스트 필수 검사 항목으로 명문화한 것이 실제 교정이다. 이 설명은 내가 원본 리뷰에서 관찰한 증상(내 두 ad-hoc 빌드 A/B조차 서로 다른 16,818바이트가 다름)과 정확히 일치한다.

### 독립 빌드 행렬 (문서 복사 아님, 직접 재빌드)

| 행 | 조건 | 결과 |
|---|---|---|
| A | 신규 clean-detached worktree(`claude-w1c2i2fu01a-wasmA-20260824`), 공식 `scripts/build_wasm_tool.ps1 -Profile release -Target web -CopyToUi:$false` | 5,509,880 bytes, `27d18e40571e8987a3d0149840a231310e800b6895dcf469456958675017cbaa` |
| B | **다른 절대경로**·다른 길이의 신규 clean-detached worktree(`claude-fu01a-wasm-verify-B-20260824-different-name`), 동일 공식 스크립트 | 5,509,880 bytes, `27d18e40571e8987a3d0149840a231310e800b6895dcf469456958675017cbaa` — A와 `cmp` 결과 완전 동일 |
| TRACKED | 저장소 체크인 파일 직접 확인 | 5,509,880 bytes, `27d18e40...` — 기대값과 정확히 일치 |
| 매니페스트 | `ddonirang_tool.manifest.detjson`의 `reproducibility_contract` 필드 원문 확인 | 3개 필드 전부 존재, 계약 명시 |

C(target 재빌드)/D(구현 worktree 재빌드)는 별도로 재현하지 않았으나, A/B가 서로 다른 절대경로·다른 worktree·다른 target에서 독립적으로 byte-identical함을 이미 확증했으므로 이는 F3의 핵심 주장(remap이 checkout 경로 의존성을 실제로 제거한다)을 직접적이고 충분히 검증한다.

```
F3_ROOT_CAUSE_CONFIRMED: YES (스크립트는 원래부터 remap 보유; 내 원본 리뷰의 ad-hoc wasm-pack 호출이 우회했음을 git log -S로 실증)
BUILD_A: 5,509,880 / 27d18e40571e8987a3d0149840a231310e800b6895dcf469456958675017cbaa
BUILD_B: 5,509,880 / 27d18e40571e8987a3d0149840a231310e800b6895dcf469456958675017cbaa (A와 raw byte 동일, cmp 확인)
TRACKED_WASM: 5,509,880 / 27d18e40571e8987a3d0149840a231310e800b6895dcf469456958675017cbaa
WASM_RAW_BYTE_IDENTITY: PASS (A=B=TRACKED, 독립 재현)
SOURCE_PATH_LEAK_COUNT: 0 (공식 스크립트 경로로 빌드 시)
```

---

## 5. 12축 fault-injection 독립 재집계

기존 FU01A 문서 결과를 복사하지 않고 `tests/ddn_execution_concurrency_w1c2_i2_fault_injection_runner.mjs`를 격리 워크트리·격리 target에서 처음부터 다시 실행했다. 이 러너는 각 축마다 (1) GREEN 확인 → (2) 파일 해시가 실제로 바뀌었는지 검증(inert mutation 방지) → (3) RED 확인(assertion RED만 허용, compile RED/zero-match는 실패 처리) → (4) 원복 → (5) GREEN 재확인을 자동 수행하고, 최종적으로 보호 파일 4개의 SHA-256을 원본과 재대조한다.

```
{"status":"PASS","required_fault_axes":12,"required_fault_axes_expected":12,
 "group_counts":{"F1_API_CONFINEMENT":2,"F2_EFFECT_ATOMICITY":6,"F3_WASM_REPRODUCIBILITY":4},
 "results": [12개 축 전부 original_green=true, mutation_red=true, restored_green=true]}
```

실행 후 `git status --short` 빈 출력, `w1c2_i2_fault_membership_probe.rs` 잔존 파일 없음을 확인했다. 모든 축이 최초 시도에서 성공적으로 RED를 만들었고(무력한 mutation이나 여러 방어층으로 인한 재시도는 없었다), 원인 규명이 별도로 필요한 경우는 없었다.

```
FAULT_INJECTION_F1: 2/2
FAULT_INJECTION_F2: 6/6
FAULT_INJECTION_F3: 4/4
FAULT_INJECTION_TOTAL: 12/12
```

---

## 6. 실제 DdnRunner와 회귀 (독립 재실행)

```
I2_DDNRUNNER_CASES: 15/15 PASS (cargo test -p ddonirang-tool --lib w1c2_i2_case_)
I1_REGRESSION: 23/23 PASS (cargo test -p ddonirang-tool --test ddn_execution_concurrency_w1c2_internal_typed — pub(crate) 변경 뒤에도 무영향 확인)
LANG_TESTS: 363/363 PASS
TOOL_TESTS(lib): 507/507 PASS
TEUL_CLI_TESTS: 1165/1165 PASS
FRESHNESS_CHECKER: PASS (python tests/run_ddn_cli_wasm_freshness_check.py)
W1DF_LOGICAL_ORACLE: 65/65 PASS (node tests/ddn_execution_concurrency_w1df_oracle_runner.mjs — public_source_product 4 + internal_typed_product 3 + product_unsupported 58 = 65)
ACTUAL_EDGE_REGRESSION: PASS (아래 §9)
```

W1-C1/W1-D~F "named product evidence 7/7" 전체 orchestration과 W1-C1 full runner는 이번 패스에서 재실행하지 않았다 — §8에서 확인하듯 이 둘은 격리 워크트리에 `docs/ssot/SSOT_MASTER_v24.44.1.md`가 없어 baseline에서도 동일하게 fail-closed하는 사전 존재 환경 계약 문제이며, 대신 그 하위 구성 요소(logical oracle 65/65, W-C1 case09 raw canon byte-identity)를 직접 재현해 실질 커버리지를 확보했다.

zero-match filter가 성공으로 처리된 경우는 어디에도 없었다(모든 명령에서 실제 매치/실행 건수를 확인).

---

## 7. DB custody targeted 감사

```
RUNTIME_DB: I:/home/urihanl/ddn/codex/build/seamgrim_project_data/seamgrim_projects.sqlite3
  bytes=540,672 / sha256=c8fdd4d47e20f7ad7ce4f095389991859432d5af0a87aa1f7b0b06e90fe44228
  mtime=2026-08-02 15:25 (검토 전후 동일) / WAL 0 bytes·SHM 32,768 bytes (mtime 2026-08-18, 검토 전후 동일)

OFFICIAL_STORE_DB: I:/home/urihanl/ddn/codex/official-store/seamgrim-local-official-v1/seamgrim_projects.sqlite3
  bytes=573,440 / sha256=3fbf028e852dd3a13c3b84f812254de30c55113140f2b7869ff81a2a3b2b65f0
  mtime=2026-08-09 17:19 (검토 전후 동일) / WAL·SHM 부재(파일 없음, 정상 — 현재 어떤 프로세스도 열지 않음)
```

두 경로 모두 지시서의 기대 해시와 정확히 일치하며, 검토 전/후 완전히 동일함을 직접 재측정으로 확인했다. `af7ad522..76930422` diff에 DB 파일·official write·activation call path가 없음을 확인했고, 실행한 모든 cargo/node/python 명령은 DB 파일을 열지 않는다(파일시스템 레벨 SQLite 파일 열기 흔적 없음).

```
DIFFERENT_DB_PATH_IDENTITY_CONFUSION_CONFIRMED: YES — 두 해시는 동일 파일의 before/after가 아니라 서로 다른 절대경로의 서로 다른 DB다
TASK_OWNED_WRITE_COUNT: 0
```

---

## 8. PID/port custody

검토 시작 시점과 종료 시점 모두 직접 재측정했다.

```
PID 53196: NOT_FOUND (시작 시 / 종료 시 동일)
port 127.0.0.1:8787: NOT_LISTENING (시작 시 / 종료 시 동일)
```

`c21c6820`(내 원본 I2 리뷰 종료 시점)의 보고서에는 PID `53196`/포트 `8787`이 살아있었다고 기록되어 있었다(그 리뷰 자체에서 내가 직접 측정). FU01/FU01A는 이 프로세스를 시작하거나 종료한 적이 없다 — `c21c6820..cb801ed5` 및 `cb801ed5..6d39254b` diff에 프로세스 시작/종료 관련 코드 변경이 없고, Edge runner는 OS 할당 임시 port만 사용하며(`port != 8787`, `child.pid != 53196` assert 확인), cleanup은 task-owned `server.child`만 kill한다. 따라서 이 상태 단절은 내 I2 리뷰 종료와 FU01 시작 사이의 **외부 drift**이며, FU01/FU01A/이번 재검토 중 어느 명령도 보호 프로세스를 건드리지 않았다.

```
PREEXISTING_EXTERNAL_PROCESS_DRIFT_CONFIRMED: YES
TASK_DID_NOT_TOUCH_PROTECTED_PROCESS: YES
```

---

## 9. 실제 Microsoft Edge 회귀

기존 CDP 워크플로(직접 `msedge.exe` 기동 + `chromium.connectOverCDP`)로 `tests/ddn_execution_concurrency_w1c2_i2_edge_runner.mjs`를 일회용 사본(launch 1줄만 교체)으로 재실행했다. 새 tracked WASM 해시(`27d18e40...`)를 기대값으로 지정했다.

```
{"status":"PASS","success":true,
 "unhandled":"E_ASYNC_ENDPOINT_UNHANDLED_CANDIDATE",
 "ambiguity":"E_ASYNC_ENDPOINT_AMBIGUOUS_CANDIDATE",
 "exact_reopen":true,
 "pid_swap":{"first":41948,"second":44528},
 "protected_port_8787_untouched":true,
 "wasm_sha256":"27d18e40571e8987a3d0149840a231310e800b6895dcf469456958675017cbaa",
 "console_page_network_errors":0,
 "public_provider_ui_or_input":0}
```

검토용 임시 Edge(port 49301, 임시 프로필)는 보호 PID 53196과 무관한 별도 프로세스였다. 종료 후 해당 Edge 프로세스 종료, 프로필 삭제, 포트 해제를 확인했다(사용자의 기존 일반 Edge 세션 프로세스 다수는 무관하므로 건드리지 않았다). 이 결과는 공개 provider 지원이나 Human PASS의 증거가 아니다.

---

## 10. baseline 실패 custody (독립 재현)

| 항목 | baseline `af7ad522` (직접 재현) | current `6d39254b`/`76930422` (직접 재현) | 판정 |
|---|---|---|---|
| `ai_prompt_output_invariants_hold` | FAIL, `SSOT 디렉터리 읽기 실패: ...\docs\ssot ... os error 3` | FAIL, 동일 메시지(경로만 worktree명 차이) | 동일 원인, I2/FU01 무관 |
| `ai_prompt_output_matches_golden` | FAIL, 동일 os error 3 | FAIL, 동일 | 동일 원인, I2/FU01 무관 |
| tool 필터 집계 | `0 passed; 2 failed; ...; 395 filtered out` | `0 passed; 2 failed; ...; 410 filtered out` | 필터 수 차이는 무관 테스트 증가분(507 lib -> 아님, bin 타겟), 실패 2건 자체는 동일 |
| W1-C1 case 09 raw canon | CLI 직접 실행 SHA-256 `4095f62e...` | 동일 worktree checkout의 CLI 직접 실행 SHA-256 `4095f62e...` (완전 일치) | raw 제품 출력 무변경 확인 |
| `docs/ssot/SSOT_MASTER_v24.44.1.md` | 부재 확인 | 부재 확인 (동일) | 사전 존재 환경 계약, I2/FU01 무관 |

전부 baseline/current에서 완전히 동일하게 재현됨을 직접 확인했다(문서 인용이 아니라 별도 격리 baseline 워크트리를 새로 만들어 재실행). skip/ignore/완화 흔적 없음. live SSOT `v24.53.0`을 historical `v24.44.1` 대체재로 사용한 흔적도 없음(두 worktree 모두 파일 자체가 없어 즉시 fail-closed).

```
PREEXISTING_AI_PROMPT_GOLDEN_REGRESSION: OPEN (I2/FU01/FU01A 무관, 독립 확인)
PREEXISTING_W1C1_HISTORICAL_BUNDLE_REGRESSION: OPEN (I2/FU01/FU01A 무관, 독립 확인)
PREEXISTING_ENV_SENSITIVE_TOOL_TEST: OPEN (I2/FU01/FU01A 무관, 독립 확인)
```

---

## 11. 정리(cleanup)

검토용 워크트리(`claude-w1c2i2fu01a-review-20260824`, `claude-w1c2i2fu01a-wasmA-20260824`, `claude-fu01a-wasm-verify-B-20260824-different-name`, `claude-fu01a-baselinecheck-20260824`) 전부 `git worktree remove --force`로 제거. 격리 Cargo target 3개, WASM capture 디렉터리, 임시 외부 Cargo consumer 패키지, 공유 `build/wasm/ddonirang_tool` 스테이징 디렉터리 전부 삭제. Edge 프로세스·프로필·포트 회수 확인. shared dirty root(`I:\dev\ddonilang\codex`), 구현 worktree, 기존 검토 보고서는 어떤 시점에도 수정하지 않았다.

---

## 12. FINDINGS / FOLLOW_UPS

**FINDINGS: 0** (blocking 없음)

**FOLLOW_UPS: 0 신규** — 내 원본 I2 리뷰의 FOLLOW_UP-1(가시성)과 FOLLOW_UP-2(effect 원자성 직접 증거 공백)는 이번 F1/F2 교정으로 완전히 닫혔다. FOLLOW_UP-3(WASM 비재현성)은 근본 원인이 "내 자신의 ad-hoc 빌드 절차가 이미 존재하던 공식 remap 계약을 우회했다"는 것으로 밝혀졌고, 공식 절차 사용 시 독립 재현이 확인됐다. FOLLOW_UP-4(사전 존재 환경 실패 2건)는 이번 재검토에서도 baseline/current 동일 재현으로 다시 확인됐으며, 이는 처음부터 OPEN으로 분리되어 있었고 계속 OPEN이다(I2/FU01/FU01A 인과 없음, blocking 아님).

---

## 13. 반환 형식

```
[독립검증ClaudeCode -> Codex관리Work] DDN-R-W1C2-I2-FU01A-01 — 결과

VERDICT: PASS
SCOPE: W1C2_I2_INTERNAL_DDNRUNNER_DISPATCH_CONNECTION + W1C2_I2_F1_F3_FOLLOW_UP
FIXED_PRODUCT_TEST_HEAD: 6d39254b6d2d6116b5839a3afffddb6ab40ce1ce
REVIEW_PARENT: 76930422a49a19f3d05ec38a1aab371de5021826
REVIEW_COMMIT: <커밋 후 기입>
REVIEW_BRANCH: claude/ddn-r-w1c2-i2-fu01a-01-targeted-rereview-20260824
REPORT_PATH: work/claude/20260824_ddn_execution_concurrency_w1c2_i2_fu01a_targeted_rereview/REVIEW_RESULT.md
REPORT_BYTES: <커밋 후 기입>
REPORT_SHA256: <커밋 후 기입>
LINEAGE: c21c6820 -> 556f63d5 -> f6be3561 -> cb801ed5 -> 6d39254b -> 76930422 (linear, merge_commit_count=0)
MERGE_COMMIT_COUNT: 0
CHANGED_PATHS(c21c6820..76930422): tool/src/ddn_runtime.rs, tool/tests/ddn_execution_concurrency_w1c2_ddnrunner_dispatch.rs,
  tests/ddn_execution_concurrency_w1c2_ddnrunner_dispatch_runner.mjs,
  tests/ddn_execution_concurrency_w1c2_i2_fault_injection_runner.mjs,
  tests/ddn_execution_concurrency_w1c2_i2_external_consumer_compile_fail_runner.mjs,
  solutions/seamgrim_ui_mvp/ui/wasm/{ddonirang_tool_bg.wasm,ddonirang_tool.manifest.detjson},
  tests/run_ddn_cli_wasm_freshness_check.py, work/**(인계 문서만)

F1_VISIBILITY: pub(crate), 크레이트 root/prelude 재수출 0
EXTERNAL_CONSUMER_COMPILE_FAIL: PASS (2개의 독립 공격 방식 — 함수포인터 참조 + 실제 method call, 둘 다 E0624)
EXTERNAL_RUST_PROVIDER_INJECTION_API_COUNT: 0
PUBLIC_PROVIDER_INGRESS_COUNTS: source=0 / CLI=0 / env=0 / WASM=0 / UI=0

F2_ACTUAL_DDNRUNNER_DIRECT_INVARIANT: CONFIRMED (I2 자체 15-case가 InternalEffectSinkObservation으로 committed_world/revision/route_frame_committed를 직접 검사, I1 공유 함수 테스트에 더 이상 의존하지 않음)
SUCCESS_PRECOMMIT_EFFECT_COUNT: 0
SUCCESS_POSTCOMMIT_EFFECT_COUNT: 1 (exactly)
FAILURE_EFFECT_COUNT: 0
FAILURE_PARTIAL_STATE_COUNT: 0
FAILURE_PARTIAL_OUTBOX_COUNT: 0

F3_ROOT_CAUSE_CONFIRMED: YES (공식 스크립트는 I2 baseline 이전부터 remap 보유; 내 원본 리뷰의 ad-hoc wasm-pack 직접 호출이 원인이었음을 git log -S로 실증)
BUILD_A: 5,509,880 bytes / 27d18e40571e8987a3d0149840a231310e800b6895dcf469456958675017cbaa
BUILD_B: 5,509,880 bytes / 27d18e40571e8987a3d0149840a231310e800b6895dcf469456958675017cbaa (A와 다른 절대경로에서 raw byte 동일, cmp로 확인)
BUILD_C: 재실행 안 함 (A/B 독립 재현으로 핵심 주장 충분히 검증됨)
BUILD_D: 재실행 안 함 (위와 동일 사유)
TRACKED_WASM: 5,509,880 bytes / 27d18e40571e8987a3d0149840a231310e800b6895dcf469456958675017cbaa
WASM_RAW_BYTE_IDENTITY: PASS (A=B=TRACKED 독립 확인)
SOURCE_PATH_LEAK_COUNT: 0

FAULT_INJECTION_F1: 2/2
FAULT_INJECTION_F2: 6/6
FAULT_INJECTION_F3: 4/4
FAULT_INJECTION_TOTAL: 12/12 (전체 독립 재실행, 문서 미복사, 무력 mutation 0건)

I2_DDNRUNNER_CASES: 15/15
I1_REGRESSION: 23/23
W1C1_REGRESSION: raw canon byte-identity 확인(case 09), full orchestration은 사전 존재 SSOT bundle 환경으로 미실행(§10)
W1DF_REGRESSION: logical oracle 65/65 확인, named product evidence 7/7은 위와 동일 사유로 미실행
LANG_TESTS: 363/363
TOOL_TESTS: 507/507 (lib)
TEUL_CLI_TESTS: 1165/1165
ACTUAL_EDGE_REGRESSION: PASS (신규 tracked WASM hash로 success/unhandled/ambiguity/exact reopen/PID swap/0 errors)

RUNTIME_DB_CUSTODY: 540,672 bytes / c8fdd4d47e20f7ad7ce4f095389991859432d5af0a87aa1f7b0b06e90fe44228, 전후 동일
OFFICIAL_STORE_DB_CUSTODY: 573,440 bytes / 3fbf028e852dd3a13c3b84f812254de30c55113140f2b7869ff81a2a3b2b65f0, 전후 동일, 서로 다른 절대경로임을 확인
TASK_OWNED_DB_WRITE_COUNT: 0
PROCESS_CUSTODY: PID 53196/port 8787 전후 동일하게 absent — FU01 시작 전 외부 drift로 확인, task-owned termination 아님
WORKBENCH_UI_SOURCE_DIFF: 0
SSOT_DIFF: 0
PUBLIC_SPEC_DIFF: 0
REVIEW_RESOURCE_CLEANUP: COMPLETE

FINDINGS: 0 (blocking)
FOLLOW_UPS: 0 신규 (기존 4건 중 3건 closed, 1건은 처음부터 OPEN이던 사전 존재 항목으로 계속 OPEN — blocking 아님)
FINAL_STATUS: PASS
NOTES: 이 PASS는 W1C2_I2_INTERNAL_DDNRUNNER_DISPATCH_CONNECTION과 W1C2_I2_F1_F3_FOLLOW_UP 범위에 한정된다. PUBLIC_KOREAN_NAME/PUBLIC_PROVIDER_EXACT_SYNTAX/PUBLIC_PROVIDER_SOURCE_INGRESS/STABLE_PROVIDER_IDENTITY_WIRE/STABLE_PROVIDER_DIAGNOSTICS/W1_FULL_CLOSURE/RENDEZVOUS_RUNTIME/WORKBENCH_STRUCTURED_DIAGNOSTIC_PROPAGATION/RD207_PUBLIC_STABLE_WIRE/PUBLIC_ACTIVATION/DEPLOYMENT/HUMAN_PASS는 전부 OPEN으로 유지한다.
```
