# BOGAE-PROD-06 explicit view identity guard handoff

- Product: `5e4c49c260bdd272611e902d7417e06f90d1d826`
- Tree: `934426b4c0203a20d78d63219d1864f735fa77be`
- Parent: `89f170ba6648677ba7d9c219bd7160570f0f2b5f`
- Scope: a committed semantic payload must carry an explicit primary view;
  `view_binding.view_family` cannot silently become a missing view identity.

The focused runner first observed RED because a hash-valid payload with an
empty `primary_view` reached an unsupported-family path rather than the view
identity failure. The fixed product rejects it before renderer selection.
Mutation M-A3 removed the primary-view requirement and reproduced RED at
`missing renderer identity failure drift`. The renderer then restored
byte-exactly to SHA-256
`418700152090fbff8ebd5fd3ff067e69dafe39fb1e71b4ea2a760947f1d1ed7e`, Git
blob `df23c12c4023198d7495f97bd668245289efb325`, followed by GREEN.

GREEN gates:

- `node tests/seamgrim_workbench_semantic_view_renderer_runner.mjs`
- `node --check solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_renderer.js`
- `git diff --check`

This remains partial PROD-06 evidence; it is not a complete Unit A target and
does not make any readiness, release, SSOT, public SPEC, or Human claim.
