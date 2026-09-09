# P5 W21 current-source Windows A/B reproducibility W22 handoff

STATUS: `P5_W21_CURRENT_SOURCE_WINDOWS_AB_REPRODUCIBILITY_IMPLEMENTED_PENDING_REVIEW`

## Authority and bounded impact

- Internal live CURRENT: `v25.47.0 / RD-001~543`.
- CURRENT SHA-256: `40b116735b834f0eecb2c252cc77f73a01a8be06b85421de1d53f2d1b9e534af`.
- Index SHA-256: `2f827e7f55d23def55be590b57482e376b1d9c43cd7db2c9f72271e59c556838`.
- Aggregate SHA-256: `d4d9bb661f1424ae5d16a6b70dc86a6bef22d13766820f6001c8f2b28f83b5e4`.
- Manifest SHA-256: `d8a9fed64085efffefd9eac4573d7ab18975b59bebdea2009e3215a7b9268493`.
- Seal SHA-256: `f1869520079909eed85f2737c27a0aada3b5d013ac6c5bb41a0c781a3e501f4d`.
- Public Language SPEC: `v0.6.0`; CURRENT SHA-256
  `6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0`.
- Successor impact on this bounded CLI/release-custody slice:
  `UNAFFECTED_WITH_ADDITIVE_OUT_OF_SCOPE_SUCCESSOR`.
- `docs/ssot/**` and `publish/spec/**` change: 0.

The persistent V1 closure goal is ACTIVE. Review commit
`181896585e6a5ce39a18a1a6a009e3ce50e7d9bf` and P5 review commit
`bc84d81d4faa55974975bdb7ec60cb18d9a7ebda` are ancestors of this lineage.
Their verdicts remain target-bound; neither is broadened here.

## Exact lineage and source custody

- W18 fixed: `fa3e49f2e457e741b1a06c7d61ad1a06e8603ab7`.
- W19 fixed: `0c26a1e5d1b38e9bedba1b219160caba05068136`.
- W20 fixed: `3209a35413c960da65e20d065a326c1a9763b854`.
- W21 product/test fixed and release source:
  `753fa87c424987597ecb98fbdc6a948356a5c82a`.
- W21 fixed tree: `a5a38d1402e0a0f8d000a53cc8302a69a8a12167`.
- W21 handoff / W22 parent:
  `3da4d222b045b64e548d7cefb7e4c75efc96a3bb`.
- Merge commits in the bounded successor chain: 0.
- Product source difference from W21 fixed to W22 parent: 0.

The projection tool read exact Git blobs from W21 fixed rather than working
tree bytes. The source manifest used only for external build custody is 8,695
bytes, SHA-256
`493b7b7fb08f95dacb4ec1c7c504e4f747657e22008cc85b0210bf946464ae05`,
and binds source commit `753fa87c424987597ecb98fbdc6a948356a5c82a`.

## Public projection

- Projection:
  `I:/home/urihanl/ddn/codex/build/candidates/v1-current-cli-753fa87-projection-r1`.
- Receipt root:
  `I:/home/urihanl/ddn/codex/build/candidates/v1-current-cli-753fa87-projection-receipts-r1`.
- File count: 174.
- Public tree identity:
  `sha256:2345f8cd169260ae2dbd601b8bcb8d4f50a940b19ba6a7bd2f1fe9e373ed4983`.
- Projection receipt: 1,143 bytes, SHA-256
  `134cbb29bc00c66cce47b9556b84ea7218cfefb64cdc4a502db88c08cc414576`.
- Tree manifest: 34,369 bytes, SHA-256
  `3a2dd989b87a3ea7b9f3f41c9e394e9edff02cdcacd33c1d6aa732cafc5b3761`.
- Validation receipt: 630 bytes, identity/SHA-256
  `6202f1417f285356472c0681cab22fd5374de971aa4238aff22b1521981e8f3c`.
- Required roles `PRODUCT_SOURCE`, `PUBLIC_CONFORMANCE_RUNNER`,
  `TRACKED_WASM_FAMILY`, and `WASM_CANDIDATE_TOOL`: 4/4 PASS.
- Projected `tools/teul-cli` paths and teul-named release artifacts: 0.

## Windows x64 A/B result

The existing `scripts/build_windows_x64_public_candidate.ps1` built twice from
the same projection into distinct output roots. Both builds used offline Cargo,
the portable public Cargo config, source/Cargo/rustup remap roots, `/Brepro`,
and a 16 MiB stack reserve.

