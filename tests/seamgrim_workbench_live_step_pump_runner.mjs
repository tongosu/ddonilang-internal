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
  if (file.endsWith(".js")) return "application/javascript; charset=utf-8";
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
  return page.evaluate(() => window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.());
}

async function createSingleProject(page, name) {
  const previous = await snapshot(page);
  await page.click("[data-testid='new-ddn-project']");
  await page.waitForSelector("[data-testid='project-create-dialog'][open]");
  await page.fill("[data-testid='project-create-name']", name);
  await page.check("input[name='project-template'][value='single']");
  await page.click("[data-testid='project-create-submit']");
  await page.waitForFunction(
    (previousId) => {
      const current = window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.();
      return current?.projectId !== previousId && current?.project?.native_creator === true;
    },
    previous?.projectId ?? "",
  );
}

async function waitForState(page, state) {
  try {
    await page.waitForFunction(
      (expected) => window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.()?.executionLifecycle?.status === expected,
      state,
      { timeout: 60000 },
    );
  } catch (err) {
    const current = await snapshot(page).catch(() => null);
    throw new Error(`state ${state} timeout: ${JSON.stringify(current)}\n${err?.message ?? err}`);
  }
  return snapshot(page);
}

async function main() {
  const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
  const { server, baseUrl } = await serve(root);
  let browser = null;
  const pageErrors = [];
  try {
    browser = await chromium.launch({ headless: true });
    const page = await browser.newPage({ viewport: { width: 1280, height: 720 }, locale: "ko-KR" });
    page.on("pageerror", (err) => pageErrors.push(err.message));
    await page.goto(`${baseUrl}/solutions/seamgrim_ui_mvp/ui/workbench/index.html`, { waitUntil: "networkidle" });
    await page.waitForFunction(() => Boolean(window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.()));

    await createSingleProject(page, "직렬 자동 펌프");
    const longLiveSource = `설정 {
  제목: "직렬 자동 펌프".
  마디수: 50.
}.

채비 {
  값: 수 <- 0.
}.

(매마디)마다 {
  값 <- 값 + 1.
  값 보여주기.
}.`;
    await page.fill("[data-testid='source-editor']", longLiveSource);
    await page.click("[data-testid='lifecycle-run']");
    await page.waitForFunction(() => {
      const snap = window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.();
      return snap?.executionLifecycle?.status === "running"
        && Number(snap?.runs?.[0]?.committed_step_count ?? 0) >= 2;
    }, null, { timeout: 60000 });
    let snap = await snapshot(page);
    const runId = snap.activeRunId;
    assert(snap.livePump.step_commit_count >= 2, "live run did not advance without another click");
    assert(snap.livePump.max_in_flight === 1, `more than one WASM step was in flight: ${JSON.stringify(snap.livePump)}`);

    await page.click("[data-testid='lifecycle-pause']");
    snap = await waitForState(page, "paused");
    const pausedCount = snap.runs[0].committed_step_count;
    await page.waitForTimeout(180);
    snap = await snapshot(page);
    assert(snap.runs[0].committed_step_count === pausedCount, "pause advanced beyond its committed boundary");
    assert(!snap.livePump.in_flight && !snap.livePump.scheduled, "paused pump retained work");
    const semanticBeforeViewChange = snap.semanticViewPayload;
    assert(semanticBeforeViewChange?.committed_frame?.run_id === snap.activeRunId, "semantic payload run identity mismatch");
    assert(semanticBeforeViewChange?.committed_frame?.frame_id === snap.activeFrame.frame_id, "semantic payload frame identity mismatch");
    assert(semanticBeforeViewChange?.committed_frame?.state_hash === snap.activeFrame.state_hash, "semantic payload state hash mismatch");
    assert(semanticBeforeViewChange?.ordered_observations?.length > 0, "semantic payload observations missing");
    const canvasBinding = await page.evaluate(() => {
      const canvas = document.querySelector("[data-testid='bogae-canvas']");
      return {
        bound: canvas?.dataset?.committedFrameBound,
        stateHash: canvas?.dataset?.committedStateHash,
        payloadHash: canvas?.dataset?.semanticPayloadHash,
        viewArtifactHash: canvas?.dataset?.viewArtifactHash,
      };
    });
    assert(canvasBinding.bound === "true", "canvas is not bound to a committed semantic frame");
    assert(canvasBinding.stateHash === snap.activeFrame.state_hash, "canvas committed state hash mismatch");
    assert(canvasBinding.payloadHash === semanticBeforeViewChange.semantic_payload_hash, "canvas semantic payload hash mismatch");
    await page.click("[data-mode='bogae-main']");
    const alternateView = await snapshot(page);
    assert(alternateView.activeFrame.state_hash === snap.activeFrame.state_hash, "view config changed runtime state hash");
    assert(alternateView.semanticViewPayload.semantic_payload_hash !== semanticBeforeViewChange.semantic_payload_hash, "view config did not change semantic payload hash");
    assert(alternateView.semanticViewPayload.view_config.participates_in_state_hash === false, "view config entered runtime hash boundary");
    await page.click("[data-mode='ddn-main']");
    const restoredPrimary = await snapshot(page);
    const restoredArtifactHash = await page.locator("[data-testid='bogae-canvas']").getAttribute("data-view-artifact-hash");
    assert(restoredPrimary.semanticViewPayload.semantic_payload_hash === semanticBeforeViewChange.semantic_payload_hash, "same frame and restored view config changed semantic payload hash");
    assert(restoredArtifactHash === canvasBinding.viewArtifactHash, "same frame and restored view config changed view artifact hash");

    assert(!(await page.locator("[data-testid='action-controls']").isVisible()), "project without an action map advertised global actions");
    await page.click("[data-testid='lifecycle-step']");
    await page.waitForFunction(
      (count) => window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.()?.runs?.[0]?.committed_step_count === count + 1,
      pausedCount,
      { timeout: 60000 },
    );
    snap = await snapshot(page);
    assert(snap.executionLifecycle.status === "paused", "manual step did not remain paused");
    assert(snap.activeFrame.input_snapshot.intent === "step", "manual step did not record its InputSnapshot boundary");
    assert(snap.nextInput === null, "project without an action map created a queued action");
    await page.click("[data-testid='lifecycle-step']");
    await page.waitForFunction(
      (count) => window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.()?.runs?.[0]?.committed_step_count === count + 2,
      pausedCount,
      { timeout: 60000 },
    );
    const actionIntentCount = (await snapshot(page)).runs[0].input_snapshots
      .filter((input) => input?.action_id).length;
    assert(actionIntentCount === 0, `project without an action map committed ${actionIntentCount} actions`);

    const sealedSourceHash = snap.runs[0].source_hash;
    await page.fill("[data-testid='source-editor']", '"새 실행 후보" 보여주기.');
    await page.click("[data-testid='lifecycle-step']");
    await page.waitForFunction(
      (count) => window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.()?.runs?.[0]?.committed_step_count === count + 3,
      pausedCount,
      { timeout: 60000 },
    );
    snap = await snapshot(page);
    assert(snap.executionLifecycle.status === "paused", "source candidate changed the sealed active run");
    assert(snap.runs[0].source_hash === sealedSourceHash, "source candidate mutated active run source hash");

    const beforeResume = snap.runs[0].committed_step_count;
    await page.click("[data-testid='lifecycle-resume']");
    await page.waitForFunction(
      ({ id, count }) => {
        const snap = window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.();
        const run = snap?.runs?.find((row) => row.run_id === id);
        return snap?.executionLifecycle?.status === "running" && Number(run?.committed_step_count ?? 0) >= count + 2;
      },
      { id: runId, count: beforeResume },
      { timeout: 60000 },
    );
    snap = await snapshot(page);
    assert(snap.activeRunId === runId && snap.runs.length === 1, "resume created a different run");

    const stopResults = await page.evaluate(async () => {
      const api = window.__SEAMGRIM_APPROVED_WORKBENCH__;
      const first = api.stopRun();
      const second = api.stopRun();
      return Promise.all([first, second]);
    });
    assert(stopResults[0] === true && stopResults[1] === false, `duplicate stop mismatch: ${JSON.stringify(stopResults)}`);
    snap = await waitForState(page, "done");
    assert(snap.runs[0].final_status === "stopped", "stop did not finalize the run once");
    assert(snap.livePump.max_in_flight === 1, "serial pump invariant regressed after resume");

    await createSingleProject(page, "설정 마디 자동 완료");
    const boundedLiveSource = `설정 {
  제목: "설정 마디 자동 완료".
  마디수: 3.
}.

채비 {
  값: 수 <- 0.
}.

(매마디)마다 {
  값 <- 값 + 1.
}.`;
    await page.fill("[data-testid='source-editor']", boundedLiveSource);
    await page.click("[data-testid='lifecycle-run']");
    snap = await waitForState(page, "done");
    assert(snap.executionLifecycle.mode === "live", "bounded live source lost live mode");
    assert(snap.runs[0].configured_madi === 3, `configured madi mismatch: ${JSON.stringify(snap.runs[0])}`);
    assert(snap.runs[0].committed_step_count === 3, `bounded run commit count mismatch: ${JSON.stringify(snap.runs[0])}`);
    assert(snap.runs[0].final_status === "completed", "bounded run did not finalize completed");
    assert(snap.livePump.max_in_flight === 1, "bounded run exceeded one step in flight");
    assert(pageErrors.length === 0, `page errors: ${pageErrors.join(" | ")}`);

    console.log("seamgrim_workbench_live_step_pump: ok");
  } finally {
    if (browser) await browser.close();
    await closeServer(server);
  }
}

main().catch((err) => {
  console.error(err?.stack || err?.message || String(err));
  process.exit(1);
});
