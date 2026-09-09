# DDN execution concurrency W1-D~F 구현 인계

## 상태와 계보

```text
GOAL_ID: DDN_EXECUTION_CONCURRENCY_W1D_W1F_ASYNC_WAIT_OUTBOX_AUTHORITY_CONVERGENCE_W1
W1C1_CLOSURE_BASELINE: eca2fbc50cd5cd50af299aad4fd87f33683c575a
W1C1_REVIEW_PARENT: c8b0f3d46c4d400d0ed83431974c8badacd2295c
W1DF_CORE_COMMIT: e46f653dae14b5b36564a7d1732aa5198f37a815
WASM_REPRO_CORRECTION: e9647e2ad39a30c7c8b19be118f1d0a2bfe23887
PRODUCT_AND_TEST_FIXED_HEAD: d8a4b2ab5b7c5fe68b1738f955d2d3d5b2b86ad1
MERGE_COMMITS_FROM_BASELINE: 0
```

기존 W1-C1 plain PASS closure의 선형 successor에서만 작업했다. Malhimnuri R2 연구
worktree는 `efe7fcf5ed1285eafb65ca95bac9f85824fafcb9` clean 상태로 보존했고 현재 계보의
ancestor가 아니다. 새 공개 의미, SSOT/SPEC 승격, UI, 배포, activation은 수행하지 않았다.

## migration map과 writer ownership

| old/current surface | current semantic owner | 이번 disposition | 남은 OPEN |
|---|---|---|---|
| tool immediate async dispatch | `lang/src/delivery.rs` + tool adapter | 공통 `LogicalAsyncQueue`로 FIFO tail/no-reentry 결속 | rendezvous runtime |
| teul-cli local bounded queue의 full 오류 | 공통 queue admission | full envelope ownership을 유지하는 logical WAIT/RESUME로 교체 | 공개 capacity contract/wire |
| handler 안 nested send | `StagedDeliveryOutbox` | reaction frame 성공 뒤에만 FIFO publish; 오류면 frame 폐기 | structured group 전체 |
| route 0/1/>1와 internal provider | W1-C1 `EndpointRoute`/occurrence authority | 변경 없이 누적 parity 재검증 | W1-C2 public provider surface |
| top-level sender `누리` fallback | shared sender contract | successor async에서 명시 sender 없으면 fail-closed | public diagnostic promotion |
| physical worker/declaration order | 의미 권위 아님 | wait/route/provider identity material에서 제외 | 실제 public worker API 없음 |
| old `~~>` async와 historical receive hooks | historical migration evidence | 원 corpus와 runner byte 변경 0 | 명시 migration batch |
| `<<-` fixed-point 역사 | 별도 persistent dependency migration | 변경 0 | coherent settle/cycle-fail migration |
| rendezvous `<~~/~~>` | distinct typed family | runtime fail-closed 유지 | rendezvous/HandoffEvent goal |

단일 writer는 다음과 같다.

```text
typed delivery/wait/outbox authority: lang/src/delivery.rs
native/WASM product adapter: tool/src/ddn_runtime.rs
teul compatibility adapter: tools/teul-cli/src/runtime/eval.rs
logical successor oracle owner: pack/future_grammar_atlas_owner_closed_delta_r2_w1df
```

## typed IR와 runtime 변화

- `LogicalDeliveryPhase::{Admit,Wait,Resume,Start,Settle,Terminal,CleanupJoin,Preflight,Publish,Release}`를
  product-local typed phase로 분리했다.
- `WaitNodeIdentity`는 queue identity, operation identity, logical admission ordinal의
  domain-separated canonical digest다. source span, vector/worker order를 포함하지 않는다.
- `LogicalWaitReceipt`, `LogicalWaitEdge`, `WaitDomain`과 `LogicalWaitGraph::classify`가
  progress, sealed internal deadlock, sealed external open wait를 구분한다.
