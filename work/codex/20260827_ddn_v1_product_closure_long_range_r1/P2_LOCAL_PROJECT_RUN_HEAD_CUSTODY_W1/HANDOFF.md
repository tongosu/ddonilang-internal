# P2 local-project saved-head run custody W1 handoff

## Status

- `P2_LOCAL_PROJECT_RUN_HEAD_CUSTODY_IMPLEMENTED_UNDER_REVIEW`
- This is one bounded P2 product vertical. It is not whole-P2, P3, P4, P5, V1, release, activation, or Human PASS closure.

## Authority and lineage

- live internal CURRENT: v25.35.0 / RD-001~490
- `docs/ssot/CURRENT.md`: 656 bytes / SHA-256 `d8224b35d8e10b134ad2c3cd6e94db7d9b32d21363515fa848df91e8972262aa`
- public Language SPEC: v0.6.0 / `publish/spec/CURRENT.md` SHA-256 `6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0`
- baseline and direct parent: `f08c25961bb89fd91ccee06efb59046123a9a382`
- product/test fixed commit: `412d75de1adf1d2ecbb15832285775f9458c0532`
- fixed tree: `31979b71c08c765abac811ecc241cefaa6ca2f37`
- merge count: 0

## Product workflow changed or unblocked

The existing create/open/edit/atomic-save/reopen/run workflow can now bind Run creation to the saved project HEAD. A client supplies `expected_head_revision_id`; the store checks it inside the same immediate transaction before inserting a Run. A stale expected HEAD fails closed with the existing conflict class, publishes no Run, and leaves the saved project HEAD unchanged. Existing callers that omit the optional field retain their prior behavior.

No public schema, public spelling, storage layout, CAS/DB contract, autosave, retention, or GC decision is claimed.

## Exact fixed diff

- `solutions/seamgrim_ui_mvp/tools/project_store.py`
- `solutions/seamgrim_ui_mvp/tools/ddn_exec_server.py`
- `tests/run_seamgrim_workbench_run_archive_store_check.py`
- `pack/seamgrim_workbench_run_archive_store_v1/golden.jsonl`

Product source outside the two listed implementation files is unchanged. Tracked WASM, visible UI, `docs/ssot/**`, and `publish/spec/**` are unchanged.

## RED, GREEN, and mutation evidence

- pre-implementation product RED: `SeamgrimProjectStore.create_run() got an unexpected keyword argument 'expected_head_revision_id'`
- focused GREEN: `python tests/run_seamgrim_workbench_run_archive_store_check.py` -> `[seamgrim-workbench-run-archive-store-v1] OK behavior-closed`
- risk mutation: disabled only the expected-HEAD comparison -> actual RED `E_PROJECT_RUN_STALE_HEAD_ACCEPTED`
- exact restore: `project_store.py` SHA-256 before/after mutation `d6f5819ecffed0520564ce1feb1d2e479374ca563409ac53addb879df6de1ac2`
- restored focused GREEN: PASS
- Python compile for the two product files and reused runner: PASS
- `git diff --check`: PASS

The reused runner covers direct store and HTTP paths, saved source/HEAD identity, reopen identity, stale direct/API rejection, partial Run publish 0, and saved HEAD mutation 0. No new runner, checker, pack family, validation framework, or meta-test was created.

## Scoped baseline events

- `run_seamgrim_project_store_check.py`: pre-existing unrelated golden drift after current P4 trace output (`1` plus `마디` and trace hash), not changed under this lease.
- `run_seamgrim_project_restart_backup_recovery_check.py`: environment block, Playwright package absent.
- `run_seamgrim_workbench_storage_security_recovery_check.py`: pre-existing unrelated golden drift after current P4 trace output.

These events do not promote a broader regression PASS and remain outside this fixed slice.

## Anti-meta and review custody

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: saved-head-bound Run creation with stale mismatch fail-closed
- `NEW_TEST_ARTIFACT_COUNT`: 0
- `EXISTING_TEST_REUSED_COUNT`: 4
- `META_TEST_CREATED`: 0
- `STOP_RULE_APPLIED`: yes; one existing product-facing runner was extended and only one fail-open mutation was used
- `NEXT_PRODUCT_DECISION_ENABLED`: whether this bounded P2 custody behavior may join the next coherent rolling-review milestone
- `NEW_REVIEW_TASK_COUNT`: 0
- `NEW_REVIEW_WORKTREE_COUNT`: 0
- `REVIEW_BUNDLE_TARGET`: next coherent P2 local-project custody milestone using the existing management-owned rolling reviewer
- `REVIEW_NEEDED_NOW`: yes, because stale project HEAD acceptance is a product atomicity and custody risk; dispatch remains management-owned

## Open gates and nonclaims

Exact project manifest/schema/wire/storage/CAS/DB spelling, resource declarations, autosave, retention/GC, full snapshot/receipt coupling, Workbench visible workflow closure, P2 closure, P3~P6 closure, V1 membership/readiness, Windows RC/release, legal/distribution, activation, and Owner Human Smoke remain OPEN. No independent PASS is self-declared.
