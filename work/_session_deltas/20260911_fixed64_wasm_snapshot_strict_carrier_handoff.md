# Fixed64 WASM snapshot strict-carrier handoff

## Fixed target

- Product commit: `301e0e9e60e448e6773524fc218a9449806565a5`
- Product tree: `9d19595888759d26065b11bf87a0334702999087`
- Parent: `db7cac203b8a1f32c2b30c519e9e39eedb1eedbb`
- Product path: `tool/src/wasm_api.rs`

## Product boundary

WASM `snapshot_v2.param_overrides` no longer serializes or restores Fixed64
through a binary JSON number / `f64` conversion.  It reuses the existing
shared `{ "raw_i64": "…" }` Fixed64 carrier consumed by `json_to_fixed64`.
JSON number input is rejected with `E_WASM_STATE_PARAMS_INVALID` before the
staged restore can publish state.  Boolean and string parameters retain their
existing distinct representations.

## Focused evidence

- `snapshot_param_overrides_use_the_shared_fixed64_raw_carrier`: PASS
- `wasm_state_snapshot_v2`: 2/2 PASS
- WASM-feature offline library check: PASS
- `git diff --check`: PASS

## Mutation evidence

- M1: restoring the previous numeric serializer produced RED: the exact raw
  carrier assertion observed `Number(4.656612873077393e-10)` instead of
  `{ "raw_i64": "2" }`.
- M2: rejecting the raw-object carrier produced RED: snapshot restore failed
  before the expected typed Fixed64 value could be restored.
- Both mutations were restored byte-exactly, then the focused tests were
  GREEN.
- Restored file SHA-256:
  `2babbbd5ea5f10b1d61af63a9adcf60efb4fa99fc18b50b0a33a3443623cd900`
- Restored Git blob: `c396fcb2abd7782513e47e8cf72db1eeedf53bd9`

## Review request

Review the immutable product target for strict shared-carrier use, rejection
of binary JSON-number authority, snapshot restore atomicity, and WASM-feature
regressions.

## Nonclaims

This target does not change the public `set_input`/`set_dt_f64` ABI, provide a
new wire field, certify all remaining float-origin ingress, release, SSOT, or
Human PASS.
