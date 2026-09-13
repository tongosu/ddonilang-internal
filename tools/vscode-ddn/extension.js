const fs = require("fs");
const path = require("path");

let activeClient = null;
let startupErrorShown = false;

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
    return stat.isFile() && !stat.isSymbolicLink();
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

function documentSelector() {
  return [
    { scheme: "file", language: "ddonilang" },
    { scheme: "untitled", language: "ddonilang" },
  ];
}

function configuration(vscode) {
  return vscode.workspace.getConfiguration("ddonilang.lsp");
}

async function activate(context) {
  if (activeClient) {
    return activeClient;
  }

  const vscode = require("vscode");
  const { LanguageClient } = require("vscode-languageclient/node");
  const settings = configuration(vscode);
  const executable = resolveServerExecutable({
    configuredPath: settings.get("executable", ""),
    autoDiscover: settings.get("autoDiscover", true),
    extensionPath: context.extensionPath,
    workspaceFolders: vscode.workspace.workspaceFolders,
  });

  if (!executable) {
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
    await activeClient.start();
    return activeClient;
  } catch (error) {
    const failedClient = activeClient;
    activeClient = null;
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

async function deactivate() {
  if (!activeClient) {
    return undefined;
  }
  const client = activeClient;
  activeClient = null;
  return client.stop();
}

module.exports = {
  activate,
  deactivate,
  boundedLocalCandidates,
  documentSelector,
  isRegularExecutable,
  resolveServerExecutable,
};
