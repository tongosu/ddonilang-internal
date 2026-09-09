# V25 Physical Closure Evidence Index

## Program input

- packet path: `C:\Users\ddongosu\.codex\attachments\a83da0f0-60f3-4d7c-aed0-20d9d9648ece\pasted-text.txt`
- bytes: `24099`
- SHA-256: `7152c582a99f15bb8bb1bb78fa5f6be99fefa6da3babdd8e174ee22b6527cc01`

## PC-02 resume packet

- path: `C:\Users\ddongosu\.codex\attachments\9a91f5dc-527c-490e-930f-84a690ae79ec\pasted-text.txt`
- bytes: `13054`
- SHA-256: `23a72d81805f3aa0c83e307c67eacbd0cb26aa781f288be8a966254bf1726a92`
- Owner-declared custody: PC-01 `CLOSED / INDEPENDENT_PASS`; fixed target
  `3ac1cefbffa4c00857f99debad3b1aad24ed08ea`; handoff
  `9cb28ee8044dd0562d99f8d5fce5911dfd01c652`; T5F
  `INDEPENDENT_PASS / CLOSED`; PC-02 authorized.
- local review artifact status: no separate review commit/report was found in
  current refs or work artifact paths; Codex does not reconstruct the verdict.

## PC-00

- baseline: `7a83d5dd457b420570ecc0f1092fff7eab9bf946`
- baseline branch before fork: `codex/ddn-product-t5f-workbench-four-family-canonical-view-payload-r1-20260824`
- program branch: `codex/ddn-v25-physical-closure-long-range-r1-20260825`
- SSOT aggregate SHA-256: `16873c08442a8ac53eff5c343e1dbea9b494c1cc5f1f4be384c54384cd291d04`
- ancestry checks: all required T1/T2/T4/T5B~T5F commits returned exit `0`
- merge count from T1 to baseline: `0`
- start clean/staged: `true / 0`
- public v0.5 publication lineage: `6974eda4`, separate from T5F product lineage

## PC-01 authority rows

- RD-325: Definition `:=` and Binding/Rebinding `<-` are distinct semantic nodes and canonical surfaces.
- RD-333~335: v25 source epoch; pre-v25 is explicit migration input, not permanent alias.
- RD-307/RD-317: named definition and full declaration binder.
- public SPEC and SSOT remain read-only.

## PC-01 implementation evidence

- product implementation: `cf97f134aebc4889bd3e13ff4850cbf76ca4c2d6`
- test-format-only successor: `3ac1cefbffa4c00857f99debad3b1aad24ed08ea`
- executable pack: `pack/ddn_v25_pc01_definition_binding_v1/`
- product parser/canon pack test: `lang/tests/v25_definition_binding_pack.rs`
- mutation runner: `tests/ddn_v25_pc01_definition_binding_mutation_runner.mjs`
- language regression: 263 unit tests + 3 pack tests PASS
- explicit V25 runtime execution: 1 PASS, Definition `1` then Rebinding `2`, output `2`
- mutation: category collapse RED; old `=` alias RED; Definition canon `<-` RED; restored GREEN; residue 0
- `cargo check --workspace`: PASS with pre-existing dead-code warnings only
- `git diff --check`: PASS
- `docs/ssot/**`, `publish/spec/**`, tracked WASM diff: 0
- whole-workspace `cargo fmt --all -- --check`: not a PC-01 gate and remains RED on broad baseline formatting debt; no formatter write was applied to existing baseline files

## PC-02 shared frontdoor evidence

- activation baseline: `f03955c01963646c0095fcffb14f9f162c9655ce`
- product implementation: `04566a2426b56084f4449b363530192aa1166d2a`
- frontdoor inventory: `pc02_shared_frontdoor/FRONTDOOR_INVENTORY.md`
- implementation result: `pc02_shared_frontdoor/IMPLEMENTATION_RESULT.md`
- executable pack: `pack/ddn_v25_pc02_shared_frontdoor_v1/`
- Rust pack test: `tool/tests/v25_pc02_shared_frontdoor_pack.rs`
- multisurface runner: `tests/ddn_v25_pc02_shared_frontdoor_runner.mjs`
- mutation runner: `tests/ddn_v25_pc02_shared_frontdoor_mutation_runner.mjs`
- pack: 7/7 across tool, established official `run-summary`, teul, source-built WASM, and Workbench RuntimeBridge
- mutation: M1-M5 independently RED; exact restore GREEN; residue 0
- source-built WASM SHA-256: `db941a629d141b0e322aaa3ed4af36d09cdfba4c9ca4c6c68eae19d8f0adb1e4` (`12,913,811` bytes)
- tracked WASM SHA-256: `22df2f73b2f720871deb34dfe2e2763c5e1ea44cf1bae63bdf8a41a2c9468399` (`3,979,001` bytes)
- tracked manifest source tree: `2cc7b9682ca4a2554878046ab45312154366100b23830d28e5336509d94f6eea`
- current source tree: `68a370d2d8a933aa08d06c851267813f537a287edab0ddc5475cfd860c9e4dfc`; 79 files
- freshness: `TRACKED_WASM_STALE`; source-built bindings contain both `wasm_v25_assignment_frontdoor_json` and `DdnWasmVm.fromPreV25Source`; tracked bindings contain neither
- actual browser regression: local cached Chromium, temporary port `38931`, Workbench readiness `ready`; no network install; only unrelated favicon 404
- `docs/ssot/**`, `publish/spec/**`, tracked WASM diff: 0
