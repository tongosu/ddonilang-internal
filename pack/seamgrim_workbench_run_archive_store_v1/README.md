# seamgrim_workbench_run_archive_store_v1

G4 product gate for the durable workbench bridge.

This pack verifies the server-side append-only run archive in the existing Seamgrim project store and HTTP API.

Boundaries:

- Run archive is separate from project source revisions.
- Checkpoints are content-addressed artifacts in the existing object store.
- Renderer pixels are not stored.
- No DDN syntax or runtime `state_hash` formula changes.
