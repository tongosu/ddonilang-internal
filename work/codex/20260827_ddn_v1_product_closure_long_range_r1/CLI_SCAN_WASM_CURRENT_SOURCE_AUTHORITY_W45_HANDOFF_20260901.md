# DDN V1 CLI scan / WASM current-source authority W45 handoff

## Identity

- Authority: internal SSOT v25.47.0 / RD-001~543, public Language SPEC v0.6.0
- Baseline: `97e7d2e100550a1ae066a7aa938e6847ed6acdb6`
- Product/test fixed: `1800aa6378f46fe1a2087fa82de5a99d455f13b5`
- Fixed tree: `9d85e301eed58554b265db56b05d427e279ed917`
- Direct lineage: yes; merge commit: 0
- Previously requested review binding: `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf` is already an ancestor of the baseline and fixed commit. No merge, cherry-pick, or status-only commit was added.

## Product value and exact diff

The deferred/internal `scan --root` workflow now consumes one shared native typed owner in `ddonirang-tool`; the teul adapter no longer owns filesystem traversal, JSON warning serialization, or scan result semantics. Directory discovery and warning order are deterministic. The current shared source tree also builds for WASM again: native-only deterministic-debug file I/O is target-gated while its pure shared operation remains available to WASM.

Exact fixed paths:

1. `tool/src/scan_workflow.rs`
2. `tool/src/lib.rs`
3. `tool/src/deterministic_debug.rs`
4. `tools/teul-cli/src/cli/scan.rs`
5. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
6. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

No JavaScript, TypeScript declaration, package metadata, visible UI, SSOT, or public SPEC path changed.

## Verification

- Shared scan unit tests: 2/2 PASS.
- Existing teul scan option/parser tests: 3/3 PASS.
- Actual repository scan repeated three times: 14 packages, 16 warnings; each normalized output 2,633 bytes, SHA-256 `7164f9b0325b579ac284347f9c72b030e87b8db0326e4727b67b03ed985ae79a`.
- Deterministic-debug focused tests: 17/17 PASS.
- Tool library regression: 562 PASS + 2 pre-existing isolated-worktree environment failures caused by unavailable `docs/ssot` input; no new failure.
- Existing post-shared-changes tracked-WASM runner: PASS.
- Direct current-source WASM deterministic-debug repeat: PASS, 373 bytes, SHA-256 `b97d33a768a027bf54f84c5babb9208ed1497df94f42527e6aec8775d10ca020`.
- Official current-source WASM build: PASS after target-gating native file I/O.
- Official WASM freshness after commit: PASS.
- `git diff --check`: PASS.

Tracked current-source candidate identity:

- WASM bytes: 5,575,187
- WASM SHA-256: `62555c83144735bc9bb231250fe4244cb4ddc4c0d4b36f844b264f18ecb227f5`
- Manifest bytes before Git LF materialization: 25,576
- Manifest worktree SHA-256 before commit: `f28f9d7f422176c3e6749de9ba2eebcb845aab877e84cdcca6d1e1ae786c8bdb`
- Source inventory: 130 files
- Manifest closure claim remains `freshness_only_no_full_cli_wasm_equivalence`.

## Mutation and restore

The risk-relevant mutation reversed scan directory ordering. The existing focused deterministic-order test produced actual RED with exit 101 and observed `z_skip` before `a_skip`. The source was byte-exact restored to SHA-256 `e26805d1029df2ad7c13044b8a9c64290169505400ec9776c17578803ee55b92`, then the focused suite returned GREEN 2/2. Mutation residue is 0. An earlier sort-removal attempt was a no-op on the Windows filesystem and is not counted as evidence.

## Authority and dependency disposition

- `scan` private teul semantic authority: 0 for the migrated workflow.
- `scan` teul adapter: consumer/re-export only.
- `scan` required semantic implementation owner: `tool/src/scan_workflow.rs` (one owner).
- WASM current-source compile blocker in deterministic-debug: removed without changing public semantics.
- Replay verification remains a separate `FILE_OWNER_EXPANSION_REQUIRED` slice because its current provider graph still depends on the private teul lexer/parser/evaluator/state/Geoul/snapshot/input-tape family. No replay product change is included here.

## Anti-meta and custody

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: YES — deterministic shared scan output and a buildable current-source WASM candidate.
- `NEW_TEST_ARTIFACT_COUNT`: 0
- `NEW_RUST_TEST_COUNT`: 2, colocated with the shared product owner
- `EXISTING_TEST_REUSED_COUNT`: 565 passing checks/runners, with overlap counted once at the full-suite level
- `META_TEST_CREATED`: 0
- `NEW_PACK`: 0
- `NEW_RUNNER`: 0
- `NEW_REVIEW_TASK`: 0
- `NEW_REVIEW_WORKTREE`: 0

The four pre-existing task-owned untracked session files were preserved byte-for-byte, unstaged, and excluded from both fixed and handoff commits.

## Status and nonclaims

Status: `IMPLEMENTED_PENDING_COHERENT_REVIEW`

This handoff does not decide public command membership, public executable or package naming, legacy alias lifetime, final internal/deferred physical placement, public `test/view/repl` membership, replay convergence, PathIR/Proof public contract, VC17 exact landing, physical teul-cli retirement, P5/Windows release closure, V1 readiness, release, activation, legal status, Owner Human Smoke, or Human PASS.

