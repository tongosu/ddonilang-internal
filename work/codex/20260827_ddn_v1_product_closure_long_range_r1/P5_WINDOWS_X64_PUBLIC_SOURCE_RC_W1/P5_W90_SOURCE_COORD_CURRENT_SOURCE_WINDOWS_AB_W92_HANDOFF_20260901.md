# P5 W90 source-coordinate current-source Windows A/B W92 handoff

STATUS: `P5_W90_WASM_PATH_CLEAN_AND_WINDOWS_AB_IMPLEMENTED_PENDING_REVIEW`

## Authority and lineage

- Internal live CURRENT: `v25.49.0 / RD-001~543`, Owner final 2026-09-01.
- Shared-root CURRENT/index authority was re-read only; `docs/ssot/**` change 0.
- Public Language SPEC: `v0.6.0`; public SPEC change 0.
- Successor impact: `UNAFFECTED_WITH_ADDITIVE_PRODUCT_AND_RELEASE_CUSTODY`.
- W90 source-coordinate fixed: `bfe1b67d917751c0e0107d202c5678c51f7388bd`.
- W90 handoff: `a7cd7fb89c2e6d4e4b6cd04148a9324f170f169c`.
- Initial W91 WASM refresh: `36485ba42d4782f1551c018daeabad4e58d04be8`.
- Initial W91 handoff: `52de89af566d82d4b6f5981b9c8807b1cbab369e`.
- Projection source-pin preparation: `04ec2c23`.
- Path-clean tracked-WASM fixed: `74bfa235d4f345500b85ae0bb557e339b9626acc`.
- Projection manifest binding: `8c1188727f569bb13fd816c32e3a23c197c5cd1d`.
- Merge count: 0.

The initial W91 binary is historical custody only: its embedded-host-path count
was 115. The path-clean successor at `74bfa235...` is the fixed product/artifact
identity used below. No initial artifact PASS is inherited.

The already verified review commit
`bc84d81d4faa55974975bdb7ec60cb18d9a7ebda` remains
`PASS_TARGET_BOUND` for its fixed P5 target
`3e205ce816e47d29f6488bd86d029750e6afaaf5` / handoff
`ccaa7132e9192a26f003917ae4f2795482c4e74f`, with blocking finding 0 and
report SHA-256
`05d9522c900d5c164064a003f92fabc100f64daf40100690b0e3c3747892a6d6`.
It proves reviewer availability and removes the previous handle-absence blocker;
it is not automatically inherited by this successor target.

## Path-clean tracked WASM

The first external remap build attempt failed closed because
`CARGO_NET_OFFLINE=true` was absent. Its external output remains custody only;
it changed no tracked product path. The second isolated output used the required
offline environment and the existing candidate-remap build/copy/freshness path.

```text
WASM_CANDIDATE_RECEIPT_IDENTITY: sha256:8aa19da6f25bb583f9ead279f003d30fee3666f8cf6d927a74e4ee17b6c6124c
TRACKED_WASM_BYTES: 5572809
TRACKED_WASM_SHA256: f70acaf6d17c968b2cd1db459127af00fdae755b43d2ebb5239997a34c2f173d
TRACKED_MANIFEST_SHA256: cabdc29fe7e4e347284425af0f0c12ca22092104d7748091f55d0d414122d37f
EMBEDDED_ABSOLUTE_PATH_COUNT: 0
OFFICIAL_FRESHNESS: PASS
PUBLIC_PROJECTION_AND_REMAP_TESTS: 58/58 PASS
```

## Fixed public projection

The existing projection generator and validator were reused. No new pack,
runner, checker or framework was created.

```text
SOURCE_COMMIT: 74bfa235d4f345500b85ae0bb557e339b9626acc
PROJECTED_FILE_COUNT: 220
PUBLIC_TREE_IDENTITY: sha256:e629e266bb635821bef82133eaf5c2d90a763013b963e4670d21b165c9f490c3
PROJECTION_RECEIPT_SHA256: 95507cc5686007c5e2a12b8367943ffc221e158d88d98f781acf5ef29eec7af2
PUBLIC_TREE_MANIFEST_SHA256: 62b82ad80bc60d0192fe73db4e2205ddae2db2553dfd7be7bab7948d92c83df5
VALIDATION_RECEIPT_IDENTITY: sha256:67714d456e2dd79563d90e9e0f7439e35248f012c7129ed9274cc32a32c64bfb
VALIDATION_RECEIPT_SHA256: 67714d456e2dd79563d90e9e0f7439e35248f012c7129ed9274cc32a32c64bfb
REQUIRED_ROLE_COUNT: 4
PROJECTED_TEUL_SOURCE_OR_ARTIFACT_COUNT: 0
VALIDATION: PASS
```

