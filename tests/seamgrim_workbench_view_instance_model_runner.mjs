#!/usr/bin/env node

import {
  closeAllSideViews,
  closeViewInstance,
  createViewWorkspace,
  hydrateViewWorkspace,
  hydrateViewWorkspaceWithMigration,
  legacySelectedView,
  openMagnifierView,
  openSideView,
  overlayViewInstances,
  reconcileViewWorkspace,
  selectViewTarget,
  serializeViewWorkspace,
  sideViewInstances,
  toggleOverlayView,
  viewRoleCapabilities,
} from "../solutions/seamgrim_ui_mvp/ui/workbench/view_instance_model.js";

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

const project = {
  id: "pendulum",
  primaryView: "pendulum",
  viewPolicy: {
    primary: "진자",
    side: "관찰값",
    overlay: "각도 측정",
    magnifier: "bob 확대",
  },
};
const payload = {
  committed_frame: { run_id: "run_1", frame_id: 2, madi: 2, state_hash: "blake3:frame_2" },
  ordered_observations: [{ name: "theta", value: 0.4 }, { name: "omega", value: -0.2 }],
};
const renderer = { status: "ready" };
const capabilities = viewRoleCapabilities(project, payload, renderer);
assert(capabilities.primary.supported, "primary view must always exist");
assert(capabilities.side.supported && capabilities.overlay.supported && capabilities.magnifier.supported, "runtime-backed roles were not exposed");

let workspace = createViewWorkspace(project);
assert(workspace.instances.length === 1 && workspace.instances[0].role === "primary", "workspace must start with exactly one primary instance");
workspace = openSideView(workspace, project, capabilities);
workspace = openSideView(workspace, project, capabilities);
const sides = sideViewInstances(workspace);
assert(sides.length === 2, "side views are not independent N instances");
assert(sides[0].view_instance_id !== sides[1].view_instance_id, "side view ids are not independent");

workspace = toggleOverlayView(workspace, project, capabilities);
const overlays = overlayViewInstances(workspace);
assert(overlays.length === 1, "overlay instance missing");
assert(overlays[0].render_surface === "target_overlay", "overlay was modeled as a global mode");
assert(overlays[0].target_view_instance_id === workspace.primary_view_instance_id, "overlay did not target the primary coordinate space");
assert(legacySelectedView(workspace) === "overlay", "legacy compatibility selection mismatch");

const withoutSelection = openMagnifierView(workspace, project, capabilities);
assert(withoutSelection === workspace, "magnifier opened without a selected target");
workspace = selectViewTarget(workspace, {
  target_id: "pendulum:bob",
  kind: "committed_renderer_current",
  state_hash: "blake3:frame_2",
  frame_id: 2,
});
workspace = openMagnifierView(workspace, project, capabilities);
const magnifier = sideViewInstances(workspace).find((instance) => instance.role === "magnifier");
assert(magnifier?.temporary === true, "magnifier is not a temporary view instance");
assert(magnifier?.target?.target_id === "pendulum:bob", "magnifier lost its selected target");

const serialized = serializeViewWorkspace(workspace);
assert(!serialized.instances.some((instance) => instance.temporary), "temporary magnifier leaked into durable snapshot");
assert(serialized.selected_target === null, "selected target leaked into durable snapshot");
const hydrated = hydrateViewWorkspace(project, serialized, "primary");
assert(hydrated.instances.filter((instance) => instance.role === "side").length === 2, "durable side instances did not hydrate");
const modernHydration = hydrateViewWorkspaceWithMigration(project, serialized, "overlay");
assert(modernHydration.migration === null, "modern workspace incorrectly reported a legacy migration");
assert(
  modernHydration.workspace.instances.filter((instance) => instance.role === "side").length === 2,
  "legacy selection overrode a modern workspace",
);
const legacySide = hydrateViewWorkspaceWithMigration(project, null, "side");
assert(legacySide.migration?.code === "W_LEGACY_VIEW_SELECTION_MIGRATED", "legacy side migration diagnostic missing");
assert(legacySide.migration?.preserved_world_state === true, "legacy migration did not declare the world-state boundary");
assert(legacySide.workspace.instances.some((instance) => instance.role === "side"), "legacy side did not create an independent instance");
const legacyOverlay = hydrateViewWorkspaceWithMigration(project, null, "overlay");
assert(legacyOverlay.workspace.instances.some((instance) => instance.role === "overlay"), "legacy overlay did not target an independent overlay instance");
const legacyMagnifier = hydrateViewWorkspaceWithMigration(project, null, "magnifier");
assert(legacyMagnifier.migration?.resolved_role === "primary", "targetless legacy magnifier did not deterministically fall back to primary");
assert(legacyMagnifier.workspace.instances.length === 1, "targetless legacy magnifier created a temporary instance");
const legacyFamily = hydrateViewWorkspaceWithMigration(project, null, "space2d");
assert(legacyFamily.migration?.resolved_role === "primary", "legacy selected-view family did not deterministically select primary");
assert(legacyFamily.workspace.active_view_instance_id === legacyFamily.workspace.primary_view_instance_id, "legacy family migration did not focus primary");

workspace = reconcileViewWorkspace(workspace, project, { state_hash: "blake3:frame_3" });
assert(workspace.selected_target === null, "frame change did not clear stale selected target");
assert(!workspace.instances.some((instance) => instance.temporary), "frame change did not close temporary magnifier");
let missingHashWorkspace = createViewWorkspace(project);
missingHashWorkspace = selectViewTarget(missingHashWorkspace, {
  target_id: "pendulum:unbound",
  kind: "committed_renderer_current",
  frame_id: 2,
});
missingHashWorkspace = openMagnifierView(missingHashWorkspace, project, capabilities);
missingHashWorkspace = reconcileViewWorkspace(missingHashWorkspace, project, { state_hash: "blake3:frame_3" });
assert(missingHashWorkspace.selected_target === null, "unbound target was retained across a committed frame");
assert(
  !missingHashWorkspace.instances.some((instance) => instance.temporary),
  "unbound target retained a temporary magnifier",
);
workspace = closeViewInstance(workspace, sides[0].view_instance_id);
assert(sideViewInstances(workspace).filter((instance) => instance.role === "side").length === 1, "individual side close failed");
workspace = closeAllSideViews(workspace);
assert(sideViewInstances(workspace).length === 0, "close-all retained a side surface");
workspace = toggleOverlayView(workspace, project, capabilities);
assert(overlayViewInstances(workspace).length === 0, "overlay toggle did not close its independent instance");

const unavailable = viewRoleCapabilities(project, null, { status: "awaiting_committed_frame" });
assert(!unavailable.side.supported && !unavailable.overlay.supported && !unavailable.magnifier.supported, "pre-run UI advertised unavailable role content");

console.log("seamgrim_workbench_view_instance_model: ok");
