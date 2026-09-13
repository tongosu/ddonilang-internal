# P5 W105 current-source Windows A/B successor W106 handoff

## Scope and authority

- Live internal authority: v25.49.0 / RD-001~543.
- Public Language SPEC: v0.6.0.
- Successor impact: `ADDITIVE_CUSTODY_ONLY`; v25.49 adds no semantic RD and does not invalidate the bounded CLI, projection, or project-run contract used here.
- Baseline/handoff: `ce877bf511b598c0b82348a005a8250c298098c0` / tree `8fa764a3ffac628b684abe4a7005886abba38c1d`.
- Product fixed: `19df6b916d68938fa5c45828a6b856c5ddd97598` / tree `06d767c5b89a3c64c29e3e826f463e6226bb683f`.
- Direct parent: `ce877bf511b598c0b82348a005a8250c298098c0`; merge count `0`.
- Fixed diff: only `PUBLIC_PROJECTION_V25_35_WINDOWS_X64_PATH_CLEAN_MANIFEST.detjson`, pinning `source_commit` to the exact W105 handoff.

## Current-source WASM candidate and projection

- Official WASM candidate source commit/tree: `ce877bf511b598c0b82348a005a8250c298098c0` / `8fa764a3ffac628b684abe4a7005886abba38c1d`.
- Candidate semantic identity: `sha256:40c3caf1a940881f127e53832f9741bc49608fcab5277eb860ddeec4269eff8d`.
- Candidate receipt: 2,470 bytes / SHA-256 `3c4d165c35a103f2fd086d198e075a5230e7f405b09770e127814b6c6c1713ba`.
- Candidate WASM: 5,576,576 bytes / SHA-256 `00f574305c6d10b77b7a262e02d9cec677c4e79015d9ddd603eaf30e13abca11`.
- Candidate forbidden path counts: internal/official/private/unknown `0/0/0/0`.
- Projection file count: `224`; teul-named projection paths: `0`.
- Projection before identity: `sha256:ea8ffd5981585cfafc5e4fe10fddeb8383dc2cce3a6f122a40f6ddc1821b11bc`.
- Projection after identity: `sha256:87952fe1ac9ddfced0fd80a2bcdb758102c7aeb2e8e7d6479131e25abba3d277`.
- Projection manifest identity: `sha256:6e8051dbdaee91ec339d96ccfec8a4440f04a92784804287a5fd8d0f6f5352a3`.
- Validation receipt identity: `sha256:4fdb0cd3f6318e0a6c0018dc0dfbae69770aa4f98188dcff9b9e8a27e21420b2`.
- Public membership remains `false`; this is a path-clean candidate, not publication authorization.

## Windows x64 A/B reproducibility

- Offline official candidate builds: `2/2 PASS`.
- Artifact: `ddonirang.exe`.
- A/B bytes: `7,043,584 / 7,043,584`.
- A/B SHA-256: `fda69b5ff735cd73e63fab543daa361ae0471caa25d3e85824e23534f51fbc84`.
- A/B byte equality: `true`.
- PE stack reserve A/B: `16,777,216 / 16,777,216`.
- Forbidden path occurrences A/B: `0/0`.
- Startup/help: `PASS`.
- Cargo PDB filename-collision and dead-code warnings were non-fatal and do not change product or release status.

## Product-facing project-run workflow

- Existing external fixture: `pack/ddn_local_project_graph_v1/fixtures/project_run_physics_v1.json`.
- Fixture: 3,234 bytes / SHA-256 `4df16386dbd388e044c334da0c777aa02e45052eff635de5f9769dba6f2dd5ec`.
- Semantic identity: `ddn.project-run.v1`.
- Options: target `앱`, graph/lock inspection, atomic `--out`.
- A/B exit: `0/0`.
- A/B result bytes: `16,488 / 16,488`.
- A/B result SHA-256: `f9c2e36f4117d4a523438c5ab3a88948c769fc4a4b48c99e9dd6495bd7f29578`.
- A/B result byte equality: `true`.
- Positional start plus `--virtual`: exit `2`, `E_CLI_OPTION_CONFLICT`.
- Conflict artifact and partial publish: `0/0`.

## Reused verification, risk evidence, and anti-meta

- Existing projection/remap/validator tests: `63/63 PASS`.
- Existing official WASM builder, projection tool, Windows candidate builder, and project-run fixture were reused.
- New tests/packs/runners/meta-tests: `0/0/0/0`.
- Risk evidence reused: W105 started from the concrete tracked-WASM embedded-path RED `115`, then official refresh produced exact path counts `0/0/0/0`; W106 revalidated the corrected current-source candidate and added no report-field mutation.
- Product source, test, pack, SSOT, SPEC, and visible UI diff in W106: `0`.
- Protected four untracked custody files remain byte-untouched and unstaged.

## Review and nonclaims

- The prior P5 fixed-target review `bc84d81d4faa55974975bdb7ec60cb18d9a7ebda` is an ancestor and remains `PASS_TARGET_BOUND` with blocking finding `0`; it is not inherited as a review of W104-W106.
- Review bundle target: W102-W106 coherent CLI authority/path-clean current-source Windows milestone.
- New review task/worktree/branch: `0/0/0`; management may reuse the existing rolling reviewer handle.
- Status: `P5_W105_CURRENT_SOURCE_WINDOWS_AB_SUCCESSOR_W106_IMPLEMENTED_UNDER_REVIEW`.

This handoff does not claim P5/P6/V1 closure, exact public command membership,
readiness, package/publication/release, public executable naming, physical
`tools/teul-cli` deletion, legal/signing/distribution approval, activation,
Owner Human Smoke PASS, or Human PASS.
