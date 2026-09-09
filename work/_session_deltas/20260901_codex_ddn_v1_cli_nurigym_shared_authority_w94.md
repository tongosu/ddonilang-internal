# 2026-09-01 DDN V1 CLI NuriGym shared authority W94

- Status: `IMPLEMENTED_UNDER_REVIEW`
- Goal: existing `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` remains active.
- Authority: internal SSOT v25.49.0 / RD-001~543; public SPEC v0.6.0; both read-only.
- Baseline: `798ca52d6ca882664c326497b9144bd3d581d336`.
- Product fixed: `7532393a5aa99b112caa89459acb8d88d515a3ff` / tree `64f67587594a7fe107719fea0a7bbbd9cd0689b5`.
- Product behavior: NuriGym spec/view/episode orchestration moved to shared host-side `tool`; teul is a one-line adapter.
- Verification: shared 12/12, actual CLI PASS and repeat artifact equality, priority pack PASS, wasm32 PASS, freshness PASS.
- Mutation: priority-order inversion RED; stable SHA `00c042872b0e16f62a9df3970ecc9c25bfa8b2f05a9528b2e02575bd830a12b1` exact restore; 12/12 GREEN; residue 0.
- Known unrelated/stale evidence: bandit two golden hashes, action-pipeline hash, public-schema Windows decode; no promotion.
- New pack/runner/meta-test/reviewer/worktree/branch: 0.
- Protected untracked 20260829 custody files: preserved and unstaged.
- Next safe task: inspect another private-core-free teul internal/deferred workflow; keep `bogae_web` frozen until shared Bogae type/value convergence is coherent.
- Nonclaims: no V1 membership/readiness/release/Human PASS, no physical teul retirement.
