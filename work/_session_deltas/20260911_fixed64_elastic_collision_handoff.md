# Fixed64 elastic-collision checked arithmetic handoff

## Target

- Product commit: `9832faa6a10b67b19e2cef60ba3f2bbfc47a0a89`
- Tree: `37c8548dbdf14ea0a2413af93fc82eb268de9de6`
- Parent: `ccea7fadbaa88c3f8c24048ffe04f910b9cae0b2`
- Product path: `tool/src/ddn_runtime.rs`

## Scope

The active `물리1d.탄성충돌1d` runtime builtin no longer uses saturating
Fixed64 arithmetic.  Its denominator and both numerator paths use checked
add/subtract/multiply/divide and propagate the existing typed arithmetic fault.

The focused workflow verifies a normal equal-mass collision (`[0, 2]`) and
rejects an intermediate-overflow collision before a run output is published,
with `E_RUNTIME_ARITH_OVERFLOW`.

## Evidence

- `cargo test -p ddonirang-tool --lib physics_ -- --nocapture` — PASS
- `cargo check -p ddonirang-tool --lib --target wasm32-unknown-unknown --features wasm --offline` — PASS
- `git diff --check` — PASS before commit

Mutation M1: replacing the checked `two * m1` intermediate with
`saturating_mul` made the overflow workflow RED by producing a successful update
instead of the required rejection.  The fixed source was restored exactly:

- SHA-256: `dc63e2323551c1f1b0a00d017ac59c64b3b0b8f2812e9d14900851af8c05094b`
- Git blob: `6e692cdd11926a90a1ebe3243a88ec5962ecc40c`

## Nonclaims

This is an active-caller slice only. It does not establish all Fixed64 runtime
callers, full Native/WASM behavioral parity, tracked WASM freshness, release
readiness, or an independent PASS.
