# Fixed64 formula unary negation handoff

## Target

- Product commit: `a2bf6b7c93a53935e4e5e8891f8291fc636cc826`
- Tree: `0fa751b248a6cba60e60f4b174dcd9d060ddd4d1`
- Parent: `6f3e6d8df286d53d8c0aa15920378ba133987563`
- Changed product path: `tool/src/ddn_runtime.rs`

## Claim

Formula unary subtraction now routes through `Fixed64::ZERO.checked_sub`.
Negating `Fixed64::MIN` returns the existing typed arithmetic overflow instead
of wrapping to `Fixed64::MAX`. The failing expression produces no `UnitValue`
success result.

## Focused evidence

- `cargo test -p ddonirang-tool --lib fixed64_formula_unary_neg_min_is_typed_overflow -- --nocapture` PASS
- `cargo test -p ddonirang-tool --lib fixed64_ -- --nocapture` PASS (14 tests)
- `cargo check -p ddonirang-tool --lib --offline` PASS
- `cargo check -p ddonirang-tool --lib --target wasm32-unknown-unknown --features wasm --offline` PASS
- `git diff --check` PASS before the product commit.

## Mutation and exact restoration

Fixed file before mutations:

- SHA-256: `e1cb5217857662281a052f51ec586e2f9ee90c668996cc1d33e8b68609911f98`
- Git blob: `b1e4e1c9108a1c87e8a849f3d65ece5853a200ee`

1. Replacing checked subtraction with raw unary negation made the new focused
   test RED: it returned raw `Fixed64::MAX` as a success.
2. Replacing the checked error with `unwrap_or(Fixed64::MAX)` also made the
   test RED by silently saturating.
3. Both mutations were restored byte-exactly to the fixed SHA/blob, then the
   focused test was GREEN.

## Regression boundary

`cargo test -p ddonirang-tool --lib` ran once: 664 passed and 5 failed.
The failures are not attributed to this one-hunk change: two `ai_prompt`
tests require an absent sparse-worktree `docs/ssot`, and the remaining three
are the pre-existing numeric-calculus 1-ULP expectation, BOM parsing, and
runtime-surface profile-canon failures. The Fixed64 focused group passed.

## Review request

Claim: active formula unary negation uses the shared checked Fixed64 owner and
fails closed for `Fixed64::MIN`.

Independent review should confirm exact target/tree/parent, allowed path
scope, the focused test, and one raw-negation or saturation mutation.

## Nonclaims

This target does not close complete Native/WASM textual boundary convergence,
all active Fixed64 callers, V1 readiness, release, or Human PASS. The public
WASM `f64` setter boundary remains outside this no-new-wire slice.
