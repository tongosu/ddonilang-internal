# D-PACK-V1-PROJECT-UX-R2-R1 design

Status: design-only. Fixtures/oracles/runners are not implemented in this census.

Coverage labels:

- `ALREADY_COVERED`: primary baseline has a directly relevant product test; R2 naming/wire is not thereby closed.
- `PARTIALLY_COVERED`: adjacent current or Editable I1 evidence exists, but the exact R2 case is incomplete.
- `NOT_COVERED`: exact product test is absent; `FUTURE_TEST`.
- `NEEDS_INDEPENDENT_REVIEW`: Editable I1 side evidence participates and cannot be promoted by this census.

| case_id | fixture | action | expected identity delta | expected storage delta | expected result | forbidden behavior | evidence |
|---|---|---|---|---|---|---|---|
| PUX01 | `안녕.ddn` only | run | one SourceTree + explicit/default epoch identity | revision 0 | success | project required | CLI/WASM/Workbench parity |
| PUX02 | editor single file | type 100 chars | EditorGeneration +100 only | durable revision +0 | success | per-keystroke revision | store row counts |
| PUX03 | run snapshot A, then edit B | continue A | A identity unchanged | no A blob rewrite | A deterministic | live editor bleed | receipt/hash |
| PUX04 | create formal project | create | semantic config + tree identities | one complete revision | `처음.ddn + 차림새` | hidden extra user files | tree listing |
| PUX05 | manifest entry points `main.ddn` | run | entry identity=`main.ddn` | none | success | `처음.ddn` magic override | Rust manifest receipt |
| PUX06 | each allowed 글판 | analyze/run | exact SourceEpoch mapping | none | same epoch both | sniffing | typed receipt |
| PUX07 | unknown 글판 | open/analyze/run | no identity committed | none | fail closed | fallback PreV25/V25 | exact diagnostic |
| PUX08 | epoch/source mismatch | analyze/run | no execution identity | none | fail closed | content sniff switch | exact diagnostic |
| PUX09 | descriptive name edit | save | authored manifest changes; semantic config unchanged | new revision, reusable source blobs | success | execution hash change | identity comparison |
| PUX10 | first-entry semantic edit | save | semantic config and project snapshot change | small manifest/revision only | success | stale execution reuse | identity comparison |
| PUX11 | no dependency, no lock | run | lock identity absent | none | success | empty lock required | receipt |
| PUX12 | dependency, lock missing | run | no execution snapshot | none | fail closed | auto resolve | `E_LOCK_MISSING` successor |
| PUX13 | dependency, lock mismatch | run | no execution snapshot | none | fail closed | best-effort run | exact diagnostic |
| PUX14 | 가지 맞추기 valid | explicit update | new lock identity | old-or-new complete lock | success | Run-triggered update | atomicity receipt |
| PUX15 | 가지 맞추기 injected failure | update | old lock identity retained | partial files 0 | fail closed | half vendor/lock | fault injection |
| PUX16 | valid locked project | Run | identities unchanged | network calls 0 | success | registry lookup | network counter |
| PUX17 | valid locked project | Run | lock bytes/hash unchanged | lock writes 0 | success | timestamp refresh | before/after hash |
| PUX18 | same vendored dep at relocated checkout | normalize | content/source logical identity same | none | success | absolute path identity | A/B checkout receipts |
| PUX19 | declared/undeclared 곳간 files | snapshot | only declared membership counts | declared blobs only | success | directory sniffing | manifest/blob ledger |
| PUX20 | add `.DS_Store`, `Thumbs.db` | snapshot | identity unchanged | blobs +0 | success | metadata ingestion | before/after receipt |
| PUX21 | same large resource referenced twice | save | one content identity | blob +1 total | success | duplicated bytes | object count/hash |
| PUX22 | unchanged source | Run x100 | same source identity | source blobs +0; runs allowed | success | source copy per Run | object-role counts |
| PUX23 | edit one of N files | save | one file blob + snapshot identity changes | unchanged blobs +0, changed blob +1 | success | full project copy | CAS ledger |
| PUX24 | save then reopen | reopen | exact snapshot identity preserved | no new revision | success | normalize-to-different bytes | byte/hash parity |
| PUX25 | crash before/after HEAD commit | recover | old or new complete identity | orphan may be ledgered | fail/recover | partial visible snapshot | phase fault matrix |
| PUX26 | two writers same expected HEAD | second save | first new identity only | second visible writes 0 | second fail closed | last-writer overwrite | concurrency test |
| PUX27 | NFC/NFD same path pair | normalize | no snapshot identity | none | collision error | silent merge | exact path diagnostic |
| PUX28 | case-only path pair | normalize | no snapshot identity | none | portability collision | platform-specific acceptance | exact diagnostic |
| PUX29 | checkout root relocation | snapshot/run | identities same | none | success | host path leakage | clean A/B |
| PUX30 | analysis snapshot A, run input B | Run | no execution identity | run/receipt writes 0 | fail closed | mixed snapshot | mutation test |
| PUX31 | forged JS source/config hash | Run | Rust recomputed identity differs | writes 0 | fail closed | trusting JS hash | CLI/WASM attack |
| PUX32 | type mismatch in touched workflow | analyze/run | diagnostic identity only | writes 0 | fail closed | old user-facing type term | exact `씨` direction review |
| PUX33 | unknown snapshot schema | reopen | none | writes 0 | fail closed | permissive migration | exact diagnostic |
| PUX34 | recovery retention exceeds bound | checkpoint | semantic project identity unchanged | oldest unpinned recovery pruned | success | saved/receipt root prune | reachability ledger |
| PUX35 | GC with saved/receipt/replay roots | collect | live identities unchanged | unreachable only removed | success | live object deletion | mark/sweep proof |

