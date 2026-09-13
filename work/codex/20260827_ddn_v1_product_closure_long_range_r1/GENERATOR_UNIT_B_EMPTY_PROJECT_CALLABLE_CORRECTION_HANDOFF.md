# Generator Unit B empty-project correction handoff

Product target: `bf81bfa2174e7c38cbc8d085b49c9ddbff68371a`
Parent: `142eb33ec31d6fe2f457ef756578bdcd5c5a26a5`
Tree: `aea80216acdc0d55535297e1576d76a9e4a877ee`

The empty Local Project template no longer inserts an inner `매마디:움직씨`
callable. Local Project supplies the shared V25 execution callable, so generated
`app/main.ddn` now contains the current declaration body:

```ddn
값:수 := 0.
값 보여주기.
```

This removes the reproduced `E_EXECUTION_PARSE` nested-callable type failure.
The existing local-project test module now verifies shared supported-profile Run,
output `0`, and deterministic state/summary identities across two executions.

Changed paths:

- `solutions/seamgrim_ui_mvp/ui/workbench/workbench.js`
- `tool/src/local_project.rs`

Focused test and `cargo check -p ddonirang-tool --offline` passed; `git diff --check`
passed before the product commit. No SSOT, SPEC, public wire, WASM artifact, or
fallback change is included. This is `PRODUCT_FIXED_PENDING_REVIEW` only.

`READY_FOR_INDEPENDENT_REVIEW=YES`. The outstanding three-name/WASM/browser
parity and mutation evidence remain for the bundled Unit A/B independent review.
