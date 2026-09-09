# nurigym_step_record_v02_public_schema_v1

Decision Closure D2 pack for the opt-in NuriGym `step_record.v0.2` public schema product wire.

Scope:

- Default `nurigym run` output remains legacy `v0.1`.
- `step_record_version: "v0.2"` emits add-only public fields on `nurigym.step.v1` rows.
- `done == terminated || truncated` is validated for v0.2 rows.
- `missing_input` is an array only on v0.2 rows. Existing v0.1 action-pipeline boolean shape is not changed.

Boundary:

- No parser grammar change.
- No runtime `state_hash` formula change.
- No Gymnasium full compatibility claim.

Verification:

- `python tests/run_pack_golden.py nurigym_step_record_v02_public_schema_v1`
- `python tests/run_nurigym_step_record_v02_public_schema_check.py`
