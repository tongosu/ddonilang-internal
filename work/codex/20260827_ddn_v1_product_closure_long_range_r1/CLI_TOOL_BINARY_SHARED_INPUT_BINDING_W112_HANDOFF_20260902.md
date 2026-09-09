# CLI tool binary shared-input binding W112 handoff

## Scope

- Product fixed commit: `a28f52590ff77f0494c32090848cecfac82fbb4b`
- Direct parent: `52bb7bb8d885cb3096d4ee9373107ff78f807d06`
- Fixed tree: `6239c7937027f114c4ca91584b066869edf05f48`
- Current authority read-only: internal SSOT v25.50.0 / RD-001~551; public Language SPEC v0.6.0.

The native `ddonirang-tool` binary continued to compile `ddn_runtime.rs` as a
binary-crate module after the shared input projection landed.  Its crate root
did not include the same shared `geoul_snapshot`, `input_tape`, and atomic
artifact-output modules.  This made the tool binary fail before any CLI user
workflow could run.

## Product change

`tool/src/main.rs` now includes those existing shared modules in the binary
crate.  No module contents, public command spelling, executable name, package,
legacy alias, `teul-cli` path, product wire, SSOT, public SPEC, or dependency
set changed.

## Evidence

- Baseline binary RED: `cargo build -p ddonirang-tool --bin ddonirang-tool`
  failed with unresolved `crate::geoul_snapshot` and `crate::input_tape` in
  `ddn_runtime.rs`.
- Fixed binary build: PASS.
- Existing binary regression: `cargo test -p ddonirang-tool --bin
  ddonirang-tool` — 368 passed, 0 failed.
- Fail-closed command probe: `ddonirang-tool build-schema missing-input.ddn`
  returned exit 1 at the existing missing project-policy guard; it did not
  publish an artifact.
- Relevant mutation: removing only `mod geoul_snapshot;` produced compile RED
  (exit 101, unresolved shared module); exact restore returned compile GREEN.
  Restored `tool/src/main.rs` SHA-256:
  `8aebbdef25fca9d550c5b8e83a27243b482223fde46b1463a61d436a6a828fa9`.

## Gate effect and nonclaims

This removes one native lang/tool frontdoor materialization failure and keeps
the shared input authority consumable by the official tool binary.  It does
not close CLI convergence, retire `teul-cli`, decide command membership or
public naming, establish Windows RC/release readiness, or make any rights,
publication, activation, V1 readiness, or Human PASS claim.

Independent review is queued only with a later coherent CLI product milestone;
no reviewer, worktree, or review artifact was created for this one-file fix.
