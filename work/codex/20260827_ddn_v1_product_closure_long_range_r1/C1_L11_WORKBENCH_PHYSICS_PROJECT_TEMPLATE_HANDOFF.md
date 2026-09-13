# C1 L11 Workbench physics-project template handoff

## Fixed target

- Product commit: `baeb794bfae505170558274d87bb8c9e01e289f7`
- Parent: `5c39c13e630ca9ae950e512c0811743d5bc19067`
- Product path: `solutions/seamgrim_ui_mvp/ui/workbench/workbench.js`

## User workflow

Choosing the Workbench local physics-project template now generates a V25
module entrypoint with the current parenthesized import directive and direct
`:=` definitions only. It no longer emits mutable `<-` updates for the first
physics step.

## Product-facing evidence

- The tracked Native/WASM module-directive carrier accepts the generated
  `app/main.ddn` source using the V25 profile.
- The carrier preserves the `./lib/힘` typed import and reports its span as
  `utf-8-byte`.
- `node --check` and `git diff --check`: PASS.
- Mutation replacing the callable head and first definition with `채비 {` and
  `<-` returned `REJECTED / E_V25_DEFINITION_BINDING_CATEGORY`.
- Exact restored source: SHA-256
  `393d2ee02b950aca692a1ede690f412ecc4d9363b4628ce9fd1732721c5a56ed`,
  blob `ca108a94199a31981f2a3bbac42a8ec435ed1118`; carrier GREEN again.

## Boundaries

The template remains an internal Workbench producer and reuses the existing
carrier. No new language semantics, public ABI, SSOT, public SPEC, release,
membership, or readiness claim is made.
