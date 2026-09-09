# CLI infer/imitation shared atomic authority W41 handoff

## Status

- Evidence class: `IMPLEMENTED_UNDER_REVIEW`
- Current authority: internal SSOT v25.47.0 / RD-001~543; public Language SPEC v0.6.0
- Successor impact: `ADDITIVE`
- Baseline/handoff: `5fa8fbb6bbaebfa25dfcf917b198ec05a2da7d85`
- Product fixed: `7b79ae69f1bbedde1e363d878a1fc2fdf05df513`
- Product tree: `b4e30f458f48611dc6656c7cea8663c6e761377a`
- Direct parent: yes; merge count: 0

## User workflow and authority change

The existing `infer mlp` and `imitation` workflows now execute their product semantics from `ddonirang-tool`; `teul-cli` is an adapter/re-export only for these two commands. Imitation's three output artifacts are published as one atomic set. This removes the private teul semantic owner for these workflows without changing command spelling, public membership, or executable/package naming.

Exact product paths:

- `tool/src/infer_workflow.rs`
- `tool/src/imitation_workflow.rs`
- `tool/src/lib.rs`
- `tools/teul-cli/src/cli/infer.rs`
- `tools/teul-cli/src/cli/imitation.rs`

New test artifact count: 0. New pack count: 0. Meta-test count: 0. Existing product packs and direct CLI workflows were reused.

## Product RED -> GREEN

Baseline binary was built from `5fa8fbb6...`. With `dataset.sha256` pre-created as a directory, baseline imitation failed after publishing `imitation.dataset.jsonl` (product file count 1). The fixed product preflights and atomically publishes the complete artifact set: the same fault returns `E_SHARED_ARTIFACT_OUTPUT_TARGET_NOT_FILE` with product file count 0.

Risk mutation temporarily replaced the artifact-set transaction with sequential single-artifact writes. The same fault became RED with product file count 1. Exact restore returned `tool/src/imitation_workflow.rs` to SHA-256 `dec0713cb93fb75fd957146602b9cf288a008973bf000f1df7cac90e16a42daf`, rebuilt GREEN with product file count 0, and left mutation residue 0.

## Direct product evidence

Three deterministic fixed repeats produced one identity per artifact:

- `infer.output.detjson`: 136 bytes; SHA-256 `46397b3e7b2da63e3043ea8d8bebc41ca49230855b5fbdb8eef29bb4b355b85`
- `imitation.dataset.jsonl`: 1,051 bytes; SHA-256 `59f0c0f32ad4a1e212011919763f574fdc1b51a21e9bfb572b16d1826ab3cd2c`
- `dataset.sha256`: 72 bytes; SHA-256 `30d6c95fe179fe92619f1ff2472bedef0f930055686e66b73930c67efd60fe35`
- `metrics_curve.detjsonl`: 402 bytes; SHA-256 `f5657b01f21df938e4f0a9747f464ae4f1b9642875df467d19388d36207ff419`

Baseline and fixed direct artifact identities are equal. Fixed stdout SHA-256 values were `a3316a000c33d28412e2353dc0c01474841e39228536598f636d847bea650e7f` for infer and `ee88b3ca2a5b0930a534f885c5ef9632b7ecd1a38ef3beebe46892b2b519b890` for imitation.

## Regression disposition

- `cargo check --offline --manifest-path tool/Cargo.toml --lib`: PASS
- `cargo check --offline --manifest-path tools/teul-cli/Cargo.toml`: PASS
- fixed `teul-cli` build: PASS
- `tests/run_model_artifact_inference_pack_check.py`: PASS
- tool library regression: 560 PASS / 2 FAIL. The two failures are the unchanged isolated-worktree `docs/ssot` absence in `ai_prompt`; they do not touch this slice.
- existing golden runner: `model_artifact_inference_v1` PASS; `gogae8_w85_ondevice_infer_v1` and `gogae8_w86_imitation_learning_v1` FAIL from pre-existing stale expected values. The same actual values occur on baseline and fixed binaries: infer uses model hash `blake3:e5c511e9bbe54dc9e104d0f9feb279ecd6bee254d15c5ec70fbeacce77a11788` while the golden contains `blake3:1391c84a...`; imitation uses dataset hash `sha256:59f0c0f3...` and mismatch series 3/2/1/0 while the golden contains `sha256:7109024d...` and 2/1/0/0. No golden was promoted or rewritten.

## Boundaries and custody

- Applicable native CLI: GREEN.
- WASM/Workbench: no new projection and no semantic transition; both modules remain non-WASM product workflows.
- Product partial publish on the tested failure: 0.
- `docs/ssot/**`, public SPEC, tracked WASM, UI, packs, tests: diff 0.
- The four pre-existing task-owned untracked custody files remained byte-identical and unstaged.
- An initial path-resolution error briefly created two task-owned untracked copies under the shared dirty root. They were detected before use and removed exactly; shared-root residue is 0. No shared-root tracked file was staged, reset, stashed, or cleaned.

## C0-C8 bounded status

- Registry/public membership and executable naming: unchanged and OPEN where previously open.
- Infer/imitation semantic owner: shared `ddonirang-tool` authority.
- Private teul infer/imitation parser/runtime/value/canon fallback: 0 in these two adapters.
- Other teul internal/deferred custody and physical package/binary: preserved.
- Whole required build/test/pack/publish dependency 0 and physical retirement: not claimed by this slice.

## Review and nonclaims

No new review task or worktree was created. This fixed milestone is ready to be queued into the existing rolling coherent CLI/teul review by management. It does not claim whole CLI convergence, teul-cli retirement/deletion, public command membership, P0-P6 closure, V1 readiness, release, activation, legal approval, Owner Human Smoke, or Human PASS.
