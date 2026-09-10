#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { extractCanonicalViewAuthorityInputsFromState } from "../solutions/seamgrim_ui_mvp/ui/seamgrim_runtime_state.js";
import {
  buildCanonicalViewPayloadSet,
  buildCommittedSemanticViewPayload,
} from "../solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_payload.js";
import {
  buildSemanticRenderModel,
  renderCommittedSemanticView,
} from "../solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_renderer.js";

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

const resultSchemas = {
  line: "seamgrim.workbench.line_result.v1_candidate",
  pendulum: "seamgrim.workbench.pendulum_result.v1_candidate",
  projectile: "seamgrim.workbench.projectile_result.v1_candidate",
  grid: "seamgrim.workbench.grid_result.v1_candidate",
};

function authoritativeResultSet(family, content) {
  return {
    schema: "seamgrim.workbench.authoritative_result_set.v1_candidate",
    producer: "ddonirang_tool.wasm_runtime",
    provenance: "native_authoritative_structured_result",
    results: {
      [family]: {
        schema: resultSchemas[family],
        family,
        status: "available",
        producer: "ddonirang_tool.wasm_runtime",
        provenance: "native_authoritative_structured_result",
        content,
      },
    },
  };
}

function frame(frameId, values, { resources = {}, viewMeta = {}, workbench = null } = {}) {
  const entries = Object.entries(values);
  return {
    frame_id: frameId,
    madi: frameId + 1,
    state_hash: `blake3:frame_${frameId}`,
    source_hash: "sha256:semantic_renderer",
    wasm_state: {
      channels: entries.map(([key, value]) => ({ key, dtype: typeof value === "number" ? "num" : "str", role: "state" })),
      row: entries.map(([, value]) => value),
      resources: { value_json: { ...values, ...resources } },
      view_meta: workbench ? { ...viewMeta, workbench } : viewMeta,
    },
  };
}

function canonicalFor(run, row) {
  const inputs = extractCanonicalViewAuthorityInputsFromState(row.wasm_state);
  inputs.identity = {
    ...inputs.identity,
    state_hash: row.state_hash,
    source_hash: row.source_hash ?? run.source_hash,
    tick_id: row.madi,
  };
  return buildCanonicalViewPayloadSet(inputs);
}

function payloadFor(primaryView, frames, activeIndex = frames.length - 1, role = "primary") {
  const run = { run_id: `run_${primaryView}`, source_hash: "sha256:semantic_renderer", frames };
  const canonicalViewHistory = frames.slice(0, activeIndex + 1).map((row) => ({
    frame_id: row.frame_id,
    madi: row.madi,
    state_hash: row.state_hash,
    canonical_views: canonicalFor(run, row),
  }));
  return buildCommittedSemanticViewPayload({
    project: { id: primaryView, primaryView },
    run,
    frame: frames[activeIndex],
    viewConfig: { primary_view: primaryView, role, mode: "ddn-main" },
    canonicalViewPayloads: canonicalViewHistory.at(-1).canonical_views,
    canonicalViewHistory,
  });
}

function payloadWithoutRendererIdentity(frames, activeIndex = frames.length - 1) {
  const run = { run_id: "run_missing_renderer_identity", source_hash: "sha256:semantic_renderer", frames };
  const canonicalViewHistory = frames.slice(0, activeIndex + 1).map((row) => ({
    frame_id: row.frame_id,
    madi: row.madi,
    state_hash: row.state_hash,
    canonical_views: canonicalFor(run, row),
  }));
  return buildCommittedSemanticViewPayload({
    project: { id: "missing_renderer_identity" },
    run,
    frame: frames[activeIndex],
    viewConfig: { role: "primary", mode: "ddn-main" },
    canonicalViewPayloads: canonicalViewHistory.at(-1).canonical_views,
    canonicalViewHistory,
  });
}

