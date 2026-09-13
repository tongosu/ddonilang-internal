# C1-L11 strict-current conversion mutation handoff

## Target custody

- Strict product target: `23f1a319553a0b8ac333aaae3dad4451eaef9209`
- Strict product tree: `5193995c792158d9a1df4e04dcff891b72a55c7d`
- Current evidence parent: `c202628298be488fec90ec5d117c58fbb68db5ff`

## M2: compatibility conversion fault

The fixed parser has no compatibility conversion path. To prove that boundary,
a task-local mutation made brace-form `쓰임 { ... }` bypass the V25 L11 guard
and classify it as a current metadata block. That fault accepted
`쓰임 { 운동: "./lib/운동". }` as a V25 program, so
`v25_current_frontdoor_rejects_legacy_l11_brace_blocks_without_lexical_false_positives`
was RED (exit `101`) at the required rejection assertion.

The mutation was not committed. `lang/src/parser.rs` was restored byte-exactly:

- Blob: `6259b2607a66df20a0294665ad6d617060e1fcf7`
- SHA-256: `7fc55a8d5f33bbf5919fa5b312260ecf8ceed5242e4c68ba7c0312ef4d0dd956`
- Restored focused gate: GREEN.

This fault demonstrates that treating a retired brace directive as current
metadata would silently erase its directive authority, which is forbidden.
The fixed parser instead returns
`E_V25_DEFINITION_MIGRATION_REQUIRED` before AST admission.

## Nonclaims

This records one mutation only. It does not replace independent review or
claim V1 readiness, release, activation, legal clearance, or Human PASS.
