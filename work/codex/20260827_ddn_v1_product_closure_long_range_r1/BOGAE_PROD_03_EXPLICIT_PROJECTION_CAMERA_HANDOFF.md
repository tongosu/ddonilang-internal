# Bogae PROD-03 — explicit projection camera handoff

## Fixed target

- product: `234ec4ecfb730f0720394b9514c8bfb68ba0174b`
- tree: `497acf18b87462b143302b2135016ab8efbe3ab5`
- parent: `e22d069eae7256d01c349e521d9c43da733392de`
- merge count: `0`

## Behavior

Line, projectile, and grid projection now require finite, ordered existing
camera bounds. The renderer no longer creates data-derived min/max bounds,
fixed `0/1` bounds, or a geometry/default grid camera. A missing or invalid
camera returns the existing typed canonical unsupported projection failure;
semantic payload and geometry remain unchanged and no success canvas model is
published. Explicit cameras continue to drive deterministic supported renders.

## Paths and gates

- `solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_renderer.js`
- `tests/seamgrim_workbench_semantic_view_renderer_runner.mjs`
- `node tests/seamgrim_workbench_semantic_view_renderer_runner.mjs` — PASS
- `python tests/run_seamgrim_view_only_state_hash_invariant_check.py` — PASS
- changed JS syntax checks and `git diff --check` — PASS

## Mutations

Both mutations RED on the canonical runner with
`geometry must not synthesize a grid camera`, then exact-restored and GREEN:

1. B1 restored fallback `0/1` camera bounds for missing/invalid input.
2. B2 restored a grid default camera when `space2d.camera` was absent.

Fixed renderer blob/SHA-256 after each restore:
`101b46c035046dea9066261e774ba92aa4e2a710` /
`ae6b4e8536cd2bec30524ee7b82cbe898d474976e1fb26f87225b7d931332894`.

## Nonclaims

`PRODUCT_FIXED_PENDING_REVIEW` only. This does not claim broad Bogae
conformance, Native/WASM parity closure, V1 readiness/release, or Human PASS.
