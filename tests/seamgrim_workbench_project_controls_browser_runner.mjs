#!/usr/bin/env node

import fs from "node:fs/promises";
import http from "node:http";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function mimeType(file) {
  if (file.endsWith(".html")) return "text/html; charset=utf-8";
  if (file.endsWith(".js") || file.endsWith(".mjs")) return "application/javascript; charset=utf-8";
  if (file.endsWith(".json") || file.endsWith(".detjson")) return "application/json; charset=utf-8";
  if (file.endsWith(".wasm")) return "application/wasm";
  if (file.endsWith(".css")) return "text/css; charset=utf-8";
  return "application/octet-stream";
}

async function serve(root) {
  const resolvedRoot = path.resolve(root);
  const server = http.createServer(async (req, res) => {
    try {
      const url = new URL(req.url || "/", "http://127.0.0.1");
      const relative = decodeURIComponent(url.pathname === "/"
        ? "/solutions/seamgrim_ui_mvp/ui/workbench/index.html"
        : url.pathname).replace(/^\/+/, "");
      const file = path.resolve(resolvedRoot, relative);
      if (file !== resolvedRoot && !file.startsWith(`${resolvedRoot}${path.sep}`)) {
        res.writeHead(403).end("forbidden");
        return;
      }
      const bytes = await fs.readFile(file);
      res.writeHead(200, { "content-type": mimeType(file), "cache-control": "no-store" });
      res.end(bytes);
    } catch (_) {
      res.writeHead(404).end("not found");
    }
  });
  await new Promise((resolve, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", resolve);
  });
  const address = server.address();
  assert(address && typeof address !== "string", "server address unavailable");
  return { server, baseUrl: `http://127.0.0.1:${address.port}` };
}

async function closeServer(server) {
  await new Promise((resolve) => server.close(resolve));
}

async function snapshot(page) {
  return page.evaluate(() => window.__SEAMGRIM_APPROVED_WORKBENCH__.getSnapshot());
}

async function waitForControls(page, projectId) {
  await page.waitForFunction((expected) => {
    const snap = window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.();
    return snap?.projectId === expected
      && snap?.projectControls?.project_id === expected
      && snap?.projectControls?.status === "ready";
  }, projectId, { timeout: 60000 });
  return snapshot(page);
}

async function selectProject(page, projectId) {
  await page.click(`[data-testid='project-card-${projectId}']`);
  return waitForControls(page, projectId);
}

