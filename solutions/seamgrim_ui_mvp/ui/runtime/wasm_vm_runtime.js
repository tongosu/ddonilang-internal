import {
  createWasmLoader,
  stripMetaHeader,
} from "../wasm_page_common.js";
import { preprocessDdnText } from "./ddn_preprocess.js";
import {
  inspectNativeObservationManifest,
} from "./observation_manifest_contract.js";

const INERT_SUPPORTED_PROFILE_BOOTSTRAP_SOURCE = "1 보여주기.";

function normalizeStatusLines(lines) {
  if (Array.isArray(lines)) return lines;
  if (typeof lines === "string") return [lines];
  return [];
}

function normalizeWasmModulePath(wasmUrl) {
  if (typeof wasmUrl !== "string" || !wasmUrl.trim()) {
    return "../wasm/ddonirang_tool.js";
  }
  if (wasmUrl.endsWith(".js")) return wasmUrl;
  return "../wasm/ddonirang_tool.js";
}

function buildParseWarningsReadDiag(code, message, detail = "") {
  return [
    {
      code,
      message,
      detail: String(detail ?? ""),
      span: { start: 0, end: 0 },
    },
  ];
}

function normalizeParseWarningRow(raw) {
  const row = raw && typeof raw === "object" ? raw : {};
  const spanRaw = row.span && typeof row.span === "object" ? row.span : {};
  const startNum = Number(spanRaw.start);
  const endNum = Number(spanRaw.end);
  return {
    code: String(row.code ?? "W_WASM_PARSE_WARNING_UNKNOWN"),
    message: String(row.message ?? ""),
    detail: String(row.detail ?? ""),
    span: {
      start: Number.isFinite(startNum) ? startNum : 0,
      end: Number.isFinite(endNum) ? endNum : 0,
    },
  };
}

function buildRuntimeDiag(code, message, detail = "") {
  return {
    code,
    message,
    detail: String(detail ?? ""),
  };
}

function requireNativeObservationManifest(payload, operation) {
  const inspected = inspectNativeObservationManifest(payload, operation);
  if (inspected.status !== "available") {
    const diagnostic = inspected.diagnostic;
    const error = new Error(`${diagnostic.code}: ${diagnostic.message}`);
    error.name = "ObservationManifestContractError";
    error.code = diagnostic.code;
    error.phase = diagnostic.phase;
    error.outcome = diagnostic.outcome;
    error.detail = diagnostic.detail;
    throw error;
  }
  return inspected.manifest;
}

function requireTypedFrameInput(input) {
  if (!input || typeof input !== "object" || Array.isArray(input)) {
    throw new Error("typed frame input is required");
  }
  const hasOwn = (key) => Object.prototype.hasOwnProperty.call(input, key);
  if (
    !hasOwn("keys") ||
    !hasOwn("lastKey") ||
    !hasOwn("px") ||
    !hasOwn("py") ||
    !hasOwn("dt") ||
    !Number.isInteger(input.keys) ||
    input.keys < 0 ||
    typeof input.lastKey !== "string" ||
    !Number.isFinite(input.px) ||
    !Number.isFinite(input.py) ||
    !Number.isFinite(input.dt) ||
    input.dt < 0
  ) {
    throw new Error("typed frame input is invalid");
  }
  return input;
}

export class WasmVmHandle {
  constructor({
    loader,
    defaultSourceText = "",
    seedU64 = undefined,
    sourceProfileIdentity = "",
  } = {}) {
    this.loader = loader;
    this.defaultSourceText = String(defaultSourceText ?? "");
    this.seedU64 = Number.isFinite(Number(seedU64)) ? Number(seedU64) : null;
    this.sourceProfileIdentity = String(sourceProfileIdentity ?? "");
    this.client = null;
    this.lastSourceText = "";
    this.lastBodyText = "";
    this.lastPragmas = [];
    this.lastDiags = [];
    this.lastObservationManifest = null;
    this.lastExecutionModeDecision = null;
    this.lastConfiguredMadi = 0;
    this.lastParseWarnings = [];
    this.lastRuntimeDiags = [];
  }