## Runner contract

- same original source inputs go through CLI, WASM, and Workbench product frontdoors.
- logical oracle does not replace product execution.
- identity fields are recomputed by Rust, never accepted solely from JS.
- negative cases assert state/revision/output/effect atomicity.
- mutation runs are GREEN → one-axis RED → exact restore → GREEN with residue 0.
- source-built and tracked WASM identities remain separately reported; no tracked refresh is authorized here.

## Current coverage classification

Every case is assigned exactly once to the primary coverage groups.

```yaml
DPACK_TOTAL: 35
ALREADY_COVERED_COUNT: 10
ALREADY_COVERED: [PUX01, PUX11, PUX12, PUX13, PUX16, PUX17, PUX24, PUX26, PUX27, PUX28]
PARTIALLY_COVERED_COUNT: 19
PARTIALLY_COVERED: [PUX02, PUX03, PUX05, PUX06, PUX08, PUX09, PUX10, PUX14, PUX15, PUX18, PUX19, PUX21, PUX22, PUX23, PUX25, PUX29, PUX30, PUX31, PUX33]
NOT_COVERED_COUNT: 6
NOT_COVERED: [PUX04, PUX07, PUX20, PUX32, PUX34, PUX35]
CLASSIFICATION_BIJECTION: 35/35
```

Primary evidence mapping:

- `PUX01`: single-file CLI/runtime and Workbench runner families.
- `PUX11-PUX13`, `PUX16-PUX17`: `ddn_local_project_*` Rust/CLI/WASM lock/run evidence.
- `PUX24`: `run_seamgrim_project_save_reopen_check.py`, server Workbench reopen runner.
- `PUX26`: project revision conflict/restore runners and expected-parent store tests.
- `PUX27-PUX28`: `normalize_virtual_project_source` duplicate/NFC/case collision Rust tests.

Editable I1 overlay classification:

