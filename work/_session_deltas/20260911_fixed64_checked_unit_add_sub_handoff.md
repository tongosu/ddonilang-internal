# Fixed64 active unit add/sub checked migration handoff

## Fixed target

- Product commit: `8b6b4bcbbab5c1ba6f1ed325bdbd055d3a55e3fe`
- Product tree: `fd64299e841ffbfee5ecb458470909e829d48aa9`
- Parent: `a8aca6c9e4ecee9dc9ba60d74b2169db366e5e54`
- Product path: `tool/src/ddn_runtime.rs`

## Product boundary

The active runtime unit addition and subtraction paths now use checked raw
Fixed64 operations.  The shared helper is consumed by aggregate reduction,
Euler and semi-implicit Euler updates, linear interpolation, infix `+` and
`-`, and formula addition/subtraction.  A raw overflow returns the existing
typed arithmetic failure before a runtime update is published.

## Focused evidence

- `fixed64_infix_add_sub_overflow_publish_nothing`: PASS
- `fixed64_infix_multiply_overflow_publishes_nothing`: PASS
- `fixed64_formula_pow_overflow_is_typed_and_does_not_saturate`: PASS
- `fixed64_powi_`: PASS
- Native library offline check: PASS
- WASM library offline check: PASS
- `git diff --check`: PASS

## Mutation evidence

- M1: replacing checked addition with raw `+` made the `+` overflow case
  succeed and the no-publication assertion RED.
- M2: replacing checked subtraction with `unwrap_or(Fixed64::MIN)` made the
  `-` overflow case succeed and the no-publication assertion RED.
- Both mutations were restored byte-exactly before the focused suite GREEN.
- Restored file SHA-256:
  `0437c60fc94c0d607e6939fff7ce3c0ac8a20f72db9f243c1393e74e00e75042`
- Restored Git blob: `0c5834772172c9ed5e56fb346b0f5c16aebf932e`

## Review request

Review the immutable product target above for active add/sub callers,
overflow diagnostic identity, and no publication on rejected updates.

## Nonclaims

This handoff does not claim Native/WASM textual floating-boundary convergence,
transcendental fixed-point authority, public ABI changes, V1 readiness,
release, or Human PASS.
