import {
  buildProjectSnapshotArtifactV0,
} from "../../project_snapshot.js";
import {
  PROJECT_API_BASE,
  requestProjectApi,
} from "../../project_service_client.js";

export const WORKBENCH_PROJECT_ADAPTER_SCHEMA = "seamgrim.workbench.project_adapter.v1";

function asText(value, fallback = "") {
  const text = String(value ?? "").trim();
  return text || fallback;
}

function mainDdnText(files = []) {
  const rows = Array.isArray(files) ? files : [];
  const main = rows.find((file) => file.path === "lesson.ddn") ?? rows[0] ?? {};
  return String(main.text ?? "");
}

export async function buildWorkbenchProjectArtifact({
  projectId = "custom",
  projectName = "",
  files = [],
  controlsSnapshot = null,
  localPackagePayload = null,
  lineage = null,
  metadata = null,
} = {}) {
  return buildProjectSnapshotArtifactV0({
    projectName: asText(projectName, "이름 없는 셈그림"),
    ddnText: mainDdnText(files),
    lessonPlanText: "",
    sourceLessonId: asText(projectId, "custom"),
    controlsSnapshot,
    localPackagePayload,
    lineage,
    metadata: {
      schema: WORKBENCH_PROJECT_ADAPTER_SCHEMA,
      one_file_project: files.length <= 1,
      generated_artifacts_hidden_from_user_files: true,
      ...metadata,
    },
  });
}

export async function createServerProject({
  artifact,
  title = "",
  fetchImpl = globalThis.fetch,
} = {}) {
  return requestProjectApi(PROJECT_API_BASE, {
    method: "POST",
    body: { project_snapshot_artifact: artifact, title },
    fetchImpl,
  });
}

export async function openServerProject({
  projectId = "",
  capability = "",
  fetchImpl = globalThis.fetch,
} = {}) {
  return requestProjectApi(projectId, { capability, fetchImpl });
}

export async function appendServerRevision({
  projectId = "",
  capability = "",
  artifact,
  expectedParentRevisionId = "",
  fetchImpl = globalThis.fetch,
} = {}) {
  return requestProjectApi(`${projectId}/revisions`, {
    method: "POST",
    capability,
    body: {
      project_snapshot_artifact: artifact,
      expected_parent_revision_id: expectedParentRevisionId,
    },
    fetchImpl,
  });
}

export async function listServerRevisions({
  projectId = "",
  capability = "",
  fetchImpl = globalThis.fetch,
} = {}) {
  return requestProjectApi(`${projectId}/revisions`, { capability, fetchImpl });
}

export async function restoreServerRevision({
  projectId = "",
  capability = "",
  sourceRevisionId = "",
  expectedParentRevisionId = "",
  fetchImpl = globalThis.fetch,
} = {}) {
  return requestProjectApi(`${projectId}/restore`, {
    method: "POST",
    capability,
    body: {
      source_revision_id: sourceRevisionId,
      expected_parent_revision_id: expectedParentRevisionId,
    },
    fetchImpl,
  });
}

export async function cloneServerProject({
  projectId = "",
  capability = "",
  title = "",
  fetchImpl = globalThis.fetch,
} = {}) {
  return requestProjectApi(`${projectId}/clone`, {
    method: "POST",
    capability,
    body: { title },
    fetchImpl,
  });
}
