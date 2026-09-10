# BOGAE-PROD-04 exact provider/kind binding handoff

- Product target: `6dfb365eb6dda7d6ac75162bc9cb8658308b946d`
- Product tree: `4d64f07212df050b6b8b14ac4a07ab1ef8fb6589`
- Direct parent: `a1bcf503937fb814be0c1917d4fce35fc9fa6476`
- Scope: exact existing draw-kind identity mapping and Workbench projection rejection.

## Product behavior

`tool/src/wasm_api.rs` no longer case-folds, substring-matches, or assigns a
default Bogae kind.  It maps only the existing exact canonical and Korean
identities; an unrecognized value remains unrecognized.  The Workbench
semantic renderer accepts only exact canonical draw kinds and returns the
existing canonical unsupported-projection failure before canvas publication
when a draw list contains an unsupported kind.

The semantic payload is not changed during either successful or rejected
projection.

## Validation

- `cargo check -p ddonirang-tool --lib --features wasm --offline` — PASS
- `cargo test -p ddonirang-tool --lib --features wasm bogae_kind_mapping_requires_an_exact_existing_identity --offline -- --nocapture` — PASS
- `node tests/seamgrim_workbench_semantic_view_renderer_runner.mjs` — PASS
- `node --check solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_renderer.js` — PASS
- `git diff --check` — PASS

## Mutation evidence

- M-A1: restored `raw.contains("line")`; the Rust exact-identity test failed
  for `prefix-line`.  Restore SHA-256
  `ecf1cc2fb381dfe5f092c706411b9d4e6de7382f115fe3b2666ade0fac298ef0`,
  blob `4db1ab214ba3969364acf686d1f2cd1f8e2986c7`; focused GREEN after restore.
- M-A2: changed the renderer identity test to `includes("line")`; the
  canonical Node runner failed at `unknown Bogae kind must fail closed`.
  Restore SHA-256
  `ddd28cf964b76e9848f043db07ce0f11d93ae6b15385625d5c1a0d6c7df61c31`,
  blob `ca4c66ddf836db0a087451273273e27e5c621cd1`; GREEN after restore.
- M-A3: mapped unrecognized kinds to `line`; the Rust exact-identity test
  failed for `prefix-line`.  Restore SHA-256 and blob equal M-A1; focused
  GREEN after restore.

## Custody and nonclaims

- Changed product paths are exactly `tool/src/wasm_api.rs`,
  `solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_renderer.js`, and
  `tests/seamgrim_workbench_semantic_view_renderer_runner.mjs`.
- No SSOT, public SPEC, renderer identity, public wire, release, or Human gate
  changed.
- This is `PRODUCT_FIXED_PENDING_REVIEW`, not `CLOSED_TARGET_BOUND`.
- Next non-overlapping vertical: BOGAE-PROD-05 raw-source shared-frontdoor
  parity.
