# Current → PROJECT_UX_R2 delta matrix

| Area | CURRENT_BEHAVIOR | CURRENT_TEST | TARGET_R2 | 판정 | MIGRATION_IMPACT | PROPOSED_VERTICAL |
|---|---|---|---|---|---|---|
| single file | `lesson.ddn`/raw source may run without project | CLI/runtime and Workbench runners | arbitrary one `.ddn` runs | `ALIGNED` | default filename presentation only | FD03 tests |
| formal root | `뿌리.ddn` or `ddn.project.json` | local project graph/parity | `차림새` project config | `CONFLICT` | compatibility adapter required; mass rename forbidden | later manifest vertical |
| default entry | Workbench `lesson.ddn`; project root declares entry | project runners | newly created `처음.ddn`; role `첫글` authoritative | `PARTIAL` | creation UX and manifest writer change | later manifest vertical |
| entry non-magic | entry path is carried explicitly | graph/authoring tests | `처음.ddn` can be renamed | `ALIGNED` concept | rename/canon tests needed | D-PACK |
| semantic config identity | combined manifest hashes | local project Rust tests | semantic vs descriptive split | `MISSING` | new typed identity without public wire claim | FD03 |
| SourceEpoch | typed enum, API-chosen | lang V25 tests | project-owned `글판` | `MISSING` | no sniff; old projects explicit PreV25 compatibility | FD03 |
| lock | local candidate `ddn.lock.v0-local` | graph/CLI/WASM tests | 사용자 `가지잠금`, exact outcome | `PARTIAL` | keep physical wire candidate/open | later lock successor |
| Run mutation | lock read/compare only | project run tests | lock/update/network mutation 0 | `ALIGNED` | mutation proof consolidate | D-PACK |
| local dependencies | vendored `gaji.toml` recursive graph | gaji quality gates | relocation-invariant content/source identity | `PARTIAL` | path removed from semantic identity or explicitly scoped | FD03 tests |
| resources | explicit `ddn.asset.json` for sealed data; all disk metadata ingested | asset/project runners | explicit `곳간` membership | `PARTIAL` | binary blob model and ignore policy | FD02B |
| accidental OS files | `.DS_Store`/`Thumbs.db` enter metadata or may fail UTF-8 | no exact R2 case | ignored and identity-neutral | `CONFLICT` | bounded ignore policy | FD02B |
| path canonicalization | NFC, slash, duplicate and ASCII case collision guards | local_project Rust tests | portable NFC/case fail-closed | `ALIGNED` | add explicit D-PACK evidence | FD02B |
| editor generation | JS counters and input events | Workbench runners | typed memory-only generation | `PARTIAL` | name/identity owner in Rust envelope | FD02A |
| recovery | every-input localStorage rewrite | UI persistence tests | bounded RecoveryCheckpoint | `PARTIAL` | retention, crash recovery, explicit mode | FD02B |
| saved revision | explicit server Save + expected parent | project store/workbench tests | user save history | `ALIGNED` core | candidate adoption review | FD02A |
| execution snapshot | run freezes in-memory inputs; server archive points at revision | run prerequisite tests | exact analysis/run/saved input binding | `PARTIAL` | I1 candidate closes much, review pending | FD02A |
| JS identity | snapshot JS SHA-256; local fallback FNV candidate | snapshot tests | Rust semantic identity authority | `CONFLICT` | JS may transport but not invent semantic identity | FD02A |
| object model | monolithic snapshot object CAS | store tests | per-content blobs + small reference manifest | `PARTIAL` | schema migration candidate | FD02B |
| dedup | identical whole snapshot/checkpoint dedup | object store tests | file/resource-level dedup | `PARTIAL` | new object graph | FD02B |
| transaction | atomic replace + DB transaction; possible orphan file | failure tests | old or new complete snapshot only, orphan custody | `PARTIAL` | I1 orphan ledger candidate review | FD02A-B |
| stale concurrent save | expected-parent conflict | conflict runners | fail-closed | `ALIGNED` | preserve | FD02A regression |
| stale run | server run accepts any existing project revision, not exact current head | run prerequisite tests | current saved head + editor source exact | `MISSING` | I1 exact head binding candidate | FD02A |
| GC | no reachability GC | none | saved/receipt/replay roots pin; collect rest | `MISSING` | storage migration/operational policy | FD02B |
| portable | experimental v0 payload/catalog | portable tests | not stable authority | `LEGACY_AUTHORITY` | compatibility-only, no stable claim | keep isolated |
| Ttonimaru DB | separate project/revision/publication store | platform tests | not Workbench owner | `OUT_OF_V1` | do not converge in this program | none |

