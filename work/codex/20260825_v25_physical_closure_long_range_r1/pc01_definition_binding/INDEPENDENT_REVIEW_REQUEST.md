# [언어물리Codex -> 독립검토ClaudeCode] V25 PC-01 Definition / Binding 읽기 전용 검토 요청

```text
PROGRAM_ID: DDN_V25_PHYSICAL_CLOSURE_LONG_RANGE_R1
SLICE: PC-01_DEFINITION_BINDING
START_BASELINE: 55f57623ab419d9ccb99b9e0527efa912eaccee3
PRODUCT_IMPLEMENTATION_COMMIT: cf97f134aebc4889bd3e13ff4850cbf76ca4c2d6
FIXED_REVIEW_TARGET: 3ac1cefbffa4c00857f99debad3b1aad24ed08ea
REQUESTED_VERDICT: PASS / PASS_WITH_FOLLOW_UP / REWORK
REVIEW_MODE: FIXED_HEAD_READ_ONLY
```

## Required independent decisions

1. `:=` lexes and parses as Definition while `<-` remains Binding/Rebinding.
2. `Stmt::Definition` and `Stmt::Mutate` stay physically and semantically distinct.
3. V25 top-level old `=` is not a silent alias and receives the migration-required diagnostic.
4. V25 `채비` cannot introduce a name through `<-`.
5. Canon emits the correct symbol for each category and parse-canon-parse preserves category identity.
6. The executable pack's JSONL ledger is the test owner and all positive/negative cases are exercised.
7. The explicit V25 `DdnRunner` path evaluates Definition then Rebinding to output `2` without turning Definition into root mutation.
8. All three supplied mutations are independently reproducible as RED and restoration leaves residue 0.
9. Existing pre-V25 product behavior is preserved; default frontdoors are not silently switched in PC-01.
10. `docs/ssot/**`, `publish/spec/**`, and tracked WASM are unchanged.

## Suggested commands

Set offline Cargo and an isolated external `CARGO_TARGET_DIR`, then run:

```text
cargo test -p ddonirang-lang
cargo test -p ddonirang-tool --lib v25_definition_then_rebinding_executes_as_distinct_local_operations -- --nocapture
node tests/ddn_v25_pc01_definition_binding_mutation_runner.mjs
cargo check --workspace
git diff --check 55f57623ab419d9ccb99b9e0527efa912eaccee3..3ac1cefbffa4c00857f99debad3b1aad24ed08ea
```

Do not modify product code or reinterpret a harness/logical oracle as product
support. A plain PASS is required before the dependent PC-02 semantic slice may
start.
