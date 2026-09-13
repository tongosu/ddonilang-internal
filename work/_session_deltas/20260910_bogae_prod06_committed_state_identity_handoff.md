# BOGAE-PROD-06 committed state identity handoff

## Fixed target

- Product commit: `fa14edb9c9ce5e3cb35dad12213d06e41291aa90`
- Tree: `43b7f7edc38ce8832e5a8393cbeca526c579c0f0`
- Parent: `2c681e4c28d6caabde95c283142f400882edc28c`
- Product paths:
  - `solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_payload.js`
  - `tests/seamgrim_workbench_semantic_view_payload_runner.mjs`

## Behavior fixed

Canonical view payload construction now requires the existing non-blank
committed `state_hash`. A `result_identity` alone is insufficient to publish a
canonical projection. This reuses the existing unavailable identity outcome;
it adds no identity field, hash algorithm, wire, renderer, or fallback.

## Evidence

- Product-facing RED before implementation: a result-only identity generated
  an available console projection.
- M1 restored the former `state_hash || result_identity` guard: RED at
  `result identity without committed state identity was accepted for projection`.
- M2 stopped trimming `state_hash`: RED at
  `blank state identity was accepted for projection`.
- Both restores returned to product blob SHA-256
  `2cee3bc15d93cb6891e283521101227b35a877f06741a5e8b3a3cb12a2dbd521`, Git
  blob `b9fd6365283b113c3daa4949896c87a9f28b3e59`, followed by GREEN.
- GREEN gates:
  - `node tests/seamgrim_workbench_semantic_view_payload_runner.mjs`
  - `node tests/seamgrim_workbench_semantic_view_renderer_runner.mjs`
  - `node tests/seamgrim_workbench_source_analysis_t4_runner.mjs`
  - `node --check solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_payload.js`
  - `git diff --check`

## Scope and nonclaims

`PRODUCT_FIXED_PENDING_REVIEW`. This is a narrow PROD-06 state/world identity
firewall successor. It does not close full PROD-06, full PROD-07, the
persistent two-blocker goal, V1 readiness, release, SSOT, public SPEC, or
Human approval.

## Review request

Verify the exact product identity, independently restore either the result-only
or whitespace-state acceptance path, then return `PASS_TARGET_BOUND` or
`FAIL_TARGET_BOUND` only for this fixed target.
