# Bogae PROD-07 raw-source run-summary binding handoff

- Product/tree/parent: `d61b3436f514b0eb709fa216fde8e944407a12e0` /
  `0ffe9393d7959dd815fe1d1632aecba6dc177dcf` /
  `b38c823debfd09beb17eeeae124a4f77b18ace83`.
- Scope: existing Workbench source-readiness helper, `workbench.js`, and the
  existing source-readiness contract runner.

Workbench now computes the SHA-256 of the raw source it supplies to the shared
RuntimeBridge and accepts a run summary only when all existing fields bind
exactly: source profile, execution-envelope `source_bytes_sha256`, committed
state hash, and WorkCost receipt. A mismatch fails before the summary, receipt,
or success data is stored on the run. No source rewrite, local retry, ABI,
wire field, or semantic owner was added.

Mutations were all actual contract-runner RED followed by exact restore and
GREEN:

- omit envelope source-hash comparison → `shared run summary source mismatch
  must fail closed`;
- replace exact profile equality with prefix matching → `shared run summary
  profile mismatch must fail closed`;
- allow missing receipt → `shared run summary receipt mismatch must fail
  closed`.

Restored validator SHA-256:
`f9b3b3797bf68837bd97dcc1d880680ab5e4db5f71839c380a05b67d18c0d6a2`;
blob `49f8cc1f53eae88c9440f223e5a2ecb5bfcabcf7`.

GREEN gates: source-readiness contract, Workbench source-analysis T4, runtime
bridge T1, JS syntax, and diff check. The existing Playwright browser vertical
could not start because this worktree lacks the `playwright` package; browser
behavior is therefore `ENVIRONMENT_BLOCKED`, not claimed PASS.

This is `PRODUCT_FIXED_PENDING_REVIEW`. It closes neither the entire PROD-07
InputSnapshot matrix nor broader PROD-06 workspace/world hash coverage.

READY_FOR_FIXED_TARGET_INDEPENDENT_REVIEW=YES
