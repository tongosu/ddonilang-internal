# CLI file-metadata shared authority W25 handoff

## Authority and status

```text
INTERNAL_CURRENT: v25.47.0 / RD-001~543
PUBLIC_LANGUAGE_SPEC: v0.6.0
SUCCESSOR_IMPACT: UNAFFECTED_WITH_ADDITIVE_OUT_OF_SCOPE_SUCCESSOR
GOAL_STATUS: ACTIVE
MILESTONE_STATUS: IMPLEMENTED_UNDER_REVIEW
SSOT_CHANGE: 0
PUBLIC_SPEC_CHANGE: 0
```

All CURRENT/index/aggregate/manifest/seal and public SPEC hashes remain exactly
the identities recorded in the W23+W24 handoff. No authority file was modified.

## Exact lineage and file owner

```text
BASELINE: d2fc52998cf52c5a0a0edfab2060d3962edfbb57
PRODUCT_FIXED: 3c09c7e41d2d6c9b5c4cf101e272c01f7d1f75e5
PRODUCT_TREE: 539ba87280f7e3269baab30c74ebc125abd8a9c2
DIRECT_PARENT: d2fc52998cf52c5a0a0edfab2060d3962edfbb57
DIRECT_LINEAGE: YES
MERGE_COUNT: 0
```

Exact changed product paths:

- `tool/src/main.rs`
- `tool/src/preprocess.rs`
- `tools/teul-cli/src/cli/frontdoor_input.rs`
- `tools/teul-cli/src/file_meta.rs`

## Product problem and change

The same source-header metadata operation had three implementation owners:

1. `tool/src/file_meta.rs`
2. `tool/src/preprocess.rs`
3. `tools/teul-cli/src/file_meta.rs`

That allowed runtime preprocessing, canonicalization, and the retained teul
frontdoor to drift in duplicate-key, CRLF, header stripping, and JSON projection
behavior.

W25 keeps only `tool/src/file_meta.rs` as the product owner:

- `tool::preprocess` re-exports the shared metadata types and operations;
- the tool binary consumes the library preprocess module rather than compiling
  a local module copy;
- retained teul `file_meta` is a three-line shared-tool adapter;
- the existing frontdoor test now also proves header removal and body retention
  through the actual canon preparation path.

```text
BASELINE_SPLIT_FILE_META_IMPLEMENTATIONS: 3
FIXED_SPLIT_FILE_META_IMPLEMENTATIONS: 1
BASELINE_FORMAT_FILE_META_IMPLEMENTATIONS: 3
FIXED_FORMAT_FILE_META_IMPLEMENTATIONS: 1
TEUL_PRIVATE_FILE_META_DEFINITIONS: 0
TOOL_PREPROCESS_PRIVATE_FILE_META_DEFINITIONS: 0
SHARED_FILE_META_OWNER_COUNT: 1
```

No public source spelling, wire schema, command membership, executable/package
name, or legacy duration was changed.

## RED, tests, and clean materialization

Baseline and fixed focused results are identical:

```text
legacy_header_is_detected_via_lang_single_source: PASS -> PASS
legacy_root_prefix_is_rejected_via_frontdoor_guard: PASS -> PASS
canon_rejects_legacy_hash_header_for_all_emit_kinds: PASS -> PASS
supported_profile_canon_uses_shared_authority_and_atomic_output: PASS -> PASS
boim_is_accepted_via_frontdoor_guard: FAIL -> same FAIL
NEW_REGRESSION_COUNT: 0
```

The existing `보임` failure is pre-existing contract drift and was neither
hidden nor counted as W25 closure evidence.

Both binaries built successfully from a new isolated external Cargo target:

```text
TOOL_BUILD: PASS
TEUL_BUILD: PASS
CLEAN_TARGET:
  I:/home/urihanl/ddn/codex/build/targets/v1-file-meta-shared-authority-w25
```

An older reused target briefly produced duplicate path-crate identities during
linking even though `cargo tree` showed one source path. No repository source
was changed to mask that environment event; the new target materialization
proved the product graph compiles cleanly.

## Mutation

A local `split_file_meta` definition was temporarily reintroduced into the teul
adapter.

```text
MUTATION_PRIVATE_SPLIT_COUNT: 1
MUTATION_GUARD: RED
MUTATED_ADAPTER_SHA256:
  e5c5f4d7298521423d06f3d3ff012cb828aa45a98e8cd7ef9782818acb27f025
RESTORED_ADAPTER_SHA256:
  9458695615c0142d460dd14f72fbfde4f00e26d40b9afe716487579b0792495f
RESTORED_PRIVATE_SPLIT_COUNT: 0
RESTORED_SHARED_IMPORT_COUNT: 1
RESTORED_FRONTDOOR_TEST: GREEN
MUTATION_RESIDUE: 0
```

## C0~C8 bounded impact

| Gate | W25 impact |
|---|---|
| C0 | Historical registry custody unchanged. |
| C1 | `ddn.project-run.v1` and naming gates unchanged. |
| C2 | Shared preprocessing/file-metadata authority strengthened to one owner. |
| C3 | Public command membership unchanged. |
| C4 | Teul private file-metadata authority reduced to 0. |
| C5 | Bounded required teul execution dependency remains 0. |
| C6 | Native supported canon and fail-closed guards retain baseline behavior. |
| C7 | Reviewed P5 identities remain target-bound and unchanged. |
| C8 | Physical teul retirement/deletion remains Owner-gated. |

## Anti-meta, review, and nonclaims

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED:
  runtime/canon/retained teul source-header handling now consumes one product owner
REUSED_TEST_COUNT: 5
NEW_TEST_ARTIFACT_COUNT: 0
NEW_PACK: 0
NEW_RUNNER: 0
META_TEST_CREATED: 0
ACTIVE_REVIEW_TASK_COUNT: 0
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
REVIEWER_HANDLE: 01a04b17-66bb-7fa3-b827-53ad450005b4
REVIEW_BUNDLE_TARGET: W25 plus the next adjacent preprocessing authority vertical
```

SPEC history, PathIR public contract, public test/view/repl membership, and
VC17 exact landing remain slice-local OPEN. This does not claim whole CLI or
C0~C8 closure, physical teul retirement, P0~P6 closure, V1 readiness/release,
activation, legal approval, Owner Human Smoke, or Human PASS.
