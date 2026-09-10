# BOGAE-PROD-06 semantic payload hash firewall handoff

- Product target: `11c0d6249648d24c917660fa3a32ed09e78163da`
- Tree: `372de217753d1473699e9bc5e4fbe8f955c5e2f7`
- Parent: `07d00e6b1fa349502453afc371d3ee78c23794e4`
- Product scope: `semantic_view_renderer.js` and its existing renderer runner.

The renderer now recomputes the existing semantic payload hash over the
payload excluding `semantic_payload_hash`; a mismatch produces the existing
canonical unsupported projection failure before any render model or canvas
success projection is created.  No identity family, public wire, or hash
algorithm was added.

Focused evidence: semantic renderer runner, semantic payload runner, and view
instance model runner PASS; JavaScript syntax and `git diff --check` PASS.

Mutation evidence, all restored to renderer SHA-256
`eacc7f3d57c5601fe066d052ca40875d41cabedaab0193a38663dda8190526d6`,
blob `7937b53c8c07f460e68332d1ff739bf97edfec2d`:

1. Bypass hash comparison: stale payload reached a success renderer (RED).
2. Permit the stale declared hash: stale reuse reached a success renderer (RED).
3. Downgrade typed hash failure to `lineModel`: stale payload reached a
   success renderer (RED).

`BOGAE-PROD-06 = PRODUCT_FIXED_PENDING_REVIEW`. This handoff does not claim
complete workspace/world/provider hash closure, browser PASS, Native/WASM
parity, tracked WASM freshness, release, or V1 readiness.