async function main() {
  const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
  const { server, baseUrl } = await serve(root);
  let browser = null;
  const pageErrors = [];
  try {
    browser = await chromium.launch({ headless: true });
    const page = await browser.newPage({ viewport: { width: 1360, height: 900 }, locale: "ko-KR" });
    page.on("pageerror", (err) => pageErrors.push(err.message));
    await page.goto(`${baseUrl}/solutions/seamgrim_ui_mvp/ui/workbench/index.html`, { waitUntil: "networkidle" });
    let snap = await waitForControls(page, "rep_phys_projectile_xy_v1");

    const projectileNames = snap.projectControls.controls.map((control) => control.name);
    assert(
      projectileNames.join(",") === "초기속도x,초기속도y,중력가속도,dt,마디수",
      `projectile controls did not come from its WASM maegim plan: ${JSON.stringify(projectileNames)}`,
    );
    assert(snap.projectControls.source === "rust_wasm_authoring_plan", "project controls did not report Rust/WASM authority");
    assert(snap.projectControls.authoring_plan_hash, "project authoring-plan hash missing");
    assert(await page.locator("[data-testid='setup-control-list'] input").count() === projectileNames.length, "setup DOM does not match the current plan");
    assert(!(await page.locator("[data-testid='action-controls']").isVisible()), "action UI appeared without a project action map");
    assert(await page.locator("[data-testid='action-left']").count() === 0, "global left arrow survived without an action map");

    const gravity = page.locator("[data-testid='setup-control-list'] input[data-control-name='중력가속도']");
    await gravity.fill("12.3");
    await page.click("[data-testid='setup-apply']");
    snap = await snapshot(page);
    assert(snap.pendingRecipe?.schema === "seamgrim.workbench.run_recipe_candidate.v1", "setup change did not create a run recipe candidate");
    assert(snap.pendingRecipe?.values?.중력가속도 === 12.3, `recipe did not capture gravity: ${JSON.stringify(snap.pendingRecipe)}`);
    assert(snap.activeFrame === null, "setup recipe mutated a world before a new run");

    await page.click("[data-testid='lifecycle-run']");
    await page.waitForFunction(() => {
      const snap = window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.();
      return Boolean(snap?.activeFrame) || snap?.executionLifecycle?.status === "failed";
    }, null, { timeout: 60000 });
    snap = await snapshot(page);
    assert(
      Math.abs(Number(snap.activeFrame?.wasm_state?.param_overrides?.중력가속도) - 12.3) < 1e-6,
      `WASM run did not apply the recipe override: ${JSON.stringify({ lifecycle: snap.executionLifecycle, setup: snap.runs[0]?.setup, diagnostics: snap.diagnostics, params: snap.activeFrame?.wasm_state?.param_overrides })}`,
    );
    assert(snap.runs[0]?.setup?.values?.중력가속도 === 12.3, "sealed run did not retain its setup recipe");
    assert(snap.pendingRecipe === null, "accepted recipe was not consumed by the new run");
    if (snap.executionLifecycle.status === "running") {
      await page.click("[data-testid='lifecycle-pause']");
      await page.waitForFunction(() => window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.()?.executionLifecycle?.status === "paused");
    }
    snap = await snapshot(page);
    const committedHashBeforeNextRecipe = snap.activeFrame.state_hash;
    const committedGravityBeforeNextRecipe = snap.activeFrame.wasm_state.param_overrides.중력가속도;
    await gravity.fill("10.7");
    await page.click("[data-testid='setup-apply']");
    snap = await snapshot(page);
    assert(snap.pendingRecipe?.values?.중력가속도 === 10.7, "active-run setup change did not remain a next-run candidate");
    assert(snap.activeFrame.state_hash === committedHashBeforeNextRecipe, "setup candidate mutated the committed active run");
    assert(snap.activeFrame.wasm_state.param_overrides.중력가속도 === committedGravityBeforeNextRecipe, "setup candidate changed the active VM parameter");

    snap = await selectProject(page, "rep_phys_pendulum_wave1_v1");
    const pendulumNames = snap.projectControls.controls.map((control) => control.name);
    assert(
      pendulumNames.join(",") === "g,L,theta0,omega0,damp,dt,t_max",
      `pendulum controls did not replace projectile controls: ${JSON.stringify(pendulumNames)}`,
    );
    assert(!pendulumNames.includes("중력가속도") && !pendulumNames.includes("초기속도x"), "previous project controls leaked after switch");
    assert(snap.pendingRecipe === null && snap.nextInput === null, "project switch retained pending world input");
    assert(!(await page.locator("[data-testid='action-controls']").isVisible()), "pendulum advertised actions without an action map");

    snap = await selectProject(page, "rep_grid_game_state_drop_v1");
    assert(snap.projectControls.controls.length === 0, `grid advertised undeclared setup controls: ${JSON.stringify(snap.projectControls.controls)}`);
    assert(!(await page.locator("[data-testid='setup-controls']").isVisible()), "empty setup card occupied the first screen");
    assert(await page.locator("[data-testid='action-controls']").isVisible(), "declared grid action map did not create action UI");
    assert(snap.projectControls.actions.map((action) => action.action_id).join(",") === "left,right,drop", "grid action map order/content mismatch");
    assert(snap.projectControls.action_map_hash, "grid action-map hash missing");

    await page.click("[data-testid='action-drop']");
    snap = await snapshot(page);
    assert(snap.nextInput?.action_id === "drop", "action did not identify its declared action-map row");
    assert(snap.nextInput?.intent === "drop" && snap.nextInput?.keys === 4 && snap.nextInput?.lastKey === "ArrowDown", "action did not create the declared next InputSnapshot");
    assert(snap.nextInput?.action_map_hash === snap.projectControls.action_map_hash, "queued input lost action-map lineage");
    const queuedDropInputId = snap.nextInput.input_id;

    await page.click("[data-testid='lifecycle-run']");
    await page.waitForFunction(() => {
      const snap = window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.();
      return snap?.runs?.[0]?.input_snapshots?.some((input) => input?.action_id === "drop");
    }, null, { timeout: 60000 });
    snap = await snapshot(page);
    const dropInputs = snap.runs[0].input_snapshots.filter((input) => input?.action_id === "drop");
    assert(
      dropInputs.length === 1,
      `declared action committed ${dropInputs.length} times instead of once: ${JSON.stringify(snap.runs[0].input_snapshots)}`,
    );
    assert(!snap.runs[0].input_snapshots[0]?.action_id, "live reset frame falsely recorded a queued world action");
    assert(dropInputs[0].input_id === queuedDropInputId, "committed InputSnapshot lost its queued input identity");
    assert(dropInputs[0].action_map_hash === snap.projectControls.action_map_hash, "committed InputSnapshot lost action-map lineage");

    snap = await selectProject(page, "rep_phys_pendulum_wave1_v1");
    assert(snap.nextInput === null, "queued action leaked into the next project");
    assert(await page.locator("[data-testid='action-left']").count() === 0, "grid action DOM leaked into a project without an action map");
    assert(!(await page.locator("[data-testid='action-controls']").isVisible()), "action card remained visible after project switch");

    const viewBefore = structuredClone(snap.viewWorkspace);
    await page.click("[data-testid='lifecycle-run']");
    await page.waitForFunction(() => Boolean(window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.()?.activeFrame));
    await page.click("[data-testid='lifecycle-pause']");
    await page.waitForFunction(() => window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.()?.executionLifecycle?.status === "paused");
    const hashBeforeView = (await snapshot(page)).activeFrame.state_hash;
    await page.click("[data-testid='view-role-side']");
    snap = await snapshot(page);
    assert(snap.activeFrame.state_hash === hashBeforeView, "view setting entered the world state hash");
    assert(snap.pendingRecipe === null && snap.nextInput === null, "view setting created a setup recipe or InputSnapshot");
    assert(snap.viewWorkspace.instances.length > viewBefore.instances.length, "view setting did not stay in the view snapshot");

    assert(pageErrors.length === 0, `page errors: ${pageErrors.join(" | ")}`);
    console.log("seamgrim_workbench_project_controls_browser: ok");
  } finally {
    if (browser) await browser.close();
    await closeServer(server);
  }
}

main().catch((err) => {
  console.error(err?.stack || err?.message || String(err));
  process.exit(1);
});
