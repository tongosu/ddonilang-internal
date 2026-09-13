# DDN EXECUTION / CONCURRENCY SURFACE MIGRATION W1

## 판정

```text
DDN_EXECUTION_CONCURRENCY_SURFACE_MIGRATION_W1_FIRST_SAFE_ASYNC_VERTICAL_IMPLEMENTED_UNDER_REVIEW
W1_FULL_CLOSURE_NOT_CLAIMED
HUMAN_PASS_NOT_CLAIMED
PUBLIC_ACTIVATION_NOT_AUTHORIZED
```

이번 변경은 v24.45.1의 successor async 의미를 제품의 typed identity, parser/canon,
logical queue, EndpointRoute cardinality 및 별도 successor D-PACK에 처음 착지시킨다.
W1 전체 DoD는 아직 닫히지 않았으며 아래 OPEN 항목을 승격하지 않는다.

## 1. baseline

- 권위 조사 root: `I:/dev/ddonilang/codex`
- 권위 조사 시작 HEAD: `a000e262cb96b51007286e2fb70bb2fa31e2af32`
- root 시작 dirty/status: `1,073`, staged `0`
- root 마지막 관찰 dirty/status: `1,078`, staged `0`
- 다른 세션이 root를 계속 변경했으므로 root dirty는 수정·정리·stage하지 않았다.
- 구현 fixed base: `de9cb9ed95f71910bedd2b1bce0769a8257a7f27`
- 구현 commit: `aaf72e08498031feeabfabc6692316e42dcfdc42`
- current authority at 조사 시점: SSOT `v24.45.1 / RD-001~299`
- SSOT_ALL: `eeccf1a82e056c52fdb88fa2a189791b5be5a27f6f739900fa53d34da80d0102`
- public SPEC: `v0.5.0`

구현 fixed base는 검증된 G30 제품 계보이고, 최신 권위 문서는 dirty root에서 읽기 전용으로
감사했다. 따라서 통합 시에는 최신 root와의 authority drift를 다시 감사해야 한다.

## 2. session/worktree ownership plan

| 범위 | 단일 writer / 소유권 | disposition |
|---|---|---|
| typed delivery identity/cardinality/queue | 이 branch의 `lang/src/delivery.rs` | W1 semantic source |
| shared tool/native/WASM adapter | 이 branch의 `tool/src/ddn_runtime.rs` | 첫 async vertical |
| teul legacy runtime adapter | 이 branch의 `tools/teul-cli/src/runtime/eval.rs` | parity adapter |
| parser/token/canon | 각 lang frontdoor adapter, identity는 `ddonirang_lang` 사용 | 부분 결속 |
| successor corpus | 새 `pack/future_grammar_atlas_owner_closed_delta_r2/**`만 | historical overwrite 금지 |
| SSOT/public SPEC | SSOT 관리자/owner | 이 branch 수정 금지, diff 0 |
| root dirty/다른 세션 작업 | 각 기존 session owner | 비침범 |

## 3. migration map

