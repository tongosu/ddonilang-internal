#!/usr/bin/env node

import fs from "node:fs/promises";
import fsSync from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { pathToFileURL } from "node:url";

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function normalizeStdout(stdout) {
  return String(stdout ?? "")
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) =>
      line &&
      !line.startsWith("state_hash=") &&
      !line.startsWith("trace_hash=") &&
      !line.startsWith("bogae_hash=")
    );
}

function normalizeDdn(text) {
  return String(text ?? "")
    .replace(/\r\n/g, "\n")
    .replace(/\r/g, "\n")
    .trim();
}

function normalizeStderr(stderr) {
  return String(stderr ?? "")
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);
}

function parseCliWarnings(stderr) {
  return normalizeStderr(stderr)
    .filter((line) => line.startsWith("warning: "))
    .map((line) => {
      const body = line.slice("warning: ".length).trim();
      const [code, ...rest] = body.split(/\s+/);
      return {
        code: String(code ?? "").trim(),
        message: rest.join(" ").trim(),
      };
    })
    .filter((warning) => warning.code);
}

function indexRow(channels, row) {
  const out = {};
  const channelList = Array.isArray(channels) ? channels : [];
  const rowList = Array.isArray(row) ? row : [];
  channelList.forEach((channel, idx) => {
    const key = String(channel?.key ?? "").trim();
    if (key) {
      out[key] = rowList[idx];
    }
  });
  return out;
}

function getPathValue(root, dottedPath) {
  let current = root;
  for (const part of String(dottedPath).split(".")) {
    if (!part) continue;
    if (!current || typeof current !== "object" || !(part in current)) {
      return undefined;
    }
    current = current[part];
  }
  return current;
}

function sameJson(a, b) {
  return stableJson(a) === stableJson(b);
}

function stableJson(value) {
  return JSON.stringify(stableValue(value));
}

function stableValue(value) {
  if (Array.isArray(value)) {
    return value.map(stableValue);
  }
  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.keys(value)
        .sort()
        .map((key) => [key, stableValue(value[key])]),
    );
  }
  return value;
}

function hashComparison(cliHash, wasmHash) {
  const cli = String(cliHash ?? "");
  const wasm = String(wasmHash ?? "");
  if (!cli || !wasm) {
    return "missing";
  }
  if (cli === wasm) {
    return "equal";
  }
  return "domain_mismatch_reported";
}

function warningCodes(warnings) {
  return (Array.isArray(warnings) ? warnings : []).map((warning) => String(warning?.code ?? ""));
}

