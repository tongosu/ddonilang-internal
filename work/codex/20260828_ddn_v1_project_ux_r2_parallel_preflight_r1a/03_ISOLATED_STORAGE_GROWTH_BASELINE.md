# Isolated storage growth baseline

## Method

The measurement imported `solutions/seamgrim_ui_mvp/tools/project_store.py` from product baseline `6824ef7c...` and used a new `TemporaryDirectory`. It did not touch the official DB, protected PID/port, tracked files, or network. The temporary directory was removed automatically; final residue was false.

Each saved snapshot contained the same 1,048,595-byte UTF-8 resource and a one-line source whose value changed from `1` to `2`.

## Results

| Point | objects | object bytes | projects | revisions | runs | checkpoints | DB bytes |
|---|---:|---:|---:|---:|---:|---:|---:|
| initialized | 0 | 0 | 0 | 0 | 0 | 0 | 94,208 |
| explicit save A | 1 | 1,049,017 | 1 | 1 | 0 | 0 | 94,208 |
| explicit save B / one source edit | 2 | 2,098,034 | 1 | 2 | 0 | 0 | 94,208 |
| reopen | 2 | 2,098,034 | 1 | 2 | 0 | 0 | 94,208 |
| stale expected-head save | 2 | 2,098,034 | 1 | 2 | 0 | 0 | 94,208 |
| 100 archived run rows | 2 | 2,098,034 | 1 | 2 | 100 | 0 | 126,976 |

Exact identities:

```yaml
SAVE_A_CONTENT_SHA256: f84a6855aa8d4bca8b5cb536f711e05405f5a9b77ae7b8356d97f5bac443c0bf
SAVE_B_CONTENT_SHA256: 1e9394f622ca85052cc87f0839e597f980d0b96869f9f4231e5344aaae0f8a3a
REOPEN_HEAD_SAME: true
REOPEN_CONTENT_SHA_SAME: true
STALE_RESULT: ProjectConflictError / expected parent revision does not match head
STALE_OBJECT_DELTA: 0
STALE_DB_ROW_DELTA: 0
RUN_100_OBJECT_DELTA: 0
RUN_100_REVISION_DELTA: 0
RUN_100_RUN_ROW_DELTA: 100
RUN_100_DB_BYTE_DELTA: 32768
NETWORK_CALLS: 0
LOCK_WRITES: 0
TEMP_RESIDUE: 0
```

The 100 operations used `SeamgrimProjectStore.create_run` with the same saved revision. They prove archive-row growth and source-object reuse, not 100 executions of the DDN runtime.

## Resource reuse finding

The resource literal occurred twice across the two monolithic snapshot objects. The two revisions had different object identities and no separately addressed resource blob existed.

```yaml
SAME_LARGE_RESOURCE_REFERENCES: 2
RESOURCE_LITERAL_OCCURRENCES_IN_OBJECT_FILES: 2
REUSABLE_RESOURCE_BLOB_IDENTITY: NONE
CURRENT_STORAGE_DISPOSITION: MONOLITHIC_SNAPSHOT_DUPLICATION
FD02B_CAS_NEED: CONFIRMED
```

## Existing runner attempts

- `python tests/run_seamgrim_project_save_reopen_check.py`: RED before product execution because local `playwright` package is absent; network install was not attempted.
- `python tests/run_seamgrim_project_revision_conflict_restore_check.py`: same environment RED.
- `python tests/run_seamgrim_project_store_check.py`: runner error while printing golden failure under CP949 (`UnicodeEncodeError`); the direct isolated store measurement above remains valid but does not replace browser/product proof.

## Not executable in this preflight

| Case | Status | Required hook/evidence |
|---|---|---|
| editor keystrokes ×100 | `NOT_EXECUTABLE_CURRENTLY` | authoritative EditorGeneration observation without durable save; I1 candidate review/adoption first |
| actual DDN Run ×100 | `NOT_EXECUTABLE_CURRENTLY` | fixed-head CLI/WASM/Workbench execution hook plus network/lock counters |
| crash before/after HEAD commit | `NOT_EXECUTABLE_CURRENTLY` | documented task-owned phase fault hooks; no fault was fabricated |
| recovery entry and retention | `NOT_EXECUTABLE_CURRENTLY` | typed RecoveryCheckpoint/orphan/reachability ledger |
| file/resource dedup | `NOT_EXECUTABLE_CURRENTLY` | content-addressed file/resource schema and reference graph |
| browser save/reopen | `NOT_EXECUTABLE_CURRENTLY` in this worktree | sealed local Playwright dependency or approved existing browser harness |

No unsupported case was simulated and no runner threshold was weakened.
