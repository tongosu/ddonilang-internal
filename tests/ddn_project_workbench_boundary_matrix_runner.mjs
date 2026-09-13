#!/usr/bin/env node

import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { spawn, spawnSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";
import { buildProjectSnapshotArtifactV0 } from "../solutions/seamgrim_ui_mvp/ui/project_snapshot.js";
import { parsePortableProjectArtifactBytes } from "../solutions/seamgrim_ui_mvp/ui/workbench/persistence/portable_project_artifact.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, "..");
const SERVER = path.resolve(ROOT, "solutions/seamgrim_ui_mvp/tools/ddn_exec_server.py");
const OK = "ddn_project_workbench_boundary_matrix: ok";

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function baseProject(files = []) {
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
  이름: "Boundary".
  뿌리: "./".
  첫글: "./app/main.ddn".
  목표 { 앱: "./app/main.ddn". }
  모듈길 { 로컬: "./lib". }
}.
`,
      },
      { path: "app/main.ddn", role: "ddn_source", utf8_text: "1 보여주기.\n" },
      ...files,
    ],
  };
}

function projectWithFile(file) {
  return baseProject([file]);
}

async function initWasm() {
  const uiDir = path.join(ROOT, "solutions", "seamgrim_ui_mvp", "ui");
  const freshWasmDir = String(process.env.DDN_WASM_DIR ?? "").trim();
  const wasmDir = freshWasmDir ? path.resolve(freshWasmDir) : path.join(uiDir, "wasm");
  const wasmModule = await import(pathToFileURL(path.join(wasmDir, "ddonirang_tool.js")).href);
  const wasmBytes = await fs.readFile(path.join(wasmDir, "ddonirang_tool_bg.wasm"));
  if (typeof wasmModule.default === "function") {
    await wasmModule.default({ module_or_path: wasmBytes });
  }
  for (const name of [
    "DdnWasmVm",
    "wasm_normalize_project_source_json",
    "wasm_project_prepare_link_json",
    "wasm_project_run_summary_json",
    "wasm_project_symbols_json",
  ]) {
    assert(typeof wasmModule[name] === "function", `${name} export missing`);
  }
  return wasmModule;
}

function capture(fn) {
  try {
    return { ok: true, text: String(fn()) };
  } catch (err) {
    return { ok: false, text: String(err?.message ?? err) };
  }
}

function expectWasmError(results, id, fn, expectedCodes) {
  const codes = Array.isArray(expectedCodes) ? expectedCodes : [expectedCodes];
  const result = capture(fn);
  assert(!result.ok, `${id}: expected failure but passed`);
  const matched = codes.find((code) => result.text.includes(code));
  assert(matched, `${id}: expected ${codes.join("|")} in ${result.text}`);
  assert(!result.text.includes(ROOT), `${id}: leaked absolute repo path`);
  results.push({ id, surface: "wasm_project_frontdoor", ok: true, code: matched });
}

function expectStringCommentAliasControl(results, fn) {
  const result = capture(fn);
  assert(result.ok, `comment_string_alias_negative_control: expected pass but failed ${result.text}`);
  const payload = JSON.parse(result.text);
  const rows = Array.isArray(payload.output_rows) ? payload.output_rows.map((row) => String(row)) : [];
  assert(rows.includes("도움.값"), `comment_string_alias_negative_control: literal alias string was not preserved ${JSON.stringify(rows)}`);
  assert(!rows.includes("3"), `comment_string_alias_negative_control: comment/string alias unexpectedly executed ${JSON.stringify(rows)}`);
  results.push({ id: "comment_string_alias_negative_control", surface: "wasm_project_frontdoor", ok: true, code: "STRING_COMMENT_ALIAS_NOT_EXECUTED" });
}

function runDirectWasmVm(wasm, source) {
  let vm = null;
  try {
    vm = new wasm.DdnWasmVm(String(source ?? ""));
    vm.update_logic(String(source ?? ""));
    const state = JSON.parse(String(vm.run_ticks(1) ?? "{}"));
    return { ok: true, state, state_hash: String(vm.get_state_hash?.() ?? "") };
  } catch (err) {
    return { ok: false, text: String(err?.message ?? err ?? "") };
  } finally {
    try {
      vm?.free?.();
    } catch (_) {
      // Best-effort cleanup for wasm-bindgen handles.
    }
  }
}

function expectResolverBypassControls(results, wasm, project, runSummary, prepareLink) {
  const entryFile = project.files.find((file) => file.path === "app/main.ddn");
  const directEntry = runDirectWasmVm(wasm, entryFile?.utf8_text ?? "");
  assert(!directEntry.ok, `direct_entry_file_vm_rejected_without_project_linker: expected direct VM failure but passed ${JSON.stringify(directEntry)}`);
  assert(
    directEntry.text.includes("파싱 실패") || directEntry.text.includes("정의되지 않은 변수") || directEntry.text.includes("운동"),
    `direct_entry_file_vm_rejected_without_project_linker: unexpected failure ${directEntry.text}`,
  );
  results.push({ id: "direct_entry_file_vm_rejected_without_project_linker", surface: "wasm_vm_single_file", ok: true, code: "E_DIRECT_ENTRY_REJECTED_WITHOUT_PROJECT_LINKER" });

  const direct = runDirectWasmVm(wasm, "운동.속도구하기 보여주기.\n");
  assert(!direct.ok, `direct_entry_vm_unresolved_module: expected direct alias VM failure but passed ${JSON.stringify(direct)}`);
  assert(direct.text.includes("정의되지 않은 변수") && direct.text.includes("운동"), `direct_entry_vm_unresolved_module: unexpected failure ${direct.text}`);
  results.push({ id: "direct_entry_vm_unresolved_module", surface: "wasm_vm_single_file", ok: true, code: "E_ALIAS_UNRESOLVED_WITHOUT_PROJECT_LINKER" });

  const prepared = prepareLink(project);
  assert(prepared.frontdoor === "wasm_project_prepare_link_json", `resolver_linked_project_vm_succeeds: frontdoor ${prepared.frontdoor}`);
  assert(String(prepared.linked_execution_source ?? "").includes("속도구하기 보여주기."), "resolver_linked_project_vm_succeeds: linked source missing executable symbol");
  assert(!String(prepared.linked_execution_source ?? "").includes("운동.속도구하기"), "resolver_linked_project_vm_succeeds: linked source still contains module alias access");
  const linkedRun = runDirectWasmVm(wasm, prepared.linked_execution_source);
  assert(linkedRun.ok, `resolver_linked_project_vm_succeeds: linked VM failed ${linkedRun.text}`);
  const summary = JSON.parse(runSummary(project));
  assert(linkedRun.state_hash === summary.runtime_state_hash, `resolver_linked_project_vm_succeeds: state hash mismatch ${linkedRun.state_hash} != ${summary.runtime_state_hash}`);
  results.push({ id: "resolver_linked_project_vm_succeeds", surface: "wasm_project_prepare_link_json_to_vm", ok: true, code: "PROJECT_LINKER_REQUIRED_FOR_MODULE_ALIAS" });
}

function expectAliasSpacingEquivalence(results, normalProject, spacingProject, runSummary, prepareLink) {
  const normal = JSON.parse(runSummary(normalProject));
  const spacing = JSON.parse(runSummary(spacingProject));
  assert(JSON.stringify(normal.output_rows) === JSON.stringify(spacing.output_rows), `alias_spacing_same_runtime_state_hash: output mismatch ${JSON.stringify(normal.output_rows)} != ${JSON.stringify(spacing.output_rows)}`);
  assert(normal.runtime_state_hash === spacing.runtime_state_hash, `alias_spacing_same_runtime_state_hash: state hash mismatch ${normal.runtime_state_hash} != ${spacing.runtime_state_hash}`);
  results.push({ id: "alias_spacing_same_runtime_state_hash", surface: "wasm_project_run_summary_json", ok: true, code: normal.runtime_state_hash });

  const normalPrepared = prepareLink(normalProject);
  const spacingPrepared = prepareLink(spacingProject);
  assert(normalPrepared.linked_execution_source_sha256 === spacingPrepared.linked_execution_source_sha256, `alias_spacing_prepare_link_equivalent: linked source mismatch ${normalPrepared.linked_execution_source_sha256} != ${spacingPrepared.linked_execution_source_sha256}`);
  assert(normalPrepared.symbol_boundary?.symbol_boundary_sha256 === spacingPrepared.symbol_boundary?.symbol_boundary_sha256, "alias_spacing_prepare_link_equivalent: symbol boundary mismatch");
  results.push({ id: "alias_spacing_prepare_link_equivalent", surface: "wasm_project_prepare_link_json", ok: true, code: normalPrepared.linked_execution_source_sha256 });
}

async function langToolInvocation(args) {
  const candidates = [
    path.join("I:", "home", "urihanl", "ddn", "codex", "target", "debug", process.platform === "win32" ? "ddonirang.exe" : "ddonirang"),
    path.join(ROOT, "target", "debug", process.platform === "win32" ? "ddonirang.exe" : "ddonirang"),
  ];
  for (const candidate of candidates) {
    try {
      await fs.access(candidate);
      return { command: candidate, args };
    } catch (_) {
      // Try the next known target directory.
    }
  }
  return {
    command: "cargo",
    args: ["run", "-q", "-p", "ddonirang-tool", "--bin", "ddonirang", "--", ...args],
  };
}

async function expectPortableError(results, id, artifactText, expectedCode) {
  try {
    await parsePortableProjectArtifactBytes(artifactText);
    throw new Error(`${id}: expected portable parse failure`);
  } catch (err) {
    assert(String(err?.code ?? err?.message ?? err).includes(expectedCode), `${id}: expected ${expectedCode}, got ${err?.code ?? err}`);
    assert(!String(err?.message ?? "").includes(ROOT), `${id}: portable error leaked absolute repo path`);
    results.push({ id, surface: "portable_project_artifact", ok: true, code: expectedCode });
  }
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

async function waitForHealth(baseUrl, child) {
  for (let index = 0; index < 100; index += 1) {
    if (child.exitCode !== null) throw new Error(`server exited: ${child.exitCode}`);
    try {
      const response = await fetch(`${baseUrl}/api/v1/projects/health`);
      if (response.ok) return;
    } catch (_) {
      await new Promise((resolve) => setTimeout(resolve, 100));
    }
  }
  throw new Error("server health timeout");
}

async function startServer() {
  const dataDir = await fs.mkdtemp(path.join(os.tmpdir(), "seamgrim-g13-boundary-"));
  const port = await freePort();
  const child = spawn(process.env.PYTHON || "python", [SERVER, "--host", "127.0.0.1", "--port", String(port)], {
    cwd: ROOT,
    env: { ...process.env, SEAMGRIM_PROJECT_DATA_DIR: dataDir },
    stdio: ["ignore", "pipe", "pipe"],
  });
  child.stdout.on("data", () => {});
  child.stderr.on("data", () => {});
  const baseUrl = `http://127.0.0.1:${port}`;
  await waitForHealth(baseUrl, child);
  return { child, baseUrl, dataDir };
}

