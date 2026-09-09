#!/usr/bin/env node

import fs from "node:fs/promises";
import http from "node:http";
import path from "node:path";
import { chromium } from "playwright";

const ROOT = process.cwd();
const START_PATH = "/solutions/seamgrim_ui_mvp/ui/workbench/index.html";

function mimeType(file) {
  if (file.endsWith(".html")) return "text/html; charset=utf-8";
  if (file.endsWith(".js")) return "application/javascript; charset=utf-8";
  if (file.endsWith(".css")) return "text/css; charset=utf-8";
  if (file.endsWith(".json") || file.endsWith(".detjson")) return "application/json; charset=utf-8";
  if (file.endsWith(".wasm")) return "application/wasm";
  if (file.endsWith(".ddn") || file.endsWith(".toml") || file.endsWith(".md")) return "text/plain; charset=utf-8";
  return "application/octet-stream";
}

function createServer() {
  const resolvedRoot = path.resolve(ROOT);
  const server = http.createServer(async (req, res) => {
    try {
      const url = new URL(req.url || "/", "http://127.0.0.1");
      const rel = decodeURIComponent(url.pathname === "/" ? START_PATH : url.pathname).replace(/^\/+/, "");
      const file = path.resolve(resolvedRoot, rel);
      if (file !== resolvedRoot && !file.startsWith(`${resolvedRoot}${path.sep}`)) {
        res.writeHead(403);
        res.end("forbidden");
        return;
      }
      const bytes = await fs.readFile(file);
      res.writeHead(200, {
        "content-type": mimeType(file),
        "cache-control": "no-store",
        "access-control-allow-origin": "*",
      });
      res.end(bytes);
    } catch (_) {
      res.writeHead(404, { "content-type": "text/plain; charset=utf-8" });
      res.end("not found");
    }
  });
  return new Promise((resolve, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", () => {
      const address = server.address();
      if (!address || typeof address === "string") return reject(new Error("server bind failed"));
      resolve({ server, baseUrl: `http://127.0.0.1:${address.port}` });
    });
  });
}

async function closeServer(server) {
  await new Promise((resolve) => server.close(resolve));
}

async function canvasProbe(page) {
  return page.evaluate(() => {
    const canvas = document.querySelector("[data-testid='bogae-canvas']");
    const ctx = canvas.getContext("2d", { willReadFrequently: true });
    const pixels = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
    let hash = 0x811c9dc5;
    let nonWhite = 0;
    for (let index = 0; index < pixels.length; index += 1) {
      hash ^= pixels[index];
      hash = Math.imul(hash, 0x01000193) >>> 0;
      if (index % 4 === 0 && pixels[index + 3] && (pixels[index] < 240 || pixels[index + 1] < 240 || pixels[index + 2] < 240)) {
        nonWhite += 1;
      }
    }
    return {
      width: canvas.width,
      height: canvas.height,
      pixel_fnv1a32: hash.toString(16).padStart(8, "0"),
      non_white_pixels: nonWhite,
      project_run_bound: canvas.dataset.projectRunBound,
      view_artifact_hash: canvas.dataset.viewArtifactHash,
    };
  });
}

async function selectProject(page, projectId) {
  await page.click(`[data-testid='project-card-${projectId}']`);
  await page.waitForSelector(`[data-testid='approved-workbench-root'][data-project-id='${projectId}']`);
}