const pendulumPrimary = buildSemanticRenderModel(payloadFor("pendulum", [
  frame(0, { theta: 99, omega: 99, energy: 99, L: 99 }, {
    workbench: authoritativeResultSet("pendulum", {
      current: {
        theta: 0.25,
        omega: -0.1,
        energy: 1.4,
        kinetic_energy: 0.4,
        potential_energy: 1,
        length: 2,
        physical_bob: { x: 0.4948079185090459, y: -1.9378248434212895 },
        normalized_bob: { x: 0.24740395925452294, y: 0.9689124217106447 },
      },
    }),
  }),
]));
const pendulumOverlay = buildSemanticRenderModel(payloadFor("pendulum", [
  frame(0, { theta: 99 }, {
    workbench: authoritativeResultSet("pendulum", {
      current: {
        theta: 0.25,
        omega: -0.1,
        energy: 1.4,
        kinetic_energy: 0.4,
        potential_energy: 1,
        length: 2,
        physical_bob: { x: 0.4948079185090459, y: -1.9378248434212895 },
        normalized_bob: { x: 0.24740395925452294, y: 0.9689124217106447 },
      },
    }),
  }),
], 0, "overlay"));
assert(pendulumPrimary.status === "ready", "pendulum renderer did not resolve committed theta");
assert(pendulumPrimary.current.theta === 0.25, "pendulum used a non-committed theta");
assert(Math.abs(pendulumPrimary.current.physical_bob.x - 2 * Math.sin(0.25)) < 1e-12, "pendulum bob x was not derived from committed theta/L");
assert(Math.abs(pendulumPrimary.current.physical_bob.y + 2 * Math.cos(0.25)) < 1e-12, "pendulum bob y was not derived from committed theta/L");
assert(JSON.stringify(pendulumOverlay.overlay.normalized_bob) === JSON.stringify(pendulumPrimary.current.normalized_bob), "pendulum overlay left the primary coordinate system");
assert(pendulumPrimary.labels.some((row) => row.key === "omega" && row.value === -0.1), "pendulum committed omega label missing");

const projectileFrames = [
  frame(0, { t: 99, x: 99, y: 99, vx: 99, vy: 99 }, {
    workbench: authoritativeResultSet("projectile", { current: { t: 0, x: 0, y: 0, vx: 8, vy: 15 }, camera: { x_min: -1, x_max: 3, y_min: -1, y_max: 4 } }),
  }),
  frame(1, { t: 99, x: 99, y: 99, vx: 99, vy: 99 }, {
    workbench: authoritativeResultSet("projectile", { current: { t: 1, x: 0.8, y: 1.5, vx: 8, vy: 14.02 }, camera: { x_min: -1, x_max: 3, y_min: -1, y_max: 4 } }),
  }),
  frame(2, { t: 99, x: 99, y: 99, vx: 99, vy: 99 }, {
    workbench: authoritativeResultSet("projectile", { current: { t: 2, x: 1.6, y: 2.902, vx: 8, vy: 13.04 }, camera: { x_min: -1, x_max: 3, y_min: -1, y_max: 4 } }),
  }),
];
const projectilePayload = payloadFor("projectile", projectileFrames, 1);
const projectile = buildSemanticRenderModel(projectilePayload);
assert(projectile.status === "ready", "projectile renderer did not resolve committed x/y");
assert(projectile.current.x === 0.8 && projectile.current.y === 1.5, "projectile current point was not the active committed frame");
assert(projectile.trajectory.length === 2, "projectile trajectory included a future committed frame beyond the active cursor");
assert(projectile.trajectory.at(-1).state_hash === "blake3:frame_1", "projectile trajectory did not end at the active committed frame");
assert(projectile.labels.some((row) => row.key === "vy" && row.value === 14.02), "projectile committed velocity label missing");

