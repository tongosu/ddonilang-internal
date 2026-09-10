import { createRuntimeBridgeV1 } from "../runtime/runtime_bridge.js";
import { createHostBridgeV1 } from "../host/host_bridge.js";
import { extractCanonicalViewAuthorityInputsFromState } from "../seamgrim_runtime_state.js";
import {
  analyzeSourceReadiness,
  MODULE_DIRECTIVE_ANALYSIS_SNAPSHOT_SCHEMA,
  applySourceReadinessFix,
  projectAuthoritativeSourceAnalysis,
  projectSourceAnalysisUnavailable,
  SOURCE_ANALYSIS_PROFILE_IDENTITY,
  SOURCE_READINESS_DIAGNOSTIC_CODE,
  SOURCE_READINESS_FIX_ID,
} from "./source_readiness.js";
import {
  describePersistenceStatus,
  localProjectStorageKey as projectStorageKey,
  loadLocalFallbackSnapshot,
  saveLocalFallbackSnapshot,
  stableCanonicalJson,
} from "./persistence/local_fallback.js";
import {
  appendServerRevision,
  buildWorkbenchProjectArtifact,
  cloneServerProject,
  createServerProject,
  listServerRevisions,
  openServerProject,
  restoreServerRevision,
} from "./persistence/project_adapter.js";
import {
  buildWorkbenchCapabilityLink,
  captureWorkbenchCapabilitySession,
  clearWorkbenchCapabilitySession,
  readWorkbenchCapabilitySession,
  writeWorkbenchCapabilitySession,
} from "./persistence/capability_session.js";
import {
  appendRunCheckpoint,
  buildCheckpointPayload,
  buildRunArchiveDraft,
  createRunArchive,
  finalizeRunArchive,
  getRunArchive,
  listRunArchives,
  summarizeRunArchiveBoundary,
} from "./persistence/run_archive_adapter.js";
import {
  buildPortableProjectArtifact,
  parsePortableProjectArtifactBytes,
  portableProjectDiagnostic,
} from "./persistence/portable_project_artifact.js";
import { exportLocalGotganArtifact, importLocalGotganArtifact, loadLocalGotganStore, publishToLocalGotgan, searchLocalGotgan } from "./persistence/local_gotgan_store.js";
import {
  EXECUTION_EVENTS,
  EXECUTION_STATES,
  claimRunFinalization,
  createExecutionLifecycle,
  executionControlPolicy,
  executionStatusLabel,
  legacyRuntimeStatus,
  transitionExecutionLifecycle,
} from "./execution_lifecycle.js";
import {
  buildCanonicalViewPayloadSet,
  buildCommittedSemanticViewPayload,
  stableSemanticJson,
} from "./semantic_view_payload.js";
import {
  renderCommittedSemanticView,
} from "./semantic_view_renderer.js";
import {
  closeAllSideViews,
  closeViewInstance,
  createViewWorkspace,
  focusPrimaryView,
  hydrateViewWorkspaceWithMigration,
  legacySelectedView,
  openMagnifierView,
  openSideView,
  overlayViewInstances,
  primaryViewInstance,
  reconcileViewWorkspace,
  selectViewTarget,
  serializeViewWorkspace,
  sideViewInstances,
  toggleOverlayView,
  viewRoleCapabilities,
} from "./view_instance_model.js";
import {
  actionById,
  buildProjectControlModel,
  buildSetupRecipe,
  emptyProjectControlModel,
  normalizeActionMap,
} from "./project_control_model.js";

const runtimeBridge = createRuntimeBridgeV1();
const hostBridge = createHostBridgeV1();

const FALLBACK_PENDULUM_DDN = `매마디:움직씨 := {
  중력:수 := 9.8.
  줄길이:수 := 1.
  처음각:수 := 0.5.
  처음각 보여주기.
}
`;

const FALLBACK_GRID_DDN = `설정 {
  제목: "격자 상태와 낙하 조각".
  설명: "격자게임상태와 격자 그림으로 한 단계 진행을 관찰합니다.".
  마디수: 12.
}.

(매마디)마다 {
  "grid" 보여주기.
  보개로 그려.
}.`;

const FALLBACK_PROJECTILE_DDN = `매마디:움직씨 := {
  초기속도x:수 := 8.
  초기속도y:수 := 15.
  중력가속도:수 := 9.8.
  시간간격:수 := 0.1.
  초기속도x 보여주기.
  초기속도y 보여주기.
  중력가속도 보여주기.
}
`;

const PROJECTS = [
  {
    id: "rep_phys_projectile_xy_v1",
    title: "포물선 운동",
    kind: "공식 물리 DDN",
    summary: "초기 가로속도, 세로속도, 중력가속도를 DDN에서 읽어 봉인 WASM 실행과 궤적 보개로 확인합니다.",
    tags: ["공식", "물리", "포물선", "WASM", "공개 쐐기"],
    primaryView: "projectile",
    viewGrade: "explicit",
    viewPolicy: {
      primary: "포물선 공간 보개와 궤적선",
      side: "가로속도/세로속도/중력 관찰값",
      overlay: "속도 벡터와 현재 물체",
      magnifier: "현재 위치 돋보기",
    },
    files: [
      {
        path: "lesson.ddn",
        role: "main",
        url: "../../lessons/rep_phys_projectile_xy_v1/lesson.ddn",
        fallback: FALLBACK_PROJECTILE_DDN,
      },
    ],
  },
  {
    id: "rep_phys_pendulum_wave1_v1",
    title: "진자 보기 코어",
    kind: "단일 DDN 파일",
    summary: "한 DDN 원문에서 실행, 관찰, 보개 역할을 함께 여는 대표 물리 프로젝트입니다.",
    tags: ["물리", "진자", "보개", "WASM"],
    primaryView: "pendulum",
    viewGrade: "explicit",
    viewPolicy: {
      primary: "진자 공간 보개",
      side: "theta/omega/energy 그래프",
      overlay: "각도재기와 길이재기",
      magnifier: "bob 위치 돋보기",
    },
    files: [
      {
        path: "lesson.ddn",
        role: "main",
        url: "../../lessons/rep_phys_pendulum_wave1_v1/lesson.ddn",
        fallback: FALLBACK_PENDULUM_DDN,
      },
    ],
  },
  {
    id: "rep_grid_game_state_drop_v1",
    title: "격자 상태와 낙하 조각",
    kind: "DDN + 보개 자료",
    summary: "게임 상태를 DDN 원문, 보개 자료, 표 관찰로 나누어 탐색하는 비수업용 프로젝트입니다.",
    tags: ["게임", "격자", "상태", "보개"],
    primaryView: "grid",
    viewGrade: "auto",
    viewPolicy: {
      primary: "격자 보개",
      side: "틱/낙하 위치 표",
      overlay: "낙하 조각 강조",
      magnifier: "현재 조각 확대",
    },
    files: [
      {
        path: "lesson.ddn",
        role: "main",
        url: "../../lessons/rep_grid_game_state_drop_v1/lesson.ddn",
        fallback: FALLBACK_GRID_DDN,
      },
      {
        path: "space2d.json",
        role: "view",
        url: "../../lessons/rep_grid_game_state_drop_v1/space2d.json",
        fallback: "{\n  \"schema\": \"seamgrim.space2d.v0\",\n  \"view_family\": \"grid2d\"\n}\n",
      },
      {
        path: "table.json",
        role: "observation",
        url: "../../lessons/rep_grid_game_state_drop_v1/table.json",
        fallback: "{\n  \"schema\": \"seamgrim.table.v0\",\n  \"columns\": [\"tick\", \"x\", \"y\"]\n}\n",
      },
      {
        path: "meta.toml",
        role: "meta",
        url: "../../lessons/rep_grid_game_state_drop_v1/meta.toml",
        fallback: "id = \"rep_grid_game_state_drop_v1\"\n",
      },
      {
        path: "action_map.json",
        role: "meta",
        url: "../../lessons/rep_grid_game_state_drop_v1/action_map.json",
        fallback: "{\n  \"schema\": \"ddn.input_action_map.v1\",\n  \"project_id\": \"rep_grid_game_state_drop_v1\",\n  \"actions\": []\n}\n",
      },
    ],
  },
  {
    id: "local_linear_slope_v1",
    title: "일차함수 기울기 작업",
    kind: "로컬 초안",
    summary: "공식 모음에 올리기 전 로컬 DDN 초안입니다. 모듈이 없는 한 파일 프로젝트로 유지됩니다.",
    tags: ["수학", "일차함수", "내 작업"],
    primaryView: "line",
    viewGrade: "output-only",
    viewPolicy: {
      primary: "그래프 보개",
      side: "x/y 관찰 표",
      overlay: "기울기 표시",
      magnifier: "점 좌표 확대",
    },
    files: [
      {
        path: "lesson.ddn",
        role: "main",
        fallback: `매마디:움직씨 := {
  a:수 := 2.
  b:수 := 1.
  x:수 := 2.
  y:수 := a * x + b.
  "series:line" 보여주기.
  x 보여주기.
  y 보여주기.
}
`,
      },
    ],
  },
];

const MY_WORK_INDEX_KEY = "seamgrim.workbench.my_work_index.v1";
const PORTABLE_PROJECT_CATALOG_KEY = "seamgrim.workbench.portable_project_catalog.v1";
const ONE_FILE_DDN_PROJECT_ID = "local_one_file_ddn_v1";
const ONE_FILE_DDN_DRAFT_KEY = "seamgrim.workbench.one_file_ddn.draft.v1";
const NATIVE_PROJECT_CATALOG_KEY = "seamgrim.workbench.native_project_catalog.v1";

let customOneFileProject = null;
let receivedPortableProjects = [];
let nativeProjects = [];

function writeNativeProjectCatalog() {
  try {
    globalThis.localStorage?.setItem?.(NATIVE_PROJECT_CATALOG_KEY, JSON.stringify(nativeProjects.slice(0, 30)));
  } catch (_) {
    // Local recovery is best-effort; portable export remains available.
  }
}

function loadNativeProjectCatalog() {
  try {
    const raw = globalThis.localStorage?.getItem?.(NATIVE_PROJECT_CATALOG_KEY) ?? "";
    const rows = raw ? JSON.parse(raw) : [];
    nativeProjects = Array.isArray(rows) ? rows.filter((row) => row?.id && Array.isArray(row?.files)) : [];
  } catch (_) {
    nativeProjects = [];
  }
}

function syncNativeProjectFromState(project = currentProject()) {
  const index = nativeProjects.findIndex((row) => row.id === project?.id);
  if (index < 0) return;
  const files = project.files.map((file) => ({
    ...file,
    fallback: String(state.fileTexts.get(file.path) ?? file.fallback ?? ""),
  }));
  const payload = project.portableSnapshot?.local_package_payload;
  const portableSnapshot = { ...project.portableSnapshot };
  if (localProjectTreePayloadFromSnapshot(project.portableSnapshot ?? {})) {
    portableSnapshot.local_package_payload = {
      ...payload,
      files: files.map((file) => ({ path: file.path, role: file.role, utf8_text: file.fallback })),
    };
  }
  nativeProjects[index] = {
    ...project,
    files,
    portableSnapshot,
  };
  writeNativeProjectCatalog();
}

function initialProjectIdFromLocation() {
  try {
    const params = new URLSearchParams(globalThis.location?.search ?? "");
    for (const key of ["project", "project_id", "lesson", "lesson_id", "source_lesson_id"]) {
      const value = String(params.get(key) ?? "").trim();
      if (value && PROJECTS.some((project) => project.id === value)) return value;
    }
  } catch (_) {
    // Static file and restricted contexts can keep the default public project.
  }
  return PROJECTS[0].id;
}

const state = {
  globalEntry: "ddn-search",
  projectId: initialProjectIdFromLocation(),
  activeFilePath: "lesson.ddn",
  mode: "ddn-main",
  fileTexts: new Map(),
  fileFilter: "",
  projectFilter: "",
  myWorkRows: [],
  recipeVersion: 1,
  pendingRecipe: null,
  nextInput: null,
  actionSeq: 0,
  projectControlsGeneration: 0,
  projectControlsRefreshTimer: null,
  projectControls: emptyProjectControlModel(initialProjectIdFromLocation()),
  diagnostics: [],
  runSeq: 0,
  activeRunId: "",
  runs: [],
  runArchives: [],
  selectedRunArchive: null,
  cursorIndex: -1,
  runtimeStatus: "idle",
  runtimeBusy: false,
  executionLifecycle: createExecutionLifecycle(),
  livePump: {
    generation: 0,
    scheduled: false,
    timerId: null,
    inFlight: false,
    inFlightPromise: null,
    stepStartCount: 0,
    stepCommitCount: 0,
    maxInFlight: 0,
    currentInFlight: 0,
    lastOrigin: "",
    lastCancelReason: "",
  },
  semanticViewPayload: null,
  semanticRenderModel: null,
  wasm: null,
  wasmVmEntryCount: 0,
  sourceReadiness: null,
  sourceAnalysisGeneration: 0,
  sourceAnalysisSourceText: "",
  sourceAnalysisInFlight: false,
  completionDocumentVersion: 1,
  completionGeneration: 0,
  completionItems: [],
  completionSelectedIndex: 0,
  sourceReadinessRunBlocked: false,
  sourceReadinessLastApplyOutcome: {
    schema: "seamgrim.workbench.source_readiness_apply_outcome.v1",
    status: "none",
    code: "",
    fix_it_id: "",
  },
  sourceReadinessLastRunOutcome: {
    schema: "seamgrim.workbench.source_readiness_run_outcome.v1",
    status: "none",
    code: "",
    source_hash: "",
  },
  projectExecution: {
    importedRecord: null,
    current: null,
    previousSuccess: null,
    failure: null,
    lockManuallyEdited: false,
    lockTrust: {
      schema: "seamgrim.workbench.project_lock_trust.v1",
      verified_source_hash: "",
      verified_lock_sha256: "",
      local_non_lock_edit_after_verified: false,
    },
  },
  viewWorkspace: createViewWorkspace(PROJECTS[0]),
  persistenceStatus: null,
  persistenceOperation: {
    generation: 0,
    completedGeneration: 0,
    phase: "idle",
    outcome: "",
  },
  lastPortableExport: null,
  pendingPortableImport: null,
  projectEditUndo: [],
  pendingProjectEdit: null,
  projectGraph: null,
  portableMetadataDraft: null,
  capabilitySession: null,
  serverProject: {
    projectId: "",
    headRevisionId: "",
    contentSha256: "",
    packageHash: "",
    editCapability: "",
    viewCapability: "",
    role: "",
    revisions: [],
    conflict: null,
  },
};

function emptyServerProjectState() {
  return {
    projectId: "",
    headRevisionId: "",
    contentSha256: "",
    packageHash: "",
    editCapability: "",
    viewCapability: "",
    role: "",
    revisions: [],
    conflict: null,
  };
}

function defaultOneFileDdnSource(title = "새 한 파일 DDN") {
  // The user-facing one-file template is current V25 source. Its title is
  // Workbench presentation metadata, not hidden source syntax.
  void title;
  return `매마디:움직씨 := {
  값:수 := 1.
  값 보여주기.
}
`;
}

function readOneFileDraft() {
  try {
    const raw = globalThis.localStorage?.getItem?.(ONE_FILE_DDN_DRAFT_KEY) ?? "";
    if (!raw) return "";
    const parsed = JSON.parse(raw);
    return String(parsed.source ?? "");
  } catch (_) {
    return "";
  }
}

function writeOneFileDraft(source) {
  try {
    globalThis.localStorage?.setItem?.(ONE_FILE_DDN_DRAFT_KEY, stableCanonicalJson({
      schema: "seamgrim.workbench.one_file_ddn_draft.v1",
      project_id: ONE_FILE_DDN_PROJECT_ID,
      source: String(source ?? ""),
    }));
  } catch (_) {
    // Local recovery is best-effort in restricted browser contexts.
  }
}

function readPortableProjectCatalog() {
  try {
    const parsed = JSON.parse(globalThis.localStorage?.getItem?.(PORTABLE_PROJECT_CATALOG_KEY) ?? "[]");
    return Array.isArray(parsed) ? parsed : [];
  } catch (_) {
    return [];
  }
}

function writePortableProjectCatalog(rows = []) {
  try {
    globalThis.localStorage?.setItem?.(PORTABLE_PROJECT_CATALOG_KEY, JSON.stringify(rows.slice(0, 30)));
  } catch (_) {
    // Local catalog is best-effort; import preview still works without it.
  }
}

function normalizePortableTextArray(value) {
  return Array.isArray(value)
    ? value.map((item) => String(item ?? "").trim()).filter(Boolean).slice(0, 12)
    : [];
}

function localProjectTreePayloadFromSnapshot(snapshot = {}) {
  const payload = snapshot?.local_package_payload;
  if (
    payload &&
    typeof payload === "object" &&
    payload.kind === "seamgrim.local_project_tree.v0" &&
    Array.isArray(payload.files) &&
    payload.files.length > 0
  ) {
    return payload;
  }
  return null;
}

function projectRunLineageFromPayload(payload = {}) {
  const source = payload?.run_lineage && typeof payload.run_lineage === "object" ? payload.run_lineage : {};
  const request = payload?.execution_preparation?.runtime_request && typeof payload.execution_preparation.runtime_request === "object"
    ? payload.execution_preparation.runtime_request
    : {
      frontdoor: String(payload?.frontdoor ?? "wasm_project_run_summary_json"),
      requested_ticks: Number(payload?.runtime_execution_envelope?.requested_ticks ?? 1),
      target: String(payload?.target ?? "앱"),
      target_path: String(payload?.target_path ?? payload?.entry_path ?? "app/main.ddn"),
    };
  const runRequestHash = String(source.run_request_hash ?? "").trim()
    || `candidate:fnv1a32:project_run_request:${stableHash(stableCanonicalJson(request))}`;
  const lineage = {
    schema: "seamgrim.local_project_run_lineage.v0",
    project_graph_hash: String(source.project_graph_hash ?? payload?.project_graph_sha256 ?? ""),
    lock_hash: String(source.lock_hash ?? payload?.lock_sha256 ?? ""),
    linked_source_hash: String(
      source.linked_source_hash
        ?? payload?.linked_execution_source_sha256
        ?? payload?.execution_preparation?.linked_source?.source_sha256
        ?? "",
    ),
    run_request_hash: runRequestHash,
    parent_run_id: String(source.parent_run_id ?? ""),
    branch_madi: source.branch_madi === null || source.branch_madi === undefined ? null : Number(source.branch_madi),
    branch_state_hash: String(source.branch_state_hash ?? ""),
    final_state_hash: String(source.final_state_hash ?? payload?.runtime_state_hash ?? ""),
    view_artifact_hash: String(source.view_artifact_hash ?? ""),
    created_revision: String(source.created_revision ?? payload?.summary_sha256 ?? payload?.bounded_state_sha256 ?? ""),
  };
  return {
    ...lineage,
    lineage_hash: String(source.lineage_hash ?? "").trim()
      || `candidate:fnv1a32:project_run_lineage:${stableHash(stableCanonicalJson(lineage))}`,
  };
}

function localProjectRunEvidenceFromProject(project = currentProject()) {
  if (state.projectExecution?.current?.evidence) {
    return state.projectExecution.current.evidence;
  }
  void project;
  return null;
}

function importedProjectRunEvidenceFromProject(project = currentProject()) {
  const payload = localProjectTreePayloadFromSnapshot(project.portableSnapshot ?? {});
  if (!payload) return null;
  const trace = payload.project_observation_trace && typeof payload.project_observation_trace === "object"
    ? payload.project_observation_trace
    : null;
  const traceRows = Array.isArray(trace?.rows) ? trace.rows : [];
  const outputRows = Array.isArray(payload.output_rows) ? payload.output_rows.map((row) => String(row ?? "")) : [];
  if (!traceRows.length && !outputRows.length && !String(payload.bounded_state_sha256 ?? "").trim()) return null;
  return {
    schema: "seamgrim.approved_workbench.local_project_run_evidence.v1",
    frontdoor: String(payload.frontdoor ?? "wasm_project_run_summary_json"),
    bounded_state_sha256: String(payload.bounded_state_sha256 ?? ""),
    runtime_state_hash: String(payload.runtime_state_hash ?? trace?.determinism?.runtime_state_hash ?? ""),
    summary_sha256: String(payload.summary_sha256 ?? ""),
    trace_sha256: String(trace?.trace_sha256 ?? ""),
    run_lineage: projectRunLineageFromPayload(payload),
    output_rows: outputRows,
    observation_rows: traceRows.map((row, index) => ({
      index: Number(row?.index ?? index),
      observation_id: String(row?.observation_id ?? `project.obs.${index + 1}`),
      name: String(row?.name ?? `output_${index + 1}`),
      value_text: String(row?.value_text ?? outputRows[index] ?? ""),
      unit: row?.unit === null || row?.unit === undefined ? "" : String(row.unit),
      state_hash_participation: Boolean(row?.state_hash_participation),
    })),
  };
}

function gajiIdsFromLocalProjectPayload(payload = {}) {
  const ids = new Set();
  for (const file of Array.isArray(payload.files) ? payload.files : []) {
    const pathValue = String(file?.path ?? "");
    const match = pathValue.match(/^vendor\/([^/]+)\/gaji\.toml$/u);
    if (match?.[1]) ids.add(match[1]);
  }
  return Array.from(ids).sort();
}

function filesFromLocalProjectPayload(payload = {}, snapshot = {}) {
  const entryPath = String(payload.entry_path ?? "").trim();
  const rows = (Array.isArray(payload.files) ? payload.files : [])
    .map((file) => ({
      path: String(file?.path ?? "").trim(),
      role: String(file?.role ?? "ddn_source").trim() || "ddn_source",
      fallback: String(file?.utf8_text ?? file?.text ?? ""),
    }))
    .filter((file) => file.path);
  rows.sort((left, right) => {
    if (left.path === entryPath) return -1;
    if (right.path === entryPath) return 1;
    return left.path.localeCompare(right.path, "ko");
  });
  if (!rows.length) {
    return [{
      path: "lesson.ddn",
      role: "main",
      fallback: String(snapshot.ddn_text ?? ""),
    }];
  }
  return rows;
}

function portableProjectFromArtifact(artifact = {}, { catalogId = "", importedAt = "" } = {}) {
  const snapshot = artifact.project_snapshot ?? {};
  const localProjectPayload = localProjectTreePayloadFromSnapshot(snapshot);
  const payloadGaji = localProjectPayload ? gajiIdsFromLocalProjectPayload(localProjectPayload) : [];
  const metadata = {
    ...(snapshot.metadata ?? {}),
    required_gaji: Array.isArray(snapshot.metadata?.required_gaji)
      ? snapshot.metadata.required_gaji
      : payloadGaji,
  };
  const title = String(metadata.title || snapshot.project_name || "받은 셈그림 프로젝트");
  const summary = String(metadata.summary || "검증된 local file에서 가져온 프로젝트입니다.");
  const tags = Array.from(new Set(["받은 프로젝트", ...normalizePortableTextArray(metadata.tags)]));
  const sourceLessonId = String(snapshot.source_lesson_id || "portable");
  const known = PROJECTS.find((project) => project.id === sourceLessonId);
  const hashPrefix = String(artifact.content_sha256 || "portable").slice(0, 12) || "portable";
  const id = catalogId || `portable_${hashPrefix}_${String(Date.now()).slice(-6)}`;
  const files = localProjectPayload
    ? filesFromLocalProjectPayload(localProjectPayload, snapshot)
    : [
      {
        path: "lesson.ddn",
        role: "main",
        fallback: String(snapshot.ddn_text ?? ""),
      },
    ];
  return {
    id,
    title,
    kind: localProjectPayload ? "받은 로컬 프로젝트" : "받은 프로젝트",
    summary,
    tags,
    primaryView: known?.primaryView ?? "line",
    viewGrade: "portable-verified",
    viewPolicy: known?.viewPolicy ?? {
      primary: "가져온 DDN 보개",
      side: "가져온 관찰값",
      overlay: "가져온 보기 후보",
      magnifier: "가져온 보기 확대",
    },
    portableMetadata: {
      ...metadata,
      title,
      summary,
      tags,
      origin_hash_prefix: hashPrefix,
      received_at: importedAt || new Date().toISOString(),
      official_claim_ignored: true,
      trust_badge: "integrity_verified_only",
    },
    portableSnapshot: snapshot,
    portableArtifact: artifact,
    files,
  };
}

function loadPortableProjectCatalog() {
  receivedPortableProjects = readPortableProjectCatalog()
    .map((row) => {
      try {
        return portableProjectFromArtifact(row.artifact, {
          catalogId: String(row.project_id || ""),
          importedAt: String(row.imported_at || ""),
        });
      } catch (_) {
        return null;
      }
    })
    .filter(Boolean);
}

function rememberPortableProject(project) {
  const artifact = project.portableArtifact;
  if (!artifact?.content_sha256) return;
  const rows = readPortableProjectCatalog();
  const next = {
    schema: "seamgrim.workbench.portable_project_entry.v1",
    project_id: project.id,
    title: project.title,
    content_sha256: artifact.content_sha256,
    imported_at: project.portableMetadata?.received_at || new Date().toISOString(),
    artifact,
  };
  writePortableProjectCatalog([next, ...rows]);
}

function buildOneFileProject(source = "") {
  return {
    id: ONE_FILE_DDN_PROJECT_ID,
    title: "새 한 파일 DDN",
    kind: "로컬 한 파일 DDN",
    summary: "예제 복제가 아니라 사용자가 직접 편집하는 최소 한 파일 프로젝트입니다.",
    tags: ["새 DDN", "로컬", "한 파일"],
    primaryView: "line",
    viewGrade: "source-only",
    viewPolicy: {
      primary: "실행 출력 보개",
      side: "값 관찰",
      overlay: "후보 원문 표시",
      magnifier: "현재 출력 확대",
    },
    files: [
      {
        path: "lesson.ddn",
        role: "main",
        fallback: source || defaultOneFileDdnSource(),
      },
    ],
  };
}

