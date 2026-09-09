# 2026-09-01 DDN V1 CLI scan / WASM current-source authority W45

- Persistent goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` remains active.
- Branch/worktree: existing single writer reused; no new branch/worktree/task/reviewer.
- Authority: v25.47.0 / RD-001~543; public SPEC v0.6.0; SSOT/SPEC change 0.
- Review `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf` was confirmed already bound as an ancestor.
- Fixed: `1800aa6378f46fe1a2087fa82de5a99d455f13b5`, tree `9d85e301eed58554b265db56b05d427e279ed917`, direct parent `97e7d2e100550a1ae066a7aa938e6847ed6acdb6`.
- Product behavior: teul `scan` delegates to one shared typed tool owner; deterministic warning ordering; current-source WASM build restored by target-gating native-only deterministic-debug artifact I/O.
- Tests: scan 2/2, teul scan parser 3/3, scan repeats 3, deterministic-debug 17/17, tool lib 562 PASS + same 2 environment failures, tracked-WASM runner PASS, direct WASM debug repeat PASS, freshness PASS.
- Mutation: reverse ordering RED exit 101 -> byte-exact restore `e26805d1029df2ad7c13044b8a9c64290169505400ec9776c17578803ee55b92` -> GREEN 2/2; residue 0.
- WASM: 5,575,187 bytes, SHA-256 `62555c83144735bc9bb231250fe4244cb4ddc4c0d4b36f844b264f18ecb227f5`; manifest source inventory 130; freshness-only custody.
- Anti-meta: new pack/runner/review/worktree/branch 0; new test artifact 0; colocated Rust tests 2; meta-test 0.
- Separate frozen slice: replay convergence requires exact expanded ownership and was not modified.
- Nonclaims: no broad P0~P6, CLI membership, teul physical retirement, PathIR/Proof closure, V1 readiness/release/activation/Human PASS claim.