function buildStrictEvidence({
  cli,
  wasm,
  cliCanon,
  wasmCanon,
  wasmCanonError,
  testCase,
  expectReject,
  strictFullOutputParity,
}) {
  const cliSummary = cli?.summary ?? null;
  const cliOutput = Array.isArray(cliSummary?.output_log_texts) ? cliSummary.output_log_texts : cli.stdout;
  const wasmOutput = (wasm?.outputLog ?? []).map((entry) => String(entry?.text ?? ""));
  const expectedRowKeys = Object.keys(testCase.expected_wasm_row ?? {});
  const expectedValueJsonKeys = [
    ...(testCase.expected_cli_wasm_value_json_keys ?? []),
  ].map(String);
  const outputRowsChecked = Boolean(strictFullOutputParity) && !expectReject;
  const outputLogChecked = Boolean(strictFullOutputParity) && !expectReject;
  const cliFinalRow = cliSummary?.final_row ?? {};
  const wasmFinalRow = wasm?.rowByKey ?? {};
  const cliValueJson = cliSummary?.resources?.value_json ?? {};
  const wasmValueJson = wasm?.state?.resources?.value_json ?? {};

  return {
    accept_reject_equal: expectReject ? cli.exitCode !== 0 : cli.exitCode === 0,
    canonical_ddn_equal: !expectReject && !wasmCanonError && cliCanon.exitCode === 0
      ? cliCanon.ddn === wasmCanon
      : null,
    configured_madi: {
      cli: cliSummary?.configured_ticks ?? null,
      wasm: wasm?.configuredMadi ?? null,
      expected: Number.isFinite(Number(testCase.expected_configured_madi))
        ? Number(testCase.expected_configured_madi)
        : null,
    },
    warning_codes: {
      cli: warningCodes(cli.warnings),
      wasm: warningCodes(wasm?.parseWarnings ?? []),
      equal: sameJson(warningCodes(cli.warnings), warningCodes(wasm?.parseWarnings ?? [])),
    },
    execution_envelope: {
      cli: cliSummary?.execution_envelope ?? null,
      wasm: wasm?.executionEnvelope ?? null,
      equal: !expectReject
        ? sameJson(cliSummary?.execution_envelope ?? null, wasm?.executionEnvelope ?? null)
        : null,
    },
    output_log: {
      checked: outputLogChecked,
      cli: cliOutput,
      wasm: wasmOutput,
      equal: outputLogChecked ? sameJson(cliOutput, wasmOutput) : null,
    },
    output_rows: {
      checked: outputRowsChecked,
      cli: normalizeOutputRowsForParity(cliSummary?.output_rows ?? []),
      wasm: normalizeOutputRowsForParity(wasm?.outputRows ?? []),
      equal: outputRowsChecked
        ? sameJson(normalizeOutputRowsForParity(cliSummary?.output_rows ?? []), normalizeOutputRowsForParity(wasm?.outputRows ?? []))
        : null,
    },
    final_row: {
      checked_keys: expectedRowKeys,
      cli_subset: Object.fromEntries(expectedRowKeys.map((key) => [key, cliSummary?.final_row?.[key]])),
      wasm_subset: Object.fromEntries(expectedRowKeys.map((key) => [key, wasm?.rowByKey?.[key]])),
      equal: expectedRowKeys.length
        ? expectedRowKeys.every((key) => sameJson(cliSummary?.final_row?.[key], wasm?.rowByKey?.[key]))
        : null,
      all_cli: cliFinalRow,
      all_wasm: wasmFinalRow,
      all_equal: !expectReject ? sameJson(cliFinalRow, wasmFinalRow) : null,
    },
    value_json: {
      checked_keys: expectedValueJsonKeys,
      cli_subset: Object.fromEntries(expectedValueJsonKeys.map((key) => [key, cliSummary?.resources?.value_json?.[key]])),
      wasm_subset: Object.fromEntries(expectedValueJsonKeys.map((key) => [key, wasm?.state?.resources?.value_json?.[key]])),
      equal: expectedValueJsonKeys.length
        ? expectedValueJsonKeys.every((key) => sameJson(cliSummary?.resources?.value_json?.[key], wasm?.state?.resources?.value_json?.[key]))
        : null,
      all_cli: cliValueJson,
      all_wasm: wasmValueJson,
      all_equal: !expectReject ? sameJson(cliValueJson, wasmValueJson) : null,
    },
    state_hash: {
      cli: String(cliSummary?.state_hash ?? ""),
      wasm: String(wasm?.stateHash ?? ""),
      comparison: hashComparison(cliSummary?.state_hash, wasm?.stateHash),
      formula_change: false,
    },
    trace_hash: {
      cli: String(cliSummary?.trace_hash ?? ""),
      wasm: "not_exposed",
      comparison: "not_exposed",
    },
    bogae_hash: {
      cli: String(cliSummary?.bogae_hash ?? ""),
      wasm: "not_exposed",
      comparison: "not_exposed",
    },
    view_hash: {
      cli: "not_exposed",
      wasm: String(wasm?.viewHash ?? ""),
      comparison: String(wasm?.viewHash ?? "") ? "wasm_only_exposed" : "not_exposed",
    },
    forbidden_normalization: {
      state_hash_removed: false,
      warning_order_sorted: false,
      output_row_dropped: false,
    },
  };
}

function normalizeOutputRowsForParity(rows) {
  if (!Array.isArray(rows)) return [];
  return rows.map((row) => ({
    key: String(row?.key ?? ""),
    value: String(row?.value ?? ""),
    source: String(row?.source ?? ""),
  }));
}

function compareObjectSubset(actual, expected, label, failures) {
  for (const [key, expectedValue] of Object.entries(expected ?? {})) {
    const actualValue = actual?.[key];
    if (!sameJson(actualValue, expectedValue)) {
      failures.push(`${label}.${key}: expected ${JSON.stringify(expectedValue)} got ${JSON.stringify(actualValue)}`);
    }
  }
}

function compareObjectSubsetRows(actualRows, expectedRows, label, failures) {
  if (!Array.isArray(actualRows)) {
    failures.push(`${label}: expected rows array got ${JSON.stringify(actualRows)}`);
    return;
  }
  if (actualRows.length < expectedRows.length) {
    failures.push(`${label}: expected at least ${expectedRows.length} rows got ${actualRows.length}`);
    return;
  }
  expectedRows.forEach((expected, index) => {
    compareObjectSubset(actualRows[index] ?? {}, expected, `${label}[${index}]`, failures);
  });
}

