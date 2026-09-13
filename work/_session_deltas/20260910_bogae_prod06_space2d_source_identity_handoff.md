# BOGAE-PROD-06 space2d source identity handoff

## Fixed target

- Product commit: `b90d68f872f12224c08cc8b7efd5ee5bee7d6d5a`
- Tree: `d6a79444c01fda9dfacbfa057048b673e73b9cc9`
- Parent: `f2789bb0bf31437da12540d41e305192ef46f597`
- Product paths:
  - `solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_payload.js`
  - `tests/seamgrim_workbench_semantic_view_payload_runner.mjs`

## Behavior fixed

`space2d` canonical payload construction no longer derives entity identities
from collection, shape, or structural FNV data. Every projected entity must
carry an existing `id` or `group_id`; otherwise the existing canonical invalid
path prevents projection. No identity family, hash algorithm, wire, renderer,
or fallback was added.

## Evidence

- Pre-change RED: a source-less `space2d` drawlist row received a derived
  identity and emitted an available canonical payload.
- M1 restored structural derivation: RED at
  `source-less space2d entity received a derived identity`.
- M2 removed the empty-identity rejection: the same focused case RED because
  a source-less row was published.
- Both restores returned to SHA-256
  `74fccb8efc45bf73efc6219bbac28464268a5508f55b33bb6e83e2ace04ee437`, Git
  blob `51c57f2d1f2a3ef2752324fbdf771078432d6ce7`, followed by GREEN.
- GREEN gates:
  - `node tests/seamgrim_workbench_semantic_view_payload_runner.mjs`
  - `node tests/seamgrim_workbench_semantic_view_renderer_runner.mjs`
  - `node tests/seamgrim_workbench_source_analysis_t4_runner.mjs`
  - `node --check solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_payload.js`
  - `git diff --check`

## Scope and nonclaims

`PRODUCT_FIXED_PENDING_REVIEW`. This is a narrow PROD-06 missing-identity
firewall. It does not close full PROD-06, full PROD-07, the persistent goal,
V1 readiness, release, SSOT, public SPEC, or Human approval.

## Review request

Verify the product target, independently restore structural identity derivation
or remove the empty-id guard, and return `PASS_TARGET_BOUND` or
`FAIL_TARGET_BOUND` for this target only.
