# Independent review: Fixed64 formula unary negation

## Verdict

`PASS_TARGET_BOUND`

## Reviewed target

- Product commit: `a2bf6b7c93a53935e4e5e8891f8291fc636cc826`
- Tree: `0fa751b248a6cba60e60f4b174dcd9d060ddd4d1`
- Parent: `6f3e6d8df286d53d8c0aa15920378ba133987563`
- Scope: `tool/src/ddn_runtime.rs` only
- Fixed blob: `b1e4e1c9108a1c87e8a849f3d65ece5853a200ee`

## Independent evidence

- `fixed64_formula_unary_neg_min_is_typed_overflow` passed.
- Related `fixed64_formula_pow_overflow_is_typed_and_does_not_saturate` passed.
- `git diff --check` passed for the reviewed scope.
- Replacing checked subtraction with raw negation makes `-Fixed64::MIN`
  unrepresentable (debug overflow/panic); a saturation substitution would
  instead publish successful `Fixed64::MAX`. Both violate the typed-overflow
  assertion. The reviewed product blob remained byte-identical.

## Scope limit

This is a narrow active-formula caller verdict. It does not certify full
Native/WASM Fixed64 convergence, every active caller, V1 readiness, release,
or Human PASS.
