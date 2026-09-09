# P0 CLI01 lint shared authority W7 handoff

Date: 2026-08-30
Session: DDN V1제품마감Codex
Persistent goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1`

## Fixed identity and scope

```text
STATUS: IMPLEMENTED_UNDER_REVIEW
CURRENT_AUTHORITY: internal v25.40.0 / RD-001~515
PUBLIC_SPEC: v0.6.0
BASELINE: c0bda454a22df9cf00108f4bd8d0f8117d0637dd
PRODUCT_TEST_FIXED: 64abb938b7eccf38ce71213ec03dfec2dd15fd5e
FIXED_TREE: bfb1482af0055abe6a1e9a8d057ba852664fe866
BRANCH: codex/ddn-v1-p1a-core-supported-ingress-w1-20260829
MERGE_COUNT: 0
```

This vertical changes one user workflow: `ddonirang lint` now accepts raw V25
source with an explicit supported profile, uses the shared language lexer and
`tool::source_analysis`, and produces the same warning/patch artifact as the
teul adapter. Before the change the candidate rejected `lint` with
`E_CLI_COMMAND_UNKNOWN`.

The teul lint command is now an adapter over the same product function. Its
historical PreV25 golden custody is explicit through a hidden
`--legacy-internal` switch. There is no second parser, private runtime/value
authority, hidden PreV25 retry, global default switch or test-only lowering.

## Exact fixed diff

```text
tool/src/bin/ddonirang.rs
tool/src/lib.rs
tool/src/lint.rs
tools/teul-cli/src/cli/lint.rs
tools/teul-cli/src/main.rs
tools/teul-cli/tests/golden/W90/W90_G05_lint_suggest_patch/test.dtest.json
```

No new pack, runner, checker, meta-test, reviewer, review worktree, branch,
goal or public command-membership decision was created.

## Product evidence

- shared lint unit tests: 4/4 PASS
- candidate command tests: 7/7 PASS
- full tool library regression in isolated target: 531/531 PASS
- existing W90 lint golden case G05: PASS
- actual V25 Korean source candidate/teul patch bytes: exact, SHA-256
  `c9dc90e85e68b92aef4fadb153597dd48346d8f53e40326e44a1e29b707ac38f`
- missing profile: both fail closed with `E_SOURCE_PROFILE_REQUIRED`
- unknown profile: both fail closed with `E_SOURCE_PROFILE_UNSUPPORTED`
- output-directory fault: both fail closed with
  `E_LINT_OUTPUT_IS_DIRECTORY`; partial patch publish 0
- isolated candidate binary build: PASS
- `git diff --check`: PASS

The full W90 runner also reported four failures outside the changed G05 lint
case; no baseline/new-drift disposition is claimed for them. G05 itself
passed. Two runner-written expected-output residues outside the owned slice
were restored to their exact HEAD blobs and staged diff remained zero.

## C0~C8 status

```text
C0: historical 91-command custody remains confirmed (tool 28 + teul 63).
C1: V1 core 15 semantic owners audited; whole convergence remains partial.
C2: candidate ddonirang now reaches 11/15 workflows.
C3: lint moved to shared lang/tool authority; prior W1~W6 migrations preserved.
C4: lint private parser authority removed; other teul parser/runtime/value/canon residues remain.
C5: V1-required build/test/pack/publish teul dependency-zero remains OPEN.
C6: lint artifact/diagnostic parity PASS as scoped; whole CLI parity OPEN.
C7: final Windows/WASM/public projection revalidation remains OPEN.
C8: teul binary/package retirement, deletion inventory/review/Owner approval remain OPEN.
```

Reached candidate workflows are `run`, `check`, `build`, `canon`,
`project-normalize`, `project-discover`, `project-graph`, `project-symbols`,
`project-lock`, `currentline-run` and `lint`. Remaining are `project-run`,
`view`, `test` and `repl`.

## project-run Owner identity and concrete detail gap

Owner fixed the executable-neutral semantic identity to
`ddn.project-run.v1`. It does not select an executable/package name or legacy
alias. The existing product implementation already fixes the positive input,
summary schema, structured diagnostics, runtime state, WorkCost receipt and
artifact hash contracts.

Candidate implementation stopped before product mutation because two negative
input/materialization contracts are not fixed by existing executable evidence:

1. The current teul handler accepts `--virtual` together with positional
   `start` or `--project` and silently ignores the disk selector. No product
   test/pack fixes whether this combination must fail or preserve precedence.
2. `--out` currently creates parent directories and directly overwrites the
   target. No fixed contract establishes direct overwrite versus atomic
   replacement on failure.

Recommended decisions:

- input conflict: fail closed with `E_CLI_OPTION_CONFLICT` whenever `--virtual`
  is combined with positional `start` or `--project`; this prevents silent
  source-selection drift. The compatibility alternative is to preserve
  `--virtual` precedence and document ignored disk selectors.
- output materialization: preserve existing successful parent creation, but
  atomically replace the final artifact with no partial publish. The strict
  compatibility alternative is current direct overwrite.

Until those details are approved, `ddn.project-run.v1` is bound as the semantic
identity decision only; no candidate command, golden artifact, summary hash or
teul output was changed.

## Anti-meta and nonclaims

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED: explicit-profile lint on candidate frontdoor
NEW_TEST_ARTIFACT_COUNT: 0
EXISTING_TEST_REUSED_COUNT: 4 groups
META_TEST_CREATED: 0
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
ACTIVE_REVIEW_TASK_COUNT: 0
NEXT_PRODUCT_DECISION_ENABLED: project-run negative input/output contract
```

This handoff does not claim whole CLI convergence, teul semantic authority 0,
required dependency 0, project-run migration, public executable or command
membership, teul retirement/deletion approval, independent PASS, P0~P6
closure, V1 readiness, release, activation, legal clearance or Human PASS.
