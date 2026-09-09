# seamgrim_workbench_durable_persistence_adapters_v1

G1 evidence pack for the durable workbench bridge.

This pack verifies that the approved workbench no longer treats direct `localStorage`
as the product persistence contract. Local fallback remains available, but it is
explicitly labeled as device-only and separated from the server project adapter.
The browser gate waits for explicit Workbench/control readiness and proves that
the completed persistence generation belongs to the click under test. It also
checks that its owned process, socket, and temporary-directory residuals are zero.

Behavior claim boundary:

- Product UI behavior: adapter-backed local fallback status and artifact builder.
- Server project save/open: G2.
- Run archive server binding: G4.
