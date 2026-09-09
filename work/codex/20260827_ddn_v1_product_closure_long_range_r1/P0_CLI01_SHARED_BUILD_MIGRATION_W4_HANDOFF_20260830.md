# DDN V1 CLI convergence — shared build migration W4

Date: 2026-08-30
Goal: existing `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1`
Status: `IMPLEMENTED_UNDER_COHERENT_MILESTONE_REVIEW`

## Fixed lineage

- live CURRENT: internal v25.40.0 / RD-001~515; public SPEC v0.6.0
- authority impact: `ADDITIVE`; no SSOT/SPEC edit or status promotion
- baseline / W3 handoff: `3b5630b0b7599afd0771174b6abcabad6e161224`
- product/test fixed: `b4e738b9dc551b1079c79da9e41269c77f99c02c`
- fixed tree: `75c1087ac82a66229f9142073b84b567e60e46b1`
- direct parent: exactly `3b5630b0b7599afd0771174b6abcabad6e161224`
- merge count from P5 handoff `ee9d28bb`: 0

Exact fixed diff:

- `tool/src/bin/ddonirang.rs`
- `tests/run_v1_core_supported_ingress_w1.py`

## User workflow and authority convergence

Historical `teul-cli build` calls the exact same private `cli::check::run`
handler as historical `check`; it is not a separate compiler or artifact
pipeline. The candidate already has reviewed supported-profile shared analysis
for `check`. This vertical therefore adds only:

```text
ddonirang build <source.ddn> --source-profile v1-core-v25
  == ddonirang check <source.ddn> --source-profile v1-core-v25
  -> tool::source_analysis::analyze_source
```

No compiler, parser, schema writer, fallback or test-only lowering was added.
The candidate build result is the same structured analysis payload as check.
Missing/unknown profiles use the existing fail-closed profile diagnostics.

The historical private check/build implementation and schema side effect are
not promoted into the V1 candidate. They remain teul retirement residue until
dependency classification and deletion gates are satisfied.

## RED, GREEN and fixed evidence

- RED at baseline: candidate `build` -> `E_CLI_COMMAND_UNKNOWN build`, exit 2
- candidate unit tests: 4/4 PASS
- build/check positive structured payload: byte-identical, SHA-256
  `9fa8ce5d86fcc63da743d670f119c0671cbc8bde9ada38eb8bebc84e24c7adaf`
- build deterministic repeats: 3/3 identical
- build omitted-profile failure: exit 2 / `E_SOURCE_PROFILE_REQUIRED`
- reused P1-A runner in a clean external target:
  - native 7 PASS
  - native/WASM exact 2 PASS
  - tracked-WASM cases 10 PASS
  - candidate CLI positive 4 / negative 4 PASS
- initial reused target produced duplicate `ddonirang_lang` crate-identity
  E0271/E0308 errors from cross-checkout build residue; a fresh external target
  reproduced GREEN and classified the event as build-environment contamination,
  not a product failure
- new pack/runner/checker/framework/meta-test: 0

## C0~C8 delta

- C0 historical registry: unchanged, 28 + 63 = 91 identities
- candidate frontdoor: 9 commands
- C3: `IN_PROGRESS_9_OF_15`
- newly reached historical core candidate: `build`
- C1/C4/C5/C6/C7/C8: unchanged OPEN/proposal/queued boundaries

The nine candidate commands are `run`, `check`, `build`, `canon`,
`project-normalize`, `project-discover`, `project-graph`, `project-symbols` and
`project-lock`.

## Remaining six core candidates

The fixed-object handler audit found no further write-safe command without a
semantic/detail decision or broader product-authority convergence:

| command | current blocking authority |
|---|---|
| `project-run` | artifact embeds `teul-cli project-run`; neutral wire identity and checkout materialization remain unresolved |
| `currentline-run` | shared cell compiler is followed by private teul run/state path and a hardcoded teul command identity |
| `view` | private teul view/Bogae/UI orchestration; visible behavior and launch policy are outside this lease |
| `test` | mixes product test, golden recorder and WASM smoke harness; exact V1 public command membership is unresolved |
| `lint` | private lexer/parser plus legacy-term patch contract; shared diagnostic/patch authority is absent |
| `repl` | private state/runtime execution path; no shared stateful REPL transaction API |

`SEMANTIC_SPEC_GAP_DETECTED` for the next product vertical:

1. `project-run`: bind a versioned neutral semantic frontdoor identity,
   independent of executable spelling. Recommended because it unblocks shared
   execution while preserving the final binary/alias decision.
2. `lint`: first define a shared diagnostic/patch product API, then make both
   candidate and predecessor consumers. Larger scope but removes a real private
   parser owner.
3. `repl/currentline-run`: first define a shared stateful execution transaction
   contract. Highest runtime/compatibility risk; do after project-run.

No exact FILE_OWNER is issued for these blocked product paths. The next safe
non-mutating action is management/Owner selection of the neutral project-run
identity. Dependency classification and already-migrated command test routing
may continue only where it changes a V1-required build/test/pack decision.

## Anti-meta, review and nonclaims

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: supported V25 source can now be built
  through the shared candidate without the legacy binary
- `NEW_TEST_ARTIFACT_COUNT`: 0
- `EXISTING_TEST_REUSED_COUNT`: candidate unit and P1-A ingress runner
- `META_TEST_CREATED`: 0
- `ACTIVE_REVIEW_TASK_COUNT`: 0 for the CLI bundle
- `NEW_REVIEW_TASK_COUNT`: 0
- `NEW_REVIEW_WORKTREE_COUNT`: 0
- `REVIEW_BUNDLE_TARGET`: W2 project-normalize + W3 project inspection/lock +
  W4 build at one later fixed CLI milestone, using the existing rolling reviewer

This handoff does not approve final executable naming, public command
membership, legacy alias duration, internal/deferred placement, physical teul
deletion, C3~C8 closure, P0~P6 closure, V1 readiness/release/activation,
legal/distribution status, Owner Human Smoke or Human PASS.
