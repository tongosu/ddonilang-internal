# P4 canon CLI failure exit W1 — handoff

## Status and fixed lineage

- Status: `IMPLEMENTED_PENDING_REVIEW`
- Authority: internal CURRENT `v25.35.0 / RD-001~490`; public SPEC `v0.6.0`
- Baseline: `7a90710ea74c4e50d3313ba2252b3aa251199540`
- Product/test fixed HEAD: `e748dc3b7a7955ea58e4250d6567d4446aac7652`
- Product/test fixed tree: `17aad3916fc46642296f5def67fbc04b21bdf959`
- Direct parent / merge count: exact / 0

## User workflow and correction

The existing shared-authority `ddonirang-tool canon` product path returned exit
0 for invalid invocation before canonicalization. Missing input, invalid bridge
and extra positional arguments could therefore be accepted by automation as
successful canon operations.

The fixed `tool/src/main.rs` canon arm now uses:

- exit 1 for feature/product execution failure;
- exit 2 for missing option value, invalid bridge, extra argument or missing
  input;
- exit 0 for a successful canonical-output operation.

Canon/parser/preprocess authority, output bytes, command spelling and public
membership were not changed.

## Product RED -> GREEN

Direct executable baseline:

| case | baseline | fixed |
|---|---:|---:|
| missing input | exit 0 | exit 2 |
| invalid `--bridge` | exit 0 | exit 2 |
| extra positional argument | exit 0 | exit 2 |
| valid canonical output | not changed | exit 0 |

Reused verification:

- native binary build: PASS
- current canon-filtered tool tests: 82/82 PASS
- current preprocess-filtered tool tests: 58/58 PASS
- shared canon/preprocess authority checker: owner 1/1, reverse imports 0,
  private fallback 0 — PASS
- `git diff --check`: PASS

No new test, runner, pack, checker, mutation harness, framework or meta-test was
created. The real executable supplied all three RED cases.

## P2 authority gate observed before this non-overlapping slice

Live v25.35 RD-452~456 approves project lifecycle role separation and immutable
execution-snapshot principles, but still marks exact manifest spelling/wire,
hash domain, CAS/DB layout and autosave/storage/GC as OPEN. Durable
create/save/reopen implementation was therefore not invented.

```text
P2_DURABLE_SAVE_REOPEN: CONFLICT_OR_OWNER_DECISION
FILE_OWNER_EXPANSION_REQUIRED_AFTER_EXACT_SCHEMA: tool/src/local_project.rs and exact storage/frontdoor paths
RECOMMENDATION: preserve logical roles now; bind an exact versioned durable-revision wire before product persistence implementation
```

## Review and anti-meta checkpoint

- Bundle with the P4 runtime-default, unit-registry and bootstrap-exit fixed
  lineage for the existing rolling reviewer; writer created reviewer/worktree 0.
- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: canon automation now distinguishes
  invalid invocation from a successful canonicalization.
- `NEW_TEST_ARTIFACT_COUNT`: 0
- `EXISTING_TEST_REUSED_COUNT`: 140 filtered tests plus four executable checks
- `META_TEST_CREATED`: 0
- `STOP_RULE_APPLIED`: yes
- `NEXT_PRODUCT_DECISION_ENABLED`: coherent P4 CLI/runtime failure-boundary
  review can proceed without conflating P2's unresolved persistence wire.

## Nonclaims

No public command membership decision, independent PASS, whole P2/P4/P5
closure, Windows RC promotion, V1 membership/readiness, release, activation,
Owner Human Smoke PASS or Human PASS is claimed.
