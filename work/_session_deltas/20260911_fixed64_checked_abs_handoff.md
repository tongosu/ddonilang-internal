# Fixed64 checked absolute-value caller handoff

- Product: `26aebcf03be1611e04e16374e9f2502b6315bebc`
- Tree: `de742513b25b68e4d7e09d775035d40adb13e26f`
- Parent: `b53228de54218ca2dad64376a59260a34d7ca7a0`
- Product path: `tool/src/ddn_runtime.rs`
- Fixed blob: `cf854e6bb471b22e30ac8810c01d6feed4da168c`
- Fixed SHA-256: `a1a10e0ae2f3e159c78702d56dfdbe202e41f27f0a9c19bc8ea05888344ab761`

## Claim

The active absolute-value helper no longer maps `Fixed64::MIN` to `MAX`.
It returns typed arithmetic overflow, which is propagated through formula
`abs`, Gini, numeric derivative/integral errors, and bisection residuals
before a successful runtime publication.

## Mutation

M1 temporarily restored `MIN -> MAX` saturation while retaining the checked
signature.  `fixed64_min_abs_is_typed_and_publishes_nothing` then RED because
the update returned success rather than rejecting before publication.  The
helper was restored exactly to blob `cf854e6…`, and the focused test GREENed.

## Gates

- `cargo test -p ddonirang-tool --lib fixed64_min_abs_is_typed_and_publishes_nothing -- --nocapture` — PASS.
- `cargo test -p ddonirang-tool --lib numeric_root_finding_v1_bisection_returns_root_residual_iteration_method -- --nocapture` — PASS.
- Native offline tool library check — PASS.
- WASM offline tool library check — PASS.
- `git diff --check` — PASS before product commit.

## Review boundary

Ready for independent review: YES.  Nonclaims: this target does not close the
existing public f64 snapshot/setter ABI, every Fixed64 caller, release, or
Human PASS.
