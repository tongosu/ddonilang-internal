# [셈그림Codex -> 셈그림검증ClaudeCode] T5H browser/fallback readiness targeted review 요청

```text
PROGRAM_ID: DDN_PRODUCT_LONG_RANGE_CANONICAL_VIEW_CONVERGENCE_R1
REVIEW_SCOPE: T5H_BROWSER_FALLBACK_READINESS_EVIDENCE_R1
BASELINE: a684b0d058ee96e89935eb07df977e97b6f3bbab
PRODUCT_FIXED_HEAD: 290f2095d67882f9de26e0b029632399a9f4198e
EXPECTED_PRODUCT_DIFF: 0
ALLOWED_VERDICTS: PASS / PASS_WITH_FOLLOW_UP / REWORK
```

Use an isolated detached worktree at the exact fixed HEAD. Do not modify product, test, pack, SSOT, SPEC, or tracked WASM files.

## Required determinations

1. Does the matrix enumerate exactly the existing fourteen active keys/families with no registry-only promotion?
2. Does every family map exactly once to an actual browser group and an existing golden/mutation semantic-fallback evidence group?
3. Are applicable surfaces byte-for-byte equal to the pre-existing T5H consumer matrix, with exact complement cells recorded as `NOT_APPLICABLE`?
4. Does the new T5B/T5C browser runner consume the existing canonical owner and existing graph/space2d presentation modules without creating a third semantic/view abstraction?
5. Does that runner prove exact golden parity, console order/value, graph render structure, and space2d render structure for the three previously missing browser-family probes?
6. Do all five browser groups, the representative curriculum browser runner, and the existing 13-command cross-family aggregate reproduce using only locally installed Playwright and the supplied source-built WASM?
7. Are semantic-fallback evidence mappings grounded in actual golden/mutation assertions rather than marker-only completion claims?
8. Are random-origin stdout hashes correctly limited to per-run custody rather than deterministic cross-run identity?
9. Are T5G plain PASS, T5H status totality, per-surface product browser parity, T5H closure, and T5I closure all still unclaimed?
10. Are product, SSOT, public SPEC, and tracked WASM diffs exactly zero?

## Reproduction

```powershell
$env:DDN_T5F_SOURCE_WASM_DIR = '<current source-built WASM directory>'
$env:DDN_LOCAL_PLAYWRIGHT_NODE_MODULES = '<local node_modules containing playwright and playwright-core>'
node tests/seamgrim_canonical_view_t5h_browser_fallback_readiness_runner.mjs
git diff --check
git status --short
```

The verdict applies only to this dependency-independent evidence slice. A plain `PASS` does not close T5G or T5H and does not authorize the dependent status-totality product correction.
