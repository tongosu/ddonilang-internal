# seamgrim_approved_workbench_runtime_lineage_v1

G3-G5 product evidence for the approved deterministic Seamgrim workbench.

- Product path: `solutions/seamgrim_ui_mvp/ui/workbench/index.html`
- Browser runner: `tests/seamgrim_approved_workbench_runtime_lineage_runner.mjs`
- Checker: `tests/run_seamgrim_approved_workbench_runtime_lineage_check.py`

This pack verifies actual browser-side WASM lifecycle controls, setup/action/view separation, and immutable run lineage.
It does not change DDN syntax or the runtime `state_hash` formula.
