# DDN V1 CLI convergence — project inspection/lock migration W3

Date: 2026-08-30
Goal: existing `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1`
Status: `IMPLEMENTED_UNDER_COHERENT_MILESTONE_REVIEW`

## Authority and fixed lineage

- live internal CURRENT: v25.40.0 / RD-001~515, Owner final 2026-08-30
- requested v25.35: live predecessor; successor impact for this vertical is `ADDITIVE`
- public Language SPEC: v0.6.0, unchanged
- product baseline / prior handoff: `fdf4993488d09c8b9a945d2a7be10c66b1910213`
- product/test fixed: `a4ca66171df3b2cbc2700ab73d867c01bb76dcb6`
- fixed tree: `a5023dfbbb4a3a16fce42d8897071db547e0658b`
- fixed parent: exactly `fdf4993488d09c8b9a945d2a7be10c66b1910213`
- P5 fixed/handoff custody `d47ed2df -> ee9d28bb` was preserved and not rebuilt
- merge count from `ee9d28bb`: 0

## Product value and exact diff

Before this fixed commit the candidate shared CLI rejected `project-graph` with
`E_CLI_COMMAND_UNKNOWN`, exit 2. The following user workflow now runs through
the existing `tool::local_project` authority without importing or falling back
to `teul-cli`:

```text
ddonirang project-discover
  -> ddonirang project-graph
  -> ddonirang project-symbols
  -> ddonirang project-lock [--frozen]
```

The four commands are adapters over the already shared APIs:

- `discover_virtual_project_root_json` / `discover_disk_project_root_json`
- `build_project_graph_json`
- `build_project_symbol_boundary_json`
- `build_project_gaji_lock_json` / `verify_project_gaji_lock_json`

No parser, runtime, value, canon or fallback authority was added. Ambiguous
virtual/disk discovery inputs and unsupported output-materialization options
fail closed rather than silently selecting a path.

Exact product/test fixed diff:

- `tool/src/bin/ddonirang.rs`
- `tests/run_ddn_local_project_graph_check.py`

The existing runner was parameterized in place: only discover/graph/symbols/
lock calls moved to the candidate binary. Existing `project-run` and linked
`run --summary-json` calls remain on the historical executable until their
separate blockers are resolved. New pack, runner, checker, framework and
meta-test count is 0.

## RED, GREEN, parity and fixed reproduction

- product RED: `ddonirang project-graph <fixture>` -> unknown command, exit 2
- candidate binary unit tests: 4/4 PASS
- reused project inspection/lock checks: 8/8 PASS
- root discovery, graph, symbols/re-export and gaji lock native/tracked-WASM
  structured payload checks all PASS
- current teul adapter vs candidate: 6/6 exact exit/stdout/stderr byte parity
- the six parity cases each repeated three times with identical payloads
- representative graph failure stayed fail-closed at exit 2
- existing local-project normalization CLI/WASM runner: PASS
- shared local-project library regression: 40/40 PASS
- post-commit clean fixed-head reproduction: candidate 4/4 and product checks
  8/8 PASS; tracked diff after reproduction 0
- no mutation harness was added: the actual missing-command RED plus existing
  outside-root/private-symbol/module/lock failure cases cover the concrete risk

The complete historical runner cannot be claimed as whole-GREEN at this fixed
checkout. Its baseline phase refers to an absent historical report, and the
later `project-run` phase reproduces an existing checkout/text materialization
mismatch. Neither path was changed by this commit. They remain explicit
rebase/product-custody work rather than being hidden or bypassed.

## C0~C8 actual status

The source registry remains 28 `ddonirang-tool` commands plus 63 `teul-cli`
commands = 91 historical identities. The later candidate frontdoor is tracked
separately and now exposes eight commands.

