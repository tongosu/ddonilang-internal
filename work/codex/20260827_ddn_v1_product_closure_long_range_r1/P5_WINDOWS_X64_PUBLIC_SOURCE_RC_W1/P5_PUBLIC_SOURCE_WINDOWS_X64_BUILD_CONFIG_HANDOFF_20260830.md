# P5 public-source Windows x64 build-config handoff

## Authority and fixed lineage

```text
AI_PROVIDER: OpenAI
AI_SURFACE: Codex Work
AI_CAPABILITY: product single-writer implementation and fixed-artifact verification
SESSION_NICKNAME: DDN V1제품마감Codex
PROJECT_ROLE: DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1 single product writer
RETURN_LABEL: [DDN V1제품마감Codex -> Codex관리Work]
DEEP_RESEARCH_CHECK: NOT_USE — live repository authority and local fixed-object build evidence decide this slice.

INTERNAL_CURRENT: v25.35.0 / RD-001~490 / Owner final 2026-08-30
INTERNAL_CURRENT_POINTER_SHA256: d8224b35d8e10b134ad2c3cd6e94db7d9b32d21363515fa848df91e8972262aa
INTERNAL_SSOT_CURRENT_SHA256: a9bd37606dab7c25be5af527db93c4eb8c9e0cd6f1b54988b4211e67190c8ad4
INTERNAL_INDEX_SHA256: 911f87fb4516b5c8db342f5180b3e6facbc76292fc44f3ec15c39f148eab7cd6
PUBLIC_SPEC: v0.6.0
PUBLIC_SPEC_CURRENT_SHA256: 6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0

BASELINE: 3553735988dcb2476fda7d9c769552b56c8bb1c8
PRODUCT_FIXED: b1fd4c174634a2a851e6c1a3e1fe72ab97f6db62
PRODUCT_FIXED_TREE: fd241b522f57ccc1bedb86c4d027cf0b0a7db56c
```

The product fixed commit is the baseline's direct successor and changes exactly
`tools/public_cargo_config.toml`. It adds the portable Windows-only Cargo link
setting `/STACK:16777216` without copying the repository-local absolute
`target-dir` configuration into a public-source projection.

## User workflow and release blocker

Before this change, the fixed public projection manifest had no rule capable of
materializing `.cargo/config.toml`:

```text
PUBLIC_CARGO_CONFIG_RULE_COUNT: 0
RED: E_PUBLIC_WINDOWS_CARGO_CONFIG_MISSING
EXIT: 1
```

The added source config is 144 bytes with SHA-256
`454a4ba886da1e98d2d44bf85d91babd1a6a3d3178ae381195b759750404ede5`.
The projected `.cargo/config.toml` is byte-identical and has the same digest.
Both projected Windows release executables carry the required PE stack reserve:

| executable | bytes | SHA-256 | PE stack reserve |
|---|---:|---|---:|
| `ddonirang-tool.exe` | 8,540,160 | `bff12e509182a29ae20f0166da30d63e03ded7515fe819e1f1ef69d09df291bd` | 16,777,216 bytes |
| `teul-cli.exe` | 21,890,560 | `41b9139e972274e3d2e699a555fc31201362d07474a5a463db1979f86bb54b4d` | 16,777,216 bytes |

`ddonirang-tool.exe --help` and `teul-cli.exe --help` both exit 0 from the
projected source build. This closes only the portable Windows build-config gap;
it does not make these local binaries release artifacts.

## Public projection and WASM candidate identities