  addRuntimeDiag(code, message, detail = "") {
    this.lastRuntimeDiags = [
      ...this.lastRuntimeDiags,
      buildRuntimeDiag(code, message, detail),
    ];
  }

  addOperationFailureDiag(error, fallbackCode, fallbackMessage) {
    this.addRuntimeDiag(
      String(error?.code ?? fallbackCode),
      String(error?.message ?? fallbackMessage),
      String(error?.detail ?? ""),
    );
  }

  async ensureClientForOp(sourceText, code, message) {
    try {
      return await this.ensureClient(sourceText);
    } catch (err) {
      this.addRuntimeDiag(code, message, err?.message ?? String(err ?? ""));
      throw err;
    }
  }

  preprocess(sourceText) {
    const source = String(sourceText ?? this.lastSourceText ?? this.defaultSourceText);
    const pre = preprocessDdnText(source);
    const bodyText = stripMetaHeader(pre.bodyText ?? "");
    this.lastSourceText = source;
    this.lastBodyText = bodyText;
    this.lastPragmas = Array.isArray(pre.pragmas) ? pre.pragmas : [];
    this.lastDiags = Array.isArray(pre.diags) ? pre.diags : [];
    return {
      bodyText: this.lastBodyText,
      pragmas: this.lastPragmas,
      diags: this.lastDiags,
    };
  }

  async ensureClient(sourceText) {
    const pre = this.preprocess(sourceText);
    // A supported-profile VM must be constructed from the loader's inert
    // fallback, then explicitly populated through the same Rust V25 path as
    // the native frontdoor. Passing V25 text to the legacy constructor would
    // create a private parser boundary before the profile-aware update.
    const client = await this.loader.ensure(
      this.sourceProfileIdentity ? INERT_SUPPORTED_PROFILE_BOOTSTRAP_SOURCE : pre.bodyText,
    );
    this.client = client;
    this.lastRuntimeDiags = [];
    if (this.seedU64 !== null) {
      if (typeof client?.setRngSeed === "function") {
        try {
          client.setRngSeed(this.seedU64);
        } catch (err) {
          this.addRuntimeDiag(
            "E_WASM_SET_RNG_SEED_FAILED",
            "setRngSeed 호출에 실패했습니다.",
            err?.message ?? String(err ?? ""),
          );
        }
      } else {
        this.addRuntimeDiag(
          "E_WASM_SET_RNG_SEED_API_MISSING",
          "setRngSeed API가 없어 시드를 적용할 수 없습니다.",
        );
      }
      this.seedU64 = null;
    }
    this.lastParseWarnings = this.readParseWarnings(client);
    this.refreshExecutionContractForSource(client, this.lastSourceText);
    return client;
  }

  readExecutionModeDecision(client = this.client) {
    if (!client || typeof client.executionModeDecisionParsed !== "function") {
      return null;
    }
    const decision = client.executionModeDecisionParsed();
    return decision && typeof decision === "object" ? decision : null;
  }

  readExecutionContractForSource(client = this.client, sourceText = this.lastSourceText) {
    const executionEnvelope = client?.wasmModule?.wasm_execution_envelope_json;
    const fallbackConfiguredMadi = typeof client?.configuredMadi === "function"
      ? Number(client.configuredMadi())
      : 0;
    if (typeof executionEnvelope !== "function") {
      return {
        decision: this.readExecutionModeDecision(client),
        configuredMadi: Number.isFinite(fallbackConfiguredMadi) ? Math.max(0, Math.floor(fallbackConfiguredMadi)) : 0,
      };
    }
    try {
      const parsed = JSON.parse(executionEnvelope(String(sourceText ?? ""), 1));
      const decision = parsed?.execution_mode_decision;
      const configuredMadi = Number(parsed?.configured_madi ?? 0);
      return {
        decision: decision && typeof decision === "object"
          ? decision
          : this.readExecutionModeDecision(client),
        configuredMadi: Number.isFinite(configuredMadi) ? Math.max(0, Math.floor(configuredMadi)) : 0,
      };
    } catch (_) {
      return {
        decision: this.readExecutionModeDecision(client),
        configuredMadi: Number.isFinite(fallbackConfiguredMadi) ? Math.max(0, Math.floor(fallbackConfiguredMadi)) : 0,
      };
    }
  }

