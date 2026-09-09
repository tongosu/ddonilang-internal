# CLI project-run teul test dependency migration W114 handoff

## Scope

- Product/test fixed commit: `52c87186c4299f6ea6ad23cc8993f7d99a45be95`
- Direct parent: `358af346b97c6d04a8e86e9aca299750395d1f32`
- Fixed tree: `ea9470837f7c7553d81d33edf3a6e099737a6f54`
- Changed path only: `tests/ddn_project_workbench_boundary_matrix_runner.mjs`
- Semantic identity retained: `ddn.project-run.v1`.

The existing symlink-escape CLI verification now invokes the existing shared
`ddonirang-tool` binary (`ddonirang project-run`) rather than `teul-cli`.
It retains the same arguments, expected `E_PROJECT_SYMLINK_ESCAPE` failure,
and host-path non-leak assertion. No command spelling, public executable name,
legacy alias, package identity, or product semantics changed.

## Product value and evidence

- User workflow: `project-run` is exercised through its shared lang/tool
  frontdoor for the existing disk-project symlink-escape safety boundary.
- Removed required dependency: this runner has `teul` references `0` after the
  change; the fallback is `cargo run -p ddonirang-tool --bin ddonirang --`.
- Reused tests: 2 Rust focused tests passed:
  - `tests::project_run_binds_neutral_identity_inputs_and_rejects_virtual_conflicts`
  - `local_project::tests::prepare_link_and_project_run_bind_verified_dataset_identity_to_execution`
- Direct native positive fixture passed with schema
  `ddn.local_project_run_summary.v1` and frontdoor `ddn.project-run.v1`.
- Direct native `--virtual` plus `--project` failed closed with
  `E_CLI_OPTION_CONFLICT` (exit `2`).
- The existing WASM boundary matrix was re-run but stopped at its pre-existing
  `running_file_change_fake_summary` expectation before the migrated symlink
  case. It is `REBASE_REQUIRED` tracked-WASM evidence, not a pass for this
  change and not a reason to retain `teul-cli` as a required test dependency.

## Boundaries

- New pack/runner/dependency/meta-test: `0`.
- Product source, tracked WASM, SSOT, public SPEC, UI, package, and release
  artifact changes: `0`.
- No physical `tools/teul-cli` deletion or public-retirement claim.
- No independent-review dispatch. This fixed commit is eligible to be bundled
  with the existing CLI convergence milestone for the existing rolling review
  custody when management selects the target.

## Nonclaims

This does not close C0--C8, M1, P0--P6, P5, V1 readiness, membership, release,
activation, legal/rights attribution, public publication, or Human PASS.
