# Project identity and storage graph

## Current product graph

```text
disk project
  ├─ 뿌리.ddn / ddn.project.json
  ├─ *.ddn
  ├─ vendor/**/gaji.toml
  ├─ ddn.lock
  └─ ddn.asset.json + dataset files
        │ collect_disk_project_files (UTF-8, broad metadata inclusion)
        ▼
VirtualProjectSource
        │ normalize_virtual_project_source
        ▼
NormalizedProjectManifest
  ├─ entry_path
  ├─ file SHA-256 identities
  ├─ project_json_sha256
  ├─ project_graph_sha256
  └─ lock_sha256
        │ build_project_prepare_link / build_project_run_summary
        ▼
linked execution source ──► DdnProgram ──► runtime result
```

```text
Workbench editor state
  ├─ every input ──► native project catalog / one-file draft (localStorage)
  ├─ explicit Save ──► JS snapshot artifact ──► HTTP service
  │                                      └─► SQLite revision/head
  │                                           └─► monolithic SHA-256 object
  ├─ server failure subset ──► local fallback snapshot (localStorage)
  ├─ portable import/export ──► experimental portable catalog (localStorage)
  └─ Run ──► in-memory source/recipe ──► WASM
             └─ optional server runs/checkpoints linked to a revision
```

## Target R2 identity graph

```text
AuthoredManifestIdentity (exact authored 차림새 bytes)
          │ parse/validate in Rust
          ├─ descriptive fields ──► presentation only
          └─ semantic fields
              ├─ first-entry role/path
              ├─ SourceEpoch / 글판
              ├─ dependency requirements
              ├─ declared 곳간 membership
              └─ execution-affecting config
                      │
                      ▼
           SemanticProjectConfigIdentity

source blobs ─────────────► SourceTreeIdentity
가지잠금 exact result ─────► DependencyLockIdentity
곳간 declared blobs ───────► ResourceSetIdentity

ProjectSnapshotIdentity = H(
  SourceTreeIdentity,
  SemanticProjectConfigIdentity,
  SourceEpochIdentity,
  DependencyLockIdentity?,
  ResourceSetIdentity
)
```

다음은 ProjectSnapshotIdentity에 포함하지 않는다: editor generation, saved revision number, cursor/UI, absolute host path, mtime, machine/user identity, cache/temp path, wall-clock time.

## State and storage ownership

| State | Identity owner | Durability | mutation trigger | forbidden coupling |
|---|---|---|---|---|
| EditorGeneration | editor session, monotonic counter | memory-first | character/input edit | SavedProjectRevision 생성 |
| RecoveryCheckpoint | recovery service/store | bounded local | debounce/explicit recovery policy | public revision number, semantic identity invention |
| SavedProjectRevision | project store HEAD CAS | durable | explicit Save/Restore | automatic Run increment |
| ExecutionSnapshot | Rust sealed envelope | immutable per run | Run after validation | later editor mutation, implicit lock update/network |

## Target CAS graph

```text
blob(hash, bytes)
  ▲        ▲       ▲
  │        │       └─ resource blobs
  │        └─ manifest authored bytes
  └─ source file blobs

small snapshot manifest
  ├─ normalized path -> blob hash
  ├─ semantic config identity
  ├─ source epoch identity
  ├─ dependency lock identity
  └─ resource membership -> blob hash

roots
  ├─ saved project revisions
  ├─ execution receipts
  ├─ replay records
  └─ retained recovery checkpoints
        │
        └─ mark reachable → collect unpinned objects
```

Full Git-like delta packing, distributed CAS, branch/merge/blame는 V1 blocker가 아니다.

## Transaction requirements

1. new blobs may be staged before the metadata transaction.
2. snapshot manifest, revision row, HEAD switch become visible in one atomic commit.
3. crash exposes old complete HEAD or new complete HEAD only.
4. staged but unreachable objects enter an explicit orphan ledger and are not treated as committed.
5. stale expected HEAD fails before new visible revision/reference.
6. execution envelope validates exact saved head and exact editor source before runtime.
7. GC never deletes objects pinned by saved revisions, receipts, replay, or retained recovery checkpoints.

## Authority migration rule

- Existing server store remains the SavedProjectRevision authority during migration.
- Browser local stores are recovery/compatibility surfaces, not co-equal semantic authorities.
- Editable I1 candidate may supply the saved-head/envelope slice only after targeted plain PASS and product-first integration review.
- `차림새`, `가지잠금`, `글판`, public snapshot wire are not fixed by this census.

## 2026-08-29 audited product/authority delta

Current product identity is not yet the target graph:

```text
disk crawl (all regular UTF-8 files)
  -> VirtualProjectSource(root_path, entry_path, files[])
  -> LocalProjectGraph(project_name, targets, module_paths, gaji_aliases, all files)
  -> project_graph_sha256
```

`project_name` is descriptive under candidate RD-452 but is currently hashed. Incidental
files discovered by recursive directory crawl are also hashed even when they are not declared
resources. Conversely, execution-affecting `ddn.project.json` policy is resolved by a different
CLI owner and is not projected into one typed ProjectSemanticConfiguration. These are product
architecture deltas, not permission to invent new fields.

The required successor graph is:

```text
ProjectSemanticConfigurationIdentity
  = SourceEpoch
  + effective entry/target path
  + logical module mapping
  + dependency requirements
  + declared resource membership
  + canonically classified execution-semantic configuration

ProjectExecutionSnapshotIdentity
  = logical source tree content identity
  + ProjectSemanticConfigurationIdentity
  + verified dependency resolution identity
  + declared resource content identity
```

Name/description/author/tags, host path, mtime, cache and Workbench state stay outside both
identities. Raw target labels are provenance unless they select different effective semantic
inputs.

Storage readiness remains split:

- `READY`: expected-head concurrent-save rejection (PUX26) as product policy;
- `READY_AFTER_V25_17_PROMOTION`: recovery is not saved authority, and Run is not Save;
- `BLOCKED_BY_SEMANTIC_GAP`: visible crash outcome and reopen mismatch disposition;
- `BLOCKED_BY_OWNER_DECISION`: declared directory/resource membership and SourceEpoch omission/migration.

No CAS table name, compression choice, cache layout, or private Rust type is a semantic blocker.

### Observable storage contract audit

| Operation | Product evidence | Authority completeness |
|---|---|---|
| atomic save | current object write is atomic and DB HEAD/revision update is transactional; I1 adds typed orphan candidate custody | multi-file/resource visible result `OLD_COMPLETE | NEW_COMPLETE`, never `HALF`, still needs SSOT clarification |
| reopen | current object read recomputes content hash; I1 rejects unknown local schema | one cross-surface decision for hash mismatch (fail closed versus separate recovery candidate) is still open |
| recovery | local recovery/checkpoint surfaces exist; server SavedProjectRevision remains separate | candidate RD-455 is sufficient if promoted: recovery never silently replaces saved HEAD; explicit Save is the durability transition |
| concurrent save | current server and I1 compare expected parent/HEAD and reject stale writer | exact product policy is ready; no last-writer, implicit merge, or retry fallback |
| Run versus Save | current/I1 can bind an immutable run snapshot without writing a revision | candidate RD-455 is sufficient if promoted; SavedRevision ordinal is provenance, not semantic execution identity |

Current browser-local recovery and server revision stores remain multiple physical stores. Until a
single typed authority projection is adopted, no UI label or fallback may silently promote local
recovery to server saved authority.
