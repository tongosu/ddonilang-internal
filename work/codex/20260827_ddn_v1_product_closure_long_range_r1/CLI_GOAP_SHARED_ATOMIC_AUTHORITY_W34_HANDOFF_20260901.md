# CLI GOAP shared atomic authority W34 handoff

## Identity

- Authority: internal SSOT v25.47.0 / RD-001~543; public Language SPEC v0.6.0.
- Baseline: `a481e66d717359709ccb92e9c8bc7368046b34b5`.
- Product fixed: `2e7c51039647d874e2e2cdf8440600ed4dbd33d7`.
- Fixed tree: `224164c745eb23e3c9516402bba5e891f5d37517`.
- Direct parent: yes. Merge count: 0.

## Product workflow

The existing full `goap plan` workflow now consumes `ddonirang_tool::goap_workflow`, completing the GOAP side of the W32 goal/planning family. Its world-state, target, action parsing and `ddonirang_core::seulgi::goap::GoapPlanner` invocation no longer live as private teul authority. `tools/teul-cli/src/cli/goap.rs` is an adapter only.

Existing command spelling and `goap.plan.v1` payload are unchanged. No public command membership, schema, alias, parser/runtime/value family, or executable/package naming decision was made.

Exact product paths:

- `tool/src/goap_workflow.rs`
- `tool/src/lib.rs`
- `tools/teul-cli/src/cli/goap.rs`

## Evidence

- Existing `pack/gogae5_w48_goap_planner/input.json` -> expected plan payload: exact 1/1 PASS.
- Existing output-directory RED before convergence: generic OS access failure, explicit guard absent, published entries 0.
- Fixed output-directory behavior: exit 1 with `E_SHARED_ARTIFACT_OUTPUT_TARGET_NOT_FILE`, published entries 0.
- Tool regression: 554 PASS plus unchanged two isolated-checkout missing-`docs/ssot` environment failures; new regression 0.
- `teul-cli` offline build: PASS.
- `git diff --check`: PASS.
- New pack/runner/meta-test: 0/0/0.

The exact shared output guard is unchanged from W32. Its risk mutation evidence is reused: inversion RED -> byte-exact restore SHA-256 `9abdfe9426519552cba0227ce50d08e1bb333f78e2282a2463f0a8ba081805f7` -> GREEN, residue 0. No redundant mutation was created.

## Separate frozen gap

`input_tape` was audited but not edited. The shared official `run` frontdoor currently rejects `--sam`, `--record-sam`, and `--latency-madi` with `E_SHARED_RUNTIME_OPTION_UNSUPPORTED` before tape read/write is reached. Moving the teul module alone would therefore be wrapper-only work. Supporting those legacy options requires a separate approved shared-runtime option contract; this slice-local gap does not block other V1 development.

## Status and nonclaims

- Private teul GOAP semantic authority: 0 for this workflow.
- Native payload/failure behavior: PASS at the fixed target.
- WASM/Workbench: no new projection or semantic reconstruction; tracked WASM and visible UI diff 0.
- Ready for the existing coherent CLI convergence rolling-review bundle; new reviewer/task/worktree 0.

This does not claim whole C0~C8 closure, required teul dependency zero beyond already proven scopes, physical teul retirement, V1 readiness/release, activation, legal approval, or Human PASS.
