# P5 P2/P3 current-head public-source Windows x64 candidate rebase handoff

Date: 2026-08-30

## Scope and authority

This handoff rebinds the existing P5 public-source and Windows x64 candidate
workflow to the fixed product lineage after the P2 saved-head Run custody and
P3 Workbench saved-head frontdoor verticals. It reuses the existing candidate
WASM, projection, validator and Windows build entrypoints; no new test,
checker, pack or release framework was created.

```text
STATUS: P5_P2_P3_CURRENT_HEAD_CANDIDATE_FIXED_UNDER_REVIEW
CURRENT_AUTHORITY: internal SSOT v25.35.0 / RD-001~490
CURRENT_POINTER_SHA256: d8224b35d8e10b134ad2c3cd6e94db7d9b32d21363515fa848df91e8972262aa
PUBLIC_SPEC: Language SPEC v0.6.0
PUBLIC_SPEC_CURRENT_SHA256: 6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0
PRODUCT_SOURCE_HEAD: c50d348226f3d4093a1e1f9bb7f9b33bb341f167
PRODUCT_SOURCE_TREE: 8c63e0513a829c783afc392b362ebca88b717baa
EVIDENCE_FIXED_COMMIT: d47ed2df36d4cce484ce0a178a53351bdf8b303f
EVIDENCE_FIXED_TREE: e6e99002766e319817b12d77abd775675339d04d
EVIDENCE_FIXED_PARENT: c50d348226f3d4093a1e1f9bb7f9b33bb341f167
```

The evidence fixed commit changes exactly the existing P5 projection manifest
and updates its `source_commit` from `7ed20696...` to the P2/P3 handoff
`c50d3482...`. Product code, tests, packs, tracked WASM, UI, SSOT and public
SPEC changes are zero.

```text
MANIFEST_PATH: work/codex/20260827_ddn_v1_product_closure_long_range_r1/P5_WINDOWS_X64_PUBLIC_SOURCE_RC_W1/PUBLIC_PROJECTION_V25_35_WINDOWS_X64_PATH_CLEAN_MANIFEST.detjson
MANIFEST_BYTES: 9327
MANIFEST_SHA256: c5d14a91bd3fc78727e8b3fcdf5de0073ff2327dc5e43723e7af68928cc1e880
FIXED_DIFF: exactly 1 tracked evidence/custody path, 1 line
PRODUCT_SOURCE_DIFF: 0
TEST_DIFF: 0
PACK_DIFF: 0
TRACKED_WASM_DIFF: 0
UI_DIFF: 0
SSOT_DIFF: 0
SPEC_DIFF: 0
```

## Fixed-source WASM candidate

The official candidate-only build contract was run from a clean LF
materialization of the exact product source head with `core.autocrlf=false`,
`core.longpaths=true`, no inherited Rust flags and offline Cargo resolution.
The first current-worktree candidate was rejected by the substitution tool
because it carried the evidence commit identity rather than the declared
product source identity. The accepted candidate below was rebuilt from exact
`c50d3482...`; the rejected external output is not evidence.

```text
WASM_CANDIDATE_DIR: I:/home/urihanl/ddn/codex/build/p5-v25-35-source-c50d3482-wasm-r2/wasm/ddonirang_tool
WASM_CANDIDATE_SEMANTIC_IDENTITY: sha256:aa5deb9540b42f42508de4d9d602338f3b320f47b489eaf2c6e82f733fb60c48
WASM_BYTES: 5559604
WASM_SHA256: 017e43e8a6a3fdb5ef383629ed4e9394efcc6ba37eeda1e2662f2eafb4e66eab
WASM_REMAP_RECEIPT_BYTES: 2470
WASM_REMAP_RECEIPT_SHA256: 5ea587db0a4d226cda5a8118e02db60fdb347c0ff6ace487defba9124435314a
WASM_INTERNAL_ABSOLUTE_PATH_COUNT: 0
WASM_OFFICIAL_STORE_PATH_COUNT: 0
WASM_PRIVATE_INCLUDE_COUNT: 0
WASM_UNKNOWN_PATH_COUNT: 0
TRACKED_WASM_WRITE: 0
PUBLIC_MEMBERSHIP: false
```

The WASM artifact bytes match the preceding `7ed20696...` candidate. The
candidate receipt identity changes because the exact source commit/tree is now
`c50d3482.../8c63e051...`.

## Public projection and validation

