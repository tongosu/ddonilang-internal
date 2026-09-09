# ast_project_visual_workbench_gate_v1

G14 integrated regression and determinism gate for the DDN AST project runtime and Seamgrim multi-file visual Workbench.

The dedicated checker is `tests/run_ast_project_visual_workbench_gate_check.py`.
It directly verifies:

- whitespace-independent AST module lowering via raw WASM project summaries,
- multi-file project runtime result binding to actual Workbench Bogae evidence.

Non-claims: no new DDN grammar, no runtime `state_hash` formula change, no public registry, no remote resolver, no full DDN module-system completion.
