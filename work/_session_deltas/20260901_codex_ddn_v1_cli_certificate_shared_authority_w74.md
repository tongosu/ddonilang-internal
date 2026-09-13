# 2026-09-01 DDN V1 CLI certificate shared authority W74

- goal: existing `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1`, ACTIVE
- authority: internal v25.47.0/RD-001~543; public SPEC v0.6.0
- baseline: `5033fb9eb7fad7a40bac987d1b8dcd88e0ce0df7`
- product fixed: `146ac3d46b536967e4c34e02f67bcd54263690a4`
- tree: `cf1e7dfd6c5a6c4eab38fa085d539a978017d6df`
- product files: `tool/src/cert_workflow.rs`, `tool/src/lib.rs`, `tools/teul-cli/src/cli/cert.rs`
- product change: moved 8 certificate/proof-certificate functions from private teul ownership into shared host `tool` authority; retained teul adapter has private function count 0
- user workflow: existing keygen/sign/verify and proof-certificate verify dispatch now consume the shared authority without changing spelling or wire
- fixed tests: tool check PASS; teul check PASS; W95 cert pack 2/2 PASS; W73 deterministic output replay PASS
- historical proof bundle selftest: stopped at pre-existing `E_SHARED_RUNTIME_OPTION_UNSUPPORTED` in legacy run prerequisite; not claimed PASS
- mutation: private authority reintroduction RED count1 -> adapter exact SHA restore -> GREEN count0 and W95 2/2; residue0
- new pack/runner/meta-test/reviewer/worktree/branch: 0/0/0/0/0/0
- protected four untracked custody files: byte-identical and unstaged
- docs/ssot, public SPEC, tracked WASM, visible UI, membership and release transition: 0
- review: no new dispatch; queue for the existing rolling reviewer as part of the next coherent CLI/teul milestone
- nonclaims: public PathIR contract, whole C0~C8/P0~P6/V1 closure, teul physical retirement, release and Human PASS remain OPEN
