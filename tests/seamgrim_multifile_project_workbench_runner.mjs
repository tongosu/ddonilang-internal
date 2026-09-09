#!/usr/bin/env node

import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { createHash } from "node:crypto";
import { spawn } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";
import { chromium } from "playwright";
import { buildProjectSnapshotArtifactV0 } from "../solutions/seamgrim_ui_mvp/ui/project_snapshot.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, "..");
const SERVER = path.resolve(ROOT, "solutions/seamgrim_ui_mvp/tools/ddn_exec_server.py");
const OK = "seamgrim_multifile_project_workbench: ok";
const VIEWPORTS = [
  { width: 1440, height: 900 },
  { width: 1024, height: 768 },
  { width: 778, height: 912 },
  { width: 390, height: 844 },
];
const LONG_FILE_PATH = "lib/아주긴한국어파일이름_진단_겹침_확인용_helper.ddn";

async function resolveEvidenceDir() {
  const candidates = [
    process.env.SEAMGRIM_MULTIFILE_WORKBENCH_EVIDENCE_DIR,
    "I:/home/urihanl/ddn/codex/out/seamgrim_multifile_project_workbench_v1",
    "C:/ddn/codex/out/seamgrim_multifile_project_workbench_v1",
  ].filter(Boolean);
  for (const candidate of candidates) {
    try {
      const dir = path.resolve(String(candidate), "latest");
      await fs.mkdir(dir, { recursive: true });
      return dir;
    } catch (_) {
      // Try the next configured local artifact root.
    }
  }
  const fallback = await fs.mkdtemp(path.join(os.tmpdir(), "seamgrim-workbench-evidence-"));
  return fallback;
}

function viewportLabel(viewport) {
  return `${viewport.width}x${viewport.height}`;
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function base64Utf8(text) {
  return Buffer.from(String(text ?? ""), "utf8").toString("base64");
}

function stableCanonicalJson(value) {
  if (Array.isArray(value)) return `[${value.map((item) => stableCanonicalJson(item)).join(",")}]`;
  if (value && typeof value === "object") {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${stableCanonicalJson(value[key])}`).join(",")}}`;
  }
  return JSON.stringify(value);
}

function stableHash(text) {
  let hash = 0x811c9dc5;
  const source = String(text ?? "");
  for (let index = 0; index < source.length; index += 1) {
    hash ^= source.charCodeAt(index);
    hash = Math.imul(hash, 0x01000193);
  }
  return (hash >>> 0).toString(16).padStart(8, "0");
}

function sha256HexUtf8(text) {
  return createHash("sha256").update(String(text ?? ""), "utf8").digest("hex");
}

function byteLengthUtf8(text) {
  return Buffer.byteLength(String(text ?? ""), "utf8");
}

function cloneJson(value) {
  return JSON.parse(JSON.stringify(value ?? null));
}

function buildProjectRunLineage(summary) {
  const request = summary.execution_preparation?.runtime_request && typeof summary.execution_preparation.runtime_request === "object"
    ? summary.execution_preparation.runtime_request
    : {
      frontdoor: String(summary.frontdoor ?? "wasm_project_run_summary_json"),
      requested_ticks: Number(summary.runtime_execution_envelope?.requested_ticks ?? 1),
      target: String(summary.target ?? "앱"),
      target_path: String(summary.target_path ?? "app/main.ddn"),
    };
  const runRequestHash = `candidate:fnv1a32:project_run_request:${stableHash(stableCanonicalJson(request))}`;
  const lineage = {
    schema: "seamgrim.local_project_run_lineage.v0",
    project_graph_hash: String(summary.project_graph_sha256 ?? ""),
    lock_hash: String(summary.lock_sha256 ?? ""),
    linked_source_hash: String(summary.linked_execution_source_sha256 ?? summary.execution_preparation?.linked_source?.source_sha256 ?? ""),
    run_request_hash: runRequestHash,
    parent_run_id: "",
    branch_madi: null,
    branch_state_hash: "",
    final_state_hash: String(summary.runtime_state_hash ?? ""),
    view_artifact_hash: "",
    created_revision: `fixture:${String(summary.summary_sha256 ?? summary.bounded_state_sha256 ?? "run").slice(0, 12)}`,
  };
  return {
    ...lineage,
    lineage_hash: `candidate:fnv1a32:project_run_lineage:${stableHash(stableCanonicalJson(lineage))}`,
  };
}

function freePort() {
  return new Promise((resolve, reject) => {
    import("node:net").then(({ default: net }) => {
      const server = net.createServer();
      server.once("error", reject);
      server.listen(0, "127.0.0.1", () => {
        const address = server.address();
        const port = address && typeof address !== "string" ? address.port : 0;
        server.close(() => resolve(port));
      });
    }).catch(reject);
  });
}

async function startServer(existingDataDir = "") {
  const dataDir = existingDataDir || await fs.mkdtemp(path.join(os.tmpdir(), "seamgrim-g11-viewports-"));
  const port = await freePort();
  const child = spawn(process.env.PYTHON || "python", [SERVER, "--host", "127.0.0.1", "--port", String(port)], {
    cwd: ROOT,
    env: { ...process.env, SEAMGRIM_PROJECT_DATA_DIR: dataDir },
    stdio: ["ignore", "pipe", "pipe"],
  });
  child.stdout.on("data", () => {});
  child.stderr.on("data", () => {});
  const baseUrl = `http://127.0.0.1:${port}`;
  for (let index = 0; index < 100; index += 1) {
    if (child.exitCode !== null) throw new Error(`server exited: ${child.exitCode}`);
    try {
      const response = await fetch(`${baseUrl}/api/v1/projects/health`);
      if (response.ok) return { child, baseUrl, dataDir };
    } catch (_) {
      await new Promise((resolve) => setTimeout(resolve, 100));
    }
  }
  throw new Error("server health timeout");
}

function rebaseProjectLink(link, baseUrl) {
  const source = new URL(String(link));
  const base = new URL(String(baseUrl));
  return `${base.origin}${source.pathname}${source.search}${source.hash}`;
}

async function stopServer(child) {
  if (!child || child.exitCode !== null) return;
  child.kill();
  await new Promise((resolve) => child.once("exit", resolve));
}

async function initWasm() {
  const uiDir = path.join(ROOT, "solutions", "seamgrim_ui_mvp", "ui");
  const wasmModule = await import(pathToFileURL(path.join(uiDir, "wasm", "ddonirang_tool.js")).href);
  const wasmBytes = await fs.readFile(path.join(uiDir, "wasm", "ddonirang_tool_bg.wasm"));
  if (typeof wasmModule.default === "function") {
    await wasmModule.default({ module_or_path: wasmBytes });
  }
  for (const name of ["wasm_normalize_project_source_json", "wasm_project_gaji_lock_json", "wasm_project_run_summary_json"]) {
    assert(typeof wasmModule[name] === "function", `${name} export missing`);
  }
  return wasmModule;
}

async function loadFixture(name) {
  const file = path.join(ROOT, "pack", "ddn_local_project_graph_v1", "fixtures", name);
  return JSON.parse(await fs.readFile(file, "utf8"));
}

function withLongKoreanFile(source) {
  const next = JSON.parse(JSON.stringify(source));
  next.files = Array.isArray(next.files) ? next.files : [];
  if (!next.files.some((file) => file.path === LONG_FILE_PATH)) {
    next.files.push({
      path: LONG_FILE_PATH,
      role: "ddn_source",
      utf8_text: `드러냄 {
긴값.
}
긴값 <- 99.
`,
    });
  }
  return next;
}

function buildDynamicCounterSource() {
  return {
    schema: "ddn.virtual_project_source.v1",
    kind: "seamgrim.local_project_tree.v0",
    root_path: "뿌리.ddn",
    entry_path: "app/main.ddn",
    files: [
      {
        path: "뿌리.ddn",
        role: "root",
        utf8_text: `프로젝트 {
  이름: "dynamic-lifecycle".
  첫글: "./app/main.ddn".
  목표 { 앱: "./app/main.ddn". }
  모듈길 { 로컬: "./lib". }
}.
`,
      },
      {
        path: "lib/counter.ddn",
        role: "ddn_source",
        utf8_text: `드러냄 { count. }
(시작)할때 {
  count <- 0.
}.
(매마디)마다 {
  count <- count + 1.
}.
`,
      },
      {
        path: "app/main.ddn",
        role: "ddn_source",
        utf8_text: `쓰임 { 계수: "./lib/counter". }
(매마디)마다 {
  계수.count 보여주기.
}.
`,
      },
    ],
  };
}

function replaceFileText(source, filePath, oldText, newText) {
  const next = JSON.parse(JSON.stringify(source));
  const file = next.files.find((row) => String(row?.path ?? "") === filePath);
  assert(file, `file not found for replacement: ${filePath}`);
  const text = String(file.utf8_text ?? "");
  assert(text.includes(oldText), `replacement source not found in ${filePath}`);
  file.utf8_text = text.replace(oldText, newText);
  return next;
}

function withRefreshedLock(wasmModule, source) {
  const next = JSON.parse(JSON.stringify(source));
  next.files = Array.isArray(next.files) ? next.files : [];
  const withoutLock = {
    ...next,
    files: next.files.filter((file) => String(file?.path ?? "") !== "ddn.lock"),
  };
  const lockText = String(wasmModule.wasm_project_gaji_lock_json(JSON.stringify(withoutLock)) ?? "").trimEnd();
  next.files = next.files.filter((file) => String(file?.path ?? "") !== "ddn.lock");
  next.files.splice(1, 0, {
    path: "ddn.lock",
    role: "lock",
    utf8_text: `${lockText}\n`,
  });
  return next;
}

async function buildArtifactFromVirtualSource(wasmModule, source, {
  projectName = "G11 대표 로컬 프로젝트",
  sourceLessonId = "rep_phys_projectile_xy_v1",
} = {}) {
  const normalized = JSON.parse(wasmModule.wasm_normalize_project_source_json(JSON.stringify(source)));
  const summary = JSON.parse(wasmModule.wasm_project_run_summary_json(JSON.stringify(source), "앱", true, true));
  const sourceFiles = new Map((source.files ?? []).map((file) => [String(file.path ?? ""), file]));
  const files = (normalized.files ?? []).map((file) => {
    const sourceFile = sourceFiles.get(String(file.path ?? "")) ?? {};
    return {
      path: String(file.path ?? ""),
      role: String(file.role ?? "ddn_source"),
      utf8_text: String(sourceFile.utf8_text ?? sourceFile.text ?? ""),
      byte_length: Number(file.byte_length ?? 0),
      sha256: String(file.sha256 ?? ""),
    };
  });
  const entry = files.find((file) => file.path === String(source.entry_path ?? normalized.entry_path ?? ""));
  const payload = {
    schema: "seamgrim.local_project_tree_payload.v0",
    kind: "seamgrim.local_project_tree.v0",
    root_path: String(source.root_path ?? "."),
    entry_path: String(source.entry_path ?? normalized.entry_path ?? "app/main.ddn"),
    files,
    project_graph_sha256: String(summary.project_graph_sha256 ?? normalized.project_graph_sha256 ?? ""),
    lock_sha256: String(summary.lock_sha256 ?? normalized.lock_sha256 ?? ""),
    canonical_manifest_sha256: String(summary.canonical_manifest_sha256 ?? normalized.canonical_manifest_sha256 ?? ""),
    symbol_boundary_sha256: String(summary.symbol_boundary_sha256 ?? ""),
    bounded_state_sha256: String(summary.bounded_state_sha256 ?? ""),
    runtime_state_hash: String(summary.runtime_state_hash ?? ""),
    summary_sha256: String(summary.summary_sha256 ?? ""),
    output_rows: Array.isArray(summary.output_rows) ? summary.output_rows.map((row) => String(row ?? "")) : [],
    project_observation_trace: summary.project_observation_trace ?? null,
    execution_preparation: summary.execution_preparation ?? null,
    run_lineage: buildProjectRunLineage(summary),
    limits: normalized.limits ?? {},
    frontdoor: "wasm_project_run_summary_json",
    state_hash_formula_change: false,
  };
  return {
    artifact: await buildProjectSnapshotArtifactV0({
      projectName,
      ddnText: String(entry?.utf8_text ?? ""),
      sourceLessonId,
      localPackagePayload: payload,
      metadata: {
        title: projectName,
        summary: "G11 viewport evidence fixture",
        tags: ["G11", "multi-file", "viewport"],
        required_gaji: ["edu.physics"],
      },
    }),
    summary,
    manifest: normalized,
  };
}

function payloadFromArtifact(artifact) {
  const payload = artifact?.project_snapshot?.local_package_payload;
  assert(payload && Array.isArray(payload.files), "artifact local package payload missing");
  return cloneJson(payload);
}

function payloadFile(payload, filePath) {
  return (payload.files ?? []).find((file) => String(file?.path ?? "") === filePath) ?? null;
}

function payloadFileText(payload, filePath) {
  const file = payloadFile(payload, filePath);
  assert(file, `payload file not found: ${filePath}`);
  return String(file.utf8_text ?? file.text ?? "");
}

function setPayloadFileText(payload, filePath, text) {
  const next = cloneJson(payload);
  const file = payloadFile(next, filePath);
  assert(file, `payload file not found: ${filePath}`);
  file.utf8_text = String(text ?? "");
  file.byte_length = byteLengthUtf8(file.utf8_text);
  file.sha256 = sha256HexUtf8(file.utf8_text);
  return next;
}

function removePayloadFile(payload, filePath) {
  const next = cloneJson(payload);
  next.files = (next.files ?? []).filter((file) => String(file?.path ?? "") !== filePath);
  return next;
}

function tamperLockJson(lockText, mutator) {
  const lock = JSON.parse(String(lockText ?? ""));
  mutator(lock);
  return `${stableCanonicalJson(lock)}\n`;
}

async function artifactFromPayload(baseArtifact, payload, title, tags = []) {
  const snapshot = baseArtifact.project_snapshot ?? {};
  const entry = payloadFile(payload, String(payload.entry_path ?? "app/main.ddn"))
    ?? (payload.files ?? [])[0]
    ?? { utf8_text: "" };
  return buildProjectSnapshotArtifactV0({
    projectName: title,
    ddnText: String(entry.utf8_text ?? ""),
    sourceLessonId: String(snapshot.source_lesson_id ?? "rep_phys_projectile_xy_v1"),
    localPackagePayload: payload,
    metadata: {
      ...(snapshot.metadata ?? {}),
      title,
      summary: "G11 lock trust boundary attack fixture with valid outer wrapper hash",
      tags: ["G11", "multi-file", "lock-boundary", ...tags],
    },
  });
}

async function buildLockAttackArtifacts(baseArtifact) {
  const payload = payloadFromArtifact(baseArtifact);
  const lockText = payloadFileText(payload, "ddn.lock");
  const tamperedLock = setPayloadFileText(
    payload,
    "ddn.lock",
    tamperLockJson(lockText, (lock) => {
      lock.lock_sha256 = "0".repeat(64);
    }),
  );
  const missingLock = removePayloadFile(payload, "ddn.lock");
  const graphHashLock = setPayloadFileText(
    payload,
    "ddn.lock",
    tamperLockJson(lockText, (lock) => {
      lock.project_graph_sha256 = `tampered:${String(lock.project_graph_sha256 ?? "").slice(0, 24)}`;
    }),
  );
  const packageHashLock = setPayloadFileText(
    payload,
    "ddn.lock",
    tamperLockJson(lockText, (lock) => {
      assert(Array.isArray(lock.packages) && lock.packages.length > 0, "lock packages missing");
      lock.packages[0] = {
        ...lock.packages[0],
        package_sha256: "sha256:tampered-package-pin",
      };
    }),
  );
  return {
    valid_lock_text: lockText,
    tampered_lock: await artifactFromPayload(baseArtifact, tamperedLock, "G11 변조 ddn.lock", ["tampered-lock"]),
    missing_lock: await artifactFromPayload(baseArtifact, missingLock, "G11 누락 ddn.lock", ["missing-lock"]),
    project_graph_hash_tamper: await artifactFromPayload(baseArtifact, graphHashLock, "G11 graph hash 변조 lock", ["project-graph-hash-tamper"]),
    package_pin_hash_tamper: await artifactFromPayload(baseArtifact, packageHashLock, "G11 package pin 변조 lock", ["package-pin-hash-tamper"]),
  };
}

async function writeTempArtifact(prefix, artifact) {
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), `seamgrim-${prefix}-`));
  const file = path.join(dir, `${prefix}.seamgrim-project.json`);
  await fs.writeFile(file, JSON.stringify(artifact, null, 2), "utf8");
  return file;
}

