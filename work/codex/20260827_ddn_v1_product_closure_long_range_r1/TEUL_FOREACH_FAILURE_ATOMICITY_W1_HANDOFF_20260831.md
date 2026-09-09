# teul foreach failure atomicity W1 handoff

## Scope and authority

- Persistent goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1`
- Live internal authority: SSOT v25.45.0 / RD-001~536
- Public Language SPEC: v0.6.0
- Authority successor impact: `UNAFFECTED_FOR_THIS_INTERNAL_FAILURE_ATOMICITY_SLICE`
- Review PASS bound before this slice:
  `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf`
  (`PASS_TARGET_BOUND` for the CLI test shared-authority target only)
- Product baseline: `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf`
- Product fixed commit: `873d3cb236e9f7ab40307bc55c305861e2d7aeef`
- Product fixed tree: `bf753c9d47c1d3706b27da2531aa619ea1c85309`
- Direct lineage: yes; merge count: 0

## User workflow changed or unblocked

An INTERNAL/DEFERRED teul runtime execution that fails inside `foreach` no
longer leaks the current-item binding into the failed result, a later rerun, or
an enclosing loop. Existing outer bindings are restored and bindings created
only for iteration are removed. Failure output remains atomic in the covered
call-error case.

No public command membership, executable name, package name, alias, source
syntax, diagnostic spelling, wire schema, WASM export or Workbench UI surface
changed.

## Exact FILE_OWNER and product diff

The exclusive product write was limited to:

```text
tools/teul-cli/src/runtime/eval.rs
```

At the fixed commit:

- Git blob: `fbb159549b6f6bd2952cd3c2f68ca1894ac9d4ef`
- checkout bytes: 823,200
- checkout SHA-256:
  `9be82063008984768df94c13b8d9695540cec20a8e697be2e125433092c0db6c`
- implementation: replace the error-propagating `?` at the foreach body seam
  with explicit error handling that restores the pre-loop binding or removes
  the iteration-only binding before propagating the original error.

Product source diff outside this file: 0. Test/pack/tracked-WASM/UI/SSOT/SPEC
diff: 0.

## RED, GREEN and regression evidence

### Product-facing RED before implementation

Existing filter `foreach_` executed 13 existing Rust product tests:

- PASS: 8
- FAIL: 5
- exact failures:
  - `failed_foreach_rerun_does_not_retain_item_binding`
  - `foreach_body_call_error_restores_binding_and_failure_output_is_atomic`
  - `foreach_body_error_restores_shadowed_binding`
  - `foreach_scope_removes_new_binding_after_body_error`
  - `nested_foreach_error_restores_same_name_and_distinct_outer_bindings`

### Fixed GREEN

- Existing `foreach_` tests: 13/13 PASS.
- Full `teul-cli` binary suite: 1,045 PASS / 9 FAIL.
- The predecessor custody was 1,040 PASS / 14 FAIL; all five foreach failures
  are removed and the remaining nine are the pre-existing legacy-boim,
  shared-right-assignment/frontdoor and assignment-atomicity set.
- Official tracked WASM freshness: PASS. This teul-private source is not a
  tracked-WASM source family and tracked WASM diff is 0.

### Risk-relevant mutation

One direct mutation removed only the new error-path restoration:

- RED: `foreach_body_error_restores_shadowed_binding` 0/1, with leaked
  `Some(Str("첫째"))` instead of the outer `Some(Str("바깥"))`.
- Exact restore SHA-256:
  `9be82063008984768df94c13b8d9695540cec20a8e697be2e125433092c0db6c`.
- Restore GREEN: existing `foreach_` tests 13/13.
- Mutation residue: 0.

No new test, pack, runner, checker or meta-test was created.

## C0 through C8 impact

| Gate | Status after this fixed target |
|---|---|
| C0 | Historical 28 tool + 63 teul = 91 inventory remains custody. |
| C1 | `ddn.project-run.v1` remains fixed; executable/package/alias choices remain OPEN. |
| C2 | Shared source/canon/preprocess authority is unchanged. This slice removes no shared authority and adds no parser family. |
| C3 | Official candidate remains 12/15 audited workflows; `view` and `repl` remain open and public `test` spelling is not inferred. |
| C4 | INTERNAL/DEFERRED teul physical source remains custody. This slice improves its fail-closed behavior only. |
| C5 | Bounded V1-required build/test/pack/publish teul execution dependency remains 0. |
| C6 | Whole command/source/diagnostic/state/artifact parity remains OPEN. |
| C7 | Applicable native regression and tracked-WASM freshness pass; no new WASM/Workbench surface applies. |
| C8 | Physical retirement/deletion remains Owner-gated and is not claimed. |

## Anti-meta and review state

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: failed foreach execution no longer
  leaks its iteration binding.
- `NEW_TEST_ARTIFACT_COUNT`: 0
- `EXISTING_TEST_REUSED_COUNT`: 13 focused + 1,054 full-suite cases
- `META_TEST_CREATED`: 0
- `STOP_RULE_APPLIED`: yes; one product file and one risk mutation only
- `NEXT_PRODUCT_DECISION_ENABLED`: the retained INTERNAL/DEFERRED runtime can
  be kept as reversible custody without carrying this known state-leak defect.
- `NEW_REVIEW_TASK_COUNT`: 0
- `NEW_REVIEW_WORKTREE_COUNT`: 0
- `REVIEW_BUNDLE_TARGET`: next coherent CLI convergence/retirement milestone
  using the existing rolling reviewer only.
- `REVIEW_NEEDED_NOW`: yes for this product-behavior change, but no reviewer
  was created or dispatched by this handoff.

## Open gates and nonclaims

The public PathIR XP-02/M12 physical contract remains
`CONCRETE_DETAIL_GAP_DETECTED`; no public registry, wire field, raw-DDN syntax,
CLI option, WASM transport or Workbench mapping was invented. `view` and `repl`
still require product/public contract decisions. The remaining nine teul test
failures are not silently reclassified as PASS.

This is `TEUL_FOREACH_FAILURE_ATOMICITY_IMPLEMENTED_UNDER_REVIEW` only. It is
not whole C0~C8 closure, teul semantic-authority zero, physical retirement,
PathIR P1 PASS, ERQ closure, V1 membership/readiness/release/activation, legal
approval, Owner Human Smoke or Human PASS.
