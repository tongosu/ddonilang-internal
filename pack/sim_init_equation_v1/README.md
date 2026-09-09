# sim_init_equation_v1

This pack verifies `채비 { 세움 { ... }. }` as an initialization assertion
artifact.

Scope:

- S0/S1 initialization assertions are accepted and marked with `init_plan.kind`
  `t0_one_shot`.
- S2/S3 initialization assertions are not executed as initialization and emit
  `E_INIT_UNSUPPORTED` in the SolvePlan artifact.

Boundary:

- This is an artifact/planner landing only. It does not apply initialization
  values to runtime state and does not change `state_hash`.

Verification:

- `python tests/run_pack_golden.py sim_init_equation_v1`
- `python tests/run_declarative_closure_g6_init_vector_check.py`
