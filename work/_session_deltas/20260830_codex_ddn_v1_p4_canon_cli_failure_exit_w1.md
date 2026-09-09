# 2026-08-30 DDN V1 P4 canon CLI failure exit W1

- Session/role: `DDN V1제품마감Codex` / single product writer
- Authority: internal `v25.35.0 / RD-001~490`; public SPEC `v0.6.0`
- Baseline: `7a90710ea74c4e50d3313ba2252b3aa251199540`
- Fixed: `e748dc3b7a7955ea58e4250d6567d4446aac7652`
- Fixed tree: `17aad3916fc46642296f5def67fbc04b21bdf959`
- Product path: `tool/src/main.rs`
- RED: canon missing-input, invalid-bridge and extra-argument cases each exit 0.
- GREEN: same cases exit 2; valid canonical output exit 0.
- Reused tests: canon 82/82, preprocess 58/58, authority checker PASS, binary build/diff-check PASS.
- New test/runner/pack/framework/meta-test: 0/0/0/0/0.
- P2 gate: exact durable revision schema/wire/hash/CAS/DB remains Owner-open; product mutation 0.
- Review: coherent P4 rolling bundle pending; new reviewer/worktree 0.
- Nonclaims: no P2/P4/P5/V1 closure, membership/readiness, release, activation or Human PASS.