async function stopServer(child) {
  if (!child || child.exitCode !== null) return;
  child.kill();
  await new Promise((resolve) => child.once("exit", resolve));
}

async function requestJson(url, { method = "GET", capability = "", body = null } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (capability) headers.Authorization = `Bearer ${capability}`;
  const response = await fetch(url, {
    method,
    headers,
    body: body === null ? undefined : JSON.stringify(body),
  });
  let payload = {};
  try {
    payload = await response.json();
  } catch (_) {
    payload = {};
  }
  return { status: response.status, ok: response.ok, payload };
}

async function buildArtifact(label = "boundary") {
  return buildProjectSnapshotArtifactV0({
    projectName: `G13 ${label}`,
    ddnText: "1 보여주기.\n",
    sourceLessonId: `g13_${label}`,
    localPackagePayload: {
      schema: "seamgrim.local_project_tree_payload.v0",
      kind: "seamgrim.local_project_tree.v0",
      root_path: "뿌리.ddn",
      entry_path: "app/main.ddn",
      files: baseProject().files.map((file) => ({
        path: file.path,
        role: file.role,
        utf8_text: file.utf8_text,
        byte_length: file.utf8_text.length,
        sha256: "0".repeat(64),
      })),
      frontdoor: "wasm_project_run_summary_json",
      state_hash_formula_change: false,
    },
  });
}