## Conflicts

1. 현행 formal root/manifest 이름과 R2의 `차림새` 모델.
2. Workbench JS-local identities와 Rust semantic authority 원칙.
3. accidental file ingestion and UTF-8-only disk collector versus explicit `곳간` membership.
4. run-time editable source versus saved server HEAD의 불완전 결속.
5. monolithic project snapshot versus file/resource CAS graph.

이 충돌은 bounded successor 설계로 해결 가능하다. 현재 배포된 public stable project/lock wire의 비가역 계약은 확인되지 않았으므로 Owner Gate A/B를 지금 발동하지 않는다. 실제 compatibility inventory에서 public contract가 발견되면 즉시 Owner Gate로 전환한다.

## Legacy authorities

- `뿌리.ddn` + `ddn.project.json` dual discovery.
- Workbench native/local fallback/portable localStorage project payloads.
- `seamgrim.project_snapshot.v0` monolithic snapshot.
- `ddn.lock.v0-local` local candidate physical format.
- PreV25 default single-file frontdoor.

기존 기능은 삭제하거나 일괄 rewrite하지 않는다.

## OPEN_BY_SSOT

- exact `차림새` schema, wire, field order and compatibility reader.
- exact public `가지잠금` schema/wire.
- `글판` manifest field and public diagnostic family.
- stable ProjectSnapshot/CAS graph wire.
- public V25 default and PreV25 removal.
- resource binary/public membership contract.

## FD02A impact classification

```yaml
ALREADY_IMPLEMENTED_IN_EDITABLE_I1_SIDE_CANDIDATE:
  - Rust typed editable source tree and canonical identity
  - exact saved server revision/content descriptor
  - stale current tree versus saved head rejection
  - analysis/execution source identity binding
  - candidate execution envelope and receipt tamper checks
  - expected-head server run creation
  - unknown local snapshot schema fail-closed
  - orphan-object candidate custody ledger
TEST_OR_DOCUMENT_EVIDENCE_ONLY:
  - Rust 5-case evidence claims
  - source mutation 12/12 claims
  - CLI/WASM A/B and Edge claims
  - no independent verdict commit after review parent
MISSING:
  - exact four-state R2 model
  - bounded recovery retention and GC
  - R2 semantic manifest/epoch/lock/resource identity composition
  - product-first adoption commit
REVIEW_DUE_TO_PROJECT_UX_R2:
  - source tree identity inputs
  - PreV25-only candidate boundary
  - local-only versus server-saved authority labels
  - receipt pin roots and FD02B GC interaction
PRODUCT_FIRST_ADOPTION_CONDITIONS:
  - fresh targeted plain PASS
  - primary-successor linear integration without side merge
  - R3N-FU01 overlap and source identity revalidation
  - candidate-only wire preserved
  - CLI/WASM/Workbench and fault parity at adopted fixed HEAD
```

## 2026-08-29 implementation-readiness re-audit

Authority was re-read immediately before this audit. Live authority remains internal SSOT
`v25.16.1` (`RD-001~451`) and public Language SPEC `v0.6.0`. The independently reviewed
v25.17 candidate is evidence only; v25.19 is neither current nor independently reviewed.

```yaml
V25_17_INDEPENDENT_REVIEW: PASS_BOUND_AS_CANDIDATE_ONLY
V25_17_CURRENT: false
V25_19_STATUS: NOT_CURRENT_PENDING_INDEPENDENT_REVIEW
EDITABLE_I1_REVIEW: PASS_WITH_FOLLOW_UP
EDITABLE_I1_ADOPTION_DISPOSITION: ADOPTABLE_WITH_TARGETED_CORRECTION
```

