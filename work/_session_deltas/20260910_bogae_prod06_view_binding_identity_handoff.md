# Bogae PROD-06 view-binding identity handoff

- Product/tree/parent: `55140a1f567c7fa34f090509723106839c936c97` /
  `87e0585150eb6ed3fea02b68e493793dc1b2c4e7` /
  `a1e39a97615ca2e124e4736ae852a6b7a5afe0d6`.
- Scope: existing semantic renderer and its existing focused runner.

A hash-valid semantic payload could previously declare one primary view in
`view_config` while binding another family in `view_binding`; the renderer used
the configuration and published a projection. The renderer now requires the
existing view-binding schema, exact `view_family`, and the existing canonical
payload key to agree before any family model is built. It reuses the existing
typed canonical projection failure and changes no payload field, hash
algorithm, renderer identity, or public wire.

Pre-change RED: a hash-recomputed line payload with `view_binding.view_family`
changed to `grid` still returned a ready model. The new focused assertion was
RED before the product hunk. Removing the new guard after implementation was
RED at `hash-valid mismatched view binding must fail before projection`.
Restored renderer SHA-256:
`3a2cf323b36018a1feb6091f87c0e249e123a7b5bb7b0accd59112a9124e6d8f`;
blob `537f09f56b9a557c0ddf835af009e5b15f1afca5`.

GREEN: semantic renderer runner, semantic payload runner, Workbench T4
source-analysis runner, JS syntax, and diff check. This is
`PRODUCT_FIXED_PENDING_REVIEW`. Broader workspace/world/provider/receipt hash
coverage remains outside this narrow view-binding target.

READY_FOR_FIXED_TARGET_INDEPENDENT_REVIEW=YES