```text
WINDOWS_A: I:/home/urihanl/ddn/codex/build/candidates/v1-current-cli-753fa87-windows-r1
WINDOWS_B: I:/home/urihanl/ddn/codex/build/candidates/v1-current-cli-753fa87-windows-r2
ARTIFACT: ddonirang.exe
BYTES_A: 7043584
BYTES_B: 7043584
SHA256_A: 8129df4e1fc0419b658bd74278751a286d5127b1a37db630f014f3d9f609ff71
SHA256_B: 8129df4e1fc0419b658bd74278751a286d5127b1a37db630f014f3d9f609ff71
A_EQUALS_B: true
PE_STACK_RESERVE_BYTES_A_B: 16777216
FORBIDDEN_PATH_OCCURRENCES_A_B: 0
TEUL_NAMED_ARTIFACT_COUNT_A_B: 0
```

The existing Cargo PDB filename-collision warning and dead-code warnings were
non-fatal and unchanged in kind. Both builds completed successfully.

## Product-facing workflow and failure boundary

Reused fixture:
`pack/ddn_local_project_graph_v1/fixtures/project_run_physics_v1.json`.
Both executables ran the exact `ddn.project-run.v1` request with target `앱`,
`--inspect-graph`, `--inspect-lock`, and atomic `--out` publication.

```text
PROJECT_RUN_EXIT_A_B: 0
PROJECT_RUN_BYTES_A_B: 16488
PROJECT_RUN_SHA256_A_B: f9c2e36f4117d4a523438c5ab3a88948c769fc4a4b48c99e9dd6495bd7f29578
PROJECT_RUN_A_EQUALS_B: true
OPTION_CONFLICT: positional-start + --virtual
OPTION_CONFLICT_EXIT: 2
OPTION_CONFLICT_DIAGNOSTIC: E_CLI_OPTION_CONFLICT
PARTIAL_SUCCESS_ARTIFACT_ON_CONFLICT: 0
TEMP_RESIDUE_A_B: 0
```

This preserves the Owner-bound semantic identity `ddn.project-run.v1` without
deciding executable name, package name, legacy alias duration, or public
command membership.

## C0~C8 actual state

| Gate | Current bounded state |
|---|---|
| C0 | Historical 91-command registry remains custody; no bulk promotion. |
| C1 | `ddn.project-run.v1` is fixed and reachable; executable/package/alias naming remains OPEN. |
| C2 | Shared lang/tool canon, preprocess, runtime, value and output-authority convergence remains preserved. |
| C3 | Approved candidate workflows exist; public test/view/repl membership remains slice-local OPEN. |
| C4 | Migrated workflows have private teul semantic fallback 0; internal/deferred physical custody remains. |
| C5 | Bounded V1-required build/test/pack/publish teul execution dependency remains 0. |
| C6 | Native candidate output and failure boundary are deterministic; tracked WASM/Workbench claims remain only at their fixed reviewed targets. |
| C7 | W21 source public projection and Windows x64 A/B reproducibility PASS in bounded custody. |
| C8 | Candidate projection/binary excludes teul; physical deletion and final public retirement remain Owner-gated. |

## Product value, anti-meta, and review queue

USER_WORKFLOW_CHANGED_OR_UNBLOCKED: the cumulative W18~W21 shared output
authority now has a reproducible path-clean Windows candidate, while the real
`project-run` workflow preserves exact structured output and fail-closed option
conflict behavior.

NEXT_PRODUCT_DECISION_ENABLED: the existing rolling reviewer can evaluate the
coherent W18~W21 product milestone with this W22 release-custody companion at
one fixed source identity.

```text
REUSED_TEST_COUNT: 1 product fixture + existing projection/build guards
NEW_TEST_ARTIFACT_COUNT: 0
NEW_PACK: 0
NEW_RUNNER: 0
META_TEST_CREATED: 0
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
ACTIVE_REVIEW_TASK_COUNT: 0
REUSABLE_REVIEWER_HANDLE_COUNT: 1
REVIEWER_HANDLE: 01a04b17-66bb-7fa3-b827-53ad450005b4
REVIEW_BUNDLE_TARGET: W18-W21 shared atomic-output authority + W22 Windows/public-source custody
```

## Remaining gates and nonclaims

The following remain slice-local OPEN and are not a whole-goal impasse:
strict SPEC-history projection, PathIR public contract, public test/view/repl
membership, VC17 exact provider landing, final executable/package naming,
legacy alias duration, teul physical deletion, and external distribution.

PathIR/Proof P0 containment remains preserved. This handoff does not claim
whole P5 closure, final RC, public release, V1 membership/readiness, activation,
legal clearance, Owner Human Smoke, Human PASS, whole teul retirement, or
physical deletion approval.