### ProjectSemanticConfiguration field/family classification

| Field/family | Classification | Exact audit result |
|---|---|---|
| SourceEpoch | `SEMANTIC_IDENTITY_INPUT` | RD-333~337 define epoch semantics; candidate RD-452 makes the formal project the owner. Product project owner is absent. |
| `첫글` / effective entry | `SEMANTIC_IDENTITY_INPUT` | changes linked source and execution snapshot. Current Rust checks payload/root/JSON entry equality. |
| dependency requirements | `SEMANTIC_IDENTITY_INPUT` | RD-452 project identity input; current `가지`/manifest requirements are split across local graph and lock. |
| verified resolved dependency reference | `SEMANTIC_IDENTITY_INPUT` | RD-453 execution-snapshot input, distinct from the requirements themselves. |
| logical module mapping | `SEMANTIC_IDENTITY_INPUT` | changes import resolution; current `모듈길` participates in `project_graph_sha256`. |
| declared non-code resource membership/content | `SEMANTIC_IDENTITY_INPUT` | RD-452/RD-453 require declared membership plus content identity. Current disk crawl is not that contract. |
| `age_target`, `det_tier`, `lang_mode`, execution-affecting seal/lock profile | `SEMANTIC_IDENTITY_INPUT` | current CLI consumes these fields, but no single PSC inventory/owner binds them across all frontdoors. |
| trace/observation configuration | `SEMANTIC_IDENTITY_INPUT` when it changes sealed observation/receipt; otherwise `PRODUCT_LOCAL` | exact split is an `UNKNOWN_BLOCKER`; implementer must not choose it field-by-field. |
| selected target/profile | `SEMANTIC_IDENTITY_INPUT` for effective target path and effective semantic profile; `PROVENANCE_ONLY` for a label that maps to identical effective inputs | current target label/path and standalone policy are not normalized by one owner. |
| project name, description, author, tags | `DESCRIPTIVE_NON_SEMANTIC` | candidate RD-452 is exact. Current `project_name` is incorrectly hashed. |
| Workbench layout, cursor, selection, viewport | `PRODUCT_LOCAL` | must not alter semantic project identity. |
| host path, mtime, cache, machine/user identity | `PRODUCT_LOCAL` | RD-453 excludes them from semantic identity. |
| historical `ddn.project.json` container | `LEGACY` | recognized fields require explicit semantic/descriptive migration; unknown fields must not silently enter identity. |
| `ssot_requires` / bundle hash as compatibility provenance | `PROVENANCE_ONLY` unless a supported product gate deliberately changes accepted execution | current `tool::project_meta` mixes them with execution gates; one PSC projection is missing. |
| current graph `root/entry/targets/module_paths/gaji_aliases/declared files` | `SEMANTIC_IDENTITY_INPUT` after canonical projection | current graph also includes non-semantic name and incidental files, which is a product correction. |
| current `package_hash` and unowned extra metadata | `UNKNOWN_BLOCKER` until explicitly classified or rejected | it is not a license to hash arbitrary fields. |

### Declared resource membership audit

| Question | Verdict | Current product / required target |
|---|---|---|
| membership authority | `CLOSED` at candidate meaning | an explicit project declaration owns membership; directory presence and source reference alone do not |
| all files in a folder automatically included | `SEMANTIC_GAP` in current product | current disk loader does this; target must not |
| explicit declaration | `CLOSED` at role level | exact spelling/schema is nonblocking, but one typed declaration owner is required |
| source reference as membership authority | `CLOSED` | no; a reference may consume a resource only after declaration |
| directory declaration recursion | `SEMANTIC_GAP` | whether directories are admitted and their recursion semantics require Owner selection |
| undeclared physical file | `CLOSED` at target meaning | identity-neutral and unavailable through declared-resource authority; current crawl violates this |
| declared-but-missing file | `FAILURE_GAP` until current authority | required target is fail-closed before execution snapshot/receipt commit |
| symlink/reparse point | `PRODUCT_POLICY_ONLY` | logical identity must remain project-relative; host escape is rejected, and current per-entry handling needs hardening |
| project-relative canonical path | `CLOSED` in product | `/` only, relative, NFC, no `.`/`..`, no absolute/URI path |
| NFC/NFD collision | `CLOSED` in product | duplicate normalized path fails |
| case portability collision | `CLOSED` in product | ASCII case-fold collision fails |
| duplicate logical declaration | `FAILURE_GAP` for future directory membership; otherwise `CLOSED` | current virtual paths reject duplicates; successor must also reject declaration aliasing |
| resource content change | `CLOSED` at candidate meaning | changes declared-resource-content identity and therefore execution snapshot |
| physical mutation during Run | `IDENTITY_GAP` until sealed capture is unified | a sealed snapshot must see captured bytes or fail; it may not mix pre/post-mutation bytes |