function ddnQuotedText(value) {
  return String(value ?? "").replace(/\\/g, "\\\\").replace(/"/g, '\\"').replace(/[\r\n]+/g, " ").trim();
}

function nativeProjectFiles(name, template = "physics") {
  const safeName = ddnQuotedText(name) || "새 DDN 프로젝트";
  if (template === "single") {
    return [
      {
        path: "lesson.ddn",
        role: "main",
        utf8_text: defaultOneFileDdnSource(safeName),
      },
    ];
  }
  const root = `프로젝트 {
  이름: "${safeName}".
  첫글: "./app/main.ddn".
  목표 { 앱: "./app/main.ddn". }
  모듈길 { 로컬: "./lib". }
}.`;
  if (template === "empty") {
    return [
      { path: "뿌리.ddn", role: "root", utf8_text: root },
      {
        path: "app/main.ddn",
        role: "ddn_source",
        // Local Project owns the shared V25 execution callable.  Its entry
        // file must contribute the callable body, not a second nested callable.
        utf8_text: `값:수 := 0.
값 보여주기.
`,
      },
    ];
  }
  return [
    { path: "뿌리.ddn", role: "root", utf8_text: root },
    {
      path: "app/main.ddn",
      role: "ddn_source",
      utf8_text: `(힘="./lib/힘") 쓰임.

운동:움직씨 := {
  위치초기:수 := 0.
  속도초기:수 := 20.
  시간간격:수 := 0.1.
  중력가속도:수 := 힘.중력.
  속도:수 := 속도초기 - 중력가속도 * 시간간격.
  위치:수 := 위치초기 + 속도 * 시간간격.
  위치 보여주기.
  속도 보여주기.
  힘.중력 보여주기.
}
`,
    },
    {
      path: "lib/힘.ddn",
      role: "ddn_source",
      utf8_text: `(중력=중력) 드러냄.

중력:수 := 9.8.
`,
    },
  ];
}

function buildNativeProject(name, template = "physics") {
  const title = String(name ?? "").trim() || "새 DDN 프로젝트";
  const files = nativeProjectFiles(title, template);
  const singleFile = template === "single";
  const payload = singleFile
    ? null
    : {
        schema: "seamgrim.local_project_payload.v0",
        kind: "seamgrim.local_project_tree.v0",
        root_path: "뿌리.ddn",
        entry_path: "app/main.ddn",
        files,
      };
  const id = `native_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 7)}`;
  const kind = template === "physics"
    ? "로컬 물리 DDN 프로젝트"
    : singleFile
      ? "로컬 한 파일 DDN 프로젝트"
      : "로컬 빈 DDN 프로젝트";
  const summary = singleFile
    ? "가져오기 없이 이 작업대에서 만든 네이티브 한 파일 프로젝트입니다."
    : "가져오기 없이 이 작업대에서 만든 네이티브 다중 파일 프로젝트입니다.";
  const templateTag = template === "physics" ? "물리" : singleFile ? "한 파일" : "빈 프로젝트";
  const portableSnapshot = {
    project_name: title,
    source_lesson_id: id,
    creation_template: template,
    metadata: { title, summary: "셈그림에서 새로 만든 DDN 프로젝트", tags: ["내 작업", "네이티브", templateTag] },
  };
  if (payload) portableSnapshot.local_package_payload = payload;
  const moduleDirectiveRegistry = template === "physics"
    ? {
        known_import_targets: ["./lib/힘"],
        public_definition_targets: ["중력"],
      }
    : null;
  return {
    id,
    title,
    kind,
    summary,
    creationTemplate: template,
    tags: ["내 작업", "로컬", "네이티브", templateTag],
    primaryView: template === "physics" ? "projectile" : "line",
    viewGrade: "source-authored",
    viewPolicy: {
      primary: template === "physics" ? "위치/속도 운동 보개" : "실행 출력 보개",
      side: "이름·값·단위 관찰",
      overlay: "현재 마디 상태",
      magnifier: "현재 관찰값 확대",
    },
    portableSnapshot,
    moduleDirectiveRegistry,
    files: files.map((file) => ({ path: file.path, role: file.role, fallback: file.utf8_text })),
  };
}

async function createNativeProject(name, template) {
  const project = buildNativeProject(name, template);
  nativeProjects = [project, ...nativeProjects];
  writeNativeProjectCatalog();
  await selectProject(project.id);
  state.activeFilePath = localProjectEntryPath(project);
  state.persistenceStatus = {
    schema: "seamgrim.workbench.persistence_status.v1",
    mode: "local_recovery",
    server_saved: false,
    local_saved: true,
    user_label: `새 네이티브 ${project.files.length === 1 ? "한 파일 " : ""}프로젝트 local recovery 준비`,
  };
  rememberMyWorkProject({
    projectId: project.id,
    title: project.title,
    source: "local_only",
    role: "edit",
    updatedAt: new Date().toISOString(),
  });
  pushDiagnostic("W_NATIVE_PROJECT_CREATED", `${project.title}: 실제 DDN 파일 ${project.files.length}개를 만들었습니다.`);
  renderAll();
}

function allProjects() {
  return [
    ...nativeProjects,
    ...(customOneFileProject ? [customOneFileProject] : []),
    ...receivedPortableProjects,
    ...PROJECTS,
  ];
}

const els = {
  root: document.querySelector("[data-testid='approved-workbench-root']"),
  projectCount: document.querySelector("#project-count"),
  projectList: document.querySelector("#project-list"),
  projectSearch: document.querySelector("#project-search"),
  myWorkPanel: document.querySelector("[data-testid='my-work-panel']"),
  myWorkList: document.querySelector("[data-testid='my-work-list']"),
  myWorkCount: document.querySelector("[data-testid='my-work-count']"),
  title: document.querySelector("#project-title"),
  kind: document.querySelector("#project-kind"),
  summary: document.querySelector("#project-summary"),
  sourceTitle: document.querySelector("#source-panel-title"),
  sourceEditor: document.querySelector("#source-editor"),
  completionPopup: document.querySelector("#completion-popup"),
  fileTabs: document.querySelector("[data-testid='file-tabs']"),
  fileDrawer: document.querySelector("[data-testid='file-drawer']"),
  fileList: document.querySelector("#file-list"),
  fileSearch: document.querySelector("#file-search"),
  fileCount: document.querySelector("#file-count"),
  layout: document.querySelector("[data-testid='workbench-layout']"),
  canvas: document.querySelector("#canvas-bogae"),
  ratioLabel: document.querySelector("#mode-ratio-label"),
  viewGradeLabel: document.querySelector("#view-grade-label"),
  projectServerMeta: document.querySelector("[data-testid='project-server-meta']"),
  projectEditLink: document.querySelector("[data-testid='project-edit-link']"),
  projectViewLink: document.querySelector("[data-testid='project-view-link']"),
  projectRevisionList: document.querySelector("[data-testid='project-revision-list']"),
  projectClone: document.querySelector("[data-testid='project-clone']"),
  portableExport: document.querySelector("[data-testid='portable-project-export']"),
  portableExportStatus: document.querySelector("[data-testid='portable-project-export-status']"),
  portableImport: document.querySelector("[data-testid='portable-project-import']"),
  portableDialog: document.querySelector("[data-testid='portable-project-dialog']"),
  portableImportInput: document.querySelector("[data-testid='portable-project-import-input']"),
  portableImportPreview: document.querySelector("[data-testid='portable-project-import-preview']"),
  portableImportTitle: document.querySelector("[data-testid='portable-project-import-title']"),
  portableImportIntegrity: document.querySelector("[data-testid='portable-project-import-integrity']"),
  portableImportTrust: document.querySelector("[data-testid='portable-project-import-trust']"),
  portableImportDetails: document.querySelector("[data-testid='portable-project-import-details']"),
  portableOpen: document.querySelector("[data-testid='portable-project-open']"),
  portableCancel: document.querySelector("[data-testid='portable-project-cancel']"),
  portableMetadataStatus: document.querySelector("[data-testid='portable-metadata-status']"),
  portableMetaTitle: document.querySelector("[data-testid='portable-meta-title']"),
  portableMetaSummary: document.querySelector("[data-testid='portable-meta-summary']"),
  portableMetaContentKind: document.querySelector("[data-testid='portable-meta-content-kind']"),
  portableMetaTags: document.querySelector("[data-testid='portable-meta-tags']"),
  portableMetaSubject: document.querySelector("[data-testid='portable-meta-subject']"),
  portableMetaLevel: document.querySelector("[data-testid='portable-meta-level']"),
  portableMetaRequiredViews: document.querySelector("[data-testid='portable-meta-required-views']"),
  portableMetaRequiredGaji: document.querySelector("[data-testid='portable-meta-required-gaji']"),
  portableLineageOrigin: document.querySelector("[data-testid='portable-lineage-origin']"),
  portableLineageFile: document.querySelector("[data-testid='portable-lineage-file']"),
  portableLineageVersion: document.querySelector("[data-testid='portable-lineage-version']"),
  projectConflictPanel: document.querySelector("[data-testid='project-conflict-panel']"),
  projectConflictMessage: document.querySelector("[data-testid='project-conflict-message']"),
  projectConflictServer: document.querySelector("[data-testid='project-conflict-server']"),
  projectConflictLocal: document.querySelector("[data-testid='project-conflict-local']"),
  projectConflictLocalPackage: document.querySelector("[data-testid='project-conflict-local-package']"),
  projectStorageDrawer: document.querySelector("[data-testid='project-storage-drawer']"),
  projectHistoryDrawer: document.querySelector("[data-testid='project-history-drawer']"),
  projectVerificationDrawer: document.querySelector("[data-testid='project-verification-drawer']"),
  projectVerificationOpen: document.querySelector("[data-testid='project-verification-open']"),
  runStatus: document.querySelector("[data-testid='run-status']"),
  runHash: document.querySelector("[data-testid='run-hash']"),
  currentMadi: document.querySelector("[data-testid='current-madi']"),
  runLineage: document.querySelector("[data-testid='run-lineage']"),
  runArchiveStatus: document.querySelector("[data-testid='run-archive-status']"),
  runArchiveList: document.querySelector("[data-testid='run-archive-list']"),
  runArchiveDetail: document.querySelector("[data-testid='run-archive-detail']"),
  runArchiveDetailTitle: document.querySelector("[data-testid='run-archive-detail-title']"),
  runArchiveCheckpointList: document.querySelector("[data-testid='run-archive-checkpoint-list']"),
  saveStatus: document.querySelector("[data-testid='project-save-status']"),
  bogaeStage: document.querySelector("[data-testid='bogae-stage']"),
  sideViewTitle: document.querySelector("[data-testid='side-view-title']"),
  sideViewBody: document.querySelector("[data-testid='side-view-body']"),
  sideViewList: document.querySelector("[data-testid='side-view-list']"),
  viewPrimary: document.querySelector("[data-testid='view-role-primary']"),
  viewSide: document.querySelector("[data-testid='view-role-side']"),
  viewOverlay: document.querySelector("[data-testid='view-role-overlay']"),
  viewMagnifier: document.querySelector("[data-testid='view-role-magnifier']"),
  bogaeSourceAccess: document.querySelector("[data-testid='bogae-source-access']"),
  layoutPolicy: document.querySelector("[data-testid='layout-policy']"),
  viewRoleSummary: document.querySelector("[data-testid='view-role-summary']"),
  controlGrid: document.querySelector("[data-testid='control-grid']"),
  setupControls: document.querySelector("[data-testid='setup-controls']"),
  setupControlList: document.querySelector("[data-testid='setup-control-list']"),
  setupStatus: document.querySelector("[data-testid='setup-status']"),
  actionControls: document.querySelector("[data-testid='action-controls']"),
  actionButtonList: document.querySelector("[data-testid='action-button-list']"),
  actionStatus: document.querySelector("[data-testid='action-status']"),
  viewStatus: document.querySelector("[data-testid='view-status']"),
  diagnostics: document.querySelector("[data-testid='diagnostic-list']"),
  semanticObservations: document.querySelector("[data-testid='semantic-observations']"),
  projectCreateDialog: document.querySelector("[data-testid='project-create-dialog']"),
  projectCreateForm: document.querySelector("[data-testid='project-create-form']"),
  projectCreateName: document.querySelector("[data-testid='project-create-name']"),
  projectEditDialog: document.querySelector("[data-testid='project-edit-dialog']"),
  projectEditSummary: document.querySelector("[data-testid='project-edit-summary']"),
  projectEditPreview: document.querySelector("[data-testid='project-edit-preview']"),
  projectGraphSummary: document.querySelector("[data-testid='project-graph-summary']"),
  projectGraphList: document.querySelector("[data-testid='project-graph-list']"),
  projectGraphDiagnostics: document.querySelector("[data-testid='project-graph-diagnostics']"),
  gajiBundleDialog: document.querySelector("[data-testid='gaji-bundle-dialog']"),
  gajiBundleForm: document.querySelector("[data-testid='gaji-bundle-form']"),
  gajiBundleId: document.querySelector("[data-testid='gaji-bundle-id']"),
  gajiBundleVersion: document.querySelector("[data-testid='gaji-bundle-version']"),
  gajiBundleDescription: document.querySelector("[data-testid='gaji-bundle-description']"),
  gajiBundleTags: document.querySelector("[data-testid='gaji-bundle-tags']"),
  gajiBundleSelected: document.querySelector("[data-testid='gaji-bundle-selected']"),
  gajiBundlePreview: document.querySelector("[data-testid='gaji-bundle-preview']"),
  gajiBundleStatus: document.querySelector("[data-testid='gaji-bundle-status']"),
  gajiBundlePublish: document.querySelector("[data-testid='gaji-bundle-publish']"),
  gajiShelfDialog: document.querySelector("[data-testid='gaji-shelf-dialog']"),
  gajiShelfSearch: document.querySelector("[data-testid='gaji-shelf-search']"),
  gajiShelfResults: document.querySelector("[data-testid='gaji-shelf-results']"),
  gajiInstallAlias: document.querySelector("[data-testid='gaji-install-alias']"),
  gajiInstallPreview: document.querySelector("[data-testid='gaji-install-preview']"),
  gajiInstallStatus: document.querySelector("[data-testid='gaji-install-status']"),
  gajiInstallApply: document.querySelector("[data-testid='gaji-install-apply']"),
  gajiInstallRemove: document.querySelector("[data-testid='gaji-install-remove']"),
  gajiRemixStart: document.querySelector("[data-testid='gaji-remix-start']"),
  gajiRemixEditor: document.querySelector("[data-testid='gaji-remix-editor']"),
  gajiRemixId: document.querySelector("[data-testid='gaji-remix-id']"),
  gajiRemixVersion: document.querySelector("[data-testid='gaji-remix-version']"),
  gajiRemixSource: document.querySelector("[data-testid='gaji-remix-source']"),
  gajiRemixPublish: document.querySelector("[data-testid='gaji-remix-publish']"),
};

let pendingGajiBundle = null;
let pendingGajiInstall = null;

function currentProject() {
  return allProjects().find((project) => project.id === state.projectId) ?? PROJECTS[0];
}

function activeFile(project = currentProject()) {
  return project.files.find((file) => file.path === state.activeFilePath) ?? project.files[0];
}

function activeRun() {
  return state.runs.find((run) => run.run_id === state.activeRunId) ?? null;
}

function activeFrame() {
  const run = activeRun();
  if (!run || state.cursorIndex < 0) return null;
  return run.frames[state.cursorIndex] ?? null;
}

function executionLifecycleContext() {
  const run = activeRun();
  return {
    hasFrame: Boolean(activeFrame()),
    frameCount: run?.frames.length ?? 0,
    cursorIndex: state.cursorIndex,
  };
}

function syncExecutionLifecycleCompatibility() {
  state.runtimeStatus = legacyRuntimeStatus(state.executionLifecycle);
}

function applyExecutionEvent(event, payload = {}) {
  const result = transitionExecutionLifecycle(state.executionLifecycle, event, payload);
  if (result.accepted) {
    state.executionLifecycle = result.lifecycle;
    syncExecutionLifecycleCompatibility();
  }
  return result;
}

function executionGenerationIsCurrent(generation, projectId) {
  return Number(state.executionLifecycle.generation) === Number(generation)
    && state.projectId === projectId;
}

function assertExecutionGeneration(generation, projectId) {
  if (executionGenerationIsCurrent(generation, projectId)) return;
  const err = new Error("E_EXECUTION_GENERATION_SUPERSEDED: 오래된 실행 준비 결과를 폐기했습니다");
  err.code = "E_EXECUTION_GENERATION_SUPERSEDED";
  throw err;
}

const LIVE_PUMP_INTERVAL_MS = 32;

function cancelLivePump(reason = "cancelled", { invalidateInFlight = true } = {}) {
  if (state.livePump.timerId !== null) {
    clearTimeout(state.livePump.timerId);
  }
  state.livePump.timerId = null;
  state.livePump.scheduled = false;
  state.livePump.lastCancelReason = reason;
  if (invalidateInFlight) state.livePump.generation += 1;
}

function resetLivePumpMetricsForRun() {
  state.livePump.stepStartCount = 0;
  state.livePump.stepCommitCount = 0;
  state.livePump.maxInFlight = 0;
  state.livePump.currentInFlight = 0;
  state.livePump.lastOrigin = "";
}

function livePumpToken() {
  return {
    executionGeneration: Number(state.executionLifecycle.generation),
    pumpGeneration: Number(state.livePump.generation),
    projectId: state.projectId,
    runId: state.activeRunId,
  };
}

function livePumpTokenIsCurrent(token, { allowPausing = false, allowPaused = false } = {}) {
  if (!token || Number(token.pumpGeneration) !== Number(state.livePump.generation)) return false;
  if (!executionGenerationIsCurrent(token.executionGeneration, token.projectId)) return false;
  if (state.activeRunId !== token.runId) return false;
  const status = state.executionLifecycle.status;
  return status === EXECUTION_STATES.RUNNING
    || (allowPausing && status === EXECUTION_STATES.PAUSING)
    || (allowPaused && status === EXECUTION_STATES.PAUSED);
}

async function beginCommittedLiveStep(origin = "auto") {
  if (state.livePump.inFlight) return false;
  const token = livePumpToken();
  const allowPaused = origin === "manual";
  if (!livePumpTokenIsCurrent(token, { allowPaused })) return false;
  state.livePump.inFlight = true;
  state.livePump.currentInFlight += 1;
  state.livePump.maxInFlight = Math.max(state.livePump.maxInFlight, state.livePump.currentInFlight);
  state.livePump.stepStartCount += 1;
  state.livePump.lastOrigin = origin;
  renderAll();
  const operation = commitNextLiveStep({ origin, token });
  state.livePump.inFlightPromise = operation;
  try {
    return await operation;
  } finally {
    state.livePump.currentInFlight = Math.max(0, state.livePump.currentInFlight - 1);
    state.livePump.inFlight = false;
    if (state.livePump.inFlightPromise === operation) state.livePump.inFlightPromise = null;
    if (state.executionLifecycle.status === EXECUTION_STATES.PAUSING) {
      applyExecutionEvent(EXECUTION_EVENTS.PAUSE_COMMITTED);
    }
    renderAll();
  }
}

async function runLivePumpTurn(expectedPumpGeneration) {
  if (Number(expectedPumpGeneration) !== Number(state.livePump.generation)) return false;
  if (state.executionLifecycle.status !== EXECUTION_STATES.RUNNING) return false;
  const committed = await beginCommittedLiveStep("auto");
  if (committed && state.executionLifecycle.status === EXECUTION_STATES.RUNNING) {
    scheduleLivePump();
  }
  return committed;
}

function scheduleLivePump() {
  const lifecycle = state.executionLifecycle;
  if (lifecycle.status !== EXECUTION_STATES.RUNNING || lifecycle.mode !== "live") return false;
  if (state.livePump.scheduled || state.livePump.inFlight) return false;
  const expectedPumpGeneration = Number(state.livePump.generation);
  state.livePump.scheduled = true;
  state.livePump.timerId = setTimeout(() => {
    state.livePump.timerId = null;
    state.livePump.scheduled = false;
    runLivePumpTurn(expectedPumpGeneration).catch((err) => {
      pushDiagnostic("E_LIVE_PUMP_TURN_FAILED", String(err?.message ?? err), "error");
      renderAll();
    });
  }, LIVE_PUMP_INTERVAL_MS);
  return true;
}

function includesFilter(project, filter) {
  const needle = String(filter ?? "").trim().toLowerCase();
  if (!needle) return true;
  const metadata = project.portableMetadata ?? {};
  const haystack = [
    project.id,
    project.title,
    project.kind,
    project.summary,
    metadata.summary,
    metadata.subject,
    metadata.level,
    metadata.origin_hash_prefix,
    ...(project.tags ?? []),
    ...(metadata.tags ?? []),
    ...(metadata.content_kinds ?? []),
    ...(metadata.required_views ?? []),
    ...(metadata.required_gaji ?? []),
  ]
    .join(" ")
    .toLowerCase();
  return haystack.includes(needle);
}

function projectsForGlobalEntry() {
  if (state.globalEntry === "official-collection") return PROJECTS;
  return allProjects();
}

function inferContentKinds(project = currentProject()) {
  const text = [project.kind, project.primaryView, ...(project.tags ?? [])].join(" ").toLowerCase();
  if (text.includes("게임") || text.includes("game") || text.includes("grid")) return ["game"];
  if (text.includes("manim")) return ["korean_manim"];
  if (text.includes("ai")) return ["ai_gym"];
  if (text.includes("증명") || text.includes("시험")) return ["test_or_proof"];
  if (text.includes("수업") || text.includes("교과")) return ["lesson"];
  return ["simulation"];
}

function inferSubject(project = currentProject()) {
  const text = [project.kind, project.title, project.summary, ...(project.tags ?? [])].join(" ").toLowerCase();
  if (text.includes("물리") || text.includes("phys") || text.includes("진자") || text.includes("포물선")) return "physics";
  if (text.includes("수학") || text.includes("math") || text.includes("일차함수")) return "math";
  if (text.includes("게임") || text.includes("grid")) return "game";
  return "general";
}

function defaultPortableMetadata(project = currentProject()) {
  return {
    title: project.title,
    summary: project.summary,
    content_kinds: inferContentKinds(project),
    tags: [...(project.tags ?? [])],
    subject: inferSubject(project),
    level: "local",
    required_views: Object.keys(project.viewPolicy ?? {}),
    required_gaji: [],
    determinism_grade: project.viewGrade || "candidate",
    trust_badge: "unverified_local_file",
  };
}

function trimPortableText(value, limit = 120) {
  return String(value ?? "").replace(/\s+/g, " ").trim().slice(0, limit);
}

function portableListFromText(value, limit = 8) {
  return String(value ?? "")
    .split(/[,\n]/u)
    .map((item) => trimPortableText(item, 40))
    .filter(Boolean)
    .slice(0, limit);
}

function normalizePortableMetadataDraft(value = {}, project = currentProject()) {
  const base = defaultPortableMetadata(project);
  const row = value && typeof value === "object" && !Array.isArray(value) ? value : {};
  const kind = String(row.content_kind ?? row.content_kinds?.[0] ?? base.content_kinds[0] ?? "simulation");
  const allowedKind = ["simulation", "game", "lesson", "korean_manim", "ai_gym", "test_or_proof"].includes(kind)
    ? kind
    : "simulation";
  return {
    title: trimPortableText(row.title ?? base.title, 80),
    summary: trimPortableText(row.summary ?? base.summary, 180),
    content_kinds: [allowedKind],
    tags: Array.isArray(row.tags) ? row.tags.map((item) => trimPortableText(item, 40)).filter(Boolean).slice(0, 8) : portableListFromText(base.tags.join(", "), 8),
    subject: trimPortableText(row.subject ?? base.subject, 40),
    level: trimPortableText(row.level ?? base.level, 40),
    required_views: Array.isArray(row.required_views) ? row.required_views.map((item) => trimPortableText(item, 40)).filter(Boolean).slice(0, 8) : [...base.required_views],
    required_gaji: Array.isArray(row.required_gaji) ? row.required_gaji.map((item) => trimPortableText(item, 40)).filter(Boolean).slice(0, 8) : [...base.required_gaji],
    determinism_grade: trimPortableText(row.determinism_grade ?? base.determinism_grade, 40),
    trust_badge: "unverified_local_file",
  };
}

function metadataDraftFromProject(project = currentProject()) {
  return normalizePortableMetadataDraft(project.portableMetadata ?? defaultPortableMetadata(project), project);
}

function currentPortableMetadata(project = currentProject()) {
  return normalizePortableMetadataDraft(state.portableMetadataDraft ?? metadataDraftFromProject(project), project);
}

function currentPortableLineage(project = currentProject()) {
  if (project.portableArtifact?.content_sha256) {
    const snapshot = project.portableSnapshot ?? {};
    return {
      source_lesson_id: String(snapshot.source_lesson_id || "portable"),
      source_project_id: "",
      source_revision_id: "",
      source_package_hash: "",
      origin_content_sha256: String(project.portableArtifact.content_sha256 || ""),
      origin_kind: project.id.includes("_clone_") ? "portable_clone" : "portable_import",
    };
  }
  const sourceLessonId = project.id === ONE_FILE_DDN_PROJECT_ID ? "custom" : project.id;
  const originKind = state.serverProject.projectId
    ? "server_project"
    : project.id === ONE_FILE_DDN_PROJECT_ID
      ? "one_file_ddn"
      : "official_lesson";
  return {
    source_lesson_id: sourceLessonId,
    source_project_id: state.serverProject.projectId || "",
    source_revision_id: state.serverProject.headRevisionId || "",
    source_package_hash: state.serverProject.packageHash || "",
    origin_content_sha256: "",
    origin_kind: originKind,
  };
}

async function loadText(file) {
  if (file.url) {
    try {
      const response = await fetch(new URL(file.url, import.meta.url), { cache: "no-store" });
      if (response.ok) {
        return await response.text();
      }
    } catch (_) {
      // Local file previews and restricted test contexts use the deterministic fallback.
    }
  }
  return String(file.fallback ?? "");
}

async function loadProjectFiles(project) {
  state.fileTexts.clear();
  for (const file of project.files) {
    state.fileTexts.set(file.path, await loadText(file));
  }
}

function renderGlobalNav() {
  document.querySelectorAll("[data-global-entry]").forEach((button) => {
    button.classList.toggle("active", button.dataset.globalEntry === state.globalEntry);
  });
  const myWork = state.globalEntry === "my-work";
  els.myWorkPanel.classList.toggle("hidden", !myWork);
  els.projectList.classList.toggle("hidden", myWork);
  renderMyWork();
}

function readMyWorkIndex() {
  try {
    const parsed = JSON.parse(globalThis.localStorage?.getItem?.(MY_WORK_INDEX_KEY) ?? "[]");
    return Array.isArray(parsed) ? parsed : [];
  } catch (_) {
    return [];
  }
}

function writeMyWorkIndex(rows = []) {
  globalThis.localStorage?.setItem?.(MY_WORK_INDEX_KEY, JSON.stringify(rows.slice(0, 20)));
}

function rememberMyWorkProject({
  projectId = "",
  title = "",
  headRevisionId = "",
  editCapability = "",
  viewCapability = "",
  source = "",
  role = "",
} = {}) {
  const normalizedProjectId = String(projectId || "").trim();
  if (!normalizedProjectId) return;
  const next = {
    schema: "seamgrim.workbench.my_work_entry.v1",
    project_id: normalizedProjectId,
    title: String(title || currentProject().title || normalizedProjectId),
    head_revision_id: String(headRevisionId || ""),
    edit_capability: String(editCapability || ""),
    view_capability: String(viewCapability || ""),
    origin_kind: String(source || (editCapability || viewCapability ? "server_saved" : "local_only")),
    access_role: String(role || (editCapability ? "edit" : viewCapability ? "view" : "edit")),
    updated_at: new Date().toISOString(),
  };
  const rows = readMyWorkIndex().filter((row) => String(row.project_id ?? "") !== normalizedProjectId);
  writeMyWorkIndex([next, ...rows]);
  state.myWorkRows = [next, ...rows];
}

async function refreshMyWorkIndex() {
  const rows = readMyWorkIndex();
  const verified = [];
  for (const row of rows) {
    const capability = String(row.edit_capability || row.view_capability || "");
    const projectId = String(row.project_id || "");
    let status = "server 확인 전";
    let head = String(row.head_revision_id || "");
    if (projectId && capability) {
      try {
        const payload = await openServerProject({ projectId, capability });
        status = "server 확인됨";
        head = String(payload.head_revision_id || head);
      } catch (err) {
        status = err?.status === 404 ? "삭제됨 또는 만료됨" : err?.status === 403 || err?.status === 401 ? "권한 만료" : "서버 확인 실패";
      }
    }
    verified.push({ ...row, verify_status: status, head_revision_id: head });
  }
  state.myWorkRows = verified;
  renderMyWork();
  return verified;
}

function renderMyWork() {
  if (!els.myWorkList) return;
  const filter = String(state.projectFilter || "").trim().toLowerCase();
  const rows = (state.myWorkRows.length ? state.myWorkRows : readMyWorkIndex())
    .filter((row) => !filter || String(row.title || row.project_id).toLowerCase().includes(filter));
  const portableRows = readPortableProjectCatalog()
    .filter((row) => !filter || String(row.title || row.project_id).toLowerCase().includes(filter));
  els.myWorkCount.textContent = `${rows.length + portableRows.length}`;
  els.myWorkList.innerHTML = "";
  if (!rows.length && !portableRows.length) {
    els.myWorkList.innerHTML = `<span class="my-work-item">저장된 작업 없음</span>`;
    return;
  }
  rows.forEach((row) => {
    const capability = String(row.edit_capability || row.view_capability || "");
    const role = row.edit_capability ? "edit" : "view";
    const href = capability
      ? projectLink({ projectId: row.project_id, role, capability })
      : "#";
    const link = document.createElement("a");
    link.className = "my-work-item";
    link.href = href;
    link.setAttribute("data-testid", "my-work-item");
    link.dataset.projectId = String(row.project_id || "");
    const origin = row.origin_kind === "local_only" ? "로컬 전용" : "서버 저장";
    const access = row.access_role === "view" || (!row.edit_capability && row.view_capability) ? "보기 전용" : "편집 가능";
    link.innerHTML = `<strong>${escapeHtml(row.title || row.project_id)}</strong><span>${origin} · ${access} · ${escapeHtml(row.verify_status || (origin === "로컬 전용" ? "이 기기" : "server 확인 전"))} · head ${escapeHtml(row.head_revision_id || "-")}</span>`;
    els.myWorkList.appendChild(link);
  });
  portableRows.forEach((row) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "my-work-item";
    button.setAttribute("data-testid", "my-work-item");
    button.dataset.portableProjectId = String(row.project_id || "");
    button.innerHTML = `<strong>${escapeHtml(row.title || row.project_id)}</strong><span>받은 프로젝트 · 편집 가능 복제본 · ${escapeHtml(String(row.content_sha256 || "").slice(0, 12) || "-")}</span>`;
    els.myWorkList.appendChild(button);
  });
}

function renderProjects() {
  const visible = projectsForGlobalEntry().filter((project) => includesFilter(project, state.projectFilter));
  els.projectCount.textContent = `${visible.length}`;
  els.projectList.innerHTML = "";
  visible.forEach((project) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `project-card${project.id === state.projectId ? " active" : ""}`;
    button.dataset.projectId = project.id;
    button.setAttribute("role", "option");
    button.setAttribute("aria-selected", project.id === state.projectId ? "true" : "false");
    button.setAttribute("data-testid", `project-card-${project.id}`);
    button.innerHTML = `<strong>${project.title}</strong><span>${project.kind} · ${project.tags.join(", ")}</span>`;
    button.addEventListener("click", () => selectProject(project.id));
    els.projectList.appendChild(button);
  });
}

function renderFileTabs(project) {
  const visibleTabs = project.files.slice(0, Math.min(3, project.files.length));
  els.fileTabs.innerHTML = "";
  if (project.files.length <= 1) {
    els.fileTabs.classList.add("hidden");
    return;
  }
  els.fileTabs.classList.remove("hidden");
  visibleTabs.forEach((file) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `file-tab${file.path === state.activeFilePath ? " active" : ""}`;
    button.dataset.filePath = file.path;
    button.setAttribute("data-testid", `file-tab-${file.path.replace(/[^a-z0-9]/gi, "-")}`);
    button.textContent = file.path;
    button.addEventListener("click", () => selectFile(file.path));
    els.fileTabs.appendChild(button);
  });
}

function renderFileDrawer(project) {
  const manyFiles = project.files.length > 1;
  els.fileDrawer.classList.toggle("hidden", !manyFiles);
  els.fileCount.textContent = `${project.files.length}`;
  els.fileList.innerHTML = "";
  const filter = String(state.fileFilter ?? "").trim().toLowerCase();
  project.files
    .filter((file) => !filter || file.path.toLowerCase().includes(filter) || file.role.toLowerCase().includes(filter))
    .forEach((file) => {
      const wrap = document.createElement("div");
      wrap.className = "file-row-wrap";
      const button = document.createElement("button");
      button.type = "button";
      button.className = `file-row${file.path === state.activeFilePath ? " active" : ""}`;
      button.dataset.filePath = file.path;
      button.setAttribute("data-testid", `file-row-${file.path.replace(/[^a-z0-9]/gi, "-")}`);
      button.innerHTML = `<strong>${file.path}</strong><span>${file.role}</span>`;
      button.addEventListener("click", () => selectFile(file.path));
      wrap.appendChild(button);
      if (nativeProjects.some((item) => item.id === project.id)) {
        const actions = document.createElement("div");
        actions.className = "file-row-actions";
        actions.setAttribute("aria-label", `${file.path} 작업`);
        const definitions = [
          ["rename", "이름 변경", "✎"],
          ["duplicate", "복제", "⧉"],
          ["set_entry", "진입 파일 지정", "▶"],
          ["delete", "삭제", "×"],
        ];
        definitions.forEach(([action, label, glyph]) => {
          const actionButton = document.createElement("button");
          actionButton.type = "button";
          actionButton.className = "panel-action";
          actionButton.dataset.fileAction = action;
          actionButton.dataset.filePath = file.path;
          actionButton.title = `${file.path} ${label}`;
          actionButton.setAttribute("aria-label", `${file.path} ${label}`);
          actionButton.textContent = glyph;
          actions.appendChild(actionButton);
        });
        wrap.appendChild(actions);
      }
      els.fileList.appendChild(wrap);
    });
  renderProjectGraph();
}

function projectDiagnosticFix(code = "") {
  const fixes = {
    E_MODULE_MISSING: "쓰임 경로를 존재하는 DDN 파일로 바꾸거나 해당 모듈을 추가하세요.",
    E_IMPORT_CYCLE: "순환을 이루는 쓰임 중 하나를 제거하거나 공통 모듈로 분리하세요.",
    E_SYMBOL_NOT_EXPORTED: "대상 모듈의 드러냄 목록에 심볼을 추가하세요.",
    E_PROJECT_ENTRY_MISSING: "존재하는 DDN 파일을 진입 파일로 지정하세요.",
    E_GAJI_LOCK_STALE: "현재 project graph에서 lock을 다시 생성하세요.",
  };
  return fixes[code] || "표시된 파일과 경로를 확인한 뒤 다시 실행하세요.";
}

function renderProjectGraph() {
  if (!els.projectGraphSummary || !els.projectGraphList || !els.projectGraphDiagnostics) return;
  const row = state.projectGraph;
  els.projectGraphList.innerHTML = "";
  els.projectGraphDiagnostics.innerHTML = "";
  if (!row) {
    els.projectGraphSummary.textContent = "graph: 확인 전";
    return;
  }
  if (row.error) {
    els.projectGraphSummary.textContent = `graph: ${row.error.code || "오류"}`;
  } else {
    els.projectGraphSummary.textContent = `entry ${row.graph.entry_path} · files ${row.graph.file_count} · lock ${row.lockStatus}`;
    const edges = [
      `진입 → ${row.graph.entry_path}`,
      ...Object.entries(row.graph.module_paths ?? {}).map(([name, path]) => `모듈 ${name} → ${path}`),
      ...(row.symbols?.imports ?? []).map((item) => `${item.importer_path} —${item.alias}→ ${item.resolved_path}`),
      ...Object.entries(row.graph.gaji_aliases ?? {}).map(([name, path]) => `가지 ${name} → ${path}`),
    ];
    edges.forEach((text) => {
      const item = document.createElement("div");
      item.className = "project-graph-edge";
      item.textContent = text;
      els.projectGraphList.appendChild(item);
    });
  }
  const diagnostics = row.error ? [row.error] : [...(row.graph?.diagnostics ?? []), ...(row.symbols?.diagnostics ?? [])];
  diagnostics.forEach((diagnostic) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "project-graph-diagnostic";
    button.dataset.severity = "error";
    button.textContent = `${diagnostic.code}: ${diagnostic.message}\n위치: ${diagnostic.path || "프로젝트"}\n고침: ${projectDiagnosticFix(diagnostic.code)}`;
    if (diagnostic.path && currentProject().files.some((file) => file.path === diagnostic.path)) {
      button.addEventListener("click", () => selectFile(diagnostic.path));
    } else {
      button.disabled = true;
    }
    els.projectGraphDiagnostics.appendChild(button);
  });
}

function renderSource(project) {
  const file = activeFile(project);
  els.sourceTitle.textContent = file.path;
  els.sourceEditor.value = state.fileTexts.get(file.path) ?? "";
}

function completionPosition(source, offset) {
  const before = source.slice(0, offset);
  const line = before.lastIndexOf("\n") + 1;
  return {
    line: before.slice(0, line).split("\n").length - 1,
    character: before.slice(line).length,
  };
}

function completionOffset(source, position) {
  const lines = source.split("\n");
  if (position.line < 0 || position.line >= lines.length) return null;
  const lineStart = lines.slice(0, position.line).reduce((total, line) => total + line.length + 1, 0);
  if (position.character < 0 || position.character > lines[position.line].length) return null;
  return lineStart + position.character;
}

function closeCompletionPopup() {
  state.completionItems = [];
  state.completionSelectedIndex = 0;
  if (els.completionPopup) {
    els.completionPopup.hidden = true;
    els.completionPopup.replaceChildren();
  }
  els.sourceEditor?.removeAttribute("aria-activedescendant");
}

function renderCompletionPopup() {
  const popup = els.completionPopup;
  if (!popup || !state.completionItems.length) {
    if (popup) popup.hidden = true;
    els.sourceEditor?.removeAttribute("aria-activedescendant");
    return;
  }
  popup.replaceChildren();
  popup.hidden = false;
  state.completionItems.forEach((item, index) => {
    const option = document.createElement("button");
    option.type = "button";
    option.className = "completion-option";
    option.id = `completion-option-${index}`;
    option.setAttribute("role", "option");
    option.setAttribute("aria-selected", index === state.completionSelectedIndex ? "true" : "false");
    option.dataset.testid = `completion-option-${index}`;
    const label = document.createElement("span");
    label.textContent = String(item.label ?? "");
    const detail = document.createElement("span");
    detail.className = "completion-option-detail";
    detail.textContent = String(item.canonical_detail ?? "");
    option.append(label, detail);
    option.addEventListener("mousedown", (event) => event.preventDefault());
    option.addEventListener("click", () => selectCompletion(index));
    popup.appendChild(option);
  });
  els.sourceEditor.setAttribute("aria-activedescendant", `completion-option-${state.completionSelectedIndex}`);
}

function selectCompletion(index = state.completionSelectedIndex) {
  const item = state.completionItems[index];
  if (!item) return;
  const source = els.sourceEditor.value;
  const start = completionOffset(source, item.replacement_range?.start);
  const end = completionOffset(source, item.replacement_range?.end);
  if (start === null || end === null || start > end) {
    closeCompletionPopup();
    return;
  }
  const next = `${source.slice(0, start)}${String(item.insert_text ?? "")}${source.slice(end)}`;
  els.sourceEditor.value = next;
  els.sourceEditor.setSelectionRange(start + String(item.insert_text ?? "").length, start + String(item.insert_text ?? "").length);
  closeCompletionPopup();
  els.sourceEditor.dispatchEvent(new Event("input", { bubbles: true }));
  els.sourceEditor.focus();
}

async function requestCompletion() {
  const file = activeFile();
  const source = els.sourceEditor?.value ?? "";
  if (!file?.path?.endsWith(".ddn") || els.sourceEditor?.readOnly) {
    closeCompletionPopup();
    return;
  }
  const generation = ++state.completionGeneration;
  const version = state.completionDocumentVersion;
  const cursor = els.sourceEditor.selectionStart ?? source.length;
  const result = await runtimeBridge.sharedCompletion({
    schema: "ddonilang.completion.v1-candidate",
    profile: "v1-core-v25",
    document_identity: `seamgrim://${encodeURIComponent(currentProject().id)}/${encodeURIComponent(file.path)}`,
    document_version: version,
    source,
    position: completionPosition(source, cursor),
    encoding: "utf-16",
  }).catch(() => null);
  if (
    generation !== state.completionGeneration
    || version !== state.completionDocumentVersion
    || source !== els.sourceEditor.value
    || !result
  ) return;
  state.completionItems = Array.isArray(result.candidates) ? result.candidates : [];
  state.completionSelectedIndex = 0;
  renderCompletionPopup();
}

function renderProjectMeta(project) {
  els.title.textContent = project.title;
  els.kind.textContent = project.kind;
  els.summary.textContent = project.summary;
}

