# V25 Physical Closure Implementation Ledger

| Slice | Baseline | Result commit | Status | Product scope | Review |
|---|---|---|---|---|---|
| PC-00 custody baseline | `7a83d5dd457b420570ecc0f1092fff7eab9bf946` | `55f57623ab419d9ccb99b9e0527efa912eaccee3` | PASS | none | not required |
| PC-01 Definition/Binding | `55f57623ab419d9ccb99b9e0527efa912eaccee3` | implementation `cf97f134aebc4889bd3e13ff4850cbf76ca4c2d6`; fixed target `3ac1cefbffa4c00857f99debad3b1aad24ed08ea`; handoff `9cb28ee8044dd0562d99f8d5fce5911dfd01c652` | CLOSED_INDEPENDENT_PASS | shared lang lexer/AST/parser/canon + explicit V25 runtime reader + executable pack | Owner-attested PASS in PC-02 resume packet |
| PC-02 shared frontdoor | `f03955c01963646c0095fcffb14f9f162c9655ce` | implementation `04566a2426b56084f4449b363530192aa1166d2a` | IMPLEMENTED_PENDING_INDEPENDENT_REVIEW | shared tool/native/WASM/official CLI/teul-cli plus Workbench RuntimeBridge query | plain PASS required |
| PC-05 ResultPlace | pending | pending | NOT_STARTED | shared typed/runtime path | required |
| PC-06 Selection | pending | pending | NOT_STARTED | shared typed/runtime path | required |
| PC-11A core oracle | pending | pending | NOT_STARTED | executable migration/oracle | required with parent slices |

## PC-00 findings

- T1 RuntimeBridge `0249aa0d`, T2 HostBridge `9742086f`, T4 `cee61315`, T4f `49f3b4db`, T4h `b789e1ac`, T5B `52650675`, T5C `0c037a2f`, T5D `e0c687eb`, T5E `15e54e82`, and T5F `0abec54b` are ancestors of the baseline.
- Merge commits from T1 product commit to baseline: `0`.
- Baseline worktree was clean with staged `0`.
- Shared root stayed at 201 tracked dirty files and was not modified, reset, stashed, or cleaned.
- T5F provenance is `INDEPENDENT_PASS / CLOSED` per the PC-02 Owner resume packet; its implementation remains an ancestor of this baseline.

## PC-01 implementation

- `TokenKind::Define` owns `:=`; `Stmt::Definition` is distinct from `Stmt::Mutate`.
- `CanonProgram::source_epoch` separates historical `PreV25` parsing from explicit `V25` parsing.
- `parse_v25*` rejects top-level pre-V25 `=` with `E_V25_DEFINITION_MIGRATION_REQUIRED`.
- A V25 `채비` name cannot be introduced with `<-`; it fails with `E_V25_DEFINITION_BINDING_CATEGORY`.
- Canon emits Definition as `:=` and Binding/Rebinding as `<-`; parse-canon-parse preserves category identity.
- `DdnProgram::from_v25_source` is an explicit product runtime reader used by the pack test. The default product frontdoor remains unchanged pending PC-02.
- Local Definition evaluates its value and inserts a new local identity without publishing a root resource; later Rebinding uses the existing mutation path.
- PC-01 is CLOSED / INDEPENDENT_PASS per Owner resume authority; PC-02 is active.

## PC-02 implementation

- V25 tool/runtime/canon entrypoints use `parse_v25_with_mode`, shared canonicalization, and the PC-01 typed `Stmt::Definition` / `Stmt::Mutate` categories.
- Official `ddonirang-tool run`, `run-summary`, and `canon`, plus teul `run` and `canon`, route V25 input through shared Rust authority by default.
- Historical Gate0/maze/eco flows and teul compatibility flows use named `pre-v25` readers or `--source-epoch pre-v25`; no parse-failure fallback exists.
- `DdnWasmVm` defaults to V25. `DdnWasmVm.fromPreV25Source` is the explicit migration entry used to preserve the T5F historical lesson regression without silent syntax conversion.
- Workbench consumes `wasm_v25_assignment_frontdoor_json` through RuntimeBridge; no JS Definition/Binding rewrite or diagnostic authority was added.
- The tracked WASM was not overwritten. Source-built WASM is current and the tracked artifact is classified `TRACKED_WASM_STALE`.
