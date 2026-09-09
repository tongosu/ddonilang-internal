# [셈그림Codex -> 셈그림검증ClaudeCode] T5H per-surface evidence strength targeted review 요청

```text
PROGRAM_ID: DDN_PRODUCT_LONG_RANGE_CANONICAL_VIEW_CONVERGENCE_R1
REVIEW_SCOPE: T5H_PER_SURFACE_EVIDENCE_STRENGTH_AUDIT_R1
BASELINE: 16f9d3a3b1172aff7c559db45f49551e63a95047
PRODUCT_FIXED_HEAD: b0b8b1d7d0504e56ac4473fe6a9fd13cefee08ec
EXPECTED_PRODUCT_DIFF: 0
ALLOWED_VERDICTS: PASS / PASS_WITH_FOLLOW_UP / REWORK
```

Use an isolated detached worktree at the exact fixed HEAD. Do not modify product, tests, pack, SSOT, SPEC, or tracked WASM.

## Required determinations

1. Does the matrix enumerate exactly the 42 cells currently declared applicable by the pre-existing T5H consumer matrix?
2. Does every cell cite an executable runner and an exact source assertion marker rather than a narrative-only claim?
3. Are the fifteen product-function parity cells honestly distinguished from the four actual Workbench product browser verticals?
4. Are the two T5G product-browser/serialization boundaries and two serialization-only cells bounded without claiming positive available product execution where only fixture availability exists?
5. Are the three Bogae/Nurimaker presentation ports kept distinct from canonical product-surface parity?
6. Are the four Workbench-family Run cells correctly labeled `SYNTHETIC_ALIAS_ONLY`, with no evidence that the current Run renderer consumes those families?
7. Are exactly twelve historical Playground cells held at `OWNER_DECISION_REQUIRED` with no silent Workbench-Studio equivalence?
8. Do all nine referenced runners reproduce with the supplied local artifacts and network install `0`?
9. Do both independent structural mutations produce RED and restore to GREEN with residue `0`?
10. Are T5G plain PASS, T5H status totality, per-surface parity closure, public ABI, Native readiness, and SSOT/SPEC promotion all still unclaimed?
11. Are product, SSOT, public SPEC, and tracked WASM diffs zero?

## Reproduction

```powershell
$env:DDN_T5F_SOURCE_WASM_DIR = '<current source-built WASM directory>'
$env:DDN_LOCAL_PLAYWRIGHT_NODE_MODULES = '<local node_modules containing playwright and playwright-core>'
node tests/seamgrim_canonical_view_t5h_surface_evidence_audit_runner.mjs
node tests/seamgrim_canonical_view_t5h_surface_evidence_audit_mutation_runner.mjs
git diff --check
git status --short
```

A plain `PASS` closes only this evidence-strength audit. It does not close T5G or T5H and does not authorize dependent product correction.
