# CLI symbolic/proof shared fail-closed authority W42 handoff

## Status

- Evidence class: `IMPLEMENTED_UNDER_REVIEW`
- Current authority: internal SSOT v25.47.0 / RD-001~543; public Language SPEC v0.6.0
- Successor impact: `ADDITIVE`
- Baseline/handoff: `2243e99c3f438f3d6075daa8a70bd9788203f061`
- Product fixed: `abdad475ae8b52afab143d2a30edb0df334a162d`
- Product tree: `70c19e9dddf291cda98221d2e5664236800cad7b`
- Direct parent: yes; merge count: 0

## User workflow and authority change

The existing `symbolic` and `proof` CLI workflows now execute from shared `ddonirang-tool` product modules. The `teul-cli` modules are adapter/re-export only. Four proof-producing workflows now fail closed before artifact publication when equivalence or rewrite validation is false:

- `symbolic prove-eq`
- `proof prove-symbolic-eq`
- `proof prove-relation-eq`
- `proof rewrite-chain`

This removes their private teul semantic owner and prevents false-success exit 0 / artifact publication. Command spelling, public membership, executable/package naming, public PathIR wire, raw DDN assumption ingress, and diagnostic registry are unchanged.

Exact product paths:

- `tool/src/lib.rs`
- `tool/src/proof_workflow.rs`
- `tool/src/symbolic_workflow.rs`
- `tools/teul-cli/src/cli/proof.rs`
- `tools/teul-cli/src/cli/symbolic.rs`

New test artifact count: 0. New pack count: 0. New runner count: 0. Meta-test count: 0. Existing symbolic/proof libraries, packs, and direct CLI workflows were reused.

## Product RED -> GREEN

The baseline binary returned exit 0 and could publish an artifact for all four invalid proof requests:

- `symbolic prove-eq x x+1`: `proof_ok=true equivalent=false`
- `proof prove-symbolic-eq x x+1`: `proof_tactic_ok=true ... equivalent=false`
- `proof prove-relation-eq x+1 0 x 1`: `proof_relation_ok=true ... equivalent=false`
- `proof rewrite-chain x x+1`: `proof_rewrite_ok=false ...`

The fixed binary returns exit 1 and publishes no artifact. The internal fail-closed diagnostics are respectively `E_SYMBOLIC_EQUIVALENCE_NOT_PROVEN_INTERNAL`, `E_PROOF_EQUIVALENCE_NOT_PROVEN_INTERNAL`, `E_PROOF_RELATION_EQUIVALENCE_NOT_PROVEN_INTERNAL`, and `E_PROOF_REWRITE_NOT_PROVEN_INTERNAL`.

Positive equivalent/rewrite workflows retain exit 0 and the existing success output.

## Determinism and mutation

Three fixed repeats produced one identity per positive artifact:

- symbolic/proof equivalence certificate: SHA-256 `d488039d3e596b68d763afc01bfd8c952b9936d24d4504f6e06f47718015ecd3`
- relation certificate: SHA-256 `d985cecc55a19e53520a66200457a39fd6fb000bff528babdd1ffab716c88491`
- rewrite proof: SHA-256 `7fe05fd29fe19666ee167e9f8cbbf5d25c3347ad21ce52d6526a47ebb1f30e74`

One risk-relevant mutation disabled the rewrite checker guard. The invalid rewrite became actual RED: exit 0 with an artifact (`ff2a58131280c9ecad83e819b049210a22decc93b25191346f98d2359c725485`). Exact restore returned `tool/src/proof_workflow.rs` to 3,196 bytes and SHA-256 `21ed49d93d9609c565d2d2d3f5a6d833d15e5e05fa1df1612b1ec7310f6ab2bc`; rebuild returned exit 1 with artifact absent. Mutation residue: 0.

## Regression disposition

- `cargo check --offline --manifest-path tool/Cargo.toml --lib`: PASS
- `cargo check --offline --manifest-path tools/teul-cli/Cargo.toml`: PASS
- fixed `teul-cli` build: PASS
- symbolic library: 17/17 PASS
- proof library: 18/18 PASS
- existing packs: `symbolic_equivalence_v1`, `proof_tactic_symbolic_eq_v1`, `proof_relation_equivalence_v1`, `proof_tactic_rewrite_chain_v1`, and `symbolic_rational_expr_v1` PASS
- tool library regression with a task-specific target: 560 PASS / 2 FAIL. Both failures are the pre-existing isolated-worktree `docs/ssot` absence in `ai_prompt`; new regression count is 0.
- An initial run using the shared target cache resolved stale diagnostics from another worktree. Cargo metadata proved all live path dependencies point at this product worktree; rerunning with the isolated W42 target produced the result above. No shared target cleanup or repository mutation was performed.

## Frontdoor, dependency, and custody boundaries

- Applicable native CLI: GREEN.
- WASM/Workbench: no public projection or semantic transition in this slice; public PathIR/assumption/receipt work remains frozen at its exact contract gate.
- Partial artifact publish for all four tested invalid requests: 0.
- Private teul symbolic/proof implementation authority for the moved module surfaces: 0.
- `teul-cli` physical package/binary and other internal/deferred command custody remain preserved.
- Whole V1 build/test/pack/publish dependency 0 and physical retirement are not claimed by this slice.
- `docs/ssot/**`, public SPEC, tests, packs, tracked WASM, and visible UI: diff 0.
- Four pre-existing task-owned untracked custody files remained byte-identical and unstaged.

## C0-C8 bounded status and review

- C0 registry/public membership and executable naming: unchanged; unresolved items remain OPEN only in their own slices.
- Shared semantic owner: `ddonirang-tool` for these symbolic/proof CLI workflows.
- Teul adapter private parser/runtime/value/canon fallback for these moved module implementations: 0.
- Public `test`/`view`/`repl` membership, VC17 exact landing, SPEC history, and PathIR public contract remain slice-local gates and do not block this implementation.
- No new review task, reviewer, branch, or worktree was created. The milestone is ready for management to include in the existing rolling coherent CLI/teul review.

This handoff does not claim whole PathIR/Proof P1 closure, ERQ resolution, whole CLI convergence, teul-cli retirement/deletion, public command membership, P0~P6 closure, V1 readiness, release, activation, legal approval, Owner Human Smoke, or Human PASS.
