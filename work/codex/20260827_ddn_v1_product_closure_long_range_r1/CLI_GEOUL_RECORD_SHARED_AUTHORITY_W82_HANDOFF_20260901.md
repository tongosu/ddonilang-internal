# CLI Geoul record shared authority W82 handoff

## Fixed identity

- Authority: internal SSOT `v25.47.0 / RD-001~543`; public SPEC `v0.6.0`.
- Baseline: `c4107cb7ad269e1083d0da1007d3516b4a344dc1`.
- Product fixed: `b16e11153156847959d159816f25acad53ce42dc`.
- Product tree: `0e9292097aade21749d22d18cab74526a49e81f0`.
- Status: `CLI_GEOUL_RECORD_SHARED_AUTHORITY_W82_IMPLEMENTED_UNDER_REVIEW`.

## User workflow and product authority

The existing versioned `geoul record make/check` workflow now lives in the
shared `ddonirang_tool::geoul_record_workflow` owner. The retained teul Geoul
module reexports the two commands and keeps only the still-frozen legacy
query/backtrace evaluator paths.

Exact product paths:

- `tool/src/geoul_record_workflow.rs` (new shared owner);
- `tool/src/lib.rs` (host-only export);
- `tools/teul-cli/src/cli/geoul.rs` (record implementation removed, adapter retained).

The fixed `geoul.record.make.v0` input and `geoul.record.v0` JSONL output,
field spelling, diagnostics, stdout, ordering, and atomic artifact behavior are
byte-compatible. No new schema, command, option, pack, runner, public membership,
WASM export, Workbench UI, SSOT, or public SPEC change was introduced.

## Evidence and mutation

- Existing `pack/geoul_min_schema_v0`: baseline 3/3 PASS; fixed 3/3 PASS.
  - record make positive;
  - record check positive;
  - unknown schema fail-closed.
- Existing broader `geoul_record_query_timeline_minimum_v1`: baseline and fixed
  both retain the same 1/7 record-check PASS and 6/7 environment-dependent
  missing historical W34/W43 products. No new drift or inherited PASS.
- Mutation bypassed the `geoul.record.v0` schema check.
  - existing case 3 RED because expected exit 1 became exit 0;
  - source restored byte-exact to SHA-256
    `2200f4fbad511f3d2c236cbc149bfb4acf043401513676cdf26eb8b7c2ada0c0`;
  - fixed pack returned 3/3 GREEN;
  - mutation residue and partial publish: 0.
- `git diff --check`: PASS.

## Boundaries and review bundle

- Private teul record make/check authority: 1 -> 0.
- Shared tool record authority: 0 -> 1.
- Legacy Geoul query/backtrace evaluator and legacy State detbin remain frozen;
  W82 does not resolve the W80/W81 `NuriWorld` versus legacy State codec gap.
- Native retained CLI: PASS.
- WASM/Workbench: not applicable record ingress in this slice; semantic reconstruction 0.
- New test artifact/meta-test/reviewer/worktree/branch: 0.
- Existing tests reused: 2 pack families.
- Review bundle: W81 gateway + W82 Geoul record form one coherent internal/deferred
  structured-ingress authority milestone for the existing rolling reviewer after
  management dispatch.

This does not claim public Geoul/gateway membership, whole C0-C8 closure,
repository-wide teul authority/dependency zero, physical retirement, P0-P6
closure, V1 membership/readiness/release, activation, legal approval, Owner
Human Smoke, or Human PASS.
