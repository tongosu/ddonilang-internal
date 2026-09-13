# DDN V1 P0 WorkCost registry and dual-name CLI

- Authority read-only: internal SSOT v25.55.0 / RD-001~557; public Language SPEC v0.6.0.
- Product fixed sequence: `01e538a3` -> `0871bb62` -> `3e46eca7`, merge count 0.
- Changed product paths: `tool/src/work_cost.rs`, `tool/Cargo.toml`, `scripts/build_windows_x64_public_candidate.ps1`, `tool/src/bin/ddonirang.rs`, `tests/run_v1_core_supported_ingress_w1.py`.
- User workflow: the existing V25 supported run works again without a stale WorkCost-registry failure through either official native name. The two names share one implementation authority.
- Reused tests: WorkCost exact-total, existing supported-ingress runner, native/WASM payload test. New test artifacts: 0. Meta tests: 0.
- Mutation: stale ledger hash RED then exact restore GREEN; missing Korean bin target RED then exact restore GREEN; residue 0.
- Windows target builds contain both release executables; artifact projection retains only the English artifact, so P5 dual-artifact collection remains OPEN.
- Protected four pre-existing untracked session deltas remain unstaged and byte-preserved.
- Next safe slice: P0 required teul dependency-zero audit/convergence, or fix the P5 artifact projection with exact ownership.
