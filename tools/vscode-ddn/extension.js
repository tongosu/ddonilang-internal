const fs = require("fs");
const os = require("os");
const path = require("path");
const { spawn } = require("child_process");

let activeClient = null;
let restartInFlight = null;
let commandsRegistered = false;
let outputChannel = null;
const activeExecutions = new Map();
let startupErrorShown = false;
let lifecycleState = "inactive";
let lastStartupFailure = null;

const SUPPORTED_EXTENSIONS = [".ddn", ".또니", ".ddl", ".옮김"];
const SELECT_EXECUTABLE_COMMAND = "ddonilang.selectLanguageServerExecutable";
const SELECT_EXECUTABLE_ACTION = "실행파일 선택";
const STATUS_COMMAND = "ddonilang.showLanguageServerStatus";
const RESTART_COMMAND = "ddonilang.restartLanguageServer";
const CONSOLE_BOGAE_COMMAND = "ddonilang.runCurrentDocumentConsoleBogae";
const CONSOLE_OUTPUT_CHANNEL = "Ddonilang Console 보개";
const CURRENTLINE_SOURCE_PROFILE = "v1-core-v25";

function isLocalAbsolutePath(candidate) {
  if (typeof candidate !== "string" || candidate.length === 0) {
    return false;
  }
  if (!path.isAbsolute(candidate)) {
    return false;
  }
  return process.platform !== "win32" || !candidate.startsWith("\\\\");
}

function runtimeExecutableNames() {
  return process.platform === "win32"
    ? ["ddonilang.exe", "또니랑.exe", "ddonirang.exe"]
    : ["ddonilang", "또니랑", "ddonirang"];
}

function isRegularExecutable(candidate, allowedNames = [executableName()]) {
  if (!isLocalAbsolutePath(candidate)) {
    return false;
  }
  try {
    const stat = fs.lstatSync(candidate);
    return (
      stat.isFile() &&
      !stat.isSymbolicLink() &&
      allowedNames.some(
        (name) => path.basename(candidate).toLowerCase() === name.toLowerCase(),
      )
    );
  } catch (_) {
    return false;
  }
}

function executableName() {
  return process.platform === "win32" ? "ddonirang-lsp.exe" : "ddonirang-lsp";
}

function boundedLocalCandidatesForNames(extensionPath, workspaceFolders, names) {
  const roots = [];
  for (const folder of workspaceFolders || []) {
    if (folder && typeof folder.fsPath === "string") {
      roots.push(folder.fsPath);
    }
  }
  roots.push(path.resolve(extensionPath, "..", ".."));

  const result = [];
  const seen = new Set();
  for (const root of roots) {
    for (const profile of ["debug", "release"]) {
      for (const name of names) {
        const candidate = path.resolve(root, "target", profile, name);
        const key = candidate.toLowerCase();
        if (!seen.has(key)) {
          seen.add(key);
          result.push(candidate);
        }
      }
    }
  }
  return result;
}

function boundedLocalCandidates(extensionPath, workspaceFolders) {
  return boundedLocalCandidatesForNames(extensionPath, workspaceFolders, [executableName()]);
}

function boundedRuntimeCandidates(extensionPath, workspaceFolders) {
  return boundedLocalCandidatesForNames(extensionPath, workspaceFolders, runtimeExecutableNames());
}

function resolveServerExecutable({
  configuredPath,
  autoDiscover,
  extensionPath,
  workspaceFolders,
}) {
  if (typeof configuredPath === "string" && configuredPath.trim() !== "") {
    const exactPath = path.normalize(configuredPath.trim());
    return isRegularExecutable(exactPath) ? exactPath : null;
  }
  if (autoDiscover !== true) {
    return null;
  }
  for (const candidate of boundedLocalCandidates(extensionPath, workspaceFolders)) {
    if (isRegularExecutable(candidate)) {
      return candidate;
    }
  }
  return null;
}

