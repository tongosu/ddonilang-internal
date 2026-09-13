# CLI check schema atomic output authority W18 handoff

## Scope

This bounded V1 CLI/teul convergence vertical removes the retained `check
--emit-schema` adapter's direct final-file write. The adapter now consumes the
same shared `ddonirang_tool::artifact_output::write_text_artifact_atomic`
authority already used by canon, proof and symbolic artifact outputs.

```text
AI_PROVIDER: OpenAI
AI_SURFACE: Codex Work
AI_CAPABILITY: product single-writer implementation and verification
SESSION_NICKNAME: DDN V1제품마감Codex
PROJECT_ROLE: DDN V1 closure execution owner / file owner
RETURN_LABEL: [DDN V1제품마감Codex -> Codex관리Work]
ORIGIN_TASK_ID: DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1
INTERNAL_CURRENT: v25.47.0 / RD-001~543
PUBLIC_LANGUAGE_SPEC: v0.6.0
SUCCESSOR_IMPACT: UNAFFECTED_WITH_ADDITIVE_OUT_OF_SCOPE_SUCCESSOR
BASELINE: 05fe67df97976ab57d4c5ae2634abe959fc194fa
PRODUCT_TEST_FIXED: fa3e49f2e457e741b1a06c7d61ad1a06e8603ab7
PRODUCT_TEST_TREE: 06f0e8d7ed3d9b0ec95ae76e856e4369d76dbbe9
MERGE_COUNT: 0
```

## Product change

Exact FILE_OWNER and fixed diff:

```text
tools/teul-cli/src/cli/check.rs
```

The predecessor called `fs::write(schema_path, out)` after separately creating
the parent directory. That path could truncate or partially publish the final
schema artifact on a write failure. The fixed adapter calls the shared atomic
writer, which creates the parent, writes and syncs a sibling temporary file,
atomically replaces the target, and removes the temporary file on failure.

No schema version, field spelling, command membership, executable/package name,
legacy alias, parser, runtime value, canonical form or public API changed.

## Verification

```text
TEUL_CHECK_FOCUSED: 1/1 PASS
SHARED_ATOMIC_OUTPUT_FAULT_TESTS: 2/2 PASS
W03_SCHEMA_WORKFLOW: G01/G02/G03 = 3/3 PASS
W03_LEGACY_RUN_CASES: T10/T11/T12 = same 3 pre-existing FAIL
RUSTFMT_CHANGED_FILE: PASS
GIT_DIFF_CHECK: PASS
NEW_PACK: 0
NEW_RUNNER: 0
NEW_TEST_ARTIFACT_COUNT: 0
META_TEST_CREATED: 0
```

The two reused shared-writer tests prove successful replacement without temp
residue and injected failure before replacement preserving the predecessor.
The W03 runner exercised the real CLI. Its three schema cases passed. Its three
legacy run-option cases remain rejected by the existing shared-runtime option
boundary and are not regressions from this change. The runner-created T12 trace
was restored to its exact Git blob; mutation residue is zero.

An initial binary build reused a target directory across incompatible Cargo
workspace resolutions and failed with a serde_json 1.0.147/1.0.149 metadata
collision. A fresh isolated target built the same source successfully. This is
classified as build-target contamination, not a product defect.

## Product value and gate impact

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED:
  check --emit-schema now preserves the prior artifact on an interrupted final
  write and publishes only a complete replacement.
CHANGED_V1_GATE:
  one retained teul adapter output no longer owns a private non-atomic artifact
  publication path.
DUPLICATE_OUTPUT_AUTHORITY_ELIMINATED: 1
PARTIAL_PUBLISH_RISK_REMOVED: check schema final artifact
```

## Review and nonclaims

The fixed W18 successor is ready to be included in the next coherent
current-source CLI/release review bundle through the existing rolling reviewer.
No new reviewer, review task, branch or worktree was created.

Public test/view/repl membership, executable naming, PathIR public physical
contract, VC17 exact landing, license/NOTICE, signing, distribution and Owner
Human Smoke remain slice-local OPEN gates. Physical `tools/teul-cli` deletion
is not authorized. This handoff does not claim whole CLI retirement, P5, P6,
V1 readiness, release, activation, legal status or Human PASS.