| old surface / conflict | current AST/IR · canon · runtime | current evidence | successor identity | 이번 disposition |
|---|---|---|---|---|
| `~~>` async | 과거 `Stmt::Send` 단일 의미, canon `~~>`, teul pending FIFO와 tool/lowerer dispatch가 병존 | `lang_consistency_v1`, event dispatch packs, 39 `.ddn` / 95 occurrences | `HistoricalAsyncSend`; 새 async는 `AsyncSend` | 역사 source 무수정. parser에서 historical identity로 분리했으나 successor parser reject/migration-only mode는 `PRODUCT-OPEN` |
| `<~ / ~>` | 과거 전용 typed identity 없음 | 새 successor pack | `AsyncSend` | 양방향 token/parser, canon `~>`, product runtime 착지 `PASS` |
| `<~~ / ~~>` rendezvous | `~~>`가 historical async와 충돌 | 없음/연구 권위 | `RendezvousSend`, `RendezvousReceive` | `<~~`는 typed parse 후 `E_RENDEZVOUS_PRODUCT_OPEN`; right `~~>` clean cut과 HandoffEvent는 `PRODUCT-OPEN` |
| multi-handler declaration/rank fan-out | teul `eval_receive_handlers`, tool/canon lowering이 여러 handler를 순서로 실행 | `lang_consistency_v1/c23`, 관련 reaction packs | exactly-one `EndpointRoute`, 이후 별도 `ReactionProvider` | successor async 0/1/>1 cardinality `PASS`; provider-key dedup/fan-out은 `PRODUCT-OPEN` |
| teul FIFO/no-reentry vs tool immediate dispatch | teul `pending_signals` + guard, tool `dispatch_signal_send`, preprocess/canon static lowering | historical queue packs | `LogicalAsyncQueue<E>` | 두 runtime이 공통 queue/cardinality 타입 사용, nested tail tests `PASS`; 모든 lowering/frontdoor 단일화는 `PRODUCT-OPEN` |
| `받으면` sender-unfiltered | receiver/type/predicate 중심 old hooks | historical receive packs | passive async route + sender predicate | exact sender-filter surface/IR binding은 `PRODUCT-OPEN` |
| bounded queue | old successor contract 없음 | 없음 | capacity + WAIT slot | capacity `100,000`, `EnqueueOutcome::Wait(envelope)`, no silent drop `PASS`; resumable WaitEdge/receipt는 `PRODUCT-OPEN` |
| `<<-` fixed-point naming | teul `apply_flow_fixed_point`, conflict/cycle tests | 5 `.ddn` / 7 occurrences, `lang_flow_hook_interaction_v1` | `PersistentDependency` | lang token을 message arrow와 분리하고 shared lowering은 fail-closed. coherent topological settle migration은 `PRODUCT-OPEN` |
| `lang/currentline.rs` regex dispatch | 별도 immediate/silent-unhandled/duplicate-overwrite semantics | currentline tests | shared delivery adapter | `PRODUCT-OPEN` |
| `tools/teul-cli/src/canon.rs` lowerer | 자체 source-order fan-out/canon ownership | canon tests | shared typed frontdoor | `PRODUCT-OPEN` |
| cross-group reaction/outbox | 구현 증거 없음 | logical contract only | staged outbox/reaction closure | `PRODUCT-OPEN` |

`PlanValue`, `ExecutionRelation`, `CompositeWork`, `AttemptIdentity`, `EffectIntent`,
`WaitGraph/WaitEdge`, `ResourceAdmission`, `HandoffEvent`는 `MessageTransfer`와 별도 타입
family로 후속 추가할 수 있다. 이번 구현은 외부 effect나 physical worker identity를
message identity에 넣지 않았다.

## 4. exact touched paths

제품/런타임:

```text
lang/src/ast.rs
lang/src/delivery.rs
lang/src/lexer.rs
lang/src/lib.rs
lang/src/normalizer.rs
lang/src/parser.rs
tool/src/ddn_runtime.rs
tools/teul-cli/src/cli/run.rs
tools/teul-cli/src/lang/ast.rs
tools/teul-cli/src/lang/lexer.rs
tools/teul-cli/src/lang/parser.rs
tools/teul-cli/src/lang/token.rs
tools/teul-cli/src/runtime/error.rs
tools/teul-cli/src/runtime/eval.rs
```

successor D-PACK:

```text
pack/future_grammar_atlas_owner_closed_delta_r2/README.md
pack/future_grammar_atlas_owner_closed_delta_r2/golden.jsonl
pack/future_grammar_atlas_owner_closed_delta_r2/logical_oracle.jsonl
pack/future_grammar_atlas_owner_closed_delta_r2/c01_async_left_exact_one/input.ddn
pack/future_grammar_atlas_owner_closed_delta_r2/c02_async_zero_route_EXPECT_FAIL/input.ddn
pack/future_grammar_atlas_owner_closed_delta_r2/c03_async_multiple_route_EXPECT_FAIL/input.ddn
pack/future_grammar_atlas_owner_closed_delta_r2/c04_async_nested_fifo_tail/input.ddn
```

