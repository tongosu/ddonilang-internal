# BOGAE-IMPL-04 Workbench view selection independent review R1

## Verdict

```ini
VERDICT = PASS_TARGET_BOUND
BLOCKING_FINDINGS = 0
TARGET_STATUS = CLOSED_TARGET_BOUND
```

This verdict is bound only to the fixed BOGAE-IMPL-04 Workbench view-selection target below. It does not reopen BOGAE-IMPL-01 and does not claim whole Bogae, V1 readiness, release, public support, browser behavior, or Human PASS.

## Live authority

- Internal SSOT at review: `v25.82.0 / RD-001~618`.
- Public Language SPEC: `v0.7.0`.
- The live successor records predecessor semantic-row drift `0/617`; the BOGAE-IMPL-04 premise remains compatible with the unchanged RD-608~609 Bogae architecture rows.
- BOGAE-IMPL-01 product `8c0781d1ac10dabea4b4e5699f6b26823bc23dc4` and independent review `ffcfc8b8ad5fdbbf877757c16d54474e2f5b74fc` remain closed and were not modified or re-reviewed.

## Exact custody

```ini
PRODUCT = 2ace20a8bb506748bb5ae43746601c5926f2361c
PRODUCT_TREE = 385d964eb7dd14b195e21f01387f05806e0d3303
PRODUCT_PARENT = ffcfc8b8ad5fdbbf877757c16d54474e2f5b74fc

HANDOFF = 09a3cf03b9e9fe62a67be0afedef2f64360c2883
HANDOFF_TREE = ee2999039a6aca8575ffd463673b95cc165960a5
HANDOFF_PARENT = 2ace20a8bb506748bb5ae43746601c5926f2361c

MERGE_COUNT = 0
AUTHOR_COMMITTER = tongosu <tongosu@myarts.kr>
```

The product changes exactly two paths:

1. `solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_payload.js`
   - blob `2b6cd6ab6a0ddd5c932f5c8795ad9f5295a3db74`
   - SHA-256 `86EDC8DD9D2EFCB5920AD847FFACB7F34601149F620C58057D57F540054B2116`
2. `tests/seamgrim_workbench_semantic_view_payload_runner.mjs`
   - blob `526a60ad6d434d55290e5ce3be4759d0a554386a`
   - SHA-256 `E5D44C0919554C69148348944F962677521CE5AA02495643C21E06E5F6C821CA`

Unexpected, SSOT, public SPEC, parser, runtime, renderer, state-hash, and public-wire product paths changed: `0`.

## Static review

- `project.primaryView` is no longer a missing-binding fallback inside the semantic payload builder.
- Numeric observations are carried as committed evidence but do not select a view family.
- Candidate admission is restricted to available `workbench_*` canonical results with the existing exact provider `ddonirang_tool.wasm_runtime`, provenance `native_authoritative_structured_result`, and matching family/key.
- Selection succeeds only when the candidate count is exactly one and the explicit requested family matches it.
- Zero candidates, multiple candidates, and sole-candidate family mismatch yield non-success binding states.
- Multiple-candidate resolution clears the family and canonical key, so object/source order cannot choose first or last.
- Selection configuration remains outside the runtime state hash, and committed frame/state identity is copied unchanged.
- New semantic identity count: `0`.

## Dynamic verification

All of the following passed in the detached review worktree:

- JavaScript syntax checks for both exact product paths.
- `tests/seamgrim_workbench_semantic_view_payload_runner.mjs`.
- `tests/seamgrim_workbench_semantic_view_renderer_runner.mjs`.
- console/graph canonical payload runner.
- console-grid/grid2d canonical payload runner.
- space2d canonical payload runner.
- table/text/structure canonical payload runner.
- independent zero-candidate and wrong-provider fail-closed probes.
- product and handoff `git diff --check`.

Required cases were directly asserted by the focused runner:

```ini
BIC_WORKBENCH_02 = PASS
BIC_UNSUPPORTED_01 = PASS
BIC_MULTIVIEW_02 = PASS
COMMITTED_FRAME_STATE_HASH_DRIFT = 0
SOURCE_ORDER_UI_HEURISTIC_WINNER = 0
```

The four-family runner reports `line: renderer status canonical_unsupported` with its required source-built WASM fixture. The same failure and exit status were reproduced at clean predecessor `ffcfc8b8`; it is pre-existing and outside this two-path target finding set.

## Independent mutations

Each mutation was applied alone, produced RED in the focused runner, and was exactly restored before the next mutation.

1. Restored `project.primaryView` as an implicit fallback.
   - RED: `project/UI default selected a view without an explicit binding`.
2. Accepted the first candidate whenever candidate count was greater than zero.
   - RED: `ambiguous typed views selected a family`.
3. Accepted a sole candidate without checking the explicit family match.
   - RED: `unresolved explicit family identity was not preserved for typed failure`.

After every restore and at final custody:

```ini
FIXED_SOURCE_BLOB = 2b6cd6ab6a0ddd5c932f5c8795ad9f5295a3db74
FIXED_SOURCE_SHA256 = 86EDC8DD9D2EFCB5920AD847FFACB7F34601149F620C58057D57F540054B2116
FOCUSED_RUNNER = GREEN
RENDERER_RUNNER = GREEN
```

## Boundary

No product correction is required for this target. The verdict closes only numeric/default/ambiguous Workbench view selection under the existing typed canonical Workbench provider/binding authority. Browser execution, whole Workbench, renderer inventory, public activation, V1 readiness/release, and Human PASS remain unclaimed.
