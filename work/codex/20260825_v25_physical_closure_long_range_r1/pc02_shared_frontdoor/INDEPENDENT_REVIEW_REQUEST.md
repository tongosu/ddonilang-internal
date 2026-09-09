# [언어물리Codex -> 독립검토ClaudeCode] V25 PC-02 Shared Frontdoor 읽기 전용 검토 요청

```text
PROGRAM_ID: DDN_V25_PHYSICAL_CLOSURE_LONG_RANGE_R1
SLICE: PC-02_SHARED_FRONTDOOR_ASSIGNMENT_AUTHORITY
START_BASELINE: f03955c01963646c0095fcffb14f9f162c9655ce
PRODUCT_IMPLEMENTATION_COMMIT: 04566a2426b56084f4449b363530192aa1166d2a
REQUESTED_VERDICT: PASS / PASS_WITH_FOLLOW_UP / REWORK
REVIEW_MODE: FIXED_HEAD_READ_ONLY
```

## Required independent decisions

1. Native/tool, official CLI, teul-cli, WASM, and Workbench query consume the same PC-01 V25 Definition/Binding categories and canon.
2. Default V25 paths reject old `=` and category misuse without legacy parser fallback.
3. Teul `run`/`canon` do not use their own assignment parser or canon passthrough for V25 input.
4. Pre-V25 behavior is reachable only through named commands, `--source-epoch pre-v25`, or `DdnWasmVm.fromPreV25Source`.
5. P1-P3 and N1-N4 are all driven by the JSONL oracle and actual product APIs.
6. Native, official CLI, teul, WASM, and Workbench projections agree on categories, canon, runtime, and diagnostics.
7. M1-M5 independently produce RED and exact restoration produces GREEN with residue 0.
8. PC-01 and relevant T1/T2/T4/T4h/T5B-T5F regressions remain green.
9. Tracked WASM is unchanged and honestly classified stale; source-built bindings contain the new APIs.
10. `docs/ssot/**` and `publish/spec/**` diff is zero, ancestry is linear, and merge count is zero.

Do not modify product code or issue a closure outside the fixed reviewed scope.
A plain PASS must be bound before PC-05 implementation starts.
