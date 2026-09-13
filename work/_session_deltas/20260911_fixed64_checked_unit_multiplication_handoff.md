# Fixed64 checked active unit-multiplication handoff

- Product: `1a343aeb382498ec16aabf018175d063286b3b7d`
- Tree: `f09d9587d35859e17710969fde43bb30b508f2f3`
- Parent: `776b92dae2505cda4f959f8fd05430d1d19d683d`
- Product path: `tool/src/ddn_runtime.rs`
- Fixed blob: `7a80b902d43221ad5566a24d1b4ffd104309ccca`
- Fixed SHA-256: `a783bd2c1f6fa3174727347f92f34fa4271ed94aa86c9fae1278b479c6930e6b`

## Claim

Active generic multiplication now uses one checked helper in the runtime
infix `*` path, formula binary multiplication, Euler integration,
semi-implicit Euler integration, and linear interpolation.  The helper keeps
dimension composition while emitting typed Fixed64 overflow before a result is
published.

## Gates

- Actual `값 * 값` runtime overflow rejects before publication — PASS.
- Formula-power checked overflow — PASS.
- Existing runtime `powi` overflow suite — PASS.
- Native and WASM offline tool-library checks — PASS.
- `git diff --check` — PASS before product commit.

## Mutations

- M1 restored saturated `left.value * right.value`; actual infix runtime
  overflow test RED because the update succeeded.
- M2 downgraded `checked_mul` failure through `unwrap_or(Fixed64::MAX)`; the
  same runtime publication test RED.

Both mutations were removed and the source restored exactly to blob
`7a80b902…` / SHA-256 `a783bd2c…`; focused gates GREENed.

## Review boundary

Ready for independent review: YES.  This target does not close compile-time
formula simplification, public f64 ingress/snapshot ABI, transcendentals,
every Fixed64 caller, release, or Human PASS.
