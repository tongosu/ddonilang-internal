# CLI Gaji plan output shared authority W68 handoff

## Status

- `CLI_GAJI_PLAN_OUTPUT_SHARED_AUTHORITY_W68_IMPLEMENTED_UNDER_REVIEW`
- Persistent `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` goal remains ACTIVE.
- This is a bounded reversible CLI/shared-tool convergence milestone. It is not command-membership, retirement, P5, or V1 closure.

## Authority and exact lineage

- Internal live CURRENT: v25.47.0 / RD-001~543, Owner-final 2026-08-31.
- Public Language SPEC: v0.6.0.
- Successor impact: `ADDITIVE_NO_RELEVANT_SEMANTIC_CONFLICT`; the existing typed Gaji semantics and physical output bytes are unchanged.
- Baseline/handoff parent: `9b0fb9bfc8610f6249854a7ab76de6b1922cd62d`.
- Product/test fixed commit: `ca7bfe466eebec84d50b780c2a9eacb2256c7b73`.
- Product/test fixed tree: `970037683b08a5a7a6beca9a6cec54a7b8fae2bc`.
- Direct parent: yes. Merge count: 0.
- Review commits `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf` and `bc84d81d4faa55974975bdb7ec60cb18d9a7ebda` remain ancestors and retain only their exact target-bound scopes.

## Product value and exact FILE_OWNER

Existing `gaji plan` and `gaji lifecycle-plan` already consume the shared typed `tool::local_project` authority and have a tracked-WASM projection. Their CLI `--out` paths alone used direct `fs::write`, so a user-supplied nested output failed when the parent did not yet exist and did not consume the established atomic replacement authority.

Changed paths only:

- `tools/teul-cli/src/main.rs`
- `tests/gaji_creator_wasm_parity_runner.mjs` (existing runner extended; no new runner)

Both CLI output paths now use `ddonirang_tool::artifact_output::write_text_artifact_atomic`. Stdout behavior, request/result schema, Korean source behavior, WASM exports, Workbench UI, public spelling, executable identity, and Gaji lifecycle semantics are unchanged.

## RED, mutation, exact restore, GREEN

### Baseline product RED

- Workflow: `gaji plan --input pack/gaji_creator_wave1/g2_extraction_request.detjson --out <missing-parent>/nested/result.detjson`.
- Baseline exit: 1.
- Failure: `E_GAJI_PLAN_WRITE ... os error 3`.
- Parent and output created: no/no.

### Fixed product GREEN

- Same raw request and nested output shape: exit 0.
- Output bytes: 992.
- Output SHA-256: `e2edc66c803dc4a9a34b54d6059d7b7402c9cda7e0ad2fe3918b1bb8ce1e09f7`.
- Temporary publication residue: 0.

### Risk-relevant mutation

- Mutation: restore only the extraction `--out` route to direct `fs::write`.
- Mutation result: RED exit 1 with missing parent; output 0.
- Fixed source `main.rs` SHA-256 before mutation: `84989c439bf9289f20b7e785b7eff00de202015deb13139013bf9df0951b71b3`.
- Exact restore SHA-256: same; byte-exact restore PASS.
- Restore GREEN: exit 0, output SHA-256 `e2edc66c...`, residue 0.

## Verification

- Offline fixed product build: PASS.
- Existing `gaji_creator_wasm_parity` runner: PASS.
  - extraction stdout = tracked WASM exact.
  - extraction nested `--out` = tracked WASM exact.
  - lifecycle stdout = tracked WASM exact.
  - lifecycle nested `--out` = tracked WASM exact.
  - installed V1/V2/rollback `project-run` CLI/WASM result and state identity checks remain PASS.
- Existing focused tool Gaji tests: 10/10 PASS.
- Fixed output repeated at two distinct paths: SHA-256 identical.
- Partial result/state/outbox publish introduced: 0.
- External W68 build/test file residue after cleanup: 0.
- `git diff --check`: PASS.

The official tracked-WASM freshness checker remains `FAIL_STALE` at its three pre-existing source manifest axes (`source_file_count`, `source_tree_sha256`, `source_files`). W68 changes only teul CLI routing and its existing runner, does not change the WASM product source or export, and does not refresh/promote the tracked binary. Exact semantic parity above is product evidence, not freshness promotion.

## Anti-meta and review state

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: users can emit extraction and lifecycle plans to nested paths with the shared parent-creation/atomic replacement contract.
- `EXISTING_TEST_REUSED_COUNT`: 10 focused Rust tests + 1 existing end-to-end native/WASM runner.
- `NEW_TEST_ARTIFACT_COUNT`: 0.
- `META_TEST_CREATED`: 0.
- `NEW_REVIEW_TASK_COUNT`: 0.
- `NEW_REVIEW_WORKTREE_COUNT`: 0.
- Existing rolling reviewer handle `01a04b17-66bb-7fa3-b827-53ad450005b4` is preserved for the next coherent W62~W68 target bundle; it was not dispatched by the writer.

## C0-C8 and open boundaries

- C0: 91-command inventory custody unchanged.
- C1: `ddn.project-run.v1` identity unchanged; executable/package/alias OPEN.
- C2: Gaji plan/lifecycle native CLI now consumes the shared typed semantic and artifact publication authorities.
- C3: official 12/15 unchanged; public test/view/repl membership remains slice-frozen.
- C4: internal/deferred custody unchanged.
- C5: bounded V1-required build/test/pack/publish teul execution dependency remains 0.
- C6: applicable native/tracked-WASM plan/lifecycle parity PASS; whole Workbench/CLI parity remains OPEN.
- C7: P5 target-bound PASS preserved; whole P5 and Windows RC closure OPEN.
- C8: teul binary/package/directory physical retirement remains Owner-gated.

PathIR P0 containment is preserved. Public PathIR P1 wire/ingress/receipt, SPEC history, public command membership, VC17 exact landing, tracked-WASM refresh, physical teul deletion, legal/distribution, P5/P6, release/readiness/activation/Human PASS remain OPEN. `docs/ssot/**`, public SPEC, tracked WASM, visible UI, membership, and release state diff are all 0.

