# CLI canon artifact-set atomic authority W47 handoff

## Fixed identity

- status: `IMPLEMENTED_PENDING_COHERENT_REVIEW`
- live authority: internal SSOT v25.47.0 / RD-001~543
- public Language SPEC: v0.6.0
- baseline: `bcb06a4efbf1ff4ebcde7dc220c4992255cbcf26`
- product fixed: `56b4fa65588613f372b42c229d203da93c6c2fe1`
- product tree: `72f81cbc8537d3740c30448c1cd0c99a958da8c3`
- direct lineage: yes
- merge count: 0

## User workflow and product correction

The existing V1-required `canon --emit both` workflow publishes canonical DDN
and fix-it JSON as one artifact set. Before W47, each file used an atomic
single-file writer, but the pair was published sequentially. If the second
target failed preflight, the first file remained visible as a partial result.

W47 routes the pair through the existing shared
`write_text_artifacts_atomic` authority. Target validation, staging, commit,
rollback, and residue handling are now owned by one shared tool transaction.
No parser, canonicalizer, public option, diagnostic spelling, command
membership, executable name, or wire contract changed.

## Exact product diff

- `tools/teul-cli/src/cli/canon.rs`
- 54 insertions, 3 deletions
- new pack: 0
- new runner/framework/meta-test: 0
- one colocated product regression test was added to the existing canon suite

## RED, GREEN, and mutation

- Initial RED: a directory occupied the second `.fixits.json` target. The
  command failed, but the first `.canon.ddn` artifact was already published.
- Product GREEN: the shared set preflight rejected the blocked target before
  either file became visible; partial publish count 0.
- Success GREEN: after removing the blocker, both canonical and fix-it
  artifacts were published together.
- Risk mutation: the two shared-set outputs were changed back to sequential
  single-file writes; the same test produced actual RED with the first artifact
  visible.
- Exact restore SHA-256 for `canon.rs`:
  `2aad8e437aebb75b7088cefb7b37ee8099bfe23128bbc72d5a5402f322074d91`.
- Restore GREEN: focused 1/1 PASS.
- task-created `%TEMP%` mutation residue: 0.

## Verification

- focused canon artifact-set product test: 1/1 PASS
- canon module: 11 PASS + 2 pre-existing out-of-scope FAIL
- shared artifact-output transaction: 5/5 PASS
- full teul-cli binary suite: 1043 PASS + the same 9 pre-existing out-of-scope
  FAIL / 0 ignored
- new regression relative to W46 full-suite result: 0
- `git diff --check`: PASS

The two canon failures are the existing legacy `보임` and legacy 짜임-port
expectation drift. The other seven full-suite failures remain in the existing
frontdoor/right-assignment and runtime atomicity rows. W47 does not claim these
as resolved and does not claim whole-suite PASS.

## Parity and authority boundary

This slice changes the native filesystem multi-output publication boundary.
WASM and Workbench do not expose this filesystem `--emit both` output pair, so
no WASM/UI path was modified and broad native/WASM/Workbench parity is not
claimed. Canon semantic output remains owned by the existing shared language/
tool authority; W47 only changes all-or-nothing artifact publication.

## Anti-meta checkpoint

- USER_WORKFLOW_CHANGED_OR_UNBLOCKED: `canon --emit both` cannot expose a
  canonical artifact without its matching fix-it artifact.
- NEW_TEST_ARTIFACT_COUNT: 0
- NEW_RUST_TEST_COUNT: 1, colocated with the existing product command
- EXISTING_TEST_REUSED_COUNT: canon suite 12 predecessor rows, shared artifact
  transaction 5 rows, and the full teul-cli suite
- META_TEST_CREATED: 0
- STOP_RULE_APPLIED: yes; only the concrete partial-publish risk was mutated
- NEXT_PRODUCT_DECISION_ENABLED: canon can be classified as consuming the
  shared artifact-set transaction rather than owning a private multi-output
  commit sequence

## Custody and nonclaims

The four protected task-owned untracked files remained byte-identical and
unstaged. `docs/ssot/**`, public SPEC, tool/lang product semantics, tracked
WASM, UI, pack, and publish paths have diff 0.

This handoff does not claim public `view/test/repl` membership, final public
command membership, executable/package naming, whole C0~C8 closure, repository-
wide teul authority/dependency 0, physical teul retirement/deletion, PathIR
public closure, VC17 landing, P0~P6 closure, V1 readiness, release, activation,
legal approval, Owner Human Smoke, or Human PASS.
