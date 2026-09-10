# BOGAE-PROD-07 typed action snapshot handoff

## Fixed target

- Product commit: `4fb6e82fce6ed56c8b063fdca08d8a35c3c99127`
- Tree: `2fb65c273eba20cbefb3c725c17c39ae6c047d7b`
- Parent: `3c0f8442bd91cafbd00cdde53ad71ebd55c1b39b`
- Product paths:
  - `solutions/seamgrim_ui_mvp/ui/workbench/project_control_model.js`
  - `tests/seamgrim_project_control_model_runner.mjs`

## Behavior fixed

`normalizeAction()` now admits only the existing nested `input_snapshot` object
and its existing snake-case fields. It no longer treats `raw.input`, top-level
`keys`, top-level input fields, camel-case `lastKey`, or `px`/`py` aliases as a
typed InputSnapshot. A missing or partial typed snapshot fails before an action
is published. No schema, public wire field, renderer identity, or fallback was
added.

## Evidence

- Focused RED before the product change: `node tests/seamgrim_project_control_model_runner.mjs`
  failed with `raw input object was accepted as a typed InputSnapshot`.
- M1 temporarily restored `raw.input` fallback: the same focused test RED with
  that exact assertion; byte-exact restore then GREEN.
- M2 temporarily restored top-level `keys` fallback: the focused test RED with
  `top-level key alias was accepted as a typed InputSnapshot`; byte-exact
  restore then GREEN.
- Restored product blob: SHA-256 `5380c3750adea5a8d4a39ffd9e12c5e283a7a4f694ae3b671e1c5351b0a39f16`,
  Git blob `b790d94730e54464bf70e161115f9c9572236b3d`.
- GREEN:
  - `node tests/seamgrim_project_control_model_runner.mjs`
  - `node tests/seamgrim_workbench_runtime_bridge_t1_runner.mjs`
  - `node tests/seamgrim_workbench_source_analysis_t4_runner.mjs`
  - `node --check solutions/seamgrim_ui_mvp/ui/workbench/project_control_model.js`
  - `git diff --check`

## Scope and nonclaims

`PRODUCT_FIXED_PENDING_REVIEW`. This is one narrow BOGAE-PROD-07 firewall
vertical. It does not close the full PROD-07 Unit B, the persistent two-blocker
goal, V1 readiness, release, SSOT, public SPEC, or Human approval.

## Review request

Verify the exact product commit/tree/parent, exercise the two negative typed
snapshot cases, independently reintroduce one dangerous alias fallback, and
return `PASS_TARGET_BOUND` or `FAIL_TARGET_BOUND` for this target only.