Required roles were
`PUBLIC_CONFORMANCE_RUNNER`, `TRACKED_WASM_FAMILY`,
`WASM_CANDIDATE_TOOL`, and `WINDOWS_X64_CANDIDATE_BUILD_ENTRYPOINT`.

## Windows x64 A/B artifact

The same fixed projection was built offline into distinct A/B output roots by
the existing Windows candidate builder.

```text
ARTIFACT: ddonirang.exe
ARTIFACT_COUNT_A_B: 1 / 1
BYTES_A_B: 7043072 / 7043072
SHA256_A_B: af0df4cb069f03ac319106c71917dfeeded87690e03d2045788b6dc88083c41e
A_EQUALS_B: true
PE_STACK_RESERVE_BYTES_A_B: 16777216
FORBIDDEN_PATH_OCCURRENCES_A_B: 0
TEUL_NAMED_ARTIFACT_COUNT_A_B: 0
HELP_EXIT_A_B: 0 / 0
HELP_SHA256_A_B: 15cda0d9f1213fecf52b8efa709bcc99c3389aadf06ba23e157720036c877f65
```

## `ddn.project-run.v1` workflow

Reused fixture:
`pack/ddn_local_project_graph_v1/fixtures/project_run_physics_v1.json`.
Both A/B artifacts used target `앱`, `--inspect-graph`, `--inspect-lock`, and
atomic `--out` publication.

```text
PROJECT_RUN_EXIT_A_B: 0 / 0
PROJECT_RUN_BYTES_A_B: 16488 / 16488
PROJECT_RUN_SHA256_A_B: f9c2e36f4117d4a523438c5ab3a88948c769fc4a4b48c99e9dd6495bd7f29578
PROJECT_RUN_A_EQUALS_B: true
OPTION_CONFLICT_EXIT: 2
OPTION_CONFLICT_DIAGNOSTIC: E_CLI_OPTION_CONFLICT
PARTIAL_SUCCESS_ARTIFACT_ON_CONFLICT: 0
FAILED_TARGET_EXIT: 2
FAILED_TARGET_DIAGNOSTIC: E_PROJECT_TARGET_MISSING
PREEXISTING_ARTIFACT_PRESERVED: true
PREEXISTING_ARTIFACT_SHA256: c4381c906f7b18f801b09cdb93b926ac4f7f8f26ff415d593d61e9d4c9862af0
TEMP_OR_PARTIAL_RESIDUE: 0
```

The executable-neutral semantic identity remains exactly
`ddn.project-run.v1`. This evidence does not decide executable/package naming,
public command membership or legacy alias duration.

## C0-C8 and product value

| Gate | Actual bounded state |
|---|---|
| C0 | Historical 91-command registry remains custody; no bulk promotion. |
| C1 | `ddn.project-run.v1` is reachable on the single lang/tool artifact. Public executable naming remains OPEN. |
| C2 | Shared lang/tool source-coordinate, canon, preprocess, runtime, value and artifact-output authority is preserved. |
| C3 | Approved required workflows are reachable. Public `test/view/repl` membership remains slice-local OPEN. |
| C4 | Migrated required workflows have private teul fallback 0; internal/deferred custody remains. |
| C5 | Bounded V1-required build/test/pack/publish teul execution dependency is 0. |
| C6 | Native/WASM shared product authority and path-clean tracked WASM are GREEN. |
| C7 | Current-source public projection and Windows A/B fixed-artifact reproducibility are GREEN pending target-bound review. |
| C8 | Projection and binary exclude teul; physical deletion/final retirement remains Owner-gated. |

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED: source coordinates now reach a path-clean tracked WASM and byte-reproducible Windows artifact whose project-run output and atomic failures are exact.
REUSED_TEST_COUNT: 58 projection/remap cases, official freshness, one project-run fixture, existing builder and validator
NEW_TEST_ARTIFACT_COUNT: 0
META_TEST_CREATED: 0
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
ACTIVE_REVIEW_TASK_COUNT: 0
REVIEW_BUNDLE_TARGET: W90 source-coordinate + W91 path-clean correction + W92 current-source Windows A/B custody
```

## Nonclaims

Public `test/view/repl` membership, PathIR public physical contract, VC17 exact
landing, rights/license/NOTICE/signing/distribution, physical teul deletion,
whole P5/P6, V1 readiness/release/activation, Owner Human Smoke and Human PASS
remain OPEN. This handoff is implementation/release-custody evidence pending an
exact successor-target independent review disposition.
