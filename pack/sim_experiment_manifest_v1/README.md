# sim_experiment_manifest_v1

Candidate experiment manifest fixture for declarative closure G8.

Scope:

- Records the minimum manifest fields needed to replay an experiment envelope.
- Keeps `state_hash_policy.formula_change=false`.
- Keeps `plan_hash_status=pending_canonical_bytes_decision`.

Boundary:

- This is a fixture/checker contract only.
- It does not define canonical manifest bytes, does not add `plan_hash`, and does
  not change the runtime `state_hash` formula.

Verification:

- `python tests/run_pack_golden.py sim_experiment_manifest_v1`
- `python tests/run_declarative_closure_g8_experiment_manifest_check.py`