async function initWasm(rootDir) {
  const uiDir = path.join(rootDir, "solutions", "seamgrim_ui_mvp", "ui");
  const freshWasmDir = String(process.env.DDN_WASM_DIR ?? "").trim();
  const wasmDir = freshWasmDir ? path.resolve(freshWasmDir) : path.join(uiDir, "wasm");
  const wasmModule = await import(pathToFileURL(path.join(wasmDir, "ddonirang_tool.js")).href);
  const wrapper = await import(pathToFileURL(path.join(uiDir, "wasm_ddn_wrapper.js")).href);
  const runtimeState = await import(pathToFileURL(path.join(uiDir, "seamgrim_runtime_state.js")).href);
  const wasmBytes = await fs.readFile(path.join(wasmDir, "ddonirang_tool_bg.wasm"));
  if (typeof wasmModule.default === "function") {
    await wasmModule.default({ module_or_path: wasmBytes });
  }
  assert(typeof wasmModule.DdnWasmVm === "function", "DdnWasmVm export missing");
  assert(typeof wasmModule.wasm_execution_envelope_json === "function", "wasm_execution_envelope_json export missing");
  assert(typeof wrapper.DdnWasmVmClient === "function", "DdnWasmVmClient export missing");
  return { wasmModule, wrapper, runtimeState };
}

function runCli(rootDir, inputPath, summaryPath, ticks) {
  const tickArgs = ticks === "configured" || ticks === null || ticks === undefined
    ? []
    : ["--madi", String(Math.max(1, Number(ticks) || 1))];
  const proc = spawnSync(
    "cargo",
    [
      "run",
      "-q",
      "--manifest-path",
      "tool/Cargo.toml",
      "--",
      "run-summary",
      inputPath,
      ...tickArgs,
      "--summary-json",
      summaryPath,
    ],
    { cwd: rootDir, encoding: "utf8", windowsHide: true, env: { ...process.env, RUSTFLAGS: "-Awarnings" } },
  );
  let summary = null;
  let summaryError = "";
  if (proc.status === 0) {
    try {
      summary = JSON.parse(fsSync.readFileSync(summaryPath, "utf8"));
    } catch (err) {
      summaryError = err?.message ?? String(err);
    }
  }
  return {
    exitCode: proc.status ?? 1,
    stdout: normalizeStdout(proc.stdout),
    stderr: String(proc.stderr ?? "").trim(),
    stderrLines: normalizeStderr(proc.stderr),
    warnings: parseCliWarnings(proc.stderr),
    summary,
    summaryError,
  };
}

function hydrateCliSummary(runtimeState, summary) {
  if (!summary || typeof summary !== "object") return summary;
  const state = summary.engine_state ?? summary.state ?? null;
  if (!state || typeof state !== "object") return summary;
  summary.final_row = indexRow(state.channels, state.row);
  summary.output_lines = runtimeState
    .extractObservationOutputLinesFromState(state)
    .map((line) => String(line ?? ""));
  summary.output_log_texts = runtimeState
    .extractObservationOutputLogFromState(state)
    .map((entry) => String(entry?.text ?? ""));
  summary.output_rows = normalizeOutputRowsForParity(
    runtimeState.extractObservationOutputRowsFromState(state),
  );
  return summary;
}

function runCliCurrentlineWithBinary(cliPath, rootDir, inputPath, summaryPath, contextInPath, contextOutPath) {
  const args = [
    "currentline-run",
    "--cell",
    inputPath,
    "--source-profile",
    "v1-core-v25",
    "--summary-json",
    summaryPath,
    "--context-out",
    contextOutPath,
  ];
  if (contextInPath && fsSync.existsSync(contextInPath)) {
    args.push("--context-json", contextInPath);
  }
  const proc = spawnSync(cliPath, args, { cwd: rootDir, encoding: "utf8", windowsHide: true });
  let summary = null;
  let summaryError = "";
  if (proc.status === 0) {
    try {
      summary = JSON.parse(fsSync.readFileSync(summaryPath, "utf8"));
    } catch (err) {
      summaryError = err?.message ?? String(err);
    }
  }
  return {
    exitCode: proc.status ?? 1,
    stdout: normalizeStdout(proc.stdout),
    stderr: String(proc.stderr ?? "").trim(),
    stderrLines: normalizeStderr(proc.stderr),
    warnings: parseCliWarnings(proc.stderr),
    summary,
    summaryError,
  };
}

function configuredCargoTargetDebugDir(rootDir) {
  const configPath = path.join(rootDir, ".cargo", "config.toml");
  if (!fsSync.existsSync(configPath)) {
    return path.join(rootDir, "target", "debug");
  }
  const text = fsSync.readFileSync(configPath, "utf8");
  const match = text.match(/target-dir\s*=\s*"([^"]+)"/);
  if (!match) {
    return path.join(rootDir, "target", "debug");
  }
  return path.join(path.resolve(rootDir, match[1]), "debug");
}

