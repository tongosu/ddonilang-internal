# P0 WorkCost registry recovery and dual-name CLI handoff

## Fixed lineage

- Baseline: `01e538a3c3c7ab0a6aaba57ccfa0dfd6cc620eb2`
- Product recovery: `0871bb629561fae04d6df575d59fd3fdabab04fd`
- Product parity seal: `3e46eca7c5eb5a54dc250cb9186e4d5d1954d327`
- Merge count: `0`

## Product result

`stdlib_signature_ledger` remains a 256-row registry.  The expected SHA-256 is rebound from the stale generated candidate to `7e1bb12e2063b6ed3855d7ebccfc83d29ee70c168f46e981d95e18aec07d2794`, the hash emitted by the current `minimal_stdlib_sigs()` typed source.  This follows the TypeApp canonical type-presentation change and introduces no new semantic provider.

`ddonirang` and `또니랑` are two Cargo bin targets of the same `src/bin/ddonirang.rs` implementation.  The existing supported-ingress runner now compares both positive and legacy-negative payloads exactly; no argv0 semantic branch was added.

## Verification

- WorkCost exact-total test: PASS (256 rows).
- Supported V25 positive: both names exit `0`, stdout/stderr exact equal, state hash `blake3:d3623fcee76ad52f26063ecb2fd9fe2ef6f25a38292e07136f7d5db39365203c`.
- Legacy `=` negative: both names exit nonzero with exact equal payload and `E_V25_DEFINITION_MIGRATION_REQUIRED`.
- Native/WASM payload test: PASS.
- Mutations: stale WorkCost hash causes `E_WORK_COST_REGISTRY_MISSING_CANDIDATE` for `stdlib_signature_ledger`; exact restore GREEN. Removing the Korean bin target causes Cargo `no bin target named`; exact restore GREEN.
- Windows release targets exist for both names: 7,146,496 bytes each. Candidate artifact collection retained only `ddonirang.exe`; dual-artifact collection remains OPEN for the P5 projection slice.

## Bound and open

`WORK_COST_REGISTRY_SUPPORTED_V25_WORKFLOW=RESTORED` and `OFFICIAL_CLI_NAME_IDENTITY=IMPLEMENTED_PENDING_REVIEW` only. This does not close P0, teul physical retirement, V1 membership/readiness, P5, release, activation, legal or Human PASS.