```text
PROJECTION_MANIFEST_BYTES: 9061
PROJECTION_MANIFEST_SHA256: 2ebd95e449144df18abdef0acd0f528000bb7fcc8e17951c8cd4cdfba1d6834e
SOURCE_COMMIT: b1fd4c174634a2a851e6c1a3e1fe72ab97f6db62
SOURCE_TREE: fd241b522f57ccc1bedb86c4d027cf0b0a7db56c
PROJECTED_FILE_COUNT: 897
SECURITY_SCANNED_FILES: 897
UNSCANNED_SECURITY_RELEVANT_FILES: 0
BEFORE_PUBLIC_TREE: sha256:df7153d2a0f8417d37cff98aeed66c9e0eaf285fa05faaefa06bb4da18e58995
AFTER_PUBLIC_TREE: sha256:b3777d6a62f3190e87f7bd6feb0128dbbf9960a59b2f2dcab9744ed88935876b
VALIDATION_RECEIPT_BYTES: 613
VALIDATION_RECEIPT_SHA256: 8dab3c45cda2fd6c6a39a70a38adea5ab571373152b4d5d37c4478bdeb279415
VALIDATION_STATUS: PUBLIC_PROJECTION_VALIDATION_PASS
PUBLIC_MEMBERSHIP: false
TRACKED_SOURCE_WRITE_COUNT: 0

WASM_CANDIDATE_SEMANTIC_IDENTITY: sha256:1d6450b278eb8e92c56c79a4966bcb03b42332c53b4eea0b368c794c95aa3dbc
WASM_BYTES: 5559604
WASM_SHA256: cf4062081dec66e74057b5029b90e198de5390610e7c0c71763a95edfee6c232
TRACKED_WASM_WRITE: 0
```

The official candidate-only WASM build entrypoint and existing projection,
candidate-substitution and validator tools were reused. The validator required
`PUBLIC_CONFORMANCE_RUNNER`, `TRACKED_WASM_FAMILY` and `WASM_CANDIDATE_TOOL`;
all were present.

## Existing verification reused

```text
OFFLINE_PUBLIC_WORKSPACE_RELEASE_BUILD: PASS
OFFLINE_PUBLIC_TEUL_CLI_RELEASE_BUILD: PASS
WINDOWS_EXECUTABLE_STARTUP: 2/2 PASS
PUBLIC_PROJECTION/VALIDATOR/WASM_REMAP UNIT TESTS: 61/61 PASS
PROJECTED_CONFIG_BYTE_EQUAL: PASS
GIT_DIFF_CHECK: PASS
TCP_8787_LISTENER_COUNT: 0
PROTECTED_PROCESS_LIFECYCLE_COMMAND_COUNT: 0
```

No new runner, pack, checker, framework or meta-test was created. The actual
missing-config RED and the resulting PE header are the risk-relevant product
evidence; no receipt/hash tamper suite was added.

## Remaining blocker and stop boundary

The locally built native executables are not path-clean release artifacts. A
bounded ASCII scan found build-host path prefixes in both binaries:

```text
ddonirang-tool.exe: I:\home\urihanl=2, C:\Users\ddongosu=146
teul-cli.exe:       I:\home\urihanl=41, C:\Users\ddongosu=661
```

These binaries are external build output and were not added to the projected
source tree or Git. P5 still requires an exact path-clean native artifact build,
Windows packaging identity, rights/license/distribution gates and independent
review before RC or release closure. No unapproved compiler remap or packaging
meaning is introduced in this slice.

## Anti-meta and review custody

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED:
  A public-source Windows checkout now receives the required portable stack
  reserve config and can build/start both native product executables.
NEW_TEST_ARTIFACT_COUNT: 0
EXISTING_TEST_REUSED_COUNT: 61 cases plus two existing product startups
META_TEST_CREATED: 0
STOP_RULE_APPLIED: YES
NEXT_PRODUCT_DECISION_ENABLED:
  choose or authorize the exact path-remapped Windows artifact/package contract.
ACTIVE_REVIEW_TASK_COUNT: 0 observed by this writer
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
REVIEW_BUNDLE_TARGET:
  next coherent P5 Windows x64 candidate milestone on the existing rolling reviewer,
  dispatched by management only.
```

## Nonclaims

This handoff does not claim P1, P2, P3, P4 or P5 closure; exact V1 membership or
readiness; path-clean Windows package completion; rights/license clearance;
public release or activation; Owner Human Smoke PASS; or external-user success.
It does not modify SSOT, public SPEC, tracked WASM, visible UI or public support
membership.