async function main() {
  const { server, baseUrl } = await createServer();
  let browser = null;
  try {
    browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({ viewport: { width: 1440, height: 900 }, locale: "ko-KR" });
    const page = await context.newPage();
    const browserEvents = [];
    page.on("console", (message) => {
      if (["warning", "error"].includes(message.type())) browserEvents.push(`${message.type()}: ${message.text()}`);
    });
    page.on("pageerror", (error) => browserEvents.push(`pageerror: ${error.message}`));
    page.on("response", (response) => {
      if (response.status() >= 400) browserEvents.push(`response ${response.status()}: ${response.url()}`);
    });

    await page.goto(`${baseUrl}${START_PATH}`, { waitUntil: "networkidle" });
    await page.screenshot({ path: "output/playwright/g0-workbench-first-viewport.png", fullPage: false });
    const firstViewport = await page.evaluate(() => {
      const describe = (testid) => {
        const node = document.querySelector(`[data-testid='${testid}']`);
        const rect = node?.getBoundingClientRect();
        const style = node ? getComputedStyle(node) : null;
        return {
          testid,
          present: Boolean(node),
          visible: Boolean(node && style.display !== "none" && style.visibility !== "hidden" && rect.width > 0 && rect.height > 0),
          top: rect ? Math.round(rect.top) : null,
          bottom: rect ? Math.round(rect.bottom) : null,
          height: rect ? Math.round(rect.height) : null,
          intersects_first_viewport: Boolean(rect && rect.top < innerHeight && rect.bottom > 0),
        };
      };
      const managementInputs = Array.from(document.querySelectorAll("[data-testid='portable-metadata-panel'] input, [data-testid='portable-metadata-panel'] select"))
        .filter((node) => {
          const rect = node.getBoundingClientRect();
          const style = getComputedStyle(node);
          return style.display !== "none" && style.visibility !== "hidden" && rect.top < innerHeight && rect.bottom > 0;
        });
      return {
        viewport: { width: innerWidth, height: innerHeight },
        management_input_count_in_first_viewport: managementInputs.length,
        sections: [
          describe("project-server-panel"),
          describe("portable-metadata-panel"),
          describe("lifecycle-run"),
          describe("source-panel"),
          describe("bogae-panel"),
        ],
      };
    });

    await selectProject(page, "rep_phys_pendulum_wave1_v1");
    const pendulumSource = await page.inputValue("[data-testid='source-editor']");
    const pendulumBeforeRun = await canvasProbe(page);
    await page.click("[data-testid='lifecycle-run']");
    await page.waitForFunction(() => {
      const status = document.querySelector("[data-testid='run-status']")?.textContent ?? "";
      const madi = document.querySelector("[data-testid='current-madi']")?.textContent ?? "";
      return !status.includes("loading") && !madi.endsWith("-");
    }, null, { timeout: 10_000 });
    const pendulumAfterRun = {
      current_madi: await page.textContent("[data-testid='current-madi']"),
      run_status: await page.textContent("[data-testid='run-status']"),
      canvas: await canvasProbe(page),
    };
    await page.waitForTimeout(1_500);
    const pendulumAfterDelay = {
      current_madi: await page.textContent("[data-testid='current-madi']"),
      run_status: await page.textContent("[data-testid='run-status']"),
      canvas: await canvasProbe(page),
    };
    await page.screenshot({ path: "output/playwright/g0-pendulum-after-run.png", fullPage: false });

    await selectProject(page, "rep_phys_projectile_xy_v1");
    const projectileSourceBefore = await page.inputValue("[data-testid='source-editor']");
    const projectileCanvasBefore = await canvasProbe(page);
    const projectileObservationsBefore = await page.textContent("[data-testid='semantic-observations']");
    await page.evaluate(() => {
      const editor = document.querySelector("[data-testid='source-editor']");
      editor.value = editor.value
        .replace("초기속도x: 수 <- (8.0)", "초기속도x: 수 <- (18.0)")
        .replace("중력가속도: 수 <- (9.8)", "중력가속도: 수 <- (20.0)")
        .replace("dt: 수 <- (0.1)", "dt: 수 <- (0.5)");
      editor.dispatchEvent(new Event("input", { bubbles: true }));
    });
    await page.waitForTimeout(100);
    const projectileCanvasAfterUncommittedEdit = await canvasProbe(page);
    const projectileAfterEdit = {
      current_madi: await page.textContent("[data-testid='current-madi']"),
      run_status: await page.textContent("[data-testid='run-status']"),
      source_changed: (await page.inputValue("[data-testid='source-editor']")) !== projectileSourceBefore,
      observations: await page.textContent("[data-testid='semantic-observations']"),
      canvas: projectileCanvasAfterUncommittedEdit,
    };
    await page.screenshot({ path: "output/playwright/g0-projectile-uncommitted-source-view.png", fullPage: false });

    const result = {
      schema: "seamgrim.workbench_recovery.g0_browser_probe.v1",
      url: `${baseUrl}${START_PATH}`,
      first_viewport: firstViewport,
      pendulum: {
        source_has_every_madi_hook: pendulumSource.includes("(매마디)마다"),
        before_run_canvas: pendulumBeforeRun,
        after_run: pendulumAfterRun,
        after_1500ms: pendulumAfterDelay,
        madi_auto_advanced: pendulumAfterRun.current_madi !== pendulumAfterDelay.current_madi,
        canvas_auto_changed: pendulumAfterRun.canvas.pixel_fnv1a32 !== pendulumAfterDelay.canvas.pixel_fnv1a32,
      },
      projectile: {
        source_has_every_madi_hook: projectileSourceBefore.includes("(매마디)마다"),
        observations_before_uncommitted_edit: projectileObservationsBefore,
        before_uncommitted_edit_canvas: projectileCanvasBefore,
        after_uncommitted_edit: projectileAfterEdit,
        uncommitted_source_changed_canvas: projectileCanvasBefore.pixel_fnv1a32 !== projectileCanvasAfterUncommittedEdit.pixel_fnv1a32,
      },
      browser_events: browserEvents,
    };
    console.log(JSON.stringify(result, null, 2));
    await context.close();
  } finally {
    if (browser) await browser.close();
    await closeServer(server);
  }
}

main().catch((error) => {
  console.error(error?.stack || error?.message || String(error));
  process.exit(1);
});
