# FD02A / FD02B / FD03 follow-up tickets

No product implementation is authorized by this census.

This file owns the required FD02A review ticket, FD02A gap ticket, FD02B ticket, and FD03 gap ticket. It does not authorize execution of any ticket.

## FD02A — Editable Project Snapshot Custody impact/review ticket

```yaml
TICKET: DDN-P-V1-FD02A-EDITABLE-PROJECT-SNAPSHOT-CUSTODY-ADOPTION-R1
TYPE: IMPACT_ANALYSIS_AND_TARGETED_REVIEW
PREDECESSOR_CANDIDATE: d0ff23389e27b8268fe9eead8d0138abd6d77b06
PREDECESSOR_REVIEW_PARENT: 2d489c8d9b2651f5314afdfa4a453568622dfbfd
PREDECESSOR_VERDICT: NOT_BOUND
IMPLEMENTATION_AUTHORIZED: NO
```

### Reuse; do not reimplement

- Rust `EditableSourceTreeCandidate` normalization and identity.
- saved server project/revision/content descriptor.
- stale source tree versus saved head failure.
- analysis snapshot and execution source binding.
- candidate prepared envelope/receipt tamper validation.
- expected server HEAD run creation.
- unknown local snapshot schema fail-closed.
- orphan-object candidate ledger.

### Required impact review

1. diff `d0ff2338...` against product-first successor and classify every overlap.
2. ensure R3N-FU01 source-identity changes remain intact.
3. verify candidate source-tree identity can later incorporate R2 semantic config/epoch/lock/resource identities without changing current meaning silently.
4. keep first candidate PreV25-only and public ingress 0.
5. distinguish local-only recovery from server SavedProjectRevision visibly; no silent authority fallback.
6. run direct CLI/WASM/Workbench parity, clean A/B, Edge, mutation and crash/atomicity tests at one fixed head.
7. request independent plain PASS; PASS_WITH_FOLLOW_UP does not authorize adoption closure.

### Acceptance

```text
FD02A_PREDECESSOR_REVIEWED_PLAIN_PASS
FD02A_PRODUCT_FIRST_LINEAR_ADOPTION_READY
R3N_FU01_IDENTITY_PRESERVED
PUBLIC_STABLE_WIRE_OPEN
TRACKED_WASM_REFRESH_0
```

## FD02B — Save / Reopen / Recovery / CAS ticket

```yaml
TICKET: DDN-P-V1-FD02B-SAVE-REOPEN-RECOVERY-CAS-R1
TYPE: NEW_PRODUCT_VERTICAL_AFTER_FD02A
IMPLEMENTATION_AUTHORIZED: NO
DEPENDENCY: FD02A plain PASS and product-first adoption decision
```

### Scope

- typed RecoveryCheckpoint separate from SavedProjectRevision.
- bounded recovery retention.
- file/resource content-addressed blobs and small snapshot reference manifest.
- explicit `곳간` membership; `.DS_Store`/`Thumbs.db` identity-neutral.
- old-or-new complete snapshot crash atomicity.
- reachability GC with saved revision, receipt, replay and retained recovery roots.
- no per-keystroke durable revision; no Run-triggered save.

### Non-goals

- Git delta packing, branch/merge/blame.
- distributed/network CAS.
- stable public snapshot wire.
- package marketplace.

### Acceptance

- PUX19-PUX26 and PUX34-PUX35 product runners.
- same large resource reused once; unchanged Run x100 source blob growth 0.
- one-file edit duplicates no unchanged blobs.
- fault injection at every object/manifest/HEAD/GC phase.
- CLI/WASM/Workbench exact identity parity where applicable.
- independent fixed-head plain PASS.

## FD02A gap ticket

```yaml
TICKET: DDN-P-V1-FD02A-PROJECT-UX-R2-ALIGNMENT-GAPS-R1
TYPE: CONTRACT_AND_TEST_GAP_PREPARATION
IMPLEMENTATION_AUTHORIZED: NO
INPUT: 04_FD02A_EDITABLE_I1_IMPACT_MATRIX.md
```

Scope is restricted to gaps that belong to editable execution custody: typed four-state identity names, semantic input composition interfaces, and adoption-time authority conflict checks. It must not implement FD03 manifest/epoch meaning or FD02B CAS/GC.

## FD03 — Project-Owned 글판(SourceEpoch) ticket

