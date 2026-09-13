# 저장소 project custody A-Z census

각 row는 primary baseline `6824ef7c...`의 제품 사실이다. Editable I1 side 후보는 별도 impact matrix에만 기록한다.

| ID | 판정 | EXACT_PATH / EXACT_SYMBOL | caller → callee | CURRENT_BEHAVIOR / TEST | TARGET_R2 / DELTA / PROPOSED_VERTICAL |
|---|---|---|---|---|---|
| A discovery/root | `CONFLICT` | `tool/src/local_project.rs`; `discover_project_root*`, `PROJECT_ROOT_FILE`, `PROJECT_JSON_FILE` | CLI/WASM → discovery → disk/virtual source | `뿌리.ddn` 우선, `ddn.project.json` fallback, legacy roots reject; local project runners | `차림새`가 root config, `처음.ddn`은 non-magic; compatibility migration / FD03 이후 project manifest vertical |
| B manifest/config | `PARTIAL` | `tool/src/local_project.rs`; `NormalizedProjectManifest`, `extract_ddn_first_entry`, `extract_project_json_entry` | normalize → root/json entry → manifest hash | entry/graph/lock/file identity 결속, descriptive/semantic split 없음 | `AuthoredManifestIdentity`와 `SemanticProjectConfigIdentity` 분리 / FD03 |
| C single-file | `ALIGNED` | `tools/teul-cli/src/cli/run.rs`, `tool/src/ddn_runtime.rs::DdnProgram::from_source*` | teul-cli run → runtime parse/execute | project 없이 한 `.ddn` 실행; default PreV25 | 계속 지원; 글판 selection은 explicit / FD03 |
| D SourceEpoch | `MISSING` | `lang/src/ast.rs::SourceEpoch`; project owner 없음 | parser entry API가 enum 선택 | `PreV25`, `V25` typed enum은 있으나 project 저장/selection 없음; `lang/tests/v25_definition_binding_pack.rs` | 차림새 `글판` → exact enum, unknown fail-closed / FD03 |
| E parser/AST/canon | `ALIGNED` | `lang/src/lib.rs::{parse_with_mode,parse_v25_with_mode}`, `lang/src/ast.rs::CanonProgram.source_epoch` | runtime → parser → canonicalizer | epoch가 AST/canon에 보존 | project-provided epoch를 이 existing path에 공급 / FD03 |
| F CLI epoch/project | `PARTIAL` | `tools/teul-cli/src/main.rs::{ProjectDiscover,ProjectGraph,ProjectLock,ProjectRun}` | CLI → `local_project` Rust | project frontdoor 공유; single run의 epoch는 별도 API | project-owned 글판과 one-file default contract 필요 / FD03 |
| G WASM epoch/project | `PARTIAL` | `tool/src/wasm_api.rs::wasm_*project*_json` | JS RuntimeBridge → WASM → Rust local_project | normalize/discover/graph/edit/lock/prepare/run exports 존재 | exact same snapshot+epoch envelope 필요 / FD02A, FD03 |
| H RuntimeBridge | `PARTIAL` | `solutions/seamgrim_ui_mvp/ui/runtime/runtime_bridge.js::RuntimeBridge` | Workbench → RuntimeBridge → WASM adapter | authoritative queries 사용, Editable custody exports는 primary에 없음 | I1 candidate exports 재검토/채택 / FD02A |
| I Workbench lifecycle | `CONFLICT` | `solutions/seamgrim_ui_mvp/ui/workbench/workbench.js::{syncNativeProjectFromState,startRun,saveProjectSnapshot,reopenProjectSnapshot}` | editor events → localStorage; save → project adapter; run → WASM/archive | every input local catalog write, explicit server save, Run은 auto-save 안 함, server failure 일부 local fallback | four-state model, explicit authority mode, saved-head execution / FD02A-B |
| J dependency resolver | `PARTIAL` | `tool/src/local_project.rs::{collect_gaji_dependencies,build_project_gaji_lock}` | project graph → vendored manifests → lock | vendored local transitive graph, deterministic sort/hash | dependency logical/source/content identity retain / FD03/lock successor |
| K local dependency | `ALIGNED` | `LocalGajiPin::{path,manifest_sha256,package_sha256}` | `gaji.toml` graph → pin | relative vendored path + hashes | checkout relocation proof 강화 / D-PACK |
| L external dependency | `OPEN_BY_SSOT` | `tools/teul-cli/src/cli/gaji.rs`, registry index inputs | explicit gaji command → local registry index/vendor | external metadata is file input; project Run path와 분리 | public resolver/wire/network policy not finalized / later program |
| M lock schema | `OPEN_BY_SSOT` | `tool/src/local_project.rs::{LocalGajiLock,build_project_gaji_lock}` | graph → canonical `ddn.lock` compare | schema `ddn.local_gaji_lock.v0`, `lock_format=ddn.lock.v0-local`; mismatch/missing fail closed | 사용자명 가지잠금, stable fields OPEN / later lock authority |
| N dependency identity | `PARTIAL` | `LocalGajiPin`, `LocalGajiLock::{project_graph_sha256,lock_sha256}` | manifests/files → SHA-256 graph | version, path, transitive deps, manifest/package hashes | absolute/machine/time 제외를 mutation으로 봉인 / D-PACK |
| O network/update | `ALIGNED` Run / `PARTIAL` UX | project run Rust; `tools/teul-cli/src/cli/gaji.rs::run_update_with_options` | Run → vendored read only; explicit CLI update → output | Run network/update 0; update is distinct CLI mutation | `가지 맞추기` atomic UX와 explicit user action / later vertical |
| P asset membership | `PARTIAL` | `ddn.asset.json`; `project_asset_registry_from_source`, `ProjectAssetRegistry` | source → asset registry → sealed datasets | explicit manifest for sealed datasets, but disk collector admits all metadata and only UTF-8 | `곳간` explicit membership and binary blobs / FD02B/asset successor |
| Q Unicode/path | `ALIGNED` core / `CONFLICT` accidental files | `normalize_project_path`, `normalize_virtual_project_source` | disk/virtual source → NFC + slash + duplicate checks | NFC duplicate and ASCII case-fold collision fail closed; absolute/URI/dot reject | `.DS_Store`/`Thumbs.db` must not enter snapshot; portable case policy tests / FD02B |
| R persistence DB | `PARTIAL` | `solutions/seamgrim_ui_mvp/tools/project_store.py::SeamgrimProjectStore` | HTTP service → SQLite+object CAS | saved revisions/runs/checkpoints, WAL, FK, limits; project store tests | four-state ownership and bounded recovery/GC / FD02A-B |
| R2 platform DB | `OUT_OF_V1` | `solutions/ttonimaru_platform/storage/sqlite_store.py::TtonimaruStore` | platform API → SQLite | projects/revisions/publications, separate owner | do not merge into Workbench V1 authority |
| S save transaction/HEAD | `PARTIAL` | `create_project`, `add_revision`, `_write_object_atomic` | API → object write → `BEGIN IMMEDIATE` → revision/head | expected parent fail-closed; file may orphan before DB commit | I1 orphan custody + exact head run binding review / FD02A-B |
| T autosave/recovery | `PARTIAL` | Workbench `writeOneFileDraft`, `writeNativeProjectCatalog`, local fallback | input → localStorage | best-effort every-input recovery, fixed catalog caps 30; no typed retention/checkpoint ledger | bounded RecoveryCheckpoint separate from SavedProjectRevision / FD02B |
| U stale save | `ALIGNED` save / `MISSING` run | `add_revision(expected_parent_revision_id)`, Workbench 409 path | save → CAS head compare | stale concurrent save fails; primary Run not tied to current head | I1 exact run head check targeted review / FD02A |
| V CAS/object store | `PARTIAL` | `project_store.py::{objects,_write_object_atomic,read_object_json}` | revision/checkpoint → SHA-256 object | dedup by content hash; canonical project snapshot is one large object | file/resource blobs + small reference manifest / FD02B |
| W receipt/replay | `PARTIAL` | DB `runs`, `run_checkpoints`; `run_archive_adapter.js` | Workbench run → server run/checkpoints | revision/content FK and state hashes; primary execution input seal incomplete | execution snapshot/receipt exact binding; replay root pins / FD02A-B |
| X GC/retention | `MISSING` | limits only: `MAX_PROJECT_REVISIONS`, `MAX_PROJECT_RUNS`, `MAX_RUN_CHECKPOINTS` | create path → count reject | hard caps; no object reachability GC or bounded recovery pruning | mark/sweep from saved/receipt/replay roots / FD02B |
| Y tracked/local boundary | `PARTIAL` | Git tracked source; official store outside repo; localStorage; experimental portable schemas | product source → local runtime stores | tracked product vs official DB/local browser separated; portable not stable | custody manifest and no local cache as release authority / FD02B |
| Z tests/goldens | `PARTIAL` | `tests/ddn_local_project_*`, `run_seamgrim_project_*`, `seamgrim_*project*`, `tool/tests/v1_fd01_lesson_epoch_inventory.rs` | runners → CLI/WASM/browser/store | broad current behavior coverage; R2 29-case identity/storage matrix absent | new D-PACK and fault injection / FD02A-B |

