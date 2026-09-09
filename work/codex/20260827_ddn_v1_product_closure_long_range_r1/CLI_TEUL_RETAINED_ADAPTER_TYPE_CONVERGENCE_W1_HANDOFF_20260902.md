# CLI/teul retained adapter type convergence W1 handoff

## Scope

- AI_PROVIDER: OpenAI
- AI_SURFACE: Codex Work
- AI_CAPABILITY: product single-writer implementation
- SESSION_NICKNAME: DDN V1제품마감Codex
- PROJECT_ROLE: EXECUTION_OWNER / FILE_OWNER
- RETURN_LABEL: [DDN V1제품마감Codex -> Codex관리Work]
- DEEP_RESEARCH_CHECK: NOT_USE — the fixed repository build graph and focused product tests decide this correction.

This handoff records a retained internal adapter correction only.  It does not
choose public executable or package names, legacy alias timing, command
membership, or physical `tools/teul-cli` retirement.

## Fixed product change

- Product fixed commit: `133ebcdb888353efe92614a59c3427d0c5ec335a`
- Product fixed tree: `2515712bd8a298c276bb77b88bcfe8c581aa8751`
- Direct parent: `d02e1f6526eba5f337edfe5b7c0f815fbc8f0325`
- Merge count: `0`

The nested `tools/teul-cli` workspace resolves its direct dependencies from a
different lock graph than the shared `ddonirang_tool` workspace.  The retained
adapter was passing direct `ddonirang_core` enums and direct `serde_json::Value`
objects over shared workflow boundaries.  Cargo therefore rejected the test
binary as distinct same-named Rust types.

The correction exposes only the already-owned internal shared workflow types
from `ddonirang_tool` and makes the retained adapter consume those types.  It
does not add a dependency, alter a wire value, change a command spelling, or
introduce a fallback.

Changed product paths:

- `tool/src/lib.rs`
- `tool/src/warp_workflow.rs`
- `tool/src/latency_workflow.rs`
- `tools/teul-cli/src/cli/run.rs`
- `tools/teul-cli/src/cli/sam_snapshot.rs`
- `tools/teul-cli/src/cli/warp.rs`
- `tools/teul-cli/src/main.rs`

## RED -> GREEN evidence

Baseline RED: the retained `teul-cli` test binary failed with 13 errors:
two `serde_json` identities (`1.0.149` direct versus `1.0.147` through
`ddonirang_tool`) and separate `ddonirang_core` identities at the shared
run/snapshot/warp/latency boundaries.

GREEN after the product correction, using offline existing dependencies and
`I:/home/urihanl/ddn/codex/build/cargo-target-v1-cli-continuation-20260902`:

1. `cargo test -q --manifest-path tools/teul-cli/Cargo.toml supported_profile_run_uses_shared_v25_authority_and_fails_legacy_closed --offline` — 1 passed.
2. `cargo test -q --manifest-path tools/teul-cli/Cargo.toml snapshot_adapter_consumes_shared_keyboard_and_network_projection --offline` — 1 passed.
3. `cargo build -q --manifest-path tools/teul-cli/Cargo.toml --offline` and `teul-cli.exe --help` — exit 0.
4. `cargo test -q --manifest-path tool/Cargo.toml project_run_binds_neutral_identity_inputs_and_rejects_virtual_conflicts --offline` — 1 relevant test passed.

The initial product build failure is the risk-relevant RED.  No synthetic
mutation, new pack, runner, checker, dependency, or meta-test was created.
No residual source mutation remains outside this fixed commit.

## Product and rights boundaries

- V1 required shared runtime adapter build is unblocked for this retained scope.
- `ddn.project-run.v1` remains the approved neutral semantic identity; this change does not alter its input, output, diagnostic, state, or artifact contract.
- `tools/teul-cli` remains retained internal/deferred custody.  This is not physical deletion, public binary/package retirement, or a claim that every historical command is public.
- Native retained adapter build is GREEN.  No tracked WASM, Workbench UI, SSOT, public SPEC, membership, release, activation, or Human result changed.
- Rights/publication attribution remains a separate track.  `PUBLICATION_READY`, `RELEASE_READY`, public package publication, external release, and rights-cleared artifact claims remain unasserted.

## Review and next safe work

No new reviewer, review worktree, pack, runner, or branch was created.  This
meaningful product fixed commit can be included in the next coherent rolling
CLI/teul convergence review bundle; it is not self-approved.

Next safe slice: continue the bounded C0-C8 audit and migrate only another
retained adapter whose shared owner and input/output contract are already
fixed.  `view` remains internal/deferred because its browser/assets projection
contract is not approved for public migration.

## Nonclaims

This handoff does not close P0-P6, CLI convergence as a whole, V1 readiness,
membership, release, activation, legal/rights clearance, publication, or
Owner Human Smoke/Human PASS.
