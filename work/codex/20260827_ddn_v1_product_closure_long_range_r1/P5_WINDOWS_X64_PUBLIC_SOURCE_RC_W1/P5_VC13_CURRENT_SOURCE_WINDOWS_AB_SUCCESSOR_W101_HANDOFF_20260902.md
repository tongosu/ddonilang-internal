# P5 VC13 current-source Windows A/B successor W101 handoff

## Authority and exact lineage

- Persistent goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` (`ACTIVE`).
- Internal live CURRENT: `v25.49.0 / RD-001~543`.
- Public Language SPEC: `v0.6.0`.
- Product/source handoff: `8996a020fe28e0eb61232cc7dcda90a9fb6834de`.
- Product/source tree: `8a2484033c9076393d3c6904cc8f55be7932f05c`.
- Projection-manifest fixed commit: `fd685c2e0f5a8fc159f7867a800be5f0360161c5`.
- Projection-manifest fixed tree: `7e7612786a114b4375ced8b0a9468cc850e248e1`.
- Direct parent: `8996a020fe28e0eb61232cc7dcda90a9fb6834de`.
- Merge count: `0`.
- Successor impact: `UNAFFECTED_WITH_ADDITIVE_RELEASE_CUSTODY`.
- Product source/SSOT/public SPEC diff in the fixed commit: `0/0/0`.

The historical P5 review PASS at `bc84d81d4faa55974975bdb7ec60cb18d9a7ebda`
remains target-bound with blocking finding `0`. W101 is a successor target and
does not inherit that verdict.

## Fixed diff

The fixed commit changes exactly one line in the existing public projection
manifest:

`work/codex/20260827_ddn_v1_product_closure_long_range_r1/P5_WINDOWS_X64_PUBLIC_SOURCE_RC_W1/PUBLIC_PROJECTION_V25_35_WINDOWS_X64_PATH_CLEAN_MANIFEST.detjson`

Its `source_commit` now binds exact handoff `8996a020...`.

## Exact source and WASM candidate

The official candidate entrypoint rebuilt exact source `8996a020...` from a
clean LF materialization with offline dependency resolution.

- Candidate root: `I:/home/urihanl/ddn/codex/build/p5-vc13-pathclean-8996-r3/wasm/ddonirang_tool`.
- Candidate WASM: `5,576,576` bytes / SHA-256 `00f574305c6d10b77b7a262e02d9cec677c4e79015d9ddd603eaf30e13abca11`.
- Candidate equals tracked W100 WASM: `true`.
- Candidate semantic identity: `sha256:7985a2cde0b6a8bfed12c72ae5b49da207512d80187862484966bb468715d676`.
- Internal/private/official/unknown host-path counts: `0/0/0/0`.

## Public projection

- Projection root: `I:/home/urihanl/ddn/codex/out/p5-w101-projection-8996`.
- Receipt root: `I:/home/urihanl/ddn/codex/out/p5-w101-receipts-8996`.
- Projected files: `222`.
- Before candidate substitution: `sha256:f50a8b53adcfa0f9518a8ebee7b59ac750cd5d4a0819b5858abe60e7e0f1ab75`.
- After candidate substitution: `sha256:545888b176d01bc3329eb3817724d097ba88109917b1a8699bd8e9806ad1904b`.
- Projection receipt: `1,461` bytes / SHA-256 `bb8726739e124c07290cf679ec26dd07c6fc7e18f96212fb199f58f47a63a6e8`.
- Public tree manifest: `43,793` bytes / SHA-256 `d2ca12ad3174bd588e5b40ab177cc267bc8780074b9dea7a41d3a955dab3a9fa`.
- WASM substitution receipt: `818` bytes / SHA-256 `9008caebeb0d774188fde54c3c4987b521fd196369146c856b7583d3b97cd326`.
- Validation receipt: `654` bytes / SHA-256 `6df580afa50d7674afdff582dc7bd6edf0d7330fe0e910f90388456f14914a9f`.
- Required roles: public conformance runner, tracked WASM family, WASM
  candidate tool, Windows x64 candidate build entrypoint: `4/4 PASS`.
- Projected teul-named path/source/artifact count: `0`.

An additional public-SPEC-history link check failed closed because historical
candidate manifests are intentionally not CURRENT-linked. That check is not
part of the existing W99 4-role contract; no SPEC history was edited and no
release status was inferred from it.

## Windows x64 A/B

The existing official builder compiled the same fixed projection in two
separate output roots with offline/locked dependencies.

- Artifact: `ddonirang.exe`.
- A/B count: `1/1`.
- A/B bytes: `7,043,584 / 7,043,584`.
- A/B SHA-256: `3540b047c6736acb6f7defe9eb5d602ef784ff3d2ee93e32cc4066f9a7b3cffb`.
- A equals B: `true`.
- PE stack reserve A/B: `16,777,216`.
- Forbidden path occurrences A/B: `0/0`.
- teul-named artifact count A/B: `0/0`.
- Startup/help A/B: `PASS`.

## Product workflow and failure boundary

The existing fixed Git-blob fixture
`pack/ddn_local_project_graph_v1/fixtures/project_run_physics_v1.json` was used
as external input to both binaries.

- Semantic identity: `ddn.project-run.v1`.
- Target/options: `앱`, `--inspect-graph`, `--inspect-lock`, atomic `--out`.
- Exit A/B: `0/0`.
- Result bytes A/B: `16,488 / 16,488`.
- Result SHA-256 A/B: `f9c2e36f4117d4a523438c5ab3a88948c769fc4a4b48c99e9dd6495bd7f29578`.
- Result A equals B: `true`.
- Positional start plus `--virtual`: exit `2`, `E_CLI_OPTION_CONFLICT`.
- Conflict artifact count and partial publish: `0/0`.

## Anti-meta, review and nonclaims

- Existing projection/remap/validator tests reused: `58`.
- Existing candidate builder/projection tool/product fixture reused.
- New test/pack/runner/framework/meta-test: `0/0/0/0/0`.
- New reviewer/worktree/branch/task: `0/0/0/0`.
- Protected untracked VC06/VC17/P1 custody: byte-untouched and unstaged.
- Review bundle target: VC13 strict Selection + W100 tracked-WASM path-clean
  refresh + W101 current-source Windows A/B, using only the existing rolling
  reviewer after management dispatch.

This handoff does not claim VC13/P1/P5/P6/V1 closure, exact V1 membership,
readiness, package/release, public executable naming, physical teul deletion,
legal/signing/distribution approval, activation, Owner Human Smoke PASS or
Human PASS.

Status: `P5_VC13_CURRENT_SOURCE_WINDOWS_AB_SUCCESSOR_W101_IMPLEMENTED_UNDER_REVIEW`.
