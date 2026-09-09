# 2026-09-01 DDN V1 CLI Geoul bundle reader 공유 권위 W58

- goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` ACTIVE
- authority: internal v25.47.0 / RD-001~543, public SPEC v0.6.0
- baseline/fixed/tree: `ed59294f...` / `8ab4a69d...` / `4fe396d4...`
- files: `tool/src/geoul_bundle.rs`, `tool/src/lib.rs`, teul Geoul re-export/writer adapter
- behavior: Geoul bundle header/frame/index reader와 audit hash를 shared typed authority로 이동; malformed index fail-closed; existing binary format와 writer behavior 보존
- tests: shared 2/2, existing teul Geoul 2/2, existing run consumer 1/1, teul cargo check PASS
- regression: teul 1045 PASS + same historical 9 FAIL; slice drift 0
- mutation: malformed-index guard bypass RED exit 101; exact restore SHA-256 `677faeca5ada67a91d9c109378a726295c21d6838a38a9cf58b1d2a140428fa7`; GREEN 2/2; residue 0
- new pack/runner/framework/meta-test/reviewer/worktree/branch: 0
- protected four untracked custody files: unchanged and unstaged
- SSOT/SPEC/WASM/UI/public membership change: 0
- detail gap preserved: writer overwrite/directory atomic replacement policy and private State encoding remain outside W58
- status: `IMPLEMENTED_PENDING_REVIEW`; broad closure and release nonclaims preserved