### Frontdoor/root discovery audit

| Surface | Current owner and behavior | Readiness finding |
|---|---|---|
| native `teul-cli run file.ddn` | separately walks upward for `ddn.project.json`; absent marker falls back to standalone defaults | not the local-project discovery owner |
| native project-run | walks ancestors for nearest `뿌리.ddn`; root beats JSON, legacy names fail | JSON-only discovery can be reported although disk source construction still requires `뿌리.ddn` |
| WASM project-run | caller supplies `VirtualProjectSource`, root, entry and files; Rust validates payload consistency | no shared host invocation-context discovery |
| Workbench | JS constructs the virtual project and passes caller-selected root/entry; Rust rejects internal entry conflicts | hidden/caller selection is not yet derived from a single PSC owner |
| standalone DDN | valid without a formal project; default age/mode paths differ by frontdoor | formal-project discovery must not silently capture or reinterpret it |

Detailed findings:

- parent traversal exists but uses different markers; a common nested-project stop rule is absent;
- `뿌리.ddn` plus legacy root is ambiguous/fail-closed; `뿌리.ddn` plus JSON only checks entry equality;
- caller entry versus root `첫글` conflicts fail closed in local project code;
- no marker is standalone for ordinary CLI, but project-run fails;
- `처음.ddn` has no current hidden product authority and candidate RD-456 makes it scaffold-only;
- same logical invocation context is therefore **not** guaranteed to select the same owner across
  CLI/WASM/Workbench.

### Nine-row readiness table

Five-axis cells are ordered `semantic role / surface / observable behavior / failure / identity`.

