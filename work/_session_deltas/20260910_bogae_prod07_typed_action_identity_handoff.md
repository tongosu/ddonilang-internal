# BOGAE-PROD-07 typed action identity handoff

- Product: `f5eee4e17cefc8adde25aa9d75a7649540e467b1`
- Tree: `04db5c6d5c790e57b08f9332939bc5c62fff7c91`
- Parent: `02254caa030c15db23a07193592c9c78eac56554`
- Scope: `project_control_model` accepts only the typed `action_id` field;
  raw `id` is not an action identity.

The focused runner first observed RED for an action carrying only raw `id`:
`raw action id alias was accepted as an action identity`. The product hunk then
removed the raw-id fallback. Mutation M1 restored that fallback, reproduced the
same RED assertion, and was restored byte-exactly to SHA-256
`e01b3bf8a1aeec1625fe07724e754d6f27dd2c6af816862d9c344c282d05e6b8`, Git
blob `01d33dede20316b62c60e45e03d7200f3496eb71`.

GREEN gates:

- `node tests/seamgrim_project_control_model_runner.mjs`
- `node tests/seamgrim_workbench_runtime_bridge_t1_runner.mjs`
- `node tests/seamgrim_workbench_source_analysis_t4_runner.mjs`
- `node --check solutions/seamgrim_ui_mvp/ui/workbench/project_control_model.js`
- `git diff --check`

Ready for an independent fixed-target review of typed action identity only.
This does not close full PROD-07, Unit B, the persistent goal, V1 readiness,
release, SSOT, public SPEC, or Human approval.
