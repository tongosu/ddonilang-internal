# FD02A Editable I1 impact matrix

## Custody boundary

```yaml
EDITABLE_I1_FIXED_HEAD: d0ff23389e27b8268fe9eead8d0138abd6d77b06
EDITABLE_I1_REVIEW_PARENT: 2d489c8d9b2651f5314afdfa4a453568622dfbfd
LINEAGE_USE: READ_ONLY_EVIDENCE
PRODUCT_FIRST_ADOPTION: NO
INDEPENDENT_PASS: NO
DUPLICATE_IMPLEMENTATION: FORBIDDEN
```

Tracked test/evidence가 존재한다는 사실과 그 실행 결과가 독립검토로 승인됐다는 주장을 구분한다. 아래 `TEST_EVIDENCE`는 fixed head에 존재하는 runner 또는 Rust test다.

## A. 이미 구현된 FD02A 요구

### A1. Typed editable source tree와 canonical identity

```yaml
REQUIREMENT: editable source tree를 Rust가 정규화하고 canonical identity를 계산
EXACT_PATH: tool/src/source_epoch.rs
EXACT_SYMBOL: EditableSourceTreeCandidate; normalized_source_tree; source_tree_sha256; raw_source_tree_sha256
FIXED_HEAD: d0ff23389e27b8268fe9eead8d0138abd6d77b06
TEST_EVIDENCE: source_epoch::tests::editable_revision_server_saved_positive_is_deterministic; editable_revision_lf_and_uniform_crlf_have_one_canonical_tree_identity
PROJECT_UX_R2_ALIGNMENT: PARTIAL — current tree는 R2 차림새/글판/가지잠금/곳간 합성 identity를 아직 소유하지 않음
```

### A2. Saved server HEAD descriptor

```yaml
REQUIREMENT: project/revision/content identity를 exact saved-head descriptor로 전달
EXACT_PATH: solutions/seamgrim_ui_mvp/tools/ddn_exec_server.py
EXACT_SYMBOL: project_response_from_record; editable_revision_descriptor_candidate
FIXED_HEAD: d0ff23389e27b8268fe9eead8d0138abd6d77b06
TEST_EVIDENCE: tests/run_v1_editable_workbench_revision_custody_i1_product_check.py
PROJECT_UX_R2_ALIGNMENT: ALIGNED_WITH_CANDIDATE_BOUNDARY
```

### A3. Server snapshot wrapper 재계산

```yaml
REQUIREMENT: JS wrapper canonical bytes/hash를 server가 재계산하고 불일치를 거부
EXACT_PATH: solutions/seamgrim_ui_mvp/tools/project_store.py
EXACT_SYMBOL: SeamgrimProjectStore._artifact_parts
FIXED_HEAD: d0ff23389e27b8268fe9eead8d0138abd6d77b06
TEST_EVIDENCE: run_v1_editable_workbench_revision_custody_i1_product_check.py; mutation M10_wrapper_canonical_split
PROJECT_UX_R2_ALIGNMENT: ALIGNED — JS semantic claim을 그대로 신뢰하지 않음
```

### A4. Unsaved editor source와 saved HEAD 불일치 차단

```yaml
REQUIREMENT: saved server source tree와 current editable source tree가 다르면 Run fail-closed
EXACT_PATH: tool/src/source_epoch.rs
EXACT_SYMBOL: build_editable_revision_execution_envelope; E_EDITABLE_SERVER_HEAD_STALE
FIXED_HEAD: d0ff23389e27b8268fe9eead8d0138abd6d77b06
TEST_EVIDENCE: editable_revision_adversarial_24_case_ledger_fails_closed; mutation M05_saved_head_tree
PROJECT_UX_R2_ALIGNMENT: ALIGNED core, but R2 semantic config inputs require recheck
```

### A5. Analysis/run same-snapshot binding

