# CLI Geoul inspection shared authority W83 handoff

## Identity

- Authority: internal SSOT `v25.47.0 / RD-001~543`; public SPEC `v0.6.0`.
- Baseline: `ea8e2f723c0cffe1b8beb61ba7f69800c144b60f`.
- Product fixed: `302024e36f663665ae127efbfbe742f9cc2f9b25`.
- Product tree: `ee25782790edb544b63e596db0515e122c1b262c`.
- Status: `CLI_GEOUL_INSPECTION_SHARED_AUTHORITY_W83_IMPLEMENTED_UNDER_REVIEW`.

## Product vertical

The existing read-only `geoul hash` and `geoul seek` workflows now execute from
the shared `ddonirang_tool::geoul_workflow` owner. W82 record make/check was
retained in the same shared module; the teul module is an adapter for these four
operations and still owns only the separately frozen legacy query/backtrace
evaluator.

Exact changed paths:

- `tool/src/geoul_record_workflow.rs` -> `tool/src/geoul_workflow.rs`;
- `tool/src/lib.rs`;
- `tools/teul-cli/src/cli/geoul.rs`.

No bundle bytes, hash formula, frame header, index interpretation, command or
option spelling, diagnostics, public membership, pack, runner, WASM, UI, SSOT,
or public SPEC contract changed.

## Evidence

Existing `I:/home/urihanl/ddn/codex/build/geoul_w53` fixed fixture:

- `geoul hash`: exit 0, `audit_hash=blake3:2a7e18dcce782f96e3a409f816f2ef75499993511ea6cfee954f123e6949ba40`.
- `geoul seek --madi 0`: exit 0, `state_hash=blake3:c8e546d35ab1f4155f430c3a46db8692569723559603cd31ae3e64cdae14cd9a`.
- `geoul seek --madi 1`: same fixed state identity, exit 0.
- `geoul seek --madi 2`: baseline/fixed exit 1, index-range fail-closed.
- W82 record regression: existing `geoul_min_schema_v0` 3/3 PASS.
- `git diff --check`: PASS.

Mutation forced every seek to frame zero. The out-of-range request changed from
exit 1 to exit 0 and therefore RED. The source was restored byte-exact to
SHA-256 `1b2932bdda86fd4ba979d309148c727f2acd10dd1b16bd5c03d264cd9920ef7f`;
the out-of-range request returned exit 1 again. Mutation residue and write/publish
count are 0.

## Coherent review and boundaries

- Private teul hash/seek implementation: 1 -> 0.
- Shared tool inspection owner: 0 -> 1.
- New test artifact/meta-test/reviewer/worktree/branch: 0.
- Native retained CLI: PASS.
- WASM/Workbench: not applicable inspection ingress; reconstruction 0.
- Review bundle: W81 gateway + W82 Geoul record + W83 Geoul inspection, one
  coherent internal/deferred IO-authority milestone for the existing rolling
  reviewer after management dispatch.
- Query/backtrace, replay, shared NuriWorld snapshot codec, and physical teul
  retirement remain OPEN or slice-locally frozen.

This does not claim public command membership, whole C0-C8 closure,
repository-wide teul authority/dependency zero, P0-P6 closure, V1
membership/readiness/release, activation, legal approval, Owner Human Smoke, or
Human PASS.
