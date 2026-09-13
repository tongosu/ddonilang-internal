# P5 current-source Windows A/B reproducibility W17 handoff

## Scope and authority

This release-custody checkpoint reuses the W16 path-clean public projection and
the existing Windows candidate build script. It adds no product, test, pack,
runner, public schema, command membership, SSOT or public SPEC change.

```text
AI_PROVIDER: OpenAI
AI_SURFACE: Codex Work
SESSION_NICKNAME: DDN V1제품마감Codex
ORIGIN_TASK_ID: DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1
INTERNAL_CURRENT: v25.47.0 / RD-001~543
SSOT_INDEX_SHA256: 2f827e7f55d23def55be590b57482e376b1d9c43cd7db2c9f72271e59c556838
SSOT_AGGREGATE_SHA256: d4d9bb661f1424ae5d16a6b70dc86a6bef22d13766820f6001c8f2b28f83b5e4
SSOT_MANIFEST_SHA256: d8a9fed64085efffefd9eac4573d7ab18975b59bebdea2009e3215a7b9268493
SSOT_SEAL_SHA256: f1869520079909eed85f2737c27a0aada3b5d013ac6c5bb41a0c781a3e501f4d
PUBLIC_LANGUAGE_SPEC: v0.6.0
PUBLIC_SPEC_CURRENT_SHA256: 6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0
PRODUCT_TEST_FIXED: 9e99ebaea41ede347eb432723acee3aabf804d86
PRODUCT_TEST_TREE: 889a082b69e2798ebee4edb9d8a2c5dbbc58a287
W16_HANDOFF: dd859d3c433f363fa92f4927ea2a69e8ac23bc8d
W16_HANDOFF_TREE: af10c8bf3a2e2b76a2ebb65ef9f614934e13578d
SUCCESSOR_IMPACT: UNAFFECTED_WITH_ADDITIVE_OUT_OF_SCOPE_SUCCESSOR
```

## Reused fixed inputs

- Source custody: `edd4a158d1ff95bd1f68bf972709bacf40f334cc`.
- Path-clean projection:
  `I:/home/urihanl/ddn/codex/build/candidates/v1-current-cli-edd4-projection-r1`.
- Build script: `scripts/build_windows_x64_public_candidate.ps1`.
- Existing project-run fixture:
  `pack/ddn_local_project_graph_v1/fixtures/project_run_physics_v1.json`.
- Semantic frontdoor identity: `ddn.project-run.v1`.

An attempted build from the raw exact-source clone failed before compilation
with `E_WINDOWS_CANDIDATE_PUBLIC_CONFIG_MISMATCH`, because its repository-local
`.cargo/config.toml` is not the portable public projection config. This is the
expected fail-closed boundary. No target or product file was changed, and the
failed output root was not created.

## A/B artifact result

The second build ran from the exact same path-clean projection into a separate
output root:

```text
WINDOWS_A: I:/home/urihanl/ddn/codex/build/candidates/v1-current-cli-edd4-windows-r1
WINDOWS_B: I:/home/urihanl/ddn/codex/build/candidates/v1-current-cli-edd4-windows-r2
ARTIFACT: ddonirang.exe
ARTIFACT_COUNT_A: 1
ARTIFACT_COUNT_B: 1
BYTES_A: 7043584
BYTES_B: 7043584
SHA256_A: 8129df4e1fc0419b658bd74278751a286d5127b1a37db630f014f3d9f609ff71
SHA256_B: 8129df4e1fc0419b658bd74278751a286d5127b1a37db630f014f3d9f609ff71
A_EQUALS_B: true
PE_STACK_RESERVE_BYTES: 16777216
FORBIDDEN_PATH_OCCURRENCES_A: 0
FORBIDDEN_PATH_OCCURRENCES_B: 0
TEUL_NAMED_ARTIFACT_COUNT_A: 0
TEUL_NAMED_ARTIFACT_COUNT_B: 0
```

The build used offline Cargo resolution, the existing portable Cargo config,
the existing three remap roots, `/Brepro`, and a distinct target directory.

## Product-facing workflow reproduction

The first comparison intentionally omitted inspection flags and produced a
different artifact. The only semantic differences were the explicitly
requested `graph_inspected`/`lock_inspected` fields and the resulting artifact
byte counter. This confirmed that invocation options must match and was not
treated as nondeterminism.

With the exact W16 invocation contract (`--inspect-graph --inspect-lock`), the
second executable produced byte-identical output:

```text
PROJECT_RUN_EXIT_A: 0
PROJECT_RUN_EXIT_B: 0
PROJECT_RUN_BYTES_A: 16488
PROJECT_RUN_BYTES_B: 16488
PROJECT_RUN_SHA256_A: f9c2e36f4117d4a523438c5ab3a88948c769fc4a4b48c99e9dd6495bd7f29578
PROJECT_RUN_SHA256_B: f9c2e36f4117d4a523438c5ab3a88948c769fc4a4b48c99e9dd6495bd7f29578
PROJECT_RUN_A_EQUALS_B: true
OPTION_CONFLICT_EXIT: 2
OPTION_CONFLICT_DIAGNOSTIC: E_CLI_OPTION_CONFLICT
PARTIAL_SUCCESS_ARTIFACT_ON_CONFLICT: 0
```

## Anti-meta and gate impact

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED:
  The exact current-source Windows candidate is now reproducible across two
  isolated builds while preserving byte-exact ddn.project-run.v1 output.
NEW_PACK: 0
NEW_RUNNER: 0
NEW_TEST_ARTIFACT_COUNT: 0
META_TEST_CREATED: 0
EXISTING_TEST_REUSED_COUNT: 1 product fixture plus existing build/path guard
CHANGED_V1_GATE: P5_CURRENT_SOURCE_WINDOWS_AB_REPRODUCIBILITY_EVIDENCE_READY
ACTIVE_REVIEW_TASK_COUNT: 1 existing rolling reviewer custody
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
```

The authoritative earlier P5 review remains target-bound to fixed
`3e205ce816e47d29f6488bd86d029750e6afaaf5`, handoff
`ccaa7132e9192a26f003917ae4f2795482c4e74f`, and review
`bc84d81d4faa55974975bdb7ec60cb18d9a7ebda` (report SHA-256
`05d9522c900d5c164064a003f92fabc100f64daf40100690b0e3c3747892a6d6`).
It proves that the reviewer handle and bounded P5 review gate exist; it does not
automatically review W15/W16/W17 successors.

## Remaining gates and nonclaims

- W13-W17 current-source successor bundle still needs target-bound review by
  the existing rolling reviewer; no new reviewer is created here.
- Strict historical/candidate SPEC-link ownership remains a slice-only release
  documentation gate.
- Rights, license/NOTICE, signing, distribution and Owner release approval are
  external gates.
- Public `test/view/repl` membership, PathIR public physical contract and VC17
  exact landing remain frozen only in their own slices.
- Physical `tools/teul-cli` deletion still requires exact Owner approval and
  backup/hash/restore custody.

This handoff does not claim whole P5, P6, V1 readiness, release, activation,
legal status, Owner Human Smoke or Human PASS.