```yaml
REQUIREMENT: readiness analysis revision과 execution entry source가 동일해야 함
EXACT_PATH: tool/src/source_epoch.rs
EXACT_SYMBOL: build_editable_revision_execution_envelope; analysis_snapshot_identity; E_EDITABLE_ANALYSIS_REVISION_MISMATCH
FIXED_HEAD: d0ff23389e27b8268fe9eead8d0138abd6d77b06
TEST_EVIDENCE: editable_revision_adversarial_24_case_ledger_fails_closed; mutation M06_analysis_revision
PROJECT_UX_R2_ALIGNMENT: PARTIAL — entry source는 묶지만 project-owned 글판/config identity가 없음
```

### A6. Server run current-head gate

```yaml
REQUIREMENT: run archive 생성 시 expected saved HEAD와 current project HEAD를 비교
EXACT_PATH: solutions/seamgrim_ui_mvp/tools/project_store.py; solutions/seamgrim_ui_mvp/tools/ddn_exec_server.py
EXACT_SYMBOL: SeamgrimProjectStore.create_run(expected_head_revision_id); handle_project_post
FIXED_HEAD: d0ff23389e27b8268fe9eead8d0138abd6d77b06
TEST_EVIDENCE: run_v1_editable_workbench_revision_custody_i1_product_check.py; mutation M11_run_saved_head_gate
PROJECT_UX_R2_ALIGNMENT: ALIGNED saved revision slice
```

### A7. Prepared envelope와 execution receipt tamper binding

```yaml
REQUIREMENT: execution envelope/receipt가 exact source, analysis, graph, state identities를 봉인
EXACT_PATH: tool/src/source_epoch.rs; tool/src/wasm_api.rs
EXACT_SYMBOL: editable_revision_execution_envelope_json; editable_revision_execution_receipt_json; wasm_editable_revision_execution_*_candidate_json
FIXED_HEAD: d0ff23389e27b8268fe9eead8d0138abd6d77b06
TEST_EVIDENCE: editable_revision_receipt_binds_envelope_execution_and_durability; mutation M09_receipt_envelope_tamper; run_v1_editable_workbench_revision_custody_i1_wasm_parity.mjs
PROJECT_UX_R2_ALIGNMENT: PARTIAL — internal candidate identity only, stable/public claim 없음
```

### A8. Workbench가 shared RuntimeBridge candidate를 사용

```yaml
REQUIREMENT: alternate JS runtime 없이 Workbench → RuntimeBridge → WASM Rust path 사용
EXACT_PATH: solutions/seamgrim_ui_mvp/ui/runtime/runtime_bridge.js; solutions/seamgrim_ui_mvp/ui/workbench/workbench.js
EXACT_SYMBOL: prepareEditableRevisionCandidate; finalizeEditableRevisionCandidate; prepareEditableRevisionCustodyCandidate; buildEditableRevisionReceipt
FIXED_HEAD: d0ff23389e27b8268fe9eead8d0138abd6d77b06
TEST_EVIDENCE: run_v1_editable_workbench_revision_custody_i1_js_check.mjs; run_v1_editable_workbench_revision_custody_i1_wasm_parity.mjs
PROJECT_UX_R2_ALIGNMENT: ALIGNED architecture, independent review pending
```

### A9. Local schema fail-closed와 explicit fallback

```yaml
REQUIREMENT: unknown local snapshot schema를 숨은 migration으로 수용하지 않음
EXACT_PATH: solutions/seamgrim_ui_mvp/ui/workbench/persistence/local_fallback.js; solutions/seamgrim_ui_mvp/ui/workbench/workbench.js
EXACT_SYMBOL: migrateApprovedLocalSnapshot; saveProjectSnapshot
FIXED_HEAD: d0ff23389e27b8268fe9eead8d0138abd6d77b06
TEST_EVIDENCE: run_v1_editable_workbench_revision_custody_i1_js_check.mjs; mutation M12_unknown_local_schema
PROJECT_UX_R2_ALIGNMENT: PARTIAL — authority mode UX와 bounded recovery는 FD02B
```

### A10. Orphan object custody

