# seamgrim_workbench_revision_conflict_restore_v1

G3 product gate for the durable workbench bridge.

This pack verifies that the workbench preserves local edits on a stale parent revision conflict and restores an older revision by creating a new append-only revision.

Boundaries:

- Conflict resolution does not overwrite server HEAD.
- Restore creates a new revision; it does not mutate historical revisions.
- No new DDN syntax or runtime `state_hash` formula changes.