| gate | actual status |
|---|---|
| C0 | `VERIFIED_CURRENT_SOURCE`: historical 28 + 63 = 91; candidate 8 |
| C1 | `CONCRETE_DETAIL_GAP_DETECTED`: final executable name and legacy alias duration remain Owner-open |
| C2 | `LIMITED_SCOPE_CLOSED`: shared canon/preprocess authority remains bound |
| C3 | `IN_PROGRESS_8_OF_15`: run/check/canon/project-normalize/discover/graph/symbols/lock have shared candidate reachability; migrated project options are stdout-only except lock `--frozen` |
| C4 | `PROPOSAL_ONLY`: 15 V1-core migration, 15 move-to-shared and 33 internal/deferred custody; public membership is not inferred |
| C5 | `NOT_STARTED`: selected extended-command migration not inferred |
| C6 | `OPEN`: compatibility/golden migration and alias duration not selected |
| C7 | `QUEUED_NOT_DISPATCHED`: coherent CLI milestone review must use the existing rolling reviewer only |
| C8 | `OPEN`: public projection excludes teul, but repository dependency 0 and independent PASS are incomplete |

The exact 15 historical V1-core candidates remain:

`project-normalize`, `project-discover`, `project-graph`, `project-symbols`,
`project-lock`, `project-run`, `run`, `currentline-run`, `view`, `check`,
`test`, `build`, `lint`, `repl`, `canon`.

## Teul residue and required-dependency state

- private parser: 7 files / 9,531 lines; 22 Rust consumer files
- private runtime: 7 files / 25,141 lines; 9 Rust consumer files
- private core/value: 11 files / 5,350 lines; 10 consumer files
- private canon owner remains 0 at `tools/teul-cli/src/canon.rs` because it is
  only a shared re-export; private CLI/canon/check/lint/parser/runtime/value
  consumers remain retirement residue
- repository CI explicit reference: 1 workflow file
- tracked test explicit-reference files: 190
- tracked pack explicit-reference files: 367
- tracked publish explicit-reference files: 50 overall; `publish/v1/**`: 0
- public Windows candidate/source projection teul artifact/source count: 0
- 33 internal/deferred commands remain in physical custody and were neither
  deleted nor promoted

The required/deferred classification of the remaining references is not yet
complete, so V1-required build/test/pack dependency 0 is not claimed.

## Concrete detail gate and next safe slice

`project-run` is not silently migrated. Its current structured artifact embeds
`frontdoor = "teul-cli project-run"`; changing that value would decide a
frontdoor/wire identity while the final public executable name is Owner-open.
The same fixed checkout also reproduces text materialization drift in that
workflow.

`CONCRETE_DETAIL_GAP_DETECTED` options:

1. Keep the literal historical identity until final executable naming is bound.
   Lowest compatibility risk, but blocks migration and retirement.
2. Introduce a neutral versioned semantic frontdoor identity independent of
   executable spelling. Recommended: preserves deterministic artifact meaning
   while allowing executable/alias decisions later; requires an explicit wire
   successor and compatibility check.
3. Bind the candidate spelling directly. Smallest code change, but prematurely
   decides the public executable identity and is not authorized here.

Until that decision, the next non-overlapping safe lane is a fixed-object call
graph audit of `currentline-run/view/check/test/build/lint/repl` to identify one
command whose semantics already reside entirely in shared `lang/tool` APIs.
Any next product FILE_OWNER must be issued from that RED; no private semantic
implementation or new test family may be inferred.

## Anti-meta and review custody

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: four local-project inspection/lock
  operations no longer require the legacy executable
- `NEW_TEST_ARTIFACT_COUNT`: 0
- `EXISTING_TEST_REUSED_COUNT`: 3 test surfaces (candidate unit, local-project
  graph runner, local-project normalize runner), plus focused library filter
- `META_TEST_CREATED`: 0
- `STOP_RULE_APPLIED`: yes; no hash/receipt tamper suite or review-of-review
- `NEXT_PRODUCT_DECISION_ENABLED`: select the next shared-authority CLI family
  and separately decide the neutral project-run artifact identity
- `ACTIVE_REVIEW_TASK_COUNT`: 0 for this CLI milestone
- `NEW_REVIEW_TASK_COUNT`: 0
- `NEW_REVIEW_WORKTREE_COUNT`: 0
- `REVIEW_BUNDLE_TARGET`: remaining coherent V1 CLI convergence milestone,
  using the existing rolling reviewer only after management dispatch

## Nonclaims

This handoff does not decide the final executable name, legacy alias duration,
public command membership, internal/deferred command placement or incompatible
migration. It does not close project-run, C3~C8, teul retirement/deletion,
whole P0~P6, V1 readiness, Windows/public release, activation, legal/
distribution gates, Owner Human Smoke or Human PASS.
