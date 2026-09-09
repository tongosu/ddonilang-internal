import { createWasmVm } from "./wasm_vm_runtime.js";

export const RUNTIME_BRIDGE_V1_SCHEMA = "seamgrim.runtime_bridge.v1";

export const RUNTIME_BRIDGE_V1_OPERATIONS = Object.freeze([
  "createSession",
  "sourceAnalysis",
  "runSummaryWithSourceProfile",
  "canonMaegimPlan",
  "planGajiExtraction",
  "projectSourceSha256",
  "buildLocalGajiArtifact",
  "planGajiLifecycle",
  "projectGraph",
  "projectSymbols",
  "prepareProjectLink",
  "planProjectEdit",
  "projectGajiLock",
  "publishLocalGotgan",
  "searchLocalGotgan",
]);

function requireExport(wasmModule, name, message = `${name} export 누락`) {
  const operation = wasmModule?.[name];
  if (typeof operation !== "function") throw new Error(message);
  return operation.bind(wasmModule);
}

class RuntimeSessionV1 {
  #adapterSession;

  constructor(adapterSession) {
    this.#adapterSession = adapterSession;
  }

  updateLogic(sourceText) {
    return this.#adapterSession.updateLogic(sourceText);
  }

  getExecutionModeDecision() {
    return this.#adapterSession.getExecutionModeDecision();
  }

  getConfiguredMadi() {
    return this.#adapterSession.getConfiguredMadi();
  }

  reset(options) {
    return this.#adapterSession.reset(options);
  }

  getStateJson() {
    return this.#adapterSession.getStateJson();
  }

  step(options) {
    return this.#adapterSession.step(options);
  }

  setParam(options) {
    return this.#adapterSession.setParam(options);
  }
}

export class WasmRuntimeAdapter {
  constructor({ createWasmVmImpl = createWasmVm } = {}) {
    if (typeof createWasmVmImpl !== "function") {
      throw new TypeError("createWasmVmImpl must be a function");
    }
    this.createWasmVmImpl = createWasmVmImpl;
    this.projectModulePromise = null;
  }

  async createSession(options) {
    return this.createWasmVmImpl(options);
  }

  async ensureProjectModule() {
    if (!this.projectModulePromise) {
      this.projectModulePromise = this.createWasmVmImpl({
        ddnSourceText: "1 보여주기.",
        cacheBust: "approved-workbench-project-frontdoor-v1",
        setStatus: () => {},
        clearStatusError: () => {},
      }).then(async (handle) => {
        const client = handle.client ?? await handle.ensureClient("1 보여주기.");
        const wasmModule = client?.wasmModule;
        requireExport(wasmModule, "wasm_project_prepare_link_json");
        if (
          typeof wasmModule.wasm_project_edit_plan_json !== "function"
          || typeof wasmModule.wasm_project_source_sha256_json !== "function"
        ) {
          throw new Error("project edit-plan WASM export 누락");
        }
        return wasmModule;
      });
    }
    return this.projectModulePromise;
  }

  async canonMaegimPlan(sourceText) {
    const wasmModule = await this.ensureProjectModule();
    const operation = requireExport(wasmModule, "wasm_canon_maegim_plan");
    return JSON.parse(String(operation(sourceText) ?? "{}"));
  }

  async sourceAnalysis(request) {
    const wasmModule = await this.ensureProjectModule();
    const operation = requireExport(
      wasmModule,
      "wasm_source_analysis_snapshot_json",
      "E_SOURCE_ANALYSIS_WASM_REQUIRED 공통 Rust/WASM 원문 분석 기능이 필요합니다",
    );
    return JSON.parse(String(operation(JSON.stringify(request)) ?? "{}"));
  }

  async runSummaryWithSourceProfile({
    sourceText,
    sourcePath,
    requestedTicks,
    sourceProfileIdentity,
  }) {
    const wasmModule = await this.ensureProjectModule();
    const operation = requireExport(
      wasmModule,
      "wasm_run_summary_with_source_profile_json",
      "E_WASM_RUN_SUMMARY_REQUIRED 공통 Rust/WASM 실행 결과와 영수증 기능이 필요합니다",
    );
    return JSON.parse(String(operation(
      String(sourceText ?? ""),
      String(sourcePath ?? "lesson.ddn"),
      Number(requestedTicks ?? 1),
      String(sourceProfileIdentity ?? ""),
    ) ?? "{}"));
  }

  async planGajiExtraction(request) {
    const wasmModule = await this.ensureProjectModule();
    return JSON.parse(requireExport(wasmModule, "wasm_gaji_extraction_plan_json")(JSON.stringify(request)));
  }

  async projectSourceSha256(source) {
    const wasmModule = await this.ensureProjectModule();
    return String(requireExport(wasmModule, "wasm_project_source_sha256_json")(JSON.stringify(source)));
  }

