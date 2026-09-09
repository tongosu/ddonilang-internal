# [셈그림Codex -> 셈그림검증ClaudeCode] T5H view-plan boundary targeted review 요청

```text
PROGRAM_ID: DDN_PRODUCT_LONG_RANGE_CANONICAL_VIEW_CONVERGENCE_R1
REVIEW_SCOPE: T5H_VIEW_PLAN_PRESENTATION_ONLY_BOUNDARY_AUDIT_R1
BASELINE: 2c9cfc2033c30badf40b4c7c920c7ce0db1c680b
PRODUCT_FIXED_HEAD: dfd10660b2ac8ccc64f0a4d362f7d85d08d8c969
EXPECTED_PRODUCT_DIFF: 0
ALLOWED_VERDICTS: PASS / PASS_WITH_FOLLOW_UP / REWORK
```

Use a clean detached worktree at the exact fixed HEAD and do not modify product, tests, pack, SSOT, SPEC, or tracked WASM.

## Required determinations

1. Is `semantic_view_payload.js` still the sole canonical owner with no dependency on `view_plan_runtime.js`?
2. Does the adapter avoid canonical payload construction and canonical schema emission?
3. Is `screens/run.js` the exact sole product caller, with an explicit available canonical space2d base selection?
4. Are authoritative point and shape identity/order/value preserved under presentation composition?
5. Does the no-base path remain presentation-only, state-hash-excluded, and canonical-synthesis false?
6. Does the no-base path create semantic world points `0`?
7. Does graph cursor enrichment preserve existing series and create no missing base series?
8. Do the four existing T5B/T5C golden/mutation runners reproduce?
9. Do both new mutations become RED and restore to GREEN with residue `0`?
10. Does clean-detached reproduction pass with residue `0`?
11. Are product, SSOT, public SPEC, and tracked WASM diffs zero?
12. Are T5G, T5H, T5I, public ABI, Native implementation, and release closure still unclaimed?

## Reproduction

```powershell
node tests/seamgrim_canonical_view_t5h_view_plan_boundary_audit_runner.mjs
node tests/seamgrim_canonical_view_t5h_view_plan_boundary_audit_mutation_runner.mjs
git diff --check
git status --short
```

A plain `PASS` closes only this boundary evidence slice. It does not close T5G or T5H and does not authorize dependent product correction.
