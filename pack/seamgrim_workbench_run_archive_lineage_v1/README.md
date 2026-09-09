# seamgrim_workbench_run_archive_lineage_v1

G5 product gate for the durable workbench bridge.

This pack verifies that the approved workbench persists actual sealed WASM runs into the server append-only run archive. It covers source revision binding, checkpoint append, finalize, child run branch lineage, and reopen in a new browser context.

Boundaries:

- Run archive does not create or mutate project source revisions.
- Renderer pixels are not archived.
- Run ids are storage identities outside runtime `state_hash`.