  async buildLocalGajiArtifact(request) {
    const wasmModule = await this.ensureProjectModule();
    return JSON.parse(requireExport(wasmModule, "wasm_local_gaji_artifact_json")(JSON.stringify(request)));
  }

  async planGajiLifecycle(request) {
    const wasmModule = await this.ensureProjectModule();
    return JSON.parse(requireExport(wasmModule, "wasm_gaji_lifecycle_plan_json")(JSON.stringify(request)));
  }

  async projectGraph(source) {
    const wasmModule = await this.ensureProjectModule();
    const raw = requireExport(wasmModule, "wasm_project_graph_json")(JSON.stringify(source));
    return JSON.parse(String(raw ?? "{}"));
  }

  async projectSymbols(source) {
    const wasmModule = await this.ensureProjectModule();
    const raw = requireExport(wasmModule, "wasm_project_symbols_json")(JSON.stringify(source));
    return JSON.parse(String(raw ?? "{}"));
  }

  async prepareProjectLink(projectSource, target = "앱", strict = true, includeLock = true) {
    const wasmModule = await this.ensureProjectModule();
    const raw = requireExport(wasmModule, "wasm_project_prepare_link_json")(
      JSON.stringify(projectSource),
      target,
      strict,
      includeLock,
    );
    return JSON.parse(String(raw ?? "{}"));
  }

  async planProjectEdit(request) {
    const wasmModule = await this.ensureProjectModule();
    const raw = requireExport(wasmModule, "wasm_project_edit_plan_json")(JSON.stringify(request));
    return JSON.parse(String(raw ?? "{}"));
  }

  async projectGajiLock(source, { allowMissing = false } = {}) {
    const wasmModule = await this.ensureProjectModule();
    if (allowMissing && typeof wasmModule.wasm_project_gaji_lock_json !== "function") return null;
    const raw = requireExport(wasmModule, "wasm_project_gaji_lock_json")(JSON.stringify(source));
    return String(raw ?? "");
  }

  async publishLocalGotgan(request) {
    const wasmModule = await this.ensureProjectModule();
    const operation = requireExport(
      wasmModule,
      "wasm_publish_local_gotgan_json",
      "E_GOTGAN_WASM_REQUIRED 공통 Rust/WASM 발행 기능이 필요합니다",
    );
    return JSON.parse(operation(JSON.stringify(request)));
  }

  async searchLocalGotgan(request) {
    const wasmModule = await this.ensureProjectModule();
    const operation = requireExport(
      wasmModule,
      "wasm_search_local_gotgan_json",
      "E_GOTGAN_WASM_REQUIRED 공통 Rust/WASM 검색 기능이 필요합니다",
    );
    return JSON.parse(operation(JSON.stringify(request)));
  }
}

export class RuntimeBridgeV1 {
  #adapter;

  constructor({ adapter = new WasmRuntimeAdapter() } = {}) {
    if (!adapter || typeof adapter !== "object") {
      throw new TypeError("runtime adapter must be an object");
    }
    this.schema = RUNTIME_BRIDGE_V1_SCHEMA;
    this.#adapter = adapter;
  }

  async createSession(options) {
    return new RuntimeSessionV1(await this.#adapter.createSession(options));
  }

  canonMaegimPlan(sourceText) { return this.#adapter.canonMaegimPlan(sourceText); }
  sourceAnalysis(request) { return this.#adapter.sourceAnalysis(request); }
  runSummaryWithSourceProfile(request) { return this.#adapter.runSummaryWithSourceProfile(request); }
  planGajiExtraction(request) { return this.#adapter.planGajiExtraction(request); }
  projectSourceSha256(source) { return this.#adapter.projectSourceSha256(source); }
  buildLocalGajiArtifact(request) { return this.#adapter.buildLocalGajiArtifact(request); }
  planGajiLifecycle(request) { return this.#adapter.planGajiLifecycle(request); }
  projectGraph(source) { return this.#adapter.projectGraph(source); }
  projectSymbols(source) { return this.#adapter.projectSymbols(source); }
  prepareProjectLink(projectSource, target, strict, includeLock) {
    return this.#adapter.prepareProjectLink(projectSource, target, strict, includeLock);
  }
  planProjectEdit(request) { return this.#adapter.planProjectEdit(request); }
  projectGajiLock(source, options) { return this.#adapter.projectGajiLock(source, options); }
  publishLocalGotgan(request) { return this.#adapter.publishLocalGotgan(request); }
  searchLocalGotgan(request) { return this.#adapter.searchLocalGotgan(request); }
}

export function createRuntimeBridgeV1(options = {}) {
  return new RuntimeBridgeV1(options);
}