async function checkSymlinkEscape(results) {
  const rootDir = await fs.mkdtemp(path.join(os.tmpdir(), "ddn-g13-symlink-root-"));
  const outsideDir = await fs.mkdtemp(path.join(os.tmpdir(), "ddn-g13-symlink-outside-"));
  const appDir = path.join(rootDir, "app");
  const linkPath = path.join(rootDir, "escape-link");
  await fs.mkdir(appDir, { recursive: true });
  await fs.writeFile(path.join(rootDir, "뿌리.ddn"), `프로젝트 {
  이름: "SymlinkEscape".
  뿌리: "./".
  첫글: "./app/main.ddn".
  목표 { 앱: "./app/main.ddn". }
}.
`, "utf8");
  await fs.writeFile(path.join(appDir, "main.ddn"), "1 보여주기.\n", "utf8");
  await fs.writeFile(path.join(outsideDir, "outside.ddn"), "1 보여주기.\n", "utf8");
  try {
    await fs.symlink(outsideDir, linkPath, "junction");
  } catch (err) {
    throw new Error(`symlink_escape: could not create symlink/junction fixture: ${err?.message ?? err}`);
  }
  const invocation = await langToolInvocation([
    "project-run",
    linkPath,
    "--project",
    rootDir,
    "--target",
    "앱",
  ]);
  const proc = spawnSync(invocation.command, invocation.args, {
    cwd: ROOT,
    encoding: "utf8",
    timeout: 120_000,
  });
  const output = `${proc.stdout ?? ""}${proc.stderr ?? ""}`;
  const productError = output.split(/\r?\n/).find((line) => line.includes("E_PROJECT_SYMLINK_ESCAPE")) ?? output;
  assert(proc.status !== 0, `symlink_escape: expected CLI failure but passed\n${output}`);
  assert(output.includes("E_PROJECT_SYMLINK_ESCAPE"), `symlink_escape: expected E_PROJECT_SYMLINK_ESCAPE in ${output}`);
  assert(!productError.includes(ROOT), "symlink_escape: leaked absolute repo path");
  results.push({ id: "symlink_escape", surface: "lang_tool_project_run_disk", ok: true, code: "E_PROJECT_SYMLINK_ESCAPE" });
}

