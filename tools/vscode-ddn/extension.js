const fs = require("fs");
const path = require("path");

let activeClient = null;
let restartInFlight = null;
let commandsRegistered = false;
let startupErrorShown = false;
let lifecycleState = "inactive";
let lastStartupFailure = null;

const SUPPORTED_EXTENSIONS = [".ddn", ".또니", ".ddl", ".옮김"];
const STATUS_COMMAND = "ddonilang.showLanguageServerStatus";
const RESTART_COMMAND = "ddonilang.restartLanguageServer";

function isLocalAbsolutePath(candidate) {
  if (typeof candidate !== "string" || candidate.length === 0) {
    return false;
  }
  if (!path.isAbsolute(candidate)) {
    return false;
  }
  return process.platform !== "win32" || !candidate.startsWith("\\\\");
}

function isRegularExecutable(candidate) {
  if (!isLocalAbsolutePath(candidate)) {
    return false;
  }
  try {
    const stat = fs.lstatSync(candidate);
    return (
      stat.isFile() &&
      !stat.isSymbolicLink() &&
      path.basename(candidate).toLowerCase() === executableName().toLowerCase()
    );
  } catch (_) {
    return false;
  }
}

function executableName() {
  return process.platform === "win32" ? "ddonirang-lsp.exe" : "ddonirang-lsp";
}

function boundedLocalCandidates(extensionPath, workspaceFolders) {
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
      const candidate = path.resolve(root, "target", profile, executableName());
      if (!seen.has(candidate)) {
        seen.add(candidate);
        result.push(candidate);
      }
    }
  }
  return result;
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

function configuredExecutableFailure(candidate) {
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
  if (path.basename(exactPath).toLowerCase() !== executableName().toLowerCase()) {
    return "CONFIGURED_PATH_UNSUPPORTED_FILENAME";
  }
  return null;
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

function registerCommands(context, vscode) {
  if (!vscode.commands || typeof vscode.commands.registerCommand !== "function") {
    return;
  }
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
  context.subscriptions.push(statusDisposable);
  context.subscriptions.push(restartDisposable);
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
    if (!startupErrorShown) {
      startupErrorShown = true;
      void vscode.window.showErrorMessage(
        "Ddonilang LSP를 시작할 수 없습니다. ddonilang.lsp.executable에 로컬 실행 파일 경로를 지정하거나 autoDiscover를 확인하세요.",
      );
    }
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
    return activeClient;
  } catch (error) {
    const failedClient = activeClient;
    activeClient = null;
    lifecycleState = "failed";
    lastStartupFailure = "SERVER_START_FAILED";
    failedClient.dispose();
    if (!startupErrorShown) {
      startupErrorShown = true;
      void vscode.window.showErrorMessage(
        `Ddonilang LSP 시작에 실패했습니다: ${error instanceof Error ? error.message : String(error)}`,
      );
    }
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
  if (restartInFlight) {
    await restartInFlight;
  }
  if (!activeClient) {
    lifecycleState = "inactive";
    return undefined;
  }
  await stopActiveClient();
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
  resolveServerExecutable,
  restartLanguageServer,
  statusSnapshot,
};