```yaml
REQUIREMENT: object-file 선행 write 실패/중단을 explicit candidate ledger로 관찰
EXACT_PATH: solutions/seamgrim_ui_mvp/tools/project_store.py
EXACT_SYMBOL: orphan_object_candidates; _stage_object_candidate; _clear_object_candidate; orphan_object_custody_receipt
FIXED_HEAD: d0ff23389e27b8268fe9eead8d0138abd6d77b06
TEST_EVIDENCE: run_v1_editable_workbench_revision_custody_i1_product_check.py
PROJECT_UX_R2_ALIGNMENT: PARTIAL — reachability GC와 recovery root policy는 없음
```

## B. 테스트·문서 근거만 존재하는 요구

| REQUIREMENT | EVIDENCE_KIND | EXACT_EVIDENCE | 판정 |
|---|---|---|---|
| actual Edge browser path | runner + manager result claim | `tests/run_v1_editable_workbench_revision_custody_i1_edge.mjs`; `IMPLEMENTATION_RESULT.md` | `EVIDENCE_ONLY_NEEDS_INDEPENDENT_REPRODUCTION` |
| clean A/B native/WASM byte parity | runner + manager claim | `run_v1_editable_workbench_revision_custody_i1_wasm_parity.mjs` | `EVIDENCE_ONLY_NEEDS_INDEPENDENT_REPRODUCTION` |
| source mutation 12/12 residue 0 | mutation runner + manager claim | `run_v1_editable_workbench_revision_custody_i1_source_fault_injection.py` | `EVIDENCE_ONLY_NEEDS_INDEPENDENT_REPRODUCTION` |
| visual UI change 0 | manager/handoff claim | Editable I1 handoff documents | `DOC_ONLY`; not a product requirement closure |
| R2 35-case project UX pack | this census design | `06_DPACK_PROJECT_UX_R2.md` | `DESIGN_ONLY_FUTURE_TEST` |
| independent PASS | review request only | `2d489c8d...` review parent | `MISSING_VERDICT` |

## C. 아직 누락된 요구

| Requirement | Current fact | Status | Follow-up |
|---|---|---|---|
| typed four-state model | generation/revision/envelope pieces only | `MISSING` | FD02A contract + FD02B recovery |
| R2 semantic 차림새 identity | current local tree manifest only | `MISSING` | FD03 |
| project-owned 글판 selection | candidate is fixed PreV25-only | `MISSING` | FD03 |
| 가지잠금 identity in execution snapshot | current prepare may carry local lock hash; exact R2 composition absent | `MISSING` | FD03/lock successor |
| 명시 곳간 membership in snapshot identity | sealed dataset support only | `MISSING` | FD02B/resource successor |
| bounded RecoveryCheckpoint retention | browser best-effort current value only | `MISSING` | FD02B |
| per-file/resource CAS dedup | monolithic snapshot object | `MISSING` | FD02B |
| reachability GC with saved/receipt/replay roots | row caps only | `MISSING` | FD02B |
| `처음.ddn` non-magic + 차림새 `첫글` authority | current `뿌리.ddn`/entry_path | `MISSING` | FD03/manifest successor |

## D. PROJECT_UX_R2 때문에 재검토할 부분

| Recheck | Why | Required evidence |
|---|---|---|
| `처음.ddn` non-magic | I1 carries current entry path, not R2 default/role contract | rename and alternate entry fixtures |
| `첫글` owner | entry must be semantic config, not filename/UI selection | Rust manifest authority proof |
| 차림새 vs editor state | editor/presentation fields must not change execution identity | descriptive/semantic mutation pair |
| 글판 authority | I1 hard-pins PreV25 candidate | project-owned mapping and unknown/mismatch RED |
| 가지잠금 | saved tree equality alone does not prove resolved lock equality | lock identity in envelope and mutation proof |
| 곳간 membership | broad file tree may include undeclared assets | explicit membership/blob ledger |
| absolute path leakage | canonical tree/path checks need clean relocated A/B | checkout relocation and binary scan |
| save/reopen identity | candidate descriptor must survive restart/reopen | server restart and byte identity |
| analysis/run same snapshot | source check must include semantic config/epoch/lock/resources | multi-component mismatch attacks |
| storage growth/dedup | I1 does not implement file blob graph/GC | Run×100 and one-file-edit object counts |
| Rust authority | JS must only transport all new R2 identities | forged JS identity attacks through real Workbench |