- bounded full은 `QueueAdmission::Waiting`이며 queue가 envelope ownership을 유지한다.
  slot release 시 오래된 waiter부터 pending tail로 승격되고 silent drop은 없다.
- authored cancellation은 stable wait identity 한 건만 제거한다.
- `StagedDeliveryOutbox`는 nested frame 성공을 parent에 합치고 outermost success에서만
  queue로 publish한다. abort는 해당 frame만 폐기한다.
- tool과 teul-cli의 state-machine/contract snapshot이 queue, outbox, wait receipt를
  보존한다. handler 오류는 상태·trace·diagnostic·RNG 관찰 산출물을 원복하되 실제 실행된
  work prefix 비용은 되돌리지 않는다.
- owner 밖 successor send는 임의 `누리` identity를 만들지 않고
  `E_ASYNC_SENDER_IDENTITY_UNRESOLVED_CANDIDATE`로 fail-closed한다.

이번 vertical의 parser/canon 신규 변경은 0이다. `<~/~>` async, `<~~/~~>` rendezvous,
sender-filter exact surface는 독립 PASS된 W1-B/W1-C1 baseline을 그대로 사용한다.

## exact touched paths

제품/공통 authority:

```text
lang/src/delivery.rs
lang/src/lib.rs
tool/src/ddn_runtime.rs
tools/teul-cli/src/runtime/eval.rs
tools/teul-cli/src/runtime/error.rs
tools/teul-cli/src/cli/run.rs
scripts/build_wasm_tool.ps1
solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm
solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson
```

pack/test:

```text
pack/future_grammar_atlas_owner_closed_delta_r2_w1df/README.md
pack/future_grammar_atlas_owner_closed_delta_r2_w1df/build_oracle.mjs
pack/future_grammar_atlas_owner_closed_delta_r2_w1df/logical_oracle.jsonl
tests/ddn_execution_concurrency_w1df_oracle_runner.mjs
```

## successor D-PACK와 matrix

`logical_oracle.jsonl`은 65개 고유 `case_id`와 65개 고유 `owner_delta_id`를 가진다.

| group | cases |
|---|---:|
| temporal/completion | 16 |
| cohort/retry | 12 |
| cancel/async | 15 |
| resource admission | 3 |
| flow/reclamation | 10 |
| effect/wait | 7 |
| configuration | 2 |

- oracle SHA-256: `73b2ee48dd12033c1e5ed45d7052979fdfc35a6017cc12599e521afd3f8ae8d3`
- `PRODUCT_PASS`: 누적 W1-C1 route/internal provider와 W1-D~F FIFO/WAIT/outbox에
  직접 대응하는 7건.
- `PRODUCT_UNSUPPORTED`: temporal, structured concurrency, dependency, rendezvous,
  external effect의 58건. 기대값을 완화하거나 제품 PASS로 표시하지 않았다.
- Node worker thread 1/2/8과 same-tag forward/reverse/shuffled의 9개 실제 oracle
  실행이 같은 canonical result digest
  `8d5160b13ad4726cbad895cf313a750cf2bd4337d3326e7bf811d5903ee8ac6c`로 수렴한다.
- worker digest fault는 exit 1 RED, 원복 뒤 동일 oracle hash GREEN이다.

이 worker 검증은 logical oracle의 물리 배치 비의미성을 확인한다. 제품에 공개된
configurable worker-pool API가 생겼다는 주장은 하지 않는다.

## 검증 결과

| 검증 | 결과 |
|---|---|
| `cargo test -p ddonirang-lang delivery --lib` | 14 PASS |
| `cargo test -p ddonirang-tool successor_async --lib` | 4 PASS |
| `cargo test --manifest-path tools/teul-cli/Cargo.toml successor_async` | 6 PASS |
| W1-C1 native/source-WASM/tracked-WASM parity | 10/10, success 6/failure 4 |
| W1-F 65-case oracle | 65/65, 9 worker/permutation runs |
| oracle fault injection | expected RED exit 1, restore GREEN |
| `git diff --check` | PASS |
| source build A/B/tracked WASM identity | PASS |
| clean-detached Rust/oracle/parity | PASS |
| clean-detached source/tracked WASM identity | PASS after correction |