function escapeHtml(value = "") {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function projectLink({ projectId = "", role = "view", capability = "" } = {}) {
  return buildWorkbenchCapabilityLink({
    baseUrl: globalThis.location?.href ?? "",
    projectId,
    role,
    capability,
  });
}

function updateProjectLink(node, { href = "", label = "" } = {}) {
  if (!node) return;
  if (!href) {
    node.href = "#";
    node.textContent = label || "링크 없음";
    node.setAttribute("aria-disabled", "true");
    return;
  }
  node.href = href;
  node.textContent = label;
  node.setAttribute("aria-disabled", "false");
}

const EXECUTION_CONTROL_BINDINGS = Object.freeze([
  ["lifecycle-run", "canStart", "실행", "새 실행을 시작할 수 있는 상태가 아닙니다."],
  ["lifecycle-pause", "canPause", "멈춤", "연속 실행 중에만 멈출 수 있습니다."],
  ["lifecycle-resume", "canResume", "다시 실행", "최신 마디에서 멈춘 연속 실행만 재개할 수 있습니다."],
  ["lifecycle-step", "canStep", "한 마디 앞으로", "최신 마디에서 멈춘 연속 실행만 한 마디 진행할 수 있습니다."],
  ["lifecycle-stop", "canStop", "중지", "준비 중이거나 활성 상태인 실행이 없습니다."],
  ["history-back", "canBack", "한 마디 뒤로 보기", "읽을 수 있는 이전 마디가 없습니다."],
  ["history-branch", "canBranch", "현재 마디에서 갈라 이어가기", "갈라 이어갈 기록 마디가 없습니다."],
]);

function renderExecutionControls() {
  const policy = executionControlPolicy(state.executionLifecycle, executionLifecycleContext());
  const blockConcurrentCommand = Boolean(state.runtimeBusy);
  const stepInFlight = Boolean(state.livePump.inFlight);
  for (const [testId, policyKey, label, unavailable] of EXECUTION_CONTROL_BINDINGS) {
    const button = document.querySelector(`[data-testid='${testId}']`);
    if (!button) continue;
    const preparingStop = testId === "lifecycle-stop" && policy.status === EXECUTION_STATES.PREPARING;
    const pumpBoundaryCommand = testId === "lifecycle-pause" || testId === "lifecycle-stop";
    const concurrentBlocked = (blockConcurrentCommand && !preparingStop)
      || (stepInFlight && !pumpBoundaryCommand);
    const enabled = Boolean(policy[policyKey]) && !concurrentBlocked;
    const reasonCode = concurrentBlocked ? "operation_in_flight" : enabled ? "" : `${policy.status}_${policyKey}`;
    const reasonText = concurrentBlocked ? "이전 실행 명령이 완료되는 중입니다." : unavailable;
    button.disabled = !enabled;
    button.dataset.disabledReason = reasonCode;
    button.title = enabled ? label : `${label}: ${reasonText}`;
    button.setAttribute("aria-label", enabled ? label : `${label}, 사용 불가: ${reasonText}`);
  }
  els.root.dataset.executionState = policy.status;
  els.root.dataset.executionMode = policy.mode;
  els.root.dataset.executionGeneration = String(state.executionLifecycle.generation);
}

function renderServerProject() {
  const server = state.serverProject;
  const project = currentProject();
  const projectId = server.projectId || state.capabilitySession?.project_id || "";
  const revisionId = server.headRevisionId || "";
  const role = state.capabilitySession?.role || server.role || "";
  const canEdit = role === "edit" || !projectId;
  const canPortableClone = Boolean(project.portableArtifact?.content_sha256);
  els.projectServerMeta.textContent = projectId
    ? `project: ${projectId} · head: ${revisionId || "-"} · role: ${role || "-"}`
    : "project: 아직 서버 저장 전";
  const saveButton = document.querySelector("[data-testid='project-save']");
  saveButton.disabled = Boolean(projectId && !canEdit);
  saveButton.dataset.disabledReason = saveButton.disabled ? "view_write_forbidden" : "";
  renderExecutionControls();
  if (els.projectClone) {
    els.projectClone.disabled = !canPortableClone && (!projectId || !state.capabilitySession?.capability);
    els.projectClone.dataset.disabledReason = els.projectClone.disabled ? "clone_source_unavailable" : "";
    els.projectClone.textContent = canPortableClone || role === "view" ? "내 버전 만들기" : "복제본 만들기";
  }
  updateProjectLink(els.projectEditLink, {
    href: projectId && server.editCapability
      ? projectLink({ projectId, role: "edit", capability: server.editCapability })
      : "",
    label: "편집 링크",
  });
  updateProjectLink(els.projectViewLink, {
    href: projectId && server.viewCapability
      ? projectLink({ projectId, role: "view", capability: server.viewCapability })
      : "",
    label: "보기 링크",
  });
  const revisions = Array.isArray(server.revisions) ? server.revisions : [];
  els.projectRevisionList.innerHTML = revisions.length
    ? revisions
      .map((row) => {
        const rid = String(row.revision_id ?? "");
        const content = String(row.content_sha256 ?? "").slice(0, 12);
        const pack = String(row.package_hash ?? "").slice(0, 12);
        const isHead = rid === revisionId;
        const restoreButton = isHead || !canEdit
          ? ""
          : `<button type="button" data-testid="project-restore-revision" data-project-restore-revision="${escapeHtml(rid)}" title="이 리비전을 새 HEAD로 복원">복원</button>`;
        return `<span class="project-revision-item" data-testid="project-revision-item" data-project-revision-id="${escapeHtml(rid)}" data-head="${isHead ? "true" : "false"}"><span>rev ${escapeHtml(rid)} · content ${escapeHtml(content || "-")} · package ${escapeHtml(pack || "-")}</span>${restoreButton}</span>`;
      })
      .join("")
    : "<span>revision: -</span>";
  const conflict = server.conflict;
  els.projectConflictPanel.classList.toggle("hidden", !conflict);
  if (conflict) {
    els.projectConflictMessage.textContent = conflict.message || "다른 창에서 먼저 저장되었습니다.";
    els.projectConflictServer.textContent = `server: ${conflict.serverRevisionId || "-"} · ${String(conflict.serverContentSha256 || "").slice(0, 16) || "-"}`;
    els.projectConflictLocal.textContent = `local parent: ${conflict.localParentRevisionId || "-"}`;
    els.projectConflictLocalPackage.value = conflict.localPackageJson || "";
  } else {
    els.projectConflictLocalPackage.value = "";
  }
}

function renderPortableLineage(project = currentProject()) {
  if (!els.portableLineageOrigin) return;
  const lineage = project.portableSnapshot?.lineage ?? currentPortableLineage(project);
  const originLabel = project.portableArtifact
    ? String(lineage.source_lesson_id || project.portableSnapshot?.source_lesson_id || "portable")
    : project.id === ONE_FILE_DDN_PROJECT_ID
      ? "custom"
      : project.title;
  const fileHash = project.portableArtifact?.content_sha256
    ? String(project.portableArtifact.content_sha256).slice(0, 12)
    : "-";
  const version = state.serverProject.headRevisionId
    ? `revision ${state.serverProject.headRevisionId}`
    : project.id.includes("_clone_")
      ? project.id
      : "-";
  els.portableLineageOrigin.textContent = `원본: ${originLabel || "-"}`;
  els.portableLineageFile.textContent = `받은 파일: ${fileHash}`;
  els.portableLineageVersion.textContent = `내 버전: ${version}`;
}

function stableHash(text) {
  let hash = 0x811c9dc5;
  for (let i = 0; i < text.length; i += 1) {
    hash ^= text.charCodeAt(i);
    hash = Math.imul(hash, 0x01000193);
  }
  return (hash >>> 0).toString(16).padStart(8, "0");
}

function activeSourceText() {
  return state.fileTexts.get("lesson.ddn") ?? state.fileTexts.get(activeFile().path) ?? "";
}

function localProjectEntryPath(project = currentProject()) {
  const payload = localProjectTreePayloadFromSnapshot(project.portableSnapshot ?? {});
  return String(payload?.entry_path ?? project.files?.[0]?.path ?? "lesson.ddn").trim() || "lesson.ddn";
}

function activeRuntimeSourceText(project = currentProject()) {
  const entryPath = localProjectEntryPath(project);
  return state.fileTexts.get(entryPath) ?? state.fileTexts.get("lesson.ddn") ?? state.fileTexts.get(activeFile(project).path) ?? "";
}

function sourceReadinessViewOnly() {
  const capabilityRole = state.capabilitySession?.role || state.serverProject.role || "";
  return Boolean((state.serverProject.projectId || state.capabilitySession?.project_id) && capabilityRole === "view");
}

function sourceReadinessApplyOutcome(status, details = {}) {
  const outcome = {
    schema: "seamgrim.workbench.source_readiness_apply_outcome.v1",
    status,
    code: String(details.code ?? ""),
    fix_it_id: String(details.fix_it_id ?? ""),
    changed: Boolean(details.changed),
    changed_count: Number(details.changed_count ?? 0),
    source_hash_before: String(details.source_hash_before ?? ""),
    source_hash_after: String(details.source_hash_after ?? ""),
  };
  state.sourceReadinessLastApplyOutcome = outcome;
  return outcome;
}

function sourceReadinessRunOutcome(status, details = {}) {
  const outcome = {
    schema: "seamgrim.workbench.source_readiness_run_outcome.v1",
    status,
    code: String(details.code ?? ""),
    source_hash: String(details.source_hash ?? ""),
    run_generation: Number(state.runSeq),
    run_record_count: state.runs.length,
    wasm_vm_entry_count: Number(state.wasmVmEntryCount),
  };
  state.sourceReadinessLastRunOutcome = outcome;
  return outcome;
}

function refreshPendingSourceReadiness(project = currentProject()) {
  const previousHash = String(state.sourceReadiness?.source_hash ?? "");
  const entryPath = localProjectEntryPath(project);
  const next = analyzeSourceReadiness(activeRuntimeSourceText(project), entryPath);
  state.sourceReadiness = next;
  if (previousHash && previousHash !== next.source_hash) {
    state.sourceReadinessRunBlocked = false;
  }
  return next;
}

function refreshSourceReadiness(project = currentProject()) {
  const entryPath = localProjectEntryPath(project);
  const pending = analyzeSourceReadiness(activeRuntimeSourceText(project), entryPath);
  if (
    state.sourceReadiness?.authority_status === "shared_frontend"
    && state.sourceReadiness.source_hash === pending.source_hash
  ) {
    return state.sourceReadiness;
  }
  return refreshPendingSourceReadiness(project);
}

function moduleDirectiveRegistryForProject(project) {
  const registry = project?.moduleDirectiveRegistry;
  if (!registry) return null;
  const known = registry.known_import_targets;
  const publicDefinitions = registry.public_definition_targets;
  if (!Array.isArray(known) || !Array.isArray(publicDefinitions)) return null;
  if (![...known, ...publicDefinitions].every((value) => typeof value === "string" && value.length > 0)) {
    return null;
  }
  return {
    known_import_targets: [...known],
    public_definition_targets: [...publicDefinitions],
  };
}

async function refreshAuthoritativeSourceReadiness(project = currentProject()) {
  const projectIdAtRequest = project.id;
  const entryPath = localProjectEntryPath(project);
  const pending = analyzeSourceReadiness(activeRuntimeSourceText(project), entryPath);
  if (!pending.ready) {
    state.sourceReadiness = pending;
    return pending;
  }

  for (let attempt = 0; attempt < 2; attempt += 1) {
    const sourceAtRequest = activeRuntimeSourceText(project);
    const generation = state.sourceAnalysisGeneration + 1;
    state.sourceAnalysisGeneration = generation;
    state.sourceAnalysisSourceText = sourceAtRequest;
    try {
      const registry = moduleDirectiveRegistryForProject(project);
      const request = {
        source_text: sourceAtRequest,
        path: entryPath,
        analysis_generation: generation,
        source_profile_identity: SOURCE_ANALYSIS_PROFILE_IDENTITY,
      };
      const snapshot = registry
        ? await runtimeBridge.moduleDirectiveAnalysis({
            schema: MODULE_DIRECTIVE_ANALYSIS_SNAPSHOT_SCHEMA,
            ...request,
            module_registry: registry,
          })
        : await runtimeBridge.sourceAnalysis(request);
      if (currentProject().id !== projectIdAtRequest) {
        return { ...pending, ready: false, blocked: true, superseded: true };
      }
      const sourceStillCurrent = activeRuntimeSourceText(currentProject()) === sourceAtRequest;
      const generationStillCurrent = state.sourceAnalysisGeneration === generation;
      if (!sourceStillCurrent || !generationStillCurrent) continue;
      const projected = projectAuthoritativeSourceAnalysis(snapshot, {
        expectedAnalysisGeneration: generation,
        sourceHash: pending.source_hash,
        sourceText: sourceAtRequest,
      });
      if (projected.stale) continue;
      state.sourceReadiness = projected;
      return projected;
    } catch (error) {
      const unavailable = projectSourceAnalysisUnavailable(error, {
        analysisGeneration: generation,
        sourceHash: pending.source_hash,
      });
      state.sourceReadiness = unavailable;
      return unavailable;
    }
  }

  const stale = projectSourceAnalysisUnavailable("E_SOURCE_ANALYSIS_STALE", {
    analysisGeneration: state.sourceAnalysisGeneration,
    sourceHash: pending.source_hash,
  });
  stale.authority_status = "shared_frontend_stale_rejected";
  state.sourceReadiness = stale;
  return stale;
}

function getSourceReadinessCandidate() {
  const candidate = state.sourceReadiness?.candidate;
  return candidate ? JSON.parse(JSON.stringify(candidate)) : null;
}

function sameAuthoritativeRepairCandidate(left, right) {
  if (!left || !right) return false;
  return String(left.repair_proposal_identity ?? "") === String(right.repair_proposal_identity ?? "")
    && String(left.diagnostic_identity ?? "") === String(right.diagnostic_identity ?? "")
    && String(left.source_revision_identity ?? "") === String(right.source_revision_identity ?? "")
    && Number(left.analysis_generation) === Number(right.analysis_generation)
    && String(left.source_hash ?? "") === String(right.source_hash ?? "")
    && String(left.original_source ?? "") === String(right.original_source ?? "")
    && Number(left.start_offset_utf16) === Number(right.start_offset_utf16)
    && Number(left.end_offset_utf16) === Number(right.end_offset_utf16)
    && String(left.expected_slice ?? "") === String(right.expected_slice ?? "")
    && String(left.replacement ?? "") === String(right.replacement ?? "");
}

function sourceReadinessSnapshot() {
  const readiness = state.sourceReadiness ?? refreshSourceReadiness();
  const diagnostic = readiness.diagnostics?.[0] ?? null;
  const viewOnly = sourceReadinessViewOnly();
  return {
    schema: readiness.schema,
    policy_layer: readiness.policy_layer,
    authority_status: String(readiness.authority_status ?? ""),
    ready: Boolean(readiness.ready),
    blocked: Boolean(readiness.blocked),
    source_hash: String(readiness.source_hash ?? ""),
    source_revision_identity: String(readiness.source_revision_identity ?? ""),
    analysis_generation: Number(readiness.analysis_generation ?? 0),
    source_profile_identity: String(readiness.source_profile_identity ?? ""),
    analysis_outcome: String(readiness.analysis_outcome ?? ""),
    code: String(diagnostic?.code ?? ""),
    severity: String(diagnostic?.severity ?? ""),
    status_axis: String(diagnostic?.status_axis ?? ""),
    upstream_cause_code: String(diagnostic?.upstream_cause_code ?? ""),
    what: String(diagnostic?.what ?? ""),
    where: String(diagnostic?.where ?? ""),
    fix: String(diagnostic?.fix ?? ""),
    span: diagnostic?.span ? JSON.parse(JSON.stringify(diagnostic.span)) : null,
    diagnostic_identity: String(diagnostic?.diagnostic_identity ?? ""),
    repair_proposal_identity: String(readiness.candidate?.repair_proposal_identity ?? ""),
    fix_it_id: String(diagnostic?.fix_it?.id ?? ""),
    fix_it_trigger_authority: String(readiness.candidate?.trigger_authority ?? ""),
    fix_it_replacement_authority: String(readiness.candidate?.replacement_authority ?? ""),
    run_blocked: Boolean(state.sourceReadinessRunBlocked),
    apply_available: Boolean(readiness.candidate && !viewOnly),
    apply_disabled_reason: viewOnly ? "view_only" : readiness.candidate ? "" : "no_candidate",
    last_apply_outcome: { ...state.sourceReadinessLastApplyOutcome },
    last_run_outcome: { ...state.sourceReadinessLastRunOutcome },
    run_generation: Number(state.runSeq),
    run_record_count: state.runs.length,
    wasm_vm_entry_count: Number(state.wasmVmEntryCount),
    wasm_initialized: Boolean(state.wasm),
  };
}

function applySourceReadinessFixIt(candidateOverride = undefined) {
  const project = currentProject();
  const readiness = refreshSourceReadiness(project);
  const currentSource = activeRuntimeSourceText(project);
  if (sourceReadinessViewOnly()) {
    const outcome = sourceReadinessApplyOutcome("view_only_rejected", {
      code: "E_SOURCE_FIX_VIEW_ONLY",
      fix_it_id: SOURCE_READINESS_FIX_ID,
      source_hash_before: readiness.source_hash,
      source_hash_after: readiness.source_hash,
    });
    pushDiagnostic("E_SOURCE_FIX_VIEW_ONLY", "보기 전용 프로젝트에서는 원문 고침을 적용할 수 없습니다.", "error");
    renderAll();
    return outcome;
  }

  const candidate = candidateOverride === undefined ? getSourceReadinessCandidate() : candidateOverride;
  const candidateStillCurrent = candidate && (Array.isArray(readiness.candidates) ? readiness.candidates : [])
    .some((current) => sameAuthoritativeRepairCandidate(candidate, current));
  const authorityStale = candidate && (
    readiness.authority_status !== "shared_frontend"
    || String(candidate.source_revision_identity ?? "") !== String(readiness.source_revision_identity ?? "")
    || Number(candidate.analysis_generation) !== Number(readiness.analysis_generation)
    || !candidateStillCurrent
  );
  if (authorityStale) {
    const outcome = sourceReadinessApplyOutcome("stale_rejected", {
      code: "E_SOURCE_FIX_STALE",
      fix_it_id: SOURCE_READINESS_FIX_ID,
      source_hash_before: readiness.source_hash,
      source_hash_after: readiness.source_hash,
    });
    pushDiagnostic("E_SOURCE_FIX_STALE", "원문 또는 권위 분석 세대가 고침 후보를 만든 뒤 달라져 적용하지 않았습니다.", "error");
    renderAll();
    return outcome;
  }
  const result = applySourceReadinessFix(currentSource, candidate);
  if (result.status === "stale_rejected") {
    const outcome = sourceReadinessApplyOutcome("stale_rejected", {
      ...result,
      code: "E_SOURCE_FIX_STALE",
      fix_it_id: SOURCE_READINESS_FIX_ID,
    });
    pushDiagnostic("E_SOURCE_FIX_STALE", "원문이 고침 후보를 만든 뒤 달라져 적용하지 않았습니다.", "error");
    renderAll();
    return outcome;
  }
  if (result.status === "no_op") {
    const outcome = sourceReadinessApplyOutcome("no_op", {
      ...result,
      code: "W_SOURCE_FIX_NO_OP",
      fix_it_id: SOURCE_READINESS_FIX_ID,
    });
    pushDiagnostic("W_SOURCE_FIX_NO_OP", "적용할 구식 채비: 표면이 없습니다.");
    renderAll();
    return outcome;
  }

  const entryPath = localProjectEntryPath(project);
  state.fileTexts.set(entryPath, result.source);
  state.activeFilePath = entryPath;
  state.lastPortableExport = null;
  state.sourceReadinessRunBlocked = false;
  syncNativeProjectFromState(project);
  markCurrentProjectExecutionStale("source_readiness_fix");
  if (state.projectExecution?.failure) state.projectExecution.failure = null;
  clearTimeout(state.projectGraphRefreshTimer);
  state.projectGraphRefreshTimer = setTimeout(() => refreshProjectGraph().catch(() => {}), 250);
  if (project.id === ONE_FILE_DDN_PROJECT_ID && entryPath === "lesson.ddn") {
    writeOneFileDraft(result.source);
  }
  refreshPendingSourceReadiness(project);
  const outcome = sourceReadinessApplyOutcome("applied", {
    ...result,
    code: "W_SOURCE_FIX_APPLIED",
    fix_it_id: SOURCE_READINESS_FIX_ID,
  });
  pushDiagnostic("W_SOURCE_FIX_APPLIED", "고침을 적용했습니다. 콜론을 제거해 채비 {로 바꿨습니다.");
  // The fix action lives inside the verification modal. Close the modal before
  // restoring focus; otherwise the editor is inert and keyboard focus cannot
  // return to the corrected source.
  if (els.projectVerificationDrawer?.open) els.projectVerificationDrawer.close();
  renderAll();
  els.sourceEditor.focus();
  const focusOffset = Number(result.focus_offset_utf16 ?? 0);
  els.sourceEditor.setSelectionRange?.(focusOffset, focusOffset);
  return outcome;
}

function currentVirtualProjectSource(project = currentProject()) {
  const payload = localProjectTreePayloadFromSnapshot(project.portableSnapshot ?? {});
  if (!payload) return null;
  const files = [];
  const seen = new Set();
  for (const file of Array.isArray(payload.files) ? payload.files : []) {
    const pathValue = String(file?.path ?? "").trim();
    if (!pathValue || seen.has(pathValue)) continue;
    seen.add(pathValue);
    files.push({
      path: pathValue,
      role: String(file?.role ?? "ddn_source").trim() || "ddn_source",
      utf8_text: String(state.fileTexts.get(pathValue) ?? file?.utf8_text ?? file?.text ?? ""),
    });
  }
  if (!files.length) return null;
  return {
    schema: "ddn.virtual_project_source.v1",
    kind: "seamgrim.local_project_tree.v0",
    root_path: String(payload.root_path ?? "뿌리.ddn").trim() || "뿌리.ddn",
    entry_path: String(payload.entry_path ?? files[0]?.path ?? "lesson.ddn").trim() || "lesson.ddn",
    files,
  };
}

function currentProjectDdnSources(project = currentProject()) {
  return (Array.isArray(project?.files) ? project.files : [])
    .filter((file) => String(file?.path ?? "").toLowerCase().endsWith(".ddn"))
    .map((file) => ({
      source_path: String(file.path),
      source_text: String(state.fileTexts.get(file.path) ?? file.fallback ?? ""),
    }))
    .filter((file) => file.source_text.trim());
}

function declaredActionMapFromProject(project = currentProject()) {
  const candidates = [
    project?.portableSnapshot?.controls_snapshot?.action_map,
    project?.actionMap,
  ];
  for (const file of Array.isArray(project?.files) ? project.files : []) {
    const text = String(state.fileTexts.get(file.path) ?? file.fallback ?? "").trim();
    if (!text || !String(file.path ?? "").toLowerCase().endsWith(".json")) continue;
    try {
      candidates.push(JSON.parse(text));
    } catch (_) {
      // Other project JSON files are not action-map payloads.
    }
  }
  for (const candidate of candidates) {
    const normalized = normalizeActionMap(candidate, project?.id ?? state.projectId);
    if (normalized) return normalized;
  }
  return null;
}

async function refreshProjectControls(project = currentProject()) {
  const generation = state.projectControlsGeneration + 1;
  state.projectControlsGeneration = generation;
  const projectId = String(project?.id ?? state.projectId);
  state.projectControls = emptyProjectControlModel(projectId, "loading");
  renderProjectControls();
  try {
    const planRows = [];
    for (const { source_path, source_text } of currentProjectDdnSources(project)) {
      planRows.push({
        source_path,
        plan: await runtimeBridge.canonMaegimPlan(source_text),
      });
    }
    if (generation !== state.projectControlsGeneration || state.projectId !== projectId) return null;
    state.projectControls = buildProjectControlModel({
      projectId,
      planRows,
      actionMap: declaredActionMapFromProject(project),
    });
    renderProjectControls();
    return state.projectControls;
  } catch (err) {
    if (generation !== state.projectControlsGeneration || state.projectId !== projectId) return null;
    state.projectControls = {
      ...emptyProjectControlModel(projectId, "error"),
      error: {
        code: "E_PROJECT_AUTHORING_PLAN",
        message: String(err?.message ?? err),
      },
    };
    renderProjectControls();
    return state.projectControls;
  }
}

function scheduleProjectControlsRefresh() {
  clearTimeout(state.projectControlsRefreshTimer);
  state.projectControlsRefreshTimer = setTimeout(() => {
    refreshProjectControls(currentProject()).catch(() => {});
  }, 250);
}

function setupControlTestId(name) {
  const slug = String(name ?? "")
    .trim()
    .toLowerCase()
    .replace(/[^\p{L}\p{N}_-]+/gu, "-")
    .replace(/^-+|-+$/gu, "");
  return `setup-${slug || "control"}`;
}

function renderProjectControls() {
  if (!els.controlGrid || !els.setupControls || !els.actionControls) return;
  const model = state.projectControls ?? emptyProjectControlModel(state.projectId);
  const controls = model.project_id === state.projectId && Array.isArray(model.controls) ? model.controls : [];
  const actions = model.project_id === state.projectId && Array.isArray(model.actions) ? model.actions : [];
  els.controlGrid.hidden = !controls.length && !actions.length;
  els.setupControls.hidden = !controls.length;
  els.actionControls.hidden = !actions.length;
  els.root.dataset.projectControlStatus = String(model.status ?? "idle");
  els.root.dataset.projectControlCount = String(controls.length);
  els.root.dataset.projectActionCount = String(actions.length);
  els.root.dataset.projectControlSource = controls.length ? String(model.source ?? "") : "";
  els.root.dataset.projectAuthoringPlanHash = String(model.authoring_plan_hash ?? "");
  els.root.dataset.projectActionMapHash = String(model.action_map?.action_map_hash ?? "");

  if (els.setupControlList) {
    els.setupControlList.innerHTML = "";
    for (const control of controls) {
      const label = document.createElement("label");
      label.textContent = control.label;
      label.dataset.controlName = control.name;
      const input = document.createElement("input");
      input.type = "number";
      input.value = String(model.control_values?.[control.name] ?? control.value);
      input.min = String(control.min);
      input.max = String(control.max);
      input.step = String(control.step);
      input.dataset.controlName = control.name;
      input.dataset.controlSourcePath = control.source_path;
      input.dataset.testid = setupControlTestId(control.name);
      input.setAttribute("aria-label", `${control.label} 채비 조절값`);
      label.appendChild(input);
      els.setupControlList.appendChild(label);
    }
  }

  if (els.actionButtonList) {
    els.actionButtonList.innerHTML = "";
    for (const action of actions) {
      const button = document.createElement("button");
      button.type = "button";
      button.dataset.actionId = action.action_id;
      button.dataset.testid = `action-${action.action_id}`;
      button.title = `${action.label} 입력`;
      button.setAttribute("aria-label", `${action.label} 입력`);
      const glyph = document.createElement("span");
      glyph.setAttribute("aria-hidden", "true");
      glyph.textContent = action.glyph;
      const text = document.createElement("span");
      text.textContent = action.label;
      button.append(glyph, text);
      els.actionButtonList.appendChild(button);
    }
  }

  els.setupStatus.textContent = state.pendingRecipe?.project_id === state.projectId
    ? `setup recipe pending: ${recipeHash()}`
    : controls.length
      ? `setup: Rust/WASM 매김 ${controls.length}개 · 새 실행 recipe 대기 없음`
      : model.status === "error"
        ? "setup: authoring plan을 읽지 못했습니다"
        : "setup: 현재 프로젝트 매김 없음";
  const queuedAction = actions.find((action) => action.action_id === state.nextInput?.action_id);
  els.actionStatus.textContent = state.nextInput
    ? `action: next InputSnapshot ${queuedAction?.label ?? state.nextInput.intent}`
    : "action: 다음 마디 입력 없음";
}

function closeGajiBundleDialog() {
  pendingGajiBundle = null;
  els.gajiBundlePublish.disabled = true;
  els.gajiBundleDialog?.close?.();
}

function openGajiBundleDialog() {
  const file = activeFile();
  const source = currentVirtualProjectSource();
  if (!source || !file?.path?.endsWith(".ddn") || file.path === source.root_path || file.path === source.entry_path) {
    pushDiagnostic("E_GAJI_MODULE_SELECTION_INVALID", "뿌리·진입 파일이 아닌 DDN 모듈을 먼저 선택하세요.", "error");
    renderAll();
    return;
  }
  const leaf = file.path.split("/").at(-1)?.replace(/\.ddn$/u, "") || "내가지";
  els.gajiBundleId.value = leaf;
  els.gajiBundleVersion.value = "1.0.0";
  els.gajiBundleDescription.value = `${leaf} 재사용 모듈`;
  els.gajiBundleTags.value = "";
  els.gajiBundleSelected.textContent = `선택 모듈: ${file.path}`;
  els.gajiBundlePreview.textContent = "미리보기 전";
  els.gajiBundleStatus.textContent = "확인 전에는 발행하지 않습니다.";
  els.gajiBundlePublish.disabled = true;
  pendingGajiBundle = null;
  els.gajiBundleDialog?.showModal?.();
  els.gajiBundleId?.focus?.();
}

async function previewGajiBundle() {
  const source = currentVirtualProjectSource();
  const selectedPath = activeFile()?.path ?? "";
  const request = {
    schema: "ddn.gaji_extraction_plan.v1",
    source,
    selected_modules: [selectedPath],
    gaji_id: String(els.gajiBundleId.value || "").trim(),
    version: String(els.gajiBundleVersion.value || "").trim(),
    description: String(els.gajiBundleDescription.value || "").trim(),
    tags: String(els.gajiBundleTags.value || "").split(",").map((item) => item.trim()).filter(Boolean),
    profile: "내",
    origin_project_ref: `project:${currentProject().id}`,
  };
  const plan = await runtimeBridge.planGajiExtraction(request);
  pendingGajiBundle = { request, plan, sourceHash: plan.source_project_sha256 };
  els.gajiBundlePreview.textContent = [
    `가지: ${plan.gaji_id}@${plan.version} · 내 가지곳간`,
    `선택: ${plan.selected_modules.join(", ")}`,
    `자동 포함: ${plan.included_modules.filter((path) => !plan.selected_modules.includes(path)).join(", ") || "없음"}`,
    `공개 심볼: ${plan.public_symbols.map((item) => `${item.module_path}:${item.external_name}`).join(", ")}`,
    `외부 의존: ${Object.entries(plan.external_gaji_dependencies).map(([key, value]) => `${key}=${value}`).join(", ") || "없음"}`,
    `포함 파일: ${plan.files.map((file) => `${file.path} (${file.byte_length} bytes)`).join(", ")}`,
    `제외 파일: ${plan.excluded_files.join(", ") || "없음"}`,
    `content hash: ${plan.content_sha256}`,
    `계보: ${request.origin_project_ref}`,
  ].join("\n");
  els.gajiBundleStatus.textContent = "미리보기 완료 · 발행하면 immutable version으로 저장됩니다.";
  els.gajiBundlePublish.disabled = false;
}

async function publishGajiBundle() {
  if (!pendingGajiBundle) return;
  const currentHash = await runtimeBridge.projectSourceSha256(currentVirtualProjectSource());
  if (currentHash !== pendingGajiBundle.sourceHash) {
    throw new Error("E_GAJI_PUBLISH_SOURCE_STALE 미리보기 뒤 project source가 바뀌었습니다");
  }
  const artifact = await runtimeBridge.buildLocalGajiArtifact(pendingGajiBundle.request);
  await publishToLocalGotgan(runtimeBridge, artifact);
  pushDiagnostic("W_GAJI_PUBLISHED", `${artifact.gaji_id}@${artifact.version}을 내 가지곳간에 발행했습니다.`);
  els.gajiBundleStatus.textContent = `발행 완료: ${artifact.gaji_id}@${artifact.version}`;
  els.gajiBundlePublish.disabled = true;
  pendingGajiBundle = null;
}

function currentCapabilityIsViewOnly() {
  const role = state.capabilitySession?.role || state.serverProject.role || "";
  return Boolean((state.serverProject.projectId || state.capabilitySession?.project_id) && role === "view");
}

function selectedShelfProfiles() {
  return [...document.querySelectorAll("[data-testid='gaji-profile-filters'] input:checked")].map((node) => node.value);
}

async function refreshGajiShelf() {
  const result = await searchLocalGotgan(runtimeBridge, {
    query: els.gajiShelfSearch.value,
    profiles: selectedShelfProfiles(),
  });
  els.gajiShelfResults.replaceChildren();
  for (const row of result.rows ?? []) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "gaji-shelf-row";
    button.dataset.gajiPackageSha256 = row.package_sha256;
    button.setAttribute("role", "option");
    button.setAttribute("aria-label", `${row.gaji_id} ${row.version} 설치 미리보기`);
    for (const [tag, text] of [
      ["strong", `${row.gaji_id}@${row.version}`],
      ["span", `${row.profile} · ${row.description || "설명 없음"}`],
      ["small", `${row.public_symbols.join(", ")} · ${row.content_sha256.slice(0, 12)}`],
    ]) {
      const child = document.createElement(tag);
      child.textContent = text;
      button.append(child);
    }
    button.addEventListener("click", () => previewShelfInstall(row, button).catch(reportGajiShelfError));
    els.gajiShelfResults.append(button);
  }
  if (!(result.rows ?? []).length) els.gajiShelfResults.textContent = "검색 결과 없음";
  els.gajiInstallStatus.textContent = `검색 ${result.rows?.length ?? 0}개 · ${selectedShelfProfiles().join("/") || "선택 없음"}`;
}

function reportGajiShelfError(err) {
  pendingGajiInstall = null;
  els.gajiInstallApply.disabled = true;
  els.gajiInstallStatus.textContent = String(err?.message ?? err);
  pushDiagnostic("E_GAJI_SHELF", String(err?.message ?? err), "error");
}

