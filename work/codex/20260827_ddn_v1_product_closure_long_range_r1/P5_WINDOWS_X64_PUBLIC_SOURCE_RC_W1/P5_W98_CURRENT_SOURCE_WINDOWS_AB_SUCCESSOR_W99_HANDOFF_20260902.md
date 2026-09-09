# P5 W98 current-source Windows A/B successor W99 handoff

## Authority and lineage

- Persistent goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` (`ACTIVE`)
- Branch: `codex/ddn-v1-p1a-core-supported-ingress-w1-20260829`
- Product/source handoff: `fb82dd9d4372710fd73458da8e217a65f106bfef`
- Product/source tree: `5600295d30a7c365f4ea776e3513401556f61b23`
- Projection-manifest fixed commit: `b6a203c45212f4486fb450d51dbd64621b44f399`
- Projection-manifest fixed tree: `534f39fc76e13a95c24c1e1b76a692f833ddb89c`
- Direct parent: `fb82dd9d4372710fd73458da8e217a65f106bfef`
- Merge count: `0`
- Internal live CURRENT: `v25.49.0 / RD-001~543`
- Public Language SPEC: `v0.6.0`
- Successor impact: `UNAFFECTED_WITH_ADDITIVE_RELEASE_CUSTODY`
- SSOT/SPEC/product-source diff: `0 / 0 / 0`

The existing P5 review remains target-bound in ancestry at review commit
`bc84d81d4faa55974975bdb7ec60cb18d9a7ebda`, with blocking finding `0`
and report SHA-256
`05d9522c900d5c164064a003f92fabc100f64daf40100690b0e3c3747892a6d6`.
W99 does not inherit that verdict onto this successor artifact.

## Exact tracked fixed diff

Exactly one line in:

`work/codex/20260827_ddn_v1_product_closure_long_range_r1/P5_WINDOWS_X64_PUBLIC_SOURCE_RC_W1/PUBLIC_PROJECTION_V25_35_WINDOWS_X64_PATH_CLEAN_MANIFEST.detjson`

The `source_commit` changed from historical `74bfa235...` to exact current
product/source handoff `fb82dd9d...`.

- Manifest bytes/SHA-256: `8,695` / `93b43ef8fd99bbdb0074c4e65d48523e5befeb1ad75a90baa212191a77af2353`
- Manifest Git blob: `65f164feb064c20181df86f945f90b9b6833fabf`
- Product/test/pack/tracked-WASM/UI source changes in this fixed commit: `0`

## Fixed-source WASM candidate

The existing official candidate entrypoint built exact Git object `fb82dd9d`
from an LF materialization under an external build root.

- Candidate root: `I:/home/urihanl/ddn/codex/build/p5-w99-wasm-fb82/wasm/ddonirang_tool`
- Candidate receipt: `2,470` bytes / SHA-256 `9f31496ec5f421f79dfe4d3f51cd69fcd54de4c717d744c8b0d60285534fe173`
- Candidate semantic identity: `sha256:ea5411e2887674f174e3ccdc12565f3f8632abae09296fd82e21e74f0fc350c0`
- Candidate WASM: `5,576,453` bytes / SHA-256 `46d4651db7d85e26e3e9a601f01c74d8138283e838548c3515e3597e93101913`
- Internal/private/official/unknown host paths: `0/0/0/0`
- Tracked-source write count: `0`

## Public projection

- Projection root: `I:/home/urihanl/ddn/codex/out/p5-w99-projection-fb82`
- Receipt root: `I:/home/urihanl/ddn/codex/out/p5-w99-receipts-fb82`
- Projected files: `222`
- Before candidate substitution: `sha256:2ebb034ed587eb11bd0ee1150afc2a35cd9967cb66e8b977dedba8c7fe39577a`
- After candidate substitution: `sha256:cd7b66bbc1f5210d318372e638d43982e2970024401f9a6c9ef13195e7bf4b1e`
- Projection receipt: `1,461` bytes / SHA-256 `3da875df8bc65fe6bbc11d5eabc4613c022ac54dfe7e00fdb218999d6596d67e`
- Public tree manifest: `43,793` bytes / SHA-256 `2136d3df8947061223b75b2b03e317be4429e1f6d021bc5f5a6254515d109734`
- WASM substitution receipt: `818` bytes / SHA-256 `3364448378ac0460a36e18b62543de0292fb0045ff579492aab295443d874be2`
- Validation receipt: `654` bytes / SHA-256 `e321489a24f13e171f341ace3b4e00a5dc8a5fc529cec938e077ab9c24c32497`
- Required roles: public conformance runner, tracked WASM family, WASM candidate tool, Windows x64 candidate build entrypoint: `4/4 PASS`
- Projected `teul-cli` path/source/artifact count: `0`
- Public membership transition: `0`

## Windows x64 A/B artifact

The same fixed projection was built offline into two distinct output roots
through the existing official candidate builder.

- Artifact: `ddonirang.exe`
- Count A/B: `1 / 1`
- Bytes A/B: `7,043,072 / 7,043,072`
- SHA-256 A/B: `33cb0cad360388ddbe0e1c00bbc743c6fe8e0440b530f9e71f0fa8f74f161d11`
- A equals B: `true`
- PE stack reserve A/B: `16,777,216`
- Forbidden path occurrences A/B: `0 / 0`
- teul-named artifact count A/B: `0 / 0`
- Startup/help A/B: `PASS`

The known Cargo PDB filename collision and dead-code warnings were non-fatal
and do not change product or release status.

## Product-facing workflow

The same existing fixture
`pack/ddn_local_project_graph_v1/fixtures/project_run_physics_v1.json`
(SHA-256 `4df16386dbd388e044c334da0c777aa02e45052eff635de5f9769dba6f2dd5ec`)
was supplied as external user input to both binaries.

- Semantic identity: `ddn.project-run.v1`
- Target/options: `앱`, `--inspect-graph`, `--inspect-lock`, atomic `--out`
- Exit A/B: `0 / 0`
- Result bytes A/B: `16,488 / 16,488`
- Result SHA-256 A/B: `f9c2e36f4117d4a523438c5ab3a88948c769fc4a4b48c99e9dd6495bd7f29578`
- Result A equals B: `true`
- Positional start plus `--virtual`: exit `2`, `E_CLI_OPTION_CONFLICT`, artifact `0`
- Partial publish: `0`

An initial invocation looked for the test fixture inside the intentionally
bounded projection and failed with `E_PROJECT_RUN_READ`; no artifact was
published. Re-running with the same fixed Git-blob fixture as external input
returned the expected deterministic result. This is input custody, not a
product or projection failure.

## Reused verification and anti-meta

- Existing projection/validation/remap tests: `58/58 PASS`
- Existing projection validator: `PASS`
- Offline Windows A/B full builds: `2/2 PASS`
- Existing product fixture workflows: positive A/B plus conflict fail-closed
- New test/pack/runner/framework/meta-test: `0/0/0/0/0`
- New review task/worktree/branch: `0/0/0`
- Mutation: none added; existing source-identity, path-scan and projection guards were exercised directly
- Protected untracked VC06/VC17/P1 custody: byte-untouched and unstaged

## Gate effect and nonclaims

`CHANGED_V1_GATE`: current W97/W98 CLI source now has a deterministic,
host-path-clean Windows x64 public-source candidate with projected teul
source/artifact count `0`. This makes the W90-W99 coherent milestone ready for
the existing rolling reviewer after management dispatch.

This handoff does not claim whole P5/P6 closure, archive/package/installer,
SBOM/notices, rights/license, signing/distribution, V1 membership/readiness,
public command or executable naming, teul physical deletion, release,
activation, Owner Human Smoke PASS or Human PASS.

Status: `P5_W98_CURRENT_SOURCE_WINDOWS_AB_SUCCESSOR_W99_IMPLEMENTED_UNDER_REVIEW`.
