# BC-FFI-05B external boundary — fixed-target handoff

## Fixed target

- Product fixed commit: `e5474dcb49dcf3afe8e8d8a4ea3e731fff2a75b0`
- Parent: `4490efda9cdd13a221ccde6a9fdfdd8c81fe94b2`
- Tree: `0cfc3987e9371c7bd0793bb245592a4f43fc7623`
- Lineage: direct child; merge count `0`.
- Authority read-only basis: internal SSOT `v25.58.0 / RD-001~562`; public Language SPEC `v0.6.0`.

## Implemented product boundary

`ExternalDependencyNode` accepts only the already-resolved typed node kinds
`DDN_GAJI` and `EXTERNAL_ARTIFACT`.  One internal external-boundary identity is
sealed with artifact, provenance, provider, callable, invocation, execution
contract, capability, input/output digests, and ordinal.

Dispatch requires an exact process-local capability scope and exact provider
identity before calling the provider.  Failed authorization, bounds checks,
provider failure, or receipt mismatch do not advance the ordinal or publish a
receipt.  Replay accepts only the sealed input, output, dependency, and receipt;
it has no provider parameter and therefore cannot perform a provider call.

Native and WASM internal structured adapters delegate to the same
`runtime_surface::execute_sealed_external_boundary` owner.  No new bindgen
export, CLI option, command, public wire/schema, lock-file schema, source
syntax, Workbench UI behavior, or ambient provider selection was added.
Workbench status is `EXPLICIT_NOT_PUBLICLY_PROJECTED`: its public request and
display mapping remain outside this fixed target.

## Product paths

1. `core/src/capability.rs`
2. `core/src/external_boundary.rs`
3. `core/src/lib.rs`
4. `core/src/tests/external_boundary.rs`
5. `core/src/tests/mod.rs`
6. `tool/src/runtime_surface.rs`
7. `tool/src/wasm_api.rs`

Protected paths, `docs/ssot/**`, `publish/spec/**`, LSP, teul-cli, tracked WASM,
and visible Workbench files have diff `0`.

## Verification

- `cargo test -p ddonirang-core external_boundary -- --nocapture`: `4/4 PASS`.
- `cargo test -p ddonirang-core atomic_commit_vertical_slice -- --nocapture`: `46/46 PASS`.
- `cargo test -p ddonirang-tool --features wasm external_boundary_native_and_wasm_adapters_share_one_typed_owner -- --nocapture`: `1/1 PASS`.
- `cargo check -p ddonirang-tool --features wasm`: `PASS`.
- `git diff --check`: `PASS`.

The tool build emitted existing warnings (including the pre-existing three-bin
source-path warning and dead-code warnings); no new compilation error occurred.

## Risk mutations

All mutations were applied to product source, observed RED, restored exactly,
and rerun GREEN with residue `0`.

| ID | Temporary defect | RED gate | Restore identity | GREEN gate |
| --- | --- | --- | --- | --- |
| M1 | Capability-denial bypass | rejection test fails with a published result | `core/src/external_boundary.rs` SHA-256 `3351CC49AEECD99623A84D2EE79175998DCEBF01B975B9A60A67B4D5F523AAF0` | rejection test PASS |
| M2 | Provider failure publishes a partial receipt | provider-failure test detects publication | same SHA-256 | provider-failure test PASS |
| M3 | WASM adapter does not reach shared owner | native/WASM adapter parity test fails | `tool/src/wasm_api.rs` SHA-256 `C0BFA0FCFF71BDBB635FC6CFAEFCDF678D2888A6696371C562085E179829D36C` | adapter parity PASS |
| M4 | Tampered replay is accepted | receipt-tamper test fails | `core/src/external_boundary.rs` SHA-256 `3351CC49AEECD99623A84D2EE79175998DCEBF01B975B9A60A67B4D5F523AAF0` | tamper test PASS |

## Review disposition

`PRODUCT_IMPLEMENTED_PENDING_REVIEW`.  This is one coherent fixed target for
the existing rolling reviewer; no review task, worktree, branch, or reviewer was
created by this implementation.

## Nonclaims

This handoff does not claim external-provider integration, a public external
boundary contract, PathIR/Proof closure, P0-P6 closure, V1 readiness, release,
publication, activation, legal clearance, or Human PASS.
