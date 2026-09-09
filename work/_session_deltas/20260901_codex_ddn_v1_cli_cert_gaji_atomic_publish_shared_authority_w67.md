# 2026-09-01 DDN V1 CLI cert/gaji atomic publication W67

- Goal: existing `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1`, status ACTIVE.
- Authority: internal v25.47.0/RD-001~543; public SPEC v0.6.0; SSOT/SPEC mutation 0.
- Baseline: `e75638f2b79c5d0bf5ee18d8727443ecdb6d4860`.
- Fixed: `91d07847e5b585d7fbfa99e94d123bd9c077dcd5`, tree `18832ab22c60ad34fd35b219641c875ff5192b53`, direct parent, merge 0.
- Product paths: `tools/teul-cli/src/cli/cert.rs`, `tools/teul-cli/src/cli/gaji.rs` only.
- User-visible correction: cert keygen publishes private/public keys as one shared atomic artifact set; cert JSON outputs and `gaji lock` use the shared atomic writer.
- Actual RED: invalid public-key target caused baseline private predecessor hash `de3de6...` to become `fb3173...` before overall failure.
- Fixed GREEN: same fault fails closed and preserves `de3de6...`; temporary residue 0.
- Verification: offline product build PASS; cert keygen/sign/verify PASS and 3/3 repeat identity; gaji lock PASS and repeat identity; gaji tests 47/47; shared writer tests 5/5; diff-check PASS.
- Existing full test-binary gate: 13 unrelated dual-core type mismatches; no whole-suite PASS claim.
- New pack/runner/test framework/meta-test/reviewer/worktree/branch: 0.
- Protected pre-existing untracked custody: four 20260829 session deltas preserved byte-for-byte and unstaged.
- Open: `gaji vendor` directory transaction, public test/view/repl membership, public PathIR wire, VC17 landing, physical teul retirement, P5/P6/release/Human gates.

