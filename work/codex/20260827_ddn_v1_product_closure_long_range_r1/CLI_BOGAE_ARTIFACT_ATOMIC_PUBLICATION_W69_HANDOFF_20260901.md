# DDN V1 CLI Bogae artifact atomic publication W69 handoff

## Status and authority

- Status: `CLI_BOGAE_ARTIFACT_ATOMIC_PUBLICATION_W69_IMPLEMENTED_PENDING_REVIEW`.
- Persistent goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1`, `ACTIVE`.
- Internal live CURRENT: v25.47.0 / RD-001~543, Owner-final 2026-08-31.
- Public Language SPEC: v0.6.0.
- Successor impact: `ADDITIVE_NO_RELEVANT_SEMANTIC_CONFLICT`. No prior PASS is automatically inherited or broadened.
- Review commits `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf` and `bc84d81d4faa55974975bdb7ec60cb18d9a7ebda` are verified ancestors of this fixed target and remain bound only to their exact reviewed scopes.

## Exact lineage and FILE_OWNER

- Baseline: `71aa3dd75358eab304779e7221ef5745f49572c5`.
- Product fixed commit: `260727b1e023b263d0988656538f66dd66265212`.
- Product fixed tree: `9b8d4e73fdda66181c7beb443ab3392e7a23aca2`.
- Direct parent: yes. Merge commit: no.

Changed product paths only:

- `tools/teul-cli/src/cli/bogae_bundle.rs`
- `tools/teul-cli/src/cli/bogae_edit.rs`

No pack, runner, framework, meta-test, public spelling, command membership, executable identity, wire schema, tracked WASM, Workbench UI, SSOT, or public SPEC path changed.

## User workflow and implementation

Two existing Bogae CLI workflows now consume the already established shared artifact publication authority.

1. `bogae edit --out <nested-path>` uses `write_binary_artifact_atomic`, creates the missing parent through the shared contract, and atomically replaces the final detbin.
2. `bogae bundle` materializes mapping, scene, new content-addressed assets, and manifest as one preflighted artifact set. A later invalid target can no longer leave earlier bundle files published.

Bundle payload bytes, manifest order/hash, edit detbin bytes, Korean/public command spelling, and current accepted source behavior are unchanged. Existing content-addressed assets already present at the target remain custody and are not needlessly replaced.

## Product RED, fault, mutation, restore, GREEN

### Baseline RED

- Fault: make `manifest.toml` a directory before `bogae bundle`.
- Baseline exit: 1, OS error 5.
- Mapping published despite failure: 1 file.
- Asset published despite failure: 1 file.
- Partial artifact publish: confirmed.
- `bogae edit` to a missing nested parent: exit 1, OS error 3, output 0.

### Fixed GREEN

- Same bundle fault: exit 1 with `E_SHARED_ARTIFACT_OUTPUT_TARGET_NOT_FILE`.
- Mapping files published: 0.
- Asset files published: 0.
- Normal bundle: exit 0, three output files, stable `bogae_bundle_hash=blake3:2a3552afd8d97b7506ed5cf632c7c5cb5faefe079996aef362cae7e3e90759b9`.
- Nested edit: exit 0; output SHA-256 `b2099b0d5005557f59a2283d72eb70604d3659023c78b587975c421e2ccb9785`, exactly the tracked golden bytes.

### Risk-relevant mutation

- Mutation: replace the shared artifact-set call with sequential direct writes.
- Mutation result: RED exit 1; mapping 1 and asset 1 remained after manifest failure.
- Fixed `bogae_bundle.rs` SHA-256 before mutation: `cab5f78b4fef9c03b34a6756304d1b3ce0380799277fc0f8b733f19a505e7def`.
- Exact restore SHA-256: same.
- Restore result: fail-closed exit 1, mapping 0, asset 0.
- Mutation/build/test residue after cleanup: 0.

## Verification

- Exact clean fixed-HEAD product build: PASS.
- Existing `bogae_editor_v0` golden pack: PASS.
- Existing `bogae_bundle_v1` golden pack: PASS.
- Existing shared `artifact_output` unit tests: 5/5 PASS.
- Normal bundle and nested edit actual CLI workflows: PASS.
- Edit output equals tracked golden SHA-256 exactly.
- Bundle failure partial artifact files: 0.
- Temporary/backup publication residue: 0.
- `git diff --check`: PASS.
- Protected server/browser/process lifecycle commands: 0; TCP 8787 listener remained 0; cargo/rustc process residue 0.

Applicable parity classification: the fixed seam is native filesystem publication and has no WASM or Workbench filesystem writer. Payload identity is checked against the existing product golden packs. No JS semantic reconstruction or hidden PreV25 fallback was added. Whole native/WASM/Workbench CLI parity remains OPEN.

## C0-C8 actual state

- C0: historical 28 tool + 63 teul = 91-command inventory remains custody; membership transition 0.
- C1: `ddn.project-run.v1` neutral semantic identity remains fixed; executable/package/legacy alias decisions remain OPEN.
- C2: shared source/canon/preprocess/execution/artifact authority convergence is additive; two more direct product publication seams now consume shared authority.
- C3: official V1 command reachability remains 12/15; public test/view/repl membership stays slice-frozen.
- C4: INTERNAL/DEFERRED command custody is preserved; deletion or public promotion 0.
- C5: bounded V1-required build/test/pack/publish teul execution dependency remains 0; repository-wide historical references are not claimed removed.
- C6: Bogae edit/bundle artifact bytes and failure atomicity pass in the applicable native frontdoor; whole cross-frontdoor parity remains OPEN.
- C7: P5 target-bound review PASS remains bound; whole P5/Windows RC closure remains OPEN.
- C8: teul binary/package/directory physical retirement remains gated by exact dependency inventory, coherent independent PASS, backup/hash/restore, and Owner deletion approval.

## Anti-meta, review, and next value

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: nested edit output succeeds atomically; bundle publication cannot expose a partial file set on the reproduced late-target failure.
- `EXISTING_TEST_REUSED_COUNT`: 2 existing product packs + 5 existing shared-writer unit tests.
- `NEW_TEST_ARTIFACT_COUNT`: 0.
- `META_TEST_CREATED`: 0.
- `NEW_REVIEW_TASK_COUNT`: 0.
- `NEW_REVIEW_WORKTREE_COUNT`: 0.
- Existing rolling reviewer handle `01a04b17-66bb-7fa3-b827-53ad450005b4` remains the only designated reviewer. Management may bind this fixed/handoff to the next coherent post-181 CLI artifact-publication review bundle; the writer did not create or dispatch another reviewer.
- `NEXT_PRODUCT_DECISION_ENABLED`: continue to the next bounded direct-write seam with a complete transaction boundary, prioritizing Bogae multi-file projection or another existing CLI artifact workflow without public membership changes.

## Open boundaries and nonclaims

SPEC history, PathIR public assumption/obligation contract, public test/view/repl membership, VC17 exact provider landing, public executable/package naming, legacy alias duration, physical teul deletion, legal/distribution, whole P0~P6 closure, V1 membership/readiness/release/activation, P6 Owner Human Smoke, and Human PASS remain OPEN. This handoff claims neither full Bogae/Web/Workbench closure nor whole CLI convergence.
