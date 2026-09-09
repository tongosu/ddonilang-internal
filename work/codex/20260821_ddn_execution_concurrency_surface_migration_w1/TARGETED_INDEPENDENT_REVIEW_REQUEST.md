# Targeted independent review request

## Review identity

```text
goal: DDN_EXECUTION_CONCURRENCY_SURFACE_MIGRATION_W1_FIRST_SAFE_ASYNC_VERTICAL
product_fixed_head: aaf72e08498031feeabfabc6692316e42dcfdc42
fixed_parent: de9cb9ed95f71910bedd2b1bce0769a8257a7f27
branch: codex/ddn-execution-concurrency-surface-migration-w1-20260821
```

이 요청은 W1 전체 PASS 요청이 아니다. 첫 successor async vertical의 typed identity,
parser/canon, runtime cardinality, FIFO/no-reentry, bounded-WAIT hook, successor D-PACK만
독립 재검토한다.

## Required independent checks

1. fixed parent/HEAD, merge count, exact changed paths를 검증한다.
2. `docs/ssot/**`, `publish/spec/**`, UI diff가 0인지 확인한다.
3. `<~`와 `~>`가 동일 `AsyncSend` identity/canon으로 수렴하는지 확인한다.
4. `<~~`/rendezvous와 old `~~>` historical identity가 async와 섞이지 않는지 확인한다.
5. successor async route가 0/1/>1에서 각각 unhandled/one delivery/ambiguity인지 실제 실행한다.
6. 두 matching route에서 declaration-order first를 고르지 않는지 확인한다.
7. nested async가 current handler stack에 재진입하지 않고 FIFO tail에서 실행되는지 확인한다.
8. queue full이 envelope를 silent drop하지 않고 WAIT-required 경계로 가는지 fault-inject 한다.
9. tool runtime과 teul adapter가 공통 `ddonirang_lang` queue/cardinality authority를 쓰는지 추적한다.
10. 새 D-PACK `4/4`를 깨끗한 isolated target에서 실행한다.
11. historical `~~>`/`<<-` pack 파일이 변경되지 않았는지 확인한다.
12. 역사 corpus의 현재 실패는 fixed parent에서도 별도 재현해 regression 귀속을 판정한다.

## Expected commands

```text
cargo test -p ddonirang-lang
cargo test -p ddonirang-tool --lib
cargo test --manifest-path tools/teul-cli/Cargo.toml
cargo check -p ddonirang-tool --target wasm32-unknown-unknown --lib
python tests/run_pack_golden.py future_grammar_atlas_owner_closed_delta_r2
python tests/run_alrim_dispatch_runtime_contract_selftest.py
```

## Verdict boundary

plain `PASS`는 위 첫 vertical에만 가능하다. 다음은 발견사항이 없어도 OPEN으로 유지한다.

```text
W1_FULL_CLOSURE
OLD_DOUBLE_TILDE_SUCCESSOR_CLEAN_CUT
REACTION_PROVIDER_FANOUT
ASYNC_SENDER_FILTER
WORKER_1_2_8_PERMUTATION
CROSS_GROUP_STAGED_OUTBOX
RESUMABLE_WAIT_EDGE
RENDEZVOUS_HANDOFF_EVENT
PERSISTENT_DEPENDENCY_SETTLE
FULL_65_CASE_ORACLE
PUBLIC_ACTIVATION
```