최종 tracked web-release WASM은 5,482,770 bytes, SHA-256
`fbccef544253e2ffe1c05abda1826ce34e785a4de193bfe59dec48d7898dde05`다.

첫 clean-detached 빌드는 checkout 절대 경로가 release WASM string data에 들어가 64-byte
차이를 드러냈다. 이를 숨기지 않고 `scripts/build_wasm_tool.ps1`에
`--remap-path-prefix=<repo>=/ddn-src`를 결속했다. 교정 뒤 격리 build A/B와 다른
clean-detached worktree가 위 bytes/hash로 정확히 수렴했다.

## 보호 경계

```text
docs/ssot/** diff: 0
publish/spec/** diff: 0
Workbench UI source diff: 0
historical W1-B/W1-C1 pack/runner diff: 0
Malhimnuri R2 ancestry/change: 0
official DB current measurement: 540672 bytes
official DB current SHA-256: c8fdd4d47e20f7ad7ce4f095389991859432d5af0a87aa1f7b0b06e90fe44228
official DB current mtime: 2026-08-02 15:25:18.9785384 +09:00
superseded stale citation: 573440 bytes / 3fbf028e852dd3a13c3b84f812254de30c55113140f2b7869ff81a2a3b2b65f0
custody: read-only remeasurement; DB copy/replace/write 0
PID 53196 start: 2026-08-08T12:27:21.8634297+09:00
127.0.0.1:8787 owner: 53196
official store writes: 0
activation calls: 0
```

## PASS / OPEN matrix

| 항목 | 상태 |
|---|---|
| shared FIFO/no-reentry logical authority | PRODUCT_PASS, independent review pending |
| bounded WAIT ownership/FIFO resume/cancel hook | PRODUCT_PASS, independent review pending |
| staged nested outbox/failure atomicity | PRODUCT_PASS, independent review pending |
| 65-case logical oracle | LOGICAL_ORACLE PASS; 58 PRODUCT_UNSUPPORTED |
| W1-C2 public ReactionProvider surface | OPEN |
| Workbench structured diagnostic propagation | OPEN; UI change unauthorized |
| rendezvous runtime/HandoffEvent | OPEN |
| persistent `<<-` coherent dependency | OPEN |
| structured groups, effects, resource admission full system | OPEN |
| RD-207 stable public wire | OPEN |
| W1 full closure/public activation/Human PASS | OPEN |

## 구현 세션 최종 상태

```text
DDN_EXECUTION_CONCURRENCY_W1D_W1F_ASYNC_WAIT_OUTBOX_AUTHORITY_CONVERGENCE_W1_IMPLEMENTED_UNDER_REVIEW
W1D_SHARED_LOGICAL_DELIVERY_FIFO_NO_REENTRY_LANDED
W1E_BOUNDED_WAIT_AND_STAGED_OUTBOX_LANDED
W1F_65_CASE_LOGICAL_ORACLE_AND_WORKER_MATRIX_LANDED
READY_FOR_DDN_EXECUTION_CONCURRENCY_W1D_W1F_INDEPENDENT_REVIEW

WORKBENCH_STRUCTURED_DIAGNOSTIC_PROPAGATION_OPEN
UI_CHANGE_NOT_AUTHORIZED
W1C2_REACTION_PROVIDER_PUBLIC_SURFACE_OPEN
RENDEZVOUS_RUNTIME_OPEN
RD207_PUBLIC_STABLE_WIRE_OPEN
W1_FULL_CLOSURE_OPEN
PUBLIC_ACTIVATION_NOT_AUTHORIZED
HUMAN_PASS_NOT_CLAIMED
external_user_success_count: 0
```

Codex는 독립 `PASS`, W1 full `CLOSED`, public release 또는 Human PASS를 발행하지 않는다.