const board = [
  [".", ".", "."],
  [".", "O", "."],
  [".", ".", "."],
];
const gridPayload = payloadFor("grid", [
  frame(6, { tick: 7 }, {
    resources: { board, piece: { x: 1, y: 1 } },
    viewMeta: {
      space2d: {
        camera: { x_min: 0, x_max: 3, y_min: 0, y_max: 3 },
        drawlist: [{ kind: "circle", x: 1.5, y: 1.5, r: 0.25 }],
      },
    },
    workbench: authoritativeResultSet("grid", {
      position: { x: 1, y: 1 },
      dimensions: { columns: 3, rows: 3 },
      space2d: {
        schema: "seamgrim.space2d.v0",
        camera: { x_min: 0, x_max: 3, y_min: 0, y_max: 3 },
        drawlist: [{ kind: "circle", x: 1.5, y: 1.5, r: 0.25 }],
      },
    }),
  }),
]);
const grid = buildSemanticRenderModel(gridPayload);
assert(grid.status === "ready", "grid renderer ignored committed board/view geometry");
assert(grid.tick === 7, "grid renderer did not use committed tick");
assert(grid.position.x === 1 && grid.position.y === 1, "grid renderer did not use committed piece position");
assert(grid.geometry_source === "canonical_workbench_grid_result", "grid renderer geometry was not canonical runtime data");

const missingGridCameraPayload = payloadFor("grid", [frame(7, { tick: 8 }, {
  workbench: authoritativeResultSet("grid", {
    position: { x: 1, y: 1 },
    dimensions: { columns: 3, rows: 3 },
    space2d: {
      schema: "seamgrim.space2d.v0",
      drawlist: [{ kind: "circle", x: 1.5, y: 1.5, r: 0.25 }],
    },
  }),
})]);
const missingGridCamera = buildSemanticRenderModel(missingGridCameraPayload);
assert(missingGridCamera.status === "canonical_unsupported", "geometry must not synthesize a grid camera");
assert(missingGridCamera.canonical_diagnostic?.reason === "projection_camera_missing_or_invalid", "grid missing camera diagnostic drift");

const line = buildSemanticRenderModel(payloadFor("line", [frame(0, { a: 99, b: 99, x: 99, y: 99 }, {
  workbench: authoritativeResultSet("line", {
    current: { x: 2, y: 5 },
    equation: { a: 2, b: 1 },
    camera: { x_min: -2, x_max: 4, y_min: -3, y_max: 9 },
  }),
})]));
assert(line.status === "ready" && line.current.x === 2 && line.current.y === 5, "static graph did not use committed result point");
assert(line.labels.map((row) => row.key).join(",") === "x,y,a,b", "static graph semantic labels missing");
assert(JSON.stringify(line.camera) === JSON.stringify({ minX: -2, maxX: 4, minY: -3, maxY: 9 }), "line renderer did not retain explicit camera");

const missingCameraPayload = payloadFor("line", [frame(0, { x: 9, y: 12 }, {
  workbench: authoritativeResultSet("line", {
    current: { x: 2, y: 5 },
    equation: { a: 2, b: 1 },
  }),
})]);
const missingCameraBefore = JSON.stringify(missingCameraPayload);
const missingCamera = buildSemanticRenderModel(missingCameraPayload);
assert(missingCamera.status === "canonical_unsupported", "missing explicit camera must fail closed");
assert(missingCamera.canonical_diagnostic?.reason === "projection_camera_missing_or_invalid", "missing camera diagnostic drift");
assert(!Object.hasOwn(missingCamera, "camera") && !Object.hasOwn(missingCamera, "current"), "missing camera published a projection model");
assert(JSON.stringify(missingCameraPayload) === missingCameraBefore, "missing camera projection mutated semantic payload");
for (const model of [pendulumPrimary, pendulumOverlay, projectile, grid, line]) {
  assert(model.data_source === "canonical_workbench_result", `${model.family}: raw-state authority remains active`);
}

const awaiting = buildSemanticRenderModel(buildCommittedSemanticViewPayload({
  project: { id: "empty", primaryView: "pendulum" },
  viewConfig: { primary_view: "pendulum", role: "primary", mode: "ddn-main" },
}));
assert(awaiting.status === "awaiting_committed_frame", "pre-run preview fabricated a runtime frame");