async function canvasNonBlank(page, selector) {
  return page.evaluate((sel) => {
    const canvas = document.querySelector(sel);
    if (!canvas) return false;
    const ctx = canvas.getContext("2d");
    if (!ctx) return false;
    const width = Math.max(1, Math.min(canvas.width, 120));
    const height = Math.max(1, Math.min(canvas.height, 80));
    const data = ctx.getImageData(0, 0, width, height).data;
    let changed = 0;
    for (let index = 0; index < data.length; index += 4) {
      const r = data[index];
      const g = data[index + 1];
      const b = data[index + 2];
      const a = data[index + 3];
      if (a && (r !== 255 || g !== 255 || b !== 255)) changed += 1;
      if (changed > 20) return true;
    }
    return false;
  }, selector);
}

async function canvasFingerprint(page, selector) {
  return page.evaluate((sel) => {
    const canvas = document.querySelector(sel);
    if (!canvas) return null;
    const ctx = canvas.getContext("2d", { willReadFrequently: true });
    if (!ctx) return null;
    const width = Math.max(1, Math.min(canvas.width, 160));
    const height = Math.max(1, Math.min(canvas.height, 100));
    const data = ctx.getImageData(0, 0, width, height).data;
    let hash = 2166136261;
    let changed = 0;
    for (let index = 0; index < data.length; index += 16) {
      const value = data[index] ^ (data[index + 1] << 8) ^ (data[index + 2] << 16) ^ (data[index + 3] << 24);
      hash ^= value;
      hash = Math.imul(hash, 16777619);
      if (data[index + 3] && (data[index] !== 255 || data[index + 1] !== 255 || data[index + 2] !== 255)) changed += 1;
    }
    return {
      hash: (hash >>> 0).toString(16).padStart(8, "0"),
      changed,
      datasetSignature: canvas.dataset.canvasSignature ?? "",
      viewArtifactHash: canvas.dataset.viewArtifactHash ?? "",
      projectRunBound: canvas.dataset.projectRunBound ?? "",
      traceSha256: canvas.dataset.projectRunTraceSha256 ?? "",
      lineageHash: canvas.dataset.projectRunLineageHash ?? "",
    };
  }, selector);
}