async function checkSingleFileCanvasNegativeControl(results) {
  const runnerText = await fs.readFile(path.join(ROOT, "tests", "seamgrim_multifile_project_workbench_runner.mjs"), "utf8");
  const checkerText = await fs.readFile(path.join(ROOT, "tests", "run_seamgrim_multifile_project_workbench_check.py"), "utf8");
  const required = [
    "one-file public physics source missing",
    "one-file physics canvas blank",
    "imported canvas signature did not differ from static preview",
    "imported canvas pixels did not differ from static preview",
    "module value change did not change canvas signature",
  ];
  const missing = required.filter((token) => !runnerText.includes(token) && !checkerText.includes(token));
  assert(missing.length === 0, `single_file_canvas_negative_control: missing tokens ${missing.join(", ")}`);
  results.push({ id: "single_file_canvas_negative_control", surface: "checker_static_contract", ok: true, code: "STATIC_CANVAS_MISUSE_REJECTED" });
}

async function checkProjectServerBoundaries(results) {
  const server = await startServer();
  try {
    const artifactA = await buildArtifact("server_a");
    const create = await requestJson(`${server.baseUrl}/api/v1/projects`, {
      method: "POST",
      body: { project_snapshot_artifact: artifactA, title: "G13 boundary" },
    });
    assert(create.ok, `server create failed: ${JSON.stringify(create.payload)}`);
    const { project_id: projectId, revision_id: revisionId, edit_capability: editCap, view_capability: viewCap } = create.payload;
    const artifactB = await buildArtifact("server_b");
    const viewWrite = await requestJson(`${server.baseUrl}/api/v1/projects/${projectId}/revisions`, {
      method: "POST",
      capability: viewCap,
      body: { project_snapshot_artifact: artifactB, expected_parent_revision_id: revisionId },
    });
    assert(!viewWrite.ok && viewWrite.payload?.code === "E_PROJECT_PERMISSION_DENIED", `view write mismatch: ${JSON.stringify(viewWrite)}`);
    results.push({ id: "view_capability_write_attempt", surface: "project_server", ok: true, code: viewWrite.payload.code });

    const append = await requestJson(`${server.baseUrl}/api/v1/projects/${projectId}/revisions`, {
      method: "POST",
      capability: editCap,
      body: { project_snapshot_artifact: artifactB, expected_parent_revision_id: revisionId },
    });
    assert(append.ok, `server append failed: ${JSON.stringify(append.payload)}`);
    const stale = await requestJson(`${server.baseUrl}/api/v1/projects/${projectId}/revisions`, {
      method: "POST",
      capability: editCap,
      body: { project_snapshot_artifact: await buildArtifact("server_c"), expected_parent_revision_id: revisionId },
    });
    assert(!stale.ok && stale.payload?.code === "E_PROJECT_REVISION_CONFLICT", `revision conflict mismatch: ${JSON.stringify(stale)}`);
    results.push({ id: "revision_conflict", surface: "project_server", ok: true, code: stale.payload.code });

    const parentRun = await requestJson(`${server.baseUrl}/api/v1/projects/${projectId}/runs`, {
      method: "POST",
      capability: editCap,
      body: { source_revision_id: revisionId, recipe_hash: "g13-parent", seed: "seed-a" },
    });
    assert(parentRun.ok, `parent run create failed: ${JSON.stringify(parentRun.payload)}`);
    const parentRunId = parentRun.payload?.run?.server_run_id;
    assert(parentRunId, "parent run id missing");
    const checkpoint = await requestJson(`${server.baseUrl}/api/v1/projects/${projectId}/runs/${parentRunId}/checkpoints`, {
      method: "POST",
      capability: editCap,
      body: {
        checkpoint: {
          sequence: 1,
          committed_madi: 1,
          previous_checkpoint_sha256: "",
          input_snapshots: [],
          state_hashes: ["blake3:g13-good-branch-state"],
          frame_summary: { local_run_id: "g13-parent", frame_count: 1, latest_frame_id: 1, renderer_pixels_stored: false },
        },
      },
    });
    assert(checkpoint.ok, `parent checkpoint failed: ${JSON.stringify(checkpoint.payload)}`);
    const finalized = await requestJson(`${server.baseUrl}/api/v1/projects/${projectId}/runs/${parentRunId}/finalize`, {
      method: "POST",
      capability: editCap,
      body: { final_status: "stopped" },
    });
    assert(finalized.ok, `parent finalize failed: ${JSON.stringify(finalized.payload)}`);
    const badBranch = await requestJson(`${server.baseUrl}/api/v1/projects/${projectId}/runs`, {
      method: "POST",
      capability: editCap,
      body: {
        source_revision_id: revisionId,
        recipe_hash: "g13-child",
        seed: "seed-b",
        parent_server_run_id: parentRunId,
        branch_madi: 1,
        branch_state_hash: "blake3:g13-wrong-branch-state",
      },
    });
    assert(!badBranch.ok && badBranch.payload?.code === "E_PROJECT_REVISION_CONFLICT", `branch state hash mismatch failed: ${JSON.stringify(badBranch)}`);
    results.push({ id: "branch_state_hash_mismatch", surface: "project_server", ok: true, code: badBranch.payload.code });
  } finally {
    await stopServer(server.child);
  }
}