async function previewShelfInstall(row, button) {
  const store = loadLocalGotganStore();
  const artifact = store.artifacts.find((item) => item.package_sha256 === row.package_sha256);
  if (!artifact) throw new Error("E_GAJI_SHELF_ARTIFACT_MISSING 선택한 가지 bytes가 없습니다");
  if (currentCapabilityIsViewOnly()) {
    pendingGajiInstall = null;
    els.gajiInstallPreview.textContent = [
      `${row.gaji_id}@${row.version} · ${row.profile} 가지곳간`,
      `공개 심볼: ${row.public_symbols.join(", ")}`,
      `content hash: ${row.content_sha256}`,
      `origin: ${artifact.provenance.origin_project_ref || "-"}`,
      "보기 capability에서는 project/vendor/lock을 변경하지 않습니다.",
    ].join("\n");
    els.gajiInstallStatus.textContent = "E_GAJI_VIEW_CAPABILITY_WRITE 보기 권한으로 가지를 설치할 수 없습니다.";
    els.gajiInstallApply.disabled = true;
    return;
  }
  const source = currentVirtualProjectSource();
  if (!source || !nativeProjects.some((item) => item.id === state.projectId)) {
    throw new Error("E_GAJI_INSTALL_PROJECT_REQUIRED 네이티브 프로젝트를 먼저 여세요");
  }
  const alias = String(els.gajiInstallAlias.value || artifact.gaji_id).trim();
  els.gajiInstallAlias.value = alias;
  const installedPath = state.projectGraph?.graph?.gaji_aliases?.[alias] || null;
  const installedId = installedPath?.replace(/^\.\//, "").split("/")[1] || null;
  const installedMetadata = source.files.find((file) => file.path === `vendor/${installedId}/artifact.detjson`);
  const installedArtifact = installedMetadata ? JSON.parse(installedMetadata.utf8_text) : null;
  const kind = installedPath ? "update" : "install";
  const sourceHash = await runtimeBridge.projectSourceSha256(source);
  const request = {
    schema: "ddn.gaji_lifecycle_plan.v1",
    source,
    expected_source_sha256: sourceHash,
    expected_lock_sha256: null,
    operation: { kind, alias, artifact },
  };
  const plan = await runtimeBridge.planGajiLifecycle(request);
  pendingGajiInstall = { row, artifact, request, plan };
  document.querySelectorAll(".gaji-shelf-row").forEach((node) => node.classList.toggle("active", node === button));
  els.gajiInstallPreview.textContent = [
    `${row.gaji_id}@${row.version} · ${row.profile} 가지곳간`,
    `alias: ${alias}`,
    `공개 심볼: ${row.public_symbols.join(", ")}`,
    `dependency: ${Object.entries(artifact.dependencies).map(([key, value]) => `${key}@${value}`).join(", ") || "없음"}`,
    `origin: ${artifact.provenance.origin_project_ref || "-"} · ${artifact.provenance.relation}`,
    `원본 가지: ${artifact.provenance.origin_gaji || "없음"}`,
    `vendor 변화: ${plan.affected_files.join(", ")}`,
    ...(plan.version_diff ? [
      `버전: ${plan.version_diff.from_version || "없음"} → ${plan.version_diff.to_version || "없음"}`,
      `파일: +${plan.version_diff.added_files.join(",") || "없음"} / -${plan.version_diff.removed_files.join(",") || "없음"} / 변경 ${plan.version_diff.changed_files.join(",") || "없음"}`,
      `API: +${plan.version_diff.added_public_symbols.join(",") || "없음"} / -${plan.version_diff.removed_public_symbols.join(",") || "없음"}`,
      `의존성 변경: ${plan.version_diff.dependency_changed ? "예" : "아니오"} · 위험: ${plan.version_diff.risky ? "있음" : "없음"}`,
    ] : []),
    `lock: ${plan.before_lock_sha256 || "없음"} → ${plan.after_lock_sha256 || "없음"}`,
    `project graph는 적용 전 Rust core에서 재검증됨`,
  ].join("\n");
  const rollback = installedArtifact && installedArtifact.version !== artifact.version && artifact.version < installedArtifact.version;
  els.gajiInstallApply.textContent = rollback ? "보관 버전으로 되돌리기" : (kind === "update" ? "원자적으로 갱신" : "원자적으로 설치");
  els.gajiInstallStatus.textContent = currentCapabilityIsViewOnly() ? "보기 전용 링크에서는 설치할 수 없습니다." : `${rollback ? "되돌리기" : kind === "update" ? "갱신" : "설치"} 미리보기 완료`;
  els.gajiInstallApply.disabled = currentCapabilityIsViewOnly();
  els.gajiInstallRemove.disabled = currentCapabilityIsViewOnly() || !installedPath;
  els.gajiRemixStart.disabled = currentCapabilityIsViewOnly() || !installedPath;
}

async function applyShelfInstall() {
  if (!pendingGajiInstall) return;
  if (currentCapabilityIsViewOnly()) throw new Error("E_GAJI_VIEW_CAPABILITY_WRITE 보기 권한으로 가지를 설치할 수 없습니다");
  const source = currentVirtualProjectSource();
  const sourceHash = await runtimeBridge.projectSourceSha256(source);
  const request = { ...pendingGajiInstall.request, source, expected_source_sha256: sourceHash };
  const plan = await runtimeBridge.planGajiLifecycle(request);
  applyVirtualProjectSource(plan.project_source);
  pendingGajiInstall = null;
  els.gajiInstallApply.disabled = true;
  els.gajiInstallStatus.textContent = `${plan.alias} ${plan.operation === "install" ? "설치" : "갱신"} 완료 · lock ${plan.after_lock_sha256}`;
  pushDiagnostic("W_GAJI_INSTALLED", `${plan.alias} 가지를 project graph와 lock에 원자 ${plan.operation === "install" ? "설치" : "갱신"}했습니다.`);
  await refreshProjectGraph();
}

async function removeShelfInstall() {
  if (!pendingGajiInstall) return;
  if (currentCapabilityIsViewOnly()) throw new Error("E_GAJI_VIEW_CAPABILITY_WRITE 보기 권한으로 가지를 제거할 수 없습니다");
  const source = currentVirtualProjectSource();
  const sourceHash = await runtimeBridge.projectSourceSha256(source);
  const request = {
    schema: "ddn.gaji_lifecycle_plan.v1", source, expected_source_sha256: sourceHash, expected_lock_sha256: null,
    operation: { kind: "remove", alias: String(els.gajiInstallAlias.value).trim() },
  };
  const plan = await runtimeBridge.planGajiLifecycle(request);
  applyVirtualProjectSource(plan.project_source);
  pendingGajiInstall = null;
  els.gajiInstallApply.disabled = true;
  els.gajiInstallRemove.disabled = true;
  els.gajiInstallStatus.textContent = `${plan.alias} 제거 완료`;
  pushDiagnostic("W_GAJI_REMOVED", `${plan.alias} 가지를 project graph에서 원자 제거했습니다.`);
  await refreshProjectGraph();
}

function startShelfRemix() {
  if (!pendingGajiInstall?.artifact) return;
  const artifact = pendingGajiInstall.artifact;
  const primaryPath = artifact.provenance.extraction_modules[0];
  const primary = artifact.files.find((file) => file.path === `ddn/${primaryPath}`);
  if (!primary) throw new Error("E_GAJI_REMIX_SOURCE_MISSING 리믹스할 주 모듈 bytes가 없습니다");
  els.gajiRemixId.value = `${artifact.gaji_id}-내버전`;
  els.gajiRemixVersion.value = "1.0.0";
  els.gajiRemixSource.value = primary.utf8_text;
  els.gajiRemixEditor.hidden = false;
  els.gajiInstallStatus.textContent = `${artifact.gaji_id}@${artifact.version} 원본을 보존한 리믹스 편집 준비`;
}

async function publishShelfRemix() {
  if (!pendingGajiInstall?.artifact) return;
  const origin = pendingGajiInstall.artifact;
  const primaryPath = origin.provenance.extraction_modules[0];
  const files = origin.files.filter((file) => file.path.startsWith("ddn/")).map((file) => ({
    path: file.path.slice(4), role: "ddn_source", utf8_text: file.path === `ddn/${primaryPath}` ? els.gajiRemixSource.value : file.utf8_text,
  }));
  files.push({
    path: "뿌리.ddn", role: "root",
    utf8_text: `프로젝트 { 이름: "${els.gajiRemixId.value}". 첫글: "./app/main.ddn". 목표 { 앱: "./app/main.ddn". } 모듈길 { 로컬: "./lib". } }.`,
  });
  files.push({ path: "app/main.ddn", role: "ddn_source", utf8_text: '"리믹스 묶기" 보여주기.' });
  const request = {
    schema: "ddn.gaji_extraction_plan.v1",
    source: { schema: "ddn.virtual_project_source.v1", kind: "seamgrim.local_project_tree.v0", root_path: "뿌리.ddn", entry_path: "app/main.ddn", files },
    selected_modules: [...origin.provenance.extraction_modules],
    gaji_id: String(els.gajiRemixId.value).trim(), version: String(els.gajiRemixVersion.value).trim(),
    description: `${origin.description} 리믹스`, tags: [...origin.tags, "리믹스"], profile: "내",
    origin_project_ref: origin.provenance.origin_project_ref,
    origin_gaji: `${origin.gaji_id}@${origin.version}`, relation: "remix",
  };
  const remix = await runtimeBridge.buildLocalGajiArtifact(request);
  await publishToLocalGotgan(runtimeBridge, remix);
  const originalApi = origin.public_symbols.map((item) => item.external_name).sort().join(", ");
  const remixApi = remix.public_symbols.map((item) => item.external_name).sort().join(", ");
  els.gajiInstallPreview.textContent = [
    `원본 ${origin.gaji_id}@${origin.version}: ${origin.content_sha256}`,
    `리믹스 ${remix.gaji_id}@${remix.version}: ${remix.content_sha256}`,
    `API 원본: ${originalApi || "없음"}`,
    `API 리믹스: ${remixApi || "없음"}`,
    `계보: ${remix.provenance.origin_gaji} · ${remix.provenance.relation}`,
  ].join("\n");
  els.gajiRemixEditor.hidden = true;
  await refreshGajiShelf();
  els.gajiInstallStatus.textContent = `리믹스 발행 완료: ${remix.gaji_id}@${remix.version}`;
}

async function openGajiShelf() {
  pendingGajiInstall = null;
  els.gajiInstallApply.disabled = true;
  els.gajiInstallRemove.disabled = true;
  els.gajiRemixStart.disabled = true;
  els.gajiRemixEditor.hidden = true;
  els.gajiInstallPreview.textContent = "설치할 가지를 선택하세요.";
  els.gajiShelfDialog?.showModal?.();
  await refreshGajiShelf();
  els.gajiShelfSearch?.focus?.();
}

function exportSelectedGajiArtifact() {
  const artifact = pendingGajiInstall?.artifact;
  if (!artifact) throw new Error("E_GAJI_EXPORT_SELECTION_REQUIRED 내보낼 가지를 먼저 선택하세요");
  triggerPortableDownload({
    jsonText: exportLocalGotganArtifact(artifact),
    filename: `${artifact.gaji_id}-${artifact.version}.gaji.detjson`,
  });
  els.gajiInstallStatus.textContent = `artifact 내보내기 완료: ${artifact.gaji_id}@${artifact.version}`;
}

async function importGajiArtifactFile(file) {
  if (!file) return;
  const text = await hostBridge.readTextFile(file);
  const parsed = JSON.parse(text);
  await importLocalGotganArtifact(runtimeBridge, text);
  await refreshGajiShelf();
  els.gajiInstallStatus.textContent = `artifact 가져오기 완료: ${parsed.gaji_id}@${parsed.version}`;
}

function currentVirtualProjectSourceHash(project = currentProject()) {
  const source = currentVirtualProjectSource(project);
  return virtualProjectSourceHash(source);
}

function virtualProjectSourceHash(source) {
  if (!source) return "";
  return `candidate:fnv1a32:virtual_project_source:${stableHash(stableCanonicalJson(source))}`;
}

function emptyProjectLockTrust() {
  return {
    schema: "seamgrim.workbench.project_lock_trust.v1",
    verified_source_hash: "",
    verified_lock_sha256: "",
    local_non_lock_edit_after_verified: false,
  };
}

function resetProjectExecutionState({ keepImportedRecord = true } = {}) {
  state.projectExecution = {
    importedRecord: keepImportedRecord ? state.projectExecution?.importedRecord ?? null : null,
    current: null,
    previousSuccess: state.projectExecution?.previousSuccess ?? null,
    failure: null,
    lockManuallyEdited: state.projectExecution?.lockManuallyEdited ?? false,
    lockTrust: emptyProjectLockTrust(),
  };
}

function seedImportedProjectExecutionRecord(project = currentProject()) {
  const evidence = importedProjectRunEvidenceFromProject(project);
  state.projectExecution = {
    importedRecord: evidence
      ? {
          schema: "seamgrim.workbench.imported_project_execution_record.v1",
          state: "imported_record",
          evidence,
          source_hash: currentVirtualProjectSourceHash(project),
        }
      : null,
    current: null,
    previousSuccess: state.projectExecution?.previousSuccess ?? null,
    failure: null,
    lockManuallyEdited: false,
    lockTrust: emptyProjectLockTrust(),
  };
}

function markCurrentProjectExecutionStale(reason = "source_edit") {
  const current = state.projectExecution?.current;
  if (!current) return;
  state.projectExecution.previousSuccess = {
    ...current,
    state: "previous_success",
    stale_reason: reason,
  };
  state.projectExecution.current = null;
}

function outputRowsFromWasmState(wasmState = {}) {
  const outputLog = wasmState?.resources?.value_json?.output_log;
  if (Array.isArray(outputLog) && outputLog.length) {
    return outputLog.map((row) => String(row?.text ?? row?.value ?? ""));
  }
  if (Array.isArray(wasmState?.row)) {
    return wasmState.row.map((value) => String(value ?? ""));
  }
  return [];
}

function observationRowsFromWasmState(wasmState = {}, outputRows = []) {
  const channels = Array.isArray(wasmState?.channels) ? wasmState.channels : [];
  return outputRows.map((value, index) => {
    const channel = channels[index] && typeof channels[index] === "object" ? channels[index] : {};
    return {
      index,
      observation_id: `project.obs.${index + 1}`,
      name: String(channel.key ?? `output_${index + 1}`),
      value_text: String(value ?? ""),
      unit: "",
      committed_madi: readMadi(wasmState, index === 0 ? 0 : index),
      target_path: "",
      runtime_state_hash: readStateHash(wasmState, ""),
      source: "workbench_current_file_tree_vm",
      state_hash_participation: false,
    };
  });
}

async function buildProjectObservationTraceFromVm({
  prepared,
  wasmState,
  outputRows,
  observationRows,
  vmLifecycle = "updateLogic+reset+runTicks(1)",
} = {}) {
  const trace = {
    schema: "ddn.local_project.observation_trace.v1",
    source: "workbench_current_file_tree_vm",
    row_count: observationRows.length,
    rows: observationRows.map((row) => ({
      ...row,
      target_path: String(prepared?.target_path ?? row.target_path ?? ""),
    })),
    determinism: {
      source: "workbench-current-file-tree",
      frontdoor: "wasm_project_prepare_link_json",
      vm_lifecycle: vmLifecycle,
      requested_ticks: 1,
      committed_madi: readMadi(wasmState, 0),
      runtime_state_hash: readStateHash(wasmState, ""),
      project_graph_sha256: String(prepared?.project_graph?.project_graph_sha256 ?? ""),
      linked_execution_source_sha256: String(prepared?.linked_execution_source_sha256 ?? ""),
      prepare_link_sha256: String(prepared?.prepare_link_sha256 ?? ""),
      output_rows: outputRows,
      state_hash_formula_change: false,
    },
  };
  const traceSha = await sha256HexUtf8(stableCanonicalJson(trace));
  return {
    ...trace,
    trace_sha256: traceSha ? `sha256:${traceSha}` : `candidate:fnv1a32:trace:${stableHash(stableCanonicalJson(trace))}`,
  };
}

function buildProjectRunLineageFromCurrentExecution({
  prepared,
  run,
  frame,
  boundedStateSha256,
  vmLifecycle = "updateLogic+reset+runTicks(1)",
} = {}) {
  const request = {
    frontdoor: "wasm_project_prepare_link_json",
    vm_lifecycle: vmLifecycle,
    requested_ticks: 1,
    target: String(prepared?.target ?? "앱"),
    target_path: String(prepared?.target_path ?? ""),
    run_id: String(run?.run_id ?? ""),
  };
  const runRequestHash = `candidate:fnv1a32:project_run_request:${stableHash(stableCanonicalJson(request))}`;
  const lineage = {
    schema: "seamgrim.local_project_run_lineage.v0",
    project_graph_hash: String(prepared?.project_graph?.project_graph_sha256 ?? ""),
    lock_hash: String(prepared?.verified_lock?.lock_sha256 ?? ""),
    linked_source_hash: String(prepared?.linked_execution_source_sha256 ?? ""),
    run_request_hash: runRequestHash,
    parent_run_id: String(run?.parent_run_id ?? ""),
    branch_madi: run?.parent_madi === null || run?.parent_madi === undefined ? null : Number(run.parent_madi),
    branch_state_hash: String(run?.parent_state_hash ?? ""),
    final_state_hash: String(frame?.state_hash ?? ""),
    view_artifact_hash: "",
    created_revision: boundedStateSha256,
  };
  return {
    ...lineage,
    lineage_hash: `candidate:fnv1a32:project_run_lineage:${stableHash(stableCanonicalJson(lineage))}`,
  };
}

function projectExecutionPlanFromPrepared(prepared = {}, projectSourceHash = "") {
  return {
    schema: "seamgrim.workbench.project_execution_plan.v1",
    source_hash: String(projectSourceHash ?? ""),
    frontdoor: "wasm_project_prepare_link_json",
    target: String(prepared?.target ?? "앱"),
    target_path: String(prepared?.target_path ?? ""),
    project_graph: {
      project_graph_sha256: String(prepared?.project_graph?.project_graph_sha256 ?? ""),
    },
    verified_lock: prepared?.verified_lock
      ? {
          lock_sha256: String(prepared.verified_lock.lock_sha256 ?? ""),
        }
      : null,
    linked_execution_source: String(prepared?.linked_execution_source ?? ""),
    linked_execution_source_sha256: String(prepared?.linked_execution_source_sha256 ?? ""),
    prepare_link_sha256: String(prepared?.prepare_link_sha256 ?? ""),
    execution_mode_decision: requireParsedExecutionModeDecision(
      prepared?.runtime_execution_envelope?.execution_mode_decision,
    ),
    state_hash_formula_change: false,
  };
}

function requireParsedExecutionModeDecision(decision = null) {
  const parsed = decision && typeof decision === "object" ? decision : null;
  const mode = String(parsed?.mode ?? "").trim();
  if (
    !parsed
    || String(parsed.authority ?? "") !== "parsed_program"
    || !["oneshot", "live"].includes(mode)
  ) {
    throw new Error("E_EXECUTION_MODE_DECISION_MISSING: Rust parsed_program 실행 모드 판정이 없습니다");
  }
  return { ...parsed, mode };
}

function recordVerifiedProjectLockTrust(projectSourceHash = "", projectExecutionPlan = null) {
  const lockSha = String(projectExecutionPlan?.verified_lock?.lock_sha256 ?? "").trim();
  if (!lockSha) {
    state.projectExecution.lockTrust = emptyProjectLockTrust();
    return;
  }
  state.projectExecution.lockTrust = {
    schema: "seamgrim.workbench.project_lock_trust.v1",
    verified_source_hash: String(projectSourceHash ?? ""),
    verified_lock_sha256: lockSha,
    local_non_lock_edit_after_verified: false,
  };
  state.projectExecution.lockManuallyEdited = false;
}

async function buildCurrentProjectRunEvidence({
  prepared,
  run,
  frame,
  wasmState,
  vmLifecycle = "updateLogic+reset+runTicks(1)",
} = {}) {
  const outputRows = outputRowsFromWasmState(wasmState);
  const observationRows = observationRowsFromWasmState(wasmState, outputRows);
  const trace = await buildProjectObservationTraceFromVm({
    prepared,
    wasmState,
    outputRows,
    observationRows,
    vmLifecycle,
  });
  const boundedInput = {
    schema: "ddn.local_project_run_summary.bounded_state.v1",
    state_hash: readStateHash(wasmState, ""),
    output_rows: outputRows,
  };
  const boundedSha = await sha256HexUtf8(stableCanonicalJson(boundedInput));
  const boundedStateSha256 = boundedSha
    ? `sha256:${boundedSha}`
    : `candidate:fnv1a32:bounded_state:${stableHash(stableCanonicalJson(boundedInput))}`;
  return {
    schema: "seamgrim.approved_workbench.local_project_run_evidence.v1",
    frontdoor: "wasm_project_prepare_link_json",
    runtime_lifecycle: "workbench_vm_update_reset_tick",
    bounded_state_sha256: boundedStateSha256,
    runtime_state_hash: readStateHash(wasmState, ""),
    summary_sha256: String(prepared?.prepare_link_sha256 ?? ""),
    trace_sha256: trace.trace_sha256,
    run_lineage: buildProjectRunLineageFromCurrentExecution({
      prepared,
      run,
      frame,
      boundedStateSha256,
      vmLifecycle,
    }),
    output_rows: outputRows,
    observation_rows: trace.rows,
    project_observation_trace: trace,
    execution_preparation: {
      schema: "ddn.local_project.execution_preparation.v1",
      source: "workbench_current_file_tree",
      frontdoor: "wasm_project_prepare_link_json",
      prepare_link_sha256: String(prepared?.prepare_link_sha256 ?? ""),
      project_graph_sha256: String(prepared?.project_graph?.project_graph_sha256 ?? ""),
      lock_sha256: String(prepared?.verified_lock?.lock_sha256 ?? ""),
      linked_execution_source_sha256: String(prepared?.linked_execution_source_sha256 ?? ""),
      target: String(prepared?.target ?? "앱"),
      target_path: String(prepared?.target_path ?? ""),
      state_hash_formula_change: false,
    },
  };
}

function projectDiagnosticFromError(err, fallbackCode = "E_PROJECT_RUN_FAILED") {
  const message = String(err?.message ?? err ?? "");
  const match = message.match(/\b(E_[A-Z0-9_]+)\b/u);
  return {
    code: String(err?.code ?? match?.[1] ?? fallbackCode),
    message: message || fallbackCode,
    severity: "error",
  };
}

function recipeHash() {
  const project = currentProject();
  const sourceHash = currentVirtualProjectSourceHash(project) || `candidate:fnv1a32:${stableHash(activeRuntimeSourceText(project))}`;
  const payload = JSON.stringify({
    project_id: state.projectId,
    source_hash: sourceHash,
    recipe_version: state.recipeVersion,
    setup: state.pendingRecipe ?? {},
  });
  return `candidate:fnv1a32:${stableHash(payload)}`;
}

function buildRunId(prefix = "run") {
  state.runSeq += 1;
  return `${prefix}_${String(state.runSeq).padStart(3, "0")}`;
}

function readMadi(wasmState, fallback = 0) {
  const candidates = [
    wasmState?.tick_id,
    wasmState?.madi,
    wasmState?.tick,
    wasmState?.state?.tick_id,
  ];
  for (const candidate of candidates) {
    const value = Number(candidate);
    if (Number.isFinite(value)) return Math.max(0, Math.trunc(value));
  }
  return fallback;
}

function readStateHash(wasmState, fallback = "-") {
  const value = wasmState?.state_hash ?? wasmState?.stateHash ?? wasmState?.state?.state_hash;
  const text = String(value ?? "").trim();
  return text || fallback;
}

function pushDiagnostic(code, message, severity = "warning") {
  state.diagnostics = [
    {
      code,
      message,
      severity,
      at: new Date().toISOString(),
    },
    ...state.diagnostics,
  ].slice(0, 8);
  renderDiagnostics();
}

function clearDiagnostics() {
  state.diagnostics = [];
  renderDiagnostics();
}

function resizeCanvasToDisplaySize(canvas) {
  const rect = canvas.getBoundingClientRect();
  const width = Math.max(320, Math.floor(rect.width || 640));
  const height = Math.max(240, Math.floor(rect.height || 360));
  if (canvas.width !== width || canvas.height !== height) {
    canvas.width = width;
    canvas.height = height;
  }
  return { width, height };
}

function drawProjectRunEvidence(ctx, width, height, evidence, semanticPayload) {
  const margin = Math.max(28, Math.min(width, height) * 0.09);
  ctx.fillStyle = "#eef5ed";
  ctx.strokeStyle = "#64748b";
  ctx.lineWidth = 1.5;
  ctx.fillRect(margin, margin, width - margin * 2, height - margin * 2);
  ctx.strokeRect(margin, margin, width - margin * 2, height - margin * 2);
  ctx.fillStyle = "#31533e";
  ctx.font = "700 15px Segoe UI, sans-serif";
  ctx.fillText("보관된 실행 증거", margin + 18, margin + 30);
  ctx.font = "600 13px Segoe UI, sans-serif";
  ctx.fillText(`state ${evidence.bounded_state_sha256.slice(0, 16) || "-"}`, margin + 18, margin + 58);
  ctx.fillText(`trace ${evidence.trace_sha256.slice(0, 16) || "-"}`, margin + 18, margin + 80);
  ctx.fillText(`outputs ${evidence.output_rows.length}개 · 의미 채널이 없으면 그래프로 추정하지 않음`, margin + 18, margin + 102);
  return {
    schema: "seamgrim.approved_workbench.bogae_view_artifact.v1",
    source: "local_project_run_evidence",
    trace_sha256: evidence.trace_sha256,
    bounded_state_sha256: evidence.bounded_state_sha256,
    run_lineage_hash: evidence.run_lineage?.lineage_hash ?? "",
    output_rows: evidence.output_rows,
    committed_frame: semanticPayload.committed_frame,
    semantic_payload_hash: semanticPayload.semantic_payload_hash,
    view_binding: semanticPayload.view_binding,
    view_config: semanticPayload.view_config,
  };
}

function buildCommittedFrameCanonicalViewPayloads(run, frame) {
  if (!frame) return null;
  const authorityInputs = extractCanonicalViewAuthorityInputsFromState(frame.wasm_state);
  authorityInputs.identity = {
    ...authorityInputs.identity,
    state_hash: String(frame.state_hash ?? authorityInputs.identity?.state_hash ?? ""),
    source_hash: String(frame.source_hash ?? run?.source_hash ?? authorityInputs.identity?.source_hash ?? ""),
    tick_id: Number.isFinite(Number(frame.madi))
      ? Math.trunc(Number(frame.madi))
      : authorityInputs.identity?.tick_id ?? null,
  };
  return buildCanonicalViewPayloadSet(authorityInputs);
}

function buildCommittedCanonicalViewHistory(run, activeFrame, family) {
  if (!run || !Array.isArray(run.frames) || !activeFrame) return [];
  const activeFrameId = Number(activeFrame.frame_id ?? Number.POSITIVE_INFINITY);
  const canonicalKey = `workbench_${String(family ?? "line")}`;
  return run.frames
    .filter((frame) => Number(frame?.frame_id ?? -1) <= activeFrameId)
    .map((frame) => {
      const payloads = buildCommittedFrameCanonicalViewPayloads(run, frame);
      return {
        frame_id: Number(frame.frame_id ?? -1),
        madi: Number(frame.madi ?? 0),
        state_hash: String(frame.state_hash ?? ""),
        canonical_views: { [canonicalKey]: payloads?.[canonicalKey] ?? null },
      };
    });
}

function drawPreview() {
  const project = currentProject();
  const run = activeRun();
  const frame = activeFrame();
  state.viewWorkspace = reconcileViewWorkspace(state.viewWorkspace, project, frame);
  const primaryInstance = primaryViewInstance(state.viewWorkspace);
  const overlayInstances = overlayViewInstances(state.viewWorkspace);
  const canonicalViewPayloads = buildCommittedFrameCanonicalViewPayloads(run, frame);
  const semanticPayload = buildCommittedSemanticViewPayload({
    project,
    run,
    frame,
    viewConfig: {
      primary_view: project.primaryView,
      role: "primary",
      mode: state.mode,
      view_instance_id: primaryInstance?.view_instance_id ?? "view_primary_1",
      overlay_instance_ids: overlayInstances.map((instance) => instance.view_instance_id),
      overlay_enabled: overlayInstances.length > 0,
    },
    canonicalViewPayloads,
    canonicalViewHistory: buildCommittedCanonicalViewHistory(run, frame, project.primaryView),
  });
  state.semanticViewPayload = semanticPayload;
  const canvas = els.canvas;
  const ctx = canvas.getContext("2d", { willReadFrequently: true });
  const { width, height } = resizeCanvasToDisplaySize(canvas);
  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = "#f8fbf7";
  ctx.fillRect(0, 0, width, height);
  const runEvidence = localProjectRunEvidenceFromProject(project);
  let viewArtifact = null;
  let renderModel = null;
  if (semanticPayload.committed_frame) {
    renderModel = renderCommittedSemanticView(ctx, width, height, semanticPayload);
  } else if (runEvidence) {
    viewArtifact = drawProjectRunEvidence(ctx, width, height, runEvidence, semanticPayload);
    renderModel = {
      schema: "seamgrim.workbench.semantic_render_model.v1",
      family: project.primaryView,
      status: "archived_evidence_only",
      data_source: "local_project_run_evidence",
      committed_frame: null,
      semantic_payload_hash: semanticPayload.semantic_payload_hash,
      role: "primary",
      labels: [],
    };
  } else {
    renderModel = renderCommittedSemanticView(ctx, width, height, semanticPayload);
  }
  state.semanticRenderModel = renderModel;
  ctx.fillStyle = "#31533e";
  ctx.font = "600 13px Segoe UI, sans-serif";
  ctx.fillText(project.id, 18, 24);
  if (!viewArtifact) {
    viewArtifact = {
      schema: "seamgrim.approved_workbench.bogae_view_artifact.v1",
      source: semanticPayload.committed_frame ? "committed_semantic_payload" : "static_project_preview",
      project_id: project.id,
      committed_frame: semanticPayload.committed_frame,
      semantic_payload_hash: semanticPayload.semantic_payload_hash,
      view_binding: semanticPayload.view_binding,
      view_config: semanticPayload.view_config,
      render_model: renderModel,
      view_instances: state.viewWorkspace.instances.map((instance) => ({
        view_instance_id: instance.view_instance_id,
        role: instance.role,
        target_view_instance_id: instance.target_view_instance_id,
      })),
    };
  }
  const viewArtifactHash = `candidate:fnv1a32:bogae_view:${stableHash(stableCanonicalJson(viewArtifact))}`;
  canvas.dataset.projectRunBound = runEvidence ? "true" : "false";
  canvas.dataset.projectRunTraceSha256 = runEvidence?.trace_sha256 ?? "";
  canvas.dataset.projectRunLineageHash = runEvidence?.run_lineage?.lineage_hash ?? "";
  canvas.dataset.committedFrameBound = semanticPayload.committed_frame ? "true" : "false";
  canvas.dataset.committedRunId = semanticPayload.committed_frame?.run_id ?? "";
  canvas.dataset.committedFrameId = String(semanticPayload.committed_frame?.frame_id ?? "");
  canvas.dataset.committedMadi = String(semanticPayload.committed_frame?.madi ?? "");
  canvas.dataset.committedStateHash = semanticPayload.committed_frame?.state_hash ?? "";
  canvas.dataset.semanticPayloadHash = semanticPayload.semantic_payload_hash;
  canvas.dataset.canonicalConsolePayloadStatus = canonicalViewPayloads?.console?.status ?? "";
  canvas.dataset.canonicalConsolePayloadHash = canonicalViewPayloads?.console?.candidate_payload_hash ?? "";
  canvas.dataset.canonicalGraphPayloadStatus = canonicalViewPayloads?.graph?.status ?? "";
  canvas.dataset.canonicalGraphPayloadHash = canonicalViewPayloads?.graph?.candidate_payload_hash ?? "";
  canvas.dataset.canonicalConsolePayloadJson = canonicalViewPayloads?.console
    ? stableSemanticJson(canonicalViewPayloads.console)
    : "";
  canvas.dataset.canonicalGraphPayloadJson = canonicalViewPayloads?.graph
    ? stableSemanticJson(canonicalViewPayloads.graph)
    : "";
  canvas.dataset.viewBindingResolution = semanticPayload.view_binding.resolution;
  canvas.dataset.rendererFamily = renderModel?.family ?? "";
  canvas.dataset.rendererStatus = renderModel?.status ?? "";
  canvas.dataset.rendererDataSource = renderModel?.data_source ?? "";
  canvas.dataset.rendererTrajectoryLength = String(renderModel?.trajectory?.length ?? renderModel?.points?.length ?? 0);
  canvas.dataset.rendererCurrentTheta = String(renderModel?.current?.theta ?? "");
  canvas.dataset.rendererCurrentX = String(renderModel?.current?.x ?? "");
  canvas.dataset.rendererCurrentY = String(renderModel?.current?.y ?? "");
  canvas.dataset.rendererTick = String(renderModel?.tick ?? "");
  canvas.dataset.canvasSignature = viewArtifactHash;
  canvas.dataset.viewArtifactHash = viewArtifactHash;
  globalThis.__SEAMGRIM_WORKBENCH_CANONICAL_VIEW_PAYLOADS__ = canonicalViewPayloads;
}

function renderMode() {
  els.layout.dataset.mode = state.mode;
  document.querySelectorAll("[data-mode]").forEach((button) => {
    button.classList.toggle("active", button.dataset.mode === state.mode);
    button.setAttribute("aria-selected", button.dataset.mode === state.mode ? "true" : "false");
  });
  const labels = {
    "ddn-main": "DDN 60 / 보개 40",
    "bogae-main": "DDN 40 / 보개 60",
    "bogae-full": "보개 full / 원문 접근 유지",
  };
  els.ratioLabel.textContent = labels[state.mode] ?? labels["ddn-main"];
  drawPreview();
}

function buildViewInstanceSemanticPayload(project, instance) {
  const overlays = instance.role === "primary" ? overlayViewInstances(state.viewWorkspace) : [];
  const run = activeRun();
  const frame = activeFrame();
  return buildCommittedSemanticViewPayload({
    project,
    run,
    frame,
    viewConfig: {
      primary_view: instance.family ?? project.primaryView,
      role: instance.role,
      mode: state.mode,
      view_instance_id: instance.view_instance_id,
      target_view_instance_id: instance.target_view_instance_id,
      overlay_instance_ids: overlays.map((overlay) => overlay.view_instance_id),
      overlay_enabled: overlays.length > 0,
      focus_target: instance.target,
    },
    canonicalViewPayloads: buildCommittedFrameCanonicalViewPayloads(run, frame),
    canonicalViewHistory: buildCommittedCanonicalViewHistory(run, frame, instance.family ?? project.primaryView),
  });
}

function setViewActionState(button, { visible, enabled, reason = "", active = false, pressed = null }) {
  if (!button) return;
  if (!button.dataset.enabledTitle) button.dataset.enabledTitle = button.title || "";
  button.hidden = !visible;
  button.disabled = !enabled;
  button.dataset.disabledReason = enabled ? "" : reason;
  button.title = enabled ? button.dataset.enabledTitle : reason;
  button.classList.toggle("active", active);
  if (pressed !== null) button.setAttribute("aria-pressed", pressed ? "true" : "false");
}

function renderSideViewInstances(project, instances) {
  if (!els.sideViewList) return;
  els.sideViewList.innerHTML = instances.map((instance, index) => {
    const roleLabel = instance.role === "magnifier" ? "돋보기" : `곁보기 ${index + 1}`;
    const targetLabel = instance.target?.target_id ? `target ${instance.target.target_id}` : "committed observations";
    return `<section class="side-view-instance" data-view-instance-id="${escapeHtml(instance.view_instance_id)}" data-view-instance-role="${escapeHtml(instance.role)}" data-temporary="${instance.temporary ? "true" : "false"}">
      <div class="side-view-instance-header"><strong>${escapeHtml(roleLabel)}</strong><button type="button" class="panel-action" data-view-instance-close="${escapeHtml(instance.view_instance_id)}" title="이 보기 닫기" aria-label="${escapeHtml(roleLabel)} 닫기">닫기</button></div>
      <canvas width="360" height="220" data-view-instance-canvas="${escapeHtml(instance.view_instance_id)}" aria-label="${escapeHtml(roleLabel)} canvas"></canvas>
      <span class="side-view-instance-meta">${escapeHtml(targetLabel)} · ${escapeHtml(instance.view_instance_id)}</span>
    </section>`;
  }).join("");
  instances.forEach((instance) => {
    const canvas = els.sideViewList.querySelector(`[data-view-instance-canvas='${instance.view_instance_id}']`);
    if (!canvas) return;
    const ctx = canvas.getContext("2d", { willReadFrequently: true });
    const { width, height } = resizeCanvasToDisplaySize(canvas);
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = "#f8fbf7";
    ctx.fillRect(0, 0, width, height);
    const payload = buildViewInstanceSemanticPayload(project, instance);
    const model = renderCommittedSemanticView(ctx, width, height, payload);
    canvas.dataset.viewInstanceId = instance.view_instance_id;
    canvas.dataset.viewInstanceRole = instance.role;
    canvas.dataset.targetViewInstanceId = instance.target_view_instance_id;
    canvas.dataset.committedStateHash = payload.committed_frame?.state_hash ?? "";
    canvas.dataset.semanticPayloadHash = payload.semantic_payload_hash;
    canvas.dataset.rendererStatus = model.status;
  });
}

function renderViewPolicy(project) {
  state.viewWorkspace = reconcileViewWorkspace(state.viewWorkspace, project, activeFrame());
  const policy = project.viewPolicy ?? {};
  const capabilities = viewRoleCapabilities(project, state.semanticViewPayload, state.semanticRenderModel);
  const sideInstances = sideViewInstances(state.viewWorkspace);
  const overlays = overlayViewInstances(state.viewWorkspace);
  const selectedTarget = state.viewWorkspace.selected_target;
  const primary = primaryViewInstance(state.viewWorkspace);
  setViewActionState(els.viewPrimary, {
    visible: true,
    enabled: true,
    active: state.viewWorkspace.active_view_instance_id === primary?.view_instance_id,
  });
  els.viewPrimary.textContent = "으뜸 1";
  setViewActionState(els.viewSide, {
    visible: capabilities.side.supported || sideInstances.some((instance) => instance.role === "side"),
    enabled: capabilities.side.supported && capabilities.side.enabled,
    reason: capabilities.side.reason,
  });
  els.viewSide.textContent = `+ 곁 (${sideInstances.filter((instance) => instance.role === "side").length})`;
  setViewActionState(els.viewOverlay, {
    visible: capabilities.overlay.supported || overlays.length > 0,
    enabled: overlays.length > 0 || (capabilities.overlay.supported && capabilities.overlay.enabled),
    reason: capabilities.overlay.reason,
    active: overlays.length > 0,
    pressed: overlays.length > 0,
  });
  els.viewOverlay.textContent = overlays.length ? "겹 끄기" : "겹 켜기";
  setViewActionState(els.viewMagnifier, {
    visible: capabilities.magnifier.supported || sideInstances.some((instance) => instance.role === "magnifier"),
    enabled: capabilities.magnifier.supported && capabilities.magnifier.enabled && Boolean(selectedTarget),
    reason: selectedTarget ? capabilities.magnifier.reason : "으뜸보기에서 움직이는 대상을 먼저 선택하세요.",
  });
  els.bogaeStage.dataset.sideOpen = sideInstances.length ? "true" : "false";
  els.bogaeStage.dataset.viewInstanceCount = String(state.viewWorkspace.instances.length);
  els.bogaeStage.dataset.sideInstanceCount = String(sideInstances.length);
  els.bogaeStage.dataset.overlayInstanceCount = String(overlays.length);
  els.bogaeStage.dataset.selectedTarget = selectedTarget?.target_id ?? "";
  els.sideViewTitle.textContent = `열린 곁보기 ${sideInstances.length}`;
  els.sideViewBody.textContent = "각 보기는 독립 instance이며 UI layout policy가 DDN/보개 비중과 화면 폭에 맞춰 배치합니다.";
  const layoutText = state.mode === "ddn-main"
    ? "layout policy: DDN 메인 · 곁보기는 보개 아래에 배치"
    : state.mode === "bogae-main"
      ? "layout policy: 보개 메인 · 곁보기는 옆 공간, 으뜸보기는 남은 폭에 refit"
      : "layout policy: 보개 전체 · view instance 2면과 DDN 이동 버튼 유지";
  els.layoutPolicy.textContent = `${layoutText}; 좁은 화면은 수직 배치`;
  els.viewRoleSummary.textContent = `primary=1(${policy.primary ?? "보개"}); side=${sideInstances.filter((instance) => instance.role === "side").length}; overlay=${overlays.length}; magnifier=${sideInstances.filter((instance) => instance.role === "magnifier").length}`;
  renderSideViewInstances(project, sideInstances);
}

function selectPrimaryCanvasTarget(event) {
  const frame = activeFrame();
  const model = state.semanticRenderModel;
  const canvas = els.canvas;
  if (!frame || model?.status !== "ready" || !canvas) return false;
  const projection = model.canvas_projection ?? {};
  const targetPoint = projection.canvas_bob ?? projection.canvas_current ?? null;
  if (!targetPoint) {
    state.viewWorkspace = selectViewTarget(state.viewWorkspace, null);
    renderAll();
    return false;
  }
  const rect = canvas.getBoundingClientRect();
  const scaleX = canvas.width / Math.max(1, rect.width);
  const scaleY = canvas.height / Math.max(1, rect.height);
  const pointer = {
    x: (event.clientX - rect.left) * scaleX,
    y: (event.clientY - rect.top) * scaleY,
  };
  const distance = Math.hypot(pointer.x - targetPoint.x, pointer.y - targetPoint.y);
  const threshold = 56 * Math.max(scaleX, scaleY);
  if (distance > threshold) {
    state.viewWorkspace = selectViewTarget(state.viewWorkspace, null);
    renderAll();
    return false;
  }
  const targetKind = model.family === "pendulum" ? "bob" : "current_point";
  state.viewWorkspace = selectViewTarget(state.viewWorkspace, {
    target_id: `${model.family}:${targetKind}:${frame.state_hash}`,
    kind: "committed_renderer_current",
    family: model.family,
    run_id: activeRun()?.run_id ?? "",
    frame_id: frame.frame_id,
    madi: frame.madi,
    state_hash: frame.state_hash,
    canvas_point: { x: targetPoint.x, y: targetPoint.y },
  });
  renderAll();
  return true;
}

function renderSemanticObservations(project) {
  if (!els.semanticObservations) return;
  const runEvidence = localProjectRunEvidenceFromProject(project);
  const activeRunValue = activeRun();
  const activeFrameValue = activeFrame();
  const semanticPayload = state.semanticViewPayload ?? buildCommittedSemanticViewPayload({
    project,
    run: activeRunValue,
    frame: activeFrameValue,
    viewConfig: { primary_view: project.primaryView, role: "primary", mode: state.mode },
    canonicalViewPayloads: buildCommittedFrameCanonicalViewPayloads(activeRunValue, activeFrameValue),
    canonicalViewHistory: buildCommittedCanonicalViewHistory(activeRunValue, activeFrameValue, project.primaryView),
  });
  if (semanticPayload.ordered_observations.length) {
    els.semanticObservations.dataset.projectRunBound = "true";
    els.semanticObservations.dataset.traceSha256 = runEvidence?.trace_sha256 ?? semanticPayload.semantic_payload_hash;
    els.semanticObservations.dataset.semanticPayloadHash = semanticPayload.semantic_payload_hash;
    els.semanticObservations.dataset.rowCount = String(semanticPayload.ordered_observations.length);
    els.semanticObservations.dataset.committedStateHash = semanticPayload.committed_frame?.state_hash ?? "";
    els.semanticObservations.innerHTML = semanticPayload.ordered_observations.map((row) => {
      return `<span class="semantic-observation" data-project-observation-id="${escapeHtml(row.observation_id)}" data-project-observation-name="${escapeHtml(row.name)}" data-project-observation-value="${escapeHtml(row.value_text)}" data-state-hash-participation="${row.state_hash_participation ? "1" : "0"}"><strong>${escapeHtml(row.name)}</strong><span>${escapeHtml(row.value_text)} ${escapeHtml(row.unit)}</span></span>`;
    }).join("");
    return;
  }
  els.semanticObservations.dataset.projectRunBound = "false";
  els.semanticObservations.dataset.traceSha256 = "";
  els.semanticObservations.dataset.semanticPayloadHash = "";
  els.semanticObservations.dataset.rowCount = "0";
  els.semanticObservations.dataset.committedStateHash = "";
  els.semanticObservations.innerHTML = `<span class="semantic-observation" data-observation-status="awaiting-committed-frame"><strong>관찰값</strong><span>${escapeHtml(project.title)} 실행 후 committed frame에서 표시</span></span>`;
}

function renderRunMetadata(project) {
  const source = activeRuntimeSourceText(project);
  const run = activeRun();
  const frame = activeFrame();
  const runEvidence = localProjectRunEvidenceFromProject(project);
  const sourceHash = `candidate:fnv1a32:${stableHash(`${project.id}\n${source}`)}`;
  const activeSourceHash = currentVirtualProjectSourceHash(project) || `candidate:fnv1a32:${stableHash(source)}`;
  const sourceDirty = Boolean(run && run.source_hash !== activeSourceHash);
  const lifecycleText = executionStatusLabel(state.executionLifecycle);
  const frameHash = frame?.state_hash ?? "-";
  const executionState = runEvidence
    ? "current_success"
    : state.projectExecution?.failure
      ? "current_failure"
      : state.projectExecution?.previousSuccess
        ? "previous_success"
        : state.projectExecution?.importedRecord
          ? "imported_record"
          : "idle";
  els.root.dataset.sourceDirty = sourceDirty ? "true" : "false";
  els.root.dataset.projectRunBound = runEvidence ? "true" : "false";
  els.root.dataset.projectExecutionState = executionState;
  els.root.dataset.projectRunTraceSha256 = runEvidence?.trace_sha256 ?? "";
  els.root.dataset.projectRunBoundedStateSha256 = runEvidence?.bounded_state_sha256 ?? "";
  els.root.dataset.projectRunRuntimeStateHash = runEvidence?.runtime_state_hash ?? "";
  els.root.dataset.projectRunLineageHash = runEvidence?.run_lineage?.lineage_hash ?? "";
  els.root.dataset.projectRunRequestHash = runEvidence?.run_lineage?.run_request_hash ?? "";
  els.root.dataset.projectRunCreatedRevision = runEvidence?.run_lineage?.created_revision ?? "";
  els.root.dataset.projectRunOutputRows = runEvidence?.output_rows?.join("|") ?? "";
  els.root.dataset.previousProjectRunLineageHash = state.projectExecution?.previousSuccess?.evidence?.run_lineage?.lineage_hash ?? "";
  els.root.dataset.projectRunFailureSourceHash = state.projectExecution?.failure?.source_hash ?? "";
  els.root.dataset.importedProjectRecordSourceHash = state.projectExecution?.importedRecord?.source_hash ?? "";
  if (runEvidence) {
    els.runStatus.textContent = `current project VM run · ${lifecycleText}`;
    els.runHash.textContent = runEvidence.bounded_state_sha256
      ? `state_hash: ${runEvidence.runtime_state_hash || "-"} · bounded_state: ${runEvidence.bounded_state_sha256}`
      : `state_hash: ${runEvidence.runtime_state_hash || frameHash}`;
  } else if (state.projectExecution?.failure) {
    const failure = state.projectExecution.failure;
    els.runStatus.textContent = `project run failed · ${failure.diagnostic?.code ?? "E_PROJECT_RUN_FAILED"}`;
    els.runHash.textContent = `failed_source: ${failure.source_hash || "-"}`;
  } else if (state.projectExecution?.previousSuccess) {
    const previous = state.projectExecution.previousSuccess;
    els.runStatus.textContent = `previous successful project run · current ${lifecycleText}`;
    els.runHash.textContent = `previous_state_hash: ${previous.evidence?.runtime_state_hash || "-"}`;
  } else if (state.projectExecution?.importedRecord) {
    els.runStatus.textContent = `imported project record · run required`;
    els.runHash.textContent = `imported_source: ${state.projectExecution.importedRecord.source_hash || "-"}`;
  } else {
    els.runStatus.textContent = sourceDirty
      ? `sealed runtime: ${lifecycleText}; source candidate differs from committed run`
      : `sealed runtime: ${lifecycleText}`;
    els.runHash.textContent = frameHash === "-" ? `source_hash: ${sourceHash}` : `state_hash: ${frameHash}`;
  }
  els.currentMadi.textContent = `madi: ${frame?.madi ?? "-"}`;
  els.runLineage.textContent = runEvidence
    ? `project-run: ${runEvidence.frontdoor} · lineage ${String(runEvidence.run_lineage?.lineage_hash ?? "").slice(0, 24)} · revision ${runEvidence.run_lineage?.created_revision || "-"}`
    : run
      ? `run: ${run.run_id}${run.parent_run_id ? ` / parent ${run.parent_run_id}@${run.parent_madi}` : ""}`
      : state.projectExecution?.previousSuccess
        ? `previous-project-run: ${String(state.projectExecution.previousSuccess.evidence?.run_lineage?.lineage_hash ?? "").slice(0, 24)}`
        : "run: -";
  els.runArchiveStatus.textContent = run?.server_run_id
    ? `archive: ${run.server_run_id} · cp ${run.server_checkpoint_count ?? 0} · ${run.server_final_status ?? "running"}`
    : runEvidence
      ? `archive: current VM run · 출력 ${runEvidence.output_rows.length}줄 · request ${String(runEvidence.run_lineage?.run_request_hash ?? "").slice(0, 24)}`
      : `archive: ${state.runArchives.length} server runs`;
  els.viewGradeLabel.textContent = project.files.length === 1
    ? `view grade: ${project.viewGrade}, single-file, module UI hidden`
    : `view grade: ${project.viewGrade}, multi-file drawer/search`;
  els.viewStatus.textContent = "view: 역할 전환은 state_hash 밖";
  const capabilityRole = state.capabilitySession?.role || state.serverProject.role || "";
  const viewOnly = Boolean((state.serverProject.projectId || state.capabilitySession?.project_id) && capabilityRole === "view");
  els.sourceEditor.readOnly = viewOnly || Boolean(run && state.cursorIndex >= 0 && state.cursorIndex < run.frames.length - 1);
  if (!state.persistenceStatus) {
    try {
      const localSnapshot = loadLocalFallbackSnapshot(project.id);
      if (localSnapshot) {
        state.persistenceStatus = {
          schema: "seamgrim.workbench.persistence_status.v1",
          mode: "local_fallback",
          server_saved: false,
          local_saved: true,
          user_label: `이 기기에만 임시 저장 ${localSnapshot.canonical_hash}`,
          snapshot: localSnapshot,
        };
      }
    } catch (_) {
      state.persistenceStatus = null;
    }
  }
  els.saveStatus.textContent = describePersistenceStatus(state.persistenceStatus);
}

function renderDiagnostics() {
  if (!els.diagnostics) return;
  const errorCount = state.diagnostics.filter((diag) => diag.severity === "error").length;
  if (els.projectVerificationOpen) {
    els.projectVerificationOpen.textContent = state.diagnostics.length ? `검증 (${state.diagnostics.length})` : "검증";
    els.projectVerificationOpen.dataset.hasErrors = errorCount ? "true" : "false";
    els.projectVerificationOpen.setAttribute("aria-label", state.diagnostics.length
      ? `검증 drawer 열기, 진단 ${state.diagnostics.length}개${errorCount ? `, 오류 ${errorCount}개` : ""}`
      : "검증 drawer 열기, 진단 없음");
  }
  els.diagnostics.innerHTML = "";
  const readinessDiagnostic = state.sourceReadiness?.diagnostics?.[0] ?? null;
  if (!readinessDiagnostic && !state.diagnostics.length) {
    const row = document.createElement("li");
    row.textContent = "diagnostics: -";
    els.diagnostics.appendChild(row);
    return;
  }
  if (readinessDiagnostic) {
    const row = document.createElement("li");
    row.dataset.severity = readinessDiagnostic.severity;
    row.dataset.diagnosticCode = readinessDiagnostic.code;
    const message = document.createElement("span");
    message.textContent = `${readinessDiagnostic.code}: ${readinessDiagnostic.message} `;
    row.append(message);
    const candidate = getSourceReadinessCandidate();
    if (candidate && readinessDiagnostic.fix_it) {
      const fixButton = document.createElement("button");
      fixButton.type = "button";
      fixButton.className = "project-graph-diagnostic";
      fixButton.dataset.testid = "source-readiness-fixit";
      fixButton.textContent = "콜론 제거하기";
      fixButton.disabled = sourceReadinessViewOnly();
      fixButton.dataset.disabledReason = fixButton.disabled ? "view_only" : "";
      fixButton.addEventListener("click", () => applySourceReadinessFixIt(candidate));
      row.append(fixButton);
    }
    els.diagnostics.appendChild(row);
  }
  state.diagnostics.forEach((diag) => {
    const row = document.createElement("li");
    row.dataset.severity = diag.severity;
    row.textContent = `${diag.code}: ${diag.message}`;
    els.diagnostics.appendChild(row);
  });
}

function renderAll() {
  const project = currentProject();
  refreshSourceReadiness(project);
  renderGlobalNav();
  renderProjects();
  renderProjectMeta(project);
  renderFileTabs(project);
  renderFileDrawer(project);
  renderSource(project);
  renderMode();
  renderViewPolicy(project);
  renderSemanticObservations(project);
  renderRunMetadata(project);
  renderRunArchiveHistory();
  renderProjectControls();
  renderServerProject();
  renderPortableLineage(project);
  renderPortableExportStatus();
  renderPortableImportPreview();
  renderPortableMetadataEditor();
  renderDiagnostics();
  els.root.dataset.projectId = project.id;
  els.root.dataset.singleFile = project.files.length === 1 ? "true" : "false";
}

async function selectProject(projectId, { preserveServerSession = false } = {}) {
  const project = allProjects().find((item) => item.id === projectId) ?? PROJECTS[0];
  const supersededRun = activeRun();
  const inFlightStep = state.livePump.inFlightPromise;
  clearTimeout(state.projectControlsRefreshTimer);
  cancelLivePump("project_switch");
  applyExecutionEvent(EXECUTION_EVENTS.PROJECT_SWITCHED);
  state.runtimeBusy = true;
  renderAll();
  try {
    if (inFlightStep) await inFlightStep.catch(() => false);
    try {
      await finalizeRunRecord(supersededRun, "stopped");
    } catch (archiveErr) {
      pushDiagnostic("E_RUN_ARCHIVE_FINALIZE_FAILED", String(archiveErr?.message ?? archiveErr), "error");
    }
    state.projectId = project.id;
    state.projectControlsGeneration += 1;
    state.projectControls = emptyProjectControlModel(project.id, "loading");
    state.activeFilePath = project.files[0].path;
    state.fileFilter = "";
    els.fileSearch.value = "";
    await loadProjectFiles(project);
    state.pendingRecipe = null;
    state.nextInput = null;
    state.selectedRunArchive = null;
    state.runs = [];
    state.activeRunId = "";
    state.cursorIndex = -1;
    state.wasm = null;
    resetProjectExecutionState({ keepImportedRecord: false });
    state.projectExecution.lockManuallyEdited = false;
    const portableControls = project.portableSnapshot?.controls_snapshot;
    state.viewWorkspace = portableControls && typeof portableControls === "object"
      ? hydrateProductViewWorkspace(
          project,
          portableControls.view_workspace,
          portableControls.selected_view ?? portableControls.view_role ?? "",
          "portable_project",
        )
      : createViewWorkspace(project);
    state.persistenceStatus = null;
    state.lastPortableExport = null;
    state.portableMetadataDraft = metadataDraftFromProject(project);
    if (!preserveServerSession) {
      state.capabilitySession = null;
      clearWorkbenchCapabilitySession();
      state.serverProject = emptyServerProjectState();
      state.runArchives = [];
    }
    await refreshProjectControls(project);
  } finally {
    state.runtimeBusy = false;
    renderAll();
  }
  setTimeout(() => refreshProjectGraph().catch(() => {}), 0);
}

async function createOneFileDdnProject() {
  const draft = readOneFileDraft();
  customOneFileProject = buildOneFileProject(draft);
  await selectProject(ONE_FILE_DDN_PROJECT_ID);
  const source = state.fileTexts.get("lesson.ddn") ?? defaultOneFileDdnSource();
  writeOneFileDraft(source);
  state.persistenceStatus = {
    schema: "seamgrim.workbench.persistence_status.v1",
    mode: "local_recovery",
    server_saved: false,
    local_saved: true,
    user_label: "새 DDN local recovery 준비",
  };
  pushDiagnostic(
    draft ? "W_ONE_FILE_DDN_RECOVERED" : "W_ONE_FILE_DDN_CREATED",
    draft ? "이 기기의 임시 원문을 복구했습니다." : "새 한 파일 DDN을 만들었습니다.",
  );
  renderAll();
}

function selectFile(path) {
  state.activeFilePath = path;
  renderAll();
}

document.querySelectorAll("[data-global-entry]").forEach((button) => {
  button.addEventListener("click", () => {
    state.globalEntry = button.dataset.globalEntry;
    renderGlobalNav();
    renderProjects();
    if (state.globalEntry === "my-work") {
      refreshMyWorkIndex().catch((err) => {
        pushDiagnostic("E_MY_WORK_REFRESH_FAILED", String(err?.message ?? err), "error");
        renderAll();
      });
    }
  });
});

document.querySelectorAll("[data-mode]").forEach((button) => {
  button.addEventListener("click", () => {
    state.mode = button.dataset.mode;
    renderAll();
  });
});

document.querySelectorAll("[data-view-action]").forEach((button) => {
  button.addEventListener("click", () => {
    const project = currentProject();
    const capabilities = viewRoleCapabilities(project, state.semanticViewPayload, state.semanticRenderModel);
    const action = button.dataset.viewAction;
    if (action === "focus-primary") state.viewWorkspace = focusPrimaryView(state.viewWorkspace);
    if (action === "add-side") state.viewWorkspace = openSideView(state.viewWorkspace, project, capabilities);
    if (action === "toggle-overlay") state.viewWorkspace = toggleOverlayView(state.viewWorkspace, project, capabilities);
    if (action === "open-magnifier") state.viewWorkspace = openMagnifierView(state.viewWorkspace, project, capabilities);
    renderAll();
  });
});

els.canvas?.addEventListener("click", (event) => selectPrimaryCanvasTarget(event));
els.bogaeSourceAccess?.addEventListener("click", () => {
  state.mode = "ddn-main";
  renderAll();
  els.sourceEditor?.focus();
});

els.projectSearch.addEventListener("input", () => {
  state.projectFilter = els.projectSearch.value;
  renderProjects();
  if (state.globalEntry === "my-work") renderMyWork();
});

document.querySelector("[data-testid='new-ddn-project']")?.addEventListener("click", () => {
  els.projectCreateDialog?.showModal();
  els.projectCreateName?.focus();
});

function closeProjectCreateDialog() {
  els.projectCreateDialog?.close();
}

document.querySelector("[data-testid='project-create-close']")?.addEventListener("click", closeProjectCreateDialog);
document.querySelector("[data-testid='project-create-cancel']")?.addEventListener("click", closeProjectCreateDialog);
els.projectCreateForm?.addEventListener("submit", (event) => {
  event.preventDefault();
  const data = new FormData(els.projectCreateForm);
  const name = String(data.get("project-name") ?? "").trim();
  const template = String(data.get("project-template") ?? "physics");
  if (!name) {
    els.projectCreateName?.focus();
    return;
  }
  createNativeProject(name, template)
    .then(closeProjectCreateDialog)
    .catch((err) => {
      pushDiagnostic("E_NATIVE_PROJECT_CREATE_FAILED", String(err?.message ?? err), "error");
      renderAll();
    });
});

els.fileSearch.addEventListener("input", () => {
  state.fileFilter = els.fileSearch.value;
  renderFileDrawer(currentProject());
});

function reportProjectEditError(err) {
  const diagnostic = projectEditDiagnostic(err);
  pushDiagnostic(diagnostic.code || "E_PROJECT_EDIT_FAILED", diagnostic.message || String(err), "error");
  renderAll();
}

document.querySelector("[data-testid='file-add']")?.addEventListener("click", () => {
  const path = globalThis.prompt?.("추가할 DDN 파일 경로", "app/새파일.ddn");
  if (!path) return;
  requestProjectEdit({ kind: "add_file", path, utf8_text: "# 새 DDN 파일\n", role: "ddn_source" }).catch(reportProjectEditError);
});

document.querySelector("[data-testid='module-add']")?.addEventListener("click", () => {
  const path = globalThis.prompt?.("추가할 모듈 경로", "lib/새모듈.ddn");
  if (!path) return;
  const moduleName = globalThis.prompt?.("모듈 이름", path.split("/").at(-1)?.replace(/\.ddn$/u, "") || "새모듈");
  if (!moduleName) return;
  requestProjectEdit({ kind: "add_module", path, module_name: moduleName }).catch(reportProjectEditError);
});
document.querySelector("[data-testid='gaji-bundle-open']")?.addEventListener("click", openGajiBundleDialog);
document.querySelector("[data-testid='gaji-bundle-close']")?.addEventListener("click", closeGajiBundleDialog);
document.querySelector("[data-testid='gaji-bundle-cancel']")?.addEventListener("click", closeGajiBundleDialog);
els.gajiBundleForm?.addEventListener("submit", (event) => {
  event.preventDefault();
  previewGajiBundle().catch((err) => {
    pendingGajiBundle = null;
    els.gajiBundlePublish.disabled = true;
    els.gajiBundleStatus.textContent = String(err?.message ?? err);
    pushDiagnostic("E_GAJI_EXTRACTION_PLAN", String(err?.message ?? err), "error");
  });
});
els.gajiBundlePublish?.addEventListener("click", () => {
  publishGajiBundle().catch((err) => {
    els.gajiBundleStatus.textContent = String(err?.message ?? err);
    pushDiagnostic("E_GAJI_PUBLISH", String(err?.message ?? err), "error");
    renderAll();
  });
});
document.querySelector("[data-testid='gaji-shelf-open']")?.addEventListener("click", () => {
  const menu = document.querySelector("[data-testid='project-more-menu']");
  if (menu) menu.open = false;
  openGajiShelf().catch(reportGajiShelfError);
});
document.querySelector("[data-testid='gaji-shelf-close']")?.addEventListener("click", () => els.gajiShelfDialog?.close?.());
els.gajiShelfSearch?.addEventListener("input", () => refreshGajiShelf().catch(reportGajiShelfError));
document.querySelectorAll("[data-testid='gaji-profile-filters'] input").forEach((node) => {
  node.addEventListener("change", () => refreshGajiShelf().catch(reportGajiShelfError));
});
els.gajiInstallAlias?.addEventListener("input", () => {
  if (!pendingGajiInstall) return;
  const rowButton = document.querySelector(`.gaji-shelf-row[data-gaji-package-sha256="${pendingGajiInstall.row.package_sha256}"]`);
  previewShelfInstall(pendingGajiInstall.row, rowButton).catch(reportGajiShelfError);
});
els.gajiInstallApply?.addEventListener("click", () => applyShelfInstall().catch(reportGajiShelfError));
els.gajiInstallRemove?.addEventListener("click", () => removeShelfInstall().catch(reportGajiShelfError));
els.gajiRemixStart?.addEventListener("click", () => {
  try { startShelfRemix(); } catch (err) { reportGajiShelfError(err); }
});
els.gajiRemixPublish?.addEventListener("click", () => publishShelfRemix().catch(reportGajiShelfError));
document.querySelector("[data-testid='gaji-store-export']")?.addEventListener("click", () => {
  try { exportSelectedGajiArtifact(); } catch (err) { reportGajiShelfError(err); }
});
document.querySelector("[data-testid='gaji-store-import']")?.addEventListener("click", () => document.querySelector("[data-testid='gaji-store-import-input']")?.click());
document.querySelector("[data-testid='gaji-store-import-input']")?.addEventListener("change", (event) => {
  importGajiArtifactFile(event.target.files?.[0]).catch(reportGajiShelfError).finally(() => { event.target.value = ""; });
});

els.fileList.addEventListener("click", (event) => {
  const button = event.target?.closest?.("[data-file-action]");
  if (!button) return;
  event.preventDefault();
  event.stopPropagation();
  const path = String(button.dataset.filePath || "");
  const action = String(button.dataset.fileAction || "");
  let operation = null;
  if (action === "rename") {
    const toPath = globalThis.prompt?.("바꿀 파일 경로", path);
    if (toPath && toPath !== path) operation = { kind: "rename_file", from_path: path, to_path: toPath };
  } else if (action === "duplicate") {
    const toPath = globalThis.prompt?.("복제할 파일 경로", path.replace(/\.ddn$/u, "_복사.ddn"));
    if (toPath) operation = { kind: "duplicate_file", from_path: path, to_path: toPath };
  } else if (action === "set_entry") {
    operation = { kind: "set_entry", path };
  } else if (action === "delete") {
    operation = { kind: "delete_file", path };
  }
  if (operation) requestProjectEdit(operation).catch(reportProjectEditError);
});

document.querySelector("[data-testid='project-edit-undo']")?.addEventListener("click", () => {
  const previous = state.projectEditUndo.shift();
  if (!previous) {
    pushDiagnostic("W_PROJECT_EDIT_UNDO_EMPTY", "되돌릴 구조 변경이 없습니다.");
    renderAll();
    return;
  }
  applyVirtualProjectSource(previous, { rememberUndo: false });
  pushDiagnostic("W_PROJECT_EDIT_UNDONE", "최근 구조 변경을 되돌렸습니다.");
  renderAll();
});

function closeProjectEditDialog() {
  state.pendingProjectEdit = null;
  els.projectEditDialog?.close();
}
document.querySelector("[data-testid='project-edit-close']")?.addEventListener("click", closeProjectEditDialog);
document.querySelector("[data-testid='project-edit-cancel']")?.addEventListener("click", closeProjectEditDialog);
document.querySelector("[data-testid='project-edit-apply']")?.addEventListener("click", () => {
  applyPendingProjectEdit().catch(reportProjectEditError);
});

els.sourceEditor.addEventListener("input", () => {
  state.completionDocumentVersion += 1;
  state.completionGeneration += 1;
  closeCompletionPopup();
  const editedPath = activeFile().path;
  state.fileTexts.set(editedPath, els.sourceEditor.value);
  if (editedPath === "ddn.lock") {
    state.projectExecution.lockManuallyEdited = true;
    state.projectExecution.lockTrust = emptyProjectLockTrust();
  } else if (state.projectExecution?.lockTrust?.verified_lock_sha256) {
    state.projectExecution.lockTrust = {
      ...state.projectExecution.lockTrust,
      local_non_lock_edit_after_verified: true,
    };
  }
  state.lastPortableExport = null;
  syncNativeProjectFromState();
  state.projectControlsGeneration += 1;
  state.projectControls = emptyProjectControlModel(state.projectId, "loading");
  state.pendingRecipe = null;
  renderProjectControls();
  scheduleProjectControlsRefresh();
  clearTimeout(state.projectGraphRefreshTimer);
  state.projectGraphRefreshTimer = setTimeout(() => refreshProjectGraph().catch(() => {}), 250);
  markCurrentProjectExecutionStale("source_edit");
  if (state.projectExecution?.failure) {
    state.projectExecution.failure = null;
  }
  if (currentProject().id === ONE_FILE_DDN_PROJECT_ID && activeFile().path === "lesson.ddn") {
    writeOneFileDraft(els.sourceEditor.value);
    state.persistenceStatus = {
      schema: "seamgrim.workbench.persistence_status.v1",
      mode: "local_recovery",
      server_saved: false,
      local_saved: true,
      user_label: "새 DDN local recovery 저장됨",
    };
  } else if (nativeProjects.some((project) => project.id === currentProject().id)) {
    state.persistenceStatus = {
      schema: "seamgrim.workbench.persistence_status.v1",
      mode: "local_recovery",
      server_saved: false,
      local_saved: true,
      user_label: `${currentProject().title} local recovery 저장됨`,
    };
  }
  refreshSourceReadiness(currentProject());
  renderDiagnostics();
  renderSemanticObservations(currentProject());
  renderRunMetadata(currentProject());
  drawPreview();
  setTimeout(() => requestCompletion(), 120);
});

els.sourceEditor.addEventListener("keydown", (event) => {
  if (els.completionPopup?.hidden || !state.completionItems.length) return;
  if (event.key === "ArrowDown" || event.key === "ArrowUp") {
    event.preventDefault();
    const delta = event.key === "ArrowDown" ? 1 : -1;
    state.completionSelectedIndex = (state.completionSelectedIndex + delta + state.completionItems.length)
      % state.completionItems.length;
    renderCompletionPopup();
  } else if (event.key === "Enter" || event.key === "Tab") {
    event.preventDefault();
    selectCompletion();
  } else if (event.key === "Escape") {
    event.preventDefault();
    closeCompletionPopup();
  }
});

window.addEventListener("resize", () => drawPreview());

loadNativeProjectCatalog();
loadPortableProjectCatalog();
state.capabilitySession = captureWorkbenchCapabilitySession() ?? readWorkbenchCapabilitySession();
await selectProject(state.projectId, { preserveServerSession: Boolean(state.capabilitySession?.project_id) });
try {
  await openProjectFromServerSession();
} catch (err) {
  pushDiagnostic(err?.payload?.code ?? "E_PROJECT_SERVER_OPEN", err?.message ?? "서버 프로젝트 열기 실패", "error");
  renderAll();
}

async function refreshProjectGraph() {
  const source = currentVirtualProjectSource();
  if (!source) {
    state.projectGraph = null;
    renderProjectGraph();
    return null;
  }
  try {
    const graph = await runtimeBridge.projectGraph(source);
    const symbols = await runtimeBridge.projectSymbols(source);
    state.projectGraph = {
      graph,
      symbols,
      lockStatus: source.files.some((file) => file.path === "ddn.lock") ? "있음/실행 시 검증" : "없음",
      error: null,
    };
  } catch (err) {
    state.projectGraph = { graph: null, symbols: null, lockStatus: "확인 실패", error: projectEditDiagnostic(err) };
  }
  renderProjectGraph();
  return state.projectGraph;
}

async function prepareCurrentProjectLink(projectSource) {
  return runtimeBridge.prepareProjectLink(projectSource, "앱", true, true);
}

function projectEditDiagnostic(err) {
  const text = String(err?.message ?? err ?? "project edit 실패");
  const start = text.indexOf("{");
  if (start >= 0) {
    try { return JSON.parse(text.slice(start)); } catch (_) { /* use fallback */ }
  }
  return { code: "E_PROJECT_EDIT_FAILED", message: text };
}

async function requestProjectEdit(operation) {
  const source = currentVirtualProjectSource();
  if (!source || !nativeProjects.some((item) => item.id === state.projectId)) {
    throw new Error("네이티브 로컬 프로젝트에서만 구조를 편집할 수 있습니다");
  }
  const beforeHash = await runtimeBridge.projectSourceSha256(source);
  const plan = await runtimeBridge.planProjectEdit({
    schema: "ddn.local_project_edit_plan.v1",
    source,
    operation,
    expected_source_sha256: beforeHash,
  });
  state.pendingProjectEdit = plan;
  els.projectEditSummary.textContent = `${plan.operation} · 파일 ${plan.affected_files?.length ?? 0}개 · 참조 ${plan.affected_references?.length ?? 0}개 · lock ${plan.lock_stale ? "stale→적용 시 갱신" : "유지"}`;
  els.projectEditPreview.textContent = (plan.patches ?? []).map((patch) => (
    `${patch.path} [${patch.reason}]\n- ${patch.before || "(없음)"}\n+ ${patch.after || "(삭제)"}`
  )).join("\n\n") || "변경 patch 없음";
  els.projectEditDialog?.showModal();
  document.querySelector("[data-testid='project-edit-apply']")?.focus();
  return plan;
}

function applyVirtualProjectSource(source, { rememberUndo = true } = {}) {
  const index = nativeProjects.findIndex((item) => item.id === state.projectId);
  if (index < 0) throw new Error("현재 네이티브 프로젝트를 찾지 못했습니다");
  if (rememberUndo) {
    state.projectEditUndo = [currentVirtualProjectSource(), ...state.projectEditUndo].filter(Boolean).slice(0, 10);
  }
  const current = nativeProjects[index];
  const files = source.files.map((file) => ({ path: file.path, role: file.role, fallback: file.utf8_text }));
  const updated = {
    ...current,
    files,
    portableSnapshot: {
      ...current.portableSnapshot,
      local_package_payload: {
        ...current.portableSnapshot.local_package_payload,
        root_path: source.root_path,
        entry_path: source.entry_path,
        files: source.files,
      },
    },
  };
  nativeProjects[index] = updated;
  state.fileTexts = new Map(source.files.map((file) => [file.path, file.utf8_text]));
  if (!source.files.some((file) => file.path === state.activeFilePath)) state.activeFilePath = source.entry_path;
  writeNativeProjectCatalog();
  state.lastPortableExport = null;
  state.pendingRecipe = null;
  state.nextInput = null;
  state.selectedRunArchive = null;
  state.projectControlsGeneration += 1;
  state.projectControls = emptyProjectControlModel(state.projectId, "loading");
  resetProjectExecutionState({ keepImportedRecord: false });
  state.persistenceStatus = {
    schema: "seamgrim.workbench.persistence_status.v1",
    mode: "local_recovery",
    server_saved: false,
    local_saved: true,
    user_label: "프로젝트 구조 변경 local recovery 저장됨",
  };
  renderAll();
  scheduleProjectControlsRefresh();
  refreshProjectGraph().catch(() => {});
}

async function applyPendingProjectEdit() {
  const plan = state.pendingProjectEdit;
  if (!plan?.atomic_apply) throw new Error("원자 적용 가능한 계획이 아닙니다");
  const currentHash = await runtimeBridge.projectSourceSha256(currentVirtualProjectSource());
  if (currentHash !== plan.before_source_sha256) {
    throw new Error("E_PROJECT_EDIT_SOURCE_CONFLICT: 미리보기 뒤 원문이 바뀌어 적용을 취소했습니다");
  }
  let sourceToApply = plan.project_source;
  if (plan.lock_stale && sourceToApply.files.some((file) => file.path === "ddn.lock")) {
    const sourceWithoutLock = {
      ...sourceToApply,
      files: sourceToApply.files.filter((file) => file.path !== "ddn.lock"),
    };
    const lockText = `${(await runtimeBridge.projectGajiLock(sourceWithoutLock)).trimEnd()}\n`;
    sourceToApply = {
      ...sourceToApply,
      files: sourceToApply.files.map((file) => file.path === "ddn.lock"
        ? { path: "ddn.lock", role: "lock", utf8_text: lockText }
        : file),
    };
  }
  applyVirtualProjectSource(sourceToApply);
  state.pendingProjectEdit = null;
  els.projectEditDialog?.close();
  pushDiagnostic("W_PROJECT_EDIT_APPLIED", "검토한 구조 변경을 원자적으로 적용했습니다.");
  renderAll();
}

async function refreshGeneratedProjectLockForRun(projectSource) {
  if (!projectSource || state.projectExecution?.lockManuallyEdited) return projectSource;
  const files = Array.isArray(projectSource.files) ? projectSource.files : [];
  const lockIndex = files.findIndex((file) => String(file?.path ?? "") === "ddn.lock");
  if (lockIndex < 0) return projectSource;
  const lockTrust = state.projectExecution?.lockTrust ?? emptyProjectLockTrust();
  if (!lockTrust.local_non_lock_edit_after_verified || !lockTrust.verified_lock_sha256) {
    return projectSource;
  }
  const currentLockText = String(files[lockIndex]?.utf8_text ?? "");
  if (!currentLockText.includes(String(lockTrust.verified_lock_sha256))) {
    return projectSource;
  }
  const sourceWithoutLock = {
    ...projectSource,
    files: files.filter((file) => String(file?.path ?? "") !== "ddn.lock"),
  };
  const lockPayload = await runtimeBridge.projectGajiLock(sourceWithoutLock, { allowMissing: true });
  if (lockPayload === null) return projectSource;
  const lockText = `${lockPayload.trimEnd()}\n`;
  const nextFiles = files.map((file, index) => index === lockIndex
    ? {
        path: "ddn.lock",
        role: "lock",
        utf8_text: lockText,
      }
    : file);
  state.fileTexts.set("ddn.lock", lockText);
  state.projectExecution.lockTrust = emptyProjectLockTrust();
  return {
    ...projectSource,
    files: nextFiles,
  };
}

function makeSnapshot(intent = "none", input = state.nextInput) {
  return {
    schema: "seamgrim.input_snapshot.ui.v1",
    madi: activeRun()?.frames.length ?? 0,
    intent,
    input_id: String(input?.input_id ?? ""),
    action_id: String(input?.action_id ?? ""),
    action_map_hash: String(input?.action_map_hash ?? ""),
    keys: Number(input?.keys ?? 0),
    lastKey: String(input?.lastKey ?? ""),
    pointer: { x: Number(input?.px ?? 0), y: Number(input?.py ?? 0) },
    dt: Number(input?.dt ?? 0.015625),
  };
}

function buildFrame(run, wasmState, snapshot) {
  return {
    frame_id: run.frames.length,
    madi: readMadi(wasmState, run.frames.length),
    state_hash: readStateHash(wasmState, `candidate:missing:${run.frames.length}`),
    source_hash: run.source_hash,
    recipe_hash: run.recipe_hash,
    input_snapshot: snapshot,
    wasm_state: wasmState,
  };
}

function appendFrame(run, wasmState, snapshot) {
  const frame = buildFrame(run, wasmState, snapshot);
  run.frames.push(frame);
  state.cursorIndex = run.frames.length - 1;
  return frame;
}

function runtimeStateSignalsDone(wasmState) {
  return wasmState?.done === true
    || wasmState?.runtime_done === true
    || wasmState?.status === "done"
    || wasmState?.lifecycle === "done";
}

function runReachedDone(run, wasmState) {
  const configuredMadi = Math.max(0, Number(run?.configured_madi ?? 0));
  const committedSteps = Math.max(0, Number(run?.committed_step_count ?? 0));
  return runtimeStateSignalsDone(wasmState)
    || (configuredMadi > 0 && committedSteps >= configuredMadi);
}

function editableProjectSession() {
  const session = state.capabilitySession ?? readWorkbenchCapabilitySession();
  if (!state.serverProject.projectId || !state.serverProject.headRevisionId) return null;
  if (!session?.capability || session.role !== "edit") return null;
  return session;
}

function renderRunArchiveHistory() {
  if (!els.runArchiveList || !els.runArchiveDetail) return;
  const selectedId = String(state.selectedRunArchive?.run?.server_run_id ?? "");
  els.runArchiveList.innerHTML = "";
  if (!state.runArchives.length) {
    const empty = document.createElement("span");
    empty.className = "run-hash";
    empty.textContent = "저장된 실행 없음";
    els.runArchiveList.appendChild(empty);
  } else {
    for (const archive of state.runArchives) {
      const runId = String(archive.server_run_id ?? "");
      const button = document.createElement("button");
      button.type = "button";
      button.dataset.serverRunId = runId;
      button.dataset.testid = `run-archive-open-${runId}`;
      button.setAttribute("aria-current", selectedId === runId ? "true" : "false");
      const identity = document.createElement("span");
      identity.textContent = `${runId}${archive.parent_server_run_id ? ` · parent ${archive.parent_server_run_id}` : ""}`;
      const status = document.createElement("span");
      const checkpointCount = Math.max(0, Number(archive.latest_sequence ?? -1) + 1);
      status.textContent = `${archive.final_status ?? "running"} · cp ${checkpointCount}`;
      button.append(identity, status);
      els.runArchiveList.appendChild(button);
    }
  }

  const selected = state.selectedRunArchive?.run;
  els.runArchiveDetail.hidden = !selected;
  if (!selected) {
    if (els.runArchiveCheckpointList) els.runArchiveCheckpointList.innerHTML = "";
    return;
  }
  const checkpoints = Array.isArray(selected.checkpoints) ? selected.checkpoints : [];
  els.runArchiveDetailTitle.textContent = `${selected.server_run_id} · ${selected.final_status} · checkpoint ${checkpoints.length}개`;
  els.runArchiveCheckpointList.innerHTML = "";
  for (const checkpoint of checkpoints) {
    const row = document.createElement("li");
    const stateHash = String(checkpoint.artifact?.state_hashes?.[0] ?? "-");
    row.dataset.checkpointSequence = String(checkpoint.sequence ?? "");
    row.textContent = `seq ${checkpoint.sequence} · madi ${checkpoint.committed_madi} · state ${stateHash} · sha ${checkpoint.checkpoint_sha256}`;
    els.runArchiveCheckpointList.appendChild(row);
  }
}

async function openRunArchiveDetail(serverRunId) {
  const session = state.capabilitySession ?? readWorkbenchCapabilitySession();
  const projectId = state.serverProject.projectId || session?.project_id || "";
  const capability = session?.capability || state.serverProject.viewCapability || state.serverProject.editCapability || "";
  const requestedRunId = String(serverRunId ?? "").trim();
  if (!projectId || !capability || !requestedRunId) return null;
  const payload = await getRunArchive({
    projectId,
    serverRunId: requestedRunId,
    capability,
  });
  if (state.serverProject.projectId !== projectId && state.capabilitySession?.project_id !== projectId) return null;
  state.selectedRunArchive = payload;
  renderRunArchiveHistory();
  return payload;
}

async function refreshRunArchives() {
  const session = state.capabilitySession ?? readWorkbenchCapabilitySession();
  const projectId = state.serverProject.projectId || session?.project_id || "";
  const capability = session?.capability || state.serverProject.viewCapability || state.serverProject.editCapability || "";
  if (!projectId || !capability) {
    state.runArchives = [];
    state.selectedRunArchive = null;
    renderRunArchiveHistory();
    return [];
  }
  const payload = await listRunArchives({ projectId, capability });
  state.runArchives = Array.isArray(payload.runs) ? payload.runs : [];
  const selectedId = String(state.selectedRunArchive?.run?.server_run_id ?? "");
  if (selectedId && !state.runArchives.some((run) => run.server_run_id === selectedId)) {
    state.selectedRunArchive = null;
  }
  renderRunArchiveHistory();
  return state.runArchives;
}

async function createServerRunArchive(run, { branchFrom = null } = {}) {
  const session = editableProjectSession();
  if (!session) {
    run.server_archive_status = "local_only";
    return null;
  }
  run.server_project_id = state.serverProject.projectId;
  run.server_edit_capability = session.capability;
  const draft = buildRunArchiveDraft({
    projectId: state.serverProject.projectId,
    sourceRevisionId: state.serverProject.headRevisionId,
    expectedHeadRevisionId: state.serverProject.headRevisionId,
    sourceContentSha256: state.serverProject.contentSha256,
    recipeHash: run.recipe_hash,
    seed: `ui:${run.run_id}`,
    parentServerRunId: branchFrom?.server_run_id ?? "",
    branchMadi: branchFrom?.madi ?? null,
    branchStateHash: branchFrom?.state_hash ?? "",
  });
  const payload = await createRunArchive({
    projectId: state.serverProject.projectId,
    capability: session.capability,
    draft,
  });
  const serverRun = payload.run ?? {};
  run.server_run_id = String(serverRun.server_run_id ?? "");
  run.source_revision_id = String(serverRun.source_revision_id ?? state.serverProject.headRevisionId);
  run.source_content_sha256 = String(serverRun.source_content_sha256 ?? state.serverProject.contentSha256);
  run.server_archive_status = "running";
  run.server_checkpoint_count = 0;
  run.server_final_status = String(serverRun.final_status ?? "running");
  await refreshRunArchives();
  return serverRun;
}

async function persistRunCheckpoint(run, frame) {
  if (!run?.server_run_id || !frame) return null;
  const currentSession = editableProjectSession();
  const projectId = String(run.server_project_id || state.serverProject.projectId || "");
  const capability = String(run.server_edit_capability || currentSession?.capability || "");
  if (!projectId || !capability) return null;
  const previous = run.server_latest_checkpoint_sha256 ?? "";
  const checkpoint = buildCheckpointPayload({
    run,
    frame,
    sequence: Number(run.server_checkpoint_count ?? 0),
    previousCheckpointSha256: previous,
  });
  const payload = await appendRunCheckpoint({
    projectId,
    serverRunId: run.server_run_id,
    capability,
    checkpoint,
  });
  const checkpoints = payload.run?.checkpoints ?? [];
  const latest = checkpoints.at(-1) ?? {};
  run.server_latest_checkpoint_sha256 = String(latest.checkpoint_sha256 ?? "");
  run.server_checkpoint_count = checkpoints.length;
  run.server_archive_status = "checkpointed";
  if (state.serverProject.projectId === projectId) await refreshRunArchives();
  return latest;
}

async function finalizeRunRecord(run, finalStatus = "stopped") {
  if (!run) return null;
  if (run.local_finalized || run.server_finalized || run.server_finalization_started) return null;
  run.final_status = finalStatus;
  if (!run.server_run_id) {
    if (["local_only", "error"].includes(run.server_archive_status)) run.local_finalized = true;
    return null;
  }
  const currentSession = editableProjectSession();
  const projectId = String(run.server_project_id || (
    currentSession && state.serverProject.projectId === run.project_id ? state.serverProject.projectId : ""
  ));
  const capability = String(run.server_edit_capability || (
    currentSession && state.serverProject.projectId === run.project_id ? currentSession.capability : ""
  ));
  if (!projectId || !capability) return null;
  if (!claimRunFinalization(run, finalStatus).claimed) return null;
  const payload = await finalizeRunArchive({
    projectId,
    serverRunId: run.server_run_id,
    capability,
    finalStatus,
  });
  run.server_finalized = true;
  run.server_archive_status = "finalized";
  run.server_final_status = String(payload.run?.final_status ?? finalStatus);
  if (state.serverProject.projectId === projectId) await refreshRunArchives();
  return payload.run;
}

async function finalizeActiveRun(finalStatus = "stopped") {
  return finalizeRunRecord(activeRun(), finalStatus);
}

async function finalizeFailedRunArchive(run, diagnostic = {}) {
  if (!run) return null;
  run.server_failure_diagnostic = diagnostic;
  try {
    return await finalizeRunRecord(run, "failed");
  } catch (archiveErr) {
    run.server_archive_status = "failed-finalize-error";
    run.server_final_status = "failed";
    run.server_finalize_error = String(archiveErr?.message ?? archiveErr);
    pushDiagnostic(
      "E_RUN_ARCHIVE_FAILED_FINALIZE_FAILED",
      `실패한 실행 기록을 failed로 종료하지 못했습니다: ${run.server_finalize_error}`,
      "error",
    );
    return null;
  }
}

async function startRun({ branchFrom = null } = {}) {
  if (state.runtimeBusy || state.sourceAnalysisInFlight) return false;
  state.sourceAnalysisInFlight = true;
  const projectAtRequest = currentProject();
  let sourceReadiness;
  try {
    sourceReadiness = await refreshAuthoritativeSourceReadiness(projectAtRequest);
  } finally {
    state.sourceAnalysisInFlight = false;
  }
  if (sourceReadiness.superseded || currentProject().id !== projectAtRequest.id) return false;
  if (!sourceReadiness.ready) {
    state.runtimeStatus = "source-blocked";
    state.sourceReadinessRunBlocked = true;
    sourceReadinessRunOutcome("run_blocked", {
      code: sourceReadiness.diagnostics?.[0]?.code ?? SOURCE_READINESS_DIAGNOSTIC_CODE,
      source_hash: sourceReadiness.source_hash,
    });
    pushDiagnostic("E_SOURCE_RUN_BLOCKED", "원문 분석 또는 제품 준비 진단을 먼저 해결해야 실행할 수 있습니다.", "error");
    renderAll();
    openProgressiveDialog(els.projectVerificationDrawer);
    return false;
  }
  state.sourceReadinessRunBlocked = false;
  cancelLivePump("new_run");
  resetLivePumpMetricsForRun();
  const started = applyExecutionEvent(EXECUTION_EVENTS.START, { branch: Boolean(branchFrom) });
  if (!started.accepted) return false;
  state.runtimeBusy = true;
  clearDiagnostics();
  const executionGeneration = state.executionLifecycle.generation;
  const projectIdAtStart = state.projectId;
  let run = null;
  let projectSource = null;
  let projectSourceHash = "";
  let projectExecutionPlan = null;
  renderAll();
  try {
    const project = currentProject();
    projectSource = currentVirtualProjectSource(project);
    if (projectSource) {
      projectSource = await refreshGeneratedProjectLockForRun(projectSource);
      assertExecutionGeneration(executionGeneration, projectIdAtStart);
    }
    projectSourceHash = projectSource ? virtualProjectSourceHash(projectSource) : "";
    const source = projectSource ? activeRuntimeSourceText(project) : activeSourceText();
    if (!source.trim()) {
      applyExecutionEvent(EXECUTION_EVENTS.PREPARE_FAILED, { reason: "source_empty" });
      pushDiagnostic("E_SOURCE_EMPTY", "DDN 원문이 비어 있습니다. 실행할 원문을 입력해 주세요.", "error");
      return false;
    }
    if (projectSource) {
      markCurrentProjectExecutionStale("new_project_run");
      state.projectExecution.failure = null;
      const prepared = await prepareCurrentProjectLink(projectSource);
      assertExecutionGeneration(executionGeneration, projectIdAtStart);
      projectExecutionPlan = projectExecutionPlanFromPrepared(prepared, projectSourceHash);
      recordVerifiedProjectLockTrust(projectSourceHash, projectExecutionPlan);
    }
    const runRecipe = state.pendingRecipe?.project_id === project.id
      && state.pendingRecipe?.authoring_plan_hash === state.projectControls?.authoring_plan_hash
      ? structuredClone(state.pendingRecipe)
      : null;
    run = {
      schema: "seamgrim.run_record.v1",
      run_id: buildRunId(branchFrom ? "branch" : "run"),
      project_id: project.id,
      source_hash: projectSourceHash || `candidate:fnv1a32:${stableHash(source)}`,
      project_source_hash: projectSourceHash,
      source_kind: projectSource ? "virtual_project_source" : "single_file_source",
      recipe_hash: recipeHash(),
      recipe_version: state.recipeVersion,
      setup: runRecipe ?? {},
      parent_run_id: branchFrom?.run_id ?? "",
      parent_server_run_id: branchFrom?.server_run_id ?? "",
      parent_madi: branchFrom?.madi ?? null,
      parent_state_hash: branchFrom?.state_hash ?? "",
      frames: [],
      immutable: true,
      execution_mode_decision: null,
      execution_source: projectExecutionPlan?.linked_execution_source ?? source,
      configured_madi: 0,
      committed_step_count: 0,
    };
    if (projectExecutionPlan) {
      run.project_execution_plan = projectExecutionPlan;
      run.project_prepare_link_hash = projectExecutionPlan.prepare_link_sha256;
      run.project_graph_hash = String(projectExecutionPlan.project_graph?.project_graph_sha256 ?? "");
      run.linked_source_hash = projectExecutionPlan.linked_execution_source_sha256;
      run.execution_mode_decision = projectExecutionPlan.execution_mode_decision;
    }
    state.runs.push(run);
    state.activeRunId = run.run_id;
    state.cursorIndex = -1;
    state.wasm = null;
    try {
      await createServerRunArchive(run, { branchFrom });
    } catch (archiveErr) {
      run.server_archive_status = "error";
      pushDiagnostic("E_RUN_ARCHIVE_CREATE_FAILED", String(archiveErr?.message ?? archiveErr), "error");
    }
    assertExecutionGeneration(executionGeneration, projectIdAtStart);
    let firstFrame = null;
    if (projectSource) {
      state.wasmVmEntryCount += 1;
      const projectWasm = await runtimeBridge.createSession({
        ddnSourceText: projectExecutionPlan.linked_execution_source,
        cacheBust: "approved-workbench-linked-project-v1",
        setStatus: () => {},
        clearStatusError: () => {},
      });
      assertExecutionGeneration(executionGeneration, projectIdAtStart);
      state.wasm = projectWasm;
      await projectWasm.updateLogic(projectExecutionPlan.linked_execution_source);
      assertExecutionGeneration(executionGeneration, projectIdAtStart);
      const vmExecutionModeDecision = requireParsedExecutionModeDecision(
        projectWasm.getExecutionModeDecision(),
      );
      if (vmExecutionModeDecision.mode !== run.execution_mode_decision.mode) {
        throw new Error("E_EXECUTION_MODE_DECISION_DIVERGED: linked envelope와 VM 판정이 다릅니다");
      }
      run.configured_madi = projectWasm.getConfiguredMadi();
      await projectWasm.reset({ keepParams: false });
      await applyRunRecipeToWasm(projectWasm, runRecipe);
      assertExecutionGeneration(executionGeneration, projectIdAtStart);
      const queuedInput = state.nextInput ? { ...state.nextInput } : null;
      const executedState = await projectWasm.step({
        n: 1,
        input: queuedInput
          ? {
              keys: queuedInput.keys,
              lastKey: queuedInput.lastKey,
              px: queuedInput.px,
              py: queuedInput.py,
              dt: queuedInput.dt,
            }
          : null,
        sourceText: projectExecutionPlan.linked_execution_source,
      });
      assertExecutionGeneration(executionGeneration, projectIdAtStart);
      firstFrame = appendFrame(
        run,
        executedState,
        makeSnapshot(branchFrom ? "project_branch_start" : "project_run_start", queuedInput),
      );
      run.committed_step_count = 1;
      if (queuedInput?.input_id && state.nextInput?.input_id === queuedInput.input_id) {
        state.nextInput = null;
      }
      const evidence = await buildCurrentProjectRunEvidence({
        prepared: projectExecutionPlan,
        run,
        frame: firstFrame,
        wasmState: executedState,
      });
      assertExecutionGeneration(executionGeneration, projectIdAtStart);
      state.projectExecution.current = {
        schema: "seamgrim.workbench.current_project_execution.v1",
        state: "current_success",
        source_hash: projectSourceHash,
        prepare_link_sha256: projectExecutionPlan.prepare_link_sha256,
        project_graph_hash: String(projectExecutionPlan.project_graph?.project_graph_sha256 ?? ""),
        linked_source_hash: projectExecutionPlan.linked_execution_source_sha256,
        run_id: run.run_id,
        evidence,
      };
      state.projectExecution.failure = null;
    } else {
      state.wasmVmEntryCount += 1;
      const wasm = await runtimeBridge.createSession({
        ddnSourceText: source,
        sourceProfileIdentity: SOURCE_ANALYSIS_PROFILE_IDENTITY,
        cacheBust: "approved-workbench-v1",
        setStatus: () => {},
        clearStatusError: () => {},
      });
      assertExecutionGeneration(executionGeneration, projectIdAtStart);
      state.wasm = wasm;
      await wasm.updateLogic(source);
      assertExecutionGeneration(executionGeneration, projectIdAtStart);
      run.execution_mode_decision = requireParsedExecutionModeDecision(
        wasm.getExecutionModeDecision(),
      );
      run.configured_madi = wasm.getConfiguredMadi();
      await wasm.reset({ keepParams: false });
      await applyRunRecipeToWasm(wasm, runRecipe);
      const resetState = await wasm.getStateJson();
      assertExecutionGeneration(executionGeneration, projectIdAtStart);
      const isOneshot = run.execution_mode_decision.mode === "oneshot";
      const queuedInput = isOneshot && state.nextInput ? { ...state.nextInput } : null;
      const committedState = isOneshot
        ? await wasm.step({
            n: 1,
            input: queuedInput
              ? {
                  keys: queuedInput.keys,
                  lastKey: queuedInput.lastKey,
                  px: queuedInput.px,
                  py: queuedInput.py,
                  dt: queuedInput.dt,
                }
              : null,
            sourceText: run.execution_source,
          })
        : resetState;
      assertExecutionGeneration(executionGeneration, projectIdAtStart);
      const sharedRunSummary = await runtimeBridge.runSummaryWithSourceProfile({
        sourceText: source,
        sourcePath: localProjectEntryPath(project),
        requestedTicks: isOneshot ? 1 : 0,
        sourceProfileIdentity: SOURCE_ANALYSIS_PROFILE_IDENTITY,
      });
      assertExecutionGeneration(executionGeneration, projectIdAtStart);
      const committedStateHash = readStateHash(committedState, "");
      if (
        String(sharedRunSummary?.source_profile_identity ?? "") !== SOURCE_ANALYSIS_PROFILE_IDENTITY
        || !committedStateHash
        || String(sharedRunSummary?.state_hash ?? "") !== committedStateHash
        || !sharedRunSummary?.work_cost_receipt
      ) {
        throw new Error("E_WORKBENCH_RUN_RECEIPT_BINDING_REQUIRED");
      }
      run.shared_runtime_result = {
        schema: String(sharedRunSummary.schema ?? ""),
        source_profile_identity: String(sharedRunSummary.source_profile_identity ?? ""),
        source_identity: String(sharedRunSummary.execution_envelope?.source_bytes_sha256 ?? ""),
        state_hash: String(sharedRunSummary.state_hash ?? ""),
        output_log_texts: Array.isArray(sharedRunSummary.output_log_texts)
          ? [...sharedRunSummary.output_log_texts]
          : [],
      };
      run.work_cost_receipt = structuredClone(sharedRunSummary.work_cost_receipt);
      firstFrame = appendFrame(
        run,
        committedState,
        makeSnapshot(branchFrom ? "branch_start" : "run_start", queuedInput),
      );
      run.committed_step_count = isOneshot ? 1 : 0;
      if (queuedInput?.input_id && state.nextInput?.input_id === queuedInput.input_id) {
        state.nextInput = null;
      }
    }
    try {
      await persistRunCheckpoint(run, firstFrame);
    } catch (archiveErr) {
      run.server_archive_status = "checkpoint-error";
      pushDiagnostic("E_RUN_ARCHIVE_CHECKPOINT_FAILED", String(archiveErr?.message ?? archiveErr), "error");
    }
    assertExecutionGeneration(executionGeneration, projectIdAtStart);
    if (run.execution_mode_decision.mode === "oneshot") {
      try {
        await finalizeRunRecord(run, "completed");
      } catch (archiveErr) {
        pushDiagnostic("E_RUN_ARCHIVE_FINALIZE_FAILED", String(archiveErr?.message ?? archiveErr), "error");
      }
      assertExecutionGeneration(executionGeneration, projectIdAtStart);
    }
    applyExecutionEvent(EXECUTION_EVENTS.PREPARED, {
      mode: run.execution_mode_decision.mode,
      runId: run.run_id,
    });
    if (run.execution_mode_decision.mode === "live") {
      if (runReachedDone(run, firstFrame?.wasm_state)) {
        applyExecutionEvent(EXECUTION_EVENTS.RUNTIME_DONE, { reason: "configured_madi_reached" });
        try {
          await finalizeRunRecord(run, "completed");
        } catch (archiveErr) {
          pushDiagnostic("E_RUN_ARCHIVE_FINALIZE_FAILED", String(archiveErr?.message ?? archiveErr), "error");
        }
      } else {
        scheduleLivePump();
      }
    }
    sourceReadinessRunOutcome("run_started", {
      source_hash: sourceReadiness.source_hash,
    });
    state.pendingRecipe = null;
    if (state.projectControls?.project_id === project.id) {
      state.projectControls.control_values = Object.fromEntries(
        (state.projectControls.controls ?? []).map((control) => [control.name, control.value]),
      );
    }
    return true;
  } catch (err) {
    const superseded = err?.code === "E_EXECUTION_GENERATION_SUPERSEDED"
      || !executionGenerationIsCurrent(executionGeneration, projectIdAtStart);
    if (superseded) {
      try {
        await finalizeRunRecord(run, "stopped");
      } catch (_) {
        // The current lifecycle owns diagnostics after a generation change.
      }
      return false;
    }
    applyExecutionEvent(EXECUTION_EVENTS.PREPARE_FAILED, { reason: "prepare_failed" });
    const diagnostic = projectDiagnosticFromError(err);
    if (projectSource) {
      state.projectExecution.current = null;
      state.projectExecution.failure = {
        schema: "seamgrim.workbench.current_project_execution_failure.v1",
        state: "current_failure",
        source_hash: projectSourceHash,
        diagnostic,
        previous_success_lineage_hash: String(state.projectExecution?.previousSuccess?.evidence?.run_lineage?.lineage_hash ?? ""),
      };
    }
    if (run) {
      run.final_status = "failed";
      run.failure = diagnostic;
      await finalizeFailedRunArchive(run, diagnostic);
    }
    pushDiagnostic(diagnostic.code, diagnostic.message, "error");
    return false;
  } finally {
    if (executionGenerationIsCurrent(executionGeneration, projectIdAtStart)) {
      state.runtimeBusy = false;
      renderAll();
    }
  }
}

async function commitNextLiveStep({ origin = "auto", token = livePumpToken() } = {}) {
  const allowPaused = origin === "manual";
  const run = activeRun();
  if (!run || run.execution_mode_decision?.mode !== "live") return false;
  if (!livePumpTokenIsCurrent(token, { allowPaused, allowPausing: origin === "auto" })) return false;
  const queuedInput = state.nextInput ? { ...state.nextInput } : null;
  const inputPayload = queuedInput
    ? {
        keys: queuedInput.keys,
        lastKey: queuedInput.lastKey,
        px: queuedInput.px,
        py: queuedInput.py,
        dt: queuedInput.dt,
      }
    : null;
  const snapshot = makeSnapshot(queuedInput?.intent ?? (origin === "manual" ? "step" : "auto_step"), queuedInput);
  try {
    const plan = run.source_kind === "virtual_project_source"
      && run.project_execution_plan
      && typeof run.project_execution_plan === "object"
      ? run.project_execution_plan
      : null;
    const executionSource = plan
      ? String(plan.linked_execution_source ?? "")
      : String(run.execution_source ?? "");
    if (!executionSource.trim()) {
      throw new Error("E_RUN_EXECUTION_SOURCE_MISSING: 봉인된 실행 원문이 없습니다");
    }
    const wasm = state.wasm;
    if (!wasm) throw new Error("E_RUN_VM_MISSING: 활성 실행의 봉인 VM이 없습니다");
    const wasmState = await wasm.step({
      n: 1,
      input: inputPayload,
      sourceText: executionSource,
    });
    if (!livePumpTokenIsCurrent(token, { allowPaused, allowPausing: origin === "auto" })) return false;

    const frame = buildFrame(run, wasmState, snapshot);
    let evidence = null;
    if (plan) {
      evidence = await buildCurrentProjectRunEvidence({
        prepared: plan,
        run,
        frame,
        wasmState,
        vmLifecycle: "serial_step(1)",
      });
      if (!livePumpTokenIsCurrent(token, { allowPaused, allowPausing: origin === "auto" })) return false;
    }

    run.frames.push(frame);
    run.committed_step_count = Number(run.committed_step_count ?? 0) + 1;
    state.cursorIndex = run.frames.length - 1;
    state.livePump.stepCommitCount += 1;
    if (queuedInput?.input_id && state.nextInput?.input_id === queuedInput.input_id) {
      state.nextInput = null;
    }
    if (plan && evidence) {
      state.projectExecution.current = {
        schema: "seamgrim.workbench.current_project_execution.v1",
        state: "current_success",
        source_hash: run.project_source_hash,
        prepare_link_sha256: String(plan.prepare_link_sha256 ?? ""),
        project_graph_hash: String(plan.project_graph?.project_graph_sha256 ?? ""),
        linked_source_hash: String(plan.linked_execution_source_sha256 ?? ""),
        run_id: run.run_id,
        evidence,
      };
      state.projectExecution.failure = null;
    }
    try {
      await persistRunCheckpoint(run, frame);
    } catch (archiveErr) {
      run.server_archive_status = "checkpoint-error";
      pushDiagnostic("E_RUN_ARCHIVE_CHECKPOINT_FAILED", String(archiveErr?.message ?? archiveErr), "error");
    }

    if (runReachedDone(run, wasmState)
      && livePumpTokenIsCurrent(token, { allowPaused: true, allowPausing: true })) {
      applyExecutionEvent(EXECUTION_EVENTS.RUNTIME_DONE, { reason: "configured_madi_reached" });
      cancelLivePump("runtime_done");
      try {
        await finalizeRunRecord(run, "completed");
      } catch (archiveErr) {
        pushDiagnostic("E_RUN_ARCHIVE_FINALIZE_FAILED", String(archiveErr?.message ?? archiveErr), "error");
      }
    }
    return true;
  } catch (err) {
    if (!livePumpTokenIsCurrent(token, { allowPaused: true, allowPausing: true })) return false;
    applyExecutionEvent(EXECUTION_EVENTS.RUNTIME_FAILED, { reason: "step_failed" });
    cancelLivePump("runtime_failed");
    run.failure = projectDiagnosticFromError(err, "E_WASM_STEP_FAILED");
    await finalizeFailedRunArchive(run, run.failure);
    pushDiagnostic(run.failure.code, run.failure.message, "error");
    return false;
  }
}

async function stepForward() {
  const run = activeRun();
  if (run && state.cursorIndex >= 0 && state.cursorIndex < run.frames.length - 1) {
    pushDiagnostic("E_RUN_HISTORY_READ_ONLY", "과거 마디는 읽기 전용입니다. branch를 만들어 계속하세요.", "error");
    cancelLivePump("history_cursor");
    applyExecutionEvent(EXECUTION_EVENTS.HISTORY_OPENED);
    renderAll();
    return false;
  }
  if (!run) {
    pushDiagnostic("E_RUN_STEP_WITHOUT_ACTIVE_RUN", "한 마디 진행할 활성 실행이 없습니다.", "error");
    renderAll();
    return false;
  }
  const requested = applyExecutionEvent(EXECUTION_EVENTS.STEP_REQUESTED, {
    atLatestCursor: state.cursorIndex === run.frames.length - 1,
  });
  if (!requested.accepted) return false;
  const committed = await beginCommittedLiveStep("manual");
  if (committed && state.executionLifecycle.status === EXECUTION_STATES.PAUSED) {
    applyExecutionEvent(EXECUTION_EVENTS.STEP_COMMITTED, { atLatestCursor: true });
    renderAll();
  }
  return committed;
}

function pauseRun() {
  const requested = applyExecutionEvent(EXECUTION_EVENTS.PAUSE_REQUESTED);
  if (!requested.accepted) return false;
  cancelLivePump("pause_requested", { invalidateInFlight: false });
  renderAll();
  if (!state.livePump.inFlight) {
    queueMicrotask(() => {
      const committed = applyExecutionEvent(EXECUTION_EVENTS.PAUSE_COMMITTED);
      if (committed.accepted) renderAll();
    });
  }
  return true;
}

function resumeRun() {
  const run = activeRun();
  if (!run) return false;
  if (state.cursorIndex < run.frames.length - 1) {
    pushDiagnostic("E_RUN_HISTORY_RESUME_REJECTED", "과거 마디에서 같은 run을 재개할 수 없습니다.", "error");
    applyExecutionEvent(EXECUTION_EVENTS.HISTORY_OPENED);
    renderAll();
    return false;
  }
  const resumed = applyExecutionEvent(EXECUTION_EVENTS.RESUME, { atLatestCursor: true });
  if (resumed.accepted) scheduleLivePump();
  renderAll();
  return resumed.accepted;
}

async function stopRun() {
  const requested = applyExecutionEvent(EXECUTION_EVENTS.STOP_REQUESTED);
  if (!requested.accepted) return false;
  const inFlightStep = state.livePump.inFlightPromise;
  cancelLivePump("stop_requested");
  const stopGeneration = state.executionLifecycle.generation;
  const projectIdAtStop = state.projectId;
  state.runtimeBusy = true;
  renderAll();
  try {
    if (inFlightStep) await inFlightStep.catch(() => false);
    await finalizeActiveRun("stopped");
  } catch (archiveErr) {
    pushDiagnostic("E_RUN_ARCHIVE_FINALIZE_FAILED", String(archiveErr?.message ?? archiveErr), "error");
  } finally {
    if (executionGenerationIsCurrent(stopGeneration, projectIdAtStop)) {
      applyExecutionEvent(EXECUTION_EVENTS.STOP_COMMITTED, { finalStatus: "stopped" });
      state.runtimeBusy = false;
      renderAll();
    }
  }
  return true;
}

function backOneMadi() {
  const run = activeRun();
  const policy = executionControlPolicy(state.executionLifecycle, executionLifecycleContext());
  if (!run || !policy.canBack) return false;
  cancelLivePump("history_cursor");
  state.cursorIndex = Math.max(0, state.cursorIndex - 1);
  applyExecutionEvent(EXECUTION_EVENTS.HISTORY_OPENED);
  pushDiagnostic("W_RUN_HISTORY_READ_ONLY", "한 마디 뒤로 이동했습니다. 현재 run은 읽기 전용입니다.");
  renderAll();
  return true;
}

async function branchFromCursor() {
  const run = activeRun();
  const frame = activeFrame();
  const policy = executionControlPolicy(state.executionLifecycle, executionLifecycleContext());
  if (!run || !frame || !policy.canBranch) return false;
  try {
    await finalizeActiveRun("stopped");
  } catch (archiveErr) {
    pushDiagnostic("E_RUN_ARCHIVE_FINALIZE_FAILED", String(archiveErr?.message ?? archiveErr), "error");
  }
  return startRun({
    branchFrom: {
      run_id: run.run_id,
      server_run_id: run.server_run_id ?? "",
      madi: frame.madi,
      state_hash: frame.state_hash,
    },
  });
}

function applySetupRecipe() {
  const model = state.projectControls;
  if (model?.project_id !== state.projectId || !Array.isArray(model.controls) || !model.controls.length) {
    pushDiagnostic("E_SETUP_CONTROL_UNAVAILABLE", "현재 프로젝트가 선언한 매김 조절이 없습니다.", "error");
    renderAll();
    return null;
  }
  const values = { ...model.control_values };
  for (const input of els.setupControlList?.querySelectorAll?.("input[data-control-name]") ?? []) {
    const value = Number(input.value);
    if (Number.isFinite(value)) values[String(input.dataset.controlName)] = value;
  }
  const recipe = buildSetupRecipe(model, values);
  if (!recipe) return null;
  state.recipeVersion += 1;
  state.projectControls.control_values = { ...recipe.values };
  state.pendingRecipe = recipe;
  pushDiagnostic("W_SETUP_NEW_RECIPE", "조절값 변경은 다음 run recipe로만 적용됩니다.");
  renderAll();
  return recipe;
}

function setNextAction(actionId) {
  const action = actionById(state.projectControls, actionId);
  if (!action || state.projectControls?.project_id !== state.projectId) return null;
  const input = action.input_snapshot;
  state.actionSeq += 1;
  state.nextInput = {
    input_id: `input_${String(state.actionSeq).padStart(6, "0")}`,
    project_id: state.projectId,
    action_id: action.action_id,
    action_map_hash: String(state.projectControls.action_map?.action_map_hash ?? ""),
    intent: input.intent,
    keys: input.keys,
    lastKey: input.last_key,
    px: input.pointer_x,
    py: input.pointer_y,
    dt: input.dt,
  };
  renderAll();
  return state.nextInput;
}

async function applyRunRecipeToWasm(wasm, recipe = null) {
  const controls = Array.isArray(recipe?.controls) ? recipe.controls : [];
  for (const control of controls) {
    await wasm.setParam({ key: control.name, value: control.value });
  }
  return controls.length;
}

function attemptOverwriteActiveRun() {
  pushDiagnostic("E_RUN_IMMUTABLE_OVERWRITE_REJECTED", "기존 run record는 덮어쓸 수 없습니다.", "error");
  return false;
}

function attemptReuseRunId(runId = state.activeRunId) {
  const exists = state.runs.some((run) => run.run_id === runId);
  if (exists) {
    pushDiagnostic("E_RUN_ID_REUSE_REJECTED", "같은 run id는 다시 쓸 수 없습니다.", "error");
    return false;
  }
  return true;
}

function attemptMutateParentHash() {
  const run = activeRun();
  if (run?.parent_run_id) {
    pushDiagnostic("E_PARENT_HASH_MUTATION_REJECTED", "parent state_hash는 branch 생성 뒤 바꿀 수 없습니다.", "error");
    return false;
  }
  pushDiagnostic("W_PARENT_HASH_MUTATION_NO_PARENT", "parent가 없는 run입니다.");
  return false;
}

function buildProjectSnapshot() {
  const project = currentProject();
  const payload = {
    schema: "seamgrim.approved_workbench.project_snapshot.v1",
    project_id: project.id,
    active_file_path: state.activeFilePath,
    mode: state.mode,
    view_role: legacySelectedView(state.viewWorkspace),
    view_workspace: serializeViewWorkspace(state.viewWorkspace),
    recipe_version: state.recipeVersion,
    files: project.files.map((file) => ({
      path: file.path,
      role: file.role,
      text: state.fileTexts.get(file.path) ?? "",
    })),
    virtual_project_source_hash: currentVirtualProjectSourceHash(project),
    project_execution: {
      current_state: state.projectExecution?.current?.state ?? "",
      current_source_hash: state.projectExecution?.current?.source_hash ?? "",
      previous_success_source_hash: state.projectExecution?.previousSuccess?.source_hash ?? "",
      failure_source_hash: state.projectExecution?.failure?.source_hash ?? "",
      imported_record_source_hash: state.projectExecution?.importedRecord?.source_hash ?? "",
    },
    runs: state.runs.map((run) => ({
      run_id: run.run_id,
      parent_run_id: run.parent_run_id,
      parent_madi: run.parent_madi,
      parent_state_hash: run.parent_state_hash,
      frame_count: run.frames.length,
      latest_state_hash: run.frames.at(-1)?.state_hash ?? "",
      recipe_hash: run.recipe_hash,
      source_hash: run.source_hash,
    })),
  };
  const canonical = stableCanonicalJson(payload);
  return {
    ...payload,
    canonical_hash: `candidate:fnv1a32:${stableHash(canonical)}`,
  };
}

function hydrateProductViewWorkspace(project, snapshot, legacySelection, sourceLabel) {
  const result = hydrateViewWorkspaceWithMigration(project, snapshot, legacySelection);
  if (result.migration) {
    pushDiagnostic(
      result.migration.code,
      `${result.migration.message} (${sourceLabel})`,
    );
  }
  return result.workspace;
}

function workbenchProjectFiles(project = currentProject()) {
  return project.files.map((file) => ({
    path: file.path,
    role: file.role,
    text: state.fileTexts.get(file.path) ?? "",
  }));
}

async function sha256HexUtf8(text = "") {
  const subtle = globalThis?.crypto?.subtle;
  if (!subtle || typeof subtle.digest !== "function") return "";
  const digest = await subtle.digest("SHA-256", new TextEncoder().encode(String(text ?? "")));
  return Array.from(new Uint8Array(digest))
    .map((byte) => byte.toString(16).padStart(2, "0"))
    .join("");
}

async function currentLocalProjectTreePayload(project = currentProject()) {
  const payload = localProjectTreePayloadFromSnapshot(project.portableSnapshot ?? {});
  if (!payload) return null;
  const files = [];
  for (const file of Array.isArray(payload.files) ? payload.files : []) {
    const pathValue = String(file?.path ?? "").trim();
    if (!pathValue) continue;
    const text = String(state.fileTexts.get(pathValue) ?? file?.utf8_text ?? file?.text ?? "");
    files.push({
      ...file,
      path: pathValue,
      role: String(file?.role ?? "ddn_source").trim() || "ddn_source",
      utf8_text: text,
      byte_length: new TextEncoder().encode(text).length,
      sha256: await sha256HexUtf8(text),
    });
  }
  const evidence = localProjectRunEvidenceFromProject(project);
  if (evidence) {
    const projectGraphSha256 = String(evidence.execution_preparation?.project_graph_sha256 || payload.project_graph_sha256 || "");
    const lockSha256 = String(evidence.execution_preparation?.lock_sha256 || evidence.run_lineage?.lock_hash || payload.lock_sha256 || "");
    return {
      ...payload,
      files,
      project_graph_sha256: projectGraphSha256,
      lock_sha256: lockSha256,
      bounded_state_sha256: evidence.bounded_state_sha256,
      runtime_state_hash: evidence.runtime_state_hash,
      summary_sha256: evidence.summary_sha256,
      output_rows: evidence.output_rows,
      project_observation_trace: evidence.project_observation_trace ?? {
        schema: "ddn.local_project.observation_trace.v1",
        trace_sha256: evidence.trace_sha256,
        rows: evidence.observation_rows,
      },
      execution_preparation: evidence.execution_preparation,
      run_lineage: evidence.run_lineage,
      frontdoor: evidence.frontdoor,
      state_hash_formula_change: false,
    };
  }
  return {
    ...payload,
    files,
  };
}

function currentProjectControlSnapshot() {
  const model = state.projectControls?.project_id === state.projectId
    ? state.projectControls
    : emptyProjectControlModel(state.projectId);
  return {
    authoring_plan_hash: String(model.authoring_plan_hash ?? ""),
    authoring_source: String(model.source ?? ""),
    controls: (Array.isArray(model.controls) ? model.controls : []).map((control) => ({
      name: control.name,
      value: Number(model.control_values?.[control.name] ?? control.value),
    })),
    action_map: model.action_map
      ? {
          schema: model.action_map.schema,
          project_id: model.action_map.project_id,
          actions: model.action_map.actions.map((action) => ({
            action_id: action.action_id,
            label: action.label,
            glyph: action.glyph,
            input_snapshot: { ...action.input_snapshot },
          })),
        }
      : null,
  };
}

async function buildServerProjectArtifact() {
  const project = currentProject();
  const localProjectTreePayload = await currentLocalProjectTreePayload(project);
  return buildWorkbenchProjectArtifact({
    projectId: project.id,
    projectName: project.title,
    files: workbenchProjectFiles(project),
    controlsSnapshot: {
      selected_view: legacySelectedView(state.viewWorkspace),
      view_workspace: serializeViewWorkspace(state.viewWorkspace),
      run_mode: state.mode,
      recipe_version: state.recipeVersion,
      ...currentProjectControlSnapshot(),
    },
    localPackagePayload: localProjectTreePayload ?? project.portableSnapshot?.local_package_payload ?? null,
    lineage: currentPortableLineage(project),
    metadata: currentPortableMetadata(project),
  });
}

function buildPortableProjectInput(project = currentProject()) {
  const metadata = currentPortableMetadata(project);
  const sourceText = activeSourceText();
  return {
    projectName: metadata.title || project.title,
    ddnText: sourceText,
    lessonPlanText: String(project.lessonPlanText ?? project.portableSnapshot?.lesson_plan_text ?? ""),
    sourceLessonId: project.id === ONE_FILE_DDN_PROJECT_ID ? "custom" : project.id,
    controlsSnapshot: {
      selected_view: legacySelectedView(state.viewWorkspace),
      view_workspace: serializeViewWorkspace(state.viewWorkspace),
      run_mode: state.mode,
      recipe_version: state.recipeVersion,
      ...currentProjectControlSnapshot(),
      view_authoring: {
        primary_view: project.primaryView,
        view_grade: project.viewGrade,
      },
    },
    localPackagePayload: project.portableSnapshot?.local_package_payload ?? null,
    curriculumInquiryArtifact: project.portableSnapshot?.curriculum_inquiry_artifact ?? null,
    curriculumArtifactBundle: project.portableSnapshot?.curriculum_artifact_bundle ?? null,
    curriculumModelComparison: project.portableSnapshot?.curriculum_model_comparison ?? null,
    curriculumSemanticScene: project.portableSnapshot?.curriculum_semantic_scene ?? null,
    lineage: {
      ...(project.portableSnapshot?.lineage ?? {}),
      ...currentPortableLineage(project),
    },
    metadata,
  };
}

function renderPortableExportStatus() {
  if (!els.portableExportStatus) return;
  const row = state.lastPortableExport;
  if (!row) {
    els.portableExportStatus.textContent = "portable: -";
    return;
  }
  const hash = String(row.file?.content_sha256 ?? "").slice(0, 12) || "-";
  const bytes = Number(row.file?.byte_length ?? 0);
  els.portableExportStatus.textContent = `portable: ${hash} · ${bytes}B`;
}

function renderPortableImportPreview() {
  const preview = els.portableImportPreview;
  if (!preview) return;
  const row = state.pendingPortableImport;
  preview.classList.toggle("hidden", !row);
  preview.dataset.state = row?.error ? "error" : row ? "ready" : "";
  if (!row) return;
  if (row.error) {
    els.portableImportTitle.textContent = "가져오기 실패";
    els.portableImportIntegrity.textContent = `진단: ${row.error.code}`;
    els.portableImportTrust.textContent = "현재 작업 보존됨";
    els.portableImportDetails.textContent = row.error.message;
    els.portableOpen.disabled = true;
    return;
  }
  const artifact = row.artifact;
  const snapshot = artifact.project_snapshot ?? {};
  const metadata = snapshot.metadata ?? {};
  const title = String(metadata.title || snapshot.project_name || "받은 셈그림 프로젝트");
  const tags = normalizePortableTextArray(metadata.tags).join(", ") || "-";
  const fields = row.validation?.field_audit?.present_current_fields ?? [];
  const localProjectPayload = localProjectTreePayloadFromSnapshot(snapshot);
  els.portableImportTitle.textContent = title;
  els.portableImportIntegrity.textContent = `파일 무결성 확인됨 · ${String(artifact.content_sha256 || "").slice(0, 12)}`;
  els.portableImportTrust.textContent = "받은 프로젝트 · 공식 여부 확인 안 됨";
  if (localProjectPayload) {
    const entry = String(localProjectPayload.entry_path ?? "-");
    const fileCount = Array.isArray(localProjectPayload.files) ? localProjectPayload.files.length : 0;
    const hasLock = (localProjectPayload.files ?? []).some((file) => String(file?.path ?? "") === "ddn.lock");
    const gajiCount = gajiIdsFromLocalProjectPayload(localProjectPayload).length;
    els.portableImportDetails.textContent =
      `설명: ${String(metadata.summary || "-")} · 태그: ${tags} · entry ${entry} · files ${fileCount} · lock ${hasLock ? "checked" : "missing"} · 가지 ${gajiCount} · 부속 필드 ${fields.length}종`;
  } else {
    els.portableImportDetails.textContent = `설명: ${String(metadata.summary || "-")} · 태그: ${tags} · source ${String(snapshot.ddn_text || "").length}자 · 부속 필드 ${fields.length}종`;
  }
  els.portableOpen.disabled = false;
}

function renderPortableMetadataEditor() {
  const metadata = currentPortableMetadata();
  if (els.portableMetaTitle && document.activeElement !== els.portableMetaTitle) els.portableMetaTitle.value = metadata.title;
  if (els.portableMetaSummary && document.activeElement !== els.portableMetaSummary) els.portableMetaSummary.value = metadata.summary;
  if (els.portableMetaContentKind) els.portableMetaContentKind.value = metadata.content_kinds[0] || "simulation";
  if (els.portableMetaTags && document.activeElement !== els.portableMetaTags) els.portableMetaTags.value = metadata.tags.join(", ");
  if (els.portableMetaSubject && document.activeElement !== els.portableMetaSubject) els.portableMetaSubject.value = metadata.subject;
  if (els.portableMetaLevel && document.activeElement !== els.portableMetaLevel) els.portableMetaLevel.value = metadata.level;
  if (els.portableMetaRequiredViews && document.activeElement !== els.portableMetaRequiredViews) els.portableMetaRequiredViews.value = metadata.required_views.join(", ");
  if (els.portableMetaRequiredGaji && document.activeElement !== els.portableMetaRequiredGaji) els.portableMetaRequiredGaji.value = metadata.required_gaji.join(", ");
  if (els.portableMetadataStatus) {
    els.portableMetadataStatus.textContent = `metadata: ${metadata.content_kinds[0]} · ${metadata.tags.length} tags · artifact hash 입력`;
  }
}

function triggerPortableDownload({ jsonText = "", filename = "seamgrim-project.seamgrim-project.json" } = {}) {
  return hostBridge.downloadTextFile({
    text: jsonText,
    filename,
    mimeType: "application/json;charset=utf-8",
  });
}

async function buildCurrentPortableProjectArtifact() {
  const input = buildPortableProjectInput();
  const localProjectTreePayload = await currentLocalProjectTreePayload();
  if (localProjectTreePayload) {
    input.localPackagePayload = localProjectTreePayload;
  }
  const result = await buildPortableProjectArtifact(input);
  state.lastPortableExport = result;
  renderPortableExportStatus();
  return result;
}

async function exportPortableProject({ download = true } = {}) {
  try {
    const result = await buildCurrentPortableProjectArtifact();
    if (download) {
      triggerPortableDownload({
        jsonText: result.file.json_text,
        filename: result.file.filename,
      });
    }
    pushDiagnostic("W_PORTABLE_PROJECT_EXPORTED", `휴대형 프로젝트 ${result.file.filename} 내보내기 준비 완료`);
    renderPortableExportStatus();
    return result;
  } catch (err) {
    const diagnostic = portableProjectDiagnostic(err);
    pushDiagnostic(diagnostic.code, diagnostic.message, "error");
    renderPortableExportStatus();
    throw err;
  }
}

async function previewPortableProjectFile(file) {
  if (!file) {
    state.pendingPortableImport = null;
    renderPortableImportPreview();
    return null;
  }
  try {
    const bytes = await hostBridge.readFileBytes(file);
    const parsed = await parsePortableProjectArtifactBytes(bytes);
    state.pendingPortableImport = {
      schema: "seamgrim.workbench.pending_portable_import.v1",
      file_name: String(file.name || ""),
      artifact: parsed.artifact,
      validation: parsed.validation,
      byte_length: parsed.byte_length,
    };
    renderPortableImportPreview();
    pushDiagnostic("W_PORTABLE_PROJECT_PREVIEW_READY", "파일 무결성을 확인했습니다. 열기 전까지 실행하지 않습니다.");
    return state.pendingPortableImport;
  } catch (err) {
    const diagnostic = portableProjectDiagnostic(err);
    state.pendingPortableImport = {
      schema: "seamgrim.workbench.pending_portable_import.v1",
      file_name: String(file.name || ""),
      error: diagnostic,
    };
    renderPortableImportPreview();
    pushDiagnostic(diagnostic.code, diagnostic.message, "error");
    return null;
  } finally {
    if (els.portableImportInput) {
      els.portableImportInput.value = "";
    }
  }
}

async function openPendingPortableProject() {
  const pending = state.pendingPortableImport;
  if (!pending?.artifact || pending.error) return null;
  const artifact = pending.artifact;
  const importedAt = new Date().toISOString();
  const hashPrefix = String(artifact.content_sha256 || "portable").slice(0, 12) || "portable";
  const duplicateCount = readPortableProjectCatalog()
    .filter((row) => String(row.content_sha256 || "") === String(artifact.content_sha256 || ""))
    .length;
  const project = portableProjectFromArtifact(artifact, {
    catalogId: `portable_${hashPrefix}_${String(duplicateCount + 1).padStart(2, "0")}`,
    importedAt,
  });
  receivedPortableProjects = [
    project,
    ...receivedPortableProjects.filter((row) => row.id !== project.id),
  ];
  rememberPortableProject(project);
  state.pendingPortableImport = null;
  await selectProject(project.id);
  state.persistenceStatus = {
    schema: "seamgrim.workbench.persistence_status.v1",
    mode: "portable_import",
    server_saved: false,
    local_saved: true,
    user_label: `받은 프로젝트 ${hashPrefix}`,
  };
  state.runs = [];
  state.activeRunId = "";
  state.cursorIndex = -1;
  seedImportedProjectExecutionRecord(project);
  pushDiagnostic("W_PORTABLE_PROJECT_IMPORTED", "받은 프로젝트로 열었습니다. 실행은 사용자가 직접 시작해야 합니다.");
  renderAll();
  return project;
}

function updatePortableMetadataDraftFromInputs() {
  state.portableMetadataDraft = normalizePortableMetadataDraft({
    title: els.portableMetaTitle?.value ?? "",
    summary: els.portableMetaSummary?.value ?? "",
    content_kinds: [els.portableMetaContentKind?.value ?? "simulation"],
    tags: portableListFromText(els.portableMetaTags?.value ?? "", 8),
    subject: els.portableMetaSubject?.value ?? "",
    level: els.portableMetaLevel?.value ?? "",
    required_views: portableListFromText(els.portableMetaRequiredViews?.value ?? "", 8),
    required_gaji: portableListFromText(els.portableMetaRequiredGaji?.value ?? "", 8),
    determinism_grade: currentProject().viewGrade,
  });
  state.lastPortableExport = null;
  renderPortableExportStatus();
  renderPortableMetadataEditor();
}

function updateServerStateFromPayload(payload = {}, capabilities = {}) {
  state.serverProject = {
    ...state.serverProject,
    projectId: String(payload.project_id ?? state.serverProject.projectId ?? ""),
    headRevisionId: String(payload.revision_id ?? payload.head_revision_id ?? state.serverProject.headRevisionId ?? ""),
    contentSha256: String(payload.content_sha256 ?? state.serverProject.contentSha256 ?? ""),
    packageHash: String(payload.package_hash ?? state.serverProject.packageHash ?? ""),
    editCapability: String(capabilities.editCapability ?? payload.edit_capability ?? state.serverProject.editCapability ?? ""),
    viewCapability: String(capabilities.viewCapability ?? payload.view_capability ?? state.serverProject.viewCapability ?? ""),
    role: String(payload.capability_role ?? state.capabilitySession?.role ?? state.serverProject.role ?? ""),
  };
  if (state.serverProject.projectId && state.serverProject.editCapability) {
    state.capabilitySession = writeWorkbenchCapabilitySession({
      projectId: state.serverProject.projectId,
      role: "edit",
      capability: state.serverProject.editCapability,
    }) ?? state.capabilitySession;
  }
  if (state.serverProject.projectId && (state.serverProject.editCapability || state.serverProject.viewCapability)) {
    rememberMyWorkProject({
      projectId: state.serverProject.projectId,
      title: currentProject().title,
      headRevisionId: state.serverProject.headRevisionId,
      editCapability: state.serverProject.editCapability,
      viewCapability: state.serverProject.viewCapability,
    });
  }
}

function applyProjectSnapshot(snapshot = {}) {
  const sourceLessonId = String(snapshot.source_lesson_id ?? "").trim();
  const localProjectPayload = localProjectTreePayloadFromSnapshot(snapshot);
  const known = allProjects().find((project) => project.id === sourceLessonId);
  let project = known ?? currentProject();
  if (localProjectPayload) {
    const hashSource = String(snapshot.project_graph_sha256 ?? localProjectPayload.project_graph_sha256 ?? sourceLessonId ?? "").trim() || "server";
    const hashPrefix = hashSource.slice(0, 12) || "server";
    project = {
      id: sourceLessonId && sourceLessonId !== "custom" ? sourceLessonId : `server_local_project_${hashPrefix}`,
      title: String(snapshot.project_name ?? "저장된 로컬 프로젝트"),
      kind: "저장된 로컬 프로젝트",
      summary: "서버 snapshot에서 복원한 여러 파일 DDN 프로젝트입니다.",
      tags: ["저장", "로컬 프로젝트"],
      primaryView: known?.primaryView ?? "line",
      viewGrade: "portable-verified",
      viewPolicy: known?.viewPolicy ?? {
        primary: "복원된 DDN 보개",
        side: "복원된 관찰값",
        overlay: "복원된 보기 후보",
        magnifier: "복원된 보기 확대",
      },
      portableMetadata: snapshot.metadata ?? {},
      portableSnapshot: snapshot,
      portableArtifact: null,
      files: filesFromLocalProjectPayload(localProjectPayload, snapshot),
    };
    receivedPortableProjects = [
      project,
      ...receivedPortableProjects.filter((row) => row.id !== project.id),
    ];
  }
  const supersededRun = activeRun();
  cancelLivePump("project_snapshot_replaced");
  applyExecutionEvent(EXECUTION_EVENTS.PROJECT_SWITCHED);
  state.runtimeBusy = false;
  state.runs = [];
  state.activeRunId = "";
  state.cursorIndex = -1;
  state.wasm = null;
  finalizeRunRecord(supersededRun, "stopped").catch((archiveErr) => {
    pushDiagnostic("E_RUN_ARCHIVE_FINALIZE_FAILED", String(archiveErr?.message ?? archiveErr), "error");
  });
  state.projectId = project.id;
  state.activeFilePath = localProjectPayload
    ? String(localProjectPayload.entry_path ?? project.files[0]?.path ?? "lesson.ddn")
    : "lesson.ddn";
  state.fileTexts.clear();
  for (const file of project.files) {
    state.fileTexts.set(
      file.path,
      localProjectPayload
        ? String(file.fallback ?? "")
        : file.path === "lesson.ddn"
          ? String(snapshot.ddn_text ?? "")
          : String(file.fallback ?? ""),
    );
  }
  state.mode = ["ddn-main", "bogae-main", "bogae-full"].includes(snapshot.controls_snapshot?.run_mode)
    ? snapshot.controls_snapshot.run_mode
    : "ddn-main";
  state.viewWorkspace = hydrateProductViewWorkspace(
    project,
    snapshot.controls_snapshot?.view_workspace,
    snapshot.controls_snapshot?.selected_view ?? snapshot.controls_snapshot?.view_role ?? "",
    "project_snapshot",
  );
  state.pendingRecipe = null;
  state.nextInput = null;
  state.projectControlsGeneration += 1;
  state.projectControls = emptyProjectControlModel(project.id, "loading");
  scheduleProjectControlsRefresh();
  resetProjectExecutionState({ keepImportedRecord: false });
  seedImportedProjectExecutionRecord(project);
}

async function refreshServerRevisions() {
  const session = state.capabilitySession ?? readWorkbenchCapabilitySession();
  const projectId = state.serverProject.projectId || session?.project_id || "";
  const capability = session?.capability || state.serverProject.editCapability || state.serverProject.viewCapability || "";
  if (!projectId || !capability) {
    state.serverProject.revisions = [];
    renderServerProject();
    return [];
  }
  const payload = await listServerRevisions({ projectId, capability });
  state.serverProject.revisions = Array.isArray(payload.revisions) ? payload.revisions : [];
  state.serverProject.role = String(payload.capability_role ?? state.serverProject.role ?? "");
  renderServerProject();
  return state.serverProject.revisions;
}

async function recordServerConflict(err, artifact) {
  const session = state.capabilitySession ?? readWorkbenchCapabilitySession();
  const projectId = state.serverProject.projectId || session?.project_id || "";
  let head = null;
  if (projectId && session?.capability) {
    try {
      head = await openServerProject({ projectId, capability: session.capability });
      updateServerStateFromPayload(head, {
        editCapability: session.role === "edit" ? session.capability : "",
        viewCapability: session.role === "view" ? session.capability : "",
      });
      await refreshServerRevisions();
    } catch (_) {
      // The original conflict diagnostic remains the user-facing result.
    }
  }
  state.serverProject.conflict = {
    schema: "seamgrim.workbench.project_conflict.v1",
    message: err?.message || "다른 창에서 먼저 저장되었습니다.",
    serverRevisionId: String(head?.head_revision_id ?? state.serverProject.headRevisionId ?? ""),
    serverContentSha256: String(head?.content_sha256 ?? state.serverProject.contentSha256 ?? ""),
    localParentRevisionId: String(state.persistenceStatus?.revision_id ?? state.serverProject.headRevisionId ?? ""),
    localPackageJson: stableCanonicalJson(artifact),
  };
  state.persistenceStatus = {
    schema: "seamgrim.workbench.persistence_status.v1",
    mode: "server_conflict",
    server_saved: false,
    local_saved: false,
    revision_id: state.serverProject.headRevisionId,
    user_label: "다른 창에서 먼저 저장됨",
  };
  els.saveStatus.textContent = "project: 다른 창에서 먼저 저장됨";
  pushDiagnostic(err?.payload?.code ?? "E_PROJECT_REVISION_CONFLICT", state.serverProject.conflict.message, "error");
  renderAll();
  return state.serverProject.conflict;
}

async function restoreProjectRevision(sourceRevisionId = "") {
  const session = state.capabilitySession ?? readWorkbenchCapabilitySession();
  const projectId = state.serverProject.projectId || session?.project_id || "";
  if (!projectId || !session?.capability || session.role !== "edit") {
    pushDiagnostic("E_PROJECT_RESTORE_PERMISSION", "편집 권한이 있어야 리비전을 복원할 수 있습니다.", "error");
    return null;
  }
  const payload = await restoreServerRevision({
    projectId,
    capability: session.capability,
    sourceRevisionId,
    expectedParentRevisionId: state.serverProject.headRevisionId,
  });
  updateServerStateFromPayload(payload, { editCapability: session.capability });
  state.serverProject.conflict = null;
  if (payload.project_snapshot) {
    applyProjectSnapshot(payload.project_snapshot);
  }
  state.persistenceStatus = {
    schema: "seamgrim.workbench.persistence_status.v1",
    mode: "server_restore",
    server_saved: true,
    local_saved: false,
    revision_id: state.serverProject.headRevisionId,
    user_label: `복원됨 ${state.serverProject.headRevisionId}`,
  };
  els.saveStatus.textContent = `project: 복원됨 ${state.serverProject.headRevisionId}`;
  await refreshServerRevisions();
  pushDiagnostic("W_PROJECT_REVISION_RESTORED", `${sourceRevisionId} 새 revision으로 복원 완료`);
  renderAll();
  return payload;
}

async function cloneCurrentServerProject() {
  const session = state.capabilitySession ?? readWorkbenchCapabilitySession();
  const projectId = state.serverProject.projectId || session?.project_id || "";
  if (!projectId || !session?.capability) {
    pushDiagnostic("E_PROJECT_CLONE_NO_CAPABILITY", "복제할 서버 프로젝트 권한이 없습니다.", "error");
    return null;
  }
  const payload = await cloneServerProject({
    projectId,
    capability: session.capability,
    title: `${currentProject().title} 복제본`,
  });
  updateServerStateFromPayload(payload, {
    editCapability: payload.edit_capability,
    viewCapability: payload.view_capability,
  });
  state.serverProject.conflict = null;
  state.runArchives = [];
  if (payload.project_snapshot) {
    applyProjectSnapshot(payload.project_snapshot);
  }
  state.persistenceStatus = {
    schema: "seamgrim.workbench.persistence_status.v1",
    mode: "server_project",
    server_saved: true,
    local_saved: false,
    revision_id: state.serverProject.headRevisionId,
    user_label: `복제본 저장 ${state.serverProject.headRevisionId}`,
  };
  els.saveStatus.textContent = describePersistenceStatus(state.persistenceStatus);
  renderAll();
  await refreshServerRevisions();
  await refreshRunArchives();
  pushDiagnostic("W_PROJECT_CLONED", `복제본 ${state.serverProject.projectId} 생성 완료`);
  renderAll();
  return payload;
}

async function cloneCurrentPortableProject() {
  const source = currentProject();
  if (!source.portableArtifact?.content_sha256) {
    pushDiagnostic("E_PORTABLE_CLONE_NO_ORIGIN", "복제할 받은 프로젝트가 없습니다.", "error");
    return null;
  }
  const hashPrefix = String(source.portableArtifact.content_sha256).slice(0, 12);
  const cloneId = `portable_${hashPrefix}_clone_${String(Date.now()).slice(-6)}`;
  const snapshot = {
    ...(source.portableSnapshot ?? {}),
    lineage: {
      ...(source.portableSnapshot?.lineage ?? {}),
      origin_kind: "portable_clone",
      origin_content_sha256: source.portableArtifact.content_sha256,
    },
  };
  const clone = {
    ...source,
    id: cloneId,
    title: `${source.title} 내 버전`,
    kind: "내 작업",
    tags: Array.from(new Set([...(source.tags ?? []), "내 작업", "리믹스"])),
    portableSnapshot: snapshot,
    portableMetadata: {
      ...(source.portableMetadata ?? {}),
      title: `${source.title} 내 버전`,
      origin_hash_prefix: hashPrefix,
      trust_badge: "local_remix",
    },
  };
  receivedPortableProjects = [clone, ...receivedPortableProjects];
  await selectProject(clone.id);
  seedImportedProjectExecutionRecord(clone);
  state.persistenceStatus = {
    schema: "seamgrim.workbench.persistence_status.v1",
    mode: "portable_local_clone",
    server_saved: false,
    local_saved: true,
    user_label: `받은 프로젝트 내 버전 ${hashPrefix}`,
  };
  pushDiagnostic("W_PORTABLE_PROJECT_CLONED", "받은 프로젝트의 내 버전을 만들었습니다.");
  renderAll();
  return clone;
}

async function openProjectFromServerSession() {
  const session = state.capabilitySession ?? readWorkbenchCapabilitySession();
  if (!session?.project_id || !session?.capability) return null;
  if (!/^sgp_[A-Za-z0-9]{12,24}$/.test(session.project_id)) return null;
  const payload = await openServerProject({
    projectId: session.project_id,
    capability: session.capability,
  });
  updateServerStateFromPayload(payload, {
    editCapability: session.role === "edit" ? session.capability : "",
    viewCapability: session.role === "view" ? session.capability : "",
  });
  if (payload.project_snapshot) {
    applyProjectSnapshot(payload.project_snapshot);
  }
  state.persistenceStatus = {
    schema: "seamgrim.workbench.persistence_status.v1",
    mode: "server_project",
    server_saved: true,
    local_saved: false,
    revision_id: state.serverProject.headRevisionId,
    user_label: `서버 프로젝트 다시 열림 ${state.serverProject.headRevisionId}`,
  };
  els.saveStatus.textContent = describePersistenceStatus(state.persistenceStatus);
  await refreshServerRevisions();
  await refreshRunArchives();
  pushDiagnostic("W_PROJECT_SERVER_OPENED", `server project ${state.serverProject.projectId} 다시 열림`);
  renderAll();
  return payload;
}

function beginPersistenceOperation() {
  const generation = Number(state.persistenceOperation?.generation ?? 0) + 1;
  state.persistenceOperation = {
    generation,
    completedGeneration: Number(state.persistenceOperation?.completedGeneration ?? 0),
    phase: "saving",
    outcome: "",
  };
  return generation;
}

function completePersistenceOperation(generation, phase, outcome) {
  state.persistenceOperation = {
    generation: Math.max(Number(state.persistenceOperation?.generation ?? 0), Number(generation ?? 0)),
    completedGeneration: Number(generation ?? 0),
    phase: String(phase || "saved"),
    outcome: String(outcome || ""),
  };
}

async function saveProjectSnapshot() {
  const persistenceGeneration = beginPersistenceOperation();
  const snapshot = buildProjectSnapshot();
  let artifact = null;
  try {
    artifact = await buildServerProjectArtifact();
    const session = state.capabilitySession ?? readWorkbenchCapabilitySession();
    if (state.serverProject.projectId && session?.role !== "edit") {
      pushDiagnostic("E_PROJECT_VIEW_WRITE_REJECTED", "보기 권한에서는 저장할 수 없습니다.", "error");
      els.saveStatus.textContent = "project: 보기 권한 저장 거부";
      completePersistenceOperation(persistenceGeneration, "rejected", "view_write_forbidden");
      return {
        schema: "seamgrim.workbench.write_rejected.v1",
        code: "E_PROJECT_VIEW_WRITE_REJECTED",
      };
    }
    let payload;
    if (state.serverProject.projectId && session?.role === "edit" && session?.capability) {
      payload = await appendServerRevision({
        projectId: state.serverProject.projectId,
        capability: session.capability,
        artifact,
        expectedParentRevisionId: state.serverProject.headRevisionId,
      });
    } else {
      payload = await createServerProject({
        artifact,
        title: currentProject().title,
      });
    }
    updateServerStateFromPayload(payload);
    state.persistenceStatus = {
      schema: "seamgrim.workbench.persistence_status.v1",
      mode: "server_project",
      server_saved: true,
      local_saved: false,
      revision_id: state.serverProject.headRevisionId,
      user_label: `서버 저장 ${state.serverProject.headRevisionId}`,
      snapshot,
    };
    await refreshServerRevisions();
    completePersistenceOperation(persistenceGeneration, "saved", "server_project");
    renderAll();
    return payload;
  } catch (err) {
    if (Number(err?.status) === 409) {
      const conflict = await recordServerConflict(err, artifact);
      completePersistenceOperation(persistenceGeneration, "conflict", "server_conflict");
      return conflict;
    }
    if (err?.status && ![404, 405, 501, 503].includes(Number(err.status))) {
      pushDiagnostic(err?.payload?.code ?? "E_PROJECT_SERVER_SAVE", err?.message ?? "서버 저장 실패", "error");
      els.saveStatus.textContent = `project: 서버 저장 실패 ${err?.payload?.code ?? err?.status ?? ""}`.trim();
      completePersistenceOperation(persistenceGeneration, "error", String(err?.payload?.code ?? err?.status ?? "server_save_failed"));
      throw err;
    }
    state.persistenceStatus = saveLocalFallbackSnapshot(snapshot.project_id, snapshot);
    completePersistenceOperation(persistenceGeneration, "saved", "local_fallback");
    els.saveStatus.textContent = describePersistenceStatus(state.persistenceStatus);
    renderServerProject();
    return state.persistenceStatus.snapshot;
  }
}

async function reopenProjectSnapshot() {
  if (state.capabilitySession?.project_id || state.serverProject.projectId) {
    try {
      const serverPayload = await openProjectFromServerSession();
      if (serverPayload) return serverPayload;
    } catch (err) {
      pushDiagnostic(err?.payload?.code ?? "E_PROJECT_SERVER_REOPEN", err?.message ?? "서버 프로젝트 재열기 실패", "error");
    }
  }
  const project = currentProject();
  let parsed = null;
  try {
    parsed = loadLocalFallbackSnapshot(project.id);
  } catch (err) {
    pushDiagnostic("E_PROJECT_REOPEN_CORRUPT", String(err?.message ?? err), "error");
    return null;
  }
  if (!parsed) {
    pushDiagnostic("W_PROJECT_REOPEN_EMPTY", "저장된 프로젝트 snapshot이 없습니다.");
    return null;
  }
  const supersededRun = activeRun();
  cancelLivePump("project_reopened");
  applyExecutionEvent(EXECUTION_EVENTS.REOPENED);
  state.runtimeBusy = false;
  state.runs = [];
  state.activeRunId = "";
  state.cursorIndex = -1;
  state.wasm = null;
  finalizeRunRecord(supersededRun, "stopped").catch((archiveErr) => {
    pushDiagnostic("E_RUN_ARCHIVE_FINALIZE_FAILED", String(archiveErr?.message ?? archiveErr), "error");
  });
  state.mode = parsed.mode === "bogae-main" || parsed.mode === "bogae-full" ? parsed.mode : "ddn-main";
  state.viewWorkspace = hydrateProductViewWorkspace(
    project,
    parsed.view_workspace,
    parsed.view_role ?? parsed.selected_view ?? "",
    "local_snapshot",
  );
  state.activeFilePath = String(parsed.active_file_path ?? project.files[0].path);
  for (const file of Array.isArray(parsed.files) ? parsed.files : []) {
    state.fileTexts.set(String(file.path), String(file.text ?? ""));
  }
  state.persistenceStatus = {
    schema: "seamgrim.workbench.persistence_status.v1",
    mode: "local_fallback",
    server_saved: false,
    local_saved: true,
    user_label: `이 기기에만 임시 저장 ${parsed.canonical_hash ?? ""}`,
    snapshot: parsed,
  };
  pushDiagnostic("W_PROJECT_REOPENED", `snapshot ${parsed.canonical_hash ?? ""} 재열기 완료`);
  renderAll();
  return parsed;
}

document.querySelector("[data-testid='lifecycle-run']")?.addEventListener("click", () => startRun());
document.querySelector("[data-testid='lifecycle-pause']")?.addEventListener("click", () => pauseRun());
document.querySelector("[data-testid='lifecycle-resume']")?.addEventListener("click", () => resumeRun());
document.querySelector("[data-testid='lifecycle-step']")?.addEventListener("click", () => stepForward());
document.querySelector("[data-testid='lifecycle-stop']")?.addEventListener("click", () => {
  stopRun().catch((err) => {
    pushDiagnostic("E_RUN_STOP_FAILED", String(err?.message ?? err), "error");
    renderAll();
  });
});
document.querySelector("[data-testid='history-back']")?.addEventListener("click", () => backOneMadi());
document.querySelector("[data-testid='history-branch']")?.addEventListener("click", () => branchFromCursor());
document.querySelector("[data-testid='setup-apply']")?.addEventListener("click", () => applySetupRecipe());
els.setupControlList?.addEventListener("input", (event) => {
  const input = event.target?.closest?.("input[data-control-name]");
  if (!input || state.projectControls?.project_id !== state.projectId) return;
  const value = Number(input.value);
  if (Number.isFinite(value)) {
    state.projectControls.control_values = {
      ...state.projectControls.control_values,
      [String(input.dataset.controlName)]: value,
    };
  }
});
els.actionButtonList?.addEventListener("click", (event) => {
  const button = event.target?.closest?.("button[data-action-id]");
  if (button) setNextAction(String(button.dataset.actionId));
});
document.querySelector("[data-testid='side-view-close']")?.addEventListener("click", () => {
  state.viewWorkspace = closeAllSideViews(state.viewWorkspace);
  renderAll();
});
els.sideViewList?.addEventListener("click", (event) => {
  const button = event.target?.closest?.("[data-view-instance-close]");
  if (!button) return;
  state.viewWorkspace = closeViewInstance(state.viewWorkspace, String(button.dataset.viewInstanceClose ?? ""));
  renderAll();
});

function openProgressiveDialog(dialog) {
  const menu = document.querySelector("[data-testid='project-more-menu']");
  if (menu) menu.open = false;
  if (dialog && !dialog.open) dialog.showModal();
}

document.querySelector("[data-testid='project-storage-open']")?.addEventListener("click", () => openProgressiveDialog(els.projectStorageDrawer));
document.querySelector("[data-testid='project-history-open']")?.addEventListener("click", () => {
  openProgressiveDialog(els.projectHistoryDrawer);
  refreshRunArchives().catch((err) => {
    pushDiagnostic("E_RUN_ARCHIVE_LIST_FAILED", String(err?.message ?? err), "error");
  });
});
document.querySelector("[data-testid='project-verification-open']")?.addEventListener("click", () => openProgressiveDialog(els.projectVerificationDrawer));
document.querySelector("[data-testid='portable-project-settings']")?.addEventListener("click", () => openProgressiveDialog(els.portableDialog));
document.querySelector("[data-testid='project-storage-close']")?.addEventListener("click", () => els.projectStorageDrawer?.close());
document.querySelector("[data-testid='project-history-close']")?.addEventListener("click", () => els.projectHistoryDrawer?.close());
document.querySelector("[data-testid='project-verification-close']")?.addEventListener("click", () => els.projectVerificationDrawer?.close());
document.querySelector("[data-testid='portable-project-dialog-close']")?.addEventListener("click", () => els.portableDialog?.close());
els.runArchiveList?.addEventListener("click", (event) => {
  const button = event.target?.closest?.("button[data-server-run-id]");
  if (!button) return;
  openRunArchiveDetail(String(button.dataset.serverRunId)).catch((err) => {
    pushDiagnostic("E_RUN_ARCHIVE_OPEN_FAILED", String(err?.message ?? err), "error");
  });
});
document.querySelector("[data-testid='project-save']")?.addEventListener("click", () => {
  saveProjectSnapshot().catch(() => renderAll());
});
document.querySelector("[data-testid='project-reopen']")?.addEventListener("click", () => {
  reopenProjectSnapshot().catch(() => renderAll());
});
document.addEventListener("click", (event) => {
  const target = event.target?.nodeType === Node.TEXT_NODE ? event.target.parentElement : event.target;
  if (!target?.closest?.("[data-testid='portable-project-export']")) return;
  event.preventDefault();
  exportPortableProject().catch(() => renderAll());
});
document.querySelector("[data-testid='portable-project-export-confirm']")?.addEventListener("click", () => {
  exportPortableProject().catch(() => renderAll());
});
els.portableImport?.addEventListener("click", () => {
  openProgressiveDialog(els.portableDialog);
  els.portableImportInput?.click();
});
els.portableImportInput?.addEventListener("change", () => {
  const file = els.portableImportInput.files?.[0] ?? null;
  openProgressiveDialog(els.portableDialog);
  previewPortableProjectFile(file).catch(() => renderAll());
});
els.portableOpen?.addEventListener("click", () => {
  openPendingPortableProject()
    .then(() => els.portableDialog?.close())
    .catch(() => renderAll());
});
els.portableCancel?.addEventListener("click", () => {
  state.pendingPortableImport = null;
  renderPortableImportPreview();
  els.portableImport?.focus?.();
});
[
  els.portableMetaTitle,
  els.portableMetaSummary,
  els.portableMetaTags,
  els.portableMetaSubject,
  els.portableMetaLevel,
  els.portableMetaRequiredViews,
  els.portableMetaRequiredGaji,
].forEach((node) => {
  node?.addEventListener("input", updatePortableMetadataDraftFromInputs);
});
els.portableMetaContentKind?.addEventListener("change", updatePortableMetadataDraftFromInputs);
els.projectRevisionList?.addEventListener("click", (event) => {
  const button = event.target?.closest?.("[data-project-restore-revision]");
  if (!button) return;
  restoreProjectRevision(button.dataset.projectRestoreRevision).catch((err) => {
    pushDiagnostic(err?.payload?.code ?? "E_PROJECT_RESTORE_FAILED", err?.message ?? "리비전 복원 실패", "error");
    renderAll();
  });
});
document.querySelector("[data-testid='project-conflict-copy-local']")?.addEventListener("click", async () => {
  const text = String(state.serverProject.conflict?.localPackageJson ?? "");
  try {
    await hostBridge.writeClipboardText(text);
  } catch (_) {
    // Clipboard is optional in headless and local file contexts.
  }
  els.saveStatus.textContent = "project: 로컬 변경 보존됨";
  pushDiagnostic("W_PROJECT_LOCAL_PACKAGE_PRESERVED", "충돌한 로컬 패키지를 화면에 보존했습니다.");
});
els.projectClone?.addEventListener("click", () => {
  const project = currentProject();
  const action = project.portableArtifact?.content_sha256
    ? cloneCurrentPortableProject()
    : cloneCurrentServerProject();
  action.catch((err) => {
    pushDiagnostic(err?.payload?.code ?? "E_PROJECT_CLONE_FAILED", err?.message ?? "프로젝트 복제 실패", "error");
    renderAll();
  });
});
els.myWorkList?.addEventListener("click", (event) => {
  const link = event.target?.closest?.("[data-testid='my-work-item']");
  if (!link) return;
  event.preventDefault();
  const portableProjectId = String(link.dataset.portableProjectId || "");
  if (portableProjectId) {
    selectProject(portableProjectId).then(() => {
      state.persistenceStatus = {
        schema: "seamgrim.workbench.persistence_status.v1",
        mode: "portable_catalog_reopen",
        server_saved: false,
        local_saved: true,
        user_label: `받은 프로젝트 다시 열림 ${portableProjectId}`,
      };
      pushDiagnostic("W_PORTABLE_PROJECT_CATALOG_OPENED", "내 작업에서 받은 프로젝트를 다시 열었습니다.");
      renderAll();
    }).catch((err) => {
      pushDiagnostic("E_PORTABLE_PROJECT_CATALOG_OPEN_FAILED", String(err?.message ?? err), "error");
      renderAll();
    });
    return;
  }
  const projectId = String(link.dataset.projectId || "");
  const row = readMyWorkIndex().find((item) => String(item.project_id || "") === projectId);
  const localProject = nativeProjects.find((item) => item.id === projectId);
  if (localProject) {
    selectProject(projectId).then(() => {
      state.persistenceStatus = {
        schema: "seamgrim.workbench.persistence_status.v1",
        mode: "local_recovery",
        server_saved: false,
        local_saved: true,
        user_label: `로컬 프로젝트 다시 열림 ${projectId}`,
      };
      pushDiagnostic("W_NATIVE_PROJECT_REOPENED", "내 작업에서 로컬 프로젝트를 다시 열었습니다.");
      renderAll();
    });
    return;
  }
  const capability = String(row?.edit_capability || row?.view_capability || "");
  if (!row || !capability) {
    pushDiagnostic("E_MY_WORK_CAPABILITY_MISSING", "내 작업 항목의 권한 정보를 찾지 못했습니다.", "error");
    renderAll();
    return;
  }
  state.capabilitySession = writeWorkbenchCapabilitySession({
    projectId,
    role: row.edit_capability ? "edit" : "view",
    capability,
  }) ?? state.capabilitySession;
  openProjectFromServerSession().catch((err) => {
    pushDiagnostic(err?.payload?.code ?? "E_MY_WORK_OPEN_FAILED", err?.message ?? "내 작업 열기 실패", "error");
    renderAll();
  });
});

window.__SEAMGRIM_APPROVED_WORKBENCH__ = {
  getSnapshot() {
    const project = currentProject();
    const controlSnapshot = (testId) => {
      const node = document.querySelector(`[data-testid='${testId}']`);
      return {
        enabled: Boolean(node && !node.disabled),
        disabled_reason: node?.disabled ? String(node.dataset.disabledReason || "disabled") : "",
      };
    };
    return {
      readiness: {
        workbench_api_ready: true,
        initialization: "ready",
        source: sourceReadinessSnapshot(),
      },
      projectId: state.projectId,
      project: {
        project_id: project.id,
        title: project.title,
        kind: project.kind,
        creation_template: String(project.creationTemplate ?? project.portableSnapshot?.creation_template ?? ""),
        file_count: project.files.length,
        files: project.files.map((file) => ({ path: file.path, role: file.role })),
        native_creator: nativeProjects.some((item) => item.id === project.id),
      },
      mode: state.mode,
      viewWorkspace: {
        schema: state.viewWorkspace.schema,
        primary_view_instance_id: state.viewWorkspace.primary_view_instance_id,
        active_view_instance_id: state.viewWorkspace.active_view_instance_id,
        selected_target: state.viewWorkspace.selected_target,
        instances: state.viewWorkspace.instances.map((instance) => ({ ...instance })),
      },
      runtimeStatus: state.runtimeStatus,
      executionLifecycle: { ...state.executionLifecycle },
      activeRunId: state.activeRunId,
      cursorIndex: state.cursorIndex,
      runs: state.runs.map((run) => ({
        run_id: run.run_id,
        server_run_id: run.server_run_id ?? "",
        source_hash: run.source_hash ?? "",
        source_kind: run.source_kind ?? "",
        execution_mode: run.execution_mode_decision?.mode ?? "",
        source_revision_id: run.source_revision_id ?? "",
        parent_run_id: run.parent_run_id,
        parent_server_run_id: run.parent_server_run_id ?? "",
        parent_madi: run.parent_madi,
        parent_state_hash: run.parent_state_hash,
        frame_count: run.frames.length,
        frames: run.frames.map((frame) => ({
          frame_id: frame.frame_id,
          madi: frame.madi,
          state_hash: frame.state_hash,
          input_snapshot: { ...frame.input_snapshot },
        })),
        input_snapshots: run.frames.map((frame) => ({ ...frame.input_snapshot })),
        latest_state_hash: run.frames.at(-1)?.state_hash ?? "",
        shared_runtime_result: run.shared_runtime_result
          ? structuredClone(run.shared_runtime_result)
          : null,
        work_cost_receipt: run.work_cost_receipt
          ? structuredClone(run.work_cost_receipt)
          : null,
        server_archive_status: run.server_archive_status ?? "",
        server_checkpoint_count: run.server_checkpoint_count ?? 0,
        server_latest_checkpoint_sha256: run.server_latest_checkpoint_sha256 ?? "",
        server_final_status: run.server_final_status ?? "",
        final_status: run.final_status ?? "",
        configured_madi: run.configured_madi ?? 0,
        committed_step_count: run.committed_step_count ?? 0,
        setup: structuredClone(run.setup ?? {}),
        server_finalize_attempt_count: run.server_finalize_attempt_count ?? 0,
        server_finalized: Boolean(run.server_finalized),
      })),
      activeFrame: activeFrame(),
      diagnostics: [...state.diagnostics],
      sourceReadiness: sourceReadinessSnapshot(),
      sourceReadOnly: els.sourceEditor.readOnly,
      pendingRecipe: state.pendingRecipe,
      nextInput: state.nextInput,
      projectControls: {
        schema: state.projectControls?.schema ?? "",
        project_id: state.projectControls?.project_id ?? "",
        status: state.projectControls?.status ?? "idle",
        source: state.projectControls?.source ?? "",
        authoring_plan_hash: state.projectControls?.authoring_plan_hash ?? "",
        controls: (state.projectControls?.controls ?? []).map((control) => ({ ...control })),
        control_values: { ...(state.projectControls?.control_values ?? {}) },
        action_map_hash: state.projectControls?.action_map?.action_map_hash ?? "",
        actions: (state.projectControls?.actions ?? []).map((action) => ({
          ...action,
          input_snapshot: { ...action.input_snapshot },
        })),
        error: state.projectControls?.error ? { ...state.projectControls.error } : null,
      },
      livePump: {
        generation: state.livePump.generation,
        scheduled: state.livePump.scheduled,
        in_flight: state.livePump.inFlight,
        step_start_count: state.livePump.stepStartCount,
        step_commit_count: state.livePump.stepCommitCount,
        max_in_flight: state.livePump.maxInFlight,
        last_origin: state.livePump.lastOrigin,
        last_cancel_reason: state.livePump.lastCancelReason,
      },
      semanticViewPayload: state.semanticViewPayload
        ? {
            schema: state.semanticViewPayload.schema,
            committed_frame: state.semanticViewPayload.committed_frame,
            ordered_observations: state.semanticViewPayload.ordered_observations,
            committed_resource_keys: Object.keys(state.semanticViewPayload.committed_resources ?? {}),
            committed_view_meta_keys: Object.keys(state.semanticViewPayload.committed_view_meta ?? {}),
            view_binding: state.semanticViewPayload.view_binding,
            view_config: state.semanticViewPayload.view_config,
            committed_trajectory_length: state.semanticViewPayload.committed_trajectory.length,
            semantic_payload_hash: state.semanticViewPayload.semantic_payload_hash,
          }
        : null,
      semanticRenderer: state.semanticRenderModel
        ? {
            schema: state.semanticRenderModel.schema,
            family: state.semanticRenderModel.family,
            status: state.semanticRenderModel.status,
            data_source: state.semanticRenderModel.data_source,
            committed_frame: state.semanticRenderModel.committed_frame,
            semantic_payload_hash: state.semanticRenderModel.semantic_payload_hash,
            role: state.semanticRenderModel.role,
            overlay_enabled: Boolean(state.semanticRenderModel.overlay_enabled),
            labels: state.semanticRenderModel.labels,
            current: state.semanticRenderModel.current ?? null,
            trajectory_length: state.semanticRenderModel.trajectory?.length ?? 0,
            point_count: state.semanticRenderModel.points?.length ?? 0,
            tick: state.semanticRenderModel.tick ?? null,
            position: state.semanticRenderModel.position ?? null,
            geometry_source: state.semanticRenderModel.geometry_source ?? "",
            draw_item_count: state.semanticRenderModel.draw_list?.length ?? 0,
            canvas_projection: state.semanticRenderModel.canvas_projection ?? null,
          }
        : null,
      persistenceStatus: state.persistenceStatus,
      persistence: {
        generation: Number(state.persistenceOperation?.generation ?? 0),
        completed_generation: Number(state.persistenceOperation?.completedGeneration ?? 0),
        phase: String(state.persistenceOperation?.phase ?? "idle"),
        outcome: String(state.persistenceOperation?.outcome ?? ""),
        mode: String(state.persistenceStatus?.mode ?? "unsaved"),
        revision_id: String(state.persistenceStatus?.revision_id ?? state.serverProject.headRevisionId ?? ""),
      },
      controls: {
        project_save: controlSnapshot("project-save"),
        lifecycle_run: controlSnapshot("lifecycle-run"),
        lifecycle_pause: controlSnapshot("lifecycle-pause"),
        lifecycle_resume: controlSnapshot("lifecycle-resume"),
        lifecycle_step: controlSnapshot("lifecycle-step"),
        lifecycle_stop: controlSnapshot("lifecycle-stop"),
        history_back: controlSnapshot("history-back"),
        history_branch: controlSnapshot("history-branch"),
        project_clone: controlSnapshot("project-clone"),
      },
      serverProject: {
        project_id: state.serverProject.projectId,
        head_revision_id: state.serverProject.headRevisionId,
        content_sha256: state.serverProject.contentSha256,
        package_hash: state.serverProject.packageHash,
        revision_count: state.serverProject.revisions.length,
        conflict_open: Boolean(state.serverProject.conflict),
      },
      runArchives: state.runArchives.map((run) => ({
        server_run_id: run.server_run_id,
        source_revision_id: run.source_revision_id,
        parent_server_run_id: run.parent_server_run_id,
        branch_madi: run.branch_madi,
        branch_state_hash: run.branch_state_hash,
        latest_committed_madi: run.latest_committed_madi,
        final_status: run.final_status,
      })),
      selectedRunArchive: state.selectedRunArchive?.run
        ? {
            server_run_id: state.selectedRunArchive.run.server_run_id,
            final_status: state.selectedRunArchive.run.final_status,
            parent_server_run_id: state.selectedRunArchive.run.parent_server_run_id,
            branch_madi: state.selectedRunArchive.run.branch_madi,
            branch_state_hash: state.selectedRunArchive.run.branch_state_hash,
            checkpoints: (state.selectedRunArchive.run.checkpoints ?? []).map((checkpoint) => ({
              sequence: checkpoint.sequence,
              committed_madi: checkpoint.committed_madi,
              previous_checkpoint_sha256: checkpoint.previous_checkpoint_sha256,
              checkpoint_sha256: checkpoint.checkpoint_sha256,
              state_hashes: [...(checkpoint.artifact?.state_hashes ?? [])],
              input_snapshots: [...(checkpoint.artifact?.input_snapshots ?? [])],
            })),
          }
        : null,
      myWork: readMyWorkIndex().map((row) => ({
        project_id: row.project_id,
        head_revision_id: row.head_revision_id,
        has_edit_capability: Boolean(row.edit_capability),
        has_view_capability: Boolean(row.view_capability),
        verify_status: row.verify_status || "",
      })),
      portableCatalog: readPortableProjectCatalog().map((row) => ({
        project_id: row.project_id,
        title: row.title,
        content_sha256: row.content_sha256,
      })),
      pendingPortableImport: state.pendingPortableImport
        ? {
            has_artifact: Boolean(state.pendingPortableImport.artifact),
            error_code: state.pendingPortableImport.error?.code ?? "",
            byte_length: state.pendingPortableImport.byte_length ?? 0,
          }
        : null,
      portableLineage: {
        origin_kind: currentPortableLineage().origin_kind,
        origin_content_sha256: currentPortableLineage().origin_content_sha256,
        source_lesson_id: currentPortableLineage().source_lesson_id,
      },
      capabilitySession: state.capabilitySession
        ? {
            schema: state.capabilitySession.schema,
            source: state.capabilitySession.source,
            project_id: state.capabilitySession.project_id,
            role: state.capabilitySession.role,
            capability_redacted: true,
          }
        : null,
    };
  },
  attemptOverwriteActiveRun,
  attemptReuseRunId,
  attemptMutateParentHash,
  startRun,
  pauseRun,
  resumeRun,
  stepForward,
  stopRun,
  branchFromCursor,
  openRunArchiveDetail,
  analyzeSourceReadiness,
  getSourceReadinessCandidate,
  applySourceReadinessFixIt,
  saveProjectSnapshot,
  reopenProjectSnapshot,
  buildProjectSnapshot,
  buildCurrentPortableProjectArtifact,
  exportPortableProject,
  previewPortableProjectFile,
  openPendingPortableProject,
  cloneCurrentPortableProject,
  projectStorageKey,
  async buildProjectArtifact() {
    return buildServerProjectArtifact();
  },
  summarizeRunArchiveBoundary,
};