| Gap | Five-axis verdict | Existing owner ticket | PUX cases | Editable I1 impact | SSOT impact | Product reality | Readiness | Required next action |
|---|---|---|---|---|---|---|---|---|
| ProjectSemanticConfiguration field classification | `PARTIAL / PARTIAL / OPEN / OPEN / OPEN` | `DDN-P-V1-FD02A-PROJECT-UX-R2-ALIGNMENT-GAPS-R1` | PUX05, PUX09, PUX10, PUX30, PUX31 | `R2_RECHECK` | `SSOT_CLARIFICATION_REQUIRED` | graph hashes `project_name` and every crawled file; CLI policy fields have a separate owner | `BLOCKED_BY_SEMANTIC_GAP` | bind the exact execution-semantic field inventory and effective target/profile projection; then remove descriptive/incidental inputs |
| Declared resource membership | `CLOSED / OPEN / PARTIAL / OPEN / OPEN` | `DDN-P-V1-FD02B-SAVE-REOPEN-RECOVERY-CAS-R1` | PUX19-PUX23, PUX29 | `PRODUCT_GAP` | `NEW_OWNER_SEMANTIC_DECISION_REQUIRED` | disk loader recursively ingests every UTF-8 regular file; `ddn.asset.json` is only an asset registry, not whole-project membership | `BLOCKED_BY_OWNER_DECISION` | decide file-only versus directory declarations and, if directories exist, recursive/missing/duplicate semantics; keep undeclared files identity-neutral |
| Project root/frontdoor discovery | `PARTIAL / PARTIAL / OPEN / PARTIAL / OPEN` | FD02A alignment + FD03 ticket | PUX01, PUX04, PUX05, PUX29, PUX31 | `R2_RECHECK` | `SSOT_CLARIFICATION_REQUIRED` | local project-run walks for `뿌리.ddn`; standalone CLI walks for `ddn.project.json`; WASM/Workbench accept caller-built virtual trees | `BLOCKED_BY_SEMANTIC_GAP` | define one invocation-context algorithm, nested-root stop rule, marker absence fallback, and caller/manifest conflict rule |
| Project-owned SourceEpoch declaration/default/migration | `CLOSED / OPEN / OPEN / PARTIAL / CLOSED` | `DDN-P-V1-FD03-PROJECT-OWNED-SOURCE-EPOCH-R1` | PUX04, PUX06-PUX08, PUX29-PUX32 | `SEMANTIC_BLOCKED` | `NEW_OWNER_SEMANTIC_DECISION_REQUIRED` | supported/unknown epoch meaning exists, but formal-project omission, legacy omission, new-project default and standalone policy are unbound | `BLOCKED_BY_OWNER_DECISION` | approve the exact formal/legacy/standalone state matrix; no sniffing or hidden default |
| Save atomicity | `PARTIAL / NONBLOCKING / OPEN / OPEN / PARTIAL` | `DDN-P-V1-FD02B-SAVE-REOPEN-RECOVERY-CAS-R1` | PUX23, PUX25 | `PARTIAL` | `SSOT_CLARIFICATION_REQUIRED` | current store uses atomic object write plus DB transaction; I1 adds orphan custody, but R2 multi-file/resource visibility contract is not current authority | `BLOCKED_BY_SEMANTIC_GAP` | bind `OLD_COMPLETE | NEW_COMPLETE`, forbid visible `HALF`, and specify orphan visibility before implementation |
| Reopen validation | `PARTIAL / NONBLOCKING / OPEN / OPEN / PARTIAL` | FD02B ticket | PUX24, PUX33 | `PARTIAL` | `SSOT_CLARIFICATION_REQUIRED` | object hash and unknown local schema can fail closed, but mismatch disposition across saved/recovery surfaces is not one authority | `BLOCKED_BY_SEMANTIC_GAP` | bind fail-closed versus separate recovery-candidate behavior; forbid silent repair/continue |
| Recovery authority | `CLOSED / NONBLOCKING / CLOSED / CLOSED / CLOSED` | FD02B ticket | PUX25, PUX34, PUX35 | `PARTIAL` | `V25_17_ALREADY_SUFFICIENT_IF_PROMOTED` | RD-455 separates recovery from saved authority; UI/retention remain product policy | `READY_AFTER_V25_17_PROMOTION` | present recovery as a non-authoritative candidate; only explicit successful Save creates a durable revision |
| Concurrent save | `CLOSED / NONBLOCKING / CLOSED / CLOSED / CLOSED` | FD02B ticket | PUX26 | `ALREADY_IMPLEMENTED` | `PRODUCT_POLICY_ONLY` | current server and I1 use expected-head CAS and reject stale writer; no merge/last-writer fallback | `READY` | preserve expected-head fail-closed behavior and independently revalidate at the adopted fixed head |
| Run-vs-Save separation | `CLOSED / NONBLOCKING / CLOSED / CLOSED / CLOSED` | FD02A alignment + FD02B ticket | PUX02, PUX03, PUX22, PUX30 | `PARTIAL` | `V25_17_ALREADY_SUFFICIENT_IF_PROMOTED` | I1 seals an immutable execution snapshot; R2 composite inputs remain absent | `READY_AFTER_V25_17_PROMOTION` | preserve Run write-count 0 for saved revision/lock and bind the full snapshot identity after promotion |

```yaml
IMPLEMENTATION_READY_COUNT: 1
READY_AFTER_V25_17_COUNT: 2
SEMANTIC_BLOCKER_COUNT: 4
OWNER_DECISION_REQUIRED_COUNT: 2
PRODUCT_ONLY_GAP_COUNT: 0
DEFERRED_NONBLOCKER_COUNT: 0
READINESS_ROW_BIJECTION: 9/9
```
