# P4 native run-summary output custody W1 — handoff

## Status and fixed lineage

- Status: `IMPLEMENTED_PENDING_REVIEW`
- Authority: internal CURRENT `v25.35.0 / RD-001~490`; public SPEC `v0.6.0`
- Authority impact: `ADDITIVE`; the Higher Structure/Profile R2.1 successor does not change this native invocation/output boundary
- Baseline: `861bcfe4c924c9411ed2ca613dfec58bb0e64ad8`
- Product fixed HEAD: `fa00f9ce0f2d2dae476aef00ec61466aa084c3b2`
- Product fixed tree: `f65b3abdd8669bb845eaca974247c091e4a37971`
- Direct parent / merge count: exact / 0
- Exact product path: `tool/src/main.rs`

## User workflow and product correction

The native `ddonirang-tool run-summary` command accepted the source DDN itself
as `--summary-json` and then replaced that source with the generated JSON. It
also accepted `--madi 0`, published a successful process result and created a
summary file even though the existing execution contract requires a positive
explicit count or `configured`.

The fixed command now:

- rejects `--madi 0` as `E_CLI_OPTION_VALUE_INVALID` with exit 2 and no output;
- rejects an existing output path that refers to the input file as
  `E_CLI_OUTPUT_ALIASES_INPUT` with exit 2 before source execution or writing;
- compares real file identity, not only path text, so Windows hard links and
  Unix device/inode aliases are covered;
- preserves valid positive/configured execution, missing-source exit 1,
  command spelling, membership, source-profile default, runtime semantics and
  the structured summary payload.

No overwrite policy for distinct output files, stable public diagnostic wire,
parser/runtime authority, tracked WASM or public command membership was changed.

## Direct product RED -> GREEN

The baseline executable was run against a task-owned copy of the existing
`seamgrim_wasm_cli_runtime_parity_v1` c01 source.

| case | baseline | fixed |
|---|---|---|
| input path equals `--summary-json` | exit 0; source SHA-256 changed from `5421888c0a2ba48fafe91e8a7e826934cdbb1b1ddabea426bbc58c0746970703` to `eb3e6ea839ed303dab22d8d4cfec44d97436defe19a021c479b4e4f90095ca28` | exit 2; source hash byte-identical |
| output is a hard link to input | source-clobber risk present in the same write path | exit 2; source hash byte-identical |
| `--madi 0` | exit 0; summary file created | exit 2; summary file absent |
| positive `--madi 1`, distinct output | exit 0 | exit 0 |
| missing source, distinct output | exit 1 | exit 1; output absent |

Two valid option forms produced 46,037-byte byte-identical summaries:

```text
SHA256 eb3e6ea839ed303dab22d8d4cfec44d97436defe19a021c479b4e4f90095ca28
```

## Reused verification

- offline native binary build: PASS
- same-path and Windows hard-link source custody: PASS
- positive-count/configured-count execution: PASS
- zero-count fail-closed/no-output: PASS
- missing-source exit/no-output: PASS
- deterministic split/equal option forms: PASS
- bin regression: 406 PASS + 2 pre-existing environment FAIL
- `git diff --check`: PASS

The two bin failures remain the isolated-worktree `ai_prompt` tests that require
the intentionally absent `docs/ssot/**` directory. They do not execute the
changed CLI/output-custody path and remain
`ENVIRONMENT_DEPENDENCY_ABSENT`, not product regressions or hidden GREEN.

No new test, runner, pack, checker, framework, receipt layer or meta-test was
created. The actual executable supplied the fail-open RED; the hard-link case
is the single risk-relevant alias check.

## Anti-meta, review and next gate

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: a summary request can no longer destroy its own DDN source or succeed with a zero execution count.
- `NEW_TEST_ARTIFACT_COUNT`: 0
- `EXISTING_TEST_REUSED_COUNT`: 408 bin tests observed plus direct existing-source CLI executions
- `META_TEST_CREATED`: 0
- `STOP_RULE_APPLIED`: yes
- `NEW_REVIEW_TASK_COUNT`: 0
- `NEW_REVIEW_WORKTREE_COUNT`: 0
- `REVIEW_BUNDLE_TARGET`: the existing coherent P4 trace/default, unit-registry and official native CLI failure/output-custody milestone
- `REVIEW_NEEDED_NOW`: yes; source preservation and process/output failure classification are release-relevant product behavior

## Open gates and nonclaims

- P2 exact durable revision manifest/wire/hash/CAS/DB/storage/GC: Owner-open.
- P3 official Workbench default ingress and editable durable custody: open.
- P4 stable receipt/replay wire and independent review: open.
- P5 path-clean Windows candidate independent review, exact package/archive/installer format, rights/license/SBOM/notices, signing and distribution: open.
- VC15 English dialect activation and current-pack evidence rebase: open.
- whole P1/P2/P3/P4/P5/V1 closure, membership/readiness, release,
  activation, Owner Human Smoke PASS and Human PASS are not claimed.
