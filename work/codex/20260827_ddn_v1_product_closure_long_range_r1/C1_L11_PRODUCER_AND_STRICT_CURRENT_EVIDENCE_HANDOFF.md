# C1-L11 current producer and strict rejection evidence

## Fixed lineage

- Current handoff parent: `6eef398eacbb75545d5a803375e46662df51958d`
- Current-producer product: `9bb3e0c96e556d5acdeacb0c220a2b4c11678a8`
- Current-producer product tree: `3472f615f5c24e86e6d7c997fb304690a6261c16`
- Current-producer handoff: `f9d2f7ddcca073bc3aae0e86312c318872f02987`
- Strict current L11 product: `269460066f1f7030e0552437bf003423a1a1613b`
- Strict current L11 handoff: `d7792693e2f4c403c4284eabd9a752e6634bb73d`

The strict product is an immutable ancestor of this lineage.  This handoff
does not recreate a no-op strict product commit.

## Current producer mutation evidence

All temporary source edits were restored byte-exactly before the succeeding
GREEN run.  `tool/src/local_project.rs` restored to blob
`235b3ad07b7e91f106f4d89d11640b395719a3e9`.

1. M1, AddModule brace export restoration: replacing `(값=값) 드러냄.` with
   `드러냄 { 값. }` made
   `local_project::tests::structural_edit_plan_supports_add_module_duplicate_and_set_entry`
   RED.  Restore was GREEN.
2. M2, legacy `<-` dataset binding restoration: changing the generated sealed
   binding from `:=` to `<-` made
   `sealed_dataset_binding_edit_uses_verified_handle_and_real_runtime_call`
   RED with `E_PROJECT_ENTRY_PARSE` / `E_SHARED_CANONICAL`.  Restore was GREEN.
3. M3, export-target identity mismatch: changing generated `(값=값) 드러냄.`
   to `(값=다른값) 드러냄.` made the AddModule workflow RED.  Restore was GREEN.

## Strict current parser mutation evidence

`lang/src/parser.rs` restored to blob
`6259b2607a66df20a0294665ad6d617060e1fcf7`.

1. Removing the V25 brace L11 guard made legacy `쓰임 { ... }` return
   `E_PARSE` instead of `E_V25_DEFINITION_MIGRATION_REQUIRED`; the exact
   migration diagnostic assertion was RED.  Restore was GREEN.
2. Replacing the lexer/token-based L11 check with a raw source substring check
   made a string literal containing `쓰임 {` fail closed incorrectly; the
   lexical false-positive assertion was RED.  Restore was GREEN.

There is no current automatic brace-to-parenthesized conversion path to
mutate.  No temporary conversion implementation was introduced merely for
mutation accounting.

## Regression on the current lineage

- `project_authoring::tests::current_typed_directives_reach_the_authoring_symbol_frontdoor`: PASS.
- `local_project::tests::empty_project_current_callable_runs_through_the_shared_frontdoor`: PASS.
- `v25_definition_binding_pack`: 5/5 PASS.
- `rd457_module_directive_roundtrip`: 6/6 PASS.
- `cargo test -p ddonirang-lang`: 374 unit tests plus 11 DDL, 6 RD-457, and 5 V25 integration tests PASS.
- `cargo check -p ddonirang-tool --offline`: PASS.
- `git diff --check`: PASS.

## Open verification boundary

The browser runner source assertion update is fixed at `ef89007867495cdb2bbf51ae4ba274e761b6dcde`.
`node --check` passed, but its actual browser run is not recorded as PASS:
the checkout has no resolvable Node `playwright` package, and no network
dependency installation was performed.  Native/WASM/Workbench same-source
parity is therefore still open for a separately executable target.  No
independent review or broader closure is claimed by this handoff.
