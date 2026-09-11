const assert = require("assert");
const fs = require("fs");
const Module = require("module");
const os = require("os");
const path = require("path");

const extension = require("../extension");
const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), "ddonilang-vscode-activation-"));
const executable = path.join(tempRoot, process.platform === "win32" ? "ddonirang-lsp.exe" : "ddonirang-lsp");
fs.writeFileSync(executable, "placeholder");
const configurationState = { executable, autoDiscover: true };
const registeredCommands = new Map();
const clientInstances = [];
const clientEvents = [];

const fakeVscode = {
  workspace: {
    workspaceFolders: [],
    getConfiguration(section) {
      assert.strictEqual(section, "ddonilang.lsp");
      return {
        get(name, fallback) {
          return Object.hasOwn(configurationState, name) ? configurationState[name] : fallback;
        },
      };
    },
  },
  window: {
    showErrorMessage() {},
    showInformationMessage() {},
    activeTextEditor: null,
  },
  commands: {
    registerCommand(command, callback) {
      assert.ok([
        "ddonilang.showLanguageServerStatus",
        "ddonilang.restartLanguageServer",
      ].includes(command));
      registeredCommands.set(command, callback);
      return { dispose() {} };
    },
  },
};

class FakeLanguageClient {
  constructor(id, name, serverOptions, clientOptions) {
    this.id = id;
    this.name = name;
    this.serverOptions = serverOptions;
    this.clientOptions = clientOptions;
    this.startCalls = 0;
    this.stopCalls = 0;
    this.disposeCalls = 0;
    this.failStart = false;
    this.failStop = false;
    clientInstances.push(this);
    clientEvents.push(`construct:${clientInstances.length}`);
  }

  async start() {
    this.startCalls += 1;
    clientEvents.push(`start:${clientInstances.length}`);
    if (this.failStart || FakeLanguageClient.failNextStart) {
      FakeLanguageClient.failNextStart = false;
      throw new Error("synthetic start failure");
    }
  }

  async stop() {
    this.stopCalls += 1;
    clientEvents.push(`stop:${clientInstances.indexOf(this) + 1}`);
    if (this.failStop) {
      throw new Error("synthetic stop failure");
    }
  }

  dispose() {
    this.disposeCalls += 1;
    clientEvents.push(`dispose:${clientInstances.indexOf(this) + 1}`);
  }
}
FakeLanguageClient.failNextStart = false;

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
    assert.strictEqual(client, clientInstances[0]);
    assert.strictEqual(reusedClient, client);
    assert.strictEqual(client.startCalls, 1);
    assert.strictEqual(client.serverOptions.command, executable);
    assert.deepStrictEqual(client.clientOptions.documentSelector, [
      { scheme: "file", language: "ddonilang" },
      { scheme: "untitled", language: "ddonilang" },
    ]);
    assert.strictEqual(subscriptions.length, 3);
    const status = registeredCommands.get("ddonilang.showLanguageServerStatus")();
    assert.strictEqual(status.lifecycleState, "running");
    assert.strictEqual(status.serverProcessPresent, false);

    const restartCommand = registeredCommands.get("ddonilang.restartLanguageServer");
    const firstRestart = restartCommand();
    const secondRestart = restartCommand();
    assert.strictEqual(firstRestart, secondRestart);
    const restarted = await firstRestart;
    assert.strictEqual(restarted, clientInstances[1]);
    assert.strictEqual(clientInstances[0].stopCalls, 1);
    assert.strictEqual(clientInstances[1].startCalls, 1);
    assert.deepStrictEqual(clientEvents.slice(-3), ["stop:1", "construct:2", "start:2"]);

    FakeLanguageClient.failNextStart = true;
    const failed = await restartCommand();
    assert.strictEqual(failed, null);
    const failedStatus = registeredCommands.get("ddonilang.showLanguageServerStatus")();
    assert.strictEqual(failedStatus.lifecycleState, "failed");
    assert.strictEqual(failedStatus.lastStartupFailure, "SERVER_START_FAILED");
    assert.strictEqual(failedStatus.serverProcessPresent, false);

    const recovered = await restartCommand();
    assert.strictEqual(recovered, clientInstances[3]);
    assert.strictEqual(
      registeredCommands.get("ddonilang.showLanguageServerStatus")().lifecycleState,
      "running",
    );

    clientInstances[3].failStop = true;
    const stopFailed = await restartCommand();
    assert.strictEqual(stopFailed, null);
    const stopFailureStatus = registeredCommands.get("ddonilang.showLanguageServerStatus")();
    assert.strictEqual(stopFailureStatus.lifecycleState, "failed");
    assert.strictEqual(stopFailureStatus.lastStartupFailure, "SERVER_STOP_FAILED");
    assert.strictEqual(stopFailureStatus.serverProcessPresent, false);
    clientInstances[3].failStop = false;
    const recoveredAfterStopFailure = await restartCommand();
    assert.strictEqual(recoveredAfterStopFailure, clientInstances[4]);

    await extension.deactivate();
    assert.strictEqual(clientInstances[4].stopCalls, 1);
    await extension.deactivate();
    assert.strictEqual(clientInstances[4].stopCalls, 1);
    assert.strictEqual(
      registeredCommands.get("ddonilang.showLanguageServerStatus")().lifecycleState,
      "inactive",
    );
    console.log("activation tests: PASS");
  } finally {
    Module._load = originalLoad;
    fs.rmSync(tempRoot, { recursive: true, force: true });
  }
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
