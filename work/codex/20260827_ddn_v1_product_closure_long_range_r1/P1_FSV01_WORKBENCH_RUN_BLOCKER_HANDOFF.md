# P1 FSV01 tracked Workbench single-file run handoff

## Fixed lineage

- Base: `f5cd664fbbf6438345f74d034e499fe6bed753b1`
- Shared-WASM source-profile fixed: `48815d6d322637b271e652712120332548caa650`
- Product fixed: `baa7b0a4caf6c9cf790c2546ca46ee9ab6581435`
- Product fixed tree: `654777b5aa9e22c9232eb3c480d64f8d6286b5a2`
- This handoff is a direct, docs-only successor of the product fixed commit.

## Product change

The tracked Workbench now invokes the existing typed WASM shared-run summary with
the explicit `v1-core-v25` source-profile identity before publishing a completed
frame.  It consumes the existing structured summary and WorkCost receipt, checks
the shared state hash and profile identity, and fails with
`E_WORKBENCH_RUN_RECEIPT_BINDING_REQUIRED` if that binding is incomplete.

No parser, canonicalizer, test-only lowering, PreV25 retry, teul invocation, or
new public registry/wire field was added.  The nine-path preceding fixed commit
binds Workbench source readiness to the same typed V25 path; the product fixed
commit changes only `runtime_bridge.js` and `workbench.js`.

## Executed product evidence

- Actual tracked Workbench browser: pasted the current V25 single-file fixture,
  pressed Run, and observed `runs=1`, `status=done`, source profile
  `v1-core-v25`, state hash
  `blake3:d3623fcee76ad52f26063ecb2fd9fe2ef6f25a38292e07136f7d5db39365203c`,
  output `2`, and receipt schema `ddonirang.work_cost.v1-candidate`.
- Repeating that browser workflow produced byte-identical state/result/receipt
  projections.
- In a fresh tracked Workbench page, legacy `=` source was rejected before run:
  `E_V25_DEFINITION_MIGRATION_REQUIRED`, run records `0`, WASM VM entries `0`,
  success payload `0`, and frame/result publication `0`.
- `ddonilang`, `또니랑`, and compatibility alias `ddonirang` produced equal V25
  profile/state/receipt/output projections and equal legacy migration diagnostics.
- Existing `node tests/seamgrim_workbench_source_analysis_t4_runner.mjs` passed;
  existing `node tests/seamgrim_wasm_vm_runtime_runner.mjs` passed.
- Clean existing ingress reproduction passed: native `8`, native/WASM exact `2`,
  WASM `11`, deterministic repeats `5`, official dual-name parity `2`, and
  compatibility-alias parity `2`.  Log:
  `build/fsv01_w2_final/supported_ingress_final.log`, SHA-256
  `D362677ECC5202CF4417B6200C305E47DD03C9CD86EAB897B65750A741B38EE9`.

## Fault evidence

Each temporary mutation was restored byte-exactly before the final green run;
none is committed.

| Mutation | Actual RED | Restored GREEN |
|---|---|---|
| M1 shared V25 readiness binding removed | browser blocks before WASM/run | actual tracked V25 run completes |
| M2 current-source guard removed | existing source-analysis runner rejects the missing guard | runner passes after restore |
| M3 legacy rejection bypassed | browser creates a failed legacy run instead of preflight block | fresh legacy page has no run/frame/result |
| M4 receipt assignment removed | browser result has no receipt | receipt is present and bound |
| M5 environment-selected teul fallback inserted | browser V25 run fails through the legacy path | shared V25 path succeeds without fallback |

## Status and limits

`P1_FSV01_PRODUCT_IMPLEMENTED=YES`

`P1_FSV01_CLOSURE_CANDIDATE_READY=YES`

`READY_FOR_INDEPENDENT_REVIEW=YES`

This is a fixed-target product handoff only.  It does not claim independent PASS,
whole P1/P0--P6 closure, V1 membership/readiness/release/activation/legal status,
or Owner Human Smoke/Human PASS.
