# seamgrim_workbench_capability_share_clone_v1

G6 product gate for the durable workbench bridge.

This pack verifies workbench edit/view capability separation, URL fragment scrub,
view-mode write denial, local WASM execution without a server run append, explicit
control readiness, owned-resource cleanup, and the clone-to-edit workflow.

Boundaries:

- No public project enumeration.
- No account/team/cloud claim.
- Raw capability is not exposed through debug snapshots.
