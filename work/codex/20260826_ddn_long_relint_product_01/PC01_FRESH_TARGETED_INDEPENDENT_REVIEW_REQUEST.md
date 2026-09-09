# PC01 fresh targeted independent review request

## review custody

```text
PARENT_GOAL: DDN_LONG_RELINT_PRODUCT_01
REVIEW_TYPE: FRESH_FIXED_HEAD_TARGETED_READ_ONLY
INTEGRATION_FIXED_HEAD: a2e23fd4
INTEGRATION_PRODUCT_HEAD: f80c69b8
ORIGINAL_PC01_IMPLEMENTATION: cf97f134aebc4889bd3e13ff4850cbf76ca4c2d6
ORIGINAL_PC01_FORMAT_CORRECTION: 3ac1cefbffa4c00857f99debad3b1aad24ed08ea
ORIGINAL_PC01_HANDOFF: 9cb28ee8044dd0562d99f8d5fce5911dfd01c652
PC02_EXCLUDED_BY_EXACT_INVERSE: YES
```

The reviewer must create a detached or isolated read-only review at the exact integration
fixed HEAD. Do not modify product code, tests, public SPEC, SSOT, or tracked WASM. Do not
accept the earlier Owner-attested PASS without a locally recoverable fresh artifact.

## exact targeted scope

Review the PC01 Definition/Binding semantic distinction as it exists in the integrated
successor, including all 18 original product-range paths from `cf97f134...`, the
format-only correction, and later changes on those paths. In particular verify:

1. Definition and Binding remain distinct typed AST/parser/canonical identities.
2. old `=` is not silently accepted as the successor Definition surface.
3. Binding-as-Definition misuse fails closed with the intended product-local diagnostic.
4. parse-canon-parse preserves category and symbol identity.
5. runtime and LSP projections do not collapse the two categories.
6. the exact five-file pack is internally consistent and the oracle is consumed.
7. PC02 exclusion did not reintroduce a hidden compatibility fallback for PC01.
8. CLI/WASM/Workbench-relevant later composition does not invalidate the PC01 contract.
9. mutation M1/M2/M3 each turns RED and exact restoration returns GREEN with residue 0.
10. `docs/ssot/**`, public SPEC semantics, official DB, protected process/socket, and
    activation state are unchanged by review.

Minimum direct reproduction:

```powershell
$env:CARGO_TARGET_DIR = '<isolated-target>/pc01'
cargo test -p ddonirang-lang --test v25_definition_binding_pack -- --nocapture
node tests/ddn_v25_pc01_definition_binding_mutation_runner.mjs
```

The reviewer may add independent probes in a separate temporary location, but must not
weaken or rewrite expectations. Record exact commands, outputs, fixed HEAD, start/end
clean state, report bytes, and SHA-256.

## verdict contract

Only the independent reviewer may issue `PASS`, `PASS_WITH_FOLLOW_UP`, or `REWORK`.
Only plain `PASS` permits the integration owner to reconsider PC01 release membership.
Rights are not part of this technical verdict: even plain PASS does not authorize the
five-file public copy, projectile copy, publication, activation, or Human PASS.