## DB authority details

### 1. Seamgrim project store

```yaml
CODE_PATH: solutions/seamgrim_ui_mvp/tools/project_store.py
RUNTIME_PATH: <data_dir>/seamgrim_projects.sqlite3
SCHEMA: seamgrim.project_store.sqlite.v0
TABLES: [store_meta, objects, projects, revisions, capabilities, runs, run_checkpoints]
READER: SeamgrimProjectStore.get_project/list_revisions/get_run/read_object_json
WRITER: create_project/add_revision/restore_revision/create_run/add_run_checkpoint/finalize_run
AUTHORITY: Workbench server-saved project/revision and run archive
TRANSACTION: BEGIN IMMEDIATE for head/revision/run/checkpoint mutations; WAL + foreign_keys
```

### 2. Ttonimaru platform store

```yaml
CODE_PATH: solutions/ttonimaru_platform/storage/sqlite_store.py
RUNTIME_PATH: constructor supplied path or :memory:
SCHEMA: typed response schemas; SQLite physical schema has projects/revisions/publications
READER: TtonimaruStore.get_project and publication/revision readers
WRITER: create_project/create_revision/publish
AUTHORITY: separate Ttonimaru platform sharing domain
TRANSACTION: per-operation commit
DISPOSITION: OUT_OF_V1; not a Workbench project-revision owner
```

