# Fixed64 finite host ingress — product handoff

## Fixed target

- Product commit: `2ed5acb9444aa8e39154982fc65f96b2248c6298`
- Product tree: `b59a574b1e539201e4440a490a3dab0c6bac2e8e`
- Parent: `1962dc8f96dc3270cdd56602a7431f18ddf2d5e7`
- Claim: finite host `f64` results entering the current runtime Fixed64 boundary
  round to Q31.32 with ties-to-even rather than truncating toward zero.

## Product paths

- `tool/src/ddn_runtime.rs`
- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

No SSOT, public SPEC, public wire, new numeric identity, CLI surface, or
fallback path changed.

## Behavior and evidence

- The shared `fixed64_from_host_f64_checked` runtime boundary now rounds the
  scaled finite value before its existing checked range admission.
- The half-ULP test covers positive and negative 0.5/1.5 raw ties and proves
  the even-neighbor result.
- The existing numeric calculus workflow now records the resulting two
  changed Q31.32 raw values.
- Tracked WASM was rebuilt by the existing official builder and its existing
  freshness manifest was regenerated.

## Verification

- `cargo test -p ddonirang-tool fixed64_ --lib --offline` — PASS (22 tests).
- `cargo test -p ddonirang-tool numeric_calculus_v1_builtins_return_value_error_method --lib --offline` — PASS.
- `cargo check -p ddonirang-tool --offline --quiet` — PASS.
- `python tests/run_ddn_cli_wasm_freshness_check.py` — PASS.
- `cargo test -p ddonirang-tool --lib --offline` — 673 PASS; four inherited
  failures outside this target: two `ai_prompt` tests require absent
  `docs/ssot` in this isolated worktree, plus pre-existing
  `project_authoring` BOM and `runtime_surface` legacy-profile failures.
- `git diff --check` — PASS before the product commit.

## Mutation evidence

Fixed runtime source: SHA-256
`CF3974399187718759282D9CE34C2B236F6E5D81C73FD29EE279ED54C4B24A80`,
Git blob `40471bc9bff5512b8b106b6b7ac357a4c7cb0d7d`.

1. M1 restored truncation: the half-ULP tie test became RED because +1.5 raw
   produced raw 1 rather than the required even raw 2. Exact source restore
   returned the focused Fixed64 suite to GREEN.
2. M2 removed the finite check from the rounded-value guard: the existing
   non-finite formula test became RED because NaN reached a successful numeric
   result. Exact source restore returned the focused Fixed64 suite to GREEN.
3. M3 replaced the manifest source-tree hash: the existing freshness checker
   became RED with `source_tree_sha256 mismatch`; regeneration through the
   existing checker restored the exact manifest blob
   `8f1b007e2c14be00b1f5c33f9f563f8980b726f0` and GREEN freshness.

Tracked artifact SHA-256:
`313E74131A4769B39CB99C309BA0A3314B0E870D1C9EE0C2D95AB17A4164358C`.
Manifest SHA-256:
`08F2159E4133004CB48FEA29EF30AE7D6DFE5478459B7546DA66AC6ABA750501`.

## Review packet

Review this exact product target only. Primary review questions are whether
the shared host-result ingress is current-reachable for formula/calculus,
whether range admission remains fail-closed after rounding, and whether the
tracked artifact and freshness manifest bind to the fixed source tree.

This handoff is `PRODUCT_FIXED_PENDING_REVIEW`; it does not claim independent
PASS, V1 readiness, release, Human PASS, full CLI three-name execution parity,
or full dynamic WASM formula-result parity.
