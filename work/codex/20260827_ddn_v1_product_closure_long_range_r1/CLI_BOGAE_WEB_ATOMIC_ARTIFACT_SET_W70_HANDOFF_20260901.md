# DDN V1 CLI Bogae web atomic artifact set W70 handoff

## Status and authority

- Status: `CLI_BOGAE_WEB_ATOMIC_ARTIFACT_SET_W70_IMPLEMENTED_PENDING_REVIEW`.
- Persistent goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1`, `ACTIVE`.
- Internal live CURRENT: v25.47.0 / RD-001~543, Owner-final 2026-08-31.
- Public Language SPEC: v0.6.0.
- Successor impact: `ADDITIVE_NO_RELEVANT_SEMANTIC_CONFLICT` for this reversible publication/safety correction.
- Review commits `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf` and `bc84d81d4faa55974975bdb7ec60cb18d9a7ebda` remain exact-scope ancestors. No review scope is broadened or automatically inherited.

## Exact lineage and FILE_OWNER

- Baseline/handoff parent: `a1f941fa97ebefea4f78d1df905a1bfc8b0adbb9`.
- Product fixed commit: `57eb53ceb4a039e69e3d5fe4e917f0c9520a6b46`.
- Product fixed tree: `85714aa32fc66725c53e0719e440c4141f409584`.
- Fixed product blob: `cf07fd3db6f09dd5a9f984c11ddf21f5ad3379d5`.
- Fixed checkout SHA-256: `2287d2c40f2c2cc8a1555c75798956f70e41e44203133f9917ac14b40f9174a8`.
- Direct parent: yes. Merge commit: no.

Changed product path only:

- `tools/teul-cli/src/cli/bogae_web.rs`

No parser, runtime semantics, pack, runner, public command spelling, tracked WASM, Workbench UI/copy/layout, SSOT, public SPEC, membership, or release path changed.

## User workflow and implementation

The reachable existing workflow

```text
teul-cli view <drawlist.detbin> --bogae web --bogae-out <directory> --no-open
```

previously wrote `drawlist.json`, detbin, overlay, and `index.html` sequentially. It now materializes the complete core set through `ddonirang_tool::artifact_output::write_artifact_set_atomic`.

When an existing readable skin is supplied, `skin.detjson` and readable relative skin assets join the same set. Existing best-effort behavior is preserved for absent/unreadable optional skin files and invalid optional assets. Relative asset paths containing parent/root/prefix components are not copied outside the viewer root. Core output bytes, HTML, overlay, detbin, skin bytes, public spelling, and drawlist semantics are unchanged.

## RED, GREEN, mutation, and restore

### Product baseline RED

- Setup: `overlay.detjson` is a directory before invoking the web viewer.
- Exit: 1, OS error 5.
- `drawlist.json` was already published: 1.
- `index.html`: 0.
- Result: actual partial artifact publication.

The adjacent playback attempt was also audited. Current `run --madi ... --bogae web` rejects the legacy option shape with `E_SHARED_RUNTIME_OPTION_UNSUPPORTED` before reaching playback publication. Under the product-value stop rule, playback product files were not changed and that sub-slice remains frozen rather than being supported through a private fallback.

### Fixed GREEN

- Same overlay-directory fault: exit 1 with `E_SHARED_ARTIFACT_OUTPUT_TARGET_NOT_FILE`.
- Core artifact files published: 0.
- Normal viewer: exit 0, core files 4.
- Viewer with existing SA2 skin: exit 0, files 6.
- Copied skin SHA-256: `eecc1e00f60de850f974c5ba9d5177e3fab01d1d06b6fbb8776ce5b08c2febd0`, exact source match.
- Copied SVG SHA-256: `0869cb5bd48b22b5cd56747e6a725abe7a2f129cf620e3f54d659cfceafc0936`, exact source match.
- Two independent executions: all six output SHA-256 identities 6/6 equal.
- A skin URI `../escape.txt` produced escaped viewer-root artifact 0 while preserving valid core and skin-root output.

### Risk-relevant mutation

- Mutation: replace the shared artifact-set call with sequential direct writes.
- Mutation RED: exit 1; `drawlist.json` remained after overlay failure.
- Exact restore SHA-256: `2287d2c40f2c2cc8a1555c75798956f70e41e44203133f9917ac14b40f9174a8`.
- Restore GREEN: same fault, core artifact files 0.
- Mutation/build/test residue after cleanup: 0.

## Verification

- Fixed product binary build: PASS.
- Clean fixed-HEAD fault and normal skin workflow reproduction: PASS.
- Existing shared artifact writer tests: 5/5 PASS.
- Existing `run_bogae_alias_viewer_family_selftest.py`: PASS, surfaces 3.
- Actual native web-view workflows: baseline fault, fixed fault, no-skin, skin, traversal guard, deterministic repeat all exercised.
- Partial result/state/outbox publication introduced: 0.
- Temporary/backup files after successful and failed writes: 0.
- External task build/test residue: 0.
- Cargo/rustc process residue: 0. TCP 8787 listener: 0. Protected browser/server lifecycle commands: 0.
- `git diff --check`: PASS.

Applicable parity: this seam is a native filesystem projection. No WASM or Workbench filesystem writer consumes it, so cross-frontdoor field parity is not applicable to this exact write boundary. Drawlist/skin payload bytes remain unchanged and no JS semantic reconstruction was added. Whole native/WASM/Workbench parity remains OPEN.

## C0-C8 actual state

- C0: historical 28 tool + 63 teul = 91-command inventory remains custody; membership transition 0.
- C1: `ddn.project-run.v1` remains fixed; executable/package/legacy alias decisions remain OPEN.
- C2: the reachable web viewer now consumes shared artifact-set authority; direct multi-file publication and path escape seams are removed as scoped.
- C3: official V1 reachability remains 12/15; public test/view/repl membership stays slice-frozen.
- C4: INTERNAL/DEFERRED commands remain custody; deletion/public promotion 0.
- C5: bounded V1-required build/test/pack/publish teul execution dependency remains 0. Historical/internal references remain custody.
- C6: applicable native viewer artifact bytes, determinism, and failure atomicity PASS; whole WASM/Workbench parity OPEN.
- C7: P5 target-bound review PASS remains bound; whole P5 and Windows RC closure OPEN.
- C8: teul binary/package/directory retirement remains gated by exact dependency inventory, coherent independent PASS, backup/hash/restore, and Owner deletion approval.

## Anti-meta, review, and next safe work

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: a failed web viewer publication no longer exposes an incomplete core set, and relative skin assets cannot escape the viewer output root.
- `EXISTING_TEST_REUSED_COUNT`: 5 shared-writer unit tests + 1 existing Bogae surface checker.
- `NEW_TEST_ARTIFACT_COUNT`: 0.
- `META_TEST_CREATED`: 0.
- `NEW_REVIEW_TASK_COUNT`: 0.
- `NEW_REVIEW_WORKTREE_COUNT`: 0.
- Existing rolling reviewer handle `01a04b17-66bb-7fa3-b827-53ad450005b4` remains the only designated reviewer. W69~W70 form the next bounded Bogae artifact-publication bundle for management dispatch; the writer did not create or dispatch another reviewer.
- `NEXT_SAFE_TASK`: audit another reachable CLI artifact workflow with an exact transaction boundary. Playback remains frozen until a current shared frontdoor reaches it without private legacy fallback.

## Open boundaries and nonclaims

This handoff does not claim public `view` membership, playback support, whole Bogae/Web/Workbench closure, whole CLI convergence, repository-wide teul semantic-authority/dependency zero, physical teul retirement, PathIR public contract, VC17 exact landing, P0~P6 closure, V1 membership/readiness/release/activation, legal/distribution approval, P6 Owner Human Smoke, or Human PASS.
