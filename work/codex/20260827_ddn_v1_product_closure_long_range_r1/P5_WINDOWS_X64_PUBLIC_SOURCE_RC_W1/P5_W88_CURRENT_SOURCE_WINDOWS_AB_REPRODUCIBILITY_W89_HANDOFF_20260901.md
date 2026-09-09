# P5 W88 current-source Windows A/B reproducibility W89 handoff

STATUS: `P5_W88_WINDOWS_X64_FIXED_ARTIFACT_CUSTODY_IMPLEMENTED_PENDING_REVIEW`

## Authority and predecessor

- Internal live CURRENT: `v25.49.0 / RD-001~543`, Owner final 2026-09-01.
- CURRENT/index/aggregate/manifest/seal were read-only reverified.
- Public Language SPEC: `v0.6.0`.
- Successor impact: `UNAFFECTED_WITH_ADDITIVE_CUSTODY`; new semantic RD 0.
- W88 compile fix: `84ef438110738228b724f8052cd0711a7d036a89`.
- W88 product/artifact fixed: `0e57a5b9a1f3e3c16ad427687530587b164f2e21`.
- W88 fixed tree: `9fc7e64563c9b921deaf71a9a72b383e90683461`.
- W88 handoff / this custody parent: `053bd1d52b7b9f0b1fb03f06a14d65b6b6d105b9`.
- Review commit `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf` is an ancestor and remains `PASS_TARGET_BOUND` only for the shared CLI test workflow.
- Merge count in the W88 bounded lineage: 0.

No product, test, pack, runner, framework, WASM, UI, SSOT or public SPEC file
was changed for this A/B custody companion. It reuses the W88 fixed public
projection and the existing Windows candidate builder.

## Fixed public projection

```text
SOURCE_COMMIT: 0e57a5b9a1f3e3c16ad427687530587b164f2e21
SOURCE_TREE: git-tree:9fc7e64563c9b921deaf71a9a72b383e90683461
PROJECTED_FILE_COUNT: 219
PUBLIC_TREE_IDENTITY: sha256:ce5121d320ab32b57704da83309c80bd11f1f94609ffc5d50190e23ee2eff621
PROJECTION_RECEIPT_SHA256: 8f91864df7de3d790e7ffee66ae8c1c7beb162f33156edb4c828daeaf2768668
VALIDATION_RECEIPT_SHA256: fff45050a5e3497632f1aab337f7a92cf1a4909f672b39308657f2e76cbf18a3
TRACKED_WASM_BYTES: 5572371
TRACKED_WASM_SHA256: 50e7a22e735da6eba4b5966b0b6e05e113a9f15a31204c2a63c61f75fbb7e484
TRACKED_WASM_EMBEDDED_HOST_PATH_COUNT: 0
PROJECTED_TEUL_SOURCE_OR_ARTIFACT_COUNT: 0
```

## Windows x64 A/B artifact

The same fixed projection was built offline into two distinct output roots by
`scripts/build_windows_x64_public_candidate.ps1`. Both builds used the
portable public Cargo config, source/Cargo/rustup remap roots, `/Brepro`, and a
16 MiB PE stack reserve.

```text
ARTIFACT: ddonirang.exe
ARTIFACT_COUNT_A: 1
ARTIFACT_COUNT_B: 1
BYTES_A: 7043072
BYTES_B: 7043072
SHA256_A: 7a638db296da098e65cf573484ef9d6d66af2ca564de3bace23240a4399950c5
SHA256_B: 7a638db296da098e65cf573484ef9d6d66af2ca564de3bace23240a4399950c5
A_EQUALS_B: true
PE_STACK_RESERVE_BYTES_A_B: 16777216
FORBIDDEN_PATH_OCCURRENCES_A_B: 0
TEUL_NAMED_ARTIFACT_COUNT_A_B: 0
HELP_EXIT_A_B: 0
HELP_SHA256_A_B: 61c2d38a297baa98122674335402577f728cb1b41b001c9e9f9728443b2abda3
```

The existing Cargo PDB filename-collision and dead-code warnings were
non-fatal. No warning was converted into a closure claim.

## `ddn.project-run.v1` product workflow

Reused fixture:
`pack/ddn_local_project_graph_v1/fixtures/project_run_physics_v1.json`, SHA-256
`4df16386dbd388e044c334da0c777aa02e45052eff635de5f9769dba6f2dd5ec`.

Both binaries ran the same request with target `앱`, `--inspect-graph`,
`--inspect-lock`, and atomic `--out` publication.

```text
PROJECT_RUN_EXIT_A_B: 0
PROJECT_RUN_BYTES_A_B: 16488
PROJECT_RUN_SHA256_A_B: f9c2e36f4117d4a523438c5ab3a88948c769fc4a4b48c99e9dd6495bd7f29578
PROJECT_RUN_A_EQUALS_B: true
OPTION_CONFLICT: positional-start + --virtual
OPTION_CONFLICT_EXIT: 2
OPTION_CONFLICT_DIAGNOSTIC: E_CLI_OPTION_CONFLICT
PARTIAL_SUCCESS_ARTIFACT_ON_CONFLICT: 0
FAILED_TARGET_EXIT: 2
FAILED_TARGET_DIAGNOSTIC: E_PROJECT_TARGET_MISSING
PREEXISTING_ARTIFACT_PRESERVED: true
TEMP_OR_PARTIAL_RESIDUE: 0
```

This preserves the executable-neutral semantic identity
`ddn.project-run.v1`; it does not decide executable/package naming, public
command membership or legacy alias duration.

## C0~C8 bounded status

| Gate | Current state |
|---|---|
| C0 | Historical 91-command registry remains custody; no bulk promotion. |
| C1 | `ddn.project-run.v1` is fixed and reachable; naming/alias details remain OPEN. |
| C2 | Shared lang/tool canon, preprocess, runtime, value and artifact-output authorities remain preserved. |
| C3 | Approved candidate workflows are reachable; public `test/view/repl` membership remains slice-local OPEN. |
| C4 | Migrated required workflows have private teul fallback 0; internal/deferred physical custody remains. |
| C5 | Bounded V1-required build/test/pack/publish teul execution dependency remains 0. |
| C6 | Native/WASM structured authority is fixed; W88 tracked WASM is path-clean and deterministic. |
| C7 | W88 public projection and Windows x64 A/B fixed-artifact reproducibility are GREEN pending review. |
| C8 | Public projection/binary excludes teul; physical deletion and final retirement remain Owner-gated. |

## Anti-meta, review, and nonclaims

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED: W88 now has a reproducible Windows fixed artifact and byte-identical project-run workflow suitable for coherent target-bound review.
REUSED_TEST_COUNT: 1 product fixture plus existing projection/build/path guards
NEW_TEST_ARTIFACT_COUNT: 0
NEW_PACK: 0
NEW_RUNNER: 0
META_TEST_CREATED: 0
PARTIAL_PUBLISH_COUNT: 0
ACTIVE_REVIEW_TASK_COUNT: 0
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
REVIEW_BUNDLE_TARGET: W84-W88 product/projection milestone plus W89 fixed-artifact custody
REVIEWER_HANDLE: 01a04b17-66bb-7fa3-b827-53ad450005b4 (existing rolling reviewer; not dispatched by this writer)
```

Public `test/view/repl` membership, PathIR public contract, VC17 exact landing,
rights/license/NOTICE/signing/distribution, physical teul deletion, whole P5/P6,
V1 readiness/release/activation, Owner Human Smoke and Human PASS remain OPEN.

