# Fixed64 exact text-ingress handoff

## Immutable product target

- Claim: current textual numeric ingress rejects Q31.32 overflow rather than
  silently converting it to `Fixed64::MAX` or `Fixed64::MIN`; fractional
  decimal admission uses integer-only nearest ties-to-even rounding.
- Product: `14b3c7d5e2d9c8d6b0552ae835a99fb598eb62cf`
- Tree: `483e3b3bc9451288759937b3b546b931f7226987`
- Parent: `7476672b1f4f00270cb66b9682e6f3b0bdd08809`
- Product paths:
  - `core/src/fixed64.rs`
  - `lang/src/runtime.rs`

## Product workflow and evidence

- User workflow: current runtime string-to-number admission receives a textual
  numeric value, preserves representable Q31.32 input, and returns no numeric
  value for an out-of-range literal before a saturated value can enter state.
- Focused language runtime test: PASS.
- Core Fixed64 focused suite: PASS (`16` tests).
- Regressions: `cargo test -p ddonirang-core --offline` (`129` tests) and
  `cargo test -p ddonirang-lang --offline` (`374` unit tests plus 22 existing
  integration tests): PASS.
- Build: `cargo check -p ddonirang-core --offline`: PASS.
- All commands used the isolated
  `I:/home/urihanl/ddn/codex/build/target-v1-next-blockers` target.
- `git diff --check`: PASS before fixed commit.

## Mutations and exact restore

- M-B1 restored the prior saturating public decimal admission. The overflow
  assertion became RED (`Some(Fixed64 { raw: 9223372036854775807 })`, expected
  `None`).
- M-B2 disabled the residual-bit rounding decision. The `-0.8` current text
  assertion became RED (`-3435973836`, expected `-3435973837`).
- Both restores returned `core/src/fixed64.rs` to SHA-256
  `1DC20833146C52E8072736D00BD17DF50D6F319E1869B4E0E6CACCDF7B6F1FFA`,
  Git blob `9c4938df645ffdcc370a2f404558986716fbb93d`, and focused GREEN.

## Review packet

- Primary gate: `runtime::tests::runtime_string_to_number_keeps_q32_32_raw_value`.
- Failure behavior: oversized textual input yields `Value::None`, so no
  saturated numeric value is returned by that current ingress route.
- Status: `PRODUCT_FIXED_PENDING_REVIEW`.
- Nonclaims: this does not migrate every legacy `saturating_*` caller, prove
  float-boundary parity, refresh tracked WASM, or close Fixed64/V1/release/Human
  readiness.
