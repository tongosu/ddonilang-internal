# DDN execution concurrency W1-B 구현 인계

## 상태와 고정점

```text
GOAL_ID: DDN_EXECUTION_CONCURRENCY_SURFACE_MIGRATION_W1B_SUCCESSOR_CANON_CLEAN_CUT_AND_HISTORICAL_BOUNDARY_W1
PREDECESSOR_PRODUCT_FIXED_HEAD: aaf72e08498031feeabfabc6692316e42dcfdc42
PREDECESSOR_HANDOFF_HEAD: 6e03e0cfcff64de8a578883cb8ccba15bdf17cee
PRODUCT_FIXED_HEAD: 7610e4bfda5c322e65cf6df9a5af45e58e0ab4bf
PRODUCT_FIXED_PARENT: 6e03e0cfcff64de8a578883cb8ccba15bdf17cee
DDN_EXECUTION_CONCURRENCY_W1B_SUCCESSOR_CANON_CLEAN_CUT_IMPLEMENTED_UNDER_REVIEW
W1B_PLAIN_PASS_NOT_YET_ISSUED
W1_FULL_CLOSURE_OPEN
W1C_NOT_STARTED
RENDEZVOUS_RUNTIME_OPEN
SSOT_CHANGED_0
PUBLIC_SPEC_CHANGED_0
UI_CHANGED_0
PUBLIC_ACTIVATION_NOT_AUTHORIZED
HUMAN_PASS_NOT_CLAIMED
```

`UI_CHANGED_0`은 UI source/behavior 변경이 없다는 뜻이다. 공통 Rust runtime을 쓰는
Workbench의 tracked WASM은 제품 경계 검증을 위해 동일 source-built web release로
갱신했다.

## G0~G1 — 시작점과 predecessor PASS 결속

- 공유 root `I:/dev/ddonilang/codex`: branch `codex/queue-20260706`, HEAD
  `a000e262cb96b51007286e2fb70bb2fa31e2af32`, dirty 1,096, staged 0. 수정·정리하지 않았다.
- 구현 worktree:
  `I:/home/urihanl/ddn/codex/build/worktrees/ddn-execution-concurrency-w1b-canon-clean-cut-20260822`
- 구현 branch: `codex/ddn-execution-concurrency-w1b-canon-clean-cut-20260822`
- 시작 HEAD `6e03e0c...`, clean/staged 0, merge commit 0.
- predecessor review report: 12,814 bytes,
  SHA-256 `b3c35ddd142f01abe7cd8d3856facde5f690ce2275c7219d07fb8cf7df914ce5`.
- report는 fixed HEAD `aaf72e...`, direct parent `de9cb9...`, `PASS`, 범위
  `W1_FIRST_SAFE_ASYNC_VERTICAL_ONLY`를 직접 명시한다.
- `aaf72e...`는 `de9cb9...`의 직접 후손, `6e03e0...`은 `aaf72e...`의 직접 후손이며
  두 구간 merge commit은 0이다. review/handoff의 제품 source diff는 0이다.

따라서 아래 predecessor 한정 상태만 결속한다.

```text
DDN_EXECUTION_CONCURRENCY_W1_FIRST_SAFE_ASYNC_VERTICAL_CLOSED
DDN_EXECUTION_CONCURRENCY_W1_FIRST_SAFE_ASYNC_VERTICAL_INDEPENDENT_PASS_BOUND
W1_FULL_CLOSURE_OPEN
```

## G2~G6 — semantic ownership map