인계/운영 문서:

```text
work/codex/20260821_ddn_execution_concurrency_surface_migration_w1/MIGRATION_MAP_AND_IMPLEMENTATION_HANDOFF.md
work/codex/20260821_ddn_execution_concurrency_surface_migration_w1/TARGETED_INDEPENDENT_REVIEW_REQUEST.md
work/_session_deltas/20260821_codex_ddn_execution_concurrency_surface_migration_w1.md
```

## 5. typed IR / parser / canon

- 공통 typed family: `AsyncSend`, `RendezvousSend`, `RendezvousReceive`,
  `HistoricalAsyncSend`, `EndpointRoute`, `ReactionProvider`, `PersistentDependency`.
- `Stmt::Send`는 `MessageTransfer`를 반드시 가진다.
- `<~`와 `~>`는 같은 `MessageTransfer::ASYNC`로 수렴한다.
- `<~~`는 `MessageTransfer::RENDEZVOUS`로 분리되며 runtime에서 fail-closed 한다.
- old `~~>`는 `MessageTransfer::HISTORICAL_ASYNC`로만 들어간다.
- successor async canonical form은 `~>`다.
- `<<-`는 lang token에서 `PersistentDependencyArrow`로 분리되며 미구현 lowering은
  `E_PERSISTENT_DEPENDENCY_PRODUCT_OPEN`으로 닫힌다.

## 6. runtime / route / capacity

- `LogicalAsyncQueue<E>`는 FIFO, bounded capacity, nested `begin_drain()` 거부를
  공통 소유한다.
- route 후보는 receiver/type/predicate를 평가한 집합으로 만든 뒤 cardinality만 본다.
- 0 match: `E_ASYNC_ENDPOINT_UNHANDLED`.
- 1 match: 한 consuming delivery.
- 2+ match: `E_ASYNC_ENDPOINT_AMBIGUOUS`.
- handler 안에서 발생한 async send는 queue tail에 들어가 현재 handler가 끝난 뒤 실행된다.
- full queue는 envelope ownership을 `Wait(envelope)`로 돌려주며 silent drop하지 않는다.
- 현재 single-thread adapter는 resumable wait graph가 없으므로
  `E_ASYNC_QUEUE_WAIT_REQUIRED`로 fail-closed 한다.
- `ReactionProvider` identity는 route와 분리했지만 provider fan-out runtime은 구현하지 않았다.

## 7. tests / goldens

```text
cargo test -p ddonirang-lang
342 passed / 0 failed

cargo test -p ddonirang-tool --lib
484 passed / 0 failed

cargo test --manifest-path tools/teul-cli/Cargo.toml
1,159 passed / 0 failed

cargo check -p ddonirang-tool --target wasm32-unknown-unknown --lib
PASS

python tests/run_pack_golden.py future_grammar_atlas_owner_closed_delta_r2
4/4 PASS

python tests/run_alrim_dispatch_runtime_contract_selftest.py
PASS

git diff --check
PASS

rustfmt --edition 2024 --check lang/src/delivery.rs
PASS
```

역사 corpus 탐색 실행은 다음 기존 불일치를 재현했다.

```text
lang_consistency_v1: 18 failures
patent_c_single_funnel_nonreentry_queue_v1: 1 failure
lang_flow_hook_interaction_v1 checker: c01 failure
```