  refreshExecutionContractForSource(client = this.client, sourceText = this.lastSourceText) {
    const contract = this.readExecutionContractForSource(client, sourceText);
    this.lastExecutionModeDecision = contract.decision;
    this.lastConfiguredMadi = contract.configuredMadi;
    return contract;
  }

  readParseWarnings(client) {
    if (!client || typeof client !== "object") {
      return buildParseWarningsReadDiag(
        "E_WASM_PARSE_WARNINGS_CLIENT_MISSING",
        "parse warnings를 읽을 client가 없습니다.",
      );
    }
    if (typeof client.parseWarningsParsed !== "function") {
      return buildParseWarningsReadDiag(
        "E_WASM_PARSE_WARNINGS_API_MISSING",
        "parseWarningsParsed API가 없습니다.",
      );
    }
    try {
      const warnings = client.parseWarningsParsed();
      if (!Array.isArray(warnings)) {
        return buildParseWarningsReadDiag(
          "E_WASM_PARSE_WARNINGS_PAYLOAD_INVALID",
          "parseWarningsParsed 결과가 배열이 아닙니다.",
          typeof warnings,
        );
      }
      return warnings.map(normalizeParseWarningRow);
    } catch (err) {
      return buildParseWarningsReadDiag(
        "E_WASM_PARSE_WARNINGS_READ_FAILED",
        "parseWarningsParsed 호출에 실패했습니다.",
        err?.message ?? String(err ?? ""),
      );
    }
  }

  consumeNativeObservationManifest(payload, operation) {
    const manifest = requireNativeObservationManifest(payload, operation);
    this.lastObservationManifest = manifest;
    return payload;
  }

  captureNativeObservationManifest(payload, operation) {
    const inspected = inspectNativeObservationManifest(payload, operation);
    this.lastObservationManifest = inspected.status === "available" ? inspected.manifest : null;
    return payload;
  }

  async updateLogic(ddnSourceText) {
    const client = await this.ensureClientForOp(
      ddnSourceText,
      "E_WASM_UPDATE_ENSURE_FAILED",
      "updateLogic 진입을 위한 wasm client 준비에 실패했습니다.",
    );
    try {
      if (this.sourceProfileIdentity) {
        if (typeof client.updateLogicWithSourceProfile !== "function") {
          throw new Error("E_WASM_SOURCE_PROFILE_API_MISSING");
        }
        client.updateLogicWithSourceProfile(this.lastSourceText, this.sourceProfileIdentity);
      } else {
        client.updateLogic(this.lastBodyText);
      }
    } catch (err) {
      this.addRuntimeDiag(
        "E_WASM_UPDATELOGIC_FAILED",
        "updateLogic 호출에 실패했습니다.",
        err?.message ?? String(err ?? ""),
      );
      throw err;
    }
    this.lastParseWarnings = this.readParseWarnings(client);
    this.refreshExecutionContractForSource(client, this.lastSourceText);
    try {
      // A source update commits typed source/profile state before any frame
      // exists. Observation manifests belong to executed frame projection, so
      // requiring one here incorrectly blocks a valid V25 single-file Run.
      this.lastObservationManifest = null;
      return client.getStateParsed();
    } catch (err) {
      this.addOperationFailureDiag(
        err,
        "E_WASM_GETSTATE_AFTER_UPDATE_FAILED",
        "updateLogic 이후 상태 조회에 실패했습니다.",
      );
      throw err;
    }
  }

  async reset({ keepParams = false } = {}) {
    const client =
      this.client ??
      (await this.ensureClientForOp(
        this.defaultSourceText,
        "E_WASM_RESET_ENSURE_FAILED",
        "reset 진입을 위한 wasm client 준비에 실패했습니다.",
    ));
    try {
      // Reset likewise establishes a pre-execution state; the first executed
      // frame remains the fail-closed observation-manifest boundary.
      this.lastObservationManifest = null;
      return client.resetParsed(Boolean(keepParams));
    } catch (err) {
      this.addOperationFailureDiag(
        err,
        "E_WASM_RESET_FAILED",
        "resetParsed 호출에 실패했습니다.",
      );
      throw err;
    }
  }