async function workbenchProjectRunState(page) {
  return page.evaluate(() => {
    const root = document.querySelector("[data-testid='approved-workbench-root']");
    return {
      executionState: root?.dataset?.projectExecutionState ?? "",
      projectRunBound: root?.dataset?.projectRunBound ?? "",
      trace: root?.dataset?.projectRunTraceSha256 ?? "",
      bounded: root?.dataset?.projectRunBoundedStateSha256 ?? "",
      runtimeStateHash: root?.dataset?.projectRunRuntimeStateHash ?? "",
      lineage: root?.dataset?.projectRunLineageHash ?? "",
      requestHash: root?.dataset?.projectRunRequestHash ?? "",
      createdRevision: root?.dataset?.projectRunCreatedRevision ?? "",
      outputRows: String(root?.dataset?.projectRunOutputRows ?? "").split("|").filter(Boolean),
      previousLineage: root?.dataset?.previousProjectRunLineageHash ?? "",
      failureSourceHash: root?.dataset?.projectRunFailureSourceHash ?? "",
      importedRecordSourceHash: root?.dataset?.importedProjectRecordSourceHash ?? "",
      runStatus: document.querySelector("[data-testid='run-status']")?.textContent ?? "",
      runHash: document.querySelector("[data-testid='run-hash']")?.textContent ?? "",
      runLineage: document.querySelector("[data-testid='run-lineage']")?.textContent ?? "",
      semanticTrace: document.querySelector("[data-testid='semantic-observations']")?.dataset?.traceSha256 ?? "",
      semanticBound: document.querySelector("[data-testid='semantic-observations']")?.dataset?.projectRunBound ?? "",
      semanticRows: [...document.querySelectorAll("[data-testid='semantic-observations'] [data-project-observation-id]")].map((node) => ({
        id: node.getAttribute("data-project-observation-id"),
        name: node.getAttribute("data-project-observation-name"),
        value: node.getAttribute("data-project-observation-value"),
        stateHashParticipation: node.getAttribute("data-state-hash-participation"),
      })),
    };
  });
}

async function workbenchSnapshot(page) {
  return page.evaluate(() => window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.() ?? {});
}

async function workbenchDiagnosticCodes(page) {
  const snapshot = await workbenchSnapshot(page);
  return (snapshot.diagnostics ?? []).map((row) => String(row?.code ?? ""));
}

async function hasWorkbenchFile(page, filePath) {
  return (await page.locator(`[data-file-path="${filePath}"]`).count()) > 0;
}

async function readWorkbenchFile(page, filePath) {
  assert(await hasWorkbenchFile(page, filePath), `workbench file missing: ${filePath}`);
  await page.locator(`[data-file-path="${filePath}"]`).first().click();
  return page.locator("[data-testid='source-editor']").inputValue();
}

async function openPortableProjectFile(page, artifactFile) {
  await page.setInputFiles("[data-testid='portable-project-import-input']", artifactFile);
  await page.waitForFunction(() => document.querySelector("[data-testid='portable-project-import-preview']")?.dataset.state === "ready");
  await page.click("[data-testid='portable-project-open']");
  await page.waitForSelector("[data-testid='approved-workbench-root'][data-project-id^='portable_']");
}

async function assertMainEditorViewport(baseUrl, browser, viewport, evidenceDir) {
  const context = await browser.newContext({ viewport, locale: "ko-KR" });
  const page = await context.newPage();
  const source = `설정 {
  제목: G11_네_뷰포트.
}.

1 보여주기.
`;
  await page.goto(`${baseUrl}/solutions/seamgrim_ui_mvp/ui/index.html?tab=studio&ddn=${encodeURIComponent(base64Utf8(source))}`, {
    waitUntil: "domcontentloaded",
  });
  await page.waitForSelector("#screen-run:not(.hidden)", { state: "visible", timeout: 30_000 });
  await page.locator("#screen-run [data-shell-space='create']").click();
  await page.waitForSelector("#screen-editor:not(.hidden)", { state: "visible", timeout: 30_000 });
  await page.locator("[data-testid='project-enable']").click();
  await page.waitForSelector("[data-project-file-path='app/main.ddn']", { state: "visible", timeout: 10_000 });
  await page.locator("[data-project-file-path='app/main.ddn']").click();
  await page.locator("#ddn-textarea").focus();
  await page.keyboard.press("End");
  await page.locator("[data-testid='project-run']").click();
  await page.waitForFunction(() => {
    const result = document.querySelector("[data-testid='project-run-result']")?.textContent ?? "";
    return result.includes("ddn.local_project_run_summary.v1");
  }, null, { timeout: 30_000 });
  await page.locator("#ddn-textarea").focus();
  const state = await page.evaluate(() => {
    const panel = document.querySelector("[data-testid='project-workbench']");
    const nav = document.querySelector("[data-testid='project-file-navigator']");
    const textarea = document.querySelector("#ddn-textarea");
    const dependency = document.querySelector("[data-testid='project-dependency-status']");
    const runButton = document.querySelector("[data-testid='project-run']");
    const overflowX = document.documentElement.scrollWidth - document.documentElement.clientWidth;
    const rect = (node) => {
      if (!node) return null;
      const box = node.getBoundingClientRect();
      return { left: box.left, right: box.right, top: box.top, bottom: box.bottom, width: box.width, height: box.height };
    };
    return {
      projectMode: panel?.dataset.projectMode ?? "",
      nav: rect(nav),
      textarea: rect(textarea),
      dependencyText: dependency?.textContent ?? "",
      dependencyLabel: dependency?.getAttribute("aria-label") || dependency?.textContent || "",
      activeTag: document.activeElement?.id ?? document.activeElement?.getAttribute("data-testid") ?? "",
      runTitle: runButton?.getAttribute("title") || runButton?.textContent || "",
      overflowX,
    };
  });
  assert(state.projectMode === "1", `${viewport.width}x${viewport.height}: project mode inactive`);
  assert(state.nav?.height > 40, `${viewport.width}x${viewport.height}: file navigator unusable`);
  assert(state.textarea?.height > 120, `${viewport.width}x${viewport.height}: editor too short`);
  assert(state.dependencyText.includes("graph"), `${viewport.width}x${viewport.height}: dependency status missing graph`);
  assert(state.activeTag === "ddn-textarea", `${viewport.width}x${viewport.height}: keyboard focus did not reach editor`);
  assert(String(state.runTitle).trim(), `${viewport.width}x${viewport.height}: project run tooltip/name missing`);
  assert(state.overflowX <= 8, `${viewport.width}x${viewport.height}: main editor horizontal overflow ${state.overflowX}`);
  const shot = path.join(evidenceDir, `main-editor-${viewportLabel(viewport)}.png`);
  await page.screenshot({ path: shot, fullPage: true });
  await context.close();
  return {
    viewport: viewportLabel(viewport),
    state: "main_editor_after_run",
    screenshot: shot,
    project_mode: state.projectMode,
    navigator_box: state.nav,
    editor_box: state.textarea,
    overflow_x: state.overflowX,
    keyboard_focus: state.activeTag,
  };
}

