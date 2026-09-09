# seamgrim_workbench_storage_security_recovery_v1

G8 product gate for the durable workbench bridge.

This pack verifies failure and recovery boundaries for project revisions plus run archive records.

Boundaries:

- No stack trace, absolute data path, or raw capability in public API errors.
- Backup/restore includes run archive metadata and checkpoint objects.
- Corrupt or missing run checkpoint objects block backup.
