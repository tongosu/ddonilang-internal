#!/usr/bin/env node

import {
  actionById,
  buildProjectControlModel,
  buildSetupRecipe,
  emptyProjectControlModel,
  normalizeActionMap,
  normalizeMaegimPlans,
} from "../solutions/seamgrim_ui_mvp/ui/workbench/project_control_model.js";

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

const planRows = [
  {
    source_path: "lesson.ddn",
    plan: {
      schema: "ddn.maegim_control_plan.v1",
      controls: [
        {
          name: "g",
          type_name: "수",
          init_expr_canon: "9.8",
          range: { min_expr_canon: "1", max_expr_canon: "20" },
          step_expr_canon: "0.1",
        },
        {
          name: "L",
          type_name: "수",
          init_expr_canon: "1",
          range: { min_expr_canon: "0.2", max_expr_canon: "3" },
          split_count_expr_canon: "28",
        },
      ],
    },
  },
  {
    source_path: "module.ddn",
    plan: {
      schema: "ddn.maegim_control_plan.v1",
      controls: [{ name: "g", type_name: "수", init_expr_canon: "10" }],
    },
  },
];

const normalized = normalizeMaegimPlans(planRows);
assert(normalized.controls.map((control) => control.name).join(",") === "g,L", "project controls must be ordered and de-duplicated by the Rust plan");
assert(normalized.controls[0].source === "wasm_canon_maegim_plan", "control authority mismatch");
assert(Math.abs(normalized.controls[1].step - 0.1) < 1e-9, "split-count step derivation mismatch");

const actionMap = {
  schema: "ddn.input_action_map.v1",
  project_id: "grid",
  actions: [
    {
      action_id: "drop",
      label: "내리기",
      glyph: "↓",
      input_snapshot: { intent: "drop", keys: 4, last_key: "ArrowDown" },
    },
  ],
};
const model = buildProjectControlModel({ projectId: "grid", planRows, actionMap });
assert(model.controls.length === 2 && model.actions.length === 1, "project model did not preserve declared surfaces");
assert(model.authoring_plan_hash.startsWith("candidate:fnv1a32:authoring_plan:"), "authoring plan identity missing");
assert(model.action_map.action_map_hash.startsWith("candidate:fnv1a32:action_map:"), "action-map identity missing");
assert(actionById(model, "drop")?.input_snapshot?.last_key === "ArrowDown", "declared action lookup mismatch");
const frozenActionMap = Object.freeze({
  ...actionMap,
  actions: Object.freeze(actionMap.actions.map((action) => Object.freeze({
    ...action,
    input_snapshot: Object.freeze({ ...action.input_snapshot }),
  }))),
});
const frozenActionMapBefore = JSON.stringify(frozenActionMap);
assert(normalizeActionMap(frozenActionMap, "grid")?.actions.length === 1, "frozen action map was not accepted");
assert(JSON.stringify(frozenActionMap) === frozenActionMapBefore, "action map payload was mutated during normalization");

const recipe = buildSetupRecipe(model, { g: 12.3, L: 1.4 });
assert(recipe.values.g === 12.3 && recipe.values.L === 1.4, "run recipe candidate lost control values");
assert(recipe.authoring_plan_hash === model.authoring_plan_hash, "run recipe lost authoring-plan lineage");

assert(normalizeActionMap({ schema: "other", actions: actionMap.actions }, "grid") === null, "unknown action schema was accepted");
assert(
  normalizeActionMap(
    {
      ...actionMap,
      actions: [...actionMap.actions, { ...actionMap.actions[0] }],
    },
    "grid",
  ) === null,
  "duplicate action identity was accepted as a partial action map",
);
assert(
  normalizeActionMap(
    {
      ...actionMap,
      actions: [
        actionMap.actions[0],
        {
          action_id: "broken",
          input_snapshot: { intent: "broken", keys: "not-a-number", last_key: "ArrowDown" },
        },
      ],
    },
    "grid",
  ) === null,
  "invalid action input was accepted as a partial action map",
);
assert(
  normalizeActionMap({ ...actionMap, project_id: "other-project" }, "grid") === null,
  "foreign project action map was accepted for the current workspace",
);
assert(
  normalizeActionMap({ ...actionMap, project_id: "" }, "grid") === null,
  "unbound action map was adopted by the current workspace",
);
assert(
  normalizeActionMap({
    ...actionMap,
    actions: [{
      id: "duck-action-id",
      input_snapshot: { intent: "drop", keys: 4, last_key: "ArrowDown" },
    }],
  }, "grid") === null,
  "raw action id alias was accepted as an action identity",
);
assert(
  normalizeActionMap({
    ...actionMap,
    actions: [{
      action_id: "duck-input",
      input: { intent: "drop", keys: 4, last_key: "ArrowDown" },
    }],
  }, "grid") === null,
  "raw input object was accepted as a typed InputSnapshot",
);
assert(
  normalizeActionMap({
    ...actionMap,
    actions: [{
      action_id: "duck-key",
      keys: 4,
      input_snapshot: { intent: "drop", last_key: "ArrowDown" },
    }],
  }, "grid") === null,
  "top-level key alias was accepted as a typed InputSnapshot",
);
assert(emptyProjectControlModel("plain").actions.length === 0, "empty project advertised global actions");

console.log("seamgrim_project_control_model: ok");