async function main() {
  const wasm = await initWasm();
  const results = [];
  const normalize = (source) => wasm.wasm_normalize_project_source_json(JSON.stringify(source));
  const runSummary = (source, frozen = false) => wasm.wasm_project_run_summary_json(JSON.stringify(source), "앱", true, Boolean(frozen));
  const prepareLink = (source) => JSON.parse(wasm.wasm_project_prepare_link_json(JSON.stringify(source), "앱", true, false));

  await checkSymlinkEscape(results);

  expectWasmError(results, "path_escape", () => normalize(projectWithFile({ path: "../evil.ddn", role: "ddn_source", utf8_text: "1 보여주기.\n" })), "E_PROJECT_PATH_SEGMENT");
  expectWasmError(results, "absolute_path", () => normalize(projectWithFile({ path: "/tmp/evil.ddn", role: "ddn_source", utf8_text: "1 보여주기.\n" })), "E_PROJECT_PATH_ABSOLUTE");
  expectWasmError(results, "windows_drive_path", () => normalize(projectWithFile({ path: "C:/evil.ddn", role: "ddn_source", utf8_text: "1 보여주기.\n" })), "E_PROJECT_PATH_ABSOLUTE");
  expectWasmError(results, "unicode_normalization_collision", () => normalize(baseProject([
    { path: "lib/e\u0301.ddn", role: "ddn_source", utf8_text: "1 보여주기.\n" },
    { path: "lib/é.ddn", role: "ddn_source", utf8_text: "1 보여주기.\n" },
  ])), "E_PROJECT_PATH_DUPLICATE");
  expectWasmError(results, "case_fold_collision", () => normalize(baseProject([
    { path: "lib/Case.ddn", role: "ddn_source", utf8_text: "1 보여주기.\n" },
    { path: "lib/case.ddn", role: "ddn_source", utf8_text: "1 보여주기.\n" },
  ])), "E_PROJECT_PATH_CASE_COLLISION");

  const tooMany = baseProject(Array.from({ length: 63 }, (_, index) => ({
    path: `lib/m${index}.ddn`,
    role: "ddn_source",
    utf8_text: "1 보여주기.\n",
  })));
  expectWasmError(results, "file_count_limit", () => normalize(tooMany), "E_PROJECT_FILE_COUNT_LIMIT");
  expectWasmError(results, "file_size_limit", () => normalize(projectWithFile({
    path: "lib/huge.ddn",
    role: "ddn_source",
    utf8_text: `${"1".repeat(270_000)}\n`,
  })), "E_PROJECT_FILE_SIZE_LIMIT");
  expectWasmError(results, "payload_size_limit", () => normalize(baseProject(Array.from({ length: 40 }, (_, index) => ({
    path: `lib/payload_${index}.ddn`,
    role: "ddn_source",
    utf8_text: `${"1".repeat(60_000)}\n`,
  })))), "E_PROJECT_TOTAL_SIZE_LIMIT");

  const fixture = async (name) => JSON.parse(await fs.readFile(path.join(ROOT, "pack", "ddn_local_project_graph_v1", "fixtures", name), "utf8"));
  const moduleCycle = await fixture("project_module_cycle_v1.json");
  const privateSymbol = await fixture("project_symbol_private_v1.json");
  const duplicateExport = await fixture("project_module_duplicate_export_v1.json");
  const missingLock = await fixture("project_gaji_lock_missing_v1.json");
  const tamperedLock = await fixture("project_gaji_lock_tampered_v1.json");
  const unpinnedDependency = await fixture("project_gaji_lock_unpinned_v1.json");
  const aliasNormal = await fixture("project_run_alias_normal_v1.json");
  const aliasSpacing = await fixture("project_run_alias_spacing_v1.json");
  expectWasmError(results, "module_cycle", () => runSummary(moduleCycle), "E_IMPORT_CYCLE");
  expectWasmError(results, "private_symbol_access", () => wasm.wasm_project_symbols_json(JSON.stringify(privateSymbol)), "E_SYMBOL_NOT_EXPORTED");
  expectWasmError(results, "duplicate_export", () => runSummary(duplicateExport), "E_EXPORT_DUPLICATE");
  expectWasmError(results, "missing_lock", () => runSummary(missingLock, true), "E_LOCK_MISSING");
  expectWasmError(results, "tampered_lock", () => runSummary(tamperedLock), "E_LOCK_HASH_MISMATCH");
  expectWasmError(results, "unpinned_dependency", () => runSummary(unpinnedDependency), "E_GAJI_DEP_UNPINNED");
  expectResolverBypassControls(results, wasm, aliasNormal, runSummary, prepareLink);
  expectAliasSpacingEquivalence(results, aliasNormal, aliasSpacing, runSummary, prepareLink);
  expectWasmError(results, "running_file_change_fake_summary", () => runSummary({ ...baseProject(), files: baseProject().files.map((file) => file.path === "app/main.ddn" ? { ...file, utf8_text: "값 := 1.\n" } : file) }), ["E_PROJECT_RUNTIME", "E_PROJECT_ENTRY_PARSE"]);
  expectWasmError(results, "formatter_alias_spacing_control", () => runSummary({ ...baseProject(), files: baseProject().files.map((file) => file.path === "app/main.ddn" ? { ...file, utf8_text: "도움 . 값 보여주기.\n" } : file) }), ["E_PROJECT_RUNTIME", "E_ALIAS_UNKNOWN"]);
  const commentStringSource = baseProject([
    { path: "lib/helper.ddn", role: "ddn_source", utf8_text: "드러냄 { 값. }\n값 <- 3.\n" },
  ]);
  commentStringSource.files = commentStringSource.files.map((file) => file.path === "app/main.ddn" ? {
    ...file,
    utf8_text: '쓰임 { 도움: "./lib/helper". }\n"도움.값" 보여주기.\n// 도움.값 should not be rewritten as executable code\n',
  } : file);
  expectStringCommentAliasControl(results, () => runSummary(commentStringSource));

  await expectPortableError(results, "corrupt_portable_artifact", JSON.stringify({ schema: "seamgrim.project_snapshot_artifact.v0", content_sha256: "0".repeat(64) }), "E_PORTABLE_SNAPSHOT_SCHEMA");
  await expectPortableError(results, "old_wrapper_rejected", JSON.stringify({ schema: "seamgrim.project_snapshot_artifact.v-1" }), "E_PORTABLE_WRAPPER_SCHEMA");
  await expectPortableError(results, "portable_size_limit", "x".repeat(2_000_001), "E_PORTABLE_FILE_TOO_LARGE");

  await checkProjectServerBoundaries(results);
  await checkSingleFileCanvasNegativeControl(results);

  process.stdout.write(JSON.stringify({
    schema: "ddn.project_workbench_boundary_matrix.runner_result.v1",
    ok: true,
    case_count: results.length,
    results,
  }, null, 2));
  process.stdout.write(`\n${OK}\n`);
}

await main();
