# Seamgrim index markup release-gate handoff

## Fixed target

- Base: `84e3f114b9f1809b65a0479e1d51c52b2fdaeaa1`
- Product fixed: `5cfaa780e4190c926b96848135e619944b513dbf`
- Product tree: `cd4cc552c7c245f013e794f8172a654e9d30643f`
- Parent: `84e3f114b9f1809b65a0479e1d51c52b2fdaeaa1`
- Merge count: `0`

## Root cause and correction

The default server route redirects to the tracked Workbench.  Its document title already contained `셈그림`, but its real rendered canvas was named `bogae-canvas`; the existing release gate accepts `canvas` or `canvas-bogae`.  The actual canvas was renamed to `canvas-bogae`, and the existing Workbench renderer lookup and CSS selector were changed to the same identity.  The data-testid and renderer surface were preserved; no hidden or checker-only DOM was added.

## Evidence

- Before the fix, the release gate stopped at `index_markup_missing detail=title_or_canvas`.
- M1: removing all three real `셈그림` title/brand bindings produced the same release-gate RED; exact restore completed.
- M2: changing the actual canvas id away from `canvas-bogae` produced the same release-gate RED; exact restore completed.
- After restore, the gate progressed to the independent next blocker: `lesson_inventory_api_invalid detail=release_inventory_mismatch:missing=-:extra=elem_econ_allowance_budget,elem_econ_store_stock,elem_math_fraction_line,elem_math_number_line,elem_math_rectangle_area`.
- `node --check solutions/seamgrim_ui_mvp/ui/workbench/workbench.js`: PASS.
- Actual local `/api/run` regression: V25 `ok=true`, profile `v1-core-v25`, state hash and receipt present; legacy fixture HTTP 500 / `E_V25_DEFINITION_MIGRATION_REQUIRED` / no graph.
- `git diff --check`: PASS.

## Browser limitation

An actual browser attempt was made against the local Workbench server.  The browser automation surface refused localhost because its admin-policy check was unavailable.  The existing Workbench browser runner also could not start because the checkout has no installed `playwright` module.  No browser-security bypass and no dependency download were attempted.  Therefore browser load/V25 UI-run evidence remains OPEN even though the release gate has advanced past the index markup condition.

## Boundary

`INDEX_MARKUP_BLOCKER=IMPLEMENTED_PRODUCT_FIXED`, pending actual browser evidence.  This handoff does not close the release gate, migrate inventory membership, alter `/api/run` semantics, or claim P0--P6/V1 readiness/release/activation/legal/Human PASS.
