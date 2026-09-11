const assert = require("assert");
const fs = require("fs");
const Module = require("module");
const os = require("os");
const path = require("path");

const extension = require("../extension");
const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), "ddonilang-vscode-activation-"));
const executable = path.join(tempRoot, process.platform === "win32" ? "ddonirang-lsp.exe" : "ddonirang-lsp");
fs.writeFileSync(executable, "placeholder");

const fakeVscode = {
  workspace: {
    workspaceFolders: [],
    getConfiguration(section) {
      assert.strictEqual(section, "ddonilang.lsp");
      return {
        get(name, fallback) {
          return name === "executable" ? executable : fallback;
        },
      };
    },
  },
  window: {
    showErrorMessage() {
      throw new Error("unexpected extension startup error");
    },
    showInformationMessage() {},
    activeTextEditor: null,
  },
  commands: {
    registerCommand(command, callback) {
      assert.strictEqual(command, "ddonilang.showLanguageServerStatus");
      registeredStatusCommand = callback;
      return { dispose() {} };
    },
  },
};

let clientInstance;
let registeredStatusCommand;
class FakeLanguageClient {
  constructor(id, name, serverOptions, clientOptions) {
    this.id = id;
    this.name = name;
    this.serverOptions = serverOptions;
    this.clientOptions = clientOptions;
    this.startCalls = 0;
    this.stopCalls = 0;
    this.disposeCalls = 0;
    clientInstance = this;
  }

  async start() {
    this.startCalls += 1;
  }

  async stop() {
    this.stopCalls += 1;
  }

  dispose() {
    this.disposeCalls += 1;
  }
}

const originalLoad = Module._load;
Module._load = function patchedLoad(request, parent, isMain) {
  if (request === "vscode") {
    return fakeVscode;
  }
  if (request === "vscode-languageclient/node") {
    return { LanguageClient: FakeLanguageClient };
  }
  return originalLoad.call(this, request, parent, isMain);
};

(async () => {
  try {
    const subscriptions = [];
    const client = await extension.activate({
      extensionPath: path.join(tempRoot, "tools", "vscode-ddn"),
      subscriptions: { push(value) { subscriptions.push(value); } },
    });
    const reusedClient = await extension.activate({
      extensionPath: path.join(tempRoot, "tools", "vscode-ddn"),
      subscriptions: { push() {} },
    });
    assert.strictEqual(client, clientInstance);
    assert.strictEqual(reusedClient, client);
    assert.strictEqual(client.startCalls, 1);
    assert.strictEqual(client.serverOptions.command, executable);
    assert.deepStrictEqual(client.clientOptions.documentSelector, [
      { scheme: "file", language: "ddonilang" },
      { scheme: "untitled", language: "ddonilang" },
    ]);
    assert.strictEqual(subscriptions.length, 2);
    const status = registeredStatusCommand();
    assert.strictEqual(status.lifecycleState, "running");
    assert.strictEqual(status.serverProcessPresent, false);

    await extension.deactivate();
    assert.strictEqual(client.stopCalls, 1);
    await extension.deactivate();
    assert.strictEqual(client.stopCalls, 1);
    assert.strictEqual(registeredStatusCommand().lifecycleState, "inactive");
    console.log("activation tests: PASS");
  } finally {
    Module._load = originalLoad;
    fs.rmSync(tempRoot, { recursive: true, force: true });
  }
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
