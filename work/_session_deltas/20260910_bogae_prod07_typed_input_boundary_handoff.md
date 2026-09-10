# BOGAE-PROD-07 typed InputSnapshot boundary handoff

## Fixed target

- Product commit: `29b6af1ac9e675ece11a09cefe0104106d125075`
- Tree: `487f414a319f1aa1e24b1f54b4123fed507d3ba1`
- Parent: `c4a55c777d8c49addbcff932fe1a228c87c37d27`
- Scope: `solutions/seamgrim_ui_mvp/ui/runtime/wasm_vm_runtime.js` and the existing `tests/seamgrim_wasm_vm_runtime_runner.mjs` only.

## Product behavior

The shared WASM frame-input boundary now requires the existing five-field
runtime frame input (`keys`, `lastKey`, `px`, `py`, `dt`) before dispatch.  It
does not coerce missing fields to defaults, and it does not lower a supplied
input to `stepOneParsed()` when the typed client entrypoint is absent.  Both
conditions use the pre-existing `E_WASM_STEP_FAILED` failure path; no public
diagnostic, wire field, identity family, or fallback was added.

The existing runner proves an incomplete input has zero typed frame dispatch,
the missing typed API has zero frame dispatch, a complete input dispatches once,
and a frozen input object remains unchanged.

## Validation and mutation evidence

- `node tests/seamgrim_wasm_vm_runtime_runner.mjs`: PASS after each restore.
- `node tests/seamgrim_workbench_runtime_bridge_t1_runner.mjs`: PASS.
- `node --check` for the runtime and runner: PASS.
- `git diff --check`: PASS before the product commit.
- M-B1: bypassing the required-field validator made incomplete input pass and
  produced the runner RED assertion `incomplete typed input rejected before dispatch`.
- M-B2: restoring the old missing-typed-API fallback made the API-absence case
  pass and produced the runner RED assertion `typed input API absence rejects before fallback`.
- M-B3: mutating `input.keys` in the boundary helper made the frozen-input case
  RED with `Cannot assign to read only property 'keys'`.
- Fixed runtime restore SHA-256:
  `4aa91e59bf992de8de75c5b876e1e3664bec1559f4488671e71908d9fb24404c`.
- Fixed runtime blob: `24dd4a2a4325394285b74ea863ecafb7fab481aa`.

## Nonclaims and next work

This is a product-fixed typed frame-input boundary, not a complete closure of
the broader GUI InputSnapshot contract.  Document/profile/action and stale
receipt bindings remain to be verified through their existing Workbench
frontdoor without inventing a new WASM wire.  Browser behavior was not claimed.
The target is ready for fixed-target independent review.
