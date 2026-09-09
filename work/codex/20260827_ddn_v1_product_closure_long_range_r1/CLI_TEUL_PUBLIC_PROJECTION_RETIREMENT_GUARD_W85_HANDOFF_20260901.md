# CLI teul public projection retirement guard W85 handoff

STATUS: `TEUL_CLI_PUBLIC_PROJECTION_RETIREMENT_GUARD_IMPLEMENTED_UNDER_REVIEW`

## Authority and lineage

- Internal CURRENT: v25.49.0 / RD-001~543, `docs/ssot/CURRENT.md` SHA-256 `bc508d45e053d8c8a84b08e8c1657bc6eec5e82c1ad4a04d12d7daf22dfec6fa`.
- Public Language SPEC: v0.6.0, `publish/spec/CURRENT.md` SHA-256 `6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0`.
- Successor impact: additive release-custody guard only; no language or runtime semantic change.
- Baseline/handoff parent: `92bfcbdbd3de5071b70bfeba2896bf46a1f746d1`.
- Product/test fixed commit: `6bad095b02e2973af2245bca131dfb2249fe5ffd`.
- Fixed tree: `787c647bb09312962d5609c8cf99952c6ff0e3c2`.
- Direct lineage: yes; merge count: 0.

## Product value and exact FILE_OWNER

The deterministic public-source projector previously accepted a manifest that
projected `tools/teul-cli/**` or materialized a `teul-cli`/`teul-cli.exe`
target. That fail-open path could reintroduce the retired public package or
binary into a later V1 candidate even though the current fixed manifest omits
it.

Exact changed paths:

1. `tools/project_public_source.py`
2. `tests/test_project_public_source.py`

The existing projector now rejects both the retired source/package prefix and
the retired binary target names with `E_PUBLIC_TEUL_CLI_RETIRED` before any
projection output or receipt directory is created. Historical/internal teul
custody remains in Git and is not deleted or promoted.

## RED, GREEN, and regression evidence

- RED first: the new case projected `tools/teul-cli/Cargo.toml` successfully;
  the assertion failed because the projector returned exit 0.
- GREEN: `test_retired_teul_cli_cannot_enter_public_projection` PASS; both the
  source/package and binary target axes return nonzero with the exact diagnostic.
- Existing projector suite: 11/11 PASS.
- Existing projection validator suite: 25/25 PASS.
- `git diff --check`: PASS (Git reported only the repository LF materialization warning).
- Reused test artifacts: 2 existing unittest modules.
- New test artifacts/runners/packs/meta-tests: 0/0/0/0; one case was added to an existing product-facing suite.
- Partial projection/receipt publish on either rejected rule: 0, because rule
  validation precedes output directory creation.

## C0-C8 bounded state

- C0: historical 28 tool + 63 teul = 91-command inventory remains custody; membership transition 0.
- C1: `ddn.project-run.v1` remains fixed; executable/package/legacy alias naming remains OPEN.
- C2: W84 shared patch authority and this W85 release guard form the next coherent CLI convergence/release-custody bundle.
- C3: V1 public reachability remains 12/15; public `test`/`view`/`repl` membership is slice-frozen.
- C4: W84 patch private semantic authority is 0; other INTERNAL/DEFERRED teul custody remains nonzero.
- C5: bounded V1-required build/test/pack/publish teul execution dependency remains 0; historical/manual references remain custody.
- C6: no new WASM or Workbench semantic path; projector output/receipt fail-closed behavior is shared release custody.
- C7: P5 fixed-target review `bc84d81d4faa55974975bdb7ec60cb18d9a7ebda` remains bound PASS_TARGET_BOUND; whole P5 remains OPEN.
- C8: V1 public projection now makes teul source/package/binary inclusion fail-closed. Physical directory/ref deletion and final retirement completion remain Owner-gated.

## Review and nonclaims

Review bundle target: W84 shared patch authority plus W85 public-projection
retirement guard, using only the existing rolling reviewer after management
selection. New reviewer task/worktree/branch count is 0.

This handoff does not claim whole CLI convergence, repository-wide teul
semantic authority 0, physical teul deletion, public command membership, whole
P5/P6 closure, V1 readiness/release/activation, legal approval, Owner Human
Smoke, or Human PASS.
