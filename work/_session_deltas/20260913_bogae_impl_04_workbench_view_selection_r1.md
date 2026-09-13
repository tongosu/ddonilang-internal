# BOGAE-IMPL-04 Workbench view selection handoff R1

## Authority and custody

- Live internal SSOT at execution: `v25.81.0 / RD-001~617`.
- Public Language SPEC: `v0.7.0`.
- BOGAE-IMPL-01 closed predecessor product: `8c0781d1ac10dabea4b4e5699f6b26823bc23dc4`.
- BOGAE-IMPL-01 independent review: `ffcfc8b8ad5fdbbf877757c16d54474e2f5b74fc` (`PASS_TARGET_BOUND`).
- BOGAE-IMPL-04 product: `2ace20a8bb506748bb5ae43746601c5926f2361c`.
- Product tree: `385d964eb7dd14b195e21f01387f05806e0d3303`.
- Product parent: `ffcfc8b8ad5fdbbf877757c16d54474e2f5b74fc`.
- Author and committer: `tongosu <tongosu@myarts.kr>`.
- Merge count: `0`.

## Exact product paths

1. `solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_payload.js`
   - blob: `2b6cd6ab6a0ddd5c932f5c8795ad9f5295a3db74`
   - SHA-256: `86EDC8DD9D2EFCB5920AD847FFACB7F34601149F620C58057D57F540054B2116`
2. `tests/seamgrim_workbench_semantic_view_payload_runner.mjs`
   - blob: `526a60ad6d434d55290e5ce3be4759d0a554386a`
   - SHA-256: `E5D44C0919554C69148348944F962677521CE5AA02495643C21E06E5F6C821CA`

No SSOT, public SPEC, parser, runtime, renderer, state-hash, or public-wire path changed.

## Product behavior

- Project/UI metadata is no longer a fallback for a missing explicit `primary_view` binding.
- Numeric observations remain committed evidence and never select a view family.
- A successful binding requires one available canonical Workbench typed candidate with the existing exact provider identity `ddonirang_tool.wasm_runtime`, existing provenance `native_authoritative_structured_result`, and an explicit matching family.
- Zero candidates, multiple candidates, and a sole candidate that does not match the explicit family resolve to typed failure states with no successful family/key pair for ambiguous or implicit selection.
- Candidate/source/object order is not a winner axis.
- The committed frame and runtime state hash are carried unchanged; selection metadata remains outside the runtime state hash.
- No new semantic identity was introduced.

## Required BIC evidence

- `BIC-WORKBENCH-02`: numeric observations plus project/UI default cannot select a view; committed frame identity remains byte-equivalent.
- `BIC-UNSUPPORTED-01`: explicit family mismatch against the sole typed candidate resolves fail-closed and retains no available projection.
- `BIC-MULTIVIEW-02`: two canonical typed candidates are ambiguous in both object orders; no first/last/default winner exists.

All three are materialized in the existing semantic-view-payload runner rather than a new pack or duplicate owner.

## Verification

- `node --check solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_payload.js`: PASS.
- `node --check tests/seamgrim_workbench_semantic_view_payload_runner.mjs`: PASS.
- `node tests/seamgrim_workbench_semantic_view_payload_runner.mjs`: PASS.
- `node tests/seamgrim_workbench_semantic_view_renderer_runner.mjs`: PASS.
- Console/graph canonical payload runner: PASS.
- Console-grid/grid2d canonical payload runner: PASS.
- Space2d canonical payload runner: PASS.
- Table/text/structure canonical payload runner: PASS.
- `git diff --check`: PASS.

The four-family canonical-view runner still fails at its pre-existing missing execution-receipt fixture. The same `line: renderer status canonical_unsupported` failure was reproduced in a clean detached checkout of predecessor `ffcfc8b8`; it is not attributed to this product diff.

## Independent mutations

Each mutation was applied alone to the product source, produced RED in the focused runner, and was restored exactly before the next mutation.

1. Restore `project.primaryView` as a missing explicit-view fallback: RED at the project/UI default firewall.
2. Choose the first matching candidate from two candidates: RED at `BIC-MULTIVIEW-02`.
3. Ignore explicit-family mismatch for a sole candidate: RED at `BIC-UNSUPPORTED-01`.

Every restore returned the source to:

- blob `2b6cd6ab6a0ddd5c932f5c8795ad9f5295a3db74`
- SHA-256 `86EDC8DD9D2EFCB5920AD847FFACB7F34601149F620C58057D57F540054B2116`

The focused payload and renderer runners were GREEN after final restore.

## Review boundary

Writer status: `PRODUCT_FIXED_PENDING_INDEPENDENT_REVIEW`.

The independent reviewer must bind the exact product/tree/parent above, verify the exact two-path diff, rerun the required BIC cases and at least two high-risk RED/restore/GREEN mutations, and issue an immutable docs-only verdict. This handoff does not reopen BOGAE-IMPL-01 and does not claim whole Bogae, V1 readiness, release, public support, or Human PASS.
