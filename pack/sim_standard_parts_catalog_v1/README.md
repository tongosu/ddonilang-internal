# sim_standard_parts_catalog_v1

Candidate standard parts catalog for declarative closure G9.

Scope:

- Lists mechanical, circuit, econ, and queue part families.
- Links only existing evidence packs that are already present in this repo.
- Marks unsupported or unevidenced items as `candidate_only`.

Boundary:

- This is a catalog/checker fixture only.
- It does not create a new language block, parser surface, runtime component
  model, or solver behavior.

Verification:

- `python tests/run_pack_golden.py sim_standard_parts_catalog_v1`
- `python tests/run_declarative_closure_g9_standard_parts_catalog_check.py`
