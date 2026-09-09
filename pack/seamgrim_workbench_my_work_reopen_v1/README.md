# seamgrim_workbench_my_work_reopen_v1

G7 product gate for the durable workbench bridge.

This pack verifies the workbench "내 작업" local capability index, server verification status, and reopen after server restart.

Boundaries:

- The index is browser-local capability knowledge, not a public server enumeration.
- Raw capabilities are not exposed in DOM/debug snapshots.
- Local cache never overwrites server truth.
