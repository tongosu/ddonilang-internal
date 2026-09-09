# P5 current CLI fixed-head build/publish dependency handoff

## Authority and fixed lineage

```text
AI_PROVIDER: OpenAI
AI_SURFACE: Codex Work
AI_CAPABILITY: product single-writer implementation and fixed-artifact verification
SESSION_NICKNAME: DDN V1제품마감Codex
PROJECT_ROLE: DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1 single product writer
RETURN_LABEL: [DDN V1제품마감Codex -> Codex관리Work]
DEEP_RESEARCH_CHECK: NOT_USE — fixed Git objects and local build evidence decide this slice.

INTERNAL_CURRENT: v25.42.0 / RD-001~534 / Owner final 2026-08-30
PUBLIC_SPEC: v0.6.0
CURRENT_IMPACT: ADDITIVE_CUSTODY_ONLY / new semantic RD 0
LAST_REVIEWED_BASE: 65dcb1872d7b6b9099d85138c36bf2381c52bbed
PRODUCT_TEST_FIXED: 64abb938b7eccf38ce71213ec03dfec2dd15fd5e
PRODUCT_TEST_TREE: bfb1482af0055abe6a1e9a8d057ba852664fe866
PRODUCT_HANDOFF: 67980c0b68bcf30689d52c4bb4c47dafbfd6ed34
COHERENT_REVIEW_REQUEST: 3db8503f32c28569dcb0a7e811358a5d618e390c
```

The build and projection were reproduced from the exact product/test fixed
commit. Later commits in the product branch are document-only custody. No
tracked product, test, pack, WASM, UI, SSOT or SPEC file was changed by this
verification.

## Product and release value

This verification decides whether the current fixed V1 candidate can be
projected and compiled for Windows x64 without `tools/teul-cli` source or
package membership. It reuses the existing projection, validator, WASM remap
and Windows builder; it creates no pack, runner, checker or meta-test.

The public-source candidate contains six workspace members:
`ddonirang-core`, `ddonirang-lang`, `ddonirang-numeric`, `ddonirang-proof`,
`ddonirang-symbolic` and `ddonirang-tool`. It contains zero teul source files
and no teul workspace/package member.

```text
BUILD_REQUIRED_TEUL_DEPENDENCY: 0 at fixed source 64abb938...
PUBLISH_REQUIRED_TEUL_DEPENDENCY: 0 for the generated 170-file projection
TEUL_CLI_PUBLIC_BINARY_IN_CANDIDATE: 0
TEUL_CLI_PUBLIC_PACKAGE_IN_CANDIDATE: 0
P5_PUBLIC_PROJECTION_LINK_CLOSURE: OPEN
```

This does not establish repository-wide test/pack dependency zero or authorize
physical teul retirement.

## Exact candidate identities

External build custody roots:

```text
PROJECTION_ROOT:
  I:/home/urihanl/ddn/codex/build/candidates/
  v1-current-head-64abb-projection-20260830-2334
WASM_ROOT:
  I:/home/urihanl/ddn/codex/build/candidates/
  v1-current-head-64abb-wasm-20260830-2337
```

| Artifact | Bytes | SHA-256 / semantic identity |
|---|---:|---|
| current-head projection manifest | 14,012 | `f42fb1dda40c4c011056a7da339cea4cc9c5986e0f064c895da548d3ba9c3e50` |
| public projection receipt | 1,450 | `65f4794722e307dcab82dcc3f01f6330100bcb275f0492b73d2824e977182063` |
| public tree manifest | 34,124 | `a3d6fa3766085d915e3c58cfbba1a3c0dea60a0b19d0abeb58ce1f1556b74921` |
| public validation receipt | 684 | `0bc9fe6abaa0b1f25c9d4bb53f91eff420907c2c87c22183d9e7ab7146055aac` |
| WASM substitution receipt | 818 | `5f4c850d2feb19edd4152d6031eefdb80f692a560829efd9cd808291ecee8d7b` |
| candidate WASM | 5,562,704 | `b0c75e3e112777c0ca1dc66d428607e6596924c630675f42ef393b00d38e5385` |
| candidate WASM JS | 92,069 | `948db0355f34fdd422a5f18f0ebad6de4368bfa1e62c823cc8cf7438efdc8f71` |
| WASM remap receipt | 2,470 | `d018cd68a1077b9b4c7424e81ae41d0ee79288dfa4295ceb5b70c32c43a3d3b5` |
| Windows x64 `ddonirang.exe` candidate | 6,917,632 | `763f1546b2a429bffd5d10ecfebd2c1c5c549e77567fbf562207a47a3215603b` |

