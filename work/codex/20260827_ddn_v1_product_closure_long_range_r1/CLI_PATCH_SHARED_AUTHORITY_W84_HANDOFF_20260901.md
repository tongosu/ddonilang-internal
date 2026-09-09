# CLI patch shared authority W84 handoff

## Status

- `CLI_PATCH_PROPOSE_PREVIEW_APPROVE_APPLY_SHARED_AUTHORITY_IMPLEMENTED_UNDER_REVIEW`
- whole V1 CLI convergence, command membership, executable naming, teul-cli retirement, V1 readiness and release remain open.

## Authority and lineage

- live internal authority checked read-only at final handoff: v25.49.0 / RD-001~543
- successor impact from v25.47.0: `ADDITIVE_CUSTODY_ONLY`; new semantic RD 0 and no W84 product meaning change
- public Language SPEC: v0.6.0
- baseline: `5e63c0872e07da197fb72c189c2602c887430d28`
- product fixed: `491e164a3f726732b8638dc0bb763df67fb2cf83`
- fixed tree: `3302ad7d05b9e34ea6f6532ee0238dd84d04ed3d`
- merge count: 0

## Product change

- `tool/src/patch_workflow.rs`: owns patch proposal, preview, approval hash, apply, canonical check and atomic artifact publication.
- `tool/src/lib.rs`: exposes the native-only shared workflow.
- `tools/teul-cli/src/cli/patch.rs`: clap format adapter and shared workflow calls only.
- teul private patch implementation count: 1 -> 0.
- shared tool patch implementation count: 0 -> 1.
- no public command membership, executable naming or package decision was made.

## User workflow

The existing W90 workflow remains `source -> propose -> preview -> approve -> apply`. The semantic implementation now lives in the shared tool authority and the teul command is a consumer. Approval hash mismatch fails before artifact publication.

## Verification

- `cargo check -p ddonirang-tool --lib`: PASS.
- `cargo check --manifest-path tools/teul-cli/Cargo.toml`: PASS.
- existing W90: G01 preview PASS, G02 approve PASS, G05 lint-suggest PASS, G07 propose PASS.
- direct LF Git-blob-equivalent W90 G03 workflow: approve exit 0; apply exit 0; output `인사 <- 3.` / `대상 <- 2.`.
- approval-after-patch-mutation: exit 1, `E_PATCH_APPROVAL patch_hash 불일치`, output publish false.
- full tool lib: 585/588 PASS; two isolated-checkout SSOT-dependent ai_prompt failures and one unchanged PathIR definedness test failure are outside the three changed paths and are not promoted or hidden.
- WASM library check remains blocked by the pre-existing ungated `dataset_workflow -> artifact_output` native dependency. The new patch module is explicitly native-only and adds no WASM import failure.
- `git diff --check`: PASS.

## Mutation

- risk: approval hash validation bypass.
- mutation: disable `approval.patch_hash != expected_hash` rejection.
- RED: altered patch was accepted with exit 0 and published `인사 <- 4.`.
- exact restore SHA-256: `05de51fd683689e4e3525e95f31defa1fb9a91a368879760b879d187f6bbcc10`.
- GREEN: altered patch exit 1; partial publish 0; valid patch exit 0.
- repository mutation residue: 0.

## Existing runner disposition

The reused W90 runner reported 4/7. G03/G04 fail because the reused checkout runner does not materialize required input paths and G06 is an unrelated existing fixit expectation mismatch. No fixture, pack or runner was changed. The product-facing G03 path was therefore reproduced directly from the existing fixture with LF Git-blob-equivalent materialization; no semantic oracle or new test artifact was added.

## Anti-meta

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: patch semantic authority is usable from shared tool code while preserving the existing CLI workflow.
- `NEW_TEST_ARTIFACT_COUNT`: 0
- `EXISTING_TEST_REUSED_COUNT`: 7 W90 cases plus one direct reuse of G03 fixture
- `META_TEST_CREATED`: 0
- `STOP_RULE_APPLIED`: yes
- `NEXT_PRODUCT_DECISION_ENABLED`: patch workflow can be removed from teul semantic-authority inventory without deciding public membership or physical deletion.

## Nonclaims

This handoff does not claim whole C0~C8 completion, public patch membership, teul-cli binary/package retirement, physical deletion, independent PASS, P0~P6 closure, V1 readiness, release, activation or Human PASS.
