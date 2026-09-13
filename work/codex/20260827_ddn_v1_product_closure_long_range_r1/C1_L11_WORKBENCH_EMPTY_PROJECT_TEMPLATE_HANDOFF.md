# C1 L11 Workbench empty-project template handoff

## Fixed target

- Product commit: `643e42e8e21c0efde1f8a19b0abd914312059be0`
- Parent: `d18ac6d466a02cedff947d5d3bb974e5bc8d4c48`
- Product path: `solutions/seamgrim_ui_mvp/ui/workbench/workbench.js`

## User workflow

The Workbench “empty local project” creation path now emits an executable V25
callable with a direct typed definition. It no longer supplies the retired
`설정 {}` / `(매마디)마다` template to a new project.

## Evidence

- The tracked WASM shared source-analysis frontdoor accepts the generated
  V25 source using `v1-core-v25`.
- Mutation restoring the former `설정 {}` / `(매마디)마다` source is rejected
  with `E_V25_DEFINITION_MIGRATION_REQUIRED`.
- Exact restore: SHA-256
  `c079537d0e5341d5fe8e26a543df6455284f67eb647a7ac79c3b4a3830507474`,
  blob `178521450722f116192ec26fdfdd8db112549d75`; frontdoor GREEN again.
- `node --check` and `git diff --check`: PASS.

## Existing separate gate

The existing WASM freshness checker currently reports a source-tree/manifest
mismatch caused by `tool/src/local_project.rs` changes that postdate the
tracked artifact. This JS-only template commit did not rewrite the artifact or
manifest; artifact rematerialization is a separate P5 custody vertical.

## Nonclaims

No public syntax, SSOT, public SPEC, release, readiness, membership, or Human
PASS transition is claimed.