```text
WASM_CANDIDATE_SEMANTIC_IDENTITY:
  sha256:ca9cb71ef9c61769f916beb3ec5a504039b9838132c7cdb7824b19a4f75a5567
FINAL_PUBLIC_TREE_IDENTITY:
  sha256:7200b36c0cab0b0810187b03c0a25fe14d60f6cb49d47fa2d8778d115bd4b6ad
VALIDATION_RECEIPT_IDENTITY:
  sha256:0bc9fe6abaa0b1f25c9d4bb53f91eff420907c2c87c22183d9e7ab7146055aac
PROJECTED_FILE_COUNT: 170
SECURITY_SCANNED_FILE_COUNT: 170
UNSCANNED_SECURITY_RELEVANT_FILE_COUNT: 0
WINDOWS_STACK_RESERVE: 16777216
WINDOWS_FORBIDDEN_PATH_OCCURRENCES: 0
WINDOWS_STARTUP_HELP: PASS
```

## Fail-closed sequence and tests

1. Building directly from the product checkout failed with
   `E_WINDOWS_CANDIDATE_PUBLIC_CONFIG_MISMATCH`, correctly rejecting its
   private Cargo configuration.
2. The initial projection containing the tracked WASM failed security
   validation with `E_PUBLIC_INTERNAL_ABSOLUTE_PATH`.
3. The isolated fixed-head WASM build compiled, but the first seal invocation
   failed with `E_WASM_CANDIDATE_OFFLINE_REQUIRED` because the required
   environment variable was omitted. Reinvoking the same existing seal with
   `CARGO_NET_OFFLINE=true` passed; this is invocation custody, not a product
   defect.
4. Substituting the candidate WASM produced the fixed public tree above with
   `public_membership=false` and `tracked_source_write_count=0`.
5. Build-role and security validation passed for all 170 files.
6. The existing Windows x64 public-candidate builder passed offline and
   produced the single executable artifact above.

Existing tests were reused:

```text
python -m unittest tests.test_project_public_source \
  tests.test_validate_public_projection tests.test_wasm_candidate_remap
RESULT: 56/56 PASS
NEW_TEST_ARTIFACT_COUNT: 0
META_TEST_CREATED: 0
```

## Blocking public-link finding

Validation with `--require-spec-links` failed closed with
`E_PUBLIC_SPEC_CURRENT_LINK`. `publish/spec/CURRENT.md` references ten frozen
historical manifest paths that the current projection manifest does not
include:

- `v0.4.0-candidate/SPEC_MANIFEST_v0.4.0.md`
- `v0.4.0/SPEC_MANIFEST_v0.4.0.md`
- `v0.5.0-candidate-r3/SPEC_MANIFEST_v0.5.0.md`
- `v0.5.0/SPEC_MANIFEST_v0.5.0.md`
- `v0.6.0-source-surface-epoch-candidate/SPEC_MANIFEST_v0.6.0.md`
- `v0.6.0-source-surface-math-hott-product-sum-typed-selection-integration-candidate-r2/SPEC_MANIFEST_v0.6.0.md`
- `v0.6.0-source-surface-math-hott-product-sum-typed-selection-integration-correction-candidate-r3/SPEC_MANIFEST_v0.6.0.md`
- `v0.6.0-v25.15.0-full-reprojection-candidate-r4/SPEC_MANIFEST_v0.6.0.md`
- `v0.6.0-v25.15.0-full-reprojection-correction-candidate-r5/SPEC_MANIFEST_v0.6.0.md`
- `v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/SPEC_MANIFEST_v0.6.0.md`

Recommended resolution is to add the exact referenced frozen directories to
the public projection manifest as link-target custody without changing any
SPEC byte or public meaning. This requires an exact projection-manifest
FILE_OWNER and management/Owner approval because it changes public projection
membership. Relaxing link validation is not recommended. Editing
`publish/spec/**` is forbidden.

## CLI boundary carried forward

Candidate reachability remains 11/15. Owner fixed the executable-neutral
`project-run` semantic identity to `ddn.project-run.v1`, but two concrete
contracts remain unconfirmed: conflict behavior for `--virtual` combined with
positional/`--project`, and direct overwrite versus atomic replacement for
`--out`. No `project-run` product mutation was made. `view`, `test` and `repl`
also remain outside approved migration scope.

## Review custody and anti-meta

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED:
  current fixed source now has a path-clean Windows x64 public-source candidate
  and direct proof that build/publish candidate membership does not require teul
NEW_TEST_ARTIFACT_COUNT: 0
EXISTING_TEST_REUSED_COUNT: 3 modules / 56 cases
META_TEST_CREATED: 0
STOP_RULE_APPLIED: YES
NEXT_PRODUCT_DECISION_ENABLED:
  approve exact frozen SPEC link-target custody in the projection manifest
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
REVIEW_BUNDLE_TARGET:
  existing rolling reviewer after management rebind; this handoff supersedes
  3db8503f as the exact review parent if artifact evidence is included
```

The designated rolling reviewer thread remains
`01a04b17-66bb-7fa3-b827-53ad450005b4`; its former `3a1f` review worktree is
absent. The writer created no replacement task, reviewer, worktree, branch or
review artifact.

## Nonclaims

This handoff does not claim P5 or whole CLI closure, public projection link
closure, Windows packaging/signing/rights/license clearance, repository-wide
test/pack teul dependency zero, teul physical retirement, public executable or
package naming, V1 membership/readiness, release, activation, Owner Human Smoke
PASS, Human PASS or external-user success.
