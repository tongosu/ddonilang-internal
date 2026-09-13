# CLI gaji project-run teul test dependency W115 handoff

## Fixed identity

- Product/test fixed commit: `5ce709db1575585e1e4814e8588be39b3267f882`
- Direct parent: `d4cda6e1ae9ff5c7658b331a523bf0bc16b613c2`
- Fixed tree: `36ddf620ca5b50827823d736e3d6911d9786e879`
- Changed path: `tests/gaji_creator_wasm_parity_runner.mjs` only.

## Product-facing change

The existing gaji lifecycle parity runner now invokes the existing shared
`ddonirang project-run` frontdoor for the three installed-project run checks.
The internal `gaji plan` and `gaji lifecycle-plan` invocations remain in
`teul-cli` custody: no `gaji` command was exposed or renamed.

`ddn.project-run.v1` remains the semantic identity. Public executable naming,
command membership, package identity, legacy aliases, and physical teul-cli
retirement are unchanged.

## Verification

- `node --check tests/gaji_creator_wasm_parity_runner.mjs`: PASS.
- `git diff --check`: PASS.
- Direct existing shared product workflow: PASS, using
  `ddonirang project-run --virtual
  pack/ddn_local_project_cli_wasm_parity_v1/fixtures/virtual_project.json
  --target 앱 --inspect-graph --inspect-lock`; returned
  `frontdoor: ddn.project-run.v1`.
- Existing full `gaji_creator_wasm_parity_runner.mjs`: REBASE_REQUIRED before
  the migrated project-run section. A clean external Cargo target rebuild of
  the unchanged `teul-cli gaji plan` segment failed with `E0308`: direct
  `ddonirang_core::platform::InputSource` and the copy reached through
  `ddonirang_tool` differed; the same failure also affected `AgeTarget`.
  This is a pre-existing `tools/teul-cli` dependency-graph convergence defect,
  not a project-run source or output mismatch. No product source was changed
  to mask it.

## Boundary and next gate

- New pack/runner/dependency/meta-test: `0`.
- Product source, tracked WASM, SSOT, public SPEC, UI, release artifact diff: `0`.
- W115 removes the private CLI invocation from the runner's V1 project-run
  segment only. It does not establish zero teul dependency for the full runner
  while its separately-owned internal gaji commands remain.
- The next coherent CLI milestone must converge the teul Cargo dependency graph
  or split its internal gaji custody from V1-required project-run verification,
  with exact owner paths and a reproducible RED.

## Nonclaims

No C0--C8, M1, P0--P6, P5, V1 membership/readiness/release/activation,
legal/rights/publication, independent PASS, or Human PASS is claimed.