```text
PUBLIC_PROJECTION_DIR: I:/home/urihanl/ddn/codex/out/ddn-v1-p5-v25-35-current-public-projection-c50d3482-r1
PUBLIC_RECEIPT_DIR: I:/home/urihanl/ddn/codex/out/ddn-v1-p5-v25-35-current-public-receipts-c50d3482-r1
PROJECTED_FILE_COUNT: 898
SECURITY_SCANNED_FILES: 898
UNSCANNED_SECURITY_RELEVANT_FILES: 0
BEFORE_PUBLIC_TREE: sha256:b4c09c9ee3e58b005786f45645eb8d94e1810502cf7514111737823db1194ada
AFTER_PUBLIC_TREE: sha256:929a982c11bdb6be16a1eead65ab81a5a46db7720d15026fca25ee15bbe7fc99
PUBLIC_PROJECTION_RECEIPT: 1448 bytes / f7443ff67e26bd9694e1211ba667c8ec4009f1d68b2e3af3f28bf7e3f1592d45
PUBLIC_TREE_MANIFEST: 235548 bytes / b90359af90f6dd8b2768a70900c25074e51f80937ed1a68ab11eb6632e6fa9aa
WASM_SUBSTITUTION_RECEIPT: 818 bytes / e6291ca3da1d01582ebd597c71bf768187f93f198189def689b03da0503a4c38
VALIDATION_RECEIPT: 654 bytes / f14747d41b8007411411ea248495ecf3346c7dfe0a10c9e53e8f9509e5518b40
VALIDATION_STATUS: PUBLIC_PROJECTION_VALIDATION_PASS
REQUIRED_ROLES: PUBLIC_CONFORMANCE_RUNNER / TRACKED_WASM_FAMILY / WASM_CANDIDATE_TOOL / WINDOWS_X64_CANDIDATE_BUILD_ENTRYPOINT
TRACKED_SOURCE_WRITE_COUNT: 0
```

The new and preceding public projections each contain 898 files. Their only
byte difference is
`solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`, whose
candidate receipt and source commit/tree identities now name the exact P2/P3
product head. The P2 store/server and P3 Workbench sources are outside the
current bounded public projection contract. Their inclusion in a future
Workbench/package artifact remains a release-package scope gate; this slice
does not silently broaden the public projection.

The optional historical-SPEC-link mode was not made part of the P5 contract:
it rejects intentionally preserved non-current candidate manifests. The
current public SPEC pointer remains v0.6.0 and is unchanged.

## Windows x64 A/B evidence

Both builds used the same projected public source, offline Cargo resolution,
the existing reproducible linker/path-remap configuration and separate output
roots.

```text
WINDOWS_A_ROOT: I:/home/urihanl/ddn/codex/out/ddn-v1-p5-v25-35-windows-x64-current-a-c50d3482
WINDOWS_B_ROOT: I:/home/urihanl/ddn/codex/out/ddn-v1-p5-v25-35-windows-x64-current-b-c50d3482
WINDOWS_X64_PUBLIC_CANDIDATE_BUILD: A PASS / B PASS
WINDOWS_EXECUTABLE_STARTUP: A 2/2 PASS / B 2/2 PASS
WINDOWS_PATH_SCAN: A 0 / B 0
WINDOWS_PE_STACK_RESERVE: A 2/2 PASS / B 2/2 PASS (16777216 bytes)
WINDOWS_BINARY_DETERMINISM: 2/2 PASS
ddonirang-tool.exe: 8540160 bytes / 9563758c30f14b0dc88d18e0a94f34c5aa3b79faad8b718b514a966acd4c61fd / A==B
teul-cli.exe: 21864960 bytes / 67f23422fb2d8873c8665147ea2d9dfea98b874689e7c07d610c64f922a1a208 / A==B
PUBLIC_PROJECTION_VALIDATOR_REMAP_TESTS: 61/61 PASS
GIT_DIFF_CHECK: PASS
```

## Product value, review and remaining gates

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED:
  The fixed P2/P3 product lineage now has an exact, deterministic and path-clean
  Windows x64 CLI candidate identity derived from its bounded public source.
NEW_TEST_ARTIFACT_COUNT: 0
EXISTING_TEST_REUSED_COUNT: 61 plus two full candidate builds and four startups
META_TEST_CREATED: 0
STOP_RULE_APPLIED: YES
NEXT_PRODUCT_DECISION_ENABLED:
  management can bind this current-source P5 candidate into the next coherent
  rolling review and decide the exact Workbench/package, SBOM/NOTICE and release
  artifact boundary before P6 sealing.
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
REVIEW_BUNDLE_TARGET: existing management-owned rolling V1 reviewer; management dispatch only
REVIEW_NEEDED_NOW: YES — current-source projection and executable identities are release-critical
```

Archive/package/installer format, Workbench inclusion, SBOM/NOTICE,
rights/license, signing, external distribution and public release remain
Owner/legal/release gates. P6 remains preparation-only and unsealed until the
required P5 independent disposition and release-artifact identities are fixed.
This handoff does not claim whole P5 closure, RC promotion, V1
membership/readiness, release, activation, Owner Human Smoke PASS, Human PASS
or external-user success.