async function assertWorkbenchViewport(
  baseUrl,
  browser,
  viewport,
  artifactFile,
  expectedArtifact,
  expectedSummary,
  variantSummary,
  evidenceDir,
) {
  const context = await browser.newContext({ viewport, locale: "ko-KR" });
  const page = await context.newPage();
  await page.goto(`${baseUrl}/solutions/seamgrim_ui_mvp/ui/workbench/index.html`, { waitUntil: "networkidle" });
  await page.waitForSelector("[data-testid='approved-workbench-root']");
  const publicSource = await page.locator("[data-testid='source-editor']").inputValue();
  assert(publicSource.includes("포물선") || publicSource.includes("초기속도"), `${viewport.width}x${viewport.height}: one-file public physics source missing`);
  assert(await canvasNonBlank(page, "[data-testid='bogae-canvas']"), `${viewport.width}x${viewport.height}: one-file physics canvas blank`);
  const initialCanvas = await canvasFingerprint(page, "[data-testid='bogae-canvas']");

  await page.setInputFiles("[data-testid='portable-project-import-input']", artifactFile);
  await page.waitForFunction(() => document.querySelector("[data-testid='portable-project-import-preview']")?.dataset.state === "ready");
  const preview = await page.evaluate(() => {
    const previewNode = document.querySelector("[data-testid='portable-project-import-preview']");
    const box = previewNode?.getBoundingClientRect();
    return {
      details: document.querySelector("[data-testid='portable-project-import-details']")?.textContent ?? "",
      box: box ? { left: box.left, right: box.right, top: box.top, bottom: box.bottom, width: box.width, height: box.height } : null,
      overflowX: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    };
  });
  assert(preview.details.includes("entry app/main.ddn"), `${viewport.width}x${viewport.height}: import preview entry missing`);
  assert(preview.box?.right <= viewport.width + 4, `${viewport.width}x${viewport.height}: import preview overflows right`);
  assert(preview.overflowX <= 8, `${viewport.width}x${viewport.height}: preview horizontal overflow ${preview.overflowX}`);
  const previewShot = path.join(evidenceDir, `workbench-import-preview-${viewportLabel(viewport)}.png`);
  await page.screenshot({ path: previewShot, fullPage: true });
  await page.click("[data-testid='portable-project-open']");
  await page.waitForSelector("[data-testid='approved-workbench-root'][data-project-id^='portable_']");
  await page.locator(`[data-file-path="${LONG_FILE_PATH}"]`).first().click();
  await page.locator("[data-testid='source-editor']").focus();
  await page.keyboard.press("End");
  const opened = await page.evaluate((longPath) => {
    const sourceEditor = document.querySelector("[data-testid='source-editor']");
    const fileRow = document.querySelector(`[data-file-path="${CSS.escape(longPath)}"]`);
    const canvas = document.querySelector("[data-testid='bogae-canvas']");
    const importButton = document.querySelector("[data-testid='portable-project-import']");
    const exportButton = document.querySelector("[data-testid='portable-project-export']");
    const overflowX = document.documentElement.scrollWidth - document.documentElement.clientWidth;
    const rowBox = fileRow?.getBoundingClientRect();
    const canvasBox = canvas?.getBoundingClientRect();
    return {
      sourceTitle: document.querySelector("#source-panel-title")?.textContent ?? "",
      sourceReadOnly: sourceEditor?.readOnly ?? true,
      activeTag: document.activeElement?.getAttribute("data-testid") ?? document.activeElement?.id ?? "",
      projectRunBound: document.querySelector("[data-testid='approved-workbench-root']")?.dataset?.projectRunBound ?? "",
      projectRunTraceSha256: document.querySelector("[data-testid='approved-workbench-root']")?.dataset?.projectRunTraceSha256 ?? "",
      projectRunBoundedStateSha256: document.querySelector("[data-testid='approved-workbench-root']")?.dataset?.projectRunBoundedStateSha256 ?? "",
      projectRunLineageHash: document.querySelector("[data-testid='approved-workbench-root']")?.dataset?.projectRunLineageHash ?? "",
      projectRunRequestHash: document.querySelector("[data-testid='approved-workbench-root']")?.dataset?.projectRunRequestHash ?? "",
      projectRunCreatedRevision: document.querySelector("[data-testid='approved-workbench-root']")?.dataset?.projectRunCreatedRevision ?? "",
      runStatus: document.querySelector("[data-testid='run-status']")?.textContent ?? "",
      runHash: document.querySelector("[data-testid='run-hash']")?.textContent ?? "",
      runLineage: document.querySelector("[data-testid='run-lineage']")?.textContent ?? "",
      semanticTrace: document.querySelector("[data-testid='semantic-observations']")?.dataset?.traceSha256 ?? "",
      semanticBound: document.querySelector("[data-testid='semantic-observations']")?.dataset?.projectRunBound ?? "",
      semanticRows: [...document.querySelectorAll("[data-testid='semantic-observations'] [data-project-observation-id]")].map((node) => ({
        id: node.getAttribute("data-project-observation-id"),
        name: node.getAttribute("data-project-observation-name"),
        value: node.getAttribute("data-project-observation-value"),
        stateHashParticipation: node.getAttribute("data-state-hash-participation"),
      })),
      rowRight: rowBox?.right ?? 0,
      canvasHeight: canvasBox?.height ?? 0,
      importName: importButton?.getAttribute("aria-label") || importButton?.getAttribute("title") || "",
      exportName: exportButton?.getAttribute("aria-label") || exportButton?.getAttribute("title") || "",
      overflowX,
    };
  }, LONG_FILE_PATH);
  assert(opened.sourceTitle.includes("아주긴한국어파일이름"), `${viewport.width}x${viewport.height}: long Korean filename not active`);
  assert(!opened.sourceReadOnly, `${viewport.width}x${viewport.height}: source editor read-only`);
  assert(opened.activeTag === "source-editor", `${viewport.width}x${viewport.height}: keyboard focus did not reach workbench editor`);
  assert(opened.rowRight <= viewport.width + 4, `${viewport.width}x${viewport.height}: long filename row overflows`);
  assert(opened.canvasHeight >= 160, `${viewport.width}x${viewport.height}: primary Bogae too short`);
  assert(opened.importName && opened.exportName, `${viewport.width}x${viewport.height}: tooltip/accessibility name missing`);
  assert(opened.overflowX <= 8, `${viewport.width}x${viewport.height}: workbench horizontal overflow ${opened.overflowX}`);
  const importedState = await workbenchProjectRunState(page);
  assert(importedState.executionState === "imported_record", `${viewport.width}x${viewport.height}: imported record state missing before run`);
  assert(importedState.projectRunBound === "false", `${viewport.width}x${viewport.height}: imported record incorrectly bound as current run`);
  assert(importedState.importedRecordSourceHash, `${viewport.width}x${viewport.height}: imported record source hash missing`);

  await page.click("[data-testid='lifecycle-run']");
  await page.waitForFunction((expectedRows) => {
    const root = document.querySelector("[data-testid='approved-workbench-root']");
    return root?.dataset?.projectExecutionState === "current_success"
      && root?.dataset?.projectRunBound === "true"
      && root?.dataset?.projectRunOutputRows === expectedRows;
  }, expectedSummary.output_rows.map(String).join("|"), { timeout: 30_000 });
  const firstRun = await workbenchProjectRunState(page);
  assert(firstRun.projectRunBound === "true", `${viewport.width}x${viewport.height}: current project run evidence not bound`);
  assert(firstRun.runtimeStateHash.startsWith("blake3:"), `${viewport.width}x${viewport.height}: VM state hash missing`);
  assert(firstRun.bounded && firstRun.bounded !== expectedSummary.bounded_state_sha256, `${viewport.width}x${viewport.height}: bounded state should be Workbench VM evidence, not imported summary`);
  assert(JSON.stringify(firstRun.outputRows) === JSON.stringify(expectedSummary.output_rows.map(String)), `${viewport.width}x${viewport.height}: output rows mismatch`);
  assert(firstRun.semanticBound === "true", `${viewport.width}x${viewport.height}: semantic observations not bound after run`);
  assert(JSON.stringify(firstRun.semanticRows.map((row) => row.value)) === JSON.stringify(expectedSummary.output_rows.map(String)), `${viewport.width}x${viewport.height}: semantic values mismatch ${JSON.stringify(firstRun.semanticRows)}`);
  assert(firstRun.semanticRows.every((row) => row.stateHashParticipation === "1"), `${viewport.width}x${viewport.height}: semantic observation state hash participation mismatch ${JSON.stringify(firstRun.semanticRows)}`);
  assert(firstRun.runStatus.includes("current project VM run"), `${viewport.width}x${viewport.height}: run status not current VM run: ${firstRun.runStatus}`);
  assert(firstRun.runLineage.includes("wasm_project_prepare_link_json"), `${viewport.width}x${viewport.height}: run lineage missing prepare/link frontdoor`);
  assert(firstRun.trace && firstRun.semanticTrace === firstRun.trace, `${viewport.width}x${viewport.height}: trace DOM mismatch after current run`);
  assert(await canvasNonBlank(page, "[data-testid='bogae-canvas']"), `${viewport.width}x${viewport.height}: current project canvas blank`);
  const firstCanvas = await canvasFingerprint(page, "[data-testid='bogae-canvas']");
  assert(firstCanvas.projectRunBound === "true", `${viewport.width}x${viewport.height}: canvas not bound to project run`);
  assert(firstCanvas.traceSha256 === firstRun.trace, `${viewport.width}x${viewport.height}: canvas trace hash mismatch`);
  assert(firstCanvas.lineageHash === firstRun.lineage, `${viewport.width}x${viewport.height}: canvas lineage hash mismatch`);
  assert(firstCanvas.datasetSignature === firstCanvas.viewArtifactHash, `${viewport.width}x${viewport.height}: canvas/view hash mismatch`);
  assert(firstCanvas.datasetSignature !== initialCanvas.datasetSignature, `${viewport.width}x${viewport.height}: imported canvas signature did not differ from static preview`);
  assert(firstCanvas.hash !== initialCanvas.hash, `${viewport.width}x${viewport.height}: imported canvas pixels did not differ from static preview`);
  const verifiedLockText = await readWorkbenchFile(page, "ddn.lock");
  assert(verifiedLockText.includes(String(expectedSummary.lock_sha256 ?? "")), `${viewport.width}x${viewport.height}: verified lock hash missing before local edit`);
  const openedShot = path.join(evidenceDir, `workbench-current-run-${viewportLabel(viewport)}.png`);
  await page.screenshot({ path: openedShot, fullPage: true });

  await page.locator(`[data-file-path="lib/운동.ddn"]`).first().click();
  const moduleText = await page.locator("[data-testid='source-editor']").inputValue();
  assert(moduleText.includes("속도구하기 <- 7."), `${viewport.width}x${viewport.height}: module edit source missing 7`);
  await page.locator("[data-testid='source-editor']").fill(moduleText.replace("속도구하기 <- 7.", "속도구하기 <- 8."));
  const staleState = await workbenchProjectRunState(page);
  assert(staleState.executionState === "previous_success", `${viewport.width}x${viewport.height}: edit did not downgrade current run to previous_success`);
  assert(staleState.projectRunBound === "false", `${viewport.width}x${viewport.height}: stale run remained bound after edit`);
  await page.click("[data-testid='lifecycle-run']");
  await page.waitForFunction((expectedRows) => {
    const root = document.querySelector("[data-testid='approved-workbench-root']");
    return root?.dataset?.projectExecutionState === "current_success"
      && root?.dataset?.projectRunBound === "true"
      && root?.dataset?.projectRunOutputRows === expectedRows;
  }, variantSummary.output_rows.map(String).join("|"), { timeout: 30_000 });
  const variantCanvas = await canvasFingerprint(page, "[data-testid='bogae-canvas']");
  const variantState = await workbenchProjectRunState(page);
  assert(variantState.runtimeStateHash.startsWith("blake3:"), `${viewport.width}x${viewport.height}: variant VM state hash missing`);
  assert(JSON.stringify(variantState.outputRows) === JSON.stringify(variantSummary.output_rows.map(String)), `${viewport.width}x${viewport.height}: variant output rows mismatch`);
  assert(JSON.stringify(variantState.semanticRows.map((row) => row.value)) === JSON.stringify(variantSummary.output_rows.map(String)), `${viewport.width}x${viewport.height}: variant observation values mismatch`);
  assert(variantState.trace !== firstRun.trace, `${viewport.width}x${viewport.height}: module value change did not change trace`);
  assert(variantState.bounded !== firstRun.bounded, `${viewport.width}x${viewport.height}: module value change did not change bounded state`);
  assert(variantState.runtimeStateHash !== firstRun.runtimeStateHash, `${viewport.width}x${viewport.height}: module value change did not change runtime state hash`);
  assert(variantState.lineage !== firstRun.lineage, `${viewport.width}x${viewport.height}: module value change did not change lineage hash`);
  assert(variantCanvas.datasetSignature !== firstCanvas.datasetSignature, `${viewport.width}x${viewport.height}: module value change did not change canvas signature`);
  assert(variantCanvas.viewArtifactHash !== firstCanvas.viewArtifactHash, `${viewport.width}x${viewport.height}: module value change did not change view artifact hash`);
  assert(await canvasNonBlank(page, "[data-testid='bogae-canvas']"), `${viewport.width}x${viewport.height}: variant project canvas blank`);
  const refreshedLockText = await readWorkbenchFile(page, "ddn.lock");
  assert(refreshedLockText !== verifiedLockText, `${viewport.width}x${viewport.height}: verified local non-lock edit did not refresh lock`);
  assert(refreshedLockText.includes(String(variantSummary.lock_sha256 ?? "")), `${viewport.width}x${viewport.height}: refreshed lock hash missing after local edit`);
  const variantShot = path.join(evidenceDir, `workbench-variant-${viewportLabel(viewport)}.png`);
  await page.screenshot({ path: variantShot, fullPage: true });

  await page.locator(`[data-file-path="app/main.ddn"]`).first().click();
  const mainText = await page.locator("[data-testid='source-editor']").inputValue();
  assert(mainText.includes("\"./lib/운동\""), `${viewport.width}x${viewport.height}: main import source missing`);
  await page.locator("[data-testid='source-editor']").fill(mainText.replace("\"./lib/운동\"", "\"./lib/없음\""));
  await page.click("[data-testid='lifecycle-run']");
  await page.waitForFunction(() => {
    const root = document.querySelector("[data-testid='approved-workbench-root']");
    return root?.dataset?.projectExecutionState === "current_failure"
      && root?.dataset?.projectRunBound === "false";
  }, null, { timeout: 30_000 });
  const failedState = await workbenchProjectRunState(page);
  const failedCanvas = await canvasFingerprint(page, "[data-testid='bogae-canvas']");
  assert(failedState.previousLineage === variantState.lineage, `${viewport.width}x${viewport.height}: previous success lineage not preserved after failure`);
  assert(failedState.failureSourceHash, `${viewport.width}x${viewport.height}: failure source hash missing`);
  assert(failedState.runStatus.includes("project run failed"), `${viewport.width}x${viewport.height}: failure status missing`);
  assert(failedCanvas.projectRunBound === "false", `${viewport.width}x${viewport.height}: failed run left previous Bogae as current`);
  const failedShot = path.join(evidenceDir, `workbench-failed-${viewportLabel(viewport)}.png`);
  await page.screenshot({ path: failedShot, fullPage: true });
  await context.close();
  return {
    viewport: viewportLabel(viewport),
    state: "workbench_current_tree_edit_rerun_failure",
    screenshots: [previewShot, openedShot, variantShot, failedShot],
    preview_box: preview.box,
    preview_overflow_x: preview.overflowX,
    opened: {
      canvas_height: opened.canvasHeight,
      overflow_x: opened.overflowX,
      project_run_trace_sha256: firstRun.trace,
      project_run_bounded_state_sha256: firstRun.bounded,
      project_run_lineage_hash: firstRun.lineage,
      runtime_state_hash: firstRun.runtimeStateHash,
      source_readonly: opened.sourceReadOnly,
      keyboard_focus: opened.activeTag,
      semantic_rows: firstRun.semanticRows,
      canvas_signature: firstCanvas.datasetSignature,
      canvas_pixel_hash: firstCanvas.hash,
    },
    variant: {
      trace_sha256: variantState.trace,
      bounded_state_sha256: variantState.bounded,
      lineage_hash: variantState.lineage,
      runtime_state_hash: variantState.runtimeStateHash,
      canvas_signature: variantCanvas.datasetSignature,
      view_artifact_hash: variantCanvas.viewArtifactHash,
      canvas_pixel_hash: variantCanvas.hash,
    },
    failure: {
      execution_state: failedState.executionState,
      previous_lineage_hash: failedState.previousLineage,
      failure_source_hash: failedState.failureSourceHash,
      canvas_project_run_bound: failedCanvas.projectRunBound,
    },
  };
}