| surface | parser mode | typed identity | canon/artifact | runtime disposition | diagnostic | corpus/status |
|---|---|---|---|---|---|---|
| `<~`, `~>` | `SuccessorDefault` | `MessageTransfer::Async` | `~>` | FIFO async queue, exact-one EndpointRoute | `E_ASYNC_ENDPOINT_UNHANDLED` / `E_ASYNC_ENDPOINT_AMBIGUOUS` | successor / `PRODUCT_PASS` |
| `<~~`, `~~>` | `SuccessorDefault` | `MessageTransfer::Rendezvous` | `~~>` | 실행 전 fail-closed | `E_RENDEZVOUS_PRODUCT_OPEN` | successor / parser·canon PASS, runtime `PRODUCT_UNSUPPORTED` |
| historical `~~>` | `HistoricalMigrationEvidence`만 | `MessageTransfer::HistoricalAsync` | `ddn.historical_async_migration_evidence.v1`; 일반 normalizer는 migration-required tag | 제품 실행 금지 | `E_HISTORICAL_ASYNC_MIGRATION_REQUIRED`; 실행 진입 시 `E_HISTORICAL_ASYNC_MIGRATION_EXECUTION_FORBIDDEN` | `HISTORICAL_MIGRATION_EVIDENCE`, not successor source |
| `<<-` | successor 별도 identity | `PersistentDependency` | 이번 W1-B 변경 없음 | coherent settle 전체 `PRODUCT-OPEN` | 기존 경계 유지 | historical inventory만 보존 |

소유권은 `lang` lexer/parser/typed `MessageTransfer`/normalizer가 가진다. `tool` native,
teul runtime, CLI, WASM은 이 identity를 소비한다. private legacy projection canon은 typed
transfer IR이 없으므로 `E_CANON_TYPED_TRANSFER_REQUIRES_SHARED_FRONTDOOR`로 닫고 공통
frontdoor를 우회하지 않는다. `currentline` mini-runtime도 `~>`만 async로 실행하며
`~~>`는 rendezvous product-open으로 거부한다.

`HistoricalAsyncSend` 필드는 비공개이고 명시적 migration constructor만 제공한다.
일반 `run`, 기본 `canon`, WASM VM은 파일명·pack 경로·handler 형태·실행 가능성을 보고
mode를 추측하지 않는다.

## successor canon / migration artifact

- `받는이 <~ 값.`과 `값 ~> 받는이.` → 둘 다 `값 ~> 받는이.`
- `받는이 <~~ 값.`과 `값 ~~> 받는이.` → 둘 다 `값 ~~> 받는이.`
- historical migration artifact 필드:
  `original_surface`, `historical_identity`, `successor_replacement`,
  `diagnostic_code`, UTF-8 byte `source_span`.
- historical normalizer output은
  `~[historical-async-migration-required]>` tag를 사용하므로 rendezvous canon과
  byte-identical 의미로 위장되지 않는다.

## 제품 frontdoor와 tracked Workbench WASM

- native tool/teul CLI: 기본 `~~>`는 rendezvous이며 old handler async dispatch 0.
- CLI migration 진입점:
  `teul-cli historical-async-migration-evidence <file>`.
- WASM migration 진입점:
  `wasm_historical_async_migration_evidence_json(source, source_path)`.
- WASM VM mode는 `strict|successor-default`만 허용한다. migration mode 실행 진입은 거부한다.
- tracked Workbench web WASM:
  - bytes: `5,439,334`
  - SHA-256: `8be23053b6a6fbf74d2d1337f685dd8b2381f7b36932535fd0b69d7206db337d`
  - clean-detached source-built web release와 raw byte-identical.
- freshness manifest checker: PASS.

## historical corpus custody

successor pack `future_grammar_atlas_owner_closed_delta_r2`를 제외한 `pack/**/*.ddn` 전수 집계:

| historical surface | files | occurrences | source diff from `6e03e0...` |
|---|---:|---:|---:|
| old `~~>` | 39 | 95 | 0 |
| old `<<-` | 5 | 7 | 0 |

기존 regression도 predecessor와 동일하다.

- `lang_consistency_v1`: failure_count 18.
- `patent_c_single_funnel_nonreentry_queue_v1`: failure_count 1.
- `lang_flow_hook_interaction_v1`: 전용 checker의 첫 c01 failure 유지.

이를 successor 제품 PASS로 재표시하거나 원문을 고치지 않았다.

## successor D-PACK

