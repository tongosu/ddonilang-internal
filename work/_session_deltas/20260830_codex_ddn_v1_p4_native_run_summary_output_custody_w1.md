# 2026-08-30 DDN V1 P4 native run-summary output custody W1

- Authority: internal `v25.35.0 / RD-001~490`; public SPEC `v0.6.0`.
- Baseline: `861bcfe4c924c9411ed2ca613dfec58bb0e64ad8`.
- Fixed: `fa00f9ce0f2d2dae476aef00ec61466aa084c3b2` / tree `f65b3abdd8669bb845eaca974247c091e4a37971`.
- Exact product path: `tool/src/main.rs`.
- RED: input-as-output and `--madi 0` both exited 0; the first replaced the DDN source and the second created output.
- GREEN: same path and Windows hard-link alias exit 2 with byte-identical source; zero count exits 2 with no output; valid output exits 0; missing source remains exit 1.
- Determinism: two valid option forms emitted 46,037 identical bytes / SHA-256 `eb3e6ea839ed303dab22d8d4cfec44d97436defe19a021c479b4e4f90095ca28`.
- Tests: offline build PASS; direct source/output/exit checks PASS; bin regression 406 PASS + 2 isolated-worktree `docs/ssot` environment failures; diff check PASS.
- New test/runner/pack/checker/framework/meta-test: `0/0/0/0/0/0`.
- Review: append to the existing coherent rolling P4 milestone; writer created reviewer/worktree/branch 0.
- Nonclaims: no broad P1~P5/V1 closure, stable receipt wire, membership/readiness, release, activation or Human PASS.