async function assertWorkbenchDynamicLifecycle(baseUrl, browser, artifactFile, evidenceDir) {
  const viewport = { width: 1280, height: 720 };
  const context = await browser.newContext({ viewport, locale: "ko-KR" });
  const page = await context.newPage();
  await page.goto(`${baseUrl}/solutions/seamgrim_ui_mvp/ui/workbench/index.html`, { waitUntil: "networkidle" });
  await page.waitForSelector("[data-testid='approved-workbench-root']");
  await page.setInputFiles("[data-testid='portable-project-import-input']", artifactFile);
  await page.waitForFunction(() => document.querySelector("[data-testid='portable-project-import-preview']")?.dataset.state === "ready");
  await page.click("[data-testid='portable-project-open']");
  await page.waitForSelector("[data-testid='approved-workbench-root'][data-project-id^='portable_']");

  const samples = [];
  async function sample(label) {
    const runState = await workbenchProjectRunState(page);
    const canvas = await canvasFingerprint(page, "[data-testid='bogae-canvas']");
    const snapshot = await page.evaluate(() => window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.());
    return {
      label,
      runState,
      canvas,
      frameCount: Number(snapshot?.runs?.find((run) => run.run_id === snapshot.activeRunId)?.frame_count ?? 0),
      activeFrameId: Number(snapshot?.activeFrame?.frame_id ?? -1),
      activeMadi: Number(snapshot?.activeFrame?.madi ?? -1),
      latestStateHash: String(snapshot?.activeFrame?.state_hash ?? ""),
      runtimeStatus: String(snapshot?.runtimeStatus ?? ""),
    };
  }

  async function waitForRows(rows) {
    const expected = {
      last: String(rows.at(-1) ?? ""),
    };
    try {
      await page.waitForFunction((expectedRows) => {
        const root = document.querySelector("[data-testid='approved-workbench-root']");
        const rows = String(root?.dataset?.projectRunOutputRows ?? "").split("|").filter(Boolean);
        return root?.dataset?.projectExecutionState === "current_success"
          && root?.dataset?.projectRunBound === "true"
          && rows.length >= 1
          && rows.at(-1) === expectedRows.last;
      }, expected, { timeout: 30_000 });
    } catch (err) {
      const debug = await page.evaluate(() => {
        const root = document.querySelector("[data-testid='approved-workbench-root']");
        return {
          expectedRows: "",
          executionState: root?.dataset?.projectExecutionState ?? "",
          projectRunBound: root?.dataset?.projectRunBound ?? "",
          projectRunOutputRows: root?.dataset?.projectRunOutputRows ?? "",
          runtimeStatus: window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.().runtimeStatus ?? "",
          diagnostics: window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.().diagnostics ?? [],
          runStatus: document.querySelector("[data-testid='run-status']")?.textContent ?? "",
        };
      });
      throw new Error(`dynamic waitForRows(${JSON.stringify(expected)}) failed: ${JSON.stringify(debug)} ${err?.message ?? err}`);
    }
  }

  async function waitForAnyOutput(label) {
    try {
      await page.waitForFunction(() => {
        const root = document.querySelector("[data-testid='approved-workbench-root']");
        const rows = String(root?.dataset?.projectRunOutputRows ?? "").split("|").filter(Boolean);
        return root?.dataset?.projectExecutionState === "current_success"
          && root?.dataset?.projectRunBound === "true"
          && rows.length >= 1;
      }, null, { timeout: 30_000 });
    } catch (err) {
      const debug = await page.evaluate((labelText) => {
        const root = document.querySelector("[data-testid='approved-workbench-root']");
        return {
          label: labelText,
          executionState: root?.dataset?.projectExecutionState ?? "",
          projectRunBound: root?.dataset?.projectRunBound ?? "",
          projectRunOutputRows: root?.dataset?.projectRunOutputRows ?? "",
          runtimeStatus: window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.().runtimeStatus ?? "",
        };
      }, label);
      throw new Error(`dynamic ${label}: output rows missing ${JSON.stringify(debug)} ${err?.message ?? err}`);
    }
  }

  async function waitForOutputAdvance(previousLast, label) {
    try {
      await page.waitForFunction((previous) => {
        const root = document.querySelector("[data-testid='approved-workbench-root']");
        const rows = String(root?.dataset?.projectRunOutputRows ?? "").split("|").filter(Boolean);
        const last = Number(rows.at(-1));
        return root?.dataset?.projectExecutionState === "current_success"
          && root?.dataset?.projectRunBound === "true"
          && Number.isFinite(last)
          && last > Number(previous);
      }, previousLast, { timeout: 30_000 });
    } catch (err) {
      const debug = await page.evaluate((labelText) => {
        const root = document.querySelector("[data-testid='approved-workbench-root']");
        return {
          label: labelText,
          projectRunOutputRows: root?.dataset?.projectRunOutputRows ?? "",
          runtimeStatus: window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.().runtimeStatus ?? "",
        };
      }, label);
      throw new Error(`dynamic ${label}: output did not advance from ${previousLast}: ${JSON.stringify(debug)} ${err?.message ?? err}`);
    }
  }

  function lastOutputNumber(row) {
    const value = Number(row?.runState?.outputRows?.at(-1));
    assert(Number.isFinite(value), `dynamic ${row?.label ?? "sample"}: numeric output missing ${JSON.stringify(row?.runState?.outputRows ?? [])}`);
    return value;
  }

  async function ensureManualStepReady(label) {
    await page.waitForFunction(() =>
      document.querySelector("[data-testid='lifecycle-step']")?.disabled === false ||
      document.querySelector("[data-testid='lifecycle-pause']")?.disabled === false
    , null, { timeout: 15_000 });
    const canStep = await page.evaluate(() => document.querySelector("[data-testid='lifecycle-step']")?.disabled === false);
    if (canStep) return;
    const canPause = await page.evaluate(() => document.querySelector("[data-testid='lifecycle-pause']")?.disabled === false);
    if (canPause) {
      await page.click("[data-testid='lifecycle-pause']");
      await page.waitForFunction(() => document.querySelector("[data-testid='lifecycle-step']")?.disabled === false, null, { timeout: 15_000 });
      return;
    }
    const debug = await page.evaluate((labelText) => ({
      label: labelText,
      controls: window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.().controls ?? {},
      runtimeStatus: window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.().runtimeStatus ?? "",
      runs: window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.().runs ?? [],
    }), label);
    throw new Error(`dynamic ${label}: manual step unavailable ${JSON.stringify(debug)}`);
  }

  async function manualStepAndWait(previousLast, label) {
    await ensureManualStepReady(label);
    await page.click("[data-testid='lifecycle-step']");
    await waitForOutputAdvance(previousLast, label);
  }

  await page.click("[data-testid='lifecycle-run']");
  await ensureManualStepReady("initial-pause");
  await waitForAnyOutput("run");
  samples.push(await sample("run"));
  await manualStepAndWait(lastOutputNumber(samples.at(-1)), "step1");
  samples.push(await sample("step1"));
  await manualStepAndWait(lastOutputNumber(samples.at(-1)), "step2");
  samples.push(await sample("step2"));

  for (const [index, row] of samples.entries()) {
    assert(row.runState.runtimeStateHash.startsWith("blake3:"), `dynamic ${row.label}: state hash missing`);
    assert(row.runState.trace && row.runState.semanticTrace === row.runState.trace, `dynamic ${row.label}: trace binding mismatch`);
    assert(row.canvas.projectRunBound === "true", `dynamic ${row.label}: canvas not bound to current run`);
    assert(row.canvas.traceSha256 === row.runState.trace, `dynamic ${row.label}: canvas trace mismatch`);
    assert(row.canvas.datasetSignature === row.canvas.viewArtifactHash, `dynamic ${row.label}: view artifact mismatch`);
    assert(row.frameCount >= index + 1, `dynamic ${row.label}: frame count mismatch ${row.frameCount}`);
    assert(row.activeFrameId === row.frameCount - 1, `dynamic ${row.label}: frame id mismatch ${row.activeFrameId}/${row.frameCount}`);
    assert(Number.isFinite(lastOutputNumber(row)), `dynamic ${row.label}: output did not advance ${JSON.stringify(row.runState.outputRows)}`);
  }
  for (let index = 1; index < samples.length; index += 1) {
    assert(lastOutputNumber(samples[index]) > lastOutputNumber(samples[index - 1]), `dynamic ${samples[index].label}: output did not increase`);
    assert(samples[index].runState.runtimeStateHash !== samples[index - 1].runState.runtimeStateHash, `dynamic ${samples[index].label}: state hash reused`);
    assert(samples[index].runState.trace !== samples[index - 1].runState.trace, `dynamic ${samples[index].label}: trace reused`);
    assert(samples[index].canvas.datasetSignature !== samples[index - 1].canvas.datasetSignature, `dynamic ${samples[index].label}: canvas signature reused`);
    assert(samples[index].canvas.hash, `dynamic ${samples[index].label}: canvas pixels missing`);
  }

  const paused = await sample("pause");
  assert(paused.runtimeStatus === "paused", `dynamic pause: status mismatch ${paused.runtimeStatus}`);
  assert(paused.runState.runtimeStateHash === samples.at(-1).runState.runtimeStateHash, "dynamic pause changed runtime state hash");
  assert(paused.runState.trace === samples.at(-1).runState.trace, "dynamic pause changed trace");
  assert(paused.canvas.hash === samples.at(-1).canvas.hash, "dynamic pause changed canvas pixels");

  await page.click("[data-testid='lifecycle-resume']");
  await manualStepAndWait(lastOutputNumber(paused), "resume-step");
  const resumed = await sample("resume-step");
  assert(resumed.runtimeStatus === "paused", `dynamic resume-step: status mismatch ${resumed.runtimeStatus}`);
  assert(lastOutputNumber(resumed) > lastOutputNumber(paused), `dynamic resume-step: output mismatch ${JSON.stringify(resumed.runState.outputRows)}`);
  assert(resumed.runState.runtimeStateHash !== paused.runState.runtimeStateHash, "dynamic resume-step did not advance state hash");

  await page.click("[data-testid='lifecycle-stop']");
  await page.waitForFunction(() => window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.().runtimeStatus === "stopped", null, { timeout: 30_000 });
  const stopped = await sample("stop");
  assert(stopped.runtimeStatus === "stopped", `dynamic stop: status mismatch ${stopped.runtimeStatus}`);

  await page.locator(`[data-file-path="lib/counter.ddn"]`).first().click();
  const counterText = await page.locator("[data-testid='source-editor']").inputValue();
  assert(counterText.includes("count <- count + 1."), "dynamic source edit: counter increment missing");
  await page.locator("[data-testid='source-editor']").fill(counterText.replace("count <- count + 1.", "count <- count + 2."));
  await page.waitForFunction(() => {
    const root = document.querySelector("[data-testid='approved-workbench-root']");
    return root?.dataset?.projectExecutionState === "previous_success"
      && root?.dataset?.projectRunBound === "false"
      && document.querySelector("[data-testid='lifecycle-step']")?.disabled === true
      && document.querySelector("[data-testid='lifecycle-run']")?.disabled === false;
  }, null, { timeout: 30_000 });
  const stale = await sample("stale-source-unbound");
  assert(stale.runState.projectRunBound === "false", "dynamic stale edit: stale run still bound as current");
  assert(stale.runState.previousLineage === stopped.runState.lineage, "dynamic stale edit: previous success lineage mismatch");

  await page.click("[data-testid='lifecycle-run']");
  await waitForAnyOutput("rerun-edited-source");
  const rerun = await sample("rerun-edited-source");
  const rerunLast = lastOutputNumber(rerun);
  assert(rerunLast > 0 && rerunLast % 2 === 0, `dynamic edited rerun output mismatch ${JSON.stringify(rerun.runState.outputRows)}`);
  assert(rerun.runState.runtimeStateHash !== resumed.runState.runtimeStateHash, "dynamic edited rerun reused previous runtime state hash");

  const shot = path.join(evidenceDir, "workbench-dynamic-lifecycle-1280x720.png");
  await page.screenshot({ path: shot, fullPage: true });
  await context.close();
  return {
    viewport: "1280x720",
    state: "dynamic_lifecycle_step_pause_resume_stop_stale_rerun",
    screenshot: shot,
    samples,
    paused,
    resumed,
    stopped,
    stale,
    rerun,
  };
}