function resolveRuntimeExecutable({
  configuredPath,
  autoDiscover,
  extensionPath,
  workspaceFolders,
}) {
  const allowedNames = runtimeExecutableNames();
  if (typeof configuredPath === "string" && configuredPath.trim() !== "") {
    const exactPath = path.normalize(configuredPath.trim());
    return isRegularExecutable(exactPath, allowedNames) ? exactPath : null;
  }
  if (autoDiscover !== true) {
    return null;
  }
  for (const candidate of boundedRuntimeCandidates(extensionPath, workspaceFolders)) {
    if (isRegularExecutable(candidate, allowedNames)) {
      return candidate;
    }
  }
  return null;
}

function configuredExecutableFailureFor(candidate, allowedNames) {
  if (typeof candidate !== "string" || candidate.trim() === "") {
    return null;
  }
  const exactPath = path.normalize(candidate.trim());
  if (!path.isAbsolute(exactPath) || (process.platform === "win32" && exactPath.startsWith("\\\\"))) {
    return "CONFIGURED_PATH_NOT_ABSOLUTE";
  }
  let stat;
  try {
    stat = fs.lstatSync(exactPath);
  } catch (_) {
    return "CONFIGURED_PATH_MISSING";
  }
  if (stat.isSymbolicLink()) {
    return "CONFIGURED_PATH_SYMLINK";
  }
  if (!stat.isFile()) {
    return "CONFIGURED_PATH_DIRECTORY";
  }
  if (!allowedNames.some((name) => path.basename(exactPath).toLowerCase() === name.toLowerCase())) {
    return "CONFIGURED_PATH_UNSUPPORTED_FILENAME";
  }
  return null;
}

function configuredExecutableFailure(candidate) {
  return configuredExecutableFailureFor(candidate, [executableName()]);
}

function runtimeConfiguredExecutableFailure(candidate) {
  return configuredExecutableFailureFor(candidate, runtimeExecutableNames());
}

function documentSelector() {
  return [
    { scheme: "file", language: "ddonilang" },
    { scheme: "untitled", language: "ddonilang" },
  ];
}

function configuration(vscode) {
  return vscode.workspace.getConfiguration("ddonilang.lsp");
}

function runtimeConfiguration(vscode) {
  return vscode.workspace.getConfiguration("ddonilang.runtime");
}

function executableConfigurationTargets(vscode) {
  const configurationTarget = vscode.ConfigurationTarget || {};
  const targets = [];
  if (vscode.workspace && Array.isArray(vscode.workspace.workspaceFolders) && vscode.workspace.workspaceFolders.length > 0) {
    targets.push({
      label: "Workspace 설정에 저장 (추천)",
      description: "현재 workspace에서만 사용",
      target: configurationTarget.Workspace || 2,
    });
  }
  targets.push({
    label: "사용자 설정에 저장",
    description: "모든 workspace에서 사용",
    target: configurationTarget.Global || 1,
  });
  return targets;
}

