# future_grammar_atlas_owner_closed_delta_r2

Owner-closed execution/concurrency semantics의 successor 제품 이행 D-PACK이다.

이 W1-B는 첫 async 수직을 보존하면서 successor canon과 historical migration
evidence를 typed parser mode 수준에서 분리한다.

- `c01`: `<~` exact-one EndpointRoute
- `c02`: `~>` zero route deterministic failure
- `c03`: `~>` multiple route ambiguity failure
- `c04`: nested async FIFO tail / no direct reentry
- `c05`: `~>` exact-one EndpointRoute
- `c06`~`c07`: `<~~`/`~~>` rendezvous canon과 runtime product-open
- `c08`, `c10`: 명시적 `HistoricalMigrationEvidence` artifact와 UTF-8 byte span
- `c09`: default `~~>` legacy async enqueue 0
- `c11`~`c12`: async/rendezvous canon roundtrip identity
- `c13`: 같은 raw source의 native/WASM rendezvous runtime fail-closed parity

`logical_oracle.jsonl`은 `PRODUCT_PASS`, `MIGRATION_PASS`, `PRODUCT_UNSUPPORTED`를
구분한다. 전체 65-case logical oracle,
sender filter, ReactionProvider fan-out, worker 1/2/8 permutation, rendezvous, persistent
dependency, cross-group outbox는 `PRODUCT_UNSUPPORTED` 또는 `PRODUCT-OPEN`으로 남긴다.

기존 `~~>` corpus는 변경하지 않으며 `HISTORICAL_MIGRATION_EVIDENCE`로 보존한다.
일반 `run`/`canon`/WASM 실행은 migration mode를 자동 활성화하지 않는다.

실행:

```text
python tests/run_pack_golden.py future_grammar_atlas_owner_closed_delta_r2
```
