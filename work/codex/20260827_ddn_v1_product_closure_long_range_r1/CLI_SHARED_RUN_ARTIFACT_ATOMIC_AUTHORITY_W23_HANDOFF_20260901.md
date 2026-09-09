# CLI shared run artifact atomic authority W23 handoff

## Session and authority

```text
AI_PROVIDER: OpenAI
AI_SURFACE: Codex local task
AI_CAPABILITY: product single-writer implementation and verification
SESSION_NICKNAME: DDN V1제품마감Codex
PROJECT_ROLE: DDN V1 closure execution owner / file owner
RETURN_LABEL: [DDN V1제품마감Codex -> Codex관리Work]
GOAL_STATUS: ACTIVE
```

The filesystem Owner-approved current was reverified read-only as internal SSOT
`v25.47.0 / RD-001~543` and public Language SPEC `v0.6.0`.

```text
docs/ssot/CURRENT.md:
  5c4fdea1f0a42a7f1315bcac44dd5249e77f1e6aa4fc78c7065ee69cd53d3b04
docs/ssot/ssot/CURRENT.md:
  40b116735b834f0eecb2c252cc77f73a01a8be06b85421de1d53f2d1b9e534af
SSOT_INDEX_v25.47.0.md:
  2f827e7f55d23def55be590b57482e376b1d9c43cd7db2c9f72271e59c556838
SSOT_ALL_v25.47.0.md:
  d4d9bb661f1424ae5d16a6b70dc86a6bef22d13766820f6001c8f2b28f83b5e4
SSOT_ALL_MANIFEST_v25.47.0.md:
  d8a9fed64085efffefd9eac4573d7ab18975b59bebdea2009e3215a7b9268493
CURRENT_SHA256_v25.47.0.md:
  f1869520079909eed85f2737c27a0aada3b5d013ac6c5bb41a0c781a3e501f4d
publish/spec/CURRENT.md:
  6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0
SUCCESSOR_IMPACT: UNAFFECTED_WITH_ADDITIVE_OUT_OF_SCOPE_SUCCESSOR
SSOT_CHANGE: 0
PUBLIC_SPEC_CHANGE: 0
```

The earlier target-bound review commits are already ancestors of this lineage:

- CLI shared-test review `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf`
- P5 current-source Windows review `bc84d81d4faa55974975bdb7ec60cb18d9a7ebda`

The existing rolling reviewer handle
`01a04b17-66bb-7fa3-b827-53ad450005b4` is therefore present. Slice-local
SPEC history, PathIR public contract, public test/view/repl membership, and
VC17 landing remain frozen individually; they are not a whole-goal blocker.

## Lineage and exact ownership

```text
BASELINE: ec050ebcfc0f2ea82f42755a434a8953b4568ce7
PRODUCT_FIXED: 07ed3607066fb12e676484a6a6c097aba1de9576
PRODUCT_FIXED_TREE: 0e3f0d040265e3686b3708653e4074db79b75ef1
DIRECT_PARENT: ec050ebcfc0f2ea82f42755a434a8953b4568ce7
MERGE_COUNT: 0
EXACT_FILE_OWNER: tools/teul-cli/src/cli/run.rs
PRODUCT_CHANGED_PATH_COUNT: 1
```

No new branch, worktree, task, goal, reviewer, pack, runner, or test file was
created.

## Product workflow changed

The retained `teul-cli run --summary-json/--trace-json` adapter already consumes
the shared lang/tool runtime authority. W23 removes its two remaining direct
publication writes and routes both outputs through
`ddonirang_tool::artifact_output::write_text_artifact_atomic`.

This changes a real user/internal workflow: a failed summary or trace replacement
can no longer publish a truncated target. It does not add a private parser,
runtime, value, canon, or fallback authority and does not promote the retained
adapter to a public command.

The existing focused workflow test was extended in place to request both outputs
and prove that the standalone trace equals the summary's
`public_observation_trace`. No new test function or framework was added.

## RED, implementation, and verification

Pre-change bounded source evidence:

```text
DIRECT_FS_WRITE_COUNT: 2
SHARED_ATOMIC_WRITE_COUNT: 0
BASELINE_FOCUSED_TESTS: 2/2 PASS
```

Post-change evidence:

```text
DIRECT_FS_WRITE_COUNT: 0
SHARED_ATOMIC_WRITE_COUNT: 2
SOURCE_SHA256_AFTER_IMPLEMENTATION:
  2287defcd893f7e0c06321c676b224191fe1ecc0cbc77be13573e4341290ceb4
RUSTFMT_FILE_CHECK: PASS
GIT_DIFF_CHECK: PASS
TEUL_CLI_BUILD: PASS
FOCUSED_TESTS: 2/2 PASS
SHARED_ATOMIC_FAULT_REGRESSION: 1/1 PASS
```

Actual native product workflow, repeated twice against the V25 supported-profile
fixture:

```text
SUMMARY_BYTES: 20078
SUMMARY_SHA256_A_B:
  50f07c707e1b97a0d525157dd5dd9fbcd37dc73f02d21e1393550528d5b91267
SUMMARY_REPEAT_BYTE_EXACT: PASS
TRACE_BYTES: 724
TRACE_SHA256_A_B:
  c2bb26bce94e37b4afb6fa9b879adf24a0670170073f4166794568951e3be0f0
TRACE_REPEAT_BYTE_EXACT: PASS
TRACE_EQUALS_SUMMARY_PUBLIC_OBSERVATION_TRACE: PASS
TEMP_RESIDUE: 0
```

An actual directory-as-output fault returned exit `1` with
`E_SHARED_RUNTIME_SUMMARY_WRITE`, existing/partial child publication `0`, and
temp residue `0`.

One risk-relevant mutation replaced one shared atomic call with `fs::write`:

```text
MUTATION_DIRECT_WRITE_COUNT: 1
MUTATION_SHARED_ATOMIC_COUNT: 1
MUTATION_GUARD: RED
MUTATED_SOURCE_SHA256:
  74d8710e21a50dbb0542eca62bfe5a3b817fc1a2355794788f83656668a46630
RESTORE_SOURCE_SHA256:
  2287defcd893f7e0c06321c676b224191fe1ecc0cbc77be13573e4341290ceb4
RESTORED_GUARD: GREEN (direct 0 / shared atomic 2)
RESTORED_FOCUSED_TEST: GREEN
MUTATION_RESIDUE: 0
```

Native behavior is directly GREEN. WASM and Workbench semantic payloads were not
changed by this retained output adapter and were not re-promoted from historical
fixed-target evidence; `SEMANTIC_FIELD_CHANGE=0` and
`JS_SEMANTIC_RECONSTRUCTION=0` for this slice.

## C0~C8 actual state

| Gate | Current bounded state |
|---|---|
| C0 | Historical 91-command registry remains custody; no bulk promotion. |
| C1 | `ddn.project-run.v1` remains fixed; executable/package/alias naming remains OPEN. |
| C2 | Shared lang/tool canon, preprocess, runtime, value and artifact-output authority is preserved. |
| C3 | Public test/view/repl membership remains slice-local OPEN. |
| C4 | Migrated/shared workflows have private teul semantic fallback 0; W23 removes two retained direct output writes. |
| C5 | Bounded V1-required build/test/pack/publish teul execution dependency remains 0. |
| C6 | W23 native summary/trace payload and failure boundary are deterministic; WASM/Workbench fixed-target claims are not broadened. |
| C7 | Existing reviewed P5 target remains bound; later W18~W22 source/release custody remains queued as its own coherent review bundle. |
| C8 | Candidate projection excludes teul; physical deletion and final public retirement remain Owner-gated. |

## Anti-meta, review, and next gate

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED:
  shared-runtime run summary/trace replacement is now atomic and fail-closed
REUSED_TEST_COUNT: 3 product-facing surfaces
NEW_TEST_ARTIFACT_COUNT: 0
NEW_PACK: 0
NEW_RUNNER: 0
META_TEST_CREATED: 0
STOP_RULE_APPLIED: YES
ACTIVE_REVIEW_TASK_COUNT: 0
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
REUSABLE_ROLLING_REVIEWER_COUNT: 1
REVIEW_BUNDLE_TARGET:
  W23 plus the next nearby retained shared-output authority vertical
```

## Remaining gates and nonclaims

Remaining teul custody consists of INTERNAL/DEFERRED command code and the
physical crate/binary/package. Required execution dependency remains bounded at
zero, but whole-source authority-zero and exact physical retirement still need
their final inventory, coherent parity review, backup/hash/restore evidence, and
Owner deletion approval.

This is `IMPLEMENTED_UNDER_REVIEW`. It does not claim whole C0~C8 closure,
PathIR public-contract closure, VC17 landing, teul physical retirement, P0~P6
closure, V1 membership/readiness, final RC/release, activation, legal approval,
Owner Human Smoke, or Human PASS.
