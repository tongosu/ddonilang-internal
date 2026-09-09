# [언어물리Codex -> 제품구조Chat] V25 PC-01 Definition / Binding 구현 결과

```text
PROGRAM_ID: DDN_V25_PHYSICAL_CLOSURE_LONG_RANGE_R1
SLICE: PC-01_DEFINITION_BINDING
START_BASELINE: 55f57623ab419d9ccb99b9e0527efa912eaccee3
PRODUCT_IMPLEMENTATION_COMMIT: cf97f134aebc4889bd3e13ff4850cbf76ca4c2d6
FIXED_REVIEW_TARGET: 3ac1cefbffa4c00857f99debad3b1aad24ed08ea
STATUS: IMPLEMENTED_PENDING_INDEPENDENT_REVIEW
PC02: NOT_STARTED_DEPENDENCY_BLOCKED
```

## Landed boundary

- The shared lexer has a dedicated `Define` token for `:=`.
- The typed AST has `Stmt::Definition`; Binding/Rebinding remains `Stmt::Mutate`.
- `CanonProgram` carries an explicit `SourceEpoch`.
- `parse_v25*` is the V25 reader. Historical `parse*` remains an explicit
  `PreV25` reader during migration custody and is not treated as V25 acceptance.
- V25 top-level `=` fails closed with
  `E_V25_DEFINITION_MIGRATION_REQUIRED`.
- V25 `채비` name introduction with `<-` fails closed with
  `E_V25_DEFINITION_BINDING_CATEGORY`.
- Canon writes Definition as `:=` and Rebinding as `<-`.
- The explicit product runtime constructor `DdnProgram::from_v25_source` consumes
  the same shared V25 parser. A local Definition evaluates atomically into a new
  local identity and does not publish a root resource.

## Executable evidence

`pack/ddn_v25_pc01_definition_binding_v1/` has one positive Definition→Rebinding
case and two fail-closed cases. Its JSONL oracle is consumed by the Rust pack
test rather than duplicated in a harness. The positive case is also executed by
the product `DdnRunner`; its observed output is `2`.

## Non-promotion boundary

The default tool/native/WASM/teul-cli/Workbench frontdoors were not switched.
That authority move belongs to PC-02 and is not authorized before PC-01 plain
independent PASS. No SSOT, public SPEC, tracked WASM, deployment, Human PASS, or
external-user claim is made.
