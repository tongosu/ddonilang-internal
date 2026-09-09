# DDN V1 legacy PR-A L06 current producer correction

- Session role: product single writer; no new task, worktree, branch, runner, pack, or reviewer.
- Live authority checked read-only: v25.67.0 / RD-001~587, public SPEC v0.6.0.
- C1 current clean-break was treated as current; docs/ssot and public SPEC were not modified.
- L11 scan of `lang/src/currentline.rs`, `lang/src/normalizer.rs`, and `tool/src/preprocess.rs` found no producer. The actual current producer selected under the same PR-A boundary is V25 parameterized single-return callable normalization to retired `되돌림`.
- Product fixed `32369cc495d262caa899c25d172df46c58d9b39a` changes only `lang/src/normalizer.rs`; parent `44a38719b44ad71fb3c87505e0e980769a1b9811`.
- Evidence: initial focused RED; focused GREEN; normalizer 17/17; cargo check; M1/M2 RED -> exact restore -> GREEN; diff check.
- Dedicated local build output `build/target-l11-producer-pr-a` was used to avoid an unrelated shared Cargo/LSP build lock. It is untracked build output only; no foreign process was stopped or modified.
- Foreign tracked WIP remained unstaged and untouched. No SSOT/SPEC change, push, release, or closure claim.
