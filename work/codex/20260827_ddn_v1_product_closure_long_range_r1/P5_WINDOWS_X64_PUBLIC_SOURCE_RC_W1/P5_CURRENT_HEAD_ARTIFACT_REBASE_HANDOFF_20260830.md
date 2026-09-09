# P5 current-head public-source Windows x64 candidate rebase handoff

Date: 2026-08-30

## Scope and status

This handoff fixes a current-product-head P5 candidate identity by reusing the
existing public projection, WASM remap and Windows x64 build entrypoints. It
does not promote the candidate to a public release artifact.

```text
STATUS: P5_CURRENT_HEAD_CANDIDATE_FIXED_UNDER_REVIEW
CURRENT_AUTHORITY: internal SSOT v25.35.0 / RD-001~490
PUBLIC_SPEC: Language SPEC v0.6.0
PRODUCT_SOURCE_HEAD: 7ed20696f93eafa4fe3cb4b85c8a6102e6d57f04
PRODUCT_SOURCE_TREE: 76aaafd3338ca2c8388cd2d06263553ce6d26c9a
EVIDENCE_FIXED_COMMIT: 9c6366abb2c40a2cc1b3040b5de2ff6434582b65
EVIDENCE_FIXED_TREE: fab566425a93f025b28f887b6be9dc78a3d8be10
EVIDENCE_FIXED_PARENT: 7ed20696f93eafa4fe3cb4b85c8a6102e6d57f04
```

The fixed commit changes exactly the existing P5 projection manifest and
rebinds its `source_commit` from the historical P5 source to the current fixed
product source. Product source, tests, packs, tracked WASM, UI, SSOT and public
SPEC changes are zero.

```text
MANIFEST_PATH: work/codex/20260827_ddn_v1_product_closure_long_range_r1/P5_WINDOWS_X64_PUBLIC_SOURCE_RC_W1/PUBLIC_PROJECTION_V25_35_WINDOWS_X64_PATH_CLEAN_MANIFEST.detjson
MANIFEST_BYTES: 9327
MANIFEST_SHA256: a198c05e8ee02ee640e5b951690e53639fc3d3585359d09a13972bb5da39dcc6
FIXED_DIFF: exactly 1 tracked evidence/custody path, 1 line
PRODUCT_SOURCE_DIFF: 0
TEST_DIFF: 0
PACK_DIFF: 0
TRACKED_WASM_DIFF: 0
UI_DIFF: 0
SSOT_DIFF: 0
SPEC_DIFF: 0
```

## Current-head WASM candidate

The existing official candidate-only WASM build entrypoint materialized Git
blobs with LF in an isolated build directory and built the fixed source head.
It did not refresh the tracked WASM family.

```text
WASM_CANDIDATE_DIR: I:/home/urihanl/ddn/codex/build/p5-v25-35-current-head-7ed20696-wasm/wasm/ddonirang_tool
WASM_CANDIDATE_SEMANTIC_IDENTITY: sha256:e5b4e19512cc9fccbf34640eaaa14d4c542c637d8ba3ab5b3bb487c296144fea
WASM_BYTES: 5559604
WASM_SHA256: 017e43e8a6a3fdb5ef383629ed4e9394efcc6ba37eeda1e2662f2eafb4e66eab
WASM_REMAP_RECEIPT_BYTES: 2470
WASM_REMAP_RECEIPT_SHA256: d882700bed98d41ac212425f9d506527ba5f3705f8bbe3b47d4efdcc3407a73b
WASM_INTERNAL_ABSOLUTE_PATH_COUNT: 0
WASM_OFFICIAL_STORE_PATH_COUNT: 0
WASM_PRIVATE_INCLUDE_COUNT: 0
WASM_UNKNOWN_PATH_COUNT: 0
TRACKED_WASM_WRITE: 0
PUBLIC_MEMBERSHIP: false
```

## Public projection and validation