```yaml
TICKET: DDN-P-V1-FD03-PROJECT-OWNED-SOURCE-EPOCH-R1
TYPE: FUTURE_PRODUCT_VERTICAL
IMPLEMENTATION_AUTHORIZED: NO
DEPENDENCY: FD02A product-first adoption and exact Owner/SSOT surface authority
CURRENT_TYPE_OWNER: lang/src/ast.rs::SourceEpoch
CURRENT_PARSE_OWNERS: lang/src/lib.rs::{parse_with_mode,parse_v25_with_mode}
CURRENT_RUNTIME_SELECTOR: tool/src/ddn_runtime.rs::from_source_epoch_with_mode
CURRENT_PROJECT_OWNER: MISSING
```

Required future scope:

- `차림새` semantic config owns exact `글판` value and `첫글` role.
- Rust maps the declared value to `SourceEpoch`; caller/Workbench cannot override it.
- unknown, missing-under-required-profile, and mismatch inputs fail closed.
- content sniffing and silent PreV25/V25 fallback remain forbidden.
- analysis, execution envelope and receipt bind the same epoch/config identity.
- single-file compatibility/default policy remains separate from formal project policy.
- exact public spelling/schema/diagnostics remain OPEN until Owner/SSOT authority exists.

Evidence ticket cases: PUX04-PUX10, PUX18, PUX29-PUX32 plus CLI/WASM/Workbench parity and forged-caller mutation.

## Later sequence

1. FD03 — Project-Owned 글판(SourceEpoch), R2 semantic manifest identities.
2. FD04 — V25 migration and full product corpus.
3. FD05 — new-project V25 default.
4. FD06 — official V25 default.

FD03 must not be pulled into FD02A. FD05/FD06 require separate Owner authorization and Human/product gates.

## Safe next gate

`NEXT_SAFE_GATE: FD02A_PREDECESSOR_TARGETED_REVIEW_AND_PRODUCT_FIRST_OVERLAP_AUDIT`

This is a review/adoption-preparation gate, not implementation approval.

## 2026-08-29 readiness correction absorbed into existing tickets

No ticket ID is added or replaced.

### FD02A alignment ticket additions

- bind the exact PSC field-family table in `03_CURRENT_TO_TARGET_DELTA_MATRIX.md`;
- remove descriptive `project_name` and undeclared incidental files from semantic graph input;
- converge CLI project-run, standalone CLI, WASM and Workbench on one explicit invocation-context owner;
- preserve I1 as `PASS_WITH_FOLLOW_UP / ADOPTABLE_WITH_TARGETED_CORRECTION`, not plain PASS;
- require actual Edge evidence, LF-forced fixed-head WASM reproduction and candidate build-policy unification before adoption;
- keep the full composite analysis/run identity open until epoch/config/lock/resource owners exist.

`FD02A_READINESS: BLOCKED_BY_SEMANTIC_GAP_AND_TARGETED_CORRECTION`

### FD02B ticket additions

- resource authority is explicit declaration; directory-wide crawl and source reference alone are not membership authority;
- Owner must select file-only declaration or exact recursive-directory semantics before implementation;
- bind visible save failure to `OLD_COMPLETE | NEW_COMPLETE`, never visible `HALF`;
- bind reopen mismatch to fail-closed or a separately typed non-authoritative recovery candidate; no silent repair;
- retain expected-head optimistic concurrency as the existing product-policy contract;
- only explicit successful Save turns a selected recovery candidate into a durable revision;
- Run creates no SavedProjectRevision and does not mutate lock or declared resources.

`FD02B_READINESS: PARTIAL_WITH_SEMANTIC_AND_OWNER_BLOCKERS`

### FD03 ticket additions

The exact state matrix must be decided without inventing hidden defaults:

| State | Current readiness |
|---|---|
| new formal project | Owner decision required for recorded epoch/default |
| formal project with explicit supported epoch | ready after v25.17 promotion |
| formal project without epoch | Owner decision required |
| legacy project without epoch | Owner decision required for explicit migration marker/profile |
| supported epoch | semantics closed by RD-333~337; project ownership awaits v25.17 promotion |
| unknown/unsupported epoch | fail closed; no fallback |
| pre-V25 project | explicit compatibility/migration route required |
| standalone DDN | separate default policy; must not be inferred from public SPEC version |

`FD03_READINESS: BLOCKED_BY_OWNER_DECISION`

Unknown and unsupported epochs fail before analysis/execution identity or effects. Migration must
use an explicit compatibility reader/profile; it may not content-sniff a legacy source and parse it
as current V25. Public Language SPEC `v0.6.0` identifies a publication, not a SourceEpoch selector.
CLI, WASM and Workbench must consume the same Rust-owned project epoch projection.

### Revised safe next gate

`NEXT_SAFE_GATE: OWNER_DECISION_ON_RESOURCE_DECLARATION_AND_SOURCE_EPOCH_STATE_MATRIX_THEN_SSOT_CLARIFICATION`

This is still not product implementation authorization.