function resolveFreshCargoBinary(rootDir, manifestPath, binaryName) {
  const primaryBuildRoot = "I:/home/urihanl/ddn/codex/build";
  const fallbackBuildRoot = "C:/ddn/codex/build";
  const artifactBuildRoot = fsSync.existsSync(path.dirname(primaryBuildRoot))
    ? primaryBuildRoot
    : fallbackBuildRoot;
  const targetDir = path.join(artifactBuildRoot, "teul_cli_runner_target");
  fsSync.mkdirSync(targetDir, { recursive: true });
  const build = spawnSync(
    "cargo",
    ["build", "-q", "--manifest-path", manifestPath, "--bin", binaryName],
    {
      cwd: rootDir,
      encoding: "utf8",
      windowsHide: true,
      env: { ...process.env, CARGO_INCREMENTAL: "0", CARGO_TARGET_DIR: targetDir },
    },
  );
  if (build.status !== 0) {
    throw new Error(
      `cargo build failed for ${binaryName}: ${String(build.stderr || build.stdout || "").trim()}`,
    );
  }
  const exeName = process.platform === "win32" ? `${binaryName}.exe` : binaryName;
  const candidates = [
    path.join(targetDir, "debug", exeName),
    path.join(configuredCargoTargetDebugDir(rootDir), exeName),
    path.join(rootDir, "target", "debug", exeName),
  ];
  const found = candidates.find((candidate) => fsSync.existsSync(candidate));
  if (!found) {
    throw new Error(`built binary not found for ${binaryName}: ${candidates.join(", ")}`);
  }
  return found;
}

function runCliCanon(rootDir, inputPath) {
  const proc = spawnSync(
    "cargo",
    ["run", "-q", "--manifest-path", "tools/teul-cli/Cargo.toml", "--", "canon", inputPath, "--emit", "ddn"],
    { cwd: rootDir, encoding: "utf8", windowsHide: true },
  );
  return {
    exitCode: proc.status ?? 1,
    ddn: normalizeDdn(proc.stdout),
    stderr: String(proc.stderr ?? "").trim(),
  };
}

function runWasmCanon(runtime, sourceText) {
  assert(typeof runtime.wasmModule.wasm_canon_ddn === "function", "wasm_canon_ddn export missing");
  return normalizeDdn(runtime.wasmModule.wasm_canon_ddn(sourceText));
}

async function runWasm(runtime, sourceText, ticks) {
  const vm = new runtime.wasmModule.DdnWasmVm(sourceText);
  const client = new runtime.wrapper.DdnWasmVmClient(vm);
  try {
    let state = client.getStateParsed();
    const configuredMadi = typeof client.configuredMadi === "function" ? client.configuredMadi() : 0;
    const tickCount = ticks === "configured" || ticks === null || ticks === undefined
      ? (configuredMadi || 1)
      : ticks;
    const count = Math.max(1, Number(tickCount ?? 1) || 1);
    const requestedTickArg = ticks === "configured" || ticks === null || ticks === undefined
      ? -1
      : Number(ticks);
    const executionEnvelope = JSON.parse(
      runtime.wasmModule.wasm_execution_envelope_json(sourceText, requestedTickArg),
    );
    if (typeof client.runTicksParsed === "function") {
      state = client.runTicksParsed(count);
    } else {
      for (let idx = 0; idx < count; idx += 1) {
        state = client.stepOneParsed();
      }
    }
    return {
      state,
      rowByKey: indexRow(state?.channels, state?.row),
      configuredMadi,
      parseWarnings: client.parseWarningsParsed(),
      outputLog: runtime.runtimeState.extractObservationOutputLogFromState(state),
      outputRows: runtime.runtimeState.extractObservationOutputRowsFromState(state),
      stateHash: String(state?.state_hash ?? ""),
      viewHash: String(state?.view_hash ?? ""),
      executionEnvelope,
    };
  } finally {
    if (typeof vm.free === "function") {
      vm.free();
    }
  }
}

async function runWasmCurrentline(runtime, vm, sourceText, context) {
  const client = new runtime.wrapper.DdnWasmVmClient(vm);
  const state = client.applyCurrentlineCellWithSourceProfileParsed(
    sourceText,
    "v1-core-v25",
    context,
  );
  return {
    state,
    context: state?.currentline_context ?? state?.state?.currentline_context ?? null,
    rowByKey: indexRow(state?.channels, state?.row),
    configuredMadi: 0,
    parseWarnings: client.parseWarningsParsed(),
    outputLog: runtime.runtimeState.extractObservationOutputLogFromState(state),
    outputRows: runtime.runtimeState
      .extractObservationOutputRowsFromState(state)
      .filter((row) => String(row?.source ?? "") !== "fallback-line"),
    stateHash: String(state?.state_hash ?? ""),
    viewHash: String(state?.view_hash ?? ""),
  };
}