## Durable project authority count

`DURABLE_PROJECT_AUTHORITY_COUNT: 4`

Count rule: a store counts when it can independently retain a reopenable project payload, not when it only indexes or archives a run.

1. server SQLite + content-addressed object store (`projects/revisions`),
2. native Workbench project localStorage catalog,
3. per-project local fallback snapshot localStorage,
4. experimental portable project localStorage catalog.

`ONE_FILE_DDN_DRAFT_KEY` is an auxiliary single-file recovery buffer, `MY_WORK_INDEX_KEY` is an index, and `runs/run_checkpoints` are execution archives; they are not additional complete project authorities. Ttonimaru is a separate product domain and excluded from this count.

## Current storage growth facts

- Explicit server Save with identical canonical snapshot reuses the same object blob but adds a revision row.
- Every editor input rewrites localStorage native/single-file recovery payload; it does not add a server revision.
- Unchanged source Run does not create a SavedProjectRevision, but may create run/checkpoint rows and objects.
- Source files/resources are not individually blob-addressed. One-file edit changes the monolithic snapshot object.
- GC is absent; object growth is bounded only indirectly by row caps and manual custody.

## Exact owner summary

```yaml
EXACT_PROJECT_OWNER_PATHS:
  - tool/src/local_project.rs
  - tools/teul-cli/src/main.rs
  - tool/src/wasm_api.rs
  - solutions/seamgrim_ui_mvp/ui/workbench/workbench.js
  - solutions/seamgrim_ui_mvp/ui/project_snapshot.js
  - solutions/seamgrim_ui_mvp/tools/project_store.py
  - solutions/seamgrim_ui_mvp/tools/ddn_exec_server.py
EXACT_SOURCE_EPOCH_OWNER:
  TYPE: lang/src/ast.rs::SourceEpoch
  PARSE_SELECTION: lang/src/lib.rs::{parse_with_mode,parse_v25_with_mode}
  RUNTIME_SELECTION: tool/src/ddn_runtime.rs::from_source_epoch_with_mode
  PROJECT_OWNER: MISSING
EXACT_LOCK_OWNER: tool/src/local_project.rs::{LocalGajiLock,build_project_gaji_lock}
```
