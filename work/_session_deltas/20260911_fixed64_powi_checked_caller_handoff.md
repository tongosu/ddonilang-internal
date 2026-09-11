# Fixed64 checked `powi` runtime caller handoff

- Product: `25f3bdec0931e6d1f6c917aadd7fb94057df5d11`
- Tree: `e7d7c3594aa910866b16cc34c52200e1f225715d`
- Parent: `4874c8fffbeffbaeb2b99ae44bba4b66924b89bc`
- Product path: `tool/src/ddn_runtime.rs`
- Fixed blob: `ee804db99c3c9eca046708d424a42fee92e908e7`
- Fixed SHA-256: `73f333cea4dc0187bb567a1969d17c7c13862a4f451b539724a0f265e8f10131`

## Claim

The active integer-power caller no longer reaches saturating `Fixed64` `Mul`.
It uses `checked_mul`, preserves the dimension calculation, and returns typed
overflow for an unrepresentable multiplication.  The `i64::MIN` exponent is
also rejected instead of overflowing during absolute-exponent conversion.

## Gates

- `cargo test -p ddonirang-tool --lib fixed64_powi_ -- --nocapture` — PASS
  (checked-owner and runtime failure-atomicity cases).
- Fixed64 minimum-absolute-value regression — PASS.
- Normal bisection residual regression — PASS.
- Native offline tool-library check — PASS.
- WASM offline tool-library check — PASS.
- `git diff --check` — PASS before product commit.

## Mutations

- M1 changed the checked multiplication to `result.value * base.value`.
  Both focused tests RED: overflow saturated to `Fixed64::MAX` and the runtime
  update succeeded.
- M2 downgraded checked-multiply overflow through `unwrap_or(Fixed64::MAX)`.
  The same focused owner and runtime-publication tests RED.

After each mutation the source was restored byte-exactly to blob `ee804db…`
and SHA-256 `73f333…`; focused tests GREENed.

## Review boundary

Ready for independent review: YES.  This target covers only the active
integer-power caller.  It does not settle public f64 ingress/snapshot ABI,
transcendental libm callers, every Fixed64 caller, release, or Human PASS.
