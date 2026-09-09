# P4 shared runtime legacy trace default clean-break handoff

## Status

- `P4_ACTIVE_ROOT_LEGACY_TRACE_DEFAULT_CLEAN_BREAK_IMPLEMENTED_UNDER_REVIEW`
- This is a bounded product/configuration correction. It is not whole-P4, P1, V1, release, activation, or Human PASS.

## Authority and lineage

- live internal authority: v25.35.0 / RD-001~490
- `docs/ssot/CURRENT.md` SHA-256: `d8224b35d8e10b134ad2c3cd6e94db7d9b32d21363515fa848df91e8972262aa`
- `docs/ssot/ssot/CURRENT.md` SHA-256: `a9bd37606dab7c25be5af527db93c4eb8c9e0cd6f1b54988b4211e67190c8ad4`
- `docs/ssot/ssot/SSOT_INDEX_v25.35.0.md` SHA-256: `911f87fb4516b5c8db342f5180b3e6facbc76292fc44f3ec15c39f148eab7cd6`
- public Language SPEC: v0.6.0, unchanged
- baseline / handoff parent: `53c8c31854b906e22f205287d9408d10568ed2c9`
- product fixed: `4bb9e81a26b1a9078aa50cf43900b812e9640e39`
- product fixed tree: `5b17321a75d491002d801bd477becf6598c0f024`
- product fixed direct parent: `53c8c31854b906e22f205287d9408d10568ed2c9`
- merge count: 0

RD-181 custody says the old determinism grades, `trace_tier`, and four-value `replay_contract` clean-break to the five-axis execution contract without a new active alias. Exact successor public syntax/schema/wire/diagnostics remain OPEN. This slice therefore removes an obsolete active default and does not invent a replacement field.

## Product change

Exact product/configuration diff:

- `ddn.project.json`: remove the root `"trace_tier": "T-PATCH"` default.

Preserved without change:

- explicit historical CLI trace options and historical packs
- `age_target=AGE2`, `det_tier=D-STRICT`, `openness=closed`
- parser/runtime/canon/WASM/Workbench product code
- tracked WASM, SSOT, public SPEC, visible UI, public spelling

## User workflow and RED to GREEN

Concrete blocker: running current archive/local-project inputs from the repository root inherited `T-PATCH`; shared runtime correctly rejected the legacy option before the user's source executed.

Baseline RED:

- command: `python tests/run_pack_golden.py seamgrim_workbench_run_archive_lineage_v1`
- exit: 1
- signature: `E_SHARED_RUNTIME_OPTION_UNSUPPORTED`
- failed before the archive source executed.

Fixed product GREEN used the official native `teul-cli run` frontdoor against five existing product inputs, three repeats each. Every run had exit 0, stderr bytes 0, and byte-identical output within its case:

| Existing input | Output SHA-256 (3/3 identical) |
|---|---|
| `seamgrim_workbench_run_archive_lineage_v1` | `c40bcbf5cf021704a652bca5a4fd4439d2b48c6a33508e10a32412d506e34305` |
| `seamgrim_workbench_run_archive_store_v1` | `aad0f6543683625e872b3596fa2ad8ad7b14945b8f6223e2cd5dc9e570a9d277` |
| `seamgrim_project_store_v0` | `399f3c98ba9fe9e0ea13f412caf532e9d5331d5035bf22766ded19f0d231ecc5` |
| `seamgrim_workbench_revision_conflict_restore_v1` | `eaeb98a67af5034aa9b49016e26ff22a18bc9fec467e581839a5bbff434822bf` |
| `seamgrim_project_snapshot_v0` | `1e5db070cbc9b2d6a89c3c17ee577752e06214f85c568fe847baab798acdc6f5` |

Regression:

- `cargo test -p ddonirang-tool --lib`: 526/526 PASS, 0 ignored, 0 filtered.
- root project JSON and preserved fields: PASS.
- `git diff --check`: PASS.
- an earlier `project_meta` name filter selected 0 tests and is explicitly discarded as evidence.

## Evidence rebase boundary

The generic pack runner progressed past the product RED after the fix, then exposed independent evidence drift:

- five old goldens omit the current deterministic `madi` / `public_observation_trace_hash` summary rows;
- `project_age_target_precedence_v1` carries its own explicit legacy `T-PATCH` fixtures and remains RED with `E_SHARED_RUNTIME_OPTION_UNSUPPORTED`.

Those are `EVIDENCE_REBASE_REQUIRED`, not a reason to restore the forbidden active alias. No runner, pack, checker, fixture, or meta-test was added or edited in this slice.

## Anti-meta and review custody

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: repository-root archive/local-project native execution no longer fails before source execution because of the obsolete default.
- `NEW_TEST_ARTIFACT_COUNT`: 0
- `EXISTING_TEST_REUSED_COUNT`: 5 existing product inputs plus the existing 526-test tool lib suite
- `META_TEST_CREATED`: 0
- `STOP_RULE_APPLIED`: yes; bulk golden/fixture migration stopped when it was shown to be evidence drift rather than additional product behavior.
- `NEXT_PRODUCT_DECISION_ENABLED`: management can decide whether to rebase the old generic goldens/explicit trace fixtures and bundle this bounded P4 correction into the existing rolling product review.
- `NEW_REVIEW_TASK_COUNT`: 0
- `NEW_REVIEW_WORKTREE_COUNT`: 0
- review dispatch: management-only; writer did not wake or create a reviewer.

## Open gates and nonclaims

- exact five-axis product schema/wire/public diagnostics: OPEN
- historical explicit trace fixture migration: OPEN / EVIDENCE_REBASE_REQUIRED
- P2 exact manifest/schema/wire/storage/CAS/DB/autosave/retention/GC/resource declaration: OPEN
- P3 integration dependency on P2: OPEN
- whole P4 determinism/failure/receipt/replay closure: OPEN
- P5 package/installer/signing/rights/license/SBOM/notices/distribution: OPEN
- P6 Owner Human Smoke and all external release gates: OPEN
- no independent PASS, membership/readiness, public release, activation, legal clearance, or Human PASS is claimed.
