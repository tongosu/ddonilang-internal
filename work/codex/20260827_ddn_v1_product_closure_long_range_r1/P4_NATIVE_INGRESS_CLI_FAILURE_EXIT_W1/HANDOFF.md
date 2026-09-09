# P4 native ingress CLI failure exit W1 — handoff

## Status and fixed lineage

- Status: `IMPLEMENTED_PENDING_REVIEW`
- Authority: internal CURRENT `v25.35.0 / RD-001~490`; public SPEC `v0.6.0`
- Authority impact: `ADDITIVE`; RD-484~490 Higher Structure/Profile successor has no relevant product-semantic impact on this CLI invocation boundary
- Baseline: `23a73c2737d41245eab10017ea4a523518d31f9b`
- Product fixed HEAD: `d6f5dae4363063b03654b865fa022c0e7fdf5cff`
- Product fixed tree: `0719407287981300fa2663c960ab5a1d96bdc7d0`
- Direct parent / merge count: exact / 0
- Exact product path: `tool/src/main.rs`

## User workflow and correction

The existing native `ddonirang-tool run-summary` ingress silently treated a
missing `--madi` or `--summary-json` value as if the option had not been
provided. Both invalid invocations therefore executed successfully with exit
0, which could let release automation mistake malformed execution requests for
valid runs.

The fixed command now validates its existing argument contract before product
execution:

- missing option value, invalid `--madi`, unknown option, duplicate option or
  non-single input path: exit 2;
- actual file/runtime/product failure: exit 1;
- valid summary execution: exit 0.

Command spelling, membership, source-profile default, runtime semantics and
structured summary payload were not changed.

## Direct RED -> GREEN and determinism

Baseline RED:

| invocation | baseline |
|---|---:|
| valid input + `--madi` with no value | exit 0 |
| valid input + `--summary-json` with no value | exit 0 |
| extra positional input | exit 1, not usage-classified |

Fixed GREEN:

| invocation | fixed |
|---|---:|
| missing `--madi` value | exit 2 / `E_CLI_OPTION_VALUE_REQUIRED` |
| missing `--summary-json` value | exit 2 / `E_CLI_OPTION_VALUE_REQUIRED` |
| extra positional input | exit 2 |
| invalid `--madi bad` | exit 2 / `E_CLI_OPTION_VALUE_INVALID` |
| unknown `--unknown` | exit 2 / `E_CLI_OPTION_UNKNOWN` |
| valid input + `--madi configured` | exit 0 |
| missing source file after valid invocation | exit 1 |

Two successful summaries using split and `--key=value` option forms were
byte-identical:

```text
SHA256 828429fced1062c468abc946c56121dda71dcb5a26f5811545e582e95f5b40f9
MATCH true
```

## Reused verification and bounded environment finding

- offline native binary build: PASS
- direct executable negative cases: 5/5 expected exit 2
- direct executable positive case: PASS / exit 0
- direct product-failure case: PASS / exit 1
- bin regression: 406 PASS + 2 pre-existing environment FAIL
- `git diff --check`: PASS

The two bin failures are `ai_prompt` tests that require
`docs/ssot/**`, which is intentionally absent from this isolated product
worktree. They do not execute the changed CLI parser and are retained as
`ENVIRONMENT_DEPENDENCY_ABSENT`, not promoted to product PASS or hidden as
GREEN.

No new test, runner, pack, checker, mutation harness, framework or meta-test
was created. The actual baseline executable supplied the fail-open RED.

## VC15 evidence drift classified before this vertical

The existing `lang_dialect_smoke_v1` and `dialect_builtin_equiv_v1` packs do
not currently establish a safe product change. Their sources retain spaces in
the current attached `}인것` marker and English `if` rows lost the legacy
`#말씨: en` activator in the hard-cut commit `4f03b858`. Two further golden
rows omit current receipt/trace output fields. The attempted product change was
fully restored to the fixed Git blob before this slice.

Disposition:

```text
VC15_CURRENT_PACKS: EVIDENCE_REBASE_REQUIRED
ENGLISH_DIALECT_ACTIVATION: CONFLICT_OR_OWNER_DECISION
PRODUCT_CHANGE_FROM_VC15_AUDIT: 0
```

No private alias table, hidden header fallback, test lowering or unsupported
dialect default was introduced.

## Anti-meta, review and next gate

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: malformed native summary requests can no longer publish a successful process result.
- `NEW_TEST_ARTIFACT_COUNT`: 0
- `EXISTING_TEST_REUSED_COUNT`: 408 bin tests observed plus direct executable checks
- `META_TEST_CREATED`: 0
- `STOP_RULE_APPLIED`: yes
- `NEXT_PRODUCT_DECISION_ENABLED`: the existing rolling reviewer can assess one coherent P4 native CLI/runtime failure-boundary bundle.
- `ACTIVE_REVIEW_TASK_COUNT`: no new task created by the writer
- `NEW_REVIEW_TASK_COUNT`: 0
- `NEW_REVIEW_WORKTREE_COUNT`: 0
- `REVIEW_BUNDLE_TARGET`: P4 trace-default, unit-registry, bootstrap-exit, canon-exit and native run-summary invocation boundary

## Open gates and nonclaims

- P2 exact durable revision manifest/wire/hash/CAS/DB/storage/GC: Owner-open.
- P3 official Workbench default ingress and editable durable custody: open.
- P4 stable receipt/replay wire and independent review: open.
- P5 package/archive/installer format, rights/license/SBOM/notices, signing and distribution: open.
- VC15 English dialect activation and current-pack evidence rebase: open.
- whole P1/P2/P3/P4/P5/V1 closure, membership/readiness, release,
  activation, Owner Human Smoke PASS and Human PASS are not claimed.
