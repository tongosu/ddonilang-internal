# BOGAE-PROD-07 action-map ingress firewall handoff

## Fixed target

- Product commit: `85728864b410091969e38d381aa8c3191497d2c0`
- Tree: `e4c6ecdcce8428605b777fb268a702bd1bc4d30b`
- Parent: `c1408dcfe7d21fbdb4b6b1dff80d89ab32fe1413`
- Scope: `solutions/seamgrim_ui_mvp/ui/workbench/project_control_model.js` and
  existing `tests/seamgrim_project_control_model_runner.mjs` only.

## Product behavior

The existing `ddn.input_action_map.v1` consumer no longer turns duplicate action
identities or malformed numeric key values into a partially usable action map.
It requires a finite, non-negative integer key value and returns no action map
if any declared row is invalid or duplicates an identity.  The existing action
schema, declared snapshot field set, hashing family, and default pointer/time
projection remain unchanged.

## Validation and mutation evidence

- `node tests/seamgrim_project_control_model_runner.mjs`: PASS after restores.
- `node tests/seamgrim_wasm_vm_runtime_runner.mjs`: PASS.
- `node tests/seamgrim_workbench_runtime_bridge_t1_runner.mjs`: PASS.
- `node --check` for the model and runner: PASS.
- `git diff --check`: PASS before the product commit.
- M-B1: changing duplicate handling to `continue` made the duplicate-map
  assertion RED.
- M-B2: coercing malformed keys to zero made the malformed-action assertion RED.
- M-B3: assigning to the action snapshot made the frozen-payload assertion RED
  with `Cannot assign to read only property 'keys'`.
- Fixed model restore SHA-256:
  `42dae0f82301a8da50d0cdaf767020e1ba651dec4152af0f429843cd2c70a975`.
- Fixed model blob: `9f3ba85a0e9664d2b41ee7ebd0105cd19bc6d16d`.

## Nonclaims

This target closes only the action-map ingress partial-success boundary.  It
does not create or alter the public input schema, profile/document binding,
receipt binding, browser behavior, or a new action identity.  It is ready for
fixed-target independent review.