## E. product-first 계보 채택 조건

| Condition | Status | Evidence / unblock condition |
|---|---|---|
| `CODE_EXISTS` | `PASS` | product diff exists at `d0ff2338...` |
| `TEST_EVIDENCE_EXISTS` | `PASS` | tracked Rust/Python/JS/WASM/Edge runners exist |
| `MANAGER_REPRODUCTION` | `OPEN` | manager claim exists, but this census did not rerun or bind it to primary successor |
| `INDEPENDENT_REVIEW` | `BLOCKED` | review parent exists; verdict commit absent |
| `PROJECT_UX_R2_ALIGNMENT` | `OPEN` | core custody aligns; R2 manifest/epoch/lock/resource composition missing |
| `NO_AUTHORITY_CONFLICT` | `OPEN` | candidate PreV25-only and current multi-store authority need explicit adoption mapping |
| `NO_WIP_CONFLICT` | `OPEN` | primary product-first successor and active review/worktree ownership must be audited at adoption time |

```yaml
EDITABLE_I1_STATUS: ALREADY_IMPLEMENTED_CANDIDATE
EDITABLE_I1_INDEPENDENT_REVIEW_STATUS: PENDING_NO_VERDICT_COMMIT
FD02A_PRODUCT_FIRST_ADOPTION: BLOCKED_PENDING_PLAIN_PASS_AND_ALIGNMENT
FD02A_NEW_IMPLEMENTATION: FORBIDDEN
```

## 2026-08-29 review-bound correction

The preceding pending-review block is historical. It is superseded, not rewritten, by the
independent artifact at review commit `2d2bce5fd1bcb9fc5c864f210b15f7a5c4391747`.

```yaml
EDITABLE_I1_FIXED_PRODUCT_HEAD: d0ff23389e27b8268fe9eead8d0138abd6d77b06
EDITABLE_I1_REVIEW_PARENT: 2d489c8d9b2651f5314afdfa4a453568622dfbfd
EDITABLE_I1_REVIEW_COMMIT: 2d2bce5fd1bcb9fc5c864f210b15f7a5c4391747
EDITABLE_I1_REVIEW: PASS_WITH_FOLLOW_UP
EDITABLE_I1_ADOPTION_DISPOSITION: ADOPTABLE_WITH_TARGETED_CORRECTION
EDITABLE_I1: ALREADY_IMPLEMENTED_CANDIDATE_NOT_ADOPTED
EDITABLE_I1_DUPLICATED: false
```

The independent review reconfirmed A1-A10 (`10/10`), but did not issue plain PASS or an
adoption commit. Adoption readiness must retain all four targeted corrections:

1. independently reproduce the actual Edge workflow;
2. require LF-forced `-c core.autocrlf=false --detach <fixed-head>` WASM reproduction;
3. unify `CanonicalCandidate` with `SourceRemapMode candidate` before adopting the build script;
4. route the seven R2 missing axes rather than silently pulling them into FD02A:
   - FD03: non-magic entry, `첫글`, semantic/descriptive configuration split, project-owned SourceEpoch;
   - FD02B: declared resource membership, per-file CAS/growth/dedup;
   - FD02A/FD02B shared: full analysis/run composite identity.

Impact classes after the re-audit:

| Area | Class | Disposition |
|---|---|---|
| I1 typed editable identity/envelope/receipt | `ALREADY_IMPLEMENTED` | reuse only after targeted corrections and product-first linear adoption decision |
| actual Edge evidence | `EVIDENCE_ONLY` | OPEN; implementation claim is not inherited |
| full PSC field inventory and frontdoor owner | `R2_RECHECK` | semantic clarification first |
| project-owned SourceEpoch omission/migration | `SEMANTIC_BLOCKED` | FD03 Owner decision |
| declared resource membership/per-file CAS | `PRODUCT_GAP` plus semantic declaration decision | FD02B |
| save/reopen mismatch and crash visibility | `PARTIAL` | FD02B semantic clarification plus product vertical |

No merge, cherry-pick, rebase, or duplicate implementation occurred in this re-audit.