const missingRendererIdentityPayload = payloadWithoutRendererIdentity([frame(0, { x: 9, y: 12, a: 4, b: 2 }, {
  workbench: authoritativeResultSet("line", {
    current: { x: 2, y: 5 },
    equation: { a: 2, b: 1 },
  }),
})]);
const missingRendererIdentityBefore = JSON.stringify(missingRendererIdentityPayload);
const missingRendererIdentity = buildSemanticRenderModel(missingRendererIdentityPayload);
assert(missingRendererIdentityPayload.view_config.primary_view === "", "missing renderer identity must not default to line");
assert(missingRendererIdentity.status === "canonical_unsupported", "numeric observations must not select line without renderer identity");
assert(missingRendererIdentity.canonical_diagnostic?.reason === "unsupported_renderer_family", "missing renderer identity failure drift");
assert(!Object.hasOwn(missingRendererIdentity, "current"), "missing renderer identity created a line model");
assert(JSON.stringify(missingRendererIdentityPayload) === missingRendererIdentityBefore, "missing renderer identity mutated semantic payload");

function failureCanvas() {
  const calls = [];
  return {
    calls,
    fillText(...args) { calls.push(["fillText", ...args]); },
    set fillStyle(value) { calls.push(["fillStyle", value]); },
    set font(value) { calls.push(["font", value]); },
  };
}

function assertUnsupportedRendererFamily(family) {
  const payload = payloadFor(family, [frame(0, { x: 9, y: 12 }, {
    workbench: authoritativeResultSet("line", {
      current: { x: 2, y: 5 },
      equation: { a: 2, b: 1 },
    }),
  })]);
  const before = JSON.stringify(payload);
  const first = buildSemanticRenderModel(payload);
  const second = buildSemanticRenderModel(payload);
  assert(first.status === "canonical_unsupported", `${JSON.stringify(family)} must fail as an unsupported projection`);
  assert(first.canonical_diagnostic?.code === "E_CANONICAL_WORKBENCH_RESULT_UNSUPPORTED_CANDIDATE", `${JSON.stringify(family)} diagnostic drift`);
  assert(first.canonical_diagnostic?.reason === "unsupported_renderer_family", `${JSON.stringify(family)} must preserve projection failure cause`);
  assert(first.canonical_diagnostic?.actual_schema === family, `${JSON.stringify(family)} renderer identity drift`);
  assert(!Object.hasOwn(first, "current") && !Object.hasOwn(first, "points") && !Object.hasOwn(first, "trajectory"), `${JSON.stringify(family)} must not create a line/default model`);
  assert(JSON.stringify(first) === JSON.stringify(second), `${JSON.stringify(family)} failure must be deterministic`);
  assert(JSON.stringify(payload) === before, `${JSON.stringify(family)} renderer mutated the semantic payload`);
  const ctx = failureCanvas();
  const rendered = renderCommittedSemanticView(ctx, 320, 180, payload);
  assert(rendered.status === "canonical_unsupported", `${JSON.stringify(family)} renderer silently succeeded`);
  assert(!Object.hasOwn(rendered, "canvas_projection"), `${JSON.stringify(family)} renderer published a canvas success projection`);
  assert(ctx.calls.some(([name]) => name === "fillText"), `${JSON.stringify(family)} failure was swallowed instead of rendered as a failure`);
  assert(JSON.stringify(payload) === before, `${JSON.stringify(family)} renderer mutated payload during projection`);
}

for (const unsupportedFamily of [
  "unknown_renderer",
  "",
  "line-compatible",
  "LINE",
  "prefix-line",
  "line-suffix",
  "grid2d",
]) {
  assertUnsupportedRendererFamily(unsupportedFamily);
}

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const workbenchSource = await fs.readFile(path.join(root, "solutions/seamgrim_ui_mvp/ui/workbench/workbench.js"), "utf8");
for (const forbidden of ["theta = 0.52", "projectileParamsFromSource", "projectilePoints", "readDdnSetupNumber", "grid session tick 0"]) {
  assert(!workbenchSource.includes(forbidden), `forbidden renderer shortcut remains: ${forbidden}`);
}

console.log("seamgrim_workbench_semantic_view_renderer: ok");
