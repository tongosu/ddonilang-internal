# D-PACK Project UX R2 — 35-case physicalization ledger

Every designed case is assigned exactly once. `PRODUCT_EVIDENCE` means a current product runner/test directly exercises the core case, not that R2 naming or public wire is closed. `TEST_ONLY` includes adjacent unit/side-lineage evidence. `LOGICAL_ORACLE` has a precise expected relation but no exact current product runner. `UNSUPPORTED` requires a missing product capability.

| ID | Class | Exact existing evidence / command | Expected evidence |
|---|---|---|---|
| PUX01 | PRODUCT_EVIDENCE | `python tests/run_ddn_local_project_cli_wasm_parity_check.py`; `python tests/run_ddn_local_project_workbench_multifile_check.py` | original single-file source accepted through current product frontdoors; no forced formal project |
| PUX02 | LOGICAL_ORACLE | census oracle only; I1 JS checker is adjacent, not a keystroke counter | 100 EditorGenerations, durable revisions +0 |
| PUX03 | TEST_ONLY | at `d0ff2338...`: `python tests/run_v1_editable_workbench_revision_custody_i1_product_check.py` | run envelope remains bound to snapshot A after edit B; side candidate pending review |
| PUX04 | UNSUPPORTED | no current `처음.ddn + 차림새` creator runner | one complete formal-project revision; no hidden files |
| PUX05 | TEST_ONLY | `cargo test -p ddonirang-tool local_project`; graph fixtures with non-default `entry_path` | explicit entry wins; filename magic does not |
| PUX06 | TEST_ONLY | at `d0ff2338...`: `python tests/run_v1_fd01a_internal_source_epoch_check.py` | internal SourceEpoch mapping only; project-owned 글판 absent |
| PUX07 | UNSUPPORTED | no project-owned unknown-글판 product case | exact fail-closed diagnostic, no fallback |
| PUX08 | TEST_ONLY | at `d0ff2338...`: `python tests/run_v1_editable_workbench_revision_custody_i1_source_fault_injection.py` | epoch/source mismatch RED with writes 0 |
| PUX09 | LOGICAL_ORACLE | census identity comparison oracle | descriptive edit changes authored manifest/revision, not execution identity |
| PUX10 | LOGICAL_ORACLE | census identity comparison oracle | first-entry semantic edit changes config/snapshot identity |
| PUX11 | PRODUCT_EVIDENCE | `python tests/run_ddn_local_project_graph_check.py` | dependency-free project runs without an empty lock requirement |
| PUX12 | PRODUCT_EVIDENCE | same graph runner, missing-lock fixture | fail closed; no automatic resolution |
| PUX13 | PRODUCT_EVIDENCE | same graph runner, tampered/mismatched lock fixtures | fail closed; no best-effort run |
| PUX14 | TEST_ONLY | `python tests/run_ddn_local_project_graph_check.py`, generated-lock fixture | explicit update produces complete new lock; current evidence is not R2 transaction proof |
| PUX15 | TEST_ONLY | same runner's lock negative fixtures | invalid update rejected; exact phase fault injection still absent |
| PUX16 | PRODUCT_EVIDENCE | `python tests/run_ddn_local_project_cli_wasm_parity_check.py` and graph locked-project cases | locked Run succeeds without dependency-provider lookup |
| PUX17 | PRODUCT_EVIDENCE | same runner with fixture hash comparisons | Run does not mutate lock bytes/hash |
| PUX18 | TEST_ONLY | local-project canonicalization tests; R3N clean A/B is adjacent artifact evidence | checkout-relative project identity; exact R2 relocation pack pending |
| PUX19 | LOGICAL_ORACLE | census manifest/blob membership oracle | only explicitly declared 곳간 files enter identity |
| PUX20 | UNSUPPORTED | no `.DS_Store`/`Thumbs.db` product runner | metadata files ignored without broad directory sniffing |
| PUX21 | LOGICAL_ORACLE | this preflight's isolated measurement is RED baseline | same large resource should occupy one CAS blob; current literal count is 2 |
| PUX22 | LOGICAL_ORACLE | this preflight creates 100 archive rows against one source object | source blob +0; actual runtime Run×100 remains unexecuted |
| PUX23 | LOGICAL_ORACLE | this preflight save A/B measurement | target requires one changed file blob only; current whole snapshot duplicates unchanged resource |
| PUX24 | PRODUCT_EVIDENCE | `python tests/run_seamgrim_project_save_reopen_check.py`; direct isolated store reopen measurement | exact head/content identity on reopen; browser wrapper presently environment-RED |
| PUX25 | TEST_ONLY | at `d0ff2338...`: product checker and source fault-injection runner | I1 orphan-candidate/atomicity evidence; independent verdict pending |
| PUX26 | PRODUCT_EVIDENCE | `python tests/run_seamgrim_project_revision_conflict_restore_check.py`; direct isolated stale-CAS measurement | second writer rejected; visible/object changes 0 |
| PUX27 | PRODUCT_EVIDENCE | `cargo test -p ddonirang-tool local_project` | NFC/NFD collision rejected |
| PUX28 | PRODUCT_EVIDENCE | same Rust test family | case-only portability collision rejected |
| PUX29 | TEST_ONLY | local-project path normalization tests and R3N relocated candidate A/B/C | host root excluded; exact R2 project snapshot A/B pending |
| PUX30 | TEST_ONLY | at `d0ff2338...`: product checker + source fault injection | analysis A / execution B mismatch fails closed |
| PUX31 | TEST_ONLY | at `d0ff2338...`: WASM parity + source fault injection | Rust recomputes and rejects forged JS identity |
| PUX32 | LOGICAL_ORACLE | census diagnostic oracle; no exact touched-workflow runner | exact current type terminology and writes 0 |
| PUX33 | TEST_ONLY | at `d0ff2338...`: `node tests/run_v1_editable_workbench_revision_custody_i1_js_check.mjs` | unknown local schema fail closed; side candidate pending review |
| PUX34 | UNSUPPORTED | no bounded recovery-retention product schema/runner | prune only oldest unpinned recovery nodes |
| PUX35 | UNSUPPORTED | no reachability GC implementation/runner | saved/receipt/replay/recovery roots retained; unreachable only removed |

