# W1-C2 I1 product ownership and migration map

- `lang/src/delivery.rs`: EndpointRoute cardinality, internal descriptor/registry/identity, occurrence dedup, logical WAIT/FIFO authority.
- `tool/src/ddn_runtime.rs`: explicit internal typed registry input, settled-snapshot candidate evaluation, deterministic merge, atomic publish, staged outbox and EffectIntent release.
- `tools/teul-cli/src/runtime/eval.rs`: shared lang delivery authority와 explicit empty provider registry. legacy all-handler fallback 0.
- public source runtime: empty provider registry, `PUBLIC_PROVIDER_SOURCE_INGRESS_0`.
- `currentline`/historical receive hook: compatibility/migration evidence only; automatic provider alias 0.
- Workbench transport/UI: 변경 0. tracked WASM만 공통 Rust freshness 절차로 갱신.

G2에서 fixed baseline과 shared dirty root를 읽기 전용 대조했다. shared root의 target dirty hunk는 atomic receipt/formatting 등 별도 작업이었고 provider/delivery 구현 hunk와 겹치지 않았다. 공유 root reset/stash/clean/write는 0이다.

`반응제공자`, `반응하면`, parser production, `Stmt::Receive` provider flag, preprocess lowering, CLI config ingress, WASM public schema는 모두 0이다.