`pack/future_grammar_atlas_owner_closed_delta_r2`는 4건에서 13건으로 확장했다.
`golden.jsonl`과 `logical_oracle.jsonl`은 각각 13행이며
`PRODUCT_PASS`, `MIGRATION_PASS`, `PRODUCT_UNSUPPORTED`를 분리한다.

```text
python tests/run_pack_golden.py future_grammar_atlas_owner_closed_delta_r2
PASS (13/13)
```

## negative / fault injection

모든 mutation은 같은 worktree에서 적용하고 해당 검사가 RED임을 확인한 뒤 patch로
원복해 GREEN을 재확인했다.

| mutation | RED detector | restore result |
|---|---|---|
| default `~~>` → `HistoricalAsync` | `successor_default_owns_double_arrow_as_rendezvous` assertion RED | GREEN |
| rendezvous runtime → async queue dispatch | `double_arrow_is_rendezvous_and_never_dispatches_legacy_async_handler` RED | GREEN |
| migration `source_span` → null | `migration_evidence_is_explicit_tagged_and_non_executable` RED | GREEN |
| WASM migration path identity에 `wasm:` 주입 | native/WASM exact artifact assertion RED | GREEN |

추가 정적/동적 negative는 방향 pair identity, path/handler inference 금지, CLI runtime
migration 진입 금지, historical tag 분리, VM mode 거부, failure state/hash 보존을 검사한다.

## 전체 검증

| 검증 | 결과 |
|---|---|
| `cargo test -p ddonirang-lang` | PASS, 347/347 (predecessor 342, W1-B +5) |
| `cargo test -p ddonirang-tool --lib` | PASS, 485/485 (predecessor 484, W1-B +1) |
| `cargo test --manifest-path tools/teul-cli/Cargo.toml` | PASS, 1,161/1,161 (predecessor 1,159, W1-B +2) |
| `cargo check -p ddonirang-tool --target wasm32-unknown-unknown --lib` | PASS |
| source-built node WASM + native parity runner | PASS |
| tracked Workbench web WASM parity | PASS |
| freshness manifest negative selftests | PASS |
| `git diff --check` | PASS |

clean-detached fixed HEAD `7610e4bf...`에서 별도 CLI와 node WASM을 빌드해 13-case pack과
parity runner를 다시 통과했다. 별도 web release는 tracked artifact와 같은
5,439,334 bytes / SHA-256 `8be23053...337d`였다. node debug WASM은 build path가 달라
raw bytes가 달랐으므로 release identity 근거로 사용하지 않는다.

## 보호 경계

- 공식 DB SHA-256 전/후:
  `3fbf028e852dd3a13c3b84f812254de30c55113140f2b7869ff81a2a3b2b65f0`.
- PID `53196`: `python`, 시작 `2026-08-08 12:27:21 +09:00`, 유지.
- `127.0.0.1:8787`: PID `53196` LISTEN 유지.
- official store writes: 0.
- activation endpoint calls: 0.
- task-owned residual process/socket/temp DB: 0.
- `docs/ssot/**`, `publish/spec/**`, historical packs diff: 0.
- UI source/behavior 변경: 0. tracked common-Rust WASM artifact만 currentize.

## PASS / PRODUCT-OPEN matrix

```text
[x] predecessor PASS bound (first safe async vertical only)
[x] default parser: `~~>` is never HistoricalAsync
[x] `<~ / ~>` async identity preserved
[x] `<~~ / ~~>` rendezvous identity preserved
[x] historical migration mode explicit
[x] migration canon distinct from successor canon
[x] default product async delivery through `~~>` = 0
[x] native/source-WASM/tracked-Workbench parity
[x] historical corpus source diff 0
[x] successor D-PACK expanded to 13
[x] negative fault injection RED→restore→GREEN
[x] full Rust regression
[x] protected resources invariant
[ ] independent W1-B plain PASS — PENDING
[ ] rendezvous runtime — PRODUCT-OPEN
[ ] W1 full closure — OPEN
[ ] W1C sender filter / ReactionProvider surface — NOT STARTED
```

Codex는 독립 판정을 발행하지 않는다.