```text
PUBLIC_PROJECTION_DIR: I:/home/urihanl/ddn/codex/out/ddn-v1-p5-v25-35-current-public-projection-7ed20696-r1
PUBLIC_RECEIPT_DIR: I:/home/urihanl/ddn/codex/out/ddn-v1-p5-v25-35-current-public-receipts-7ed20696-r1
PROJECTED_FILE_COUNT: 898
BEFORE_PUBLIC_TREE: sha256:b4c09c9ee3e58b005786f45645eb8d94e1810502cf7514111737823db1194ada
AFTER_PUBLIC_TREE: sha256:f55926eefe27129d1e86933c2443796b288ef51bacd54a67a6e92caf782e9a43
PUBLIC_PROJECTION_RECEIPT: 1448 bytes / 298658e4896b4734f398f391e4e0906a88f0c922a945d8d92487ba6f8fe32fad
PUBLIC_TREE_MANIFEST: 235548 bytes / e387caf91a6bdedae267c0b20c4fce9c159c563f4ba75a9f634b2661bfc16a37
WASM_SUBSTITUTION_RECEIPT: 818 bytes / 6435961da26949a264bc7c457d80806fe37dd521f29dc3f2c9c673a560fe875b
VALIDATION_RECEIPT: 654 bytes / 7af02341e9634af4ac4cc8bf3d4b2228b8fa951f369c3e1c373d5813d6bc2d45
VALIDATION_STATUS: PUBLIC_PROJECTION_VALIDATION_PASS
REQUIRED_ROLES: PUBLIC_CONFORMANCE_RUNNER / TRACKED_WASM_FAMILY / WASM_CANDIDATE_TOOL / WINDOWS_X64_CANDIDATE_BUILD_ENTRYPOINT
TRACKED_SOURCE_WRITE_COUNT: 0
```

The optional historical-SPEC-link check was not added to the release contract:
it correctly fails on preserved non-current candidate manifests. The current
public SPEC pointer remains v0.6.0 and was not modified.

## Windows x64 A/B candidate evidence

Both builds used the same projected public source, offline Cargo resolution,
the existing reproducible linker/remap configuration and separate output
roots.

```text
WINDOWS_A_ROOT: I:/home/urihanl/ddn/codex/out/ddn-v1-p5-v25-35-windows-x64-current-a-7ed20696
WINDOWS_B_ROOT: I:/home/urihanl/ddn/codex/out/ddn-v1-p5-v25-35-windows-x64-current-b-7ed20696
WINDOWS_X64_PUBLIC_CANDIDATE_BUILD: A PASS / B PASS
WINDOWS_EXECUTABLE_STARTUP: A 2/2 PASS / B 2/2 PASS
WINDOWS_PATH_SCAN: A 0 / B 0
WINDOWS_PE_STACK_RESERVE: A 2/2 PASS / B 2/2 PASS (16777216 bytes)
WINDOWS_BINARY_DETERMINISM: 2/2 PASS
ddonirang-tool.exe: 8540160 bytes / 9563758c30f14b0dc88d18e0a94f34c5aa3b79faad8b718b514a966acd4c61fd / A==B
teul-cli.exe: 21862400 bytes / 73a56b5369feebafb8092d6f9d17564a4f80df1a4ab1a4b3011bfeda2fd6ffa0 / A==B
PUBLIC_PROJECTION_VALIDATOR_REMAP_TESTS: 61/61 PASS
GIT_DIFF_CHECK: PASS
```

## Product value, review and remaining gates

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED:
  The current fixed V1 product source, including the latest P4 runtime/CLI
  custody, now produces deterministic path-clean Windows x64 executables from
  the bounded public-source projection.
NEW_TEST_ARTIFACT_COUNT: 0
EXISTING_TEST_REUSED_COUNT: 61 plus two full candidate builds and four startups
META_TEST_CREATED: 0
STOP_RULE_APPLIED: YES
NEXT_PRODUCT_DECISION_ENABLED:
  The rolling independent reviewer can assess one coherent P4 plus current-head
  P5 candidate milestone before package/release and P6 sealing decisions.
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
REVIEW_BUNDLE_TARGET: existing management-owned rolling V1 reviewer; management dispatch only
REVIEW_NEEDED_NOW: YES, because compiler path remap and A/B executable identity are release-critical
```

Archive/package/installer format, SBOM/notices, rights/license, signing,
external distribution and public release remain Owner/legal/release gates. P6
remains preparation-only and unsealed until the P5 fixed identities receive the
required independent disposition. This handoff does not claim whole P5 closure,
RC promotion, V1 membership/readiness, release, activation, Owner Human Smoke
PASS, Human PASS or external-user success.
