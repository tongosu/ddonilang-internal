# P4 host-resource atomic publication B-01 correction — handoff

## Custody and authority

- Task: `DDN-V1-P4-HOST-RESOURCE-ATOMIC-PUBLICATION-B01-FIX-R1`
- Product worktree: `I:/home/urihanl/ddn/codex/build/worktrees/ddn-p-v1-project-ux-r2-census-r1-20260828`
- Branch: `codex/ddn-v1-p1a-core-supported-ingress-w1-20260829`
- Product fixed commit: `f49fbe19a3a795fa216b7e2ca145a09276ec10f0`
- Direct parent: `f8d0ef1d22bcf463b37d785d1ace1308894083f2`
- Product fixed tree: `74691d953bcd4fd4192989a368d8c862d44d4616`
- Merge count: `0`
- Live authority (read-only): internal SSOT `v25.53.0 / RD-001~553`; public Language SPEC `v0.6.0`.
- Successor impact: `ADDITIVE_OUT_OF_SCOPE`; this correction does not change SSOT, language semantics, membership, readiness, release, or publication authority.

The predecessor B-01 finding was observed at fixed product `8c730857b7590c14c19c5b8889824d37a3af6580`, handoff `d7d157bb5e82496adc4a37f61b29229681c3fde1`, and review `0d2992542c8291f2df596acda562e5440baa5c0c` (`FAIL_TARGET_BOUND`). Its defect was sequential transcript-then-bundle publication: a later invalid target could leave the first artifact published.

## Correction

The existing shared `artifact_output` authority now provides side-effect-free target preflight and lexical normalized overlap detection. Official `run` and `project-run` preflight every requested output before runtime. Record transcript, record bundle, and `project-run --out` (when combined with record) are serialized into one `write_artifact_set_atomic` transaction. A target-directory, duplicate, normalized-overlap, stale staging, or publication failure therefore leaves all predecessors unchanged and publishes no partial result. Existing single-file `--out` behavior remains unchanged when no host-resource record set is requested.

Changed product paths across the correction sequence (and only these paths):

- `tool/src/artifact_output.rs` — normalized target preflight and atomic-set guard.
- `tool/src/bin/ddonirang.rs` — preflight before execution and one-set publication for host record artifacts plus project output.

The immediately preceding `d4b7f77c` product correction and `f8d0ef1d` two-doc handoff remain immutable predecessor custody. `f49fbe19` only makes the normalized-target assertion portable across Windows path construction; it changes no runtime behavior.

No tracked WASM, `tool/src/host_resource.rs`, local-project semantics, UI, `docs/ssot/**`, `publish/spec/**`, teul-cli, or public command naming changed.

## Evidence

- `cargo check -p ddonirang-tool`: PASS (existing warnings only).
- `cargo test -q -p ddonirang-tool --lib artifact_output::tests`: `9/9` PASS, including all-target predecessor preservation, injected second-publication rollback, successful replacement, and normalized duplicate preflight.
- `cargo test -q -p ddonirang-tool --bin ddonirang`: `12/12` PASS, including official record/replay and the B-01 invalid bundle-directory case (`E_SHARED_ARTIFACT_OUTPUT_TARGET_NOT_FILE`, log absent).
- `cargo test -q -p ddonirang-tool --lib host_resource::`: `3/3` PASS.
- Local Project host-resource binding regression: `1/1` PASS.
- WASM feature parity regression `declared_host_resource_native_and_wasm_share_one_receipt_bound_payload`: `1/1` PASS.
- `git diff --check`: PASS.
- Fault evidence: existing artifact-set second-publication failure hook is RED at the injected failure, restores every predecessor, and the normal path is GREEN; residue `0`. No new mutation framework or receipt/meta-test was added.

The pre-fix sequential writer and the original `FAIL_TARGET_BOUND` review are preserved as predecessor custody; no old PASS is promoted. The correction is ready for the existing rolling reviewer only after management binds this handoff. No reviewer task or worktree was created here.

## Scope and anti-meta accounting

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: YES — record workflows no longer leak transcript/bundle/project artifacts on a later target failure.
- `NEW_TEST_ARTIFACT_COUNT`: `0` (existing Rust test modules were extended; no new file, runner, pack, or framework).
- `EXISTING_TEST_REUSED_COUNT`: `9` artifact-set tests + `12` official CLI tests + existing host-resource/local-project/WASM regressions.
- `META_TEST_CREATED`: `0`.
- `NEXT_PRODUCT_DECISION_ENABLED`: whether the shared host-resource contract can advance past B-01 into a single coherent P4 review bundle; all broader VE03/P4/P5 decisions remain open.

## Remaining gates and nonclaims

`P4_SHARED_HOST_RESOURCE_CONTRACT_REVIEW_FAIL_B01` is the current pre-review status. `READY_FOR_SAME_REVIEWER_REREVIEW=YES` after management verifies the fixed/handoff identities. Independent PASS, VE03 closure, broad P4/P1/V1 closure, public executable/package retirement, membership/readiness, Windows RC, release, activation, legal clearance, and Owner Human Smoke/Human PASS are not claimed.

Protected-resource lifecycle mutation: `0`; new reviewer/worktree/branch: `0`; shared-root cleanup/stage/reset: `0`.
