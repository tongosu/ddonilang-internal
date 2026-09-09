# P3 Workbench saved-head Run official-frontdoor W1 handoff

## Status

- `P3_WORKBENCH_SAVED_HEAD_RUN_FRONTDOOR_IMPLEMENTED_UNDER_REVIEW`
- This is one nonvisual official-frontdoor vertical. It does not close whole P3, P4, P5, P6, V1, release, or Human PASS.

## Authority and lineage

- live internal CURRENT: v25.35.0 / RD-001~490
- `docs/ssot/CURRENT.md`: SHA-256 `d8224b35d8e10b134ad2c3cd6e94db7d9b32d21363515fa848df91e8972262aa`
- public Language SPEC: v0.6.0 / `publish/spec/CURRENT.md` SHA-256 `6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0`
- direct baseline: `d35a2c9952814c07376834f0dea42b2e053a848a`
- product/test fixed commit: `610a64e708bc966ec36cff100897da1b00efa653`
- fixed tree: `1478030b41955407e27e8c478bd3bb05b1b56cd5`
- merge count: 0

## Product workflow changed or unblocked

The existing Workbench official Run path now carries the saved server project HEAD through `buildRunArchiveDraft` as `expected_head_revision_id`. The path is:

```text
Workbench createServerRunArchive
  -> run_archive_adapter buildRunArchiveDraft/createRunArchive
  -> existing project HTTP API
  -> P2 transactional expected-head guard
```

If another writer advances the server HEAD after the Workbench save, the stale Workbench Run request fails closed before a server Run archive is inserted. Reopening the project refreshes the HEAD and the same official frontdoor can create the archive against the new revision.

## Exact fixed diff

- `solutions/seamgrim_ui_mvp/ui/workbench/persistence/run_archive_adapter.js`
- `solutions/seamgrim_ui_mvp/ui/workbench/workbench.js`
- `tests/run_seamgrim_project_run_prerequisite_check.py`

No RuntimeBridge, HostBridge, Rust product source, tracked WASM, visible copy/layout/style, `docs/ssot/**`, or `publish/spec/**` change is included.

## RED and direct product evidence

- pre-write RED: `P3_RED_EXPECTED_HEAD_NOT_FORWARDED`; the draft omitted `expected_head_revision_id` even when the caller supplied the saved HEAD.
- adapter/request-body focused check: PASS; draft and actual `createRunArchive` HTTP body both preserve `sgr_saved` exactly.
- JavaScript syntax for adapter and Workbench: PASS.
- Python compile for the reused prerequisite test: PASS.
- RuntimeBridge T1: PASS.
- HostBridge T2: PASS.
- SourceAnalysis T4 scoped baseline: PASS, with its existing seven semantic fallbacks unchanged and no broader P3 claim.

## Actual browser workflow

A task-owned localhost `ddn_exec_server` and a temporary project store were used with the actual Workbench page.

1. Workbench saved project HEAD `sgr_P62QCuRfT6Hy79YrVNKeLG9b`.
2. The server store was advanced independently to `sgr_external_head_drift` while the page retained the old HEAD.
3. Workbench Run showed `sealed runtime: 실행 실패`; server Run archive count remained 0.
4. Workbench reopened the project and displayed the new HEAD.
5. The next Run request created exactly one server archive whose `source_revision_id` was `sgr_external_head_drift`.

The example runtime later finalized that accepted archive as failed; that is an existing example/runtime outcome and is not used as a P3 execution-success claim. The admission and revision-custody claim is proven by the 0-to-1 archive transition and exact saved-head identity.

The task-owned server was stopped, its listener was removed, the browser tab was closed, and its temporary store was removed. Residue is 0.

## Scoped baseline event

The complete existing `run_seamgrim_project_run_prerequisite_check.py` stopped at its predecessor lifecycle pack because the old golden expects only `1`, while current P4 behavior also emits `마디` and `public_observation_trace_hash`. This unrelated golden was not rewritten under the P3 lease. The product-specific adapter portion of that existing test passed independently.

## Anti-meta and review custody

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: Workbench save/reopen/Run now rejects stale saved HEAD atomically
- `NEW_TEST_ARTIFACT_COUNT`: 0
- `EXISTING_TEST_REUSED_COUNT`: 4 focused runners/checks plus one actual browser workflow
- `META_TEST_CREATED`: 0
- `STOP_RULE_APPLIED`: yes; existing adapter/prerequisite test and official Workbench page were reused
- `NEXT_PRODUCT_DECISION_ENABLED`: whether P2+P3 saved-head custody may enter the next coherent rolling-review milestone
- `NEW_REVIEW_TASK_COUNT`: 0
- `NEW_REVIEW_WORKTREE_COUNT`: 0
- `REVIEW_BUNDLE_TARGET`: P2 local-project saved-head custody plus this P3 official-frontdoor consumer
- `REVIEW_NEEDED_NOW`: yes; this change closes an actual stale-writer race at the user Run frontdoor, but dispatch remains management-owned

## Open gates and nonclaims

Editable I1 full adoption, full P3 V25/default ingress, the existing T4 fallback debt, full snapshot/receipt coupling, P4 replay closure, P5 Windows RC/release, exact rights/license/distribution, P6 Owner Human Smoke, V1 membership/readiness, activation, and Human PASS remain OPEN. No independent PASS is self-declared.