```yaml
EDITABLE_I1_ALREADY_COVERED_CANDIDATE: [PUX03, PUX24, PUX26, PUX30, PUX31, PUX33]
EDITABLE_I1_PARTIALLY_COVERED_CANDIDATE: [PUX02, PUX25]
EDITABLE_I1_NOT_COVERED: [PUX04, PUX07, PUX19, PUX20, PUX21, PUX22, PUX23, PUX32, PUX34, PUX35]
NEEDS_INDEPENDENT_REVIEW: [PUX03, PUX25, PUX30, PUX31, PUX33]
```

`ALREADY_COVERED` is a census mapping, not a new execution result. No product runner was rerun in this docs-only correction.

## Pack ownership split

- FD02A owns PUX02, PUX03, PUX24-PUX26, PUX30-PUX33.
- FD02B owns PUX19-PUX23, PUX34-PUX35 and storage portions of PUX24-PUX26.
- FD03 owns PUX04-PUX13, PUX18, PUX27-PUX29 and epoch/config portions.
- later lock/resource successors own stable wire claims. This design does not close them.

## 2026-08-29 semantic-readiness overlay

The 35 cases and their existing evidence classes are preserved byte-for-meaning. No case was
promoted to an executable oracle. Readiness gaps are mapped onto the existing family only:

| Readiness gap | Existing cases | Readiness owner |
|---|---|---|
| PSC field classification | PUX05, PUX09, PUX10, PUX30, PUX31 | FD02A alignment |
| declared resource membership | PUX19-PUX23, PUX29 | FD02B plus exact Owner decision for directory declaration semantics |
| root/frontdoor discovery | PUX01, PUX04, PUX05, PUX29, PUX31 | FD02A alignment / FD03 boundary |
| project-owned SourceEpoch | PUX04, PUX06-PUX08, PUX29-PUX32 | FD03 |
| save atomicity | PUX23, PUX25 | FD02B |
| reopen validation | PUX24, PUX33 | FD02B |
| recovery authority | PUX25, PUX34, PUX35 | FD02B |
| concurrent save | PUX26 | FD02B |
| Run-vs-Save | PUX02, PUX03, PUX22, PUX30 | FD02A/FD02B |

Invariant re-audit:

```yaml
I1_TYPING_NOT_DURABLE_REVISION: CLOSED_BY_ROLE_SEPARATION
I2_RUN_IMMUTABLE_EXECUTION_SNAPSHOT: READY_AFTER_V25_17_PROMOTION
I3_NO_MIXED_ANALYSIS_RUN_SNAPSHOT: PARTIAL_I1_FULL_COMPOSITE_OPEN
I4_SAVE_ATOMIC_PROJECT_COMMIT: BLOCKED_BY_SEMANTIC_GAP
I5_REOPEN_IDENTITY_VALIDATION: PARTIAL_MISMATCH_DISPOSITION_OPEN
I6_SOURCE_EPOCH_PROJECT_OWNED: BLOCKED_BY_OWNER_DECISION
I7_RUN_LOCK_MUTATION_0: CURRENT_PRODUCT_EVIDENCE
I8_RUN_NETWORK_DEPENDENCY_RESOLUTION_0: CURRENT_PRODUCT_EVIDENCE
I9_HOST_ABSOLUTE_PATH_NON_SEMANTIC: CANDIDATE_AND_EXISTING_EVIDENCE
I10_UNCHANGED_CONTENT_DUPLICATION_0: PRODUCT_ONLY_GAP
I11_RUST_SEMANTIC_IDENTITY_AUTHORITY: PARTIAL_I1_FULL_PSC_OPEN
I12_BEGINNER_HIDES_INTERNAL_IDENTITY_MACHINERY: DEFERRED_PRESENTATION_NONBLOCKER
```

Editable I1 review status is now `PASS_WITH_FOLLOW_UP`, not pending. Its 10/10 reconfirmed
candidate evidence remains side-lineage evidence and is not adopted or duplicated here.
