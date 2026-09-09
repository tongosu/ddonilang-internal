# lesson_plan_roundtrip_v1

G5 product gate for `lesson_plan.v0.toml`.

This pack fixes the product contract for a TOML lesson plan loader/runner/editor:

- Parse `lesson_plan.v0.toml` into a normalized AST in product UI code.
- Run the four pendulum activities in the browser product path.
- Keep list editing and code editing semantically lossless.
- Do not introduce new DDN syntax, runtime semantics, or `state_hash` inputs.

The browser proof is `tests/seamgrim_lesson_plan_v0_runner.mjs`.
