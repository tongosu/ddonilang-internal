# lang_unit_check_v1

This pack fixes the product-path unit and dimension check surface used by
`teul-cli run`.

Scope:

- accepted unit literals: `@m`, `@s`, `@m/s`, `@m/s^2`, and the existing
  temperature normalization path
- rejected expressions: add, subtract, compare, scalar-unit mix, and unknown
  units
- scalar-unit mix policy: approved default B for add/sub/compare, meaning no
  implicit scalar-to-unit conversion

Boundary:

- assignment-dimension checking is not claimed by this pack because the current
  product path does not retain a declared unit type for plain reassignment.
- unit checks do not add anything to SolvePlan `state_hash_inputs` and do not
  change the runtime `state_hash` formula.

Verification:

- `python tests/run_pack_golden.py lang_unit_check_v1`
- `python tests/run_declarative_closure_g5_unit_check.py`
