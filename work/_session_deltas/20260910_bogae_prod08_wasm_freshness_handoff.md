# Bogae PROD-08 tracked WASM freshness handoff

## Fixed target

- Product: `a48594bab2fedab24ce9b5417b311eecf627e339`
- Tree: `d7d3d1923be13eccce7508773e3507dfbfa25be6`
- Parent: `8c6001b3f54837f4eaafa6387476264cf67f75f3`
- Scope: `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm` and the
  existing `ddonirang_tool.manifest.detjson` only.

## Behavior and evidence

- The official `scripts/build_wasm_tool.ps1 -Profile release -Target web`
  build and existing copy script rematerialized the tracked artifact.
- The existing freshness checker was RED before the change for stale
  `source_tree_sha256` and `source_files`, then GREEN after the existing
  manifest writer regenerated the source/artifact binding.
- Direct tracked-WASM shared-change runner passed.  The asynchronous current
  public-rejection parity process exited after one run, but its parent output
  was not recoverable; it was not rerun.
- Mutation M3 copied the exact pre-target artifact into the tracked location:
  the existing checker was RED for `wasm_sha256` and `wasm_size`; exact copy
  from the official build output restored SHA-256
  `ffc82a6e97ba5a3af72b090f222f7f808d982d63c4297bf075d16cfd334a9f83`
  and GREEN.
- Mutation M4 replaced only `source_tree_sha256` with zeros: the existing
  checker was RED; byte-exact restored manifest SHA-256 is
  `748ca10637ee2116310a27736c49f26029c6180ef81deed77e73283f1cfed85e` and
  the checker was GREEN.

## Gates

- `python tests/run_ddn_cli_wasm_freshness_check.py`: PASS after restore.
- `node tests/ddn_cli_wasm_post_wasm_shared_changes_runner.mjs`: PASS.
- `node --check solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.js`: PASS.
- `git diff --check`: PASS before product fixed commit.

## Review request and nonclaims

This is a `PRODUCT_FIXED_PENDING_REVIEW` target for the existing independent
reviewer.  It proves only current-source-to-tracked-artifact freshness and
the listed runtime gate.  It does not claim full Native/WASM/Workbench parity,
browser behavior, V1 readiness, release readiness, or Human approval.