```yaml
DPACK_TOTAL: 35
PRODUCT_EVIDENCE_COUNT: 10
PRODUCT_EVIDENCE: [PUX01, PUX11, PUX12, PUX13, PUX16, PUX17, PUX24, PUX26, PUX27, PUX28]
TEST_ONLY_COUNT: 12
TEST_ONLY: [PUX03, PUX05, PUX06, PUX08, PUX14, PUX15, PUX18, PUX25, PUX29, PUX30, PUX31, PUX33]
LOGICAL_ORACLE_COUNT: 8
LOGICAL_ORACLE: [PUX02, PUX09, PUX10, PUX19, PUX21, PUX22, PUX23, PUX32]
UNSUPPORTED_COUNT: 5
UNSUPPORTED: [PUX04, PUX07, PUX20, PUX34, PUX35]
CLASSIFICATION_BIJECTION: 35/35
NEW_TEST_OR_FIXTURE_ADDED: 0
```

The Playwright-dependent PUX24/PUX26 wrappers were attempted but could not start because this isolated worktree has no local Playwright package. Their classification derives from existing product runners plus direct isolated server-store measurements, not a newly claimed browser PASS.

## 2026-08-29 readiness annotation

The physicalization counts above remain unchanged. This annotation adds semantic readiness and
does not convert logical/test-only evidence into product evidence.

| Gap | Existing PUX IDs | Readiness |
|---|---|---|
| PSC fields | 05, 09, 10, 30, 31 | `BLOCKED_BY_SEMANTIC_GAP` |
| resource membership | 19-23, 29 | `BLOCKED_BY_OWNER_DECISION` |
| root/frontdoor discovery | 01, 04, 05, 29, 31 | `BLOCKED_BY_SEMANTIC_GAP` |
| project SourceEpoch | 04, 06-08, 29-32 | `BLOCKED_BY_OWNER_DECISION` |
| save atomicity | 23, 25 | `BLOCKED_BY_SEMANTIC_GAP` |
| reopen validation | 24, 33 | `BLOCKED_BY_SEMANTIC_GAP` |
| recovery authority | 25, 34, 35 | `READY_AFTER_V25_17_PROMOTION` |
| concurrent save | 26 | `READY` |
| Run-vs-Save | 02, 03, 22, 30 | `READY_AFTER_V25_17_PROMOTION` |

Editable I1 is now independently `PASS_WITH_FOLLOW_UP`; the fixed-head evidence remains a
side-lineage overlay and still does not change any class/count in this ledger. Its actual Edge
reproduction remains OPEN.