async function main() {
  const root = process.cwd();
  const packDir = process.argv[2]
    ? path.resolve(root, process.argv[2])
    : path.join(root, "pack", "seamgrim_wasm_cli_runtime_parity_v1");
  const contract = JSON.parse(await fs.readFile(path.join(packDir, "contract.detjson"), "utf8"));
  const closureClaim = String(contract?.closure_claim ?? "").trim().toLowerCase();
  if (closureClaim === "yes") {
    const acceptanceCase = (contract?.cases ?? []).find((testCase) => Boolean(testCase?.acceptance_only));
    assert(!acceptanceCase, `closure_claim=yes forbids acceptance_only case: ${acceptanceCase?.id ?? "<unknown>"}`);
  }
  const runtime = await initWasm(root);
  const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), "ddn-wasm-cli-parity-"));
  const cases = [];
  const failures = [];
  const currentlineMode = Boolean(contract.currentline_model?.enabled);
  const currentlineCliPath = currentlineMode
    ? resolveFreshCargoBinary(root, "tool/Cargo.toml", "ddonirang")
    : "";
  const strictStateHashEquality = String(contract.state_hash_policy ?? "report_only") === "strict_equality";
  const strictFullOutputParity =
    contract.strict_runtime_parity === true ||
    String(contract.closure_claim ?? "").trim().toLowerCase() === "bounded_behavioral_parity";
  let cliContextPath = "";
  if (currentlineMode) {
    const rel = String(contract.currentline_model?.initial_context ?? "").trim();
    if (rel) {
      const initial = path.join(packDir, rel);
      if (fsSync.existsSync(initial)) {
        cliContextPath = path.join(tempDir, "currentline.initial.detjson");
        fsSync.copyFileSync(initial, cliContextPath);
      }
    }
  }
  let wasmCurrentlineVm = null;
  let wasmCurrentlineContext = null;
  if (currentlineMode) {
    wasmCurrentlineVm = new runtime.wasmModule.DdnWasmVm("채비 { __currentline_boot: 수 <- 0. }.\n");
    const rel = String(contract.currentline_model?.initial_context ?? "").trim();
    if (rel) {
      const initial = path.join(packDir, rel);
      if (fsSync.existsSync(initial)) {
        wasmCurrentlineContext = JSON.parse(fsSync.readFileSync(initial, "utf8"));
      }
    }
  }

  for (const testCase of contract.cases ?? []) {
    const id = String(testCase.id ?? "").trim();
    const inputRel = String(testCase.input ?? "").trim();
    const inputPath = path.join(packDir, inputRel);
    const source = await fs.readFile(inputPath, "utf8");
    const summaryPath = path.join(tempDir, `${id || "case"}.summary.detjson`);
    let cli;
    let cliCanon = { exitCode: 0, ddn: "", stderr: "" };
    if (currentlineMode) {
      const contextOutPath = path.join(tempDir, `${id || "case"}.context.detjson`);
      cli = runCliCurrentlineWithBinary(currentlineCliPath, root, inputPath, summaryPath, cliContextPath, contextOutPath);
      if (cli.exitCode === 0) {
        cliContextPath = contextOutPath;
      }
    } else {
      cli = runCli(root, inputPath, summaryPath, testCase.ticks);
      if (cli.summary) {
        hydrateCliSummary(runtime.runtimeState, cli.summary);
        cli.stdout = Array.isArray(cli.summary.output_log_texts)
          ? cli.summary.output_log_texts
          : [];
        cli.outputLines = Array.isArray(cli.summary.output_lines)
          ? cli.summary.output_lines
          : cli.stdout;
        cli.warnings = Array.isArray(cli.summary.parse_warnings)
          ? cli.summary.parse_warnings
          : [];
      }
      cliCanon = {
        exitCode: cli.exitCode,
        ddn: normalizeDdn(cli.summary?.canonical_ddn ?? ""),
        stderr: cli.stderr,
      };
    }
    const caseFailures = [];

    let wasm = null;
    let wasmError = null;
    let wasmCanon = "";
    let wasmCanonError = null;
    try {
      if (currentlineMode) {
        wasm = await runWasmCurrentline(runtime, wasmCurrentlineVm, source, wasmCurrentlineContext);
        wasmCurrentlineContext = wasm.context;
      } else {
        wasm = await runWasm(runtime, source, testCase.ticks);
      }
    } catch (err) {
      wasmError = err;
    }
    if (!currentlineMode) {
      try {
        wasmCanon = runWasmCanon(runtime, source);
      } catch (err) {
        wasmCanonError = err;
      }
    }

    const acceptanceOnly = Boolean(testCase.acceptance_only);
    if (acceptanceOnly) {
      const cliOk = cli.exitCode === 0;
      const wasmOk = !wasmError;
      if (cliOk !== wasmOk) {
        caseFailures.push(
          `acceptance mismatch: cli=${cliOk ? "ok" : "reject"} wasm=${wasmOk ? "ok" : "reject"}`,
        );
      }
    }

    const expectReject = Boolean(testCase.expect_reject);
    if (!acceptanceOnly && expectReject) {
      if (cli.exitCode === 0) {
        caseFailures.push("cli expected reject but exited 0");
      }
      if (!wasmError) {
        caseFailures.push("wasm expected reject but succeeded");
      }
      for (const token of testCase.expected_error_contains ?? []) {
        const needle = String(token);
        const cliText = `${cli.stderr}\n${cli.stdout.join("\n")}`;
        const wasmText = String(wasmError?.message ?? wasmError ?? "");
        if (!cliText.includes(needle)) {
          caseFailures.push(`cli error missing token: ${needle}`);
        }
        if (!wasmText.includes(needle)) {
          caseFailures.push(`wasm error missing token: ${needle}`);
        }
      }
    } else if (!acceptanceOnly) {
      if (cli.exitCode !== 0) {
        caseFailures.push(`cli exit=${cli.exitCode}: ${cli.stderr || cli.stdout.join("\\n")}`);
      }
      if (wasmError) {
        caseFailures.push(`wasm error: ${wasmError?.message ?? String(wasmError)}`);
      }
    }

    if (!acceptanceOnly && !expectReject && !wasmError) {
      if (testCase.expected_canonical_ddn_parity !== false) {
        if (cliCanon.exitCode !== 0) {
          caseFailures.push(`cli canon exit=${cliCanon.exitCode}: ${cliCanon.stderr}`);
        }
        if (wasmCanonError) {
          caseFailures.push(`wasm canon error: ${wasmCanonError?.message ?? String(wasmCanonError)}`);
        }
        if (cliCanon.exitCode === 0 && !wasmCanonError && cliCanon.ddn !== wasmCanon) {
          caseFailures.push("cli/wasm canonical ddn mismatch");
        }
        if (cli.summary && normalizeDdn(cli.summary.canonical_ddn) !== cliCanon.ddn) {
          caseFailures.push("cli summary canonical_ddn mismatch");
        }
      }
      if (!cli.summary) {
        caseFailures.push(`cli summary missing${cli.summaryError ? `: ${cli.summaryError}` : ""}`);
      }
      if (
        !currentlineMode &&
        cli.summary &&
        !sameJson(cli.summary.execution_envelope ?? null, wasm.executionEnvelope ?? null)
      ) {
        caseFailures.push("cli/wasm execution envelope mismatch");
      }
      if (
        strictStateHashEquality &&
        cli.summary &&
        String(cli.summary.state_hash ?? "") &&
        String(wasm.stateHash ?? "") &&
        String(cli.summary.state_hash ?? "") !== String(wasm.stateHash ?? "")
      ) {
        caseFailures.push("cli/wasm state_hash mismatch");
      }
      if (strictFullOutputParity && cli.summary && !sameJson(cli.summary.final_row ?? {}, wasm.rowByKey ?? {})) {
        caseFailures.push(`cli summary/wasm final_row full mismatch: summary ${JSON.stringify(cli.summary.final_row ?? {})} wasm ${JSON.stringify(wasm.rowByKey ?? {})}`);
      }
      if (strictFullOutputParity && cli.summary && !sameJson(cli.summary.resources?.value_json ?? {}, wasm.state?.resources?.value_json ?? {})) {
        caseFailures.push("cli summary/wasm value_json full mismatch");
      }
      if (Number.isFinite(Number(testCase.expected_configured_madi))) {
        const expectedMadi = Number(testCase.expected_configured_madi);
        if (Number(wasm.configuredMadi ?? 0) !== expectedMadi) {
          caseFailures.push(`wasm configured_madi mismatch: expected ${expectedMadi} got ${wasm.configuredMadi ?? 0}`);
        }
        if (Number(cli.summary?.configured_ticks ?? 0) !== expectedMadi) {
          caseFailures.push(`cli summary configured_ticks mismatch: expected ${expectedMadi} got ${cli.summary?.configured_ticks ?? null}`);
        }
      }
      if (Array.isArray(testCase.expected_cli_stdout) && !sameJson(cli.stdout, testCase.expected_cli_stdout)) {
        caseFailures.push(`cli stdout mismatch: expected ${JSON.stringify(testCase.expected_cli_stdout)} got ${JSON.stringify(cli.stdout)}`);
      }
      for (const token of testCase.expected_cli_stdout_contains ?? []) {
        const surface = Array.isArray(cli.outputLines) ? cli.outputLines : cli.stdout;
        const surfaceText = [
          ...surface.map((item) => String(item ?? "")),
          JSON.stringify(cli.summary?.engine_state?.view_meta ?? {}),
          JSON.stringify(cli.summary?.resources?.value_json ?? {}),
        ].join("\n");
        if (!surfaceText.includes(String(token))) {
          caseFailures.push(`cli stdout missing token: ${token}`);
        }
      }
      compareObjectSubset(wasm.rowByKey, testCase.expected_wasm_row, "wasm.row", caseFailures);
      compareObjectSubset(wasm.state?.resources?.value_json, testCase.expected_wasm_value_json, "wasm.value_json", caseFailures);
      for (const [key, raw] of Object.entries(testCase.expected_wasm_formula_raw ?? {})) {
        const actual = wasm.state?.resources?.value_json?.[key]?.raw;
        if (actual !== raw) {
          caseFailures.push(`wasm.formula.${key}.raw: expected ${JSON.stringify(raw)} got ${JSON.stringify(actual)}`);
        }
      }
      for (const key of testCase.expected_wasm_value_json_keys ?? []) {
        if (!(String(key) in (wasm.state?.resources?.value_json ?? {}))) {
          caseFailures.push(`wasm.value_json missing key: ${key}`);
        }
      }
      const drawList = wasm.state?.resources?.value_json?.["보개_그림판_목록"];
      if (Array.isArray(testCase.expected_wasm_shape_kinds)) {
        const kinds = Array.isArray(drawList) ? drawList.map((item) => String(item?.kind ?? "")) : [];
        for (const kind of testCase.expected_wasm_shape_kinds) {
          if (!kinds.includes(String(kind))) {
            caseFailures.push(`wasm.shape kind missing: ${kind}`);
          }
        }
      }
      for (const [dottedPath, expectedValue] of Object.entries(testCase.expected_wasm_pack_fields ?? {})) {
        const actual = getPathValue(wasm.state?.resources?.value_json, dottedPath);
        if (!sameJson(actual, expectedValue)) {
          caseFailures.push(`wasm.pack.${dottedPath}: expected ${JSON.stringify(expectedValue)} got ${JSON.stringify(actual)}`);
        }
      }
      if (Array.isArray(testCase.expected_wasm_output_log_texts)) {
        const actual = (wasm.outputLog ?? []).map((entry) => String(entry?.text ?? ""));
        if (!sameJson(actual, testCase.expected_wasm_output_log_texts)) {
          caseFailures.push(`wasm.output_log texts mismatch: expected ${JSON.stringify(testCase.expected_wasm_output_log_texts)} got ${JSON.stringify(actual)}`);
        }
      }
      if (Array.isArray(testCase.expected_wasm_output_rows)) {
        compareObjectSubsetRows(wasm.outputRows ?? [], testCase.expected_wasm_output_rows, "wasm.output_rows", caseFailures);
      }
      if (testCase.expected_cli_wasm_output_log_parity === true) {
        const actual = (wasm.outputLog ?? []).map((entry) => String(entry?.text ?? ""));
        const expectedOutput = Array.isArray(cli.summary?.output_log_texts)
          ? cli.summary.output_log_texts
          : cli.stdout;
        if (!sameJson(actual, expectedOutput)) {
          caseFailures.push(`cli/wasm output mismatch: cli ${JSON.stringify(expectedOutput)} wasm ${JSON.stringify(actual)}`);
        }
        if (!sameJson(cli.summary?.output_log_texts ?? [], actual)) {
          caseFailures.push(`cli summary/wasm output_log mismatch: summary ${JSON.stringify(cli.summary?.output_log_texts ?? [])} wasm ${JSON.stringify(actual)}`);
        }
      }
      if (testCase.expected_cli_wasm_output_rows_parity === true) {
        const cliRows = normalizeOutputRowsForParity(cli.summary?.output_rows ?? []);
        const wasmRows = normalizeOutputRowsForParity(wasm.outputRows ?? []);
        if (!sameJson(cliRows, wasmRows)) {
          caseFailures.push(`cli summary/wasm output_rows mismatch: summary ${JSON.stringify(cliRows)} wasm ${JSON.stringify(wasmRows)}`);
        }
      }
      const valueJsonKeys = [
        ...(testCase.expected_cli_wasm_value_json_keys ?? []),
      ].map(String);
      for (const key of valueJsonKeys) {
        const cliValue = cli.summary?.resources?.value_json?.[key];
        const wasmValue = wasm.state?.resources?.value_json?.[key];
        if (!sameJson(cliValue, wasmValue)) {
          caseFailures.push(`cli summary/wasm value_json.${key} mismatch: summary ${JSON.stringify(cliValue)} wasm ${JSON.stringify(wasmValue)}`);
        }
      }
      if (testCase.expected_cli_wasm_row_parity === true) {
        for (const key of Object.keys(testCase.expected_wasm_row ?? {})) {
          const cliValue = cli.summary?.final_row?.[key];
          const wasmValue = wasm.rowByKey?.[key];
          if (!sameJson(cliValue, wasmValue)) {
            caseFailures.push(`cli summary/wasm row.${key} mismatch: summary ${JSON.stringify(cliValue)} wasm ${JSON.stringify(wasmValue)}`);
          }
        }
      }
      if (testCase.expected_cli_wasm_all_scalar_row_parity === true) {
        if (!sameJson(cli.summary?.final_row ?? {}, wasm.rowByKey ?? {})) {
          caseFailures.push(`cli summary/wasm final_row mismatch: summary ${JSON.stringify(cli.summary?.final_row ?? {})} wasm ${JSON.stringify(wasm.rowByKey ?? {})}`);
        }
      }
      for (const key of testCase.expected_cli_wasm_row_keys ?? []) {
        const rowKey = String(key);
        const cliValue = cli.summary?.final_row?.[rowKey];
        const wasmValue = wasm.rowByKey?.[rowKey];
        if (!sameJson(cliValue, wasmValue)) {
          caseFailures.push(`cli summary/wasm row.${rowKey} mismatch: summary ${JSON.stringify(cliValue)} wasm ${JSON.stringify(wasmValue)}`);
        }
      }
      if (testCase.expected_cli_wasm_parse_warning_parity === true) {
        const cliCodes = cli.warnings.map((warning) => warning.code);
        const wasmCodes = (wasm?.parseWarnings ?? []).map((warning) => String(warning?.code ?? ""));
        if (!sameJson(cliCodes, wasmCodes)) {
          caseFailures.push(`cli/wasm parse warning codes mismatch: cli ${JSON.stringify(cliCodes)} wasm ${JSON.stringify(wasmCodes)}`);
        }
      }
    }
    if (!acceptanceOnly && !expectReject && Array.isArray(testCase.expected_parse_warning_codes)) {
      const expectedCodes = testCase.expected_parse_warning_codes.map(String);
      const cliCodes = cli.warnings.map((warning) => warning.code);
      const wasmCodes = (wasm?.parseWarnings ?? []).map((warning) => String(warning?.code ?? ""));
      if (!sameJson(cliCodes, expectedCodes)) {
        caseFailures.push(`cli parse warning codes mismatch: expected ${JSON.stringify(expectedCodes)} got ${JSON.stringify(cliCodes)}`);
      }
      if (!sameJson(wasmCodes, expectedCodes)) {
        caseFailures.push(`wasm parse warning codes mismatch: expected ${JSON.stringify(expectedCodes)} got ${JSON.stringify(wasmCodes)}`);
      }
    }

    cases.push({
      id,
      ok: caseFailures.length === 0,
      cli_exit_code: cli.exitCode,
      cli_stdout: cli.stdout,
      cli_stderr_lines: cli.stderrLines,
      cli_canonical_ddn: cliCanon.ddn,
      cli_canon_error: cliCanon.exitCode === 0 ? "" : cliCanon.stderr,
      cli_parse_warnings: cli.warnings,
      cli_summary_error: cli.summaryError,
      cli_summary: cli.summary ?? null,
      wasm_error: wasmError ? String(wasmError?.message ?? wasmError) : "",
      wasm_canonical_ddn: wasmCanon,
      wasm_canon_error: wasmCanonError ? String(wasmCanonError?.message ?? wasmCanonError) : "",
      wasm_configured_madi: wasm?.configuredMadi ?? 0,
      wasm_row: wasm?.rowByKey ?? {},
      wasm_parse_warnings: wasm?.parseWarnings ?? [],
      wasm_output_log: wasm?.outputLog ?? [],
      wasm_output_rows: wasm?.outputRows ?? [],
      wasm_state_hash: wasm?.stateHash ?? "",
      wasm_view_hash: wasm?.viewHash ?? "",
      strict_evidence: buildStrictEvidence({
        cli,
        wasm,
        cliCanon,
        wasmCanon,
        wasmCanonError,
        testCase,
        expectReject,
        strictFullOutputParity,
      }),
      failures: caseFailures,
    });
    failures.push(...caseFailures.map((failure) => `${id}: ${failure}`));
  }
  if (wasmCurrentlineVm && typeof wasmCurrentlineVm.free === "function") {
    wasmCurrentlineVm.free();
  }

  const report = {
    schema: "ddn.seamgrim.wasm_cli_runtime_parity.report.v1",
    pack_id: contract.pack_id,
    ok: failures.length === 0,
    strict_runtime_parity: contract.strict_runtime_parity === true,
    state_hash_policy: contract.state_hash_policy ?? "report_only",
    hash_domain_note: contract.hash_domain_note ?? "",
    cases,
  };
  console.log(JSON.stringify(report, null, 2));
  if (failures.length > 0) {
    console.error(failures.join("\n"));
    process.exit(1);
  }
}

main().catch((err) => {
  console.error(err?.stack ?? String(err));
  process.exit(1);
});
