# P5 Windows x64 path-clean artifact handoff

## Authority and fixed lineage

```text
AI_PROVIDER: OpenAI
AI_SURFACE: Codex Work
AI_CAPABILITY: product single-writer implementation and fixed-artifact verification
SESSION_NICKNAME: DDN V1제품마감Codex
PROJECT_ROLE: DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1 single product writer
RETURN_LABEL: [DDN V1제품마감Codex -> Codex관리Work]
DEEP_RESEARCH_CHECK: NOT_USE — live repository authority and executable fixed-object evidence decide this slice.

INTERNAL_CURRENT: v25.35.0 / RD-001~490 / Owner final 2026-08-30
INTERNAL_CURRENT_POINTER_SHA256: d8224b35d8e10b134ad2c3cd6e94db7d9b32d21363515fa848df91e8972262aa
INTERNAL_SSOT_CURRENT_SHA256: a9bd37606dab7c25be5af527db93c4eb8c9e0cd6f1b54988b4211e67190c8ad4
INTERNAL_INDEX_SHA256: 911f87fb4516b5c8db342f5180b3e6facbc76292fc44f3ec15c39f148eab7cd6
PUBLIC_SPEC: v0.6.0
PUBLIC_SPEC_CURRENT_SHA256: 6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0

BASELINE: aa2e7f087ca0485d2752e945905b9c718e32f647
PRODUCT_FIXED: b2fa6db1b422122155d5b90f5f2f4bc6ec69b0aa
PRODUCT_FIXED_TREE: 54c770af56a09a281388b6ae36c260fab77d0562
MERGE_COUNT: 0
```

The linear product commits are:

1. `b6deb6f35151f5bcf088825ddfece0dab17093f7` — shared virtual build-root consumers and the Windows candidate entrypoint.
2. `3f316a80558c99540ce89f6278aa319b9e308ce0` — exact projected Cargo config identity.
3. `a32adac259c8b9d45799356d52fbd4189aa8b8f9` — fail-closed artifact collection correction.
4. `b2fa6db1b422122155d5b90f5f2f4bc6ec69b0aa` — MSVC `/Brepro` deterministic linking.

The baseline-to-fixed product diff is exactly seven paths:

- `scripts/build_windows_x64_public_candidate.ps1`
- `tool/src/ai_prompt.rs`
- `tool/src/detmath_assets.rs`
- `tool/src/project_meta.rs`
- `tools/teul-cli/src/ai_prompt.rs`
- `tools/teul-cli/src/cli/patch.rs`
- `tools/teul-cli/src/core/bogae.rs`

SSOT, public SPEC, pack, tests, tracked WASM and visible UI diffs are zero.

## User workflow and product correction

A user or release operator can now take the fixed public-source projection on a
Windows x64 MSVC host and invoke one product entrypoint that builds, collects
and directly validates both native executables. Candidate builds use the existing
three-root remap contract, an explicit virtual repository identity `/ddn-src`,
the required 16 MiB stack reserve, path-neutral PDB metadata and reproducible
MSVC links. Ordinary developer builds keep their existing physical-root behavior.

The six compile-time repository-root consumers now read
`DDN_BUILD_REPO_ROOT` only when it is explicitly supplied by the candidate
entrypoint. There is no source heuristic, private parser/runtime, semantic
fallback, profile switch or public command/name change.

## Product RED to GREEN

The first remapped build still embedded the physical public projection root:

```text
ddonirang-tool.exe: source-root occurrence 1
teul-cli.exe: source-root occurrences 2
```

After the virtual-root consumer correction both candidate executables reported
`forbidden_path_occurrences=0`. A second independent-output RED then showed that
path-clean binaries were not byte deterministic without `/Brepro`:

| executable | A SHA-256 | B SHA-256 | result |
|---|---|---|---|
| `ddonirang-tool.exe` | `ac077ba4578d3399726c581a9d286fa15704d77aa6a216ee141b9f4e0289df59` | `bc677345a9f521b0fc048948d44b9a5ef3ef53062f8920665d6f0f8618e71000` | RED |
| `teul-cli.exe` | `cbbbe2445e6a6e6c10a6f8024d708844b3df1c02367bf9d7bd8d651ce07a8eb4` | `3726e66b96a0b9acb37676f12fe21ddf14426b491f8e52a7583ed0848958fa79` | RED |

With `/Brepro`, two clean output roots produced byte-identical results:

| executable | bytes | A/B SHA-256 | stack reserve | forbidden path occurrences | startup |
|---|---:|---|---:|---:|---|
| `ddonirang-tool.exe` | 8,537,600 | `6aa349011bc1cf304777292cdfea9fe612dfc7dc5c2a9c1291c0ec8b6a68c6bd` | 16,777,216 | 0 | PASS |
| `teul-cli.exe` | 21,873,152 | `4c6bb5165376003a7e8a29b874f0acfc8ffb1108b613ce0bdbe7dfec72cf519b` | 16,777,216 | 0 | PASS |

`BYTE_EQUAL_A_B: 2/2 PASS`. The entrypoint also rejects inherited Rust flags,
wrong host/config identity, existing output roots, missing artifacts, physical
root leaks, wrong PE stack reserve and startup failure.

## Fixed public projection and WASM identities

