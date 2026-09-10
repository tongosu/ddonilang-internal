# BOGAE-PROD-06 view-selection hash firewall handoff

## Fixed target

- Product commit: `e254da896dfef2c2b8e7b469a1dfd6518855e92f`
- Tree: `fc6d6d23491e95abc76249820541d1da1bb250bf`
- Parent: `70efb00a581dc12223557a1d4156926be30a65a0`
- Scope: `solutions/seamgrim_ui_mvp/ui/workbench/view_instance_model.js` and
  existing `tests/seamgrim_workbench_view_instance_model_runner.mjs` only.

## Product behavior

`reconcileViewWorkspace()` now treats a selected target without a committed
state hash as unbound.  On reconciliation it clears that selection and removes
dependent temporary views, instead of preserving a temporary magnifier through
a later committed frame.  Existing matching state-hash selections remain
unchanged.  No new hash family, public wire, renderer family, camera rule, or
world mutation was introduced.

## Evidence

- RED before implementation: an unbound selected target survived a committed
  frame in the existing view-instance runner.
- `node tests/seamgrim_workbench_view_instance_model_runner.mjs`: PASS.
- `node tests/seamgrim_workbench_semantic_view_renderer_runner.mjs`: PASS.
- `node tests/seamgrim_wasm_vm_runtime_runner.mjs`: PASS.
- `node --check solutions/seamgrim_ui_mvp/ui/workbench/view_instance_model.js`: PASS.
- `git diff --check`: PASS before the product commit.
- M-A1 restored the old nonempty-hash-only comparison and made the unbound
  target assertion RED.
- M-A2 bypassed reconciliation clearing and made the stale-target assertion RED.
- Fixed view-model restore SHA-256:
  `3f5b36b1c8911205c2d1db9e5da4a3230f06bb16c0ced0f1c07371fa125bc67c`.
- Fixed view-model blob: `197635894c11f2901e1e834fd5316e6782ece9c2`.

## Nonclaims

This target closes only the unbound selection/state-hash boundary.  It does not
claim all Workspace/View/Bogae/world hash matrix cases, browser behavior,
release readiness, or Human approval.  It is ready for fixed-target independent
review.