이 세 pack과 runner는 이번 commit에서 수정하지 않았다. 불일치에는 shared runtime
frontdoor/기대 diagnostic/fixed-point 표현 drift가 섞여 있다. 별도 fixed-base 비교용
worktree 생성이 checkout 제한 시간에 걸려 불완전 상태가 되었고 즉시 제거했으므로,
이번 문서는 이를 baseline failure 또는 새 regression 중 어느 쪽으로도 과장 분류하지
않는다. 정확한 귀속 재검토는 `PRODUCT-OPEN`이다.

## 8. PASS / PRODUCT-OPEN matrix

| 항목 | 결과 |
|---|---|
| latest authority/root dirty 기록 | PASS |
| migration map / owner plan | PASS |
| typed async/rendezvous/dataflow identities 분리 | PASS (runtime은 각 OPEN 경계 유지) |
| `<~ / ~>` parser/canon | PASS |
| successor async EndpointRoute 0/1/>1 | PASS |
| FIFO tail / no direct reentry | PASS |
| bounded capacity / no silent drop hook | PASS |
| tool/teul runtime shared type + 표적 의미 parity | PASS |
| successor D-PACK subset | 4/4 PASS |
| historical fixture overwrite 없음 | PASS |
| old `~~>` successor reject/migration-only | PRODUCT-OPEN |
| ReactionProvider dedup/fan-out | PRODUCT-OPEN |
| async sender filter | PRODUCT-OPEN |
| worker 1/2/8 + same-tag permutation | PRODUCT-OPEN |
| cross-group staged outbox / reaction closure | PRODUCT-OPEN |
| resumable WAIT edge/receipt | PRODUCT-OPEN |
| full frontdoor/canon/currentline single authority | PRODUCT-OPEN |
| rendezvous `~~>`/ReadyReceive/HandoffEvent | PRODUCT-OPEN |
| persistent coherent settle / zero-delay cycle migration | PRODUCT-OPEN |
| 전체 65 logical fixtures | PRODUCT-OPEN; 현재 4-case subset only |

## 9. historical preservation

- 기존 pack의 `.ddn` 39파일, `~~>` 95 occurrences를 변경하지 않았다.
- 기존 `<<-` `.ddn` 5파일, 7 occurrences를 변경하지 않았다.
- 새 successor evidence만 새 pack family에 추가했다.
- `docs/ssot/**`, `publish/spec/**`, 셈그림 UI, 공식 DB, deployment/activation diff는 0이다.

## 10. remaining batches

1. W1-B clean cut: old `~~>` reject/migration-only와 right rendezvous surface 분리.
2. W1-C: sender filter 및 `ReactionProvider` provider-key dedup/fan-out.
3. W1-D: preprocess/canon/currentline 포함 frontdoor-wide shared authority.
4. W1-E: logical WaitEdge, cancel/cleanup, staged cross-group outbox.
5. W1-F: 65-case oracle, worker 1/2/8, same-tag permutation, semantic digest.
6. W3: `<<-` coherent/glitch-free topological settle 및 cycle fail migration.
7. W7: zero-buffer rendezvous, ReadyReceive, HandoffEvent.

## 11. unresolved build/worktree blockers

- 격리 worktree의 lang/tool/teul-cli/WASM compile blocker는 없다.
- canonical root는 다른 세션 소유 dirty가 마지막 관찰 기준 1,078 rows이며 이 branch에서
  정리하거나 흡수하지 않았다.
- historical pack 3종의 frontdoor/expected-diagnostic drift 귀속은 독립 fixed-parent 비교가
  필요하다.
- `tools/teul-cli/src/canon.rs`, `tool/src/preprocess.rs`, `lang/src/currentline.rs`의 별도
  의미 소유 경로를 shared delivery authority로 수렴시키는 작업이 남았다.

## 12. protection boundary

- 원본 root HEAD/dirty는 비침범.
- `docs/ssot/**` 및 public SPEC diff 0.
- 보호 PID `53196` 시작 시각 유지.
- `127.0.0.1:8787` owner PID `53196` 유지.
- deployment, activation, external outreach: 0.
- 셈그림 UI 변경: 0.
