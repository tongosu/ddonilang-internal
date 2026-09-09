# 2026-08-30 DDN V1 P4 native ingress CLI failure exit W1

- Authority: internal `v25.35.0 / RD-001~490`; public SPEC `v0.6.0`.
- Baseline: `23a73c2737d41245eab10017ea4a523518d31f9b`.
- Fixed: `d6f5dae4363063b03654b865fa022c0e7fdf5cff` / tree `0719407287981300fa2663c960ab5a1d96bdc7d0`.
- Exact product path: `tool/src/main.rs`.
- RED: missing `run-summary --madi` and `--summary-json` values each exited 0.
- GREEN: missing/invalid/unknown/extra invocation cases exit 2; actual product failure exits 1; valid summary exits 0.
- Determinism: two valid option forms emitted identical SHA-256 `828429fced1062c468abc946c56121dda71dcb5a26f5811545e582e95f5b40f9`.
- Tests: offline build PASS; direct negative 5/5; positive and product-failure classification PASS; bin regression 406 PASS + 2 isolated-checkout `docs/ssot` environment failures.
- New test/runner/pack/checker/framework/meta-test: `0/0/0/0/0/0`.
- VC15 audit: current packs are `EVIDENCE_REBASE_REQUIRED`; English dialect activation is `CONFLICT_OR_OWNER_DECISION`; product change 0.
- Review: existing rolling P4 bundle only; writer created task/worktree/branch 0.
- Nonclaims: no broad P1~P5/V1 closure, membership/readiness, release, activation or Human PASS.
