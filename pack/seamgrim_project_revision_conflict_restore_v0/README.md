# seamgrim_project_revision_conflict_restore_v0

Wave2E G6 product pack for append-only revision guard, stale-edit conflict, local package preservation, and restore-as-new-revision.

The browser runner opens two edit contexts from the same head, saves one, verifies the second receives a conflict instead of overwriting, preserves the local package payload, lists revision audit fields, and restores an earlier revision by creating a new head revision.

No SSOT, DDN syntax, or `state_hash` formula changes are part of this pack.