```text
PROJECTION_MANIFEST_BYTES: 9327
PROJECTION_MANIFEST_SHA256: d969d4d0ec409d75e39b30cec66fa201cdc631d9c3fb01eb5691c5cd400f239d
SOURCE_COMMIT: b2fa6db1b422122155d5b90f5f2f4bc6ec69b0aa
SOURCE_TREE: git-tree:54c770af56a09a281388b6ae36c260fab77d0562
PROJECTED_FILE_COUNT: 898
BEFORE_PUBLIC_TREE: sha256:3f82839a5ab0dedc3493c43e9cfd806e6aa1c72569044446a04ff1d06d585c7a
AFTER_PUBLIC_TREE: sha256:27c7a7829dfb91c0d4f104db6cf8b91b443812bfa33eaf8f99645316cae22626
PUBLIC_PROJECTION_RECEIPT: 1448 bytes / 4d033508a50df3916acd5f1f665931a1bff794f8a5a3d418625b2a54f10348e1
PUBLIC_TREE_MANIFEST: 235548 bytes / cf0c1979f5ac501b9d315cc47a358c5e05e4c08307566bfebadf2d28e1d21a2e
WASM_SUBSTITUTION_RECEIPT: 818 bytes / 86bdecfb3a59cb4534281d67f5324f43fbdb995d8f6c68dafa62ebea2719c62c
VALIDATION_RECEIPT: 654 bytes / 1c34e3db807ae833fbd49c0b9fbef73dd073d2d9ceeb9289e41e6fa02fc599f8
VALIDATION_STATUS: PUBLIC_PROJECTION_VALIDATION_PASS
PUBLIC_MEMBERSHIP: false
TRACKED_SOURCE_WRITE_COUNT: 0

WASM_CANDIDATE_SEMANTIC_IDENTITY: sha256:615b6612e8177678790919acc8570c7515494c2ec5b1594bab7bc61f705207ab
WASM_BYTES: 5559604
WASM_SHA256: cf4062081dec66e74057b5029b90e198de5390610e7c0c71763a95edfee6c232
WASM_REMAP_RECEIPT: 2470 bytes / 8baf427e5c4bbe9e87e261cf039355d43cee7794e03de991d4512a60dbd0ae39
TRACKED_WASM_WRITE: 0
```

The validator required the existing `PUBLIC_CONFORMANCE_RUNNER`,
`TRACKED_WASM_FAMILY`, `WASM_CANDIDATE_TOOL` and the new
`WINDOWS_X64_CANDIDATE_BUILD_ENTRYPOINT` role. All were present. An additional
historical-SPEC-link option was intentionally not promoted into this projection
contract because it fail-closed on preserved non-current candidate manifests.

## Reused verification and custody

```text
WINDOWS_X64_PUBLIC_CANDIDATE_BUILD: A PASS / B PASS
WINDOWS_EXECUTABLE_STARTUP: A 2/2 PASS / B 2/2 PASS
WINDOWS_PATH_SCAN: A 0 / B 0
WINDOWS_PE_STACK_RESERVE: A 2/2 PASS / B 2/2 PASS
WINDOWS_BINARY_DETERMINISM: 2/2 PASS
PUBLIC_PROJECTION/VALIDATOR/WASM_REMAP UNIT TESTS: 61/61 PASS
FOCUSED PRODUCT REGRESSION: 41/41 PASS
GIT_DIFF_CHECK: PASS
TCP_8787_LISTENER_COUNT: 0
PROTECTED_PROCESS_LIFECYCLE_COMMAND_COUNT: 0
```

The focused product regression reused existing tests for tool detmath and
project metadata plus teul AI prompt, bogae and patch paths. No new test,
runner, pack, checker, framework or meta-test was created.

## Anti-meta, review and next gate

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED:
  A fixed public-source Windows x64 checkout can now produce two path-clean,
  startup-valid and reproducible native candidate executables through one
  fail-closed product entrypoint.
NEW_TEST_ARTIFACT_COUNT: 0
EXISTING_TEST_REUSED_COUNT: 102 cases plus two A/B product builds and four startups
META_TEST_CREATED: 0
STOP_RULE_APPLIED: YES
NEXT_PRODUCT_DECISION_ENABLED:
  independent review can decide whether the fixed native candidate behavior is
  suitable to enter the P5 package/rights/release-gate lane.
ACTIVE_REVIEW_TASK_COUNT: 0 observed by this writer
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
REVIEW_BUNDLE_TARGET:
  coherent P5 path-clean Windows x64 candidate milestone on the existing
  management-owned rolling reviewer; management dispatch only.
REVIEW_NEEDED_NOW:
  YES — compiler remap, virtual compile-time root and reproducible linker flags
  directly determine release artifact custody.
```

## Remaining gates and nonclaims

Exact archive/package/installer format and signed receipt schema remain OPEN
under current authority. Rights/license/SBOM/notices, signing, external
distribution and public release remain Owner/legal/release gates. This handoff
does not claim whole P5 closure, RC promotion, V1 membership/readiness, release,
activation, Owner Human Smoke PASS, Human PASS or external-user success. The P6
packet remains preparation-only and unsealed until P5 fixed identities and an
independent disposition are bound.
