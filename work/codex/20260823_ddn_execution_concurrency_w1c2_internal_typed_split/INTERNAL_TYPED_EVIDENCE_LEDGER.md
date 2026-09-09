# W1-C2 I1 internal typed evidence ledger

단일 oracle: `pack/ddn_execution_concurrency_w1c2_internal_typed/expected.jsonl`.

- 전체 23: GREEN
- `INTERNAL_TYPED_PRODUCT_CASE`: 20
- `PUBLIC_SOURCE_REGRESSION_CASE`: 2
- `PRODUCT_UNSUPPORTED`: 1
- compiled test identity: 23/23 exact
- public provider product token: 0
- public provider source ingress: 0
- teul legacy provider fallback: 0

사례는 route 0/2 provider 미진입, route 1 provider 0/1/2, diamond dedup, duplicate definition, identity 축, settled snapshot, permutation, conflict/body failure atomicity, staged/no-reentry/WAIT/FIFO outbox, abort discard, commit 뒤 effect release와 release failure non-rewind, historical/receive/teul 비승격을 포함한다.

명령: `DDN_W1C2_CARGO_TARGET_DIR=<isolated> node tests/ddn_execution_concurrency_w1c2_internal_typed_runner.mjs`.
