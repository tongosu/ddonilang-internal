# Fixed64 Native/WASM carrier boundary handoff

## Fixed target

- Product commit: `7ebae5b1d5a2925629e5f98bf97fda700d4ccd51`
- Tree: `6354db6f52462ddc85db26c6c92dce63e7766e3d`
- Parent: `6684284ffec4adcdc2dc68b741b1a1c622c9fd16`
- Product paths:
  - `tool/src/fixed64_boundary.rs`
  - `tool/src/unit_wire.rs`
  - `tool/src/wasm_api.rs`
  - `tool/src/ddn_runtime.rs`

## Product behavior

Native unit-wire and WASM state carriers now reject generic JSON number values
before Fixed64 admission. They continue to accept the existing textual decimal
and `raw_i64` representations, using `Fixed64::parse_decimal` for the former.
This prevents a JSON parser's binary floating-point representation from
becoming a Fixed64 authority at either carrier boundary.

The runtime arithmetic-fault projection now gives `Overflow` a stable
`ddn:overflow` location rather than leaving the checked signal variant
unhandled at tool compile time.

## Evidence

- `cargo test -p ddonirang-tool --lib --features wasm fixed64_boundary::tests::native_and_wasm_carriers_share_the_strict_fixed64_boundary -- --nocapture` — PASS
- `cargo check -p ddonirang-tool --lib --target wasm32-unknown-unknown --features wasm --offline` — PASS
- `git diff --check` — PASS

Mutation evidence, all restored byte-exactly before the product commit:

1. Native unit-wire JSON-number `f64` conversion restored — focused assertion RED.
2. WASM carrier JSON-number `f64` conversion restored — shared Native/WASM assertion RED.
3. Exact decimal ties-to-even changed to truncation — `1.5 ULP` assertion RED.
4. JSON-number rejection changed to saturation — focused assertion RED.

## Nonclaims and next action

This commit does not claim the full Fixed64 Native/WASM boundary-convergence
blocker closed. Existing `f64` convenience APIs outside these two typed carrier
owners and active runtime callers still require the next bounded audit and
checked-migration work. No tracked WASM artifact or freshness manifest changed.
No SSOT, public SPEC, pack, wire-schema, release, or Human-PASS claim is made.

Next exact action: locate one current solver/runtime arithmetic vertical that
uses saturating Fixed64 operations, migrate it to checked operations with
typed overflow propagation and atomic failure, then verify Native/WASM parity.
