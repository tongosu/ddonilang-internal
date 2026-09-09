# P5 WASM candidate materialization guard handoff

## Authority and lineage

```text
AI_PROVIDER: OpenAI
AI_SURFACE: Codex Work
AI_CAPABILITY: product single-writer implementation and fixed-artifact verification
SESSION_NICKNAME: DDN V1제품마감Codex
PROJECT_ROLE: DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1 single product writer
RETURN_LABEL: [DDN V1제품마감Codex -> Codex관리Work]
DEEP_RESEARCH_CHECK: NOT_USE — current Git objects and local executable build evidence decide this slice.

INTERNAL_CURRENT: v25.32.0 / RD-001~483 / Owner final 2026-08-30
PUBLIC_SPEC: v0.6.0
BASELINE: 2a71996c616d626d4c7850675a096ba42311ee0d
FU02_REVIEW_BOUND: 436b6b6ba3ebbef06a348679051fd48f2b58fcf9
PRODUCT_TEST_FIXED: 6edf6b586d0c0ff62761174fe958a204ce5f6938
PRODUCT_TEST_TREE: 8b771c96dc3705a96daf6ae9b626cb89b9889230
```

The FU02 review commit was integrated by ff-only from its exact parent. The
product fixed commit is its direct successor and changes exactly:

- `scripts/build_wasm_tool.ps1`
- `tests/test_wasm_source_remap_entrypoint.py`

## User and release blocker closed by the implementation

The existing candidate-only entrypoint claimed a fixed-HEAD LF materialization,
but a sufficiently long Windows build root caused Git checkout to omit one
tracked file with `Filename too long`. Git nevertheless returned success and the
entrypoint continued building from an incomplete source checkout.

The product correction:

1. enables repository-local `core.longpaths=true` before candidate checkout;
2. verifies the materialized checkout is byte-clean against `HEAD` before any
   build starts; and
3. fails closed with `E_WASM_CANDIDATE_MATERIALIZATION_INCOMPLETE` if the fixed
   source tree is incomplete.

Default builds, compiler remap policy, tracked WASM, public membership, public
spelling, SSOT, SPEC and visible UI are unchanged.

## RED and GREEN

```text
ACTUAL_RED_BUILD_ROOT:
  I:/home/urihanl/ddn/codex/build/ddn-v1-p5-candidate-b-20260830-2a71996
RED_SIGNATURE:
  Filename too long
  materialized checkout status: 1 deleted tracked file
  entrypoint exit: 0 (incorrect fail-open)
MISSING_PATH:
  work/codex/20260822_ddn_execution_concurrency_w1b_successor_canon_clean_cut/
  DDN_EXECUTION_CONCURRENCY_W1C_SENDER_FILTER_AND_REACTION_PROVIDER_OWNER_DECISION_PACKET.md

FOCUSED_RED:
  tests.test_wasm_source_remap_entrypoint 1 FAIL / 4 PASS
FOCUSED_GREEN:
  tests.test_wasm_source_remap_entrypoint + tests.test_wasm_candidate_remap
  26/26 PASS
```

The post-fix long-path reproduction used only the existing official candidate
entrypoint with `CARGO_NET_OFFLINE=true`:

```text
BUILD_ROOT:
  I:/home/urihanl/ddn/codex/build/
  ddn-v1-p5-candidate-longpath-fixed-20260830-6edf6b58
MATERIALIZED_HEAD: 6edf6b586d0c0ff62761174fe958a204ce5f6938
MATERIALIZED_TREE: 8b771c96dc3705a96daf6ae9b626cb89b9889230
MATERIALIZED_TRACKED_STATUS: 0
WASM_BYTES: 5558787
WASM_SHA256: 58a32eb83527da6da3b39dfb8f335d5293cc6499bbbae628bfe390018a6577bc
INTERNAL_ABSOLUTE_PATH_COUNT: 0
UNKNOWN_PATH_COUNT: 0
PRIVATE_INCLUDE_COUNT: 0
VIRTUAL_ROOT_OCCURRENCES:
  /ddn-src=1
  /ddn-cargo-registry=95
  /ddn-rust-toolchain=21
RECEIPT_BYTES: 2470
RECEIPT_SHA256: 2ad1120cdeeef3521a07bfdda31ac98e9cc34a92fbc20e6d0f30ff8b4655cf28
RECEIPT_SEMANTIC_IDENTITY:
  sha256:2716d1eb7b81b2482766457b174f890eee2ed4258fd43786c7dfc0cd2db0f85b
TRACKED_WASM_WRITE: 0
TRACKED_MANIFEST_WRITE: 0
```

Two pre-fix candidate builds produced byte-identical six-file WASM families,
including the same WASM hash above. One crossed the Windows path-length boundary
and exposed the incomplete-checkout defect; it is RED custody and not release
evidence. The post-fix fixed-head build is the GREEN candidate custody.

## v25.32 impact and preceding gates

| Scope | Impact | Disposition |
|---|---|---|
| P0 shared canon/preprocess | UNAFFECTED | fixed behavior remains scoped |
| P1-A, VC04, VC06, VC09, VC11, VC12 product behavior | UNAFFECTED | no relevant RD-470~483 semantic change |
| P1 membership/readiness claims | REBASE_REQUIRED | membership 40 unchanged; blocker 28, readiness UNCLAIMABLE, `SUPPORTED_FOR_V1=0` |
| P2 durable local-project save/reopen | ADDITIVE | semantic roles remain, exact physical file/field/serialization/storage contract remains OPEN |
| P3 Workbench supported-profile default | REBASE_REQUIRED | project profile identity/default selection remains an Owner product decision |
| P4 whole closure | REBASE_REQUIRED | scoped tests do not close G-A option or G-B unit-registry contracts |
| P5 candidate source materialization | ADDITIVE | this fixed commit closes only the fail-open Windows long-path guard |

Compact Owner decision still required for P2:

```text
DECISION_ID: P2-DURABLE-REVISION-PHYSICAL-CONTRACT
CURRENT_SOURCE_EXAMPLE:
  VirtualProjectSource + expected source hashes provide deterministic in-memory
  edit/run identity, but no approved durable SavedProjectRevision file/wire.
OPTION_A (recommended):
  bind a minimal internal durable revision envelope and atomic replace contract,
  retaining public spelling and richer DB/CAS/autosave/retention as OPEN.
OPTION_B:
  defer durable save and keep P2 limited to in-memory project plans.
IMPACT:
  A unblocks create/open/edit/save/reopen/run; B cannot close the requested P2 workflow.
```

## Anti-meta and review custody

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED:
  Windows candidate builds can no longer silently continue from an incomplete fixed source tree.
NEW_TEST_ARTIFACT_COUNT: 0
EXISTING_TEST_REUSED_COUNT: 2 test modules / 26 cases
META_TEST_CREATED: 0
STOP_RULE_APPLIED: YES
NEXT_PRODUCT_DECISION_ENABLED:
  management may accept or reject this fixed candidate materialization guard for the next coherent P5 review bundle.
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
REVIEW_BUNDLE_TARGET:
  existing rolling V1 product reviewer; dispatch by management only
```

## Nonclaims

This handoff does not claim P2, P3, P4 or P5 closure; Windows x64 package
completion; tracked/public WASM membership; rights/license clearance; public
release or activation; P1/V1 membership/readiness; Owner Human Smoke PASS; or
external-user success. V1.2 JIEUM implementation has not started.
