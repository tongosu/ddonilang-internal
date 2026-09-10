# Bogae PROD-07 action workspace identity handoff

- Product/tree/parent: `7246b1b20dfc96d20de73f6e748a0a50cd47295b` /
  `1bd1d87eb2725f6eec33ed859362a0a3fbbb1519` /
  `ac2d2d1a776b140fddc66966c8dbaa7c707f9074`.
- Scope: existing action-map normalizer and its existing runner only.

An action map with a blank existing `project_id` was previously adopted by the
current workspace.  When a current workspace identity is supplied, the
normalizer now requires a nonempty identical declared `project_id`; it no
longer synthesizes that binding.  No field, schema, fallback, or public wire
was added.

M-B1 restored the former empty-project acceptance and made the focused runner
RED (`unbound action map was adopted by the current workspace`); exact restore
was GREEN.  The action-map runner, runtime bridge runner, JS syntax, and diff
check passed.  This is `PRODUCT_FIXED_PENDING_REVIEW`; broader document,
profile, receipt, and browser InputSnapshot parity remain outside its scope.
