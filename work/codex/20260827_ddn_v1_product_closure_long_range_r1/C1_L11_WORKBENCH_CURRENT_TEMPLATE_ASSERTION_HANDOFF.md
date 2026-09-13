# C1-L11 Workbench current-template assertion handoff

## Fixed target

- Product/test commit: `ef89007867495cdb2bbf51ae4ba274e761b6dcde`
- Parent: `f9d2f7ddcca073bc3aae0e86312c318872f02987`
- Tree: `e6cbfc2215aa041894a289c6addb9ac282f80f5a`
- Path: `tests/seamgrim_native_project_authoring_runner.mjs`

## Correction

The existing real-browser authoring runner had retained brace-form import and
legacy setting assertions after the tracked Physics template moved to typed V25
module directives.  It now asserts the generated `(힘="./lib/힘") 쓰임.`
surface, adds an ordinary current value definition for the rename non-target,
and checks the corresponding typed import after rename.

## Evidence

- `node --check tests/seamgrim_native_project_authoring_runner.mjs`: PASS
- `project_authoring::tests::current_typed_directives_reach_the_authoring_symbol_frontdoor`: PASS
- Browser execution: NOT_RUN; the checkout has no resolvable `playwright`
  Node package. No package installation or network download was performed.

## Nonclaims

This is a regression assertion correction, not a browser PASS or independent
review. It does not close the broader C1-L11 producer, strict-frontdoor,
Native/WASM, readiness, or release gates.
