const assert = require("assert");
const fs = require("fs");
const os = require("os");
const path = require("path");

const extension = require("../extension");
const manifest = require("../package.json");

const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), "ddonilang-vscode-"));

try {
  assert.strictEqual(manifest.main, "./extension.js");
  assert.deepStrictEqual(manifest.activationEvents, [
    "onLanguage:ddonilang",
    "onCommand:ddonilang.selectLanguageServerExecutable",
    "onCommand:ddonilang.showLanguageServerStatus",
    "onCommand:ddonilang.restartLanguageServer",
    "onCommand:ddonilang.runCurrentDocumentConsoleBogae",
  ]);
  assert.strictEqual(manifest.dependencies["vscode-languageclient"], "8.1.0");
  assert.strictEqual(manifest.contributes.snippets[0].language, "ddonilang");
  assert.deepStrictEqual(
    manifest.contributes.commands.map(({ command }) => command),
    [
      "ddonilang.selectLanguageServerExecutable",
      "ddonilang.showLanguageServerStatus",
      "ddonilang.restartLanguageServer",
      "ddonilang.runCurrentDocumentConsoleBogae",
    ],
  );
  assert.deepStrictEqual(manifest.contributes.languages[0].extensions, [".ddn", ".또니", ".ddl", ".옮김"]);
  assert.deepStrictEqual(manifest.contributes.semanticTokenScopes, [
    {
      language: "ddonilang",
      scopes: {
        function: ["entity.name.function.ddn", "entity.name.function.call.ddn"],
        type: ["storage.type.ddn", "entity.name.type.ddn"],
        variable: ["variable.other.ddn"],
        parameter: ["variable.parameter.ddn"],
        keyword: ["keyword.control.ddn"],
        string: ["string.quoted.double.ddn"],
        number: ["constant.numeric.ddn"],
        operator: ["keyword.operator.ddn"],
        atom: ["constant.other.ddn"],
        josa: ["keyword.other.josa.ddn"],
      },
    },
  ]);
  assert.deepStrictEqual(manifest.contributes.themes, [
    {
      label: "Ddonilang Readable",
      uiTheme: "vs-dark",
      path: "./themes/ddonilang-readable-color-theme.json",
    },
  ]);
  assert.deepStrictEqual(extension.documentSelector(), [
    { scheme: "file", language: "ddonilang" },
    { scheme: "untitled", language: "ddonilang" },
  ]);

  const workspaceRoot = path.join(tempRoot, "workspace");
  const debugDir = path.join(workspaceRoot, "target", "debug");
  fs.mkdirSync(debugDir, { recursive: true });
  const discovered = path.join(debugDir, process.platform === "win32" ? "ddonirang-lsp.exe" : "ddonirang-lsp");
  fs.writeFileSync(discovered, "placeholder");
  const directory = path.join(tempRoot, "directory");
  fs.mkdirSync(directory);

  assert.strictEqual(
    extension.resolveServerExecutable({
      configuredPath: "",
      autoDiscover: true,
      extensionPath: path.join(workspaceRoot, "tools", "vscode-ddn"),
      workspaceFolders: [{ fsPath: workspaceRoot }],
    }),
    discovered,
  );
  assert.strictEqual(
    extension.resolveServerExecutable({
      configuredPath: path.join(workspaceRoot, "missing-lsp"),
      autoDiscover: true,
      extensionPath: path.join(workspaceRoot, "tools", "vscode-ddn"),
      workspaceFolders: [{ fsPath: workspaceRoot }],
    }),
    null,
  );
  assert.strictEqual(
    extension.configuredExecutableFailure(path.join(workspaceRoot, "missing-lsp")),
    "CONFIGURED_PATH_MISSING",
  );
  assert.strictEqual(
    extension.configuredExecutableFailure("relative-lsp"),
    "CONFIGURED_PATH_NOT_ABSOLUTE",
  );
  assert.strictEqual(
    extension.configuredExecutableFailure(directory),
    "CONFIGURED_PATH_DIRECTORY",
  );
  const unsupportedFilename = path.join(tempRoot, "other-server.exe");
  fs.writeFileSync(unsupportedFilename, "placeholder");
  assert.strictEqual(
    extension.configuredExecutableFailure(unsupportedFilename),
    "CONFIGURED_PATH_UNSUPPORTED_FILENAME",
  );
  assert.strictEqual(extension.extensionForUri("file:///a.ddn"), ".ddn");
  assert.strictEqual(extension.extensionForUri("file:///a.또니"), ".또니");
  assert.strictEqual(extension.extensionForUri("file:///a.txt"), null);
  assert.deepStrictEqual(extension.runtimeExecutableNames(),
    process.platform === "win32"
      ? ["ddonilang.exe", "또니랑.exe", "ddonirang.exe"]
      : ["ddonilang", "또니랑", "ddonirang"],
  );
  assert.strictEqual(
    extension.runtimeConfiguredExecutableFailure(path.join(workspaceRoot, "missing-runtime.exe")),
    "CONFIGURED_PATH_MISSING",
  );
  assert.strictEqual(
    extension.runtimeConfiguredExecutableFailure(path.join(tempRoot, "other-server.exe")),
    "CONFIGURED_PATH_UNSUPPORTED_FILENAME",
  );
  assert.strictEqual(
    extension.resolveRuntimeExecutable({
      configuredPath: path.join(tempRoot, "other-server.exe"),
      autoDiscover: false,
      extensionPath: path.join(workspaceRoot, "tools", "vscode-ddn"),
      workspaceFolders: [{ fsPath: workspaceRoot }],
    }),
    null,
  );
  assert.strictEqual(
    extension.resolveServerExecutable({
      configuredPath: "relative-lsp",
      autoDiscover: true,
      extensionPath: path.join(workspaceRoot, "tools", "vscode-ddn"),
      workspaceFolders: [{ fsPath: workspaceRoot }],
    }),
    null,
  );
  assert.strictEqual(
    extension.resolveServerExecutable({
      configuredPath: "",
      autoDiscover: false,
      extensionPath: path.join(workspaceRoot, "tools", "vscode-ddn"),
      workspaceFolders: [{ fsPath: workspaceRoot }],
    }),
    null,
  );

  assert.strictEqual(extension.isRegularExecutable(directory), false);

  const symlink = path.join(tempRoot, "symlink");
  try {
    fs.symlinkSync(discovered, symlink, "file");
    assert.strictEqual(extension.isRegularExecutable(symlink), false);
  } catch (error) {
    if (error.code !== "EPERM" && error.code !== "EACCES") {
      throw error;
    }
  }

  console.log("extension tests: PASS");
} finally {
  fs.rmSync(tempRoot, { recursive: true, force: true });
}
