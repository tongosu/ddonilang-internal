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
const configurationUpdates = [];
const selectionQueue = [];
let configurationUpdateFailure = false;
const registeredCommands = new Map();
const clientInstances = [];
const clientEvents = [];

const fakeVscode = {
  workspace: {
    workspaceFolders: [{ fsPath: tempRoot }],
    getConfiguration(section) {
      assert.strictEqual(section, "ddonilang.lsp");
      return {
        get(name, fallback) {
          return Object.hasOwn(configurationState, name) ? configurationState[name] : fallback;
        },
        async update(name, value, target) {
          if (configurationUpdateFailure) {
            throw new Error("synthetic configuration save failure");
          }
          configurationUpdates.push({ name, value, target });
          configurationState[name] = value;
        },
      };
    },
  },
  window: {
    showErrorMessage() {},
    showInformationMessage() {},
    async showOpenDialog() {
      return selectionQueue.shift() || [];
    },
    async showQuickPick(items) {
      return items[0];
    },
    activeTextEditor: null,
  },
  commands: {
    registerCommand(command, callback) {
      assert.ok([
        "ddonilang.selectLanguageServerExecutable",
        "ddonilang.showLanguageServerStatus",
        "ddonilang.restartLanguageServer",
        "ddonilang.runCurrentDocumentConsoleBogae",
      ].includes(command));
      registeredCommands.set(command, callback);
      return { dispose() {} };
    },
  },
  ConfigurationTarget: { Global: 1, Workspace: 2 },
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
    assert.strictEqual(subscriptions.length, 5);
    const status = registeredCommands.get("ddonilang.showLanguageServerStatus")();
    assert.strictEqual(status.lifecycleState, "running");
    assert.strictEqual(status.serverProcessPresent, false);

    const selectExecutable = registeredCommands.get("ddonilang.selectLanguageServerExecutable");
    const invalidSelection = path.join(tempRoot, "invalid-lsp.exe");
    fs.writeFileSync(invalidSelection, "placeholder");
    selectionQueue.push([{ fsPath: invalidSelection }]);
    const beforeInvalidSelection = clientInstances.length;
    assert.strictEqual(await selectExecutable(), null);
    assert.strictEqual(clientInstances.length, beforeInvalidSelection);
    assert.strictEqual(configurationUpdates.length, 0);

    configurationUpdateFailure = true;
    selectionQueue.push([{ fsPath: executable }]);
    assert.strictEqual(await selectExecutable(), null);
    assert.strictEqual(clientInstances.length, beforeInvalidSelection);
    assert.strictEqual(configurationState.executable, executable);
    configurationUpdateFailure = false;

    selectionQueue.push([{ fsPath: executable }]);
    const selected = await selectExecutable();
    assert.strictEqual(selected, clientInstances[1]);
    assert.deepStrictEqual(configurationUpdates, [
      { name: "executable", value: executable, target: 2 },
    ]);

    const restartCommand = registeredCommands.get("ddonilang.restartLanguageServer");
    const firstRestart = restartCommand();
    const secondRestart = restartCommand();
    assert.strictEqual(firstRestart, secondRestart);
    const restarted = await firstRestart;
    assert.strictEqual(restarted, clientInstances[2]);
    assert.strictEqual(clientInstances[1].stopCalls, 1);
    assert.strictEqual(clientInstances[2].startCalls, 1);
    assert.deepStrictEqual(clientEvents.slice(-3), ["stop:2", "construct:3", "start:3"]);

    FakeLanguageClient.failNextStart = true;
    const failed = await restartCommand();
    assert.strictEqual(failed, null);
    const failedStatus = registeredCommands.get("ddonilang.showLanguageServerStatus")();
    assert.strictEqual(failedStatus.lifecycleState, "failed");
    assert.strictEqual(failedStatus.lastStartupFailure, "SERVER_START_FAILED");
    assert.strictEqual(failedStatus.serverProcessPresent, false);

    const recovered = await restartCommand();
    assert.strictEqual(recovered, clientInstances[4]);
    assert.strictEqual(
      registeredCommands.get("ddonilang.showLanguageServerStatus")().lifecycleState,
      "running",
    );

    clientInstances[4].failStop = true;
    const stopFailed = await restartCommand();
    assert.strictEqual(stopFailed, null);
    const stopFailureStatus = registeredCommands.get("ddonilang.showLanguageServerStatus")();
    assert.strictEqual(stopFailureStatus.lifecycleState, "failed");
    assert.strictEqual(stopFailureStatus.lastStartupFailure, "SERVER_STOP_FAILED");
    assert.strictEqual(stopFailureStatus.serverProcessPresent, false);
    clientInstances[4].failStop = false;
    const recoveredAfterStopFailure = await restartCommand();
    assert.strictEqual(recoveredAfterStopFailure, clientInstances[5]);

    await extension.deactivate();
    assert.strictEqual(clientInstances[5].stopCalls, 1);
    await extension.deactivate();
    assert.strictEqual(clientInstances[5].stopCalls, 1);
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
