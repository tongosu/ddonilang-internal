# CLI/teul retained adapter shared JSON·preprocess convergence W2 handoff

## Fixed product identity

- Parent handoff: `713d60125ac891d15a08781a5dda0306b1fc6c3e`
- Product fixed: `dde7bb85b6a6f0099ff9f18126dcf9d7a785ff58`
- Fixed tree: `85083cb09acf9a2496540da68df681cf3d831c65`
- Merge count: `0`

## User-facing workflow and change

The retained `teul-cli` canonical diagnostic/fixit path now consumes the same
frontdoor preprocessing entry point as the shared language/tool frontdoor.
Its run-path JSON construction, parsing, and structured diagnostics now use
the existing `ddonirang_tool::serde_json` re-export as one crate boundary.
No command spelling, executable/package name, legacy alias, public command
membership, wire field, diagnostic spelling, or dependency was added.

Before this correction, a full `teul-cli` bin-test compilation after the prior
adapter convergence exposed incompatible `serde_json::Value` identities between
the retained nested CLI lock context and the tool re-export boundary. The
actual product RED had 69 type errors. This fixed product commit makes the
entire `run.rs` JSON namespace resolve through the existing shared tool
re-export; the original raw-DDN canonical/fixit preprocessing path is likewise
routed through `prepare_frontdoor_runtime_source`.

## Changed product paths

1. `tools/teul-cli/src/cli/run.rs`
2. `tools/teul-cli/src/cli/canon.rs`

Product code outside the two paths, tracked WASM, UI, SSOT, public SPEC,
package metadata, and lockfiles have no fixed-commit diff.

## Reused product evidence

All evidence uses existing tests and the existing executable:

- `supported_profile_run_uses_shared_v25_authority_and_fails_legacy_closed`: PASS
- `snapshot_adapter_consumes_shared_keyboard_and_network_projection`: PASS
- `supported_profile_canon_uses_shared_authority_and_atomic_output`: PASS
- `ddn_error_sidecar_failure_publishes_no_partial_artifact`: PASS
- `project_run_binds_neutral_identity_inputs_and_rejects_virtual_conflicts`: PASS
- offline `cargo build --manifest-path tools/teul-cli/Cargo.toml`: PASS
- built `teul-cli.exe --help`: exit `0`

New pack/runner/test artifact: `0`. Meta-test: `0`. No synthetic mutation was
added: the actual compile-time retained-adapter boundary RED was repaired, then
the existing workflow and failure-atomicity tests returned GREEN.

## Scope status

- Shared retained JSON/preprocess adapter convergence: `IMPLEMENTED_UNDER_REVIEW`
- V1 required build/test/pack/publish `teul-cli` execution dependency: no new
  required dependency introduced by this slice; global retirement remains open.
- `tools/teul-cli` physical deletion, public binary/package retirement,
  executable naming, public command membership, and legacy alias policy: OPEN
- Independent review dispatch: `0` by this writer; this handoff is available
  for the existing rolling reviewer only when management bundles a coherent
  milestone.

## Nonclaims

This handoff does not close P0--P6, P1, V1 readiness, release, activation,
legal/rights attribution, public distribution, or Owner Human Smoke/Human PASS.
