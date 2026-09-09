# 2026-08-30 DDN V1 P4 shared runtime trace default clean-break W1

- Session: DDN V1제품마감Codex
- Role: persistent V1 closure single product writer
- Authority: internal v25.35.0 / RD-001~490; public SPEC v0.6.0
- Baseline: `53c8c31854b906e22f205287d9408d10568ed2c9`
- Product fixed: `4bb9e81a26b1a9078aa50cf43900b812e9640e39`
- Product fixed tree: `5b17321a75d491002d801bd477becf6598c0f024`

## Change

Removed only the obsolete root `trace_tier: T-PATCH` default from `ddn.project.json`. Current RD-181 clean-break authority forbids carrying it forward as an active alias, while the exact successor five-axis physical schema remains OPEN.

## Verification

- baseline archive lineage pack RED: `E_SHARED_RUNTIME_OPTION_UNSUPPORTED`
- official native product runs: 5 existing inputs x 3 repeats, all exit0/stderr0 and case-local output byte identity PASS
- tool lib: 526/526 PASS
- root JSON/preserved policy fields: PASS
- diff check: PASS
- zero-match filtered command: discarded, not evidence

## Boundary

Generic pack output expectations and explicit historical `T-PATCH` fixtures need a separate evidence rebase. No new or edited test/pack/runner/checker/meta-test was created. No product code, tracked WASM, UI, SSOT, SPEC, membership, release, or activation change occurred.

Status: `P4_ACTIVE_ROOT_LEGACY_TRACE_DEFAULT_CLEAN_BREAK_IMPLEMENTED_UNDER_REVIEW`.