  async step({ n = null, input = null, sourceText = null } = {}) {
    const client = await this.ensureClientForOp(
      sourceText ?? this.lastSourceText ?? this.defaultSourceText,
      "E_WASM_STEP_ENSURE_FAILED",
      "step 진입을 위한 wasm client 준비에 실패했습니다.",
    );
    const configuredMadi =
      n === null || n === undefined
        ? (typeof client.configuredMadi === "function" ? client.configuredMadi() : 0)
        : 0;
    const countRaw = Number(configuredMadi > 0 ? configuredMadi : n);
    const count = Number.isFinite(countRaw) && countRaw > 0 ? Math.floor(countRaw) : 1;
    let state = null;
    const hasFrameInput = input !== null && input !== undefined;
    try {
      if (!hasFrameInput && typeof client.runTicksParsed === "function") {
        state = client.runTicksParsed(count);
      } else {
        const frameInput = hasFrameInput ? requireTypedFrameInput(input) : null;
        if (frameInput && typeof client.stepOneWithInputParsed !== "function") {
          throw new Error("typed frame input API is unavailable");
        }
        for (let i = 0; i < count; i += 1) {
          if (frameInput) {
            state = client.stepOneWithInputParsed(
              frameInput.keys,
              frameInput.lastKey,
              frameInput.px,
              frameInput.py,
              frameInput.dt,
          );
          } else {
            state = client.stepOneParsed();
          }
        }
      }
    } catch (err) {
      this.addRuntimeDiag(
        "E_WASM_STEP_FAILED",
        "stepOne 호출에 실패했습니다.",
        String(err?.message ?? err ?? ""),
      );
      throw err;
    }
    try {
      // A valid non-visual V25 single-file run has no observation manifest.
      // Preserve its typed state/result rather than manufacturing a visual
      // projection failure; observed programs still retain their manifest.
      return this.captureNativeObservationManifest(state, "step");
    } catch (err) {
      this.addOperationFailureDiag(
        err,
        "E_WASM_STEP_STATE_ATTACH_FAILED",
        "step 결과 상태 부착에 실패했습니다.",
      );
      throw err;
    }
  }

  async columns() {
    const client =
      this.client ??
      (await this.ensureClientForOp(
        this.defaultSourceText,
        "E_WASM_COLUMNS_ENSURE_FAILED",
        "columns 진입을 위한 wasm client 준비에 실패했습니다.",
      ));
    let payload;
    try {
      payload = client.columnsParsed();
    } catch (err) {
      this.addRuntimeDiag(
        "E_WASM_COLUMNS_FAILED",
        "columnsParsed 호출에 실패했습니다.",
        err?.message ?? String(err ?? ""),
      );
      throw err;
    }
    try {
      return this.consumeNativeObservationManifest(payload, "columns");
    } catch (err) {
      this.addOperationFailureDiag(
        err,
        "E_WASM_COLUMNS_ATTACH_FAILED",
        "columns 결과 상태 부착에 실패했습니다.",
      );
      throw err;
    }
  }

  async setParam({ key, value } = {}) {
    const client =
      this.client ??
      (await this.ensureClientForOp(
        this.defaultSourceText,
        "E_WASM_SET_PARAM_ENSURE_FAILED",
        "setParam 진입을 위한 wasm client 준비에 실패했습니다.",
      ));
    try {
      return client.setParamParsed(String(key ?? ""), value);
    } catch (err) {
      this.addRuntimeDiag(
        "E_WASM_SET_PARAM_FAILED",
        "setParamParsed 호출에 실패했습니다.",
        err?.message ?? String(err ?? ""),
      );
      throw err;
    }
  }

  async getStateHash() {
    const client =
      this.client ??
      (await this.ensureClientForOp(
        this.defaultSourceText,
        "E_WASM_STATE_HASH_ENSURE_FAILED",
        "getStateHash 진입을 위한 wasm client 준비에 실패했습니다.",
      ));
    try {
      return client.getStateHash();
    } catch (err) {
      this.addRuntimeDiag(
        "E_WASM_STATE_HASH_FAILED",
        "getStateHash 호출에 실패했습니다.",
        err?.message ?? String(err ?? ""),
      );
      throw err;
    }
  }

