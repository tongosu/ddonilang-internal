# BOGAE-PROD-07 action project-binding handoff

## Fixed target

- Product commit: `b2d81fdb98c6f6f3f844a47cb10485bbf1e9a932`
- Tree: `eef91ffdde8242614716c69be18c19f1e8d21058`
- Parent: `3e96aed9d568a0b45deffe4f05b57ada978151db`
- Scope: `solutions/seamgrim_ui_mvp/ui/workbench/project_control_model.js` and
  existing `tests/seamgrim_project_control_model_runner.mjs` only.

## Product behavior

The existing action-map normalizer now rejects a declared nonempty
`project_id` that differs from the current workspace project.  It preserves the
existing action-map schema and hash family; it only refuses cross-project action
injection before any action can be queued or dispatched.

## Evidence

- RED before implementation: a foreign project action map was accepted for the
  current workspace.
- `node tests/seamgrim_project_control_model_runner.mjs`: PASS.
- `node tests/seamgrim_wasm_vm_runtime_runner.mjs`: PASS.
- `node tests/seamgrim_workbench_runtime_bridge_t1_runner.mjs`: PASS.
- `node --check solutions/seamgrim_ui_mvp/ui/workbench/project_control_model.js`: PASS.
- `git diff --check`: PASS before the product commit.
- M-B1: bypassing the declared/current project mismatch guard made the foreign
  project assertion RED.
- M-B2: replacing the declared project id with the current project id made the
  same assertion RED.
- Fixed model restore SHA-256:
  `0dced76ccbbe0188e93e7717514131393edd65b70c88b74b8902dc6db4d2653f`.
- Fixed model blob: `f3a1e68fd5f022a86afa9cc1f18105d373d094fa`.

## Nonclaims

This closes only the cross-project action-map ingress boundary.  It does not
create a new public input field, modify document/source-profile wire, or claim
browser, V1 release, or Human closure.  It is ready for fixed-target independent
review.
