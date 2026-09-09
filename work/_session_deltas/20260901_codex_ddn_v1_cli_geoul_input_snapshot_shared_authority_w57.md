# 2026-09-01 DDN V1 CLI Geoul InputSnapshot 공유 권위 W57

- goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` ACTIVE
- authority: internal v25.47.0 / RD-001~543, public SPEC v0.6.0
- baseline/fixed/tree: `2299b0d0...` / `7fcea347...` / `998ae7f7...`
- files: `tool/src/geoul_snapshot.rs`, `tool/src/lib.rs`, teul Geoul re-export adapter
- behavior: Geoul snapshot/source-provenance codec moved to shared typed authority; source-count mismatch fail-closed; existing legacy format preserved
- tests: shared 3/3, existing teul Geoul 2/2, existing run consumer 1/1, teul cargo check PASS
- regressions: tool 569 PASS + unrelated 3 FAIL; teul 1045 PASS + same historical 9 FAIL; slice drift 0
- mutation: source-count equality bypass RED exit 101; exact restore SHA-256 `d7175ad7dd2c7bd47487ea369d051c289d7c19120d205df9884921b607141463`; GREEN 3/3; residue 0
- new pack/runner/framework/meta-test/reviewer/worktree/branch: 0
- protected four untracked custody files: unchanged and unstaged
- SSOT/SPEC/WASM/UI/public membership change: 0
- status: `IMPLEMENTED_PENDING_REVIEW`; broad closure and release nonclaims preserved
