# Fixed64 non-finite formula result handoff — 2026-09-11

## Immutable product target

- Product: `0c60c79c306196ab28c9b931aeba6ae0fcab5996`
- Tree: `0530ee3c2951d30c903825b21358eee3d2859751`
- Parent: `a67455cb5d1014098b7dd08d1e611f5f3314af8c`
- Product paths:
  - `tool/src/ddn_runtime.rs`
  - `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
  - `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

## Claim

Current formula and runtime math call paths no longer convert a host non-finite
result into Fixed64 zero or a saturated success value. `asin(2)`, `acos(2)`,
`acosh(0)`, and `atanh(1)` now fail through the existing typed
`E_RUNTIME_ARITH_OVERFLOW` path before a numeric result can publish. Finite
formula behavior is retained (`sin(0) == 0`). This is a non-finite result
firewall only; it does not introduce an exact transcendental implementation.

## Evidence

- Baseline RED: `fixed64_formula_nonfinite_host_results_must_not_publish_as_numbers`
  observed `asin(2)` returning raw zero.
- Fixed focused test: PASS, including the finite `sin(0)` positive case.
- Official tracked WASM build:
  `scripts/build_wasm_tool.ps1 -Profile release -Target web`.
- `python tests/run_ddn_cli_wasm_freshness_check.py`: PASS.
- `cargo check -p ddonirang-tool --offline`: PASS.
- `git diff --check`: PASS before product commit.

The one full `cargo test -p ddonirang-tool --offline` run had 669 passing and
the same five unrelated failures already present in this isolated worktree:
numeric-calculus one-ULP expectation, BOM/project parsing, profile canon, and
two ai_prompt tests requiring absent `docs/ssot`.

## Mutations

Fixed source before the final restored test addition: blob
`be940d05b7cb4b8585081d03bdc705225486919f`, SHA-256
`77CBDAC8D1C0BD36B1710D616E546447D1A9811C9363A1F09C2BFF58D1468FB6`.

1. Removed `is_finite()` admission guard: focused non-finite negative RED.
2. Replaced typed overflow with `Fixed64::ZERO`: focused negative RED.

Both changes were restored byte-exactly before the final positive assertion;
the final source blob is `ee16b88d7d7fe48c5b020174774d3588b3799947`, SHA-256
`E3AD167916C324C37FF4A243E3283AC4A5C34CDAC47F95EEF432CDFBF485A9EE`.

## Review request and nonclaims

Review the exact product target for non-finite host-result admission, existing
typed runtime overflow propagation, focused positive/negative behavior, and
tracked-WASM freshness. This target does not certify exact finite
transcendental arithmetic, all host-float call sites, V1 readiness, release,
or Human PASS.
