# CLI Seulgi decision artifact shared authority W32 handoff

## Fixed identity

- Live authority: internal SSOT v25.47.0 / RD-001~543; public Language SPEC v0.6.0.
- Baseline: `8f650c49fe3bd4038983065e19e347ced91a17e1`.
- Product fixed commit: `52ab31a30e5b092e09c8a62fbd685830e3484d2f`.
- Product fixed tree: `de4ce08ee37e1e353cfd67af8667fe42b3255180`.
- Direct parent relation: yes. Merge count: 0.

## User workflows

Four existing command workflows now consume product-owned `ddonirang_tool` implementations while preserving their existing command spelling and payload behavior:

1. `goal parse`
2. `goal plan`
3. `latency simulate`
4. `safety check`

The implementations continue to consume the existing `ddonirang_core::seulgi` semantic owners. `teul-cli` retains only adapters. No parser, runtime, value, canonicalization, fallback, command, schema, or public naming family was added.

All four file-output paths use the shared atomic artifact writer and the same pre-publication file-target guard. Parent creation and atomic replacement remain covered by the existing shared artifact writer tests.

## Product diff

- `tool/src/artifact_output.rs`
- `tool/src/goal_workflow.rs`
- `tool/src/latency_workflow.rs`
- `tool/src/lib.rs`
- `tool/src/safety_workflow.rs`
- `tools/teul-cli/src/cli/goal.rs`
- `tools/teul-cli/src/cli/latency.rs`
- `tools/teul-cli/src/cli/safety.rs`

## Existing evidence reused

- Goal parse golden: 1/1 exact payload PASS.
- GOAP plan fixture: 1/1 exact selected action/cost/steps payload PASS.
- Latency golden cases: 4/4 exact deterministic hash PASS, including fixed, jitter, saturated L, and late-drop behavior.
- Safety gatekeeper golden: 1/1 exact allowlist result PASS.
- Directory-target fail-closed: 4/4 exit 1 with `E_SHARED_ARTIFACT_OUTPUT_TARGET_NOT_FILE`; published entries 0.
- Shared artifact writer tests: 2/2 PASS.
- Tool library regression: 552 PASS plus the same two isolated-checkout missing-`docs/ssot` environment failures in `ai_prompt`; new regression 0.
- `teul-cli` offline build: PASS.
- `git diff --check`: PASS.

New pack: 0. New runner: 0. Meta-test: 0.

## Risk mutation

The shared non-file target guard was inverted. `goal parse --out <directory>` then lost the shared diagnostic and fell through to generic OS access failure: RED, exit 1. The source was restored byte-exact to SHA-256 `9abdfe9426519552cba0227ce50d08e1bb333f78e2282a2463f0a8ba081805f7`; rebuild and the exact shared diagnostic returned GREEN. Mutation residue: 0.

## Gate impact and open custody

- Private teul semantic authority for the four named workflows: 0.
- Required repository-wide teul dependency: not claimed zero by this slice.
- Native command behavior: PASS at the fixed target.
- WASM/Workbench: no new command projection or semantic reconstruction; tracked WASM and visible Workbench diff 0.
- Public command membership, executable/package naming, legacy alias duration, and physical `tools/teul-cli` retirement remain OPEN.

This target is ready for the existing rolling reviewer as part of the coherent CLI convergence bundle. No new reviewer, review task, worktree, branch, or status-only commit was created.

## Nonclaims

This is not C0~C8 closure, whole teul authority/dependency zero, V1 membership/readiness, P0~P6 closure, Windows/public release, activation, legal approval, or Human PASS.
