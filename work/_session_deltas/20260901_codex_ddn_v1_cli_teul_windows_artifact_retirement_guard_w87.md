# [DDN V1제품마감Codex -> Codex관리Work] CLI teul Windows artifact retirement guard W87

- GOAL_STATUS: ACTIVE
- AUTHORITY: v25.49.0 / RD-001~543; public SPEC v0.6.0
- BASELINE: `b9cbb67244d14ecaf051bf12976b062293be7f97`
- FIXED: `181d0cb203d06ef85d48051b698dc4dd535c8c3c`
- FIXED_TREE: `61f45a0369f78e45d80ae2c9ec6eab5de6399fde`
- FILE_OWNER: `scripts/build_windows_x64_public_candidate.ps1` plus this exact handoff/delta pair
- USER_WORKFLOW_CHANGED_OR_UNBLOCKED: the official Windows public-candidate builder can no longer publish a `teul-cli` package/binary artifact.
- PRODUCT_RED: isolated pre-fix builder published `ddonirang.exe` plus `teul-cli.exe` and returned success.
- PRODUCT_GREEN: fixed-target builder published one `ddonirang.exe`, `teul-cli` artifact count 0, `--help` exit 0.
- MUTATION: injected `teul-cli.exe` returned `E_WINDOWS_CANDIDATE_RETIRED_TEUL_ARTIFACT`; byte-exact restore; final GREEN; tracked residue 0.
- REUSED_TEST_COUNT: 37
- NEW_TEST_ARTIFACT_COUNT: 0
- META_TEST_CREATED: 0
- NATIVE_STATUS: Windows x64 candidate build and official executable help GREEN.
- WASM_STATUS: tracked WASM unchanged; full projection validator still reports the pre-existing embedded absolute-path finding.
- WORKBENCH_STATUS: unchanged; no new UI or semantic path.
- CHANGED_V1_GATE: teul public package/binary absence is now fail-closed at projector, validator, and Windows artifact-builder boundaries, implemented under review.
- REVIEW_BUNDLE_TARGET: W84 shared patch authority plus W85 projector guard, W86 validator guard, and W87 Windows artifact guard.
- ACTIVE_REVIEW_TASK_COUNT: 0; new reviewer/worktree/branch/task: 0.

Open slice-local gates remain unchanged: public test/view/repl membership,
PathIR public physical contract, SPEC history, VC17 exact landing, other private
teul authority, tracked-WASM path-clean candidate, final physical retirement or
deletion, legal/distribution, whole P5/P6, readiness, release, activation,
Owner Human Smoke and Human PASS.
