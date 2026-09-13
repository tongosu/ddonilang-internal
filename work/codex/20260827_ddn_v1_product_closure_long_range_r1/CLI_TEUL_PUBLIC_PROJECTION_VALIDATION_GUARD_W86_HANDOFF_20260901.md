# CLI teul public projection validation guard W86 handoff

STATUS: `TEUL_CLI_PUBLIC_PROJECTION_VALIDATION_GUARD_IMPLEMENTED_UNDER_REVIEW`

## Fixed lineage and scope

- Authority: internal v25.49.0 / RD-001~543; public Language SPEC v0.6.0.
- Baseline: W85 handoff `32aaccf9071916f5ff5197179514a9adfad42b5d`.
- Product/test fixed: `fc955a24c7f2297f335aa87ce1c142b9c204e7c8`.
- Fixed tree: `db8f332dc4526a7f03823dbf195a3c216f37b003`.
- Direct parent: yes; merge count: 0.
- Exact changed paths:
  1. `tools/validate_public_projection.py`
  2. `tests/test_validate_public_projection.py`

## User and release value

W85 prevents the official projector from creating a public projection that
contains the retired teul package or binary. W86 closes the independent
validation bypass: a preconstructed projection plus internally consistent tree
manifest can no longer obtain validation PASS when either its output path or
recorded source path contains `tools/teul-cli/**`, or when an output target is
named `teul-cli`/`teul-cli.exe`.

The validator returns `E_PUBLIC_TEUL_CLI_RETIRED` before artifact hashes,
security receipt generation, or validation-receipt publication. Historical
teul custody in the private repository remains unchanged.

## RED/GREEN and custody

- RED first: a sealed projection containing `tools/teul-cli/Cargo.toml`
  returned `PUBLIC_PROJECTION_VALIDATION_PASS` with exit 0.
- GREEN: source/package and binary target cases both return nonzero with the
  exact retirement diagnostic.
- Validator suite: 26/26 PASS.
- Projector suite: 11/11 PASS.
- Reused cases: 37 across the two existing suites.
- New pack/runner/framework/meta-test: 0/0/0/0.
- Failed validation receipt publication: 0; rejected inputs cannot publish a
  success receipt.
- SSOT/SPEC/product runtime/WASM/UI/Workbench diff: 0.

## Gate effect and nonclaims

- V1 public projection now enforces teul public source/package/binary exclusion
  at both creation and independent validation boundaries.
- Bounded V1-required build/test/pack/publish teul execution dependency remains 0.
- Other INTERNAL/DEFERRED teul command custody and private parser/runtime/value
  families remain nonzero.
- Review target is one coherent W84-W86 bundle: shared patch authority plus
  projector and validator retirement guards, through the existing rolling
  reviewer only after management dispatch.
- New reviewer/worktree/branch/task count: 0.

This does not claim physical teul deletion, exact public command membership,
whole CLI/P5/P6 closure, V1 readiness/release/activation, legal approval,
Owner Human Smoke, or Human PASS.
