# seamgrim_runner_lifecycle_reliability_v1

This pack records the Seamgrim workbench runner lifecycle reliability contract.

G1-G4 status:

- Adds structured runner lifecycle evidence.
- Adds negative controls for empty project id, missing server readiness, premature run archive access, and bounded owned-process cleanup.
- Removes the free-port close/rebind TOCTOU from the lineage runner by using server `--port 0` and the structured ready record.
- Verifies four parallel lineage runs with unique actual bound ports and residual owned PID count 0.
- Guards run archive API calls against missing project id, capability, or server run id before a project URL is constructed.
- Requires structured project save state and view-capability write rejection before run archive use.
- Closes `RELIABILITY_CLOSED` only when `tests/run_seamgrim_first_run_reliability_matrix_check.py` passes the G4 long consecutive run matrix.

No DDN syntax, parser/runtime semantics, `state_hash`, or `docs/ssot/**` behavior is changed by this pack.
