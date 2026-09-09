# CLI canon `--emit both` full artifact-set atomic authority W51 handoff

## Status

- `IMPLEMENTED_PENDING_COHERENT_REVIEW`
- Persistent goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` remains active.
- This is one reversible CLI/teul convergence vertical. It does not close V1, P5, release, activation, or Human PASS.

## Authority and lineage

- Live internal authority checked for this work: SSOT v25.47.0 / RD-001~543.
- Public Language SPEC: v0.6.0, unchanged.
- Baseline/handoff parent: `824a8f9fa871ae8aea8dd8ef7929f606e44fa758`.
- Product fixed commit: `2fd70e7901295a59f2c71bfb62ff2af66ee1bdf9`.
- Product fixed tree: `bf1a0071dd5c02cc094e743c89f418f2da312d6f`.
- Direct parent relation: yes. Merge commit count: 0.
- Previously supplied review commits `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf` and `bc84d81d4faa55974975bdb7ec60cb18d9a7ebda` are already ancestors; they were not recreated or broadened.

## User workflow changed or unblocked

For `teul-cli canon --emit both`, canonical DDN, derived fix-its, and the optional explicit fix-it, diagnostic, and metadata sidecars now form one atomic success set. If any destination cannot be committed, none of those success artifacts is published. This removes a concrete partial-publish path while keeping command spelling, output schemas, and semantic authority unchanged.

## Exact product diff

- `tools/teul-cli/src/cli/canon.rs`
- Source working-tree bytes after exact restore: 59,443.
- Source working-tree SHA-256 after exact restore: `5b13607522645ba065c49cd9655ef6bdb3a08229697ffb55d43eccdfc8d026cf`.
- Product source files outside this path: diff 0.
- New pack: 0. New runner: 0. Meta-test: 0.
- One colocated Rust product regression test was added to the existing canon test module.

## RED, implementation, and GREEN

Initial product-facing RED used an explicit optional fix-it target plus diagnostic and metadata targets while the derived fix-it target was blocked. The prior sequential path returned `E_CLI_WRITE` after publishing the explicit fix-it alone.

The implementation routes the general `EmitKind::Both` success path through one `write_text_artifacts_atomic` call containing:

1. optional explicit fix-it JSON,
2. optional success diagnostic JSONL,
3. optional metadata JSON,
4. derived canonical DDN,
5. derived fix-it JSON.

Focused final GREEN:

- `both_emit_optional_sidecar_failure_publishes_no_partial_artifact`: 1/1 PASS.
- Failure attempt: canonical/fix-it/diagnostic/metadata partial publish count 0.
- Retry after removing the blocked target: all five expected files published.

## Regression and mutation evidence

- Canon module: 15 PASS + the same pre-existing 2 FAIL; new drift 0.
- Full `teul-cli` binary suite: 1,047 PASS + the same pre-existing 9 FAIL; new drift 0.
- Risk mutation: replaced the shared atomic commit only in the new `--emit both` path with sequential writes.
- Mutation RED: focused test failed because canonical output was published before the blocked derived fix-it target.
- Exact restore: 59,443 bytes / SHA-256 `5b13607522645ba065c49cd9655ef6bdb3a08229697ffb55d43eccdfc8d026cf`.
- Restore GREEN: focused 1/1 PASS.
- Mutation/test temporary residue with task prefix: 0.
- `git diff --check`: PASS.

## Protected custody and boundaries

- Four pre-existing task-owned untracked session deltas were preserved byte-for-byte and remained unstaged.
- `docs/ssot/**`, `publish/spec/**`, lang/tool product semantics, tracked WASM, Workbench UI/copy/layout, release projection, membership, and public executable naming: diff 0.
- No new review task, review worktree, branch, or goal was created.

## Review bundle

This fixed target is ready to join the existing rolling reviewer’s coherent CLI canon artifact-atomicity bundle W47~W51. No independent PASS is claimed here.

## Nonclaims

This handoff does not claim whole CLI convergence, teul-cli retirement, required dependency 0 across every V1 surface, P0~P6 closure, V1 membership/readiness, release/activation/legal approval, or Owner Human Smoke/Human PASS.
