# CLI world-diff shared atomic authority W35 handoff

## Identity

- Authority: internal SSOT v25.47.0 / RD-001~543; public Language SPEC v0.6.0.
- Baseline: `71482f369ad8bae2ccdeefef3d01a87c749607cf`.
- Baseline tree: `efc47ed4888a29b6374a0189a316e565ff252ae1`.
- Product fixed: `5ad38c13822f33cca8e4f96b5417b6241272d9f1`.
- Fixed tree: `eeb61783dff346dd8de519ee5612b9c0b9bcfc46`.
- Direct parent: yes. Merge count: 0.
- Review commit `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf` is already an ancestor of this baseline and was not rebound, merged, or duplicated.

## Product workflow

The existing `world-diff` workflow now consumes `ddonirang_tool::world_diff_workflow` for canonical snapshots, deterministic semantic diffing, artifact construction, and atomic output publication. `tools/teul-cli/src/cli/world_diff.rs` retains only the execution-preview adapter that calls the existing shared run command.

The Workbench-consumed `world_diff_gravity_half.detjson` artifact was reproduced from the shared runtime authority. Absolute and relative project inputs are normalized to the same slash-separated, working-directory-relative execution identity before the shared run, removing host-path-dependent trace identity.

Existing command spelling and artifact schema are unchanged. No public command membership, executable/package naming, alias lifetime, or new semantic family was decided.

Exact product paths:

- `tool/src/world_diff_workflow.rs`
- `tool/src/lib.rs`
- `tools/teul-cli/src/cli/world_diff.rs`
- `solutions/seamgrim_ui_mvp/lessons/rep_phys_projectile_xy_v1/world_diff_gravity_half.detjson`

## Product RED to GREEN

1. Moving the adapter to the missing shared module produced compiler RED `E0583`.
2. The first shared execution produced `E_SHARED_RUNTIME_OPTION_UNSUPPORTED` because the legacy preview requested `no_open=true`; the adapter now uses the existing supported shared-runtime contract without changing the global default.
3. The next execution produced `E_WORLD_DIFF_EXECUTION_HASH` because the shared runtime exposes `public_observation_trace_hash`; the shared workflow accepts that authority and the historical `trace_hash` spelling as input evidence while preserving the existing output field.
4. The fixed artifact initially differed because absolute and relative project paths entered trace identity differently. Shared input normalization removed that host-path dependency.
5. Two independent fixed artifact generations are byte-identical, SHA-256 `63d19e158204279b1bfa9f6cd8f6434bf607f86228e257296681d931ee0c9f22`.
6. A directory passed as `--out` fails closed with `E_SHARED_ARTIFACT_OUTPUT_TARGET_NOT_FILE`, exit 1, published artifact count 0.

## Evidence

- Shared world-diff unit tests: 3/3 PASS.
- Existing world-diff contract and fixed generated-artifact checks: PASS.
- Existing Seulgi gatekeeper pack check: PASS.
- Tool library regression: 557/559 PASS. The two failures are unchanged isolated-checkout missing-`docs/ssot` environment failures in `ai_prompt` golden checks; new W35 regression 0.
- Combined browser runner reaches the browser seam and stops because Playwright is not installed. No download or environment mutation was performed.
- Historical `tool_world_diff_v1` golden expects five lines while the shared run emits two additional metadata hash lines; this is pre-existing evidence drift and was not rewritten into authority.
- Existing projectile representation-pair and onmungchi aggregate runners remain blocked by pre-existing `E_SHARED_RUNTIME_OPTION_UNSUPPORTED` and `anchor_missing` findings, respectively.
- `git diff --check`: PASS.
- New pack/runner/checker/meta-test: 0/0/0/0.

The exact shared atomic-output guard is unchanged from W32. Its risk mutation evidence is reused: guard inversion RED -> byte-exact restore SHA-256 `9abdfe9426519552cba0227ce50d08e1bb333f78e2282a2463f0a8ba081805f7` -> GREEN, residue 0. A redundant mutation was not created.

## Separate frozen gap

`input_tape` remains unmodified. Its `--sam`, `--record-sam`, and `--latency-madi` paths are rejected by the shared runtime with `E_SHARED_RUNTIME_OPTION_UNSUPPORTED` before tape processing. Moving its wrapper alone would not change a user workflow. A separate shared-runtime option contract is required; this slice-local concrete-detail gap is not an overall V1 development blocker.

## Status and nonclaims

- Private teul world-diff canon/diff/artifact semantic authority: 0 for this workflow.
- Native product workflow and atomic failure behavior: GREEN at the fixed target.
- Workbench artifact contract: statically GREEN and refreshed from shared authority; browser smoke is environment-blocked.
- WASM: no new projection or semantic reconstruction; tracked WASM diff 0.
- Ready for the existing rolling reviewer as part of the coherent CLI convergence milestone. Management dispatch only; new reviewer/task/worktree 0.

This does not claim whole C0~C8 closure, all required teul dependencies zero, physical teul retirement, public command membership, Workbench Human PASS, V1 readiness/release, activation, or legal approval.
