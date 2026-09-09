# 2026-08-30 DDN V1 P5 current-head artifact rebase

- Authority: internal SSOT v25.35.0 / RD-001~490; public Language SPEC v0.6.0.
- Product source fixed identity: `7ed20696f93eafa4fe3cb4b85c8a6102e6d57f04` / tree `76aaafd3338ca2c8388cd2d06263553ce6d26c9a`.
- Evidence fixed commit: `9c6366abb2c40a2cc1b3040b5de2ff6434582b65`, direct parent `7ed20696...`, exactly the existing P5 projection manifest source identity.
- Reused the official candidate-only WASM build, public projection, validator, remap substitution and Windows x64 build entrypoints. New runner/pack/checker/framework/meta-test count is zero.
- Current-head WASM candidate: 5,559,604 bytes / `017e43e8a6a3fdb5ef383629ed4e9394efcc6ba37eeda1e2662f2eafb4e66eab`; semantic identity `sha256:e5b4e19512cc9fccbf34640eaaa14d4c542c637d8ba3ab5b3bb487c296144fea`; path counts all zero; tracked WASM write zero.
- Public projection: 898 files; after-tree `sha256:f55926eefe27129d1e86933c2443796b288ef51bacd54a67a6e92caf782e9a43`; validation receipt `sha256:7af02341e9634af4ac4cc8bf3d4b2228b8fa951f369c3e1c373d5813d6bc2d45`; four required release roles present.
- Windows A/B both PASS: startup 2/2 each, forbidden path count zero, 16 MiB PE stack reserve 2/2 each. `ddonirang-tool.exe` A==B 8,540,160 bytes / `9563758c30f14b0dc88d18e0a94f34c5aa3b79faad8b718b514a966acd4c61fd`; `teul-cli.exe` A==B 21,862,400 bytes / `73a56b5369feebafb8092d6f9d17564a4f80df1a4ab1a4b3011bfeda2fd6ffa0`.
- Existing projection/validator/remap tests: 61/61 PASS. No receipt/hash meta-tamper suite was added.
- Product source/test/pack/tracked-WASM/UI/SSOT/SPEC diff is zero. The fixed diff is evidence/custody only; the handoff is docs-only.
- Review bundle target: coherent P4 plus current-head P5 candidate on the existing management-owned rolling reviewer. Writer created no reviewer, worktree or branch.
- Status remains `P5_CURRENT_HEAD_CANDIDATE_FIXED_UNDER_REVIEW`. Package/installer format, SBOM/notices, rights/license, signing, distribution, P5 closure, release and Human gates remain open.
