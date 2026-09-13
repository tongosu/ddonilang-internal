# Bogae PROD-06 committed-frame identity handoff

## Fixed target

- Product: `61a31ea145d42b6ddf07b9283112c27f1cf92951`
- Tree: `2c6fdaff3502ee83f9dc59eb1162481d6af0d44f`
- Parent: `75b2afddeb844aec2d7cc94bdd5957adf89ee538`
- Scope: existing semantic renderer and its existing behavior runner only.

## Corrected behavior

A hash-valid semantic payload with a blank committed-frame `run_id` or
`source_hash` previously reached a ready projection.  The renderer now accepts
an already-present committed frame only when its run, frame, madi, state, and
source identities are all nonempty and valid.  It reuses the existing typed
canonical-projection failure code; no carrier field, semantic identity family,
or public wire was added.

The invalid carrier produces no projection model and does not mutate the
payload.  Valid payload behavior remains covered by the existing renderer,
payload, and view-workspace runners.

## Mutation evidence

- M-A1 removed the committed-frame guard.  The runner was RED because a
  hash-valid blank `run_id` became a projection success; exact source restore
  was GREEN.
- M-A2 omitted `source_hash` from the identity guard.  The runner was RED
  because a hash-valid blank source identity became a projection success;
  exact source restore was GREEN.

## Gates and disposition

- semantic renderer runner: PASS
- semantic payload runner: PASS
- view-instance runner: PASS
- JavaScript syntax and `git diff --check`: PASS

`BOGAE-PROD-06` remains broader than this exact slice: workspace/provider and
receipt-binding coverage, browser behavior, and full three-frontdoor parity
are not claimed.  This product target is `PRODUCT_FIXED_PENDING_REVIEW`.