async function assertWorkbenchServerArchiveFailure(browser, artifactFile, evidenceDir) {
  let server = await startServer();
  let editLink = "";
  let failedRunId = "";
  let stoppedRunId = "";
  try {
    const context = await browser.newContext({ viewport: { width: 1280, height: 720 }, locale: "ko-KR" });
    const page = await context.newPage();
    await page.goto(`${server.baseUrl}/solutions/seamgrim_ui_mvp/ui/workbench/index.html`, { waitUntil: "networkidle" });
    await page.waitForSelector("[data-testid='approved-workbench-root']");
    await page.setInputFiles("[data-testid='portable-project-import-input']", artifactFile);
    await page.waitForFunction(() => document.querySelector("[data-testid='portable-project-import-preview']")?.dataset.state === "ready");
    await page.click("[data-testid='portable-project-open']");
    await page.waitForSelector("[data-testid='approved-workbench-root'][data-project-id^='portable_']");
    await page.click("[data-testid='project-save']");
    await page.waitForFunction(() => {
      const status = document.querySelector("[data-testid='project-save-status']")?.textContent ?? "";
      const edit = document.querySelector("[data-testid='project-edit-link']")?.href ?? "";
      return /서버 저장|server saved/u.test(status) && edit.includes("sg_cap=");
    }, null, { timeout: 30_000 });
    editLink = await page.locator("[data-testid='project-edit-link']").getAttribute("href");
    assert(String(editLink ?? "").includes("#sg_project="), "server archive failure: edit link missing project fragment");

    await page.click("[data-testid='lifecycle-run']");
    await page.waitForFunction(() => {
      const root = document.querySelector("[data-testid='approved-workbench-root']");
      return root?.dataset?.projectExecutionState === "current_success"
        && root?.dataset?.projectRunBound === "true";
    }, null, { timeout: 30_000 });
    await page.click("[data-testid='lifecycle-stop']");
    await page.waitForFunction(() => {
      const snapshot = window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.();
      const active = (snapshot?.runs ?? []).find((run) => run.run_id === snapshot.activeRunId);
      return snapshot?.runtimeStatus === "stopped"
        && active?.server_final_status === "stopped"
        && (snapshot?.runArchives ?? []).some((run) => run.server_run_id === active.server_run_id && run.final_status === "stopped");
    }, null, { timeout: 30_000 });
    const stopped = await page.evaluate(() => {
      const snapshot = window.__SEAMGRIM_APPROVED_WORKBENCH__.getSnapshot();
      const active = (snapshot.runs ?? []).find((run) => run.run_id === snapshot.activeRunId);
      return { snapshot, active };
    });
    stoppedRunId = String(stopped.active?.server_run_id ?? "");
    assert(stoppedRunId, "server archive failure: normal run did not create server run");
    assert(Number(stopped.active?.server_checkpoint_count ?? 0) >= 1, "server archive failure: normal run missing checkpoint");
    assert(
      (stopped.snapshot.runArchives ?? []).some((run) => run.server_run_id === stoppedRunId && run.final_status === "stopped"),
      `server archive failure: stopped run not finalized ${JSON.stringify({ active: stopped.active, archives: stopped.snapshot.runArchives })}`,
    );

    await page.locator(`[data-file-path="app/main.ddn"]`).first().click();
    await page.locator("[data-testid='source-editor']").fill("없는값 보여주기.\n");
    await page.click("[data-testid='lifecycle-run']");
    await page.waitForFunction(() => {
      const snapshot = window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.();
      const root = document.querySelector("[data-testid='approved-workbench-root']");
      const active = (snapshot?.runs ?? []).find((run) => run.run_id === snapshot.activeRunId);
      return root?.dataset?.projectExecutionState === "current_failure"
        && root?.dataset?.projectRunBound === "false"
        && active?.server_final_status === "failed";
    }, null, { timeout: 30_000 });
    const failed = await page.evaluate(() => {
      const snapshot = window.__SEAMGRIM_APPROVED_WORKBENCH__.getSnapshot();
      const active = (snapshot.runs ?? []).find((run) => run.run_id === snapshot.activeRunId);
      return {
        snapshot,
        active,
        runStatus: document.querySelector("[data-testid='run-status']")?.textContent ?? "",
        diagnostics: snapshot.diagnostics,
      };
    });
    failedRunId = String(failed.active?.server_run_id ?? "");
    assert(failedRunId, "server archive failure: failed run did not create server run");
    assert(failed.active?.server_final_status === "failed", `server archive failure: failed run status mismatch ${failed.active?.server_final_status}`);
    assert(Number(failed.active?.server_checkpoint_count ?? 0) === 0, "server archive failure: failed run received checkpoint");
    assert((failed.snapshot.runArchives ?? []).filter((run) => run.final_status === "running").length === 0, "server archive failure: running orphan remains");
    assert((failed.snapshot.runArchives ?? []).some((run) => run.server_run_id === failedRunId && run.final_status === "failed"), "server archive failure: failed archive missing");
    assert(failed.runStatus.includes("project run failed"), `server archive failure: UI failure status missing ${failed.runStatus}`);
    assert((failed.diagnostics ?? []).some((row) => String(row.code ?? "").startsWith("E_")), "server archive failure: diagnostic missing");
    const shot = path.join(evidenceDir, "workbench-server-archive-failed-1280x720.png");
    await page.screenshot({ path: shot, fullPage: true });
    await context.close();

    await stopServer(server.child);
    server = await startServer(server.dataDir);
    const reopenContext = await browser.newContext({ viewport: { width: 1280, height: 720 }, locale: "ko-KR" });
    const reopen = await reopenContext.newPage();
    await reopen.goto(rebaseProjectLink(editLink, server.baseUrl), { waitUntil: "networkidle" });
    await reopen.waitForSelector("[data-testid='approved-workbench-root']", { state: "visible", timeout: 30_000 });
    await reopen.waitForFunction(() => (window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.().runArchives ?? []).length >= 2, null, { timeout: 30_000 });
    const persisted = await reopen.evaluate((ids) => {
      const snapshot = window.__SEAMGRIM_APPROVED_WORKBENCH__.getSnapshot();
      return {
        stopped: (snapshot.runArchives ?? []).find((run) => run.server_run_id === ids.stoppedRunId) ?? null,
        failed: (snapshot.runArchives ?? []).find((run) => run.server_run_id === ids.failedRunId) ?? null,
        runningCount: (snapshot.runArchives ?? []).filter((run) => run.final_status === "running").length,
      };
    }, { stoppedRunId, failedRunId });
    assert(persisted.stopped?.final_status === "stopped", `server archive restart: stopped run lost ${JSON.stringify(persisted)}`);
    assert(persisted.failed?.final_status === "failed", `server archive restart: failed run lost ${JSON.stringify(persisted)}`);
    assert(persisted.runningCount === 0, `server archive restart: running orphan count ${persisted.runningCount}`);
    await reopenContext.close();
    return {
      state: "server_archive_failed_finalize_restart_persisted",
      data_dir: server.dataDir,
      stopped_run_id: stoppedRunId,
      failed_run_id: failedRunId,
      screenshot: path.join(evidenceDir, "workbench-server-archive-failed-1280x720.png"),
      persisted,
    };
  } finally {
    await stopServer(server?.child);
  }
}