  async getStateJson() {
    const client =
      this.client ??
      (await this.ensureClientForOp(
        this.defaultSourceText,
        "E_WASM_GET_STATE_JSON_ENSURE_FAILED",
        "getStateJson 진입을 위한 wasm client 준비에 실패했습니다.",
      ));
    try {
      return this.captureNativeObservationManifest(client.getStateParsed(), "get_state");
    } catch (err) {
      this.addOperationFailureDiag(
        err,
        "E_WASM_GET_STATE_JSON_FAILED",
        "getStateParsed 호출에 실패했습니다.",
      );
      throw err;
    }
  }

  getParseWarnings() {
    return Array.isArray(this.lastParseWarnings) ? [...this.lastParseWarnings] : [];
  }

  getExecutionModeDecision() {
    return this.lastExecutionModeDecision && typeof this.lastExecutionModeDecision === "object"
      ? { ...this.lastExecutionModeDecision }
      : null;
  }

  getConfiguredMadi() {
    const value = Number(this.lastConfiguredMadi ?? 0);
    return Number.isFinite(value) && value > 0 ? Math.floor(value) : 0;
  }

  getDebugInfo() {
    return {
      buildInfo: this.loader.getLastBuildInfo?.() ?? "",
      buildInfoDiag: this.loader.getLastBuildInfoDiag?.() ?? null,
      initDiag: this.loader.getLastInitDiag?.() ?? null,
      artifactManifest: this.loader.getLastArtifactManifest?.() ?? null,
      artifactFingerprint: this.loader.getLastArtifactFingerprint?.() ?? "",
      artifactDiag: this.loader.getLastArtifactDiag?.() ?? null,
      preprocessed: this.loader.getLastPreprocessed?.() ?? this.lastBodyText ?? "",
      preprocessDiag: this.loader.getLastPreprocessDiag?.() ?? null,
      pragmas: this.lastPragmas,
      diags: this.lastDiags,
      parseWarnings: this.getParseWarnings(),
      runtimeDiags: Array.isArray(this.lastRuntimeDiags) ? [...this.lastRuntimeDiags] : [],
      observationManifest: this.lastObservationManifest,
      executionModeDecision: this.getExecutionModeDecision(),
      configuredMadi: this.getConfiguredMadi(),
      cacheBust: this.loader.getCacheBust?.() ?? null,
    };
  }

  invalidate() {
    this.client = null;
    this.lastSourceText = "";
    this.lastBodyText = "";
    this.lastPragmas = [];
    this.lastDiags = [];
    this.lastObservationManifest = null;
    this.lastExecutionModeDecision = null;
    this.lastConfiguredMadi = 0;
    this.lastParseWarnings = [];
    this.lastRuntimeDiags = [];
    this.loader.reset();
  }
}

export async function createWasmVm({
  wasmUrl = "./wasm/ddonirang_tool.js",
  ddnSourceText = "",
  seedU64 = undefined,
  sourceProfileIdentity = "",
  cacheBust = Date.now(),
  setStatus = null,
  clearStatusError = null,
  missingExportMessage = "DdnWasmVm export missing",
  formatReadyStatus = null,
  formatFallbackStatus = null,
} = {}) {
  const modulePath = normalizeWasmModulePath(wasmUrl);
  const loader = createWasmLoader({
    cacheBust,
    modulePath,
    wrapperPath: "./wasm_ddn_wrapper.js",
    setStatus: (lines) => {
      if (typeof setStatus === "function") {
        setStatus(normalizeStatusLines(lines));
      }
    },
    clearStatusError: typeof clearStatusError === "function" ? clearStatusError : undefined,
    missingExportMessage,
    formatReadyStatus,
    formatFallbackStatus,
  });
  const handle = new WasmVmHandle({
    loader,
    defaultSourceText: ddnSourceText,
    seedU64,
    sourceProfileIdentity,
  });
  if (String(ddnSourceText ?? "").trim()) {
    await handle.ensureClient(ddnSourceText);
  }
  return handle;
}
