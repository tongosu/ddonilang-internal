# seamgrim_project_restart_backup_recovery_v0

Wave2E G7 pack for restart-safe capability links, project-store backup/restore, and integrity diagnostics.

Coverage:

- edit/view capability links still open after the local same-origin server restarts with the same data dir.
- backup copies SQLite metadata and content-addressed object files after a clean integrity audit.
- restore into an empty data dir preserves project head, revisions, content SHA, and capability hashes.
- missing objects, corrupt object bytes, and wrong DB object-path references produce diagnostics.

This is a local durable-project boundary, not a cloud sync, login, signing, or public hosting claim.
