# Bogae PROD-07 source-profile identity handoff

- Product/tree/parent: `1afb12512cedaeb2d0b39d122e6323a2a1778e04` /
  `0072fb51b271b4f414dd90053ad4831530458211` /
  `f50637e6070a0a4c0b44e3d8156c8d66a8baa13f`.
- Scope: existing Workbench source-readiness projection and its existing
  source-readiness/T4 runners only.

An `ACCEPTED` shared snapshot with a mismatched profile identity previously
became ready. The projection now requires exact equality with the already
declared `v1-core-v25` profile and returns the existing unavailable typed
failure model before it can authorize readiness. No source rewrite, fallback,
wire field, language rule, or WASM ABI was added.

Evidence:

- Pre-change product RED: `wrong-profile` projected as `ready=true`,
  `blocked=false`.
- M1 removed the profile guard: the existing contract runner was RED at
  `wrong source profile must not authorize readiness`.
- M2 made the expected profile self-declared by the snapshot: the same
  assertion was RED.
- M3 reduced equality to prefix matching: the contract runner was RED at
  `profile prefixes must not become aliases`.
- Exact restored source: SHA-256
  `06b370fe8a412a752e31edabda87c0348bbfde6a709b519d504be2b8e4aadea5`,
  blob `b37964c81497bebabe673dae18fe9521940a2989`.
- GREEN: `node tests/source_readiness_contract_runner.mjs`,
  `node tests/seamgrim_workbench_source_analysis_t4_runner.mjs`,
  `node tests/seamgrim_workbench_runtime_bridge_t1_runner.mjs`, JS syntax,
  and `git diff --check`.

This target is `PRODUCT_FIXED_PENDING_REVIEW`. It does not close the broader
PROD-07 typed input/profile/receipt/browser matrix, nor V1 readiness, release,
or Human gates.

READY_FOR_FIXED_TARGET_INDEPENDENT_REVIEW=YES
