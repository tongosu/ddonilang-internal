# 2026-09-01 DDN V1 CLI patch artifact atomic authority W71

- Persistent goal remains ACTIVE; P5 `bc84d81d...` PASS removes the stale reviewer-handle/whole-goal blocker claim.
- Live authority: internal v25.47.0 / RD-001~543; public SPEC v0.6.0.
- Baseline `9073b6a43d164f23ed496a7aed834f0085bd3ff5`.
- Fixed `777e4b1304c3c46981a854e04bdf54c0f625d12b`, tree `7492330ea3c538f7088feea4b0073ddfd9d7116f`.
- Product diff: `tools/teul-cli/src/cli/patch.rs` only.
- `patch propose`, `patch approve`, and multi-file `patch apply` now consume shared atomic artifact authority.
- Baseline late-target fault published `a.ddn`; fixed fault publishes no patch output.
- Normal out-of-place and in-place two-file applies PASS; repeat hashes exact; residue0.
- Existing shared artifact writer tests 5/5 PASS.
- Sequential-write mutation RED; exact restore SHA-256 `2dc2f7d61ffb73addc735b3d3044b8c08626ab5fe63c28ccb614407f17722b9b`; restore GREEN.
- Existing `age1_patch_approval` apply remains fail-closed at pre-existing canon mismatch and was not promoted.
- Generic runner-created golden diffs were excluded and exactly restored; protected four-file untracked custody unchanged.
- New pack/runner/meta-test/reviewer/worktree/branch: 0.
- SPEC history, PathIR public contract, public test/view/repl membership and VC17 exact landing remain slice-frozen, not whole-goal blockers.
- Whole CLI/teul retirement, P5/P6/V1 readiness/release/Human PASS remain OPEN.
