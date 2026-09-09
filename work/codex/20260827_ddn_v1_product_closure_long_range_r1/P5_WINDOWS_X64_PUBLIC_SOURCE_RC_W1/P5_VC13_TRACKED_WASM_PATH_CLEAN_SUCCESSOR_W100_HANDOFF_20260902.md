# P5 VC13 tracked-WASM path-clean successor W100 handoff

## Authority and lineage

- Persistent goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` (`ACTIVE`).
- Internal live CURRENT: `v25.49.0 / RD-001~543`.
- Public Language SPEC: `v0.6.0`.
- Product/source handoff: `41d84d9ced80ee083e582b87ecd6bb5e6dc2ad5d`.
- Product/artifact fixed commit: `0ba83239a9f8218aaea51c105154f7a2a6c2e65b`.
- Fixed tree: `a39bcab89af832503e2a5dfa92a3c65415acde41`.
- Direct parent: `41d84d9ced80ee083e582b87ecd6bb5e6dc2ad5d`.
- Merge count: `0`.
- Successor impact: `UNAFFECTED_WITH_ADDITIVE_RELEASE_CUSTODY`.

The historical P5 target-bound PASS at `bc84d81d4faa55974975bdb7ec60cb18d9a7ebda`
remains valid only for its fixed target. W100 does not inherit that verdict.

## Product and release blocker changed

VC13 strict Selection refreshed the tracked WASM through the ordinary build
path. The existing release test then produced an actual RED:

- projection/remap/validator tests: `57/58`;
- failing gate: `test_tracked_inventory_is_path_clean`;
- tracked WASM internal absolute path count: `115`.

The official candidate entrypoint was rerun from clean fixed HEAD with
`CARGO_NET_OFFLINE=true`, `CopyToUi=false`, and candidate source remapping.
The candidate was copied through the existing tracked-WASM copy path and the
existing freshness manifest writer. No product source or semantic code changed.

## Exact fixed diff and identities

Exactly two tracked paths changed:

1. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
2. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

- WASM Git blob: `9cb25aca2fc1efa07772bddd35a27b4dae2584c5`.
- WASM bytes/SHA-256: `5,576,576` / `00f574305c6d10b77b7a262e02d9cec677c4e79015d9ddd603eaf30e13abca11`.
- Manifest Git blob: `08c83bbdeb7175aaa8092e1e66d293bd64eae1cb`.
- Manifest Git-blob bytes/SHA-256: `28,754` / `97e1f73b01ecdabab42d9a1681d792a8ae44a0a54c2a4b042a7857f0397daff3`.
- Candidate remap receipt: `2,470` bytes / `a3d86aef8adc7313dcc5a06caa97be3fa3db074cc454e6b4faa54e323891e093`.
- Candidate semantic identity: `sha256:9a2c70852d90cf792f496f22b75437bc06beea44206eed181cb64e9ded5bea82`.
- Internal/private/official/unknown embedded path counts: `0/0/0/0`.

JS, d.ts and package bytes were already identical to the candidate and therefore
have tracked diff `0`. Product source, tests, packs, visible UI, SSOT and public
SPEC diff in the fixed commit are `0`.

## Verification and anti-meta

- Existing projection/remap/validator suite: `58/58 PASS` after the fix.
- Official tracked-WASM freshness: `PASS`.
- Existing P1-A supported-ingress native suite: native `8`, native/WASM exact
  `2`, official CLI positive `4`, official CLI negative `5`, all PASS.
- Existing tracked-WASM parity: `11/11`, deterministic repeats `5`, partial
  summary `0`.
- Fail-closed evidence: the pre-fix tracked artifact itself was the actual RED;
  no receipt/hash meta-mutation was added.
- New test/pack/runner/framework/meta-test: `0/0/0/0/0`.
- New reviewer/worktree/branch/task: `0/0/0/0`.
- Protected untracked VC06/VC17/P1 custody: byte-untouched and unstaged.

## Review and nonclaims

Review bundle target: VC13 strict Selection product change plus W100 path-clean
tracked-WASM materialization, using only the existing rolling reviewer after
management dispatch. This session does not create or wake review infrastructure.

This handoff does not claim VC13/P1/P5/P6/V1 closure, exact V1 membership,
readiness, package/release, public executable naming, physical teul deletion,
legal/signing/distribution approval, activation, Owner Human Smoke PASS or
Human PASS.

Status: `P5_VC13_TRACKED_WASM_PATH_CLEAN_SUCCESSOR_W100_IMPLEMENTED_UNDER_REVIEW`.