async function assertWorkbenchLockTrustBoundary(baseUrl, browser, attackFiles, evidenceDir) {
  const context = await browser.newContext({ viewport: { width: 1280, height: 720 }, locale: "ko-KR" });
  const page = await context.newPage();
  await page.goto(`${baseUrl}/solutions/seamgrim_ui_mvp/ui/workbench/index.html`, { waitUntil: "networkidle" });
  await page.waitForSelector("[data-testid='approved-workbench-root']");

  async function assertLockAttack({
    label,
    file,
    expectedCode,
    expectLockFile = true,
  }) {
    await openPortableProjectFile(page, file);
    const beforeSource = await readWorkbenchFile(page, "app/main.ddn");
    const beforeLockExists = await hasWorkbenchFile(page, "ddn.lock");
    assert(beforeLockExists === expectLockFile, `${label}: lock presence mismatch before run`);
    const beforeLock = beforeLockExists ? await readWorkbenchFile(page, "ddn.lock") : "";
    const beforeSnapshot = await workbenchSnapshot(page);
    assert((beforeSnapshot.runs ?? []).length === 0, `${label}: run list not empty before attack`);
    await page.click("[data-testid='lifecycle-run']");
    await page.waitForFunction((code) => {
      const root = document.querySelector("[data-testid='approved-workbench-root']");
      const snapshot = window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.();
      return root?.dataset?.projectExecutionState === "current_failure"
        && root?.dataset?.projectRunBound === "false"
        && (snapshot?.diagnostics ?? []).some((row) => row?.code === code);
    }, expectedCode, { timeout: 30_000 });
    const state = await workbenchProjectRunState(page);
    const snapshot = await workbenchSnapshot(page);
    const codes = await workbenchDiagnosticCodes(page);
    assert(codes.includes(expectedCode), `${label}: expected diagnostic ${expectedCode}, got ${JSON.stringify(codes)}`);
    assert(state.executionState === "current_failure", `${label}: not current_failure`);
    assert(state.projectRunBound === "false", `${label}: failed attack bound current run`);
    assert(!state.trace, `${label}: failed attack left current trace`);
    assert((snapshot.runs ?? []).length === 0, `${label}: prepare/link lock failure created a local run`);
    assert((snapshot.runArchives ?? []).filter((run) => run.final_status === "running").length === 0, `${label}: running server archive orphan remains`);
    const afterSource = await readWorkbenchFile(page, "app/main.ddn");
    assert(afterSource === beforeSource, `${label}: source bytes changed after rejected run`);
    const afterLockExists = await hasWorkbenchFile(page, "ddn.lock");
    assert(afterLockExists === beforeLockExists, `${label}: lock presence changed after rejected run`);
    if (beforeLockExists) {
      const afterLock = await readWorkbenchFile(page, "ddn.lock");
      assert(afterLock === beforeLock, `${label}: lock bytes changed after rejected run`);
    }
    return {
      label,
      expected_code: expectedCode,
      diagnostics: codes,
      source_bytes_preserved: true,
      lock_bytes_preserved: true,
      current_run_bound: state.projectRunBound,
      local_run_count: (snapshot.runs ?? []).length,
      running_archive_count: (snapshot.runArchives ?? []).filter((run) => run.final_status === "running").length,
    };
  }

  const attacks = [];
  attacks.push(await assertLockAttack({
    label: "tampered_lock_sha",
    file: attackFiles.tamperedLockFile,
    expectedCode: "E_LOCK_HASH_MISMATCH",
  }));
  attacks.push(await assertLockAttack({
    label: "missing_lock",
    file: attackFiles.missingLockFile,
    expectedCode: "E_LOCK_MISSING",
    expectLockFile: false,
  }));
  attacks.push(await assertLockAttack({
    label: "project_graph_hash_tamper",
    file: attackFiles.projectGraphHashTamperFile,
    expectedCode: "E_LOCK_HASH_MISMATCH",
  }));
  attacks.push(await assertLockAttack({
    label: "package_pin_hash_tamper",
    file: attackFiles.packagePinHashTamperFile,
    expectedCode: "E_LOCK_HASH_MISMATCH",
  }));

  await openPortableProjectFile(page, attackFiles.validFile);
  await page.click("[data-testid='lifecycle-run']");
  await page.waitForFunction(() => {
    const root = document.querySelector("[data-testid='approved-workbench-root']");
    return root?.dataset?.projectExecutionState === "current_success"
      && root?.dataset?.projectRunBound === "true";
  }, null, { timeout: 30_000 });
  const successState = await workbenchProjectRunState(page);
  const sourceBeforeManualLockEdit = await readWorkbenchFile(page, "app/main.ddn");
  const lockBeforeManualEdit = await readWorkbenchFile(page, "ddn.lock");
  const lockAfterManualEdit = lockBeforeManualEdit.replace(
    /"lock_sha256":"[0-9a-f]+"/u,
    "\"lock_sha256\":\"ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff\"",
  );
  assert(lockAfterManualEdit !== lockBeforeManualEdit, "manual lock edit did not modify lock text");
  await page.locator("[data-testid='source-editor']").fill(lockAfterManualEdit);
  const staleState = await workbenchProjectRunState(page);
  assert(staleState.executionState === "previous_success", "manual lock edit did not move current run to previous_success");
  assert(staleState.previousLineage === successState.lineage, "manual lock edit did not preserve previous success lineage");
  await page.click("[data-testid='lifecycle-run']");
  await page.waitForFunction(() => {
    const root = document.querySelector("[data-testid='approved-workbench-root']");
    const snapshot = window.__SEAMGRIM_APPROVED_WORKBENCH__?.getSnapshot?.();
    return root?.dataset?.projectExecutionState === "current_failure"
      && root?.dataset?.projectRunBound === "false"
      && (snapshot?.diagnostics ?? []).some((row) => row?.code === "E_LOCK_HASH_MISMATCH");
  }, null, { timeout: 30_000 });
  const manualFailureState = await workbenchProjectRunState(page);
  const manualSnapshot = await workbenchSnapshot(page);
  const manualLockAfterFailure = await readWorkbenchFile(page, "ddn.lock");
  const sourceAfterManualFailure = await readWorkbenchFile(page, "app/main.ddn");
  assert(manualFailureState.previousLineage === successState.lineage, "manual lock edit failure did not preserve previous success");
  assert(manualFailureState.projectRunBound === "false", "manual lock edit failure bound current run");
  assert(manualLockAfterFailure === lockAfterManualEdit, "manual lock edit was overwritten after failure");
  assert(sourceAfterManualFailure === sourceBeforeManualLockEdit, "manual lock edit changed source bytes");
  assert((manualSnapshot.runArchives ?? []).filter((run) => run.final_status === "running").length === 0, "manual lock edit left running server archive orphan");
  const manualCodes = await workbenchDiagnosticCodes(page);
  attacks.push({
    label: "manual_lock_edit_not_overwritten",
    expected_code: "E_LOCK_HASH_MISMATCH",
    diagnostics: manualCodes,
    previous_lineage_preserved: manualFailureState.previousLineage === successState.lineage,
    lock_bytes_preserved: true,
    source_bytes_preserved: true,
    running_archive_count: (manualSnapshot.runArchives ?? []).filter((run) => run.final_status === "running").length,
  });

  const shot = path.join(evidenceDir, "workbench-lock-trust-boundary-1280x720.png");
  await page.screenshot({ path: shot, fullPage: true });
  await context.close();
  return {
    viewport: "1280x720",
    state: "lock_trust_boundary_attacks_rejected",
    attacks,
    screenshot: shot,
  };
}

