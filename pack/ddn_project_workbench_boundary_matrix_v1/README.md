# ddn_project_workbench_boundary_matrix_v1

G13 boundary matrix for DDN AST local project runtime and Seamgrim multi-file Workbench.

This pack is verified by `tests/run_ddn_project_workbench_boundary_matrix_check.py`.
The runner directly exercises:

- raw WASM local-project frontdoors,
- portable project artifact parser,
- local project server API capability/revision boundaries.

Non-claims: no new DDN grammar, no runtime `state_hash` formula change, no public registry, no remote resolver.
