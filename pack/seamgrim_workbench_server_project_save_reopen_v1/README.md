# seamgrim_workbench_server_project_save_reopen_v1

G2 product gate for the durable workbench bridge.

This pack binds the workbench save/reopen buttons to the existing Seamgrim project API and SQLite-backed object store. It verifies server project creation, append-only revision save, capability-fragment reopen, URL hash scrub, and visible revision audit rows.

Boundaries:

- Uses the existing `project_snapshot.v0` and project API.
- Does not introduce a parallel project store.
- Does not change DDN syntax or runtime `state_hash`.
