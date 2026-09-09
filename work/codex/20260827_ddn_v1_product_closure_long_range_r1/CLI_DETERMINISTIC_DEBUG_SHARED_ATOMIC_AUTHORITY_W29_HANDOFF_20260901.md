# CLI deterministic-debug shared atomic authority W29 handoff

## Identity and scope

- Authority checked read-only: internal SSOT v25.47.0 / RD-001~543; public Language SPEC v0.6.0.
- Successor impact: ADDITIVE_WITH_NO_PUBLIC_MEMBERSHIP_TRANSITION.
- Baseline: `ad2c6904ab3a78143a22fa93fe040a99fea24353`.
- Product fixed: `fd19f0993fe1e8f5a4bd300b229f53d4fbb2f360`.
- Product tree: `819d46538ff1ba9de350e1e6e33bccb175c9b719`.
- Direct parent relation: yes. Merge commit: no.

Exact product paths:

1. `tool/src/deterministic_debug.rs`
2. `tools/teul-cli/src/main.rs`

No pack, runner, public registry, tracked WASM, UI, SSOT, or public SPEC path changed.

## Product workflow and authority convergence

Before W29, the retained `deterministic-debug` adapter called the shared tool
semantic operation but privately owned file reading, JSON decoding, output
serialization, parent creation, and direct `fs::write` publication. The direct
write could not provide the repository's shared atomic artifact contract and
kept command orchestration authority inside teul.

W29 adds `run_deterministic_debug_file` to the existing shared
`ddonirang_tool::deterministic_debug` module. It owns the existing file input,
JSON validation, existing operation dispatch, fail-closed serialization, stdout
projection, target-kind preflight, and atomic artifact replacement. The teul
branch is now a thin argument adapter and exit-code projection only.

No command name, command membership, executable/package name, legacy-alias
period, debug wire schema, or public diagnostic registry was selected. The
target-kind diagnostic is internal/deferred command custody.

## RED, tests, and mutation

Product-facing RED at baseline: the output branch used direct `fs::write` and
had no shared atomic replacement or target-kind authority.

Verification used an isolated external Cargo target because the shared Cargo
target contained a stale same-package build from another worktree. No shared
cache was cleaned or reset.

- New focused file-workflow tests in the existing Rust module: 2/2 PASS.
- Existing deterministic-debug module tests: 17/17 PASS.
- Clean isolated `teul-cli` build: PASS.
- Tool library regression: 549 PASS; the same two pre-existing
  `ai_prompt::*` tests failed only because this isolated worktree has no
  `docs/ssot` directory. New regression: 0.
- `rustfmt --check` for the changed shared module: PASS.
- `git diff --check`: PASS.

Risk mutation: invert the output target-kind guard. The exact focused test
failed because a directory target was downgraded to the generic write path.
The source was restored byte-for-byte to SHA-256
`4a8b2dcbc23a39e9092f4bec360bfad9ee28149fe96285937e4c74bb4680d8db`,
then the focused workflow returned GREEN 2/2. Mutation residue: 0.

## C0 through C8 bounded state

| Gate | W29 state |
|---|---|
| C0 | Historical 28 tool + 63 teul = 91 command inventory remains custody; no membership transition. |
| C1 | `ddn.project-run.v1` and executable/package/alias gates unchanged. |
| C2 | Deterministic-debug file workflow and artifact authority now have one shared tool owner. |
| C3 | Public `test`/`view`/`repl` and deterministic-debug membership remain OPEN. |
| C4 | Deterministic-debug private teul orchestration/fallback authority is 0; other INTERNAL/DEFERRED physical custody remains nonzero. |
| C5 | Bounded V1-required build/test/pack/publish teul execution dependency remains 0. |
| C6 | Successful output is atomic; invalid target kind fails before publish; partial result/state/outbox publish is 0 for this workflow. |
| C7 | P5 and earlier review identities remain target-bound; W25~W29 await one coherent rolling review. |
| C8 | Teul public binary/package retirement and physical deletion remain Owner-gated. |

## Anti-meta, review, and next safe slice

- USER_WORKFLOW_CHANGED_OR_UNBLOCKED: deterministic debug artifacts now use the same atomic shared tool authority outside the retained teul adapter.
- NEW_TEST_ARTIFACT_COUNT: 0.
- EXISTING_TEST_REUSED_COUNT: 15 deterministic-debug tests plus the existing tool regression/build gates.
- META_TEST_CREATED: 0.
- STOP_RULE_APPLIED: replay-branch was rejected as a superficial candidate because it still contains a large private parser/runtime authority that needs a coherent approved migration.
- CHANGED_V1_GATE: one more internal/deferred teul orchestration authority is zero and P4 artifact failure atomicity advanced.
- REVIEW_BUNDLE_TARGET: W25 through W29 CLI shared-authority convergence at this fixed lineage, using only existing rolling reviewer `01a04b17-66bb-7fa3-b827-53ad450005b4` when management dispatches it.
- NEW_REVIEW_TASK_COUNT: 0. NEW_REVIEW_WORKTREE_COUNT: 0.
- NEXT_SAFE_TASK: fixed-object inventory of remaining teul private semantic owners, followed by one coherent reversible convergence or release-custody vertical; no public membership inference.

## Nonclaims

Status is `IMPLEMENTED_UNDER_REVIEW`. This is not whole C0~C8 closure, public
deterministic-debug membership, teul binary/package retirement or deletion,
whole P4/P5 closure, PathIR public-contract closure, VC17 landing, V1
readiness/release/activation, legal disposition, Owner Human Smoke, or Human
PASS.
