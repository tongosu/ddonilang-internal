# CLI retained canon atomic output authority W19 handoff

## Fixed scope and authority

This reversible internal convergence removes all production `fs::write` calls
from the retained teul canon adapter. Every final ddn/json/fixit/meta/diagnostic
file now consumes `ddonirang_tool::artifact_output::write_text_artifact_atomic`.
It changes no parser, canonical data, public spelling or command membership.

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
BASELINE: ea0906b53bdbd9951db2d5350ee1d164ca119300
PRODUCT_TEST_FIXED: 0c26a1e5d1b38e9bedba1b219160caba05068136
PRODUCT_TEST_TREE: 739ee2b92498794a340881c46c253b3c1536d60b
MERGE_COUNT: 0
```

## Exact product diff

```text
FILE_OWNER: tools/teul-cli/src/cli/canon.rs
DIRECT_FINAL_FILE_WRITES_BEFORE: 10
DIRECT_FINAL_FILE_WRITES_AFTER: 0
SHARED_ATOMIC_WRITER_CONSUMER: YES
```

The affected outputs are the retained adapter's DDN, flattened composition,
notification plan, execution-policy map, binding-control, both-mode canon and
fixit files, explicit fixit file, metadata file and diagnostic file.

Each final file is now independently atomic. The two-file `Both` mode is not
claimed to be a cross-file transaction: if a later exact bundle-transaction
contract is approved, that is a separate product vertical.

## Verification

```text
TEUL_CANON_UNIT: 10 PASS / same 2 semantic baseline FAIL / 12 total
FOCUSED_POST_RESTORE: 1/1 PASS
TEUL_BINARY_BUILD: PASS on coherent external target
LEGACY_INTERNAL_W02_EXIT: 1; fixit+diag files present; temp residue 0
LEGACY_INTERNAL_W90_EXIT: 0; fixit file present; temp residue 0
LEGACY_INTERNAL_W109_EXIT: 1; fixit+diag files present; temp residue 0
BOTH_MODE_EXIT: 0
BOTH_MODE_OUTPUTS: canon/fixits/explicit-fixits/meta = 4/4 present
BOTH_MODE_TEMP_RESIDUE: 0
GIT_DIFF_CHECK: PASS
NEW_PACK: 0
NEW_RUNNER: 0
NEW_TEST_ARTIFACT_COUNT: 0
META_TEST_CREATED: 0
```

The two unit failures are the pre-existing legacy `보임 {}` removal and legacy
Jjaim quiet-output expectation; they are not hidden or promoted. The old W02,
W90 and W109 expected diagnostic details also contain historical drift, so only
the actual current exit and artifact publication behavior is claimed here.

The existing shared-writer fault tests from the direct W18 ancestor remain
applicable: replacement success and injected failure preserving the predecessor
were 2/2 PASS. No test-only semantic lowering was used.

## Mutation and exact restore

The shared call seam was changed temporarily back to one `fs::write`. The
production-source authority guard returned
`RED_DIRECT_CANON_ARTIFACT_WRITE count=1`. The exact atomic implementation was
restored to SHA-256
`c8e715efa86909e7beb56e822cb40185b2f46e712c69b60d88b50c4603d41d83`;
the guard then reported 0 and the focused product test returned GREEN 1/1.
Mutation residue is zero.

## Product value and gate impact

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED:
  retained internal canon artifact outputs preserve a predecessor and publish
  only a complete individual replacement on write failure.
CHANGED_V1_GATE:
  retained canon owns no private direct final-file publication primitive.
DUPLICATE_OUTPUT_AUTHORITY_ELIMINATED: 10 direct call sites -> 1 shared authority
PARTIAL_FINAL_FILE_PUBLISH_PATHS_REMOVED: 10
```

This is internal/deferred custody hardening, not public promotion. Supported
profile canon already used the shared semantic/canonical authority and remains
unchanged.

## Review and nonclaims

W18 and W19 may be appended to the current-source W13-W17 coherent bundle for
the existing rolling reviewer. New reviewer/task/worktree/branch count is 0.

Public test/view/repl membership, executable/package naming, PathIR public
physical contract, VC17 exact landing, rights/license/NOTICE, signing,
distribution and Owner Human Smoke remain isolated OPEN gates. Physical
`tools/teul-cli` deletion remains unauthorized. This is not whole teul
authority0, P5/P6 closure, V1 readiness, release, activation or Human PASS.
