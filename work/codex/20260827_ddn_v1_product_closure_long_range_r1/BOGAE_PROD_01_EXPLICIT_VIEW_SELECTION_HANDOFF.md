# Bogae PROD-01 — explicit view selection handoff

## Fixed target

- product: `0bbb9138f734bb481d4868f4a2c76fd050ea9acd`
- tree: `f7c222582058699df1c82b05fbf0e3ae27943be8`
- parent: `ccc10b646ae81e18e552b0d992c660fe34d5e64f`
- merge count: `0`

## Behavior

The committed semantic payload now preserves a missing primary renderer identity
as empty instead of materializing `line`. The renderer likewise has no missing
identity default. Numeric observations, x/y-shaped values, a line-capable
canonical result, and field presence cannot select a renderer. Explicit exact
supported identities retain their prior behavior. Selection failure is the
existing typed canonical projection failure and does not mutate the semantic
payload or publish a model/canvas success.

## Paths

- `solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_payload.js`
- `solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_renderer.js`
- `tests/seamgrim_workbench_semantic_view_renderer_runner.mjs`

The payload path was a direct lease expansion because it was the
current-reachable `?? "line"` materialization owner. No other path changed.

## Gates

- `node tests/seamgrim_workbench_semantic_view_renderer_runner.mjs` — PASS
- `python tests/run_seamgrim_view_only_state_hash_invariant_check.py` — PASS
- JavaScript syntax checks for changed paths — PASS
- `git diff --check` — PASS

## Mutations

Both mutations RED on the canonical runner with
`missing renderer identity must not default to line`, then exact-restored and
GREEN:

1. A1 reintroduced a numeric-observation → `line` selection.
2. A2 reintroduced missing-identity → default `line` selection.

Fixed payload blob/SHA-256 after each restore:
`1f0fee6e1e699360deb7fba4f35ce89ac974f226` /
`a3acc45dcce931a1be23aa5ebf296099b3c25a907e6570286cb9857aa8e73d36`.

## Nonclaims

`PRODUCT_FIXED_PENDING_REVIEW` only. No independent PASS, broader Bogae
closure, Native/WASM parity closure, V1 readiness/release, or Human PASS is
claimed.
