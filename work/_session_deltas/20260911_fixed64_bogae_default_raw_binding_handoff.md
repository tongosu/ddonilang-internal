# Fixed64 Bogae omitted-default raw binding — handoff

## Immutable product target

- Product commit: `6063451d7dd957fcb153a2b4b9f6543bc2082e1f`
- Tree: `2c3144f5f884ecbc31bc415809cfa59844f8c5fa`
- Parent: `a4a2ca0a6de02ce4c93cead8addbf907e569b407`
- Product path: `tool/src/ddn_runtime.rs`
- Fixed product source SHA-256: `7B0FC3138493C15B621300EF589012B09D37A3D28B89EB417EE751D8D580E656`
- Fixed product source blob: `cd6df012ee1c2559fb538877fbbf6b38dd49c0b1`

## Claim for independent review

Current Bogae shape fields omitted by a user source (`width`, `r`, `size`, `w`,
and `h`) now obtain their values from named Q31.32 raw `Fixed64` constants,
not host `f64` conversion at the runtime defaulting boundary.  The runtime
behavior test executes a real shape block and asserts the emitted draw-list
fields against literal raw values.

## Evidence

- Focused tests PASS:
  - `ddn_runtime::tests::bogae_omitted_numeric_defaults_are_exact_fixed64_raw_values`
  - `ddn_runtime::tests::bogae_omitted_shape_fields_publish_exact_fixed64_defaults`
- `cargo check -p ddonirang-tool --offline`: PASS.
- `git diff --check`: PASS before product commit.
- Full `cargo test -p ddonirang-tool`: 666 PASS / 5 pre-existing, out-of-scope
  failures: two `ai_prompt` tests need a worktree-local `docs/ssot`; one
  numeric-calculus expected-raw assertion; one BOM project-authoring test; and
  one runtime-surface profile assertion.  This handoff does not claim that
  aggregate regression is green.

## Mutation evidence

- M1 raw authority corruption: changed `BOGAE_DEFAULT_STROKE_WIDTH` to zero.
  The emitted line width changed from raw `85899345` to `0`; the focused
  omitted-shape test was RED. Restored the named raw constant exactly, then
  focused tests were GREEN.
- M2 runtime selector corruption: changed the line-shape omitted-width
  selector to `Fixed64::ZERO`. The same emitted-width assertion was RED.
  Restored `BOGAE_DEFAULT_STROKE_WIDTH` exactly, then focused tests were GREEN.

## Review scope and nonclaims

Review the single product path plus its tests in the immutable target above.
This slice does not claim that every `from_f64_lossy` use in the runtime is
removed, does not modify a public WASM API, and does not claim broader Bogae,
Fixed64, V1 readiness, release, or Human PASS closure.

Status: `PRODUCT_FIXED_PENDING_REVIEW`.