function extensionForUri(uri) {
  if (typeof uri !== "string") {
    return null;
  }
  const pathPart = uri.split(/[?#]/, 1)[0];
  const basename = pathPart.split(/[\\/]/).pop() || "";
  const extension = path.extname(basename);
  return SUPPORTED_EXTENSIONS.includes(extension) ? extension : null;
}

function serverPid(client) {
  const processHandle = client && client._serverProcess;
  return processHandle && Number.isInteger(processHandle.pid) ? processHandle.pid : null;
}

function statusSnapshot(vscode, context) {
  const settings = configuration(vscode);
  const configuredPath = settings.get("executable", "");
  const activeDocument = vscode.window.activeTextEditor && vscode.window.activeTextEditor.document;
  const uri =
    activeDocument && activeDocument.uri
      ? typeof activeDocument.uri.path === "string"
        ? activeDocument.uri.path
        : activeDocument.uri.toString()
      : null;
  const supportedExtension = extensionForUri(uri);
  return {
    extensionVersion: require("./package.json").version,
    currentDocumentLanguageId: activeDocument ? activeDocument.languageId : null,
    supportedExtension,
    documentAdmission:
      activeDocument && activeDocument.languageId === "ddonilang" && supportedExtension
        ? "admitted"
        : activeDocument
          ? "not-admitted"
          : "no-document",
    configuredExecutablePath:
      typeof configuredPath === "string" && configuredPath.trim() !== ""
        ? path.normalize(configuredPath.trim())
        : "bounded-local-discovery",
    lifecycleState,
    serverPid: serverPid(activeClient),
    serverProcessPresent: serverPid(activeClient) !== null,
    lastStartupFailure,
  };
}

function formatStatus(status) {
  return [
    `Ddonilang LSP ${status.extensionVersion}`,
    `문서=${status.currentDocumentLanguageId || "없음"}`,
    `확장자=${status.supportedExtension || "미지원"}`,
    `admission=${status.documentAdmission}`,
    `실행 파일=${status.configuredExecutablePath}`,
    `상태=${status.lifecycleState}`,
    `server PID=${status.serverPid === null ? "없음" : status.serverPid}`,
    `최근 실패=${status.lastStartupFailure || "없음"}`,
  ].join(" | ");
}

function selectedFileSystemPath(uri) {
  if (!uri) {
    return null;
  }
  if (typeof uri.fsPath === "string") {
    return uri.fsPath;
  }
  if (typeof uri.path === "string") {
    return uri.path;
  }
  return null;
}

async function selectLanguageServerExecutable(context, vscode) {
  if (!vscode.window || typeof vscode.window.showOpenDialog !== "function") {
    lastStartupFailure = "FILE_PICKER_UNAVAILABLE";
    return null;
  }
  const picked = await vscode.window.showOpenDialog({
    canSelectFiles: true,
    canSelectFolders: false,
    canSelectMany: false,
    openLabel: "이 실행파일 사용",
    title: "또니랑 LSP 실행파일 선택",
  });
  const candidate = selectedFileSystemPath(Array.isArray(picked) ? picked[0] : null);
  if (!candidate) {
    return null;
  }
  const normalized = path.normalize(candidate);
  const failure = configuredExecutableFailure(normalized);
  if (failure) {
    lastStartupFailure = failure;
    if (typeof vscode.window.showErrorMessage === "function") {
      void vscode.window.showErrorMessage(`DDN_LSP_EXECUTABLE_INVALID ${failure}`);
    }
    return null;
  }
  if (typeof vscode.window.showQuickPick !== "function") {
    lastStartupFailure = "CONFIGURATION_SCOPE_PICKER_UNAVAILABLE";
    return null;
  }
  const scope = await vscode.window.showQuickPick(executableConfigurationTargets(vscode), {
    ignoreFocusOut: true,
    placeHolder: "실행파일 설정 범위를 선택하세요",
    title: "또니랑 LSP 실행파일 설정 범위",
  });
  if (!scope) {
    return null;
  }
  const settings = configuration(vscode);
  if (!settings || typeof settings.update !== "function") {
    lastStartupFailure = "CONFIGURATION_UPDATE_UNAVAILABLE";
    return null;
  }
  try {
    await settings.update("executable", normalized, scope.target);
  } catch (_) {
    lastStartupFailure = "CONFIGURATION_SAVE_FAILED";
    if (typeof vscode.window.showErrorMessage === "function") {
      void vscode.window.showErrorMessage("DDN_LSP_CONFIGURATION_SAVE_FAILED 실행파일 설정을 저장하지 못했습니다.");
    }
    return null;
  }
  return restartLanguageServer(context, vscode);
}

function showStartupFailure(context, vscode, code, detail) {
  if (startupErrorShown || !vscode.window || typeof vscode.window.showErrorMessage !== "function") {
    return;
  }
  startupErrorShown = true;
  const notification = vscode.window.showErrorMessage(
    `${code} ${detail}`,
    SELECT_EXECUTABLE_ACTION,
  );
  void Promise.resolve(notification)
    .then((action) => {
      if (action === SELECT_EXECUTABLE_ACTION) {
        return selectLanguageServerExecutable(context, vscode);
      }
      return null;
    })
    .catch(() => {
      // A dismissed or unavailable notification must not create an unhandled rejection.
    });
}

function documentUri(document) {
  return document && document.uri && typeof document.uri.toString === "function"
    ? document.uri.toString()
    : "";
}

function executionExtension(document) {
  const uri = document && document.uri;
  const uriText = uri && typeof uri.path === "string" ? uri.path : documentUri(document);
  return extensionForUri(uriText);
}

function isExecutableSurface(extension) {
  return extension === ".ddn" || extension === ".또니";
}

function showExecutionFailure(vscode, message) {
  if (vscode.window && typeof vscode.window.showWarningMessage === "function") {
    void vscode.window.showWarningMessage(message);
  } else if (vscode.window && typeof vscode.window.showErrorMessage === "function") {
    void vscode.window.showErrorMessage(message);
  }
}

function ensureOutputChannel(context, vscode) {
  if (!outputChannel) {
    outputChannel = vscode.window.createOutputChannel(CONSOLE_OUTPUT_CHANNEL);
    context.subscriptions.push(outputChannel);
  }
  return outputChannel;
}

function isCurrentDocumentSnapshot(vscode, document, version) {
  const uri = documentUri(document);
  const documents = Array.isArray(vscode.workspace.textDocuments)
    ? vscode.workspace.textDocuments
    : [document];
  return documents.some(
    (candidate) => documentUri(candidate) === uri && candidate.version === version,
  );
}

function startRuntimeProcess(executable, cellPath) {
  let child;
  let settled = false;
  let resolveResult;
  const done = new Promise((resolve) => {
    resolveResult = resolve;
  });
  let stdout = "";
  let stderr = "";
  const finish = (result) => {
    if (!settled) {
      settled = true;
      resolveResult(result);
    }
  };
  try {
    child = spawn(
      executable,
      [
        "currentline-run",
        "--cell",
        cellPath,
        "--source-profile",
        CURRENTLINE_SOURCE_PROFILE,
      ],
      { cwd: path.dirname(executable), shell: false, windowsHide: true },
    );
  } catch (error) {
    finish({ code: null, signal: null, stdout, stderr, error });
    return { child: null, done };
  }
  if (child.stdout && typeof child.stdout.setEncoding === "function") {
    child.stdout.setEncoding("utf8");
  }
  if (child.stderr && typeof child.stderr.setEncoding === "function") {
    child.stderr.setEncoding("utf8");
  }
  child.stdout?.on("data", (chunk) => {
    stdout += String(chunk);
  });
  child.stderr?.on("data", (chunk) => {
    stderr += String(chunk);
  });
  child.on("error", (error) => finish({ code: null, signal: null, stdout, stderr, error }));
  child.on("close", (code, signal) => finish({ code, signal, stdout, stderr }));
  return { child, done };
}

async function runCurrentDocumentConsoleBogae(context, vscode) {
  const editor = vscode.window && vscode.window.activeTextEditor;
  const document = editor && editor.document;
  const extension = executionExtension(document);
  if (!document || !extension) {
    showExecutionFailure(vscode, "LSP44_UNSUPPORTED_DOCUMENT 현재 문서는 또니랑 실행 대상이 아닙니다.");
    return null;
  }
  if (!isExecutableSurface(extension)) {
    showExecutionFailure(
      vscode,
      "LSP44_NON_EXECUTABLE_SURFACE .ddl/.옮김은 현재 Console 보개 실행 대상이 아닙니다.",
    );
    return null;
  }
  const key = documentUri(document);
  if (activeExecutions.has(key)) {
    showExecutionFailure(vscode, "LSP44_DUPLICATE_INVOCATION 같은 문서의 실행이 이미 진행 중입니다.");
    return null;
  }

  const settings = runtimeConfiguration(vscode);
  const configuredPath = settings.get("executable", "");
  const configuredFailure = runtimeConfiguredExecutableFailure(configuredPath);
  const executable = resolveRuntimeExecutable({
    configuredPath,
    autoDiscover: settings.get("autoDiscover", true),
    extensionPath: context.extensionPath,
    workspaceFolders: vscode.workspace.workspaceFolders,
  });
  if (!executable) {
    showExecutionFailure(
      vscode,
      `LSP44_RUNTIME_NOT_AVAILABLE ${configuredFailure || "RUNTIME_AUTODISCOVERY_NOT_FOUND"}`,
    );
    return null;
  }

  const version = document.version;
  let tempDir = null;
  let entry = null;
  try {
    tempDir = fs.mkdtempSync(path.join(os.tmpdir(), "ddonilang-console-bogae-"));
    const cellPath = path.join(tempDir, `current${extension}`);
    fs.writeFileSync(cellPath, document.getText(), { encoding: "utf8", flag: "wx" });
    const processHandle = startRuntimeProcess(executable, cellPath);
    entry = {
      child: processHandle.child,
      done: processHandle.done,
      cancelled: false,
    };
    activeExecutions.set(key, entry);
    const result = await entry.done;
    if (entry.cancelled || result.signal || result.code !== 0) {
      showExecutionFailure(vscode, "LSP44_RUNTIME_EXECUTION_FAILED 공식 runtime 실행이 실패했습니다.");
      return null;
    }
    if (!isCurrentDocumentSnapshot(vscode, document, version)) {
      showExecutionFailure(vscode, "LSP44_STALE_DOCUMENT_SNAPSHOT 최신 문서 결과만 게시할 수 있습니다.");
      return null;
    }
    const channel = ensureOutputChannel(context, vscode);
    channel.clear();
    channel.append(result.stdout);
    channel.show(true);
    return result.stdout;
  } catch (_) {
    showExecutionFailure(vscode, "LSP44_RUNTIME_EXECUTION_FAILED 공식 runtime 실행을 시작할 수 없습니다.");
    return null;
  } finally {
    if (activeExecutions.get(key) === entry) {
      activeExecutions.delete(key);
    }
    if (tempDir) {
      try {
        fs.rmSync(tempDir, { recursive: true, force: true });
      } catch (_) {
        // The task-owned temporary directory is best-effort cleanup only.
      }
    }
  }
}

async function stopAllExecutions() {
  const entries = [...activeExecutions.values()];
  for (const entry of entries) {
    entry.cancelled = true;
    if (entry.child && typeof entry.child.kill === "function" && !entry.child.killed) {
      entry.child.kill();
    }
  }
  await Promise.all(entries.map((entry) => entry.done));
}

function registerCommands(context, vscode) {
  if (!vscode.commands || typeof vscode.commands.registerCommand !== "function") {
    return;
  }
  const selectExecutableDisposable = vscode.commands.registerCommand(
    SELECT_EXECUTABLE_COMMAND,
    () => selectLanguageServerExecutable(context, vscode),
  );
  const statusDisposable = vscode.commands.registerCommand(STATUS_COMMAND, () => {
    const status = statusSnapshot(vscode, context);
    const message = formatStatus(status);
    if (vscode.window && typeof vscode.window.showInformationMessage === "function") {
      void vscode.window.showInformationMessage(message);
    }
    return status;
  });
  const restartDisposable = vscode.commands.registerCommand(RESTART_COMMAND, () =>
    restartLanguageServer(context, vscode),
  );
  const consoleBogaeDisposable = vscode.commands.registerCommand(CONSOLE_BOGAE_COMMAND, () =>
    runCurrentDocumentConsoleBogae(context, vscode),
  );
  context.subscriptions.push(selectExecutableDisposable);
  context.subscriptions.push(statusDisposable);
  context.subscriptions.push(restartDisposable);
  context.subscriptions.push(consoleBogaeDisposable);
}

async function startClient(context, vscode) {
  if (activeClient) {
    return activeClient;
  }

  const { LanguageClient } = require("vscode-languageclient/node");
  lifecycleState = "activating";
  lastStartupFailure = null;
  const settings = configuration(vscode);
  const configuredPath = settings.get("executable", "");
  const configuredFailure = configuredExecutableFailure(configuredPath);
  const executable = resolveServerExecutable({
    configuredPath,
    autoDiscover: settings.get("autoDiscover", true),
    extensionPath: context.extensionPath,
    workspaceFolders: vscode.workspace.workspaceFolders,
  });

  if (!executable) {
    lifecycleState = "failed";
    lastStartupFailure = configuredFailure || "AUTODISCOVERY_NOT_FOUND";
    showStartupFailure(
      context,
      vscode,
      lastStartupFailure,
      "Ddonilang LSP를 시작할 수 없습니다. 실행파일을 선택해 복구할 수 있습니다.",
    );
    return null;
  }

  const serverOptions = {
    command: executable,
    args: [],
    options: { cwd: path.dirname(executable) },
  };
  const clientOptions = {
    documentSelector: documentSelector(),
    synchronize: { configurationSection: "ddonilang.lsp" },
  };

  activeClient = new LanguageClient(
    "ddonilangLsp",
    "Ddonilang Language Server",
    serverOptions,
    clientOptions,
  );
  context.subscriptions.push(activeClient);

  try {
    lifecycleState = "starting";
    await activeClient.start();
    lifecycleState = "running";
    startupErrorShown = false;
    return activeClient;
  } catch (error) {
    const failedClient = activeClient;
    activeClient = null;
    lifecycleState = "failed";
    lastStartupFailure = "SERVER_START_FAILED";
    failedClient.dispose();
    showStartupFailure(
      context,
      vscode,
      lastStartupFailure,
      `Ddonilang LSP 시작에 실패했습니다: ${error instanceof Error ? error.message : String(error)}`,
    );
    return null;
  }
}

async function stopActiveClient() {
  const client = activeClient;
  if (!client) {
    lifecycleState = "inactive";
    return true;
  }
  activeClient = null;
  lifecycleState = "stopping";
  try {
    await client.stop();
    lifecycleState = "inactive";
    return true;
  } catch (_) {
    lifecycleState = "failed";
    lastStartupFailure = "SERVER_STOP_FAILED";
    try {
      client.dispose();
    } catch (_) {
      // The client is already detached; preserve the typed failure state.
    }
    return false;
  }
}

function restartLanguageServer(context, vscode) {
  if (restartInFlight) {
    return restartInFlight;
  }
  restartInFlight = (async () => {
    if (!(await stopActiveClient())) {
      return null;
    }
    const restartedClient = await startClient(context, vscode);
    if (!restartedClient && lifecycleState !== "failed") {
      lifecycleState = "failed";
    }
    return restartedClient;
  })().finally(() => {
    restartInFlight = null;
  });
  return restartInFlight;
}

async function activate(context) {
  if (activeClient) {
    return activeClient;
  }

  const vscode = require("vscode");
  lifecycleState = "activating";
  if (!commandsRegistered) {
    registerCommands(context, vscode);
    commandsRegistered = true;
  }
  return startClient(context, vscode);
}

async function deactivate() {
  await stopAllExecutions();
  if (restartInFlight) {
    await restartInFlight;
  }
  if (activeClient) {
    await stopActiveClient();
  } else {
    lifecycleState = "inactive";
  }
  outputChannel = null;
  commandsRegistered = false;
  startupErrorShown = false;
  return undefined;
}

module.exports = {
  activate,
  deactivate,
  boundedLocalCandidates,
  configuredExecutableFailure,
  documentSelector,
  extensionForUri,
  formatStatus,
  isRegularExecutable,
  runtimeExecutableNames,
  resolveRuntimeExecutable,
  runtimeConfiguredExecutableFailure,
  runCurrentDocumentConsoleBogae,
  resolveServerExecutable,
  restartLanguageServer,
  selectLanguageServerExecutable,
  statusSnapshot,
};
