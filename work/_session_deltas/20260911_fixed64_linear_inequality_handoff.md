# Fixed64 linear inequality handoff

## Fixed target

- Product: `30319487652c3de48c20c064e590cacfd9c2cb22`
- Tree: `5523bb6d54bf27def448e7ef050fb08372ccbf43`
- Parent: `41687a823d32eabe670e481030c145ba9b23d1dc`
- Product path: `tool/src/ddn_runtime.rs`

## Claim

The active `선형부등식.풀기` runtime caller now uses checked Fixed64 subtraction for both sampled slopes and the boundary RHS.  An unrepresentable RHS is rejected with `E_RUNTIME_ARITH_OVERFLOW` before a solution pack can be published; it is not saturated into a false bounded interval.

## Evidence

- `linear_inequality_rhs_overflow_is_typed_and_publishes_nothing`: PASS for `x - 2147483647 <= 2147483647`.
- `linear_inequality_solve_minimum_v1`: PASS (bounded and empty interval regressions).
- Offline WASM library check: PASS.
- M1 fixed Git blob: `d8fe12f9aa02f0f6a00673a2451abfac79c711ef`.
- M1 fixed canonical SHA-256: `3019dbe8c96df62ebd264fbb6a288a8f1699396ad596ec3a3831447d6737cad8`.
- M1 mutation replaced all three checked subtractions with saturation.  RED: the unrepresentable RHS returned a published `linear_inequality_solution` pack rather than an error.  Exact restore matched the blob/SHA above; focused tests returned GREEN.
- Full `cargo test -p ddonirang-tool --lib -- --nocapture`: 655 passed; five existing unrelated failures remain (two ai_prompt fixture tests, numeric-calculus expected value, project-authoring BOM parse, runtime-surface profile canon).  The new linear inequality test passed.
- `git diff --check`: PASS before product commit.

## Review boundary

Review only this active solver caller and its typed overflow behavior.  Do not infer complete Fixed64 active-caller migration, global Native/WASM convergence, V1 readiness, release, or Human PASS.
