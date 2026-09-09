# CLI teul shared typed bridge W116 handoff

## Scope and lineage

- Product fixed: `b516e628f2d3b125e5f79c1362c916ca730e35d5`
- Direct parent: `046e4c7d1db7ce2ca8b7ce688734affb7da0f339`
- Tree: `5bd47e34145559a207ca4c8d1aae03299fdd7c4a`
- Merge count: `0`
- Authority read-only: internal SSOT `v25.50.0 / RD-001~551`; public Language SPEC `v0.6.0`.

W116 is an internal CLI convergence correction.  It does not select a public
executable name, command membership, legacy alias policy, public wire, or
physical `teul-cli` retirement.

## Product change

The legacy `teul-cli` run adapter retains its local option and rendering
custody, but every value crossing into `ddonirang_tool::runtime_surface` now
uses the shared crate identity:

- `InputSource` is converted at net-event and geoul-snapshot boundaries.
- `AgeTarget` is converted only for the existing profile-aware shared runtime
  call.
- `runtime_surface` exposes those already-owned typed values for this internal
  adapter boundary; it introduces no user-facing command, source syntax, or
  diagnostic.

This removes the observed `E0308` duplicate-crate identity failure from the
shared-runtime crossing while preserving local legacy/internal command custody.

## Evidence

- Baseline RED: the existing `gaji_creator_wasm_parity_runner.mjs` compiled its
  legacy `teul-cli` path with `E0308` for `InputSource` and `AgeTarget` at the
  shared runtime crossing.
- Green: `cargo check --manifest-path tools/teul-cli/Cargo.toml --offline`
  completed after the bridge change; `git diff --check` passed.
- Direct required workflow: `cargo run -p ddonirang-tool --bin ddonirang --
  project-run --virtual pack/ddn_local_project_cli_wasm_parity_v1/fixtures/
  virtual_project.json --target 앱 --inspect-graph --inspect-lock` returned
  exit `0`, schema `ddn.local_project_run_summary.v1`, and frontdoor
  `ddn.project-run.v1`.
- The existing full gaji lifecycle runner reaches an unchanged `gaji plan`
  path first and terminates with stack overflow exit `3221225725`; the migrated
  `project-run` assertion is not reached.  This is retained as
  `REBASE_REQUIRED` for internal/deferred gaji custody, not interpreted as a
  shared project-run mismatch or a W116 PASS.
- Source restore check: `tools/teul-cli/src/cli/run.rs` SHA-256 before and
  after the controlled bridge edit was
  `ea22afcd32b7c2c39a081dd0b49203c503b1ac08357045472de564632fdf1600`.

## Boundary and next gate

- Product paths: `tool/src/runtime_surface.rs`,
  `tools/teul-cli/src/cli/run.rs`.
- Test/pack/WASM/UI/SSOT/SPEC/public-export changes: `0` in this fixed commit.
- New dependency, pack, runner, or meta-test: `0`.
- Independent review dispatch: `0`; a coherent future CLI/P5 milestone may
  reuse the existing rolling reviewer only when management binds it.

Open: C0--C8 convergence, V1-required teul dependency zero, teul semantic
authority zero, gaji stack-overflow custody, command/executable membership,
physical retirement, P0--P6 closure, membership, readiness, release,
activation, legal, and Human PASS.
