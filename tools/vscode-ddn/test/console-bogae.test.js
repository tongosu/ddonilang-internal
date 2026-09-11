const assert = require("assert");
const EventEmitter = require("events");
const fs = require("fs");
const Module = require("module");
const os = require("os");
const path = require("path");

const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), "ddonilang-vscode-console-"));
const runtime = path.join(tempRoot, process.platform === "win32" ? "ddonilang.exe" : "ddonilang");
const server = path.join(tempRoot, process.platform === "win32" ? "ddonirang-lsp.exe" : "ddonirang-lsp");
fs.writeFileSync(runtime, "placeholder");
fs.writeFileSync(server, "placeholder");

const configuration = {
  "ddonilang.lsp": { executable: server, autoDiscover: false },
  "ddonilang.runtime": { executable: runtime, autoDiscover: false },
};
const commands = new Map();
const warnings = [];
const output = { text: "", shown: 0 };
const documents = [];
let activeDocument = null;
const spawnCalls = [];
const spawnBehaviors = [];

function documentFor(filePath, languageId, version, text) {
  return {
    uri: {
      path: filePath,
      toString() {
        return `file://${filePath}`;
      },
    },
    languageId,
    version,
    getText() {
      return text;
    },
  };
}

function fakeSpawn(executable, args, options) {
  const child = new EventEmitter();
  child.stdout = new EventEmitter();
  child.stderr = new EventEmitter();
  child.killed = false;
  child.kill = () => {
    if (child.killed) {
      return true;
    }
    child.killed = true;
    process.nextTick(() => child.emit("close", null, "SIGTERM"));
    return true;
  };
  spawnCalls.push({ executable, args, options, child });
  const behavior = spawnBehaviors.shift() || { stdout: "23\n", code: 0 };
  if (!behavior.hold) {
    process.nextTick(() => {
      if (typeof behavior.onStart === "function") {
        behavior.onStart();
      }
      if (behavior.stderr) {
        child.stderr.emit("data", behavior.stderr);
      }
      if (behavior.stdout) {
        child.stdout.emit("data", behavior.stdout);
      }
      child.emit("close", behavior.code ?? 0, behavior.signal ?? null);
    });
  }
  return child;
}

const fakeVscode = {
  workspace: {
    workspaceFolders: [],
    get textDocuments() {
      return documents;
    },
    getConfiguration(section) {
      const values = configuration[section] || {};
      return {
        get(name, fallback) {
          return Object.hasOwn(values, name) ? values[name] : fallback;
        },
      };
    },
  },
  window: {
    get activeTextEditor() {
      return activeDocument ? { document: activeDocument } : null;
    },
    createOutputChannel() {
      return {
        clear() {
          output.text = "";
        },
        append(value) {
          output.text += value;
        },
        show() {
          output.shown += 1;
        },
        dispose() {},
      };
    },
    showWarningMessage(message) {
      warnings.push(message);
    },
    showErrorMessage(message) {
      warnings.push(message);
    },
    showInformationMessage() {},
  },
  commands: {
    registerCommand(command, callback) {
      commands.set(command, callback);
      return { dispose() {} };
    },
  },
};

class FakeLanguageClient {
  constructor() {}
  async start() {}
  async stop() {}
  dispose() {}
}

const originalLoad = Module._load;
Module._load = function patchedLoad(request, parent, isMain) {
  if (request === "vscode") {
    return fakeVscode;
  }
  if (request === "vscode-languageclient/node") {
    return { LanguageClient: FakeLanguageClient };
  }
  if (request === "child_process") {
    return { spawn: fakeSpawn };
  }
  return originalLoad.call(this, request, parent, isMain);
};

const extension = require("../extension");

function setActive(fileName, extensionName, version, text) {
  activeDocument = documentFor(path.join(tempRoot, `${fileName}${extensionName}`), "ddonilang", version, text);
  documents.splice(0, documents.length, activeDocument);
}

(async () => {
  try {
    const context = {
      extensionPath: path.join(tempRoot, "extension"),
      subscriptions: { push() {} },
    };
    await extension.activate(context);
    const run = commands.get("ddonilang.runCurrentDocumentConsoleBogae");
    assert.strictEqual(typeof run, "function");

    setActive("current", ".ddn", 1, "값 = 2\n보여주기(😀한글)");
    spawnBehaviors.push({ stdout: "23\n", code: 0 });
    assert.strictEqual(await run(), "23\n");
    assert.strictEqual(output.text, "23\n");
    assert.strictEqual(output.shown, 1);
    assert.deepStrictEqual(spawnCalls[0].args.slice(0, 5), [
      "currentline-run",
      "--cell",
      spawnCalls[0].args[2],
      "--source-profile",
      "v1-core-v25",
    ]);
    assert.strictEqual(fs.existsSync(spawnCalls[0].args[2]), false);

    setActive("current", ".또니", 1, "값 = 2");
    spawnBehaviors.push({ stdout: "23\n", code: 0 });
    assert.strictEqual(await run(), "23\n");

    const beforeDdl = spawnCalls.length;
    setActive("current", ".ddl", 1, "#!한국어");
    assert.strictEqual(await run(), null);
    assert.strictEqual(spawnCalls.length, beforeDdl);
    assert.ok(warnings.some((message) => message.includes("LSP44_NON_EXECUTABLE_SURFACE")));

    setActive("current", ".ddn", 1, "값 = 3");
    spawnBehaviors.push({ stdout: "stale\n", code: 0, onStart: () => { activeDocument.version = 2; } });
    assert.strictEqual(await run(), null);
    assert.strictEqual(output.text, "23\n");
    assert.ok(warnings.some((message) => message.includes("LSP44_STALE_DOCUMENT_SNAPSHOT")));

    setActive("current", ".ddn", 1, "값 = 4");
    spawnBehaviors.push({ hold: true });
    const pending = run();
    await new Promise((resolve) => setImmediate(resolve));
    assert.strictEqual(await run(), null);
    assert.ok(warnings.some((message) => message.includes("LSP44_DUPLICATE_INVOCATION")));
    await extension.deactivate();
    assert.strictEqual(spawnCalls.at(-1).child.killed, true);
    assert.strictEqual(await pending, null);
    assert.ok(warnings.some((message) => message.includes("LSP44_RUNTIME_EXECUTION_FAILED")));
    console.log("console bogae tests: PASS");
  } finally {
    Module._load = originalLoad;
    fs.rmSync(tempRoot, { recursive: true, force: true });
  }
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
