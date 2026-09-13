# BOGAE-PROD-05 raw-source Workbench frontdoor handoff

- Product target: `28e3bb0ee3a450dc21da2511a790385eaaaa8694`
- Tree: `e145d10c84736e54dc18f14d30774b9d46e1b100`
- Parent: `c910e8d7482f923cf6ce572958de716f70b64666`
- Scope: `solutions/seamgrim_ui_mvp/ui/runtime/runtime_bridge.js`,
  `tests/seamgrim_workbench_runtime_bridge_t1_runner.mjs`

## Implemented behavior

`runSummaryWithSourceProfile` now passes `sourceText` to the existing shared
WASM export without JavaScript reconstruction.  The existing runtime-bridge
runner binds a newline-preserving V25 source string and explicit
`v1-core-v25` profile to the exact WASM invocation, and verifies a missing
shared run-summary export rejects with the existing
`E_WASM_RUN_SUMMARY_REQUIRED` failure instead of producing local success.

## Evidence

- `node tests/seamgrim_workbench_runtime_bridge_t1_runner.mjs` — PASS.
- `node tests/seamgrim_workbench_source_analysis_t4_runner.mjs` — PASS.
- `node --check solutions/seamgrim_ui_mvp/ui/runtime/runtime_bridge.js` — PASS.
- `cargo check -p ddonirang-tool --lib --features wasm --offline` with
  `CARGO_TARGET_DIR=I:\\home\\urihanl\\ddn\\codex\\build\\target-bogae-prod04-prod05` — PASS.
- `git diff --check` — PASS before product commit.

## Mutation and exact restore

Fixed runtime-bridge blob: `f91e663e3be9ffca26f5c706ed620000c109a176`.
Fixed SHA-256:
`f80241dcfae381f7d7e6522e4ba8faaf793b64c60541fb035dd20c2fc15c2703`.

1. `sourceText.trim()` caused the raw-source assertion to RED by removing the
   terminal LF; exact restore returned the runner to GREEN.
2. Replacing the required WASM export with an empty-success fallback caused
   the missing-export rejection assertion to RED; exact restore returned GREEN.
3. Dropping the source-profile argument caused the profile assertion to RED;
   exact restore returned GREEN.

## Nonclaims and review

`BOGAE-PROD-05 = PRODUCT_FIXED_PENDING_REVIEW`. No independent verdict,
tracked-WASM rematerialization/freshness claim, browser PASS, public wire
change, SSOT/SPEC transition, release, or V1 readiness claim is made.

The existing browser runner could not start because package `playwright` is
not installed in this checkout. No package installation or external download
was attempted.
