# Current format compatibility audit

## Counting boundary

Counts use `git grep -n -I -E` at product baseline `6824ef7c21d5a0b95d67ae0048159ed79dcd7683`. This excludes later audit prose from the counts. `matches` is literal line occurrence count; `paths` is distinct tracked-path count. Product owners, representative fixtures/examples, and public exposure are listed separately.

| Surface | Matches / paths | Current owner / consumer symbols | Representative fixture or example | `publish/**` exposure |
|---|---:|---|---|---:|
| `뿌리.ddn` | 170 / 54 | `tool/src/local_project.rs` root discovery; Workbench source tree loaders | `pack/ddn_local_project_graph_v1/root_discovery/**`, `project_frontdoor/project_run_v1/뿌리.ddn` | 0 |
| `ddn.project.json` | 90 / 47 | `tool/src/local_project.rs`, `tool/src/project_meta.rs`, `tools/teul-cli/src/cli/run.rs` | three root-discovery `ddn.project.json` fixtures | 1, only `publish/DDONIRANG_DEV_STRUCTURE.md` |
| `entry_path` | 173 / 53 | `VirtualProjectSource.entry_path`, local graph normalization, Workbench project source and run planning | `pack/ddn_local_project_cli_wasm_parity_v1/fixtures/virtual_project.json` | 0 |
| `첫글` | 61 / 42 | `tool/src/local_project.rs::parse_project_block` alias set `entry_path/entry/first/첫글`; Workbench display/fixtures | `pack/ddn_local_project_graph_v1/**/뿌리.ddn` | 0 |
| `ddn.lock.v0-local` | 5 / 5 | `tool/src/local_project.rs` `lock_format` output | local graph expected/fixture and `project_frontdoor/**/ddn.lock` | 0 |
| `ddn.lock.v0` | 4 / 4 | virtual/local project compatibility payloads | CLI/WASM, graph, Workbench multifile fixtures | 0 |
| `ddn.local_gaji_lock.v1` | 9 / 9 | local gaji lock parser/hash/validation in `tool/src/local_project.rs` | graph frozen/tampered/run-physics fixtures and actual `ddn.lock` | 0 |
| `ddn.local_gaji_lock.hash_input.v1` | 1 / 1 | `tool/src/local_project.rs` hash preimage owner | Rust-owned only | 0 |
| `SourceEpoch` | 47 / 17 | `lang/src/ast.rs`, parser and normalizer; PC01 tests | `lang/tests/v25_definition_binding_pack.rs` | 0 |
| `source_epoch` | 34 / 12 | language parse modes and `tool/src/ddn_runtime.rs::from_source_epoch_with_mode` | FD01 readiness and PC01 mutation evidence | 0 |
| persisted `analysis_epoch_identity` / `execution_epoch_identity` | 0 / 0 | no current product-baseline storage field | none | 0 |
| `ddn.asset.json` | 40 / 16 | `tool/src/local_project.rs`, corpus/schema/gate registries | local project asset handling tests | 1, only `publish/DDONIRANG_DEV_STRUCTURE.md` |
| `seamgrim.project_snapshot.v0` | 17 / 16 | `project_store.py::_artifact_parts`; `ui/project_snapshot.js::PROJECT_SNAPSHOT_SCHEMA` | `pack/seamgrim_project_snapshot_v0/**` | 0 |
| `seamgrim.project_snapshot_artifact.v0` | 41 / 35 | same server and browser wrapper owners | portable/project-store packs and runners | 0 |
| `seamgrim.workbench.local_fallback_snapshot.v1` | 2 / 2 | `local_fallback.js::LOCAL_FALLBACK_SCHEMA` | portable Workbench runner | 0 |
| `seamgrim.approved_workbench.project_snapshot.v1` | 4 / 4 | `local_fallback.js::APPROVED_WORKBENCH_LOCAL_SCHEMA`, `workbench.js` | approved semantic vertical + durable adapter tests | 0 |
| `seamgrim.project_store.sqlite.v0` | 2 / 1 | `project_store.py::SCHEMA_VERSION`, `store_meta` | server store tests | 0 |
| `seamgrim.project_record.v0` | 1 / 1 | `SeamgrimProjectStore.get_project` | server store tests | 0 |
| `seamgrim.run_archive_record.v0` | 1 / 1 | `SeamgrimProjectStore._run_row_to_dict` | run archive tests | 0 |
| `seamgrim.run_checkpoint_artifact.v0` | 1 / 1 | `SeamgrimProjectStore.add_run_checkpoint` | restart/backup/recovery tests | 0 |

The exhaustive distinct-path populations are reproducible with this fixed command form:

```powershell
git grep -n -I -E '<literal>' 6824ef7c21d5a0b95d67ae0048159ed79dcd7683 --
```

The dominant path groups are `tool/src/local_project.rs`, Workbench product JS, local-project packs, and their runners. Work/audit prose is counted but is not a consumer. No listed string occurs in `publish/spec/**`.

## Compatibility findings

1. Current project discovery uses `뿌리.ddn`, optional `ddn.project.json`, and explicit `entry_path`/`첫글` aliases. PROJECT_UX_R2's proposed `처음.ddn` and `차림새` are therefore successor concepts, not a rename that can be performed in place.
2. Current lock identity is plural: `ddn.lock.v0`, `ddn.lock.v0-local`, and `ddn.local_gaji_lock.v1` serve different payload/hash roles. A successor must translate explicitly and fail closed; it must not silently reuse one string for another schema.
3. `SourceEpoch` is Rust-owned but is not yet stored as project-selected analysis/execution identity at this product baseline. Editable I1 adds an internal candidate, still on a side lineage and pending review.
4. Browser local snapshots and server revisions/runs are distinct authority modes. Their schemas must remain explicit; silent local/server fallback is forbidden.
5. Current snapshots are monolithic JSON objects. They do not provide file/resource CAS, recovery roots, or bounded GC.
6. The two `publish/**` mentions are architecture documentation, not Language SPEC schema or stable public compatibility contracts.

```yaml
PUBLIC_LANGUAGE_SPEC_FORMAT_EXPOSURE: 0
PUBLIC_COMPATIBILITY_CONFLICT: NONE_FOUND
MASS_IRREVERSIBLE_MIGRATION_REQUIRED_NOW: NO
OWNER_GATE: NO_OWNER_GATE_FOR_REVERSIBLE_SUCCESSOR
```

Exact public spelling, stable schema/wire, migration policy, and default activation remain separate Owner/SSOT decisions.
