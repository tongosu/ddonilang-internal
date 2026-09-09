# seamgrim_workbench_durable_quality_gate_v1

G10 quality gate for the durable workbench bridge.

This pack groups the G1-G9 durable workbench gates and records the boundary for IDC readiness without claiming actual IDC deployment, HA, TLS, login, or public registry completion.

The aggregate requires explicit Workbench/control readiness, monotonic save
completion generations, local view-role WASM execution without server writes,
and no newly created runner-owned temporary directory after every component.
