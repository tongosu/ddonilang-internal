# Bogae PROD-06 canonical-result identity handoff

- Product/tree/parent: `80df31e12690c42d3dddfcae2b7a8af3d906c36e` /
  `56d02d10c810b9e70db98882e76efc62da0e242e` /
  `56588f2ecbc0b39fa09aedd60290364fd8680c73`.
- Scope: existing semantic renderer and existing focused runner.

A hash-valid payload could carry a canonical workbench result whose state hash,
source hash, or tick differed from the committed frame. The renderer now
requires exact equality before projection, reusing its typed unsupported
projection failure. No identity field, hash algorithm, renderer, or wire was
added.

Pre-change and guard-bypass RED: `hash-valid canonical identity mismatch must
fail before projection`. Restored renderer SHA-256:
`fd632c32a241f83b48e7c19d0d30efb6e00fee9616a88a9a636be1fd5bae8660`;
blob `de143a725383218836fa8871bb9ae68ae3ba3bad`. Renderer/payload tests, syntax,
and diff check are GREEN.

This is `PRODUCT_FIXED_PENDING_REVIEW`; full PROD-06 workspace/world/provider
and receipt coverage remains open.
