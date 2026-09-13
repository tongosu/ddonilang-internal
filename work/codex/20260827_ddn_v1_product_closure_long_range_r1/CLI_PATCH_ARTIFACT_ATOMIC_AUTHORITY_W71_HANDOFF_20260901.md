# DDN V1 CLI patch artifact atomic authority W71 handoff

## Status and authority

- Status: `CLI_PATCH_ARTIFACT_ATOMIC_AUTHORITY_W71_IMPLEMENTED_PENDING_REVIEW`.
- Persistent goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1`, `ACTIVE`.
- Internal live CURRENT: v25.47.0 / RD-001~543, Owner-final 2026-08-31.
- Public Language SPEC: v0.6.0.
- Successor impact: `ADDITIVE_NO_RELEVANT_SEMANTIC_CONFLICT`; this slice changes only failure-atomic artifact publication.
- Review commit `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf` remains an exact-scope ancestor.
- P5 review commit `bc84d81d4faa55974975bdb7ec60cb18d9a7ebda`, report SHA-256 `05d9522c900d5c164064a003f92fabc100f64daf40100690b0e3c3747892a6d6`, remains an exact-scope ancestor with `PASS_TARGET_BOUND`, blocking 0. This removes the previous reviewer-handle/whole-goal blocker claim but does not broaden P5 PASS.

## Exact lineage and FILE_OWNER

- Baseline/handoff parent: `9073b6a43d164f23ed496a7aed834f0085bd3ff5`.
- Product fixed commit: `777e4b1304c3c46981a854e04bdf54c0f625d12b`.
- Product fixed tree: `7492330ea3c538f7088feea4b0073ddfd9d7116f`.
- Fixed product blob: `f1e2b375d6d032bf1719bb1837db7f9871c82518`.
- Fixed checkout SHA-256: `2dc2f7d61ffb73addc735b3d3044b8c08626ab5fe63c28ccb614407f17722b9b`.
- Direct parent: yes. Merge commit: no.

Changed product path only:

- `tools/teul-cli/src/cli/patch.rs`

No parser, runtime semantics, patch schema, public command spelling, pack, runner, tracked WASM, Workbench UI/copy/layout, SSOT, public SPEC, membership, or release path changed.

## User workflow and product change

The existing native workflow

```text
patch propose -> patch approve -> patch apply
```

now consumes `ddonirang_tool::artifact_output` for all publication boundaries:

- `patch propose`: atomic single-file replacement and parent creation.
- `patch approve`: atomic single-file replacement and parent creation.
- `patch apply`: all changed files are prepared and published as one artifact set; a late target failure rolls back or prevents the entire set.

Patch semantics, approval digest, canonical source check, input/output bytes, public option spelling, and in-place/out-of-place modes are unchanged.

## RED, GREEN, mutation, and restore

### Product baseline RED

- Two-file patch: `a.ddn` and `b.ddn`.
- Fault: output target `b.ddn` pre-exists as a directory.
- Baseline exit: 1, `E_PATCH_WRITE`, OS error 5.
- Baseline `output/a.ddn` already published: 1.
- Result: actual partial multi-file artifact publication.

### Fixed GREEN

- `patch propose --out nested/proposed.patch.json`: exit 0, nested parent created.
- `patch approve --out nested/approval.json --yes`: exit 0, nested parent created.
- Same two-file late-target fault: exit 1, `E_SHARED_ARTIFACT_OUTPUT_TARGET_NOT_FILE`.
- Partial `fault/a.ddn` publication: 0.
- Normal out-of-place apply: exit 0; both outputs contain the requested replacements.
- Normal in-place apply: exit 0; both source files contain the requested replacements.
- Two normal out-of-place executions: output hashes 4/4 repeat-equal.
- Temporary/backup artifact residue: 0.

### Risk-relevant mutation

- Mutation: replace the shared artifact-set call with sequential `fs::write` calls.
- Mutation RED: exit 1; `fault/a.ddn` partial publication 1.
- Byte-exact restore SHA-256: `2dc2f7d61ffb73addc735b3d3044b8c08626ab5fe63c28ccb614407f17722b9b`.
- Restore GREEN: exit 1; `fault/a.ddn` partial publication 0.
- Mutation source/build/test residue after cleanup: 0.

## Verification

- Fixed product binary build: PASS.
- Clean fixed-HEAD direct workflow reproduction: PASS.
- Existing shared artifact writer tests: 5/5 PASS.
- Direct product cases: propose 1/1, approve 1/1, fault atomicity 1/1, normal out-of-place 1/1, normal in-place 1/1, deterministic repeat 1/1.
- Existing `age1_patch_approval` custody: preview and approve PASS; apply remains fail-closed at pre-existing `E_PATCH_CANON_MISMATCH`, published artifact 0. It is classified as historical fixture drift and is not counted as W71 GREEN or changed by this slice.
- Generic W90 golden execution was excluded after it updated two tracked golden files in the working tree; those runner-created diffs were restored exactly before fixed custody. Product/golden diff after restoration: 0 outside the owned product path.
- Partial result/state/outbox publication introduced: 0.
- External task temp/build residue after cleanup: 0.
- `git diff --check`: PASS.

Applicable parity: this exact seam is a native filesystem patch projection. WASM and Workbench do not expose this filesystem writer, so cross-frontdoor parity is not applicable to the write boundary. Patch bytes and schema remain unchanged; no JS semantic reconstruction or private fallback was added. Whole native/WASM/Workbench parity remains OPEN.

## C0-C8 actual state

- C0: historical 28 tool + 63 teul = 91-command inventory remains custody; membership transition 0.
- C1: `ddn.project-run.v1` remains fixed; executable/package/legacy alias decisions remain OPEN.
- C2: the reachable patch workflow now consumes shared artifact authority for propose, approve, and multi-file apply; sequential publication authority at this seam is 0.
- C3: official V1 reachability remains 12/15; public test/view/repl membership stays slice-frozen.
- C4: INTERNAL/DEFERRED commands remain custody; deletion/public promotion 0.
- C5: bounded V1-required build/test/pack/publish teul execution dependency remains 0. Historical/internal references remain custody.
- C6: applicable native patch determinism and failure atomicity PASS; whole WASM/Workbench parity OPEN.
- C7: P5 target-bound review PASS remains bound; whole P5 and Windows RC closure OPEN.
- C8: teul binary/package/directory retirement remains gated by exact physical inventory, coherent independent PASS, backup/hash/restore, and Owner deletion approval.

## Anti-meta, review, and next safe work

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: a failed multi-file patch can no longer expose a partially updated project, and propose/approval outputs use atomic replacement.
- `EXISTING_TEST_REUSED_COUNT`: 5 shared-writer unit tests plus existing patch CLI/fixture surfaces.
- `NEW_TEST_ARTIFACT_COUNT`: 0.
- `META_TEST_CREATED`: 0.
- `NEW_REVIEW_TASK_COUNT`: 0.
- `NEW_REVIEW_WORKTREE_COUNT`: 0.
- Existing rolling reviewer handle `01a04b17-66bb-7fa3-b827-53ad450005b4` remains the only designated reviewer. W69~W71 are a coherent CLI artifact-publication bundle ready for management dispatch; the writer did not create or dispatch another reviewer.
- `NEXT_SAFE_TASK`: audit the next reachable CLI filesystem writer whose public meaning is unchanged, preferring a direct multi-artifact or overwrite seam over membership-frozen test/view/repl surfaces.

## Frozen slices and nonclaims

SPEC history, the PathIR public contract, public test/view/repl membership, and VC17 exact landing remain individually frozen. They are not aggregated into a whole-goal blocker.

This handoff does not claim public patch/view/test/repl membership, whole CLI convergence, repository-wide teul semantic-authority/dependency zero, physical teul retirement, PathIR public contract or P1 closure, VC17 exact landing, whole P5/Windows RC, P0~P6 closure, V1 membership/readiness/release/activation, legal/distribution approval, P6 Owner Human Smoke, or Human PASS.