async function main() {
  const wasmModule = await initWasm();
  const physicsSource = withRefreshedLock(wasmModule, withLongKoreanFile(await loadFixture("project_run_physics_v1.json")));
  const gridSource = await loadFixture("project_run_grid_v1.json");
  const physics = await buildArtifactFromVirtualSource(wasmModule, physicsSource, {
    projectName: "G11 다중 파일 물리 프로젝트",
    sourceLessonId: "rep_phys_projectile_xy_v1",
  });
  const physicsVariantSource = withRefreshedLock(
    wasmModule,
    replaceFileText(physicsSource, "lib/운동.ddn", "속도구하기 <- 7.", "속도구하기 <- 8."),
  );
  const physicsVariant = await buildArtifactFromVirtualSource(wasmModule, physicsVariantSource, {
    projectName: "G11 다중 파일 물리 프로젝트 값 변경",
    sourceLessonId: "rep_phys_projectile_xy_v1",
  });
  const gridSummary = JSON.parse(wasmModule.wasm_project_run_summary_json(JSON.stringify(gridSource), "앱", true, true));
  const dynamic = await buildArtifactFromVirtualSource(wasmModule, buildDynamicCounterSource(), {
    projectName: "G14 동적 다중 파일 lifecycle",
    sourceLessonId: "seamgrim_dynamic_multifile_lifecycle_v1",
  });
  const lockAttacks = await buildLockAttackArtifacts(physics.artifact);
  assert(JSON.stringify(physics.summary.output_rows) !== JSON.stringify(gridSummary.output_rows), "physics/grid representative outputs should differ");
  assert(physics.summary.bounded_state_sha256 !== gridSummary.bounded_state_sha256, "physics/grid bounded hashes should differ");
  assert(physics.summary.project_observation_trace.trace_sha256 !== physicsVariant.summary.project_observation_trace.trace_sha256, "module value variant trace should differ");
  assert(physics.summary.bounded_state_sha256 !== physicsVariant.summary.bounded_state_sha256, "module value variant bounded state should differ");
  const artifactFile = await writeTempArtifact("g11-physics", physics.artifact);
  const dynamicArtifactFile = await writeTempArtifact("g14-dynamic", dynamic.artifact);
  const lockAttackFiles = {
    validFile: artifactFile,
    tamperedLockFile: await writeTempArtifact("g11-tampered-lock", lockAttacks.tampered_lock),
    missingLockFile: await writeTempArtifact("g11-missing-lock", lockAttacks.missing_lock),
    projectGraphHashTamperFile: await writeTempArtifact("g11-lock-graph-tamper", lockAttacks.project_graph_hash_tamper),
    packagePinHashTamperFile: await writeTempArtifact("g11-lock-package-tamper", lockAttacks.package_pin_hash_tamper),
  };
  const evidenceDir = await resolveEvidenceDir();

  const { child, baseUrl, dataDir } = await startServer();
  const browser = await chromium.launch({ headless: true });
  const evidence = [];
  try {
    for (const viewport of VIEWPORTS) {
      const mainEvidence = await assertMainEditorViewport(baseUrl, browser, viewport, evidenceDir);
      const workbenchEvidence = await assertWorkbenchViewport(
        baseUrl,
        browser,
        viewport,
        artifactFile,
        physics.artifact,
        physics.summary,
        physicsVariant.summary,
        evidenceDir,
      );
      evidence.push({
        viewport: viewportLabel(viewport),
        main: mainEvidence,
        workbench: workbenchEvidence,
      });
    }
    evidence.push({
      viewport: "1280x720",
      dynamic_lifecycle: await assertWorkbenchDynamicLifecycle(baseUrl, browser, dynamicArtifactFile, evidenceDir),
    });
    evidence.push({
      viewport: "1280x720",
      server_archive_failure: await assertWorkbenchServerArchiveFailure(browser, dynamicArtifactFile, evidenceDir),
    });
    evidence.push({
      viewport: "1280x720",
      lock_trust_boundary: await assertWorkbenchLockTrustBoundary(baseUrl, browser, lockAttackFiles, evidenceDir),
    });
  } finally {
    await browser.close();
    await stopServer(child);
  }
  const evidenceReport = {
    schema: "seamgrim.multifile_project_workbench.viewport_evidence.v1",
    runner: "tests/seamgrim_multifile_project_workbench_runner.mjs",
    viewports: evidence,
    physics_output: physics.summary.output_rows,
    dynamic_initial_output: dynamic.summary.output_rows,
    grid_output: gridSummary.output_rows,
    physics_graph: physics.summary.project_graph_sha256,
    grid_graph: gridSummary.project_graph_sha256,
    lock_attack_artifacts: {
      tampered_lock: lockAttacks.tampered_lock.content_sha256,
      missing_lock: lockAttacks.missing_lock.content_sha256,
      project_graph_hash_tamper: lockAttacks.project_graph_hash_tamper.content_sha256,
      package_pin_hash_tamper: lockAttacks.package_pin_hash_tamper.content_sha256,
    },
    data_dir: dataDir,
    evidence_dir: evidenceDir,
  };
  await fs.writeFile(path.join(evidenceDir, "evidence.detjson"), JSON.stringify(evidenceReport, null, 2), "utf8");
  process.stdout.write(JSON.stringify({
    schema: "seamgrim.multifile_project_workbench.runner_result.v1",
    viewports: evidence.map((row) => row.viewport),
    physics_output: physics.summary.output_rows,
    grid_output: gridSummary.output_rows,
    physics_graph: physics.summary.project_graph_sha256,
    grid_graph: gridSummary.project_graph_sha256,
    lock_attack_artifacts: Object.keys(lockAttackFiles),
    data_dir: dataDir,
    evidence_dir: evidenceDir,
    evidence_report: path.join(evidenceDir, "evidence.detjson"),
  }) + "\n");
  process.stdout.write(`${OK}\n`);
}

await main();
