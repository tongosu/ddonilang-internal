# CLI warp shared atomic authority W44 handoff

## Identity and scope

- persistent goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` remains active
- authority: internal SSOT v25.47.0 / RD-001~543; public Language SPEC v0.6.0
- branch: `codex/ddn-v1-p1a-core-supported-ingress-w1-20260829`
- baseline: `f493335d712f897d3759841f130509d4fd9caaf5`
- product fixed: `364e987221573dca8e9a92594a9d09d95da56287`
- fixed tree: `4c5027d3a96de759f7459a5805a5ed56f0896425`
- direct parent: exact; merge count: 0

This is a reversible INTERNAL/DEFERRED product convergence. It does not add
`warp` to V1 public command membership or choose executable/package naming.

## User workflow and authority change

The existing `warp bench <input.json>` workflow now constructs the typed core
request, runs the shared core backend, serializes the result, and publishes an
optional artifact through one `ddonirang-tool` workflow authority. The retained
teul command is an adapter only.

For `--out`, the workflow now creates the parent directory and atomically replaces
the final artifact through the existing shared artifact contract. Input/compute/
serialization failure publishes no new artifact and does not overwrite an existing
target. The default non-measured CPU/GPU result remains deterministic. `--measure`
continues to be explicitly host-performance observation and is not V1 semantic
identity or membership evidence.

Exact product paths:

- `tool/src/warp_workflow.rs`
- `tool/src/lib.rs`
- `tools/teul-cli/src/cli/warp.rs`

All tests, packs, tracked WASM, UI, `docs/ssot/**`, and public SPEC changed: 0.

## RED, GREEN, determinism, and regression

- baseline RED: a valid W79 input with `--out` under a missing parent failed with
  OS error 3 and published no artifact.
- fixed GREEN: parent created, exit 0, artifact SHA-256
  `d94996b0287079ac18c0b2f06c6968aeab8d2e8ed5440f4bd111bb2545a39932`.
- CPU strict result: 3/3 identical, stdout SHA-256
  `91cb570a8aba25aa2305f5125b91aac2e7d7a2a64d200de69f274413961d3923`.
- GPU fast result: 3/3 identical, stdout SHA-256
  `ffea883ea3e59ed27e1bcfa1852cdabbc8400f098fe47767c95c252138617b17`.
- stdout and artifact: normalized text and all structured fields exact.
- invalid JSON after a valid publish: nonzero; existing target SHA unchanged.
- core regression: 58/58 PASS.
- shared artifact focused regression: 5/5 PASS.
- teul-cli product build: PASS.
- `git diff --check`: PASS.

Risk mutation replaced shared atomic publication with direct `fs::write`. A missing
parent produced RED (exit 1, artifact absent). The second controlled cycle restored
the canonical LF source byte-exactly, SHA-256
`651d2ce132f0cd10b19f012378e034a3f27bbd099cba6ccb532c6bf5fc50d9a5`,
then returned GREEN; mutation residue 0. The first mutation observation exposed only
new-file EOL materialization drift and was not counted as the exact-restore proof.

## Dependency, anti-meta, and review

- bounded V1-required build/test/pack/publish teul execution dependency remains 0
  under the prior M1/W5 fixed contracts.
- private teul warp request/serialization/output authority: 0.
- new pack/runner/checker/meta-test: 0.
- existing pack reused: `pack/gogae8_w79_gpu_warp`.
- new review task/worktree/branch: 0.
- review bundle target: the next coherent CLI/teul rolling-review milestone.

Status: `CLI_WARP_SHARED_ATOMIC_AUTHORITY_IMPLEMENTED_UNDER_REVIEW`.

This is not whole C0~C8 closure, repository-wide teul authority/dependency zero,
public warp support, physical teul retirement/deletion, P0~P6 closure, V1 readiness,
release, activation, legal approval, Owner Human Smoke, or Human PASS.
