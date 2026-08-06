use std::collections::{BTreeMap, BTreeSet};
use std::fmt;
use std::fs;
use std::path::{Path, PathBuf};

use serde::{Deserialize, Serialize};
use serde_json::{json, Value as JsonValue};
use sha2::{Digest, Sha256};
use unicode_normalization::UnicodeNormalization;

use crate::runtime_surface;
use ddonirang_lang::{
    Body, Expr, ExprKind, Lexer, ParseMode, Stmt, Token, TokenKind, TopLevelItem,
};

pub const VIRTUAL_PROJECT_SOURCE_SCHEMA: &str = "ddn.virtual_project_source.v1";
pub const VIRTUAL_PROJECT_MANIFEST_SCHEMA: &str = "ddn.virtual_project_manifest.v1";
pub const PROJECT_ROOT_DISCOVERY_REQUEST_SCHEMA: &str = "ddn.project_root_discovery_request.v1";
pub const PROJECT_ROOT_DISCOVERY_SCHEMA: &str = "ddn.project_root_discovery.v1";
pub const PROJECT_GRAPH_SCHEMA: &str = "ddn.local_project_graph.v1";
pub const PROJECT_SYMBOL_BOUNDARY_SCHEMA: &str = "ddn.local_project_symbol_boundary.v1";
pub const LOCAL_GAJI_LOCK_SCHEMA: &str = "ddn.local_gaji_lock.v1";
pub const LOCAL_PROJECT_RUN_SUMMARY_SCHEMA: &str = "ddn.local_project_run_summary.v1";
pub const PROJECT_EDIT_PLAN_SCHEMA: &str = "ddn.local_project_edit_plan.v1";
pub const GAJI_EXTRACTION_PLAN_SCHEMA: &str = "ddn.gaji_extraction_plan.v1";
pub const LOCAL_GAJI_ARTIFACT_SCHEMA: &str = "ddn.local_gaji_artifact.v1";
pub const LOCAL_GOTGAN_STORE_SCHEMA: &str = "ddn.local_gotgan_store.v1";
pub const GAJI_LIFECYCLE_PLAN_SCHEMA: &str = "ddn.gaji_lifecycle_plan.v1";
const GAJI_ARTIFACT_MAX_FILES: usize = 256;
const GAJI_ARTIFACT_MAX_SINGLE_FILE_BYTES: usize = 1024 * 1024;
const GAJI_ARTIFACT_MAX_TOTAL_BYTES: usize = 8 * 1024 * 1024;
const GAJI_ARTIFACT_MAX_MANIFEST_BYTES: usize = 256 * 1024;
pub const LOCAL_PROJECT_TREE_KIND: &str = "seamgrim.local_project_tree.v0";
pub const MAX_PROJECT_FILES: usize = 64;
pub const MAX_FILE_BYTES: usize = 256 * 1024;
pub const MAX_SERIALIZED_ARTIFACT_BYTES: usize = 2 * 1024 * 1024;
pub const MAX_PROJECT_TOTAL_UTF8_BYTES: usize = 2 * 1024 * 1024;
pub const PROJECT_ROOT_FILE: &str = "뿌리.ddn";
pub const PROJECT_JSON_FILE: &str = "ddn.project.json";
const LEGACY_ROOT_FILES: &[&str] = &["프로젝트.ddn", "project.ddn"];

#[derive(Debug, Clone)]
pub struct LocalProjectError {
    pub code: &'static str,
    pub message: String,
    pub path: Option<String>,
    pub source_span: Option<(usize, usize)>,
}

impl LocalProjectError {
    fn new(code: &'static str, message: impl Into<String>) -> Self {
        Self {
            code,
            message: message.into(),
            path: None,
            source_span: None,
        }
    }

    fn with_path(code: &'static str, path: impl Into<String>, message: impl Into<String>) -> Self {
        Self {
            code,
            message: message.into(),
            path: Some(path.into()),
            source_span: None,
        }
    }

    fn with_path_span(
        code: &'static str,
        path: impl Into<String>,
        message: impl Into<String>,
        source_span: (usize, usize),
    ) -> Self {
        Self {
            code,
            message: message.into(),
            path: Some(path.into()),
            source_span: Some(source_span),
        }
    }

    pub fn to_json_value(&self) -> JsonValue {
        let mut value = json!({
            "schema": "ddn.local_project.error.v1",
            "code": self.code,
            "message": self.message,
            "path": self.path,
        });
        if let Some((start, end)) = self.source_span {
            if let Some(object) = value.as_object_mut() {
                object.insert(
                    "source_span".to_string(),
                    json!({"start": start, "end": end}),
                );
            }
        }
        value
    }
}

impl fmt::Display for LocalProjectError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        if let Some(path) = &self.path {
            write!(f, "{}: {} ({})", self.code, self.message, path)
        } else {
            write!(f, "{}: {}", self.code, self.message)
        }
    }
}

impl std::error::Error for LocalProjectError {}

#[derive(Debug, Clone, Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
pub struct VirtualProjectSource {
    pub schema: String,
    #[serde(default)]
    pub kind: Option<String>,
    pub root_path: String,
    pub entry_path: String,
    pub files: Vec<VirtualProjectFileSource>,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
pub struct VirtualProjectFileSource {
    pub path: String,
    pub role: String,
    pub utf8_text: String,
}

#[derive(Debug, Clone, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ProjectEditPlanRequest {
    pub schema: String,
    pub source: VirtualProjectSource,
    pub operation: ProjectEditOperation,
    pub expected_source_sha256: String,
}

#[derive(Debug, Clone, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case", deny_unknown_fields)]
pub enum ProjectEditOperation {
    RenameFile {
        from_path: String,
        to_path: String,
    },
    AddFile {
        path: String,
        utf8_text: String,
        #[serde(default = "default_ddn_source_role")]
        role: String,
    },
    AddModule {
        path: String,
        module_name: String,
    },
    DuplicateFile {
        from_path: String,
        to_path: String,
    },
    DeleteFile {
        path: String,
    },
    SetEntry {
        path: String,
    },
}

fn default_ddn_source_role() -> String {
    "ddn_source".to_string()
}

#[derive(Debug, Clone, Serialize)]
pub struct ProjectEditPatch {
    pub path: String,
    pub start: usize,
    pub end: usize,
    pub before: String,
    pub after: String,
    pub reason: &'static str,
}

#[derive(Debug, Clone, Serialize)]
pub struct ProjectEditPlan {
    pub schema: &'static str,
    pub operation: &'static str,
    pub before_source_sha256: String,
    pub after_source_sha256: String,
    pub affected_files: Vec<String>,
    pub affected_symbols: Vec<String>,
    pub affected_references: Vec<String>,
    pub patches: Vec<ProjectEditPatch>,
    pub diagnostics: Vec<ProjectDiagnostic>,
    pub project_source: VirtualProjectSource,
    pub atomic_apply: bool,
    pub lock_stale: bool,
}

#[derive(Debug, Clone, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct GajiExtractionPlanRequest {
    pub schema: String,
    pub source: VirtualProjectSource,
    pub selected_modules: Vec<String>,
    pub gaji_id: String,
    pub version: String,
    #[serde(default)]
    pub description: String,
    #[serde(default)]
    pub tags: Vec<String>,
    #[serde(default = "default_local_gotgan_profile")]
    pub profile: String,
    #[serde(default)]
    pub origin_project_ref: Option<String>,
    #[serde(default)]
    pub origin_gaji: Option<String>,
    #[serde(default = "default_gaji_relation")]
    pub relation: String,
}

fn default_local_gotgan_profile() -> String {
    "내".to_string()
}

fn default_gaji_relation() -> String {
    "extracted".to_string()
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct GajiPublicSymbol {
    pub module_path: String,
    pub external_name: String,
    pub internal_name: String,
}

#[derive(Debug, Clone, Serialize)]
pub struct GajiExtractionFile {
    pub path: String,
    pub byte_length: usize,
    pub sha256: String,
    pub selected: bool,
}

#[derive(Debug, Clone, Serialize)]
pub struct GajiExtractionPlan {
    pub schema: &'static str,
    pub gaji_id: String,
    pub version: String,
    pub profile: String,
    pub origin_project_ref: Option<String>,
    pub source_project_sha256: String,
    pub selected_modules: Vec<String>,
    pub included_modules: Vec<String>,
    pub excluded_files: Vec<String>,
    pub public_symbols: Vec<GajiPublicSymbol>,
    pub external_gaji_dependencies: BTreeMap<String, String>,
    pub files: Vec<GajiExtractionFile>,
    pub content_sha256: String,
    pub diagnostics: Vec<ProjectDiagnostic>,
    pub publishable: bool,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
pub struct LocalGajiArtifactFile {
    pub path: String,
    pub utf8_text: String,
    pub byte_length: usize,
    pub sha256: String,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
pub struct LocalGajiArtifactProvenance {
    pub origin_project_ref: Option<String>,
    pub origin_gaji: Option<String>,
    pub relation: String,
    pub extraction_modules: Vec<String>,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
pub struct LocalGajiArtifact {
    pub schema: String,
    pub gaji_id: String,
    pub version: String,
    pub profile: String,
    pub description: String,
    pub tags: Vec<String>,
    pub manifest_path: String,
    pub content_sha256: String,
    pub package_sha256: String,
    pub public_symbols: Vec<GajiPublicSymbol>,
    pub dependencies: BTreeMap<String, String>,
    pub provenance: LocalGajiArtifactProvenance,
    pub files: Vec<LocalGajiArtifactFile>,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
pub struct LocalGotganStore {
    pub schema: String,
    pub artifacts: Vec<LocalGajiArtifact>,
}

#[derive(Debug, Clone, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct LocalGotganPublishRequest {
    pub schema: String,
    pub store: LocalGotganStore,
    pub artifact: LocalGajiArtifact,
}

#[derive(Debug, Clone, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct LocalGotganSearchRequest {
    pub schema: String,
    pub store: LocalGotganStore,
    #[serde(default)]
    pub query: String,
    #[serde(default)]
    pub profiles: Vec<String>,
}

#[derive(Debug, Clone, Serialize)]
pub struct LocalGotganSearchRow {
    pub profile: String,
    pub gaji_id: String,
    pub version: String,
    pub description: String,
    pub tags: Vec<String>,
    pub public_symbols: Vec<String>,
    pub content_sha256: String,
    pub package_sha256: String,
    pub origin_project_ref: Option<String>,
    pub relation: String,
}

#[derive(Debug, Clone, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct GajiLifecyclePlanRequest {
    pub schema: String,
    pub source: VirtualProjectSource,
    pub expected_source_sha256: String,
    #[serde(default)]
    pub expected_lock_sha256: Option<String>,
    pub operation: GajiLifecycleOperation,
}

#[derive(Debug, Clone, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case", deny_unknown_fields)]
pub enum GajiLifecycleOperation {
    Install {
        alias: String,
        artifact: LocalGajiArtifact,
    },
    Update {
        alias: String,
        artifact: LocalGajiArtifact,
    },
    Remove {
        alias: String,
    },
}

#[derive(Debug, Clone, Serialize)]
pub struct GajiLifecyclePlan {
    pub schema: &'static str,
    pub operation: &'static str,
    pub alias: String,
    pub before_source_sha256: String,
    pub after_source_sha256: String,
    pub before_lock_sha256: Option<String>,
    pub after_lock_sha256: Option<String>,
    pub affected_files: Vec<String>,
    pub version_diff: Option<GajiVersionDiff>,
    pub diagnostics: Vec<ProjectDiagnostic>,
    pub project_source: VirtualProjectSource,
    pub atomic_apply: bool,
}

#[derive(Debug, Clone, Serialize)]
pub struct GajiVersionDiff {
    pub from_version: Option<String>,
    pub to_version: Option<String>,
    pub added_files: Vec<String>,
    pub removed_files: Vec<String>,
    pub changed_files: Vec<String>,
    pub added_public_symbols: Vec<String>,
    pub removed_public_symbols: Vec<String>,
    pub dependency_changed: bool,
    pub risky: bool,
}

#[derive(Debug, Clone, Serialize)]
pub struct NormalizedProjectManifest {
    pub schema: &'static str,
    pub kind: &'static str,
    pub root_path: String,
    pub entry_path: String,
    pub file_count: usize,
    pub total_utf8_bytes: usize,
    pub files: Vec<NormalizedProjectFile>,
    pub project_graph_sha256: String,
    pub lock_sha256: Option<String>,
    pub canonical_manifest_sha256: String,
    pub limits: ProjectLimits,
}

#[derive(Debug, Clone, Serialize)]
pub struct NormalizedProjectFile {
    pub path: String,
    pub role: String,
    pub byte_length: usize,
    pub sha256: String,
}

#[derive(Debug, Clone, Serialize)]
pub struct ProjectLimits {
    pub max_files: usize,
    pub max_file_bytes: usize,
    pub max_serialized_artifact_bytes: usize,
}

#[derive(Debug, Clone, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ProjectRootDiscoveryRequest {
    pub schema: String,
    pub start_path: String,
    #[serde(default)]
    pub explicit_project_path: Option<String>,
    pub files: Vec<ProjectRootDiscoveryFile>,
}

#[derive(Debug, Clone, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ProjectRootDiscoveryFile {
    pub path: String,
    #[serde(default)]
    pub utf8_text: Option<String>,
}

#[derive(Debug, Clone, Serialize)]
pub struct ProjectRootDiscoveryResult {
    pub schema: &'static str,
    pub root_kind: &'static str,
    pub root_marker_path: Option<String>,
    pub project_json_path: Option<String>,
    pub used_fallback: bool,
    pub diagnostics: Vec<ProjectDiagnostic>,
}

#[derive(Debug, Clone, Serialize)]
pub struct ProjectDiagnostic {
    pub code: &'static str,
    pub message: String,
    pub path: Option<String>,
}

#[derive(Debug, Clone, Serialize)]
pub struct LocalProjectGraph {
    pub schema: &'static str,
    pub project_name: String,
    pub root_path: String,
    pub entry_path: String,
    pub targets: BTreeMap<String, String>,
    pub module_paths: BTreeMap<String, String>,
    pub gaji_aliases: BTreeMap<String, String>,
    pub file_count: usize,
    pub files: Vec<NormalizedProjectFile>,
    pub project_graph_sha256: String,
    pub diagnostics: Vec<ProjectDiagnostic>,
}

#[derive(Debug, Clone, Serialize)]
pub struct LocalProjectSymbolBoundary {
    pub schema: &'static str,
    pub entry_path: String,
    pub module_graph_order: Vec<String>,
    pub module_graph_sha256: String,
    pub imports: Vec<ResolvedImport>,
    pub exports: Vec<ResolvedExport>,
    pub resolved_symbols: Vec<ResolvedSymbol>,
    pub output_rows: Vec<String>,
    pub symbol_boundary_sha256: String,
    pub diagnostics: Vec<ProjectDiagnostic>,
}

#[derive(Debug, Clone, Serialize)]
pub struct ResolvedImport {
    pub importer_path: String,
    pub alias: String,
    pub source: String,
    pub resolved_path: String,
}

#[derive(Debug, Clone, Serialize)]
pub struct ResolvedExport {
    pub module_path: String,
    pub external_name: String,
    pub internal_name: String,
}

#[derive(Debug, Clone, Serialize)]
pub struct ResolvedSymbol {
    pub alias: String,
    pub symbol: String,
    pub module_path: String,
    pub internal_name: String,
    pub value: String,
}

#[derive(Debug, Clone, Serialize)]
pub struct LocalGajiLock {
    pub schema: &'static str,
    pub lock_format: &'static str,
    pub root_path: String,
    pub entry_path: String,
    pub project_graph_sha256: String,
    pub packages: Vec<LocalGajiPin>,
    pub lock_sha256: String,
    pub diagnostics: Vec<ProjectDiagnostic>,
}

#[derive(Debug, Clone, Serialize)]
pub struct LocalGajiPin {
    pub id: String,
    pub version: String,
    pub path: String,
    pub direct: bool,
    pub dependency_of: Vec<String>,
    pub dependencies: BTreeMap<String, String>,
    pub manifest_path: String,
    pub manifest_sha256: String,
    pub package_sha256: String,
}

#[derive(Debug, Clone, Serialize)]
pub struct LocalProjectRunSummary {
    pub schema: &'static str,
    pub frontdoor: &'static str,
    pub root_path: String,
    pub entry_path: String,
    pub target: String,
    pub target_path: String,
    pub file_count: usize,
    pub project_graph_sha256: String,
    pub lock_sha256: Option<String>,
    pub symbol_boundary_sha256: String,
    pub output_rows: Vec<String>,
    pub runtime_output_log_texts: Vec<String>,
    pub runtime_final_row: JsonValue,
    pub runtime_state_hash: String,
    pub runtime_execution_envelope: JsonValue,
    pub execution_preparation: JsonValue,
    pub project_observation_trace: JsonValue,
    pub linked_execution_source: String,
    pub linked_execution_canonical_ddn: String,
    pub linked_execution_source_sha256: String,
    pub linked_execution_canonical_sha256: String,
    pub bounded_state_sha256: String,
    pub graph_inspected: bool,
    pub lock_inspected: bool,
    pub summary_sha256: String,
    pub diagnostics: Vec<ProjectDiagnostic>,
}

#[derive(Debug, Clone, Serialize)]
pub struct LocalProjectPrepareLink {
    pub schema: &'static str,
    pub frontdoor: &'static str,
    pub root_path: String,
    pub entry_path: String,
    pub target: String,
    pub target_path: String,
    pub file_count: usize,
    pub normalized_project: NormalizedProjectManifest,
    pub project_graph: LocalProjectGraph,
    pub graph_inspected: bool,
    pub lock_required: bool,
    pub lock_inspected: bool,
    pub verified_lock: Option<LocalGajiLock>,
    pub linked_execution_source: String,
    pub linked_execution_source_sha256: String,
    pub runtime_execution_envelope: JsonValue,
    pub symbol_boundary: LocalProjectSymbolBoundary,
    pub diagnostics: Vec<ProjectDiagnostic>,
    pub state_hash_formula_change: bool,
    pub prepare_link_sha256: String,
}

#[derive(Debug, Clone)]
struct PendingFile {
    path: String,
    role: String,
    byte_len: usize,
    sha256: String,
}

#[derive(Debug, Clone)]
struct ParsedImport {
    alias: String,
    source: String,
}

#[derive(Debug, Clone)]
struct ParsedExport {
    external_name: String,
    internal_name: String,
}

#[derive(Debug, Clone)]
struct AliasShowRequest {
    alias: String,
    symbol: String,
}

#[derive(Debug, Clone)]
struct ModuleInfo {
    path: String,
    imports: Vec<ResolvedImport>,
    exports: BTreeMap<String, String>,
}

#[derive(Debug, Clone)]
struct SymbolValue {
    module_path: String,
    internal_name: String,
}

#[derive(Debug, Clone)]
struct LinkedProject {
    symbol_boundary: LocalProjectSymbolBoundary,
    execution_source: String,
}

#[derive(Debug, Clone)]
struct ParsedGajiManifest {
    id: String,
    version: String,
    dependencies: BTreeMap<String, String>,
    manifest_path: String,
    manifest_sha256: String,
    package_sha256: String,
}

pub fn normalize_virtual_project_source_json(
    input_json: &str,
) -> Result<String, LocalProjectError> {
    let source: VirtualProjectSource = serde_json::from_str(input_json).map_err(|err| {
        LocalProjectError::new(
            "E_VIRTUAL_PROJECT_JSON_INVALID",
            format!("virtual project JSON을 읽을 수 없습니다: {err}"),
        )
    })?;
    let manifest = normalize_virtual_project_source(source)?;
    Ok(to_canonical_json_line(&manifest))
}

pub fn build_project_edit_plan_json(input_json: &str) -> Result<String, LocalProjectError> {
    let request: ProjectEditPlanRequest = serde_json::from_str(input_json).map_err(|err| {
        LocalProjectError::new(
            "E_PROJECT_EDIT_REQUEST_JSON",
            format!("edit-plan 요청 JSON이 올바르지 않습니다: {err}"),
        )
    })?;
    if request.schema != PROJECT_EDIT_PLAN_SCHEMA {
        return Err(LocalProjectError::new(
            "E_PROJECT_EDIT_SCHEMA",
            format!("schema는 {PROJECT_EDIT_PLAN_SCHEMA} 이어야 합니다"),
        ));
    }
    let plan = build_project_edit_plan(request)?;
    Ok(to_canonical_json_line(&plan))
}

pub fn build_gaji_extraction_plan_json(input_json: &str) -> Result<String, LocalProjectError> {
    let request: GajiExtractionPlanRequest = serde_json::from_str(input_json).map_err(|err| {
        LocalProjectError::new(
            "E_GAJI_EXTRACTION_REQUEST_JSON",
            format!("가지 추출 요청 JSON이 올바르지 않습니다: {err}"),
        )
    })?;
    let plan = build_gaji_extraction_plan(request)?;
    Ok(to_canonical_json_line(&plan))
}

pub fn build_local_gaji_artifact_json(input_json: &str) -> Result<String, LocalProjectError> {
    let request: GajiExtractionPlanRequest = serde_json::from_str(input_json).map_err(|err| {
        LocalProjectError::new(
            "E_GAJI_ARTIFACT_REQUEST_JSON",
            format!("가지 artifact 요청 JSON이 올바르지 않습니다: {err}"),
        )
    })?;
    let artifact = build_local_gaji_artifact(request)?;
    Ok(to_canonical_json_line(&artifact))
}

pub fn verify_local_gaji_artifact_json(input_json: &str) -> Result<String, LocalProjectError> {
    let artifact: LocalGajiArtifact = serde_json::from_str(input_json).map_err(|err| {
        LocalProjectError::new(
            "E_GAJI_ARTIFACT_JSON",
            format!("가지 artifact JSON을 읽을 수 없습니다: {err}"),
        )
    })?;
    verify_local_gaji_artifact(&artifact)?;
    Ok(to_canonical_json_line(&json!({
        "schema": "ddn.local_gaji_artifact_verification.v1",
        "status": "PASS",
        "gaji_id": artifact.gaji_id,
        "version": artifact.version,
        "content_sha256": artifact.content_sha256,
        "package_sha256": artifact.package_sha256,
    })))
}

pub fn publish_local_gotgan_json(input_json: &str) -> Result<String, LocalProjectError> {
    let request: LocalGotganPublishRequest = serde_json::from_str(input_json).map_err(|err| {
        LocalProjectError::new(
            "E_GOTGAN_PUBLISH_JSON",
            format!("내 가지곳간 발행 요청을 읽을 수 없습니다: {err}"),
        )
    })?;
    if request.schema != "ddn.local_gotgan_publish_request.v1" {
        return Err(LocalProjectError::new(
            "E_GOTGAN_PUBLISH_SCHEMA",
            "지원하지 않는 가지곳간 발행 schema입니다",
        ));
    }
    let store = publish_local_gotgan(request.store, request.artifact)?;
    Ok(to_canonical_json_line(&store))
}

pub fn search_local_gotgan_json(input_json: &str) -> Result<String, LocalProjectError> {
    let request: LocalGotganSearchRequest = serde_json::from_str(input_json).map_err(|err| {
        LocalProjectError::new(
            "E_GOTGAN_SEARCH_JSON",
            format!("가지 선반 검색 요청을 읽을 수 없습니다: {err}"),
        )
    })?;
    if request.schema != "ddn.local_gotgan_search_request.v1" {
        return Err(LocalProjectError::new(
            "E_GOTGAN_SEARCH_SCHEMA",
            "지원하지 않는 가지 선반 검색 schema입니다",
        ));
    }
    let rows = search_local_gotgan(&request.store, &request.query, &request.profiles)?;
    Ok(to_canonical_json_line(&json!({
        "schema": "ddn.local_gotgan_search_result.v1",
        "query": request.query,
        "profiles": request.profiles,
        "rows": rows,
    })))
}

pub fn build_gaji_lifecycle_plan_json(input_json: &str) -> Result<String, LocalProjectError> {
    let request: GajiLifecyclePlanRequest = serde_json::from_str(input_json).map_err(|err| {
        LocalProjectError::new(
            "E_GAJI_LIFECYCLE_JSON",
            format!("가지 lifecycle 요청을 읽을 수 없습니다: {err}"),
        )
    })?;
    let plan = build_gaji_lifecycle_plan(request)?;
    Ok(to_canonical_json_line(&plan))
}

pub fn build_gaji_lifecycle_plan(
    request: GajiLifecyclePlanRequest,
) -> Result<GajiLifecyclePlan, LocalProjectError> {
    if request.schema != GAJI_LIFECYCLE_PLAN_SCHEMA {
        return Err(LocalProjectError::new(
            "E_GAJI_LIFECYCLE_SCHEMA",
            "지원하지 않는 가지 lifecycle schema입니다",
        ));
    }
    let before_source_sha256 = virtual_project_source_sha256(&request.source)?;
    if before_source_sha256 != request.expected_source_sha256 {
        return Err(LocalProjectError::new(
            "E_GAJI_LIFECYCLE_SOURCE_STALE",
            "현재 project source hash가 계획 기준과 다릅니다",
        ));
    }
    let before_graph = build_project_graph(request.source.clone())?;
    let embedded_lock_sha256 = request
        .source
        .files
        .iter()
        .find(|file| file.path == "ddn.lock")
        .and_then(|file| serde_json::from_str::<serde_json::Value>(&file.utf8_text).ok())
        .and_then(|value| {
            value
                .get("lock_sha256")
                .and_then(|item| item.as_str())
                .map(str::to_string)
        });
    let mut unlocked_source = request.source.clone();
    unlocked_source.files.retain(|file| file.path != "ddn.lock");
    let before_lock = if before_graph.gaji_aliases.is_empty() {
        None
    } else {
        Some(build_project_gaji_lock(unlocked_source, false)?)
    };
    let before_lock_sha256 = before_lock.as_ref().map(|lock| lock.lock_sha256.clone());
    if request.expected_lock_sha256.is_some()
        && request.expected_lock_sha256 != embedded_lock_sha256
    {
        return Err(LocalProjectError::new(
            "E_GAJI_LIFECYCLE_LOCK_STALE",
            "현재 ddn.lock hash가 계획 기준과 다릅니다",
        ));
    }
    let mut source = request.source;
    source.files.retain(|file| file.path != "ddn.lock");
    let (operation, alias, affected_files, version_diff) = match request.operation {
        GajiLifecycleOperation::Install { alias, artifact } => {
            if before_graph.gaji_aliases.contains_key(&alias) {
                return Err(LocalProjectError::new(
                    "E_GAJI_ALIAS_EXISTS",
                    format!("가지 alias {alias}가 이미 설치되어 있습니다"),
                ));
            }
            let affected = install_artifact_into_source(&mut source, &alias, &artifact, false)?;
            ("install", alias, affected, None)
        }
        GajiLifecycleOperation::Update { alias, artifact } => {
            if !before_graph.gaji_aliases.contains_key(&alias) {
                return Err(LocalProjectError::new(
                    "E_GAJI_ALIAS_MISSING",
                    format!("갱신할 가지 alias {alias}가 없습니다"),
                ));
            }
            let old_path = before_graph.gaji_aliases.get(&alias).expect("alias");
            let old_id = gaji_id_from_vendor_path(old_path)?.to_string();
            let old_artifact = installed_artifact_from_source(&source, &old_id)?;
            let version_diff = diff_gaji_artifacts(Some(&old_artifact), Some(&artifact));
            let root_text = source
                .files
                .iter()
                .find(|file| file.path == source.root_path)
                .map(|file| file.utf8_text.clone());
            source
                .files
                .retain(|file| !file.path.starts_with(&format!("vendor/{old_id}/")));
            let affected = install_artifact_into_source(&mut source, &alias, &artifact, true)?;
            if old_id == artifact.gaji_id {
                if let (Some(original), Some(root)) = (
                    root_text,
                    source
                        .files
                        .iter_mut()
                        .find(|file| file.path == source.root_path),
                ) {
                    root.utf8_text = original;
                }
            }
            ("update", alias, affected, Some(version_diff))
        }
        GajiLifecycleOperation::Remove { alias } => {
            let old_path = before_graph.gaji_aliases.get(&alias).ok_or_else(|| {
                LocalProjectError::new(
                    "E_GAJI_ALIAS_MISSING",
                    format!("제거할 가지 alias {alias}가 없습니다"),
                )
            })?;
            let old_id = gaji_id_from_vendor_path(old_path)?.to_string();
            for file in &source.files {
                if file.path.starts_with("vendor/") || file.path == source.root_path {
                    continue;
                }
                if parse_imports(&file.utf8_text, &file.path)?
                    .iter()
                    .any(|item| {
                        item.alias == alias
                            || resolve_import_source_path(&file.path, &item.source)
                                .is_ok_and(|path| path.starts_with(&format!("vendor/{old_id}/")))
                    })
                {
                    return Err(LocalProjectError::with_path(
                        "E_GAJI_REMOVE_REFERENCED",
                        &file.path,
                        format!("쓰임 alias {alias}를 참조 중이므로 제거할 수 없습니다"),
                    ));
                }
            }
            let old_artifact = installed_artifact_from_source(&source, &old_id)?;
            source
                .files
                .retain(|file| !file.path.starts_with(&format!("vendor/{old_id}/")));
            set_project_gaji_alias(&mut source, &alias, None)?;
            (
                "remove",
                alias,
                vec![format!("vendor/{old_id}")],
                Some(diff_gaji_artifacts(Some(&old_artifact), None)),
            )
        }
    };
    let after_graph = build_project_graph(source.clone())?;
    let after_lock = if after_graph.gaji_aliases.is_empty() {
        None
    } else {
        Some(build_project_gaji_lock(source.clone(), false)?)
    };
    if let Some(lock) = &after_lock {
        source.files.push(VirtualProjectFileSource {
            path: "ddn.lock".to_string(),
            role: "lock".to_string(),
            utf8_text: to_canonical_json_line(lock),
        });
        source.files.sort_by(|a, b| a.path.cmp(&b.path));
    }
    normalize_virtual_project_source(source.clone())?;
    let after_source_sha256 = virtual_project_source_sha256(&source)?;
    Ok(GajiLifecyclePlan {
        schema: GAJI_LIFECYCLE_PLAN_SCHEMA,
        operation,
        alias,
        before_source_sha256,
        after_source_sha256,
        before_lock_sha256,
        after_lock_sha256: after_lock.map(|lock| lock.lock_sha256),
        affected_files,
        version_diff,
        diagnostics: Vec::new(),
        project_source: source,
        atomic_apply: true,
    })
}

fn install_artifact_into_source(
    source: &mut VirtualProjectSource,
    alias: &str,
    artifact: &LocalGajiArtifact,
    replace_alias: bool,
) -> Result<Vec<String>, LocalProjectError> {
    verify_local_gaji_artifact(artifact)?;
    let prefix = format!("vendor/{}", artifact.gaji_id);
    if source
        .files
        .iter()
        .any(|file| file.path == prefix || file.path.starts_with(&format!("{prefix}/")))
    {
        return Err(LocalProjectError::new(
            "E_GAJI_VENDOR_CONFLICT",
            "같은 가지 vendor 경로가 이미 존재합니다",
        ));
    }
    let mut affected = Vec::new();
    let metadata_path = format!("{prefix}/artifact.detjson");
    affected.push(metadata_path.clone());
    source.files.push(VirtualProjectFileSource {
        path: metadata_path,
        role: "metadata".to_string(),
        utf8_text: to_canonical_json_line(artifact),
    });
    for file in &artifact.files {
        if file.path == "artifact.detjson" {
            continue;
        }
        let path = format!("{prefix}/{}", file.path);
        affected.push(path.clone());
        source.files.push(VirtualProjectFileSource {
            path,
            role: if file.path == "gaji.toml" {
                "gaji_manifest".to_string()
            } else {
                "ddn_source".to_string()
            },
            utf8_text: file.utf8_text.clone(),
        });
    }
    if artifact.provenance.extraction_modules.is_empty() {
        return Err(LocalProjectError::new(
            "E_GAJI_ENTRY_MODULE_MISSING",
            "가지 계보에 추출 모듈이 없습니다",
        ));
    }
    set_project_gaji_alias(source, alias, Some(&prefix))?;
    if replace_alias {
        affected.push(format!("@alias:{alias}"));
    }
    Ok(affected)
}

fn installed_artifact_from_source(
    source: &VirtualProjectSource,
    id: &str,
) -> Result<LocalGajiArtifact, LocalProjectError> {
    let path = format!("vendor/{id}/artifact.detjson");
    let file = source
        .files
        .iter()
        .find(|file| file.path == path)
        .ok_or_else(|| {
            LocalProjectError::with_path(
                "E_GAJI_INSTALLED_METADATA_MISSING",
                &path,
                "갱신·되돌리기에 필요한 설치 artifact metadata가 없습니다",
            )
        })?;
    let artifact: LocalGajiArtifact = serde_json::from_str(&file.utf8_text).map_err(|err| {
        LocalProjectError::with_path(
            "E_GAJI_INSTALLED_METADATA_INVALID",
            &path,
            format!("설치 artifact metadata가 올바르지 않습니다: {err}"),
        )
    })?;
    verify_local_gaji_artifact(&artifact)?;
    Ok(artifact)
}

fn diff_gaji_artifacts(
    before: Option<&LocalGajiArtifact>,
    after: Option<&LocalGajiArtifact>,
) -> GajiVersionDiff {
    let before_files = before
        .map(|item| {
            item.files
                .iter()
                .map(|file| (file.path.clone(), file.sha256.clone()))
                .collect::<BTreeMap<_, _>>()
        })
        .unwrap_or_default();
    let after_files = after
        .map(|item| {
            item.files
                .iter()
                .map(|file| (file.path.clone(), file.sha256.clone()))
                .collect::<BTreeMap<_, _>>()
        })
        .unwrap_or_default();
    let before_symbols = before
        .map(|item| {
            item.public_symbols
                .iter()
                .map(|symbol| format!("{}:{}", symbol.module_path, symbol.external_name))
                .collect::<BTreeSet<_>>()
        })
        .unwrap_or_default();
    let after_symbols = after
        .map(|item| {
            item.public_symbols
                .iter()
                .map(|symbol| format!("{}:{}", symbol.module_path, symbol.external_name))
                .collect::<BTreeSet<_>>()
        })
        .unwrap_or_default();
    let added_files = after_files
        .keys()
        .filter(|path| !before_files.contains_key(*path))
        .cloned()
        .collect();
    let removed_files = before_files
        .keys()
        .filter(|path| !after_files.contains_key(*path))
        .cloned()
        .collect::<Vec<_>>();
    let changed_files = after_files
        .iter()
        .filter(|(path, hash)| before_files.get(*path).is_some_and(|old| old != *hash))
        .map(|(path, _)| path.clone())
        .collect();
    let added_public_symbols = after_symbols.difference(&before_symbols).cloned().collect();
    let removed_public_symbols = before_symbols
        .difference(&after_symbols)
        .cloned()
        .collect::<Vec<_>>();
    let dependency_changed =
        before.map(|item| &item.dependencies) != after.map(|item| &item.dependencies);
    let risky =
        !removed_files.is_empty() || !removed_public_symbols.is_empty() || dependency_changed;
    GajiVersionDiff {
        from_version: before.map(|item| item.version.clone()),
        to_version: after.map(|item| item.version.clone()),
        added_files,
        removed_files,
        changed_files,
        added_public_symbols,
        removed_public_symbols,
        dependency_changed,
        risky,
    }
}

fn set_project_gaji_alias(
    source: &mut VirtualProjectSource,
    alias: &str,
    path: Option<&str>,
) -> Result<(), LocalProjectError> {
    if alias.trim().is_empty() || alias.contains('.') {
        return Err(LocalProjectError::new(
            "E_GAJI_ALIAS_INVALID",
            "가지 alias가 올바르지 않습니다",
        ));
    }
    let root = source
        .files
        .iter_mut()
        .find(|file| file.path == source.root_path)
        .ok_or_else(|| LocalProjectError::new("E_PROJECT_ROOT_MISSING", "뿌리.ddn이 없습니다"))?;
    let mut pairs = extract_project_block(&root.utf8_text)
        .map(|block| parse_string_pairs_from_named_block(block, "가지"))
        .transpose()?
        .unwrap_or_default();
    match path {
        Some(value) => {
            pairs.insert(alias.to_string(), value.to_string());
        }
        None => {
            pairs.remove(alias);
        }
    }
    let body = pairs
        .iter()
        .map(|(key, value)| format!("\n  {key}: \"./{value}\"."))
        .collect::<String>()
        + "\n ";
    if let Some((start, end)) = extract_named_block_range(&root.utf8_text, "가지") {
        root.utf8_text.replace_range(start..end, &body);
    } else if let Some(project_pos) = root.utf8_text.find("프로젝트") {
        let open = project_pos
            + root.utf8_text[project_pos..].find('{').ok_or_else(|| {
                LocalProjectError::new("E_PROJECT_BLOCK_MISSING", "프로젝트 블록이 없습니다")
            })?;
        let close = find_matching_brace(&root.utf8_text, open).ok_or_else(|| {
            LocalProjectError::new(
                "E_PROJECT_BLOCK_MISSING",
                "프로젝트 블록이 닫히지 않았습니다",
            )
        })?;
        root.utf8_text
            .insert_str(close, &format!(" 가지 {{{body} }}"));
    }
    Ok(())
}

pub fn publish_local_gotgan(
    mut store: LocalGotganStore,
    artifact: LocalGajiArtifact,
) -> Result<LocalGotganStore, LocalProjectError> {
    if store.schema != LOCAL_GOTGAN_STORE_SCHEMA {
        return Err(LocalProjectError::new(
            "E_GOTGAN_STORE_SCHEMA",
            "지원하지 않는 local gotgan schema입니다",
        ));
    }
    verify_local_gaji_artifact(&artifact)?;
    for current in &store.artifacts {
        verify_local_gaji_artifact(current)?;
        if current.profile == artifact.profile
            && current.gaji_id == artifact.gaji_id
            && current.version == artifact.version
        {
            if current.package_sha256 == artifact.package_sha256 {
                return Ok(store);
            }
            return Err(LocalProjectError::new(
                "E_GOTGAN_VERSION_IMMUTABLE",
                "같은 profile/id/version에 다른 bytes를 덮어쓸 수 없습니다",
            ));
        }
    }
    store.artifacts.push(artifact);
    store.artifacts.sort_by(|a, b| {
        (&a.profile, &a.gaji_id, &a.version, &a.package_sha256).cmp(&(
            &b.profile,
            &b.gaji_id,
            &b.version,
            &b.package_sha256,
        ))
    });
    Ok(store)
}

pub fn search_local_gotgan(
    store: &LocalGotganStore,
    query: &str,
    profiles: &[String],
) -> Result<Vec<LocalGotganSearchRow>, LocalProjectError> {
    if store.schema != LOCAL_GOTGAN_STORE_SCHEMA {
        return Err(LocalProjectError::new(
            "E_GOTGAN_STORE_SCHEMA",
            "지원하지 않는 local gotgan schema입니다",
        ));
    }
    let needle = query.trim().to_lowercase();
    let profile_set = profiles.iter().cloned().collect::<BTreeSet<_>>();
    let mut rows = Vec::new();
    for artifact in &store.artifacts {
        verify_local_gaji_artifact(artifact)?;
        if !profile_set.is_empty() && !profile_set.contains(&artifact.profile) {
            continue;
        }
        let symbols = artifact
            .public_symbols
            .iter()
            .map(|item| item.external_name.clone())
            .collect::<Vec<_>>();
        let haystack = format!(
            "{} {} {} {}",
            artifact.gaji_id,
            artifact.description,
            artifact.tags.join(" "),
            symbols.join(" ")
        )
        .to_lowercase();
        if !needle.is_empty() && !haystack.contains(&needle) {
            continue;
        }
        rows.push(LocalGotganSearchRow {
            profile: artifact.profile.clone(),
            gaji_id: artifact.gaji_id.clone(),
            version: artifact.version.clone(),
            description: artifact.description.clone(),
            tags: artifact.tags.clone(),
            public_symbols: symbols,
            content_sha256: artifact.content_sha256.clone(),
            package_sha256: artifact.package_sha256.clone(),
            origin_project_ref: artifact.provenance.origin_project_ref.clone(),
            relation: artifact.provenance.relation.clone(),
        });
    }
    rows.sort_by(|a, b| {
        (&a.gaji_id, &a.profile, &a.version).cmp(&(&b.gaji_id, &b.profile, &b.version))
    });
    Ok(rows)
}

pub fn build_local_gaji_artifact(
    request: GajiExtractionPlanRequest,
) -> Result<LocalGajiArtifact, LocalProjectError> {
    if !matches!(request.relation.as_str(), "extracted" | "remix") {
        return Err(LocalProjectError::new(
            "E_GAJI_LINEAGE_RELATION",
            "가지 relation은 extracted 또는 remix여야 합니다",
        ));
    }
    if request.relation == "remix" && request.origin_gaji.as_deref().is_none_or(str::is_empty) {
        return Err(LocalProjectError::new(
            "E_GAJI_REMIX_ORIGIN_REQUIRED",
            "리믹스에는 원본 가지 id@version 계보가 필요합니다",
        ));
    }
    let source = request.source.clone();
    let description = request.description.clone();
    let tags = request.tags.clone();
    let origin_gaji = request.origin_gaji.clone();
    let relation = request.relation.clone();
    let plan = build_gaji_extraction_plan(request)?;
    let text_by_path = source
        .files
        .into_iter()
        .map(|file| (file.path, file.utf8_text))
        .collect::<BTreeMap<_, _>>();
    let mut manifest = format!(
        "id = \"{}\"\nversion = \"{}\"\ncontent_sha256 = \"{}\"\n",
        plan.gaji_id, plan.version, plan.content_sha256
    );
    manifest.push_str("\n[requires]\ndet_tier = \"D-STRICT\"\nopenness = \"closed\"\n");
    let mut files = vec![local_gaji_artifact_file("gaji.toml", manifest)];
    for path in &plan.included_modules {
        let text = text_by_path.get(path).ok_or_else(|| {
            LocalProjectError::with_path(
                "E_GAJI_ARTIFACT_SOURCE_MISSING",
                path,
                "추출 source 파일이 없습니다",
            )
        })?;
        files.push(local_gaji_artifact_file(
            &format!("ddn/{path}"),
            text.clone(),
        ));
    }
    files.sort_by(|a, b| a.path.cmp(&b.path));
    let package_sha256 = local_gaji_artifact_package_hash(&files);
    let artifact = LocalGajiArtifact {
        schema: LOCAL_GAJI_ARTIFACT_SCHEMA.to_string(),
        gaji_id: plan.gaji_id,
        version: plan.version,
        profile: plan.profile,
        description,
        tags,
        manifest_path: "gaji.toml".to_string(),
        content_sha256: plan.content_sha256,
        package_sha256,
        public_symbols: plan.public_symbols,
        dependencies: plan.external_gaji_dependencies,
        provenance: LocalGajiArtifactProvenance {
            origin_project_ref: plan.origin_project_ref,
            origin_gaji,
            relation,
            extraction_modules: plan.selected_modules,
        },
        files,
    };
    verify_local_gaji_artifact(&artifact)?;
    Ok(artifact)
}

pub fn verify_local_gaji_artifact(artifact: &LocalGajiArtifact) -> Result<(), LocalProjectError> {
    if artifact.schema != LOCAL_GAJI_ARTIFACT_SCHEMA {
        return Err(LocalProjectError::new(
            "E_GAJI_ARTIFACT_SCHEMA",
            "지원하지 않는 가지 artifact schema입니다",
        ));
    }
    if artifact.manifest_path != "gaji.toml"
        || artifact.files.iter().all(|file| file.path != "gaji.toml")
    {
        return Err(LocalProjectError::new(
            "E_GAJI_MANIFEST_MISSING",
            "가지 artifact에 gaji.toml이 필요합니다",
        ));
    }
    if artifact
        .files
        .iter()
        .all(|file| file.path != "ddn" && !file.path.starts_with("ddn/"))
    {
        return Err(LocalProjectError::new(
            "E_GAJI_DDN_MISSING",
            "가지 artifact에 ddn/ source가 필요합니다",
        ));
    }
    if artifact.files.len() > GAJI_ARTIFACT_MAX_FILES {
        return Err(LocalProjectError::new(
            "E_GAJI_ARTIFACT_FILE_COUNT_BOUND",
            format!("가지 파일은 최대 {GAJI_ARTIFACT_MAX_FILES}개입니다"),
        ));
    }
    let total_bytes = artifact
        .files
        .iter()
        .try_fold(0usize, |total, file| total.checked_add(file.byte_length))
        .ok_or_else(|| {
            LocalProjectError::new(
                "E_GAJI_ARTIFACT_TOTAL_BOUND",
                "가지 전체 byte 합이 범위를 넘었습니다",
            )
        })?;
    if total_bytes > GAJI_ARTIFACT_MAX_TOTAL_BYTES {
        return Err(LocalProjectError::new(
            "E_GAJI_ARTIFACT_TOTAL_BOUND",
            format!("가지 전체 크기는 최대 {GAJI_ARTIFACT_MAX_TOTAL_BYTES} bytes입니다"),
        ));
    }
    let mut seen = BTreeSet::new();
    let mut folded_seen = BTreeSet::new();
    for file in &artifact.files {
        let path = normalize_project_path(&file.path)?;
        if path != file.path
            || !seen.insert(path.clone())
            || !folded_seen.insert(path.to_lowercase())
        {
            return Err(LocalProjectError::with_path(
                "E_GAJI_ARTIFACT_PATH_DUPLICATE",
                path,
                "정규화 뒤 중복 artifact 경로입니다",
            ));
        }
        if file.byte_length > GAJI_ARTIFACT_MAX_SINGLE_FILE_BYTES {
            return Err(LocalProjectError::with_path(
                "E_GAJI_ARTIFACT_FILE_BOUND",
                path,
                format!("가지 단일 파일은 최대 {GAJI_ARTIFACT_MAX_SINGLE_FILE_BYTES} bytes입니다"),
            ));
        }
        if file.path == "gaji.toml" && file.byte_length > GAJI_ARTIFACT_MAX_MANIFEST_BYTES {
            return Err(LocalProjectError::with_path(
                "E_GAJI_MANIFEST_BOUND",
                path,
                format!("gaji.toml은 최대 {GAJI_ARTIFACT_MAX_MANIFEST_BYTES} bytes입니다"),
            ));
        }
        if file.byte_length != file.utf8_text.len()
            || file.sha256 != sha256_hex(file.utf8_text.as_bytes())
        {
            return Err(LocalProjectError::with_path(
                "E_GAJI_ARTIFACT_FILE_HASH",
                path,
                "가지 파일 길이 또는 hash가 일치하지 않습니다",
            ));
        }
    }
    if artifact.package_sha256 != local_gaji_artifact_package_hash(&artifact.files) {
        return Err(LocalProjectError::new(
            "E_GAJI_ARTIFACT_PACKAGE_HASH",
            "가지 package hash가 일치하지 않습니다",
        ));
    }
    let manifest = artifact
        .files
        .iter()
        .find(|file| file.path == "gaji.toml")
        .expect("checked manifest");
    let expected_content_row = format!("content_sha256 = \"{}\"", artifact.content_sha256);
    if !manifest
        .utf8_text
        .lines()
        .any(|line| line.trim() == expected_content_row)
    {
        return Err(LocalProjectError::new(
            "E_GAJI_MANIFEST_CONTENT_HASH",
            "manifest content hash가 artifact와 일치하지 않습니다",
        ));
    }
    Ok(())
}

fn local_gaji_artifact_file(path: &str, utf8_text: String) -> LocalGajiArtifactFile {
    LocalGajiArtifactFile {
        path: path.to_string(),
        byte_length: utf8_text.len(),
        sha256: sha256_hex(utf8_text.as_bytes()),
        utf8_text,
    }
}

fn local_gaji_artifact_package_hash(files: &[LocalGajiArtifactFile]) -> String {
    let mut rows = files
        .iter()
        .map(|file| (&file.path, &file.sha256, file.byte_length))
        .collect::<Vec<_>>();
    rows.sort();
    sha256_hex(
        serde_json::to_string(&rows)
            .expect("artifact package hash rows")
            .as_bytes(),
    )
}

pub fn build_gaji_extraction_plan(
    request: GajiExtractionPlanRequest,
) -> Result<GajiExtractionPlan, LocalProjectError> {
    if request.schema != GAJI_EXTRACTION_PLAN_SCHEMA {
        return Err(LocalProjectError::new(
            "E_GAJI_EXTRACTION_SCHEMA",
            format!("schema는 {GAJI_EXTRACTION_PLAN_SCHEMA} 이어야 합니다"),
        ));
    }
    if request.gaji_id.trim().is_empty()
        || request.gaji_id.contains(char::is_whitespace)
        || request.gaji_id.contains('/')
        || request.gaji_id.contains('\\')
    {
        return Err(LocalProjectError::new(
            "E_GAJI_ID_INVALID",
            "가지 id는 비어 있거나 공백·경로 구분자를 포함할 수 없습니다",
        ));
    }
    if request.version.trim().is_empty() {
        return Err(LocalProjectError::new(
            "E_GAJI_VERSION_INVALID",
            "가지 version이 필요합니다",
        ));
    }
    if !matches!(request.profile.as_str(), "표준" | "나눔" | "내") {
        return Err(LocalProjectError::new(
            "E_GOTGAN_PROFILE_INVALID",
            "profile은 표준/나눔/내 중 하나여야 합니다",
        ));
    }
    if request.selected_modules.is_empty() {
        return Err(LocalProjectError::new(
            "E_GAJI_MODULE_SELECTION_EMPTY",
            "가지로 묶을 모듈을 하나 이상 선택하세요",
        ));
    }
    let graph = build_project_graph(request.source.clone())?;
    let source_project_sha256 = virtual_project_source_sha256(&request.source)?;
    let text_by_path = request
        .source
        .files
        .iter()
        .map(|file| Ok((normalize_project_path(&file.path)?, file.utf8_text.clone())))
        .collect::<Result<BTreeMap<_, _>, LocalProjectError>>()?;
    let mut selected_modules = request
        .selected_modules
        .iter()
        .map(|path| normalize_project_reference(path))
        .collect::<Result<Vec<_>, _>>()?;
    selected_modules.sort();
    selected_modules.dedup();
    let mut modules = BTreeMap::new();
    for path in &selected_modules {
        if path == &graph.root_path || path == &graph.entry_path {
            return Err(LocalProjectError::with_path(
                "E_GAJI_MODULE_SELECTION_INVALID",
                path,
                "뿌리 또는 진입 파일은 재사용 모듈 추출 대상으로 선택할 수 없습니다",
            ));
        }
        collect_module_info(path, path, &text_by_path, &mut modules, &mut Vec::new())?;
    }
    let included_modules = modules
        .keys()
        .filter(|path| !path.starts_with("vendor/"))
        .cloned()
        .collect::<Vec<_>>();
    let mut external_gaji_dependencies = BTreeMap::new();
    for (alias, vendor_path) in &graph.gaji_aliases {
        if modules
            .keys()
            .any(|path| path == vendor_path || path.starts_with(&format!("{vendor_path}/")))
        {
            external_gaji_dependencies.insert(alias.clone(), vendor_path.clone());
        }
    }
    let mut public_symbols = Vec::new();
    for path in &included_modules {
        let info = modules.get(path).expect("included module metadata");
        for (external_name, internal_name) in &info.exports {
            public_symbols.push(GajiPublicSymbol {
                module_path: path.clone(),
                external_name: external_name.clone(),
                internal_name: internal_name.clone(),
            });
        }
    }
    public_symbols.sort_by(|a, b| {
        (&a.module_path, &a.external_name, &a.internal_name).cmp(&(
            &b.module_path,
            &b.external_name,
            &b.internal_name,
        ))
    });
    if public_symbols.is_empty() {
        return Err(LocalProjectError::new(
            "E_GAJI_PUBLIC_API_EMPTY",
            "선택한 모듈 dependency closure에 드러냄 공개 심볼이 없습니다",
        ));
    }
    let selected_set = selected_modules.iter().cloned().collect::<BTreeSet<_>>();
    let mut files = Vec::new();
    for path in &included_modules {
        let text = text_by_path.get(path).expect("included source text");
        files.push(GajiExtractionFile {
            path: path.clone(),
            byte_length: text.len(),
            sha256: sha256_hex(text.as_bytes()),
            selected: selected_set.contains(path),
        });
    }
    let included_set = included_modules.iter().cloned().collect::<BTreeSet<_>>();
    let excluded_files = text_by_path
        .keys()
        .filter(|path| !included_set.contains(*path))
        .cloned()
        .collect::<Vec<_>>();
    let content_sha256 = sha256_hex(
        serde_json::to_string(&json!({
            "schema": "ddn.gaji_extraction_content_hash_input.v1",
            "gaji_id": request.gaji_id,
            "version": request.version,
            "files": files,
            "public_symbols": public_symbols,
            "external_gaji_dependencies": external_gaji_dependencies,
        }))
        .expect("gaji extraction hash input")
        .as_bytes(),
    );
    Ok(GajiExtractionPlan {
        schema: GAJI_EXTRACTION_PLAN_SCHEMA,
        gaji_id: request.gaji_id,
        version: request.version,
        profile: request.profile,
        origin_project_ref: request.origin_project_ref,
        source_project_sha256,
        selected_modules,
        included_modules,
        excluded_files,
        public_symbols,
        external_gaji_dependencies,
        files,
        content_sha256,
        diagnostics: Vec::new(),
        publishable: true,
    })
}

pub fn virtual_project_source_sha256_json(input_json: &str) -> Result<String, LocalProjectError> {
    let source: VirtualProjectSource = serde_json::from_str(input_json).map_err(|err| {
        LocalProjectError::new(
            "E_VIRTUAL_PROJECT_JSON",
            format!("virtual project source JSON이 올바르지 않습니다: {err}"),
        )
    })?;
    virtual_project_source_sha256(&source)
}

pub fn virtual_project_source_sha256(
    source: &VirtualProjectSource,
) -> Result<String, LocalProjectError> {
    normalize_virtual_project_source(source.clone())?;
    let mut files = source.files.clone();
    files.sort_by(|a, b| a.path.cmp(&b.path));
    let canonical = serde_json::to_vec(&json!({
        "schema": source.schema,
        "kind": source.kind,
        "root_path": source.root_path,
        "entry_path": source.entry_path,
        "files": files,
    }))
    .expect("virtual project hash input serialization");
    Ok(sha256_hex(&canonical))
}

pub fn build_project_edit_plan(
    request: ProjectEditPlanRequest,
) -> Result<ProjectEditPlan, LocalProjectError> {
    let before_hash = virtual_project_source_sha256(&request.source)?;
    if request.expected_source_sha256 != before_hash {
        return Err(LocalProjectError::new(
            "E_PROJECT_EDIT_SOURCE_CONFLICT",
            "현재 project source hash가 계획 요청 시점과 달라 atomic apply를 거부했습니다",
        ));
    }
    match request.operation {
        ProjectEditOperation::RenameFile { from_path, to_path } => {
            build_rename_file_plan(request.source, &before_hash, &from_path, &to_path)
        }
        ProjectEditOperation::AddFile {
            path,
            utf8_text,
            role,
        } => build_add_file_plan(
            request.source,
            &before_hash,
            &path,
            &utf8_text,
            &role,
            "add_file",
        ),
        ProjectEditOperation::AddModule { path, module_name } => {
            let module_name = module_name.trim();
            if module_name.is_empty() || module_name.contains('.') || module_name.contains('"') {
                return Err(LocalProjectError::new(
                    "E_PROJECT_MODULE_NAME_INVALID",
                    "모듈 이름은 비어 있지 않은 한 이름이어야 합니다",
                ));
            }
            let template = format!("# {module_name} 모듈\n드러냄 {{ 값. }}\n\n값 <- 0.\n");
            build_add_file_plan(
                request.source,
                &before_hash,
                &path,
                &template,
                "ddn_source",
                "add_module",
            )
        }
        ProjectEditOperation::DuplicateFile { from_path, to_path } => {
            build_duplicate_file_plan(request.source, &before_hash, &from_path, &to_path)
        }
        ProjectEditOperation::DeleteFile { path } => {
            build_delete_file_plan(request.source, &before_hash, &path)
        }
        ProjectEditOperation::SetEntry { path } => {
            build_set_entry_plan(request.source, &before_hash, &path)
        }
    }
}

fn build_rename_file_plan(
    mut source: VirtualProjectSource,
    before_hash: &str,
    from_path: &str,
    to_path: &str,
) -> Result<ProjectEditPlan, LocalProjectError> {
    let from_path = normalize_project_path(from_path)?;
    let to_path = normalize_project_path(to_path)?;
    if from_path == PROJECT_ROOT_FILE {
        return Err(LocalProjectError::with_path(
            "E_PROJECT_ROOT_RENAME_FORBIDDEN",
            from_path,
            "뿌리.ddn은 이름을 바꿀 수 없습니다",
        ));
    }
    if source.files.iter().any(|file| file.path == to_path) {
        return Err(LocalProjectError::with_path(
            "E_PROJECT_PATH_DUPLICATE",
            to_path,
            "바꿀 경로가 이미 존재합니다",
        ));
    }
    if !source.files.iter().any(|file| file.path == from_path) {
        return Err(LocalProjectError::with_path(
            "E_PROJECT_EDIT_FILE_MISSING",
            from_path,
            "이름을 바꿀 파일이 없습니다",
        ));
    }

    let mut patches = Vec::new();
    let mut affected_files = BTreeSet::new();
    let mut affected_references = Vec::new();
    for file in &mut source.files {
        if file.path.ends_with(".ddn") {
            let block_names: &[&str] = if file.path == source.root_path {
                &["프로젝트"]
            } else {
                &["쓰임"]
            };
            for block_name in block_names {
                let edits =
                    structural_path_edits(&file.utf8_text, block_name, &from_path, &to_path)?;
                if !edits.is_empty() {
                    let original_path = file.path.clone();
                    apply_text_edits(&mut file.utf8_text, &edits);
                    affected_files.insert(original_path.clone());
                    for (start, end, before, after) in edits {
                        affected_references.push(format!("{original_path}:{start}-{end}"));
                        patches.push(ProjectEditPatch {
                            path: original_path.clone(),
                            start,
                            end,
                            before,
                            after,
                            reason: "structured_project_reference",
                        });
                    }
                }
            }
        }
    }
    let renamed = source
        .files
        .iter_mut()
        .find(|file| file.path == from_path)
        .expect("checked");
    renamed.path = to_path.clone();
    patches.push(ProjectEditPatch {
        path: from_path.clone(),
        start: 0,
        end: 0,
        before: from_path.clone(),
        after: to_path.clone(),
        reason: "file_path",
    });
    affected_files.insert(from_path.clone());
    affected_files.insert(to_path.clone());
    if source.entry_path == from_path {
        source.entry_path = to_path.clone();
    }
    let after_hash = virtual_project_source_sha256(&source)?;
    Ok(ProjectEditPlan {
        schema: PROJECT_EDIT_PLAN_SCHEMA,
        operation: "rename_file",
        before_source_sha256: before_hash.to_string(),
        after_source_sha256: after_hash,
        affected_files: affected_files.into_iter().collect(),
        affected_symbols: Vec::new(),
        affected_references,
        patches,
        diagnostics: Vec::new(),
        project_source: source,
        atomic_apply: true,
        lock_stale: true,
    })
}

fn build_add_file_plan(
    mut source: VirtualProjectSource,
    before_hash: &str,
    path: &str,
    utf8_text: &str,
    role: &str,
    operation: &'static str,
) -> Result<ProjectEditPlan, LocalProjectError> {
    let path = normalize_project_path(path)?;
    if source.files.iter().any(|file| file.path == path) {
        return Err(LocalProjectError::with_path(
            "E_PROJECT_PATH_DUPLICATE",
            path,
            "추가할 경로가 이미 존재합니다",
        ));
    }
    if role == "ddn_source" && !path.ends_with(".ddn") {
        return Err(LocalProjectError::with_path(
            "E_PROJECT_DDN_EXTENSION",
            path,
            "DDN source 파일 경로는 .ddn으로 끝나야 합니다",
        ));
    }
    source.files.push(VirtualProjectFileSource {
        path: path.clone(),
        role: role.to_string(),
        utf8_text: utf8_text.to_string(),
    });
    finish_simple_edit_plan(
        source,
        before_hash,
        operation,
        vec![path.clone()],
        vec![ProjectEditPatch {
            path,
            start: 0,
            end: 0,
            before: String::new(),
            after: utf8_text.to_string(),
            reason: "file_add",
        }],
        Vec::new(),
    )
}

fn build_duplicate_file_plan(
    source: VirtualProjectSource,
    before_hash: &str,
    from_path: &str,
    to_path: &str,
) -> Result<ProjectEditPlan, LocalProjectError> {
    let from_path = normalize_project_path(from_path)?;
    if from_path == PROJECT_ROOT_FILE {
        return Err(LocalProjectError::with_path(
            "E_PROJECT_ROOT_DUPLICATE_FORBIDDEN",
            from_path,
            "뿌리.ddn은 복제할 수 없습니다",
        ));
    }
    let original = source
        .files
        .iter()
        .find(|file| file.path == from_path)
        .ok_or_else(|| {
            LocalProjectError::with_path(
                "E_PROJECT_EDIT_FILE_MISSING",
                from_path,
                "복제할 파일이 없습니다",
            )
        })?;
    let text = original.utf8_text.clone();
    let role = original.role.clone();
    build_add_file_plan(source, before_hash, to_path, &text, &role, "duplicate_file")
}

fn build_delete_file_plan(
    mut source: VirtualProjectSource,
    before_hash: &str,
    path: &str,
) -> Result<ProjectEditPlan, LocalProjectError> {
    let path = normalize_project_path(path)?;
    if path == PROJECT_ROOT_FILE || path == source.root_path {
        return Err(LocalProjectError::with_path(
            "E_PROJECT_ROOT_DELETE_FORBIDDEN",
            path,
            "뿌리.ddn은 삭제할 수 없습니다",
        ));
    }
    if path == source.entry_path {
        return Err(LocalProjectError::with_path(
            "E_PROJECT_ENTRY_DELETE_FORBIDDEN",
            path,
            "현재 진입 파일은 삭제할 수 없습니다. 먼저 진입 파일을 바꾸세요",
        ));
    }
    if !source.files.iter().any(|file| file.path == path) {
        return Err(LocalProjectError::with_path(
            "E_PROJECT_EDIT_FILE_MISSING",
            path,
            "삭제할 파일이 없습니다",
        ));
    }
    let mut references = Vec::new();
    for file in &source.files {
        if !file.path.ends_with(".ddn") || file.path == path {
            continue;
        }
        for import in parse_imports(&file.utf8_text, &file.path)? {
            if resolve_import_source_path(&file.path, &import.source)? == path {
                references.push(format!("{}:쓰임.{}", file.path, import.alias));
            }
        }
    }
    if !references.is_empty() {
        return Err(LocalProjectError::with_path(
            "E_PROJECT_FILE_REFERENCED",
            path,
            format!(
                "참조 중인 모듈은 삭제할 수 없습니다: {}",
                references.join(", ")
            ),
        ));
    }
    let removed = source
        .files
        .iter()
        .find(|file| file.path == path)
        .expect("checked")
        .utf8_text
        .clone();
    source.files.retain(|file| file.path != path);
    finish_simple_edit_plan(
        source,
        before_hash,
        "delete_file",
        vec![path.clone()],
        vec![ProjectEditPatch {
            path,
            start: 0,
            end: removed.len(),
            before: removed,
            after: String::new(),
            reason: "file_delete",
        }],
        Vec::new(),
    )
}

fn build_set_entry_plan(
    mut source: VirtualProjectSource,
    before_hash: &str,
    path: &str,
) -> Result<ProjectEditPlan, LocalProjectError> {
    let path = normalize_project_path(path)?;
    let candidate = source
        .files
        .iter()
        .find(|file| file.path == path)
        .ok_or_else(|| {
            LocalProjectError::with_path(
                "E_PROJECT_ENTRY_MISSING",
                path.clone(),
                "진입 파일이 프로젝트에 없습니다",
            )
        })?;
    if candidate.role != "ddn_source" || !path.ends_with(".ddn") {
        return Err(LocalProjectError::with_path(
            "E_PROJECT_ENTRY_ROLE",
            path,
            "진입 파일은 DDN source여야 합니다",
        ));
    }
    let old_entry = source.entry_path.clone();
    let mut patches = Vec::new();
    let root = source
        .files
        .iter_mut()
        .find(|file| file.path == source.root_path)
        .expect("normalized root");
    let edits = structural_path_edits(&root.utf8_text, "프로젝트", &old_entry, &path)?;
    apply_text_edits(&mut root.utf8_text, &edits);
    for (start, end, before, after) in edits {
        patches.push(ProjectEditPatch {
            path: root.path.clone(),
            start,
            end,
            before,
            after,
            reason: "entry_reference",
        });
    }
    source.entry_path = path.clone();
    patches.push(ProjectEditPatch {
        path: "@project.entry_path".to_string(),
        start: 0,
        end: old_entry.len(),
        before: old_entry,
        after: path.clone(),
        reason: "entry_path",
    });
    finish_simple_edit_plan(
        source,
        before_hash,
        "set_entry",
        vec![path],
        patches,
        Vec::new(),
    )
}

fn finish_simple_edit_plan(
    source: VirtualProjectSource,
    before_hash: &str,
    operation: &'static str,
    affected_files: Vec<String>,
    patches: Vec<ProjectEditPatch>,
    affected_references: Vec<String>,
) -> Result<ProjectEditPlan, LocalProjectError> {
    let after_hash = virtual_project_source_sha256(&source)?;
    Ok(ProjectEditPlan {
        schema: PROJECT_EDIT_PLAN_SCHEMA,
        operation,
        before_source_sha256: before_hash.to_string(),
        after_source_sha256: after_hash,
        affected_files,
        affected_symbols: Vec::new(),
        affected_references,
        patches,
        diagnostics: Vec::new(),
        project_source: source,
        atomic_apply: true,
        lock_stale: true,
    })
}

fn structural_path_edits(
    text: &str,
    block_name: &str,
    from_path: &str,
    to_path: &str,
) -> Result<Vec<(usize, usize, String, String)>, LocalProjectError> {
    let Some((block_start, block_end)) = extract_named_block_range(text, block_name) else {
        return Ok(Vec::new());
    };
    let block = &text[block_start..block_end];
    let tokens = Lexer::new(block).tokenize().map_err(|err| {
        LocalProjectError::new(
            "E_PROJECT_EDIT_LEX",
            format!("구조 참조 분석에 실패했습니다: {err}"),
        )
    })?;
    let mut edits = Vec::new();
    for token in tokens {
        let TokenKind::StringLit(value) = token.kind else {
            continue;
        };
        let Ok(resolved) = normalize_project_reference(&value) else {
            continue;
        };
        let resolved = if resolved.ends_with(".ddn") {
            resolved
        } else {
            format!("{resolved}.ddn")
        };
        if resolved != from_path {
            continue;
        }
        let replacement_value = if value.ends_with(".ddn") {
            to_path.to_string()
        } else {
            to_path.trim_end_matches(".ddn").to_string()
        };
        let replacement_value = if value.starts_with("./") {
            format!("./{replacement_value}")
        } else {
            replacement_value
        };
        let start = block_start + token.span.start;
        let end = block_start + token.span.end;
        edits.push((start, end, token.raw, format!("\"{replacement_value}\"")));
    }
    Ok(edits)
}

fn apply_text_edits(text: &mut String, edits: &[(usize, usize, String, String)]) {
    for (start, end, _, after) in edits.iter().rev() {
        text.replace_range(*start..*end, after);
    }
}

pub fn discover_virtual_project_root_json(input_json: &str) -> Result<String, LocalProjectError> {
    let request: ProjectRootDiscoveryRequest = serde_json::from_str(input_json).map_err(|err| {
        LocalProjectError::new(
            "E_PROJECT_DISCOVERY_JSON_INVALID",
            format!("project root discovery JSON을 읽을 수 없습니다: {err}"),
        )
    })?;
    let result = discover_virtual_project_root(request)?;
    Ok(to_canonical_json_line(&result))
}

pub fn discover_disk_project_root_json(
    start: &Path,
    explicit_project: Option<&Path>,
) -> Result<String, LocalProjectError> {
    let result = discover_disk_project_root(start, explicit_project)?;
    Ok(to_canonical_json_line(&result))
}

pub fn build_project_graph_json(input_json: &str) -> Result<String, LocalProjectError> {
    let source: VirtualProjectSource = serde_json::from_str(input_json).map_err(|err| {
        LocalProjectError::new(
            "E_VIRTUAL_PROJECT_JSON_INVALID",
            format!("virtual project JSON을 읽을 수 없습니다: {err}"),
        )
    })?;
    let graph = build_project_graph(source)?;
    Ok(to_canonical_json_line(&graph))
}

pub fn build_project_symbol_boundary_json(input_json: &str) -> Result<String, LocalProjectError> {
    let source: VirtualProjectSource = serde_json::from_str(input_json).map_err(|err| {
        LocalProjectError::new(
            "E_VIRTUAL_PROJECT_JSON_INVALID",
            format!("virtual project JSON을 읽을 수 없습니다: {err}"),
        )
    })?;
    let symbols = build_project_symbol_boundary(source)?;
    Ok(to_canonical_json_line(&symbols))
}

pub fn build_project_gaji_lock_json(input_json: &str) -> Result<String, LocalProjectError> {
    let source: VirtualProjectSource = serde_json::from_str(input_json).map_err(|err| {
        LocalProjectError::new(
            "E_VIRTUAL_PROJECT_JSON_INVALID",
            format!("virtual project JSON을 읽을 수 없습니다: {err}"),
        )
    })?;
    let lock = build_project_gaji_lock(source, false)?;
    Ok(to_canonical_json_line(&lock))
}

pub fn verify_project_gaji_lock_json(input_json: &str) -> Result<String, LocalProjectError> {
    let source: VirtualProjectSource = serde_json::from_str(input_json).map_err(|err| {
        LocalProjectError::new(
            "E_VIRTUAL_PROJECT_JSON_INVALID",
            format!("virtual project JSON을 읽을 수 없습니다: {err}"),
        )
    })?;
    let lock = build_project_gaji_lock(source, true)?;
    Ok(to_canonical_json_line(&lock))
}

pub fn build_project_run_summary_json(
    input_json: &str,
    target: &str,
    inspect_graph: bool,
    inspect_lock: bool,
) -> Result<String, LocalProjectError> {
    let source: VirtualProjectSource = serde_json::from_str(input_json).map_err(|err| {
        LocalProjectError::new(
            "E_VIRTUAL_PROJECT_JSON_INVALID",
            format!("virtual project JSON을 읽을 수 없습니다: {err}"),
        )
    })?;
    let summary = build_project_run_summary(source, target, inspect_graph, inspect_lock)?;
    Ok(to_canonical_json_line(&summary))
}

pub fn build_project_prepare_link_json(
    input_json: &str,
    target: &str,
    inspect_graph: bool,
    inspect_lock: bool,
) -> Result<String, LocalProjectError> {
    let source: VirtualProjectSource = serde_json::from_str(input_json).map_err(|err| {
        LocalProjectError::new(
            "E_VIRTUAL_PROJECT_JSON_INVALID",
            format!("virtual project JSON을 읽을 수 없습니다: {err}"),
        )
    })?;
    let prepared = build_project_prepare_link(source, target, inspect_graph, inspect_lock)?;
    Ok(to_canonical_json_line(&prepared))
}

pub fn build_disk_project_run_summary_json(
    start: &Path,
    explicit_project: Option<&Path>,
    target: &str,
    inspect_graph: bool,
    inspect_lock: bool,
) -> Result<String, LocalProjectError> {
    let source = build_virtual_project_source_from_disk(start, explicit_project)?;
    let summary = build_project_run_summary(source, target, inspect_graph, inspect_lock)?;
    Ok(to_canonical_json_line(&summary))
}

pub fn build_project_graph(
    source: VirtualProjectSource,
) -> Result<LocalProjectGraph, LocalProjectError> {
    let normalized_manifest = normalize_virtual_project_source(source.clone())?;
    let root_path = normalized_manifest.root_path.clone();
    let entry_from_source = normalized_manifest.entry_path.clone();
    let mut text_by_path = BTreeMap::new();
    let mut role_by_path = BTreeMap::new();
    for file in source.files {
        let path = normalize_project_path(&file.path)?;
        role_by_path.insert(path.clone(), normalize_role(&file.role));
        text_by_path.insert(path, file.utf8_text);
    }
    let root_text = text_by_path.get(&root_path).ok_or_else(|| {
        LocalProjectError::with_path(
            "E_PROJECT_ROOT_MISSING",
            root_path.clone(),
            "project graph를 만들 root 파일이 없습니다",
        )
    })?;
    for (path, text) in &text_by_path {
        if path != &root_path && contains_project_block(text) {
            return Err(LocalProjectError::with_path(
                "E_PROJECT_BLOCK_OUTSIDE_ROOT",
                path,
                "프로젝트 {} 블록은 뿌리.ddn에서만 허용됩니다",
            ));
        }
    }
    let project_block = extract_project_block(root_text).ok_or_else(|| {
        LocalProjectError::with_path(
            "E_PROJECT_BLOCK_MISSING",
            root_path.clone(),
            "뿌리.ddn에 프로젝트 {} 블록이 없습니다",
        )
    })?;
    let project_name =
        extract_ddn_string_field(project_block, "이름").unwrap_or_else(|| "이름없음".to_string());
    let first_entry = extract_ddn_string_field(project_block, "첫글").ok_or_else(|| {
        LocalProjectError::with_path(
            "E_PROJECT_ENTRY_MISSING",
            root_path.clone(),
            "프로젝트 {} 안에 첫글이 필요합니다",
        )
    })?;
    let entry_path = normalize_project_reference(&first_entry)?;
    if entry_path != entry_from_source {
        return Err(LocalProjectError::with_path(
            "E_PROJECT_ENTRY_CONFLICT",
            root_path.clone(),
            format!("virtual entry({entry_from_source})와 프로젝트 첫글({entry_path})이 다릅니다"),
        ));
    }
    if !text_by_path.contains_key(&entry_path) {
        return Err(LocalProjectError::with_path(
            "E_PROJECT_ENTRY_MISSING",
            entry_path.clone(),
            "프로젝트 첫글 파일이 없습니다",
        ));
    }
    ensure_project_json_entry_matches_texts(&text_by_path, "", &root_path)?;

    let mut targets = parse_string_pairs_from_named_block(project_block, "목표")?;
    targets
        .entry("앱".to_string())
        .or_insert_with(|| entry_path.clone());
    for (target, path) in targets.iter_mut() {
        let normalized = normalize_project_reference(path)?;
        if !text_by_path.contains_key(&normalized) {
            return Err(LocalProjectError::with_path(
                "E_PROJECT_TARGET_MISSING",
                normalized,
                format!("목표 {target} 파일이 없습니다"),
            ));
        }
        *path = normalized;
    }
    let mut module_paths = parse_string_pairs_from_named_block(project_block, "모듈길")?;
    for path in module_paths.values_mut() {
        *path = normalize_project_reference_allow_root(path)?;
    }
    let mut gaji_aliases = parse_string_pairs_from_named_block(project_block, "가지")?;
    for path in gaji_aliases.values_mut() {
        *path = normalize_project_reference(path)?;
    }
    let files = normalized_manifest.files.clone();
    let hash_input = serde_json::to_string(&json!({
        "schema": "ddn.local_project_graph.hash_input.v1",
        "project_name": project_name,
        "root_path": root_path,
        "entry_path": entry_path,
        "targets": targets,
        "module_paths": module_paths,
        "gaji_aliases": gaji_aliases,
        "files": files,
    }))
    .expect("graph hash input serialization");
    let project_graph_sha256 = sha256_hex(hash_input.as_bytes());
    Ok(LocalProjectGraph {
        schema: PROJECT_GRAPH_SCHEMA,
        project_name,
        root_path,
        entry_path,
        targets,
        module_paths,
        gaji_aliases,
        file_count: files.len(),
        files,
        project_graph_sha256,
        diagnostics: Vec::new(),
    })
}

pub fn build_project_symbol_boundary(
    source: VirtualProjectSource,
) -> Result<LocalProjectSymbolBoundary, LocalProjectError> {
    build_linked_project(source, None).map(|linked| linked.symbol_boundary)
}

fn build_linked_project(
    source: VirtualProjectSource,
    target_path_override: Option<&str>,
) -> Result<LinkedProject, LocalProjectError> {
    build_linked_project_with_options(source, target_path_override, true)
}

fn build_linked_project_with_options(
    source: VirtualProjectSource,
    target_path_override: Option<&str>,
    run_for_symbol_values: bool,
) -> Result<LinkedProject, LocalProjectError> {
    let graph = build_project_graph(source.clone())?;
    let entry_path = target_path_override
        .unwrap_or(&graph.entry_path)
        .to_string();
    let mut text_by_path = BTreeMap::new();
    for file in source.files {
        let path = normalize_project_path(&file.path)?;
        text_by_path.insert(path, file.utf8_text);
    }
    let entry_text = text_by_path.get(&entry_path).ok_or_else(|| {
        LocalProjectError::with_path(
            "E_PROJECT_ENTRY_MISSING",
            entry_path.clone(),
            "entry 파일이 없습니다",
        )
    })?;
    let mut modules = BTreeMap::new();
    collect_module_info(
        &entry_path,
        &entry_path,
        &text_by_path,
        &mut modules,
        &mut Vec::new(),
    )?;

    let mut resolved_imports = Vec::new();
    let mut resolved_exports = Vec::new();
    for info in modules.values() {
        resolved_imports.extend(info.imports.iter().cloned());
        for (external_name, internal_name) in &info.exports {
            resolved_exports.push(ResolvedExport {
                module_path: info.path.clone(),
                external_name: external_name.clone(),
                internal_name: internal_name.clone(),
            });
        }
    }
    resolved_imports.sort_by(|a, b| {
        (&a.importer_path, &a.alias, &a.resolved_path).cmp(&(
            &b.importer_path,
            &b.alias,
            &b.resolved_path,
        ))
    });
    resolved_exports.sort_by(|a, b| {
        (&a.module_path, &a.external_name, &a.internal_name).cmp(&(
            &b.module_path,
            &b.external_name,
            &b.internal_name,
        ))
    });

    let show_requests = collect_alias_show_requests_from_ast(entry_text, &entry_path)?;
    let mut resolved_symbols = Vec::new();
    let mut entry_rewrites = BTreeMap::new();
    for request in show_requests {
        let entry_info = modules.get(&entry_path).expect("entry info exists");
        let import = entry_info
            .imports
            .iter()
            .find(|item| item.alias == request.alias)
            .ok_or_else(|| {
                LocalProjectError::with_path(
                    "E_ALIAS_UNKNOWN",
                    entry_path.clone(),
                    format!("알 수 없는 쓰임 alias입니다: {}", request.alias),
                )
            })?;
        let resolved = resolve_exported_symbol(
            &modules,
            &import.resolved_path,
            &request.symbol,
            &mut Vec::new(),
        )?;
        let final_row_key = resolved.internal_name.clone();
        entry_rewrites.insert(
            format!("{}.{}", request.alias, request.symbol),
            final_row_key.clone(),
        );
        resolved_symbols.push(ResolvedSymbol {
            alias: request.alias,
            symbol: request.symbol,
            module_path: resolved.module_path,
            internal_name: resolved.internal_name,
            value: String::new(),
        });
    }

    let mut module_graph_order = modules.keys().cloned().collect::<Vec<_>>();
    module_graph_order.sort();
    let module_graph_sha256 = sha256_hex(
        serde_json::to_string(&json!({
            "schema": "ddn.local_project.module_graph.hash_input.v1",
            "order": module_graph_order.clone(),
            "imports": resolved_imports.clone(),
            "exports": resolved_exports.clone(),
        }))
        .expect("module graph hash input serialization")
        .as_bytes(),
    );

    let execution_source = build_execution_source(
        &entry_path,
        &module_graph_order,
        &modules,
        &text_by_path,
        &entry_rewrites,
    )?;
    let output_rows = if run_for_symbol_values {
        let runtime =
            runtime_surface::run_summary_from_source(&execution_source, &entry_path, Some(1))
                .map_err(|err| {
                    LocalProjectError::with_path(
                        "E_PROJECT_RUNTIME",
                        entry_path.clone(),
                        format!("프로젝트 linked source 실제 실행 실패: {err}"),
                    )
                })?;
        let output_rows = json_string_array(runtime.get("output_log_texts"));
        let final_row = runtime
            .get("final_row")
            .and_then(JsonValue::as_object)
            .cloned()
            .unwrap_or_default();
        for symbol in &mut resolved_symbols {
            symbol.value = final_row
                .get(&symbol.internal_name)
                .map(json_scalar_to_output_text)
                .unwrap_or_default();
        }
        output_rows
    } else {
        Vec::new()
    };

    let hash_input = serde_json::to_string(&json!({
        "schema": "ddn.local_project_symbol_boundary.hash_input.v1",
        "entry_path": entry_path,
        "module_graph_order": module_graph_order.clone(),
        "module_graph_sha256": module_graph_sha256.clone(),
        "imports": resolved_imports.clone(),
        "exports": resolved_exports.clone(),
        "resolved_symbols": resolved_symbols.clone(),
        "output_rows": output_rows.clone(),
    }))
    .expect("symbol boundary hash input serialization");
    let symbol_boundary_sha256 = sha256_hex(hash_input.as_bytes());
    Ok(LinkedProject {
        symbol_boundary: LocalProjectSymbolBoundary {
            schema: PROJECT_SYMBOL_BOUNDARY_SCHEMA,
            entry_path,
            module_graph_order,
            module_graph_sha256,
            imports: resolved_imports,
            exports: resolved_exports,
            resolved_symbols,
            output_rows,
            symbol_boundary_sha256,
            diagnostics: Vec::new(),
        },
        execution_source,
    })
}

fn build_execution_source(
    entry_path: &str,
    module_graph_order: &[String],
    modules: &BTreeMap<String, ModuleInfo>,
    text_by_path: &BTreeMap<String, String>,
    entry_rewrites: &BTreeMap<String, String>,
) -> Result<String, LocalProjectError> {
    let mut out = String::new();
    out.push_str("// linked by ddn.local_project.linker.v1\n");
    for path in module_graph_order {
        if path == entry_path {
            continue;
        }
        let text = text_by_path.get(path).ok_or_else(|| {
            LocalProjectError::with_path("E_MODULE_MISSING", path.clone(), "모듈 파일이 없습니다")
        })?;
        let module = modules.get(path).ok_or_else(|| {
            LocalProjectError::with_path(
                "E_MODULE_MISSING",
                path.clone(),
                "모듈 metadata가 없습니다",
            )
        })?;
        let rewrites = module_alias_rewrites(module, modules)?;
        let stripped = strip_module_metadata_blocks(text)?;
        let rewritten = rewrite_alias_refs_from_tokens(&stripped, &rewrites)?;
        if !rewritten.trim().is_empty() {
            out.push_str("// module ");
            out.push_str(path);
            out.push('\n');
            out.push_str(&rewritten);
            if !out.ends_with('\n') {
                out.push('\n');
            }
        }
    }
    let entry_text = text_by_path.get(entry_path).ok_or_else(|| {
        LocalProjectError::with_path(
            "E_PROJECT_ENTRY_MISSING",
            entry_path,
            "entry 파일이 없습니다",
        )
    })?;
    let entry_body = strip_module_metadata_blocks(entry_text)?;
    let entry_rewritten = rewrite_alias_refs_from_tokens(&entry_body, entry_rewrites)?;
    out.push_str("// entry ");
    out.push_str(entry_path);
    out.push('\n');
    out.push_str(&entry_rewritten);
    if !out.ends_with('\n') {
        out.push('\n');
    }
    Ok(out)
}

fn module_alias_rewrites(
    module: &ModuleInfo,
    modules: &BTreeMap<String, ModuleInfo>,
) -> Result<BTreeMap<String, String>, LocalProjectError> {
    let mut rewrites = BTreeMap::new();
    for import in &module.imports {
        let imported = modules.get(&import.resolved_path).ok_or_else(|| {
            LocalProjectError::with_path(
                "E_MODULE_MISSING",
                import.resolved_path.clone(),
                "imported module metadata가 없습니다",
            )
        })?;
        for external_name in imported.exports.keys() {
            let resolved = resolve_exported_symbol(
                modules,
                &import.resolved_path,
                external_name,
                &mut Vec::new(),
            )?;
            rewrites.insert(
                format!("{}.{}", import.alias, external_name),
                resolved.internal_name,
            );
        }
    }
    Ok(rewrites)
}

fn strip_module_metadata_blocks(text: &str) -> Result<String, LocalProjectError> {
    let without_import = remove_named_block(text, "쓰임")?;
    let without_exports = remove_named_block(&without_import, "드러냄")?;
    remove_named_block(&without_exports, "공개")
}

fn remove_named_block(text: &str, name: &str) -> Result<String, LocalProjectError> {
    let mut out = String::new();
    let mut cursor = 0usize;
    while let Some(relative) = text[cursor..].find(name) {
        let start = cursor + relative;
        if !is_name_boundary(text, start, name.len()) {
            out.push_str(&text[cursor..start + name.len()]);
            cursor = start + name.len();
            continue;
        }
        let mut idx = start + name.len();
        while let Some(ch) = text[idx..].chars().next() {
            if ch.is_whitespace() {
                idx += ch.len_utf8();
            } else {
                break;
            }
        }
        if !text[idx..].starts_with('{') {
            out.push_str(&text[cursor..idx]);
            cursor = idx;
            continue;
        }
        let end = find_block_end(text, idx).ok_or_else(|| {
            LocalProjectError::new(
                "E_PROJECT_METADATA_BLOCK",
                format!("{name} metadata 블록을 닫지 못했습니다"),
            )
        })?;
        out.push_str(&text[cursor..start]);
        cursor = end;
    }
    out.push_str(&text[cursor..]);
    Ok(out)
}

fn find_block_end(text: &str, open_brace: usize) -> Option<usize> {
    let mut depth = 0usize;
    let mut in_string = false;
    let mut escape = false;
    let mut end = open_brace;
    for (offset, ch) in text[open_brace..].char_indices() {
        let idx = open_brace + offset;
        end = idx + ch.len_utf8();
        if in_string {
            if escape {
                escape = false;
            } else if ch == '\\' {
                escape = true;
            } else if ch == '"' {
                in_string = false;
            }
            continue;
        }
        if ch == '"' {
            in_string = true;
            continue;
        }
        if ch == '{' {
            depth += 1;
        } else if ch == '}' {
            depth = depth.checked_sub(1)?;
            if depth == 0 {
                let mut tail = end;
                while let Some(next) = text[tail..].chars().next() {
                    if next.is_whitespace() {
                        tail += next.len_utf8();
                    } else {
                        break;
                    }
                }
                if text[tail..].starts_with('.') {
                    tail += 1;
                }
                if text[tail..].starts_with('\r') {
                    tail += 1;
                }
                if text[tail..].starts_with('\n') {
                    tail += 1;
                }
                return Some(tail);
            }
        }
    }
    Some(end).filter(|_| depth == 0)
}

fn is_name_boundary(text: &str, start: usize, len: usize) -> bool {
    let before = text[..start].chars().next_back();
    let after = text[start + len..].chars().next();
    !before.map(is_identifier_char).unwrap_or(false)
        && !after.map(is_identifier_char).unwrap_or(false)
}

fn rewrite_alias_refs_from_tokens(
    text: &str,
    rewrites: &BTreeMap<String, String>,
) -> Result<String, LocalProjectError> {
    if rewrites.is_empty() {
        return Ok(text.to_string());
    }
    let tokens = Lexer::new(text).tokenize().map_err(|err| {
        LocalProjectError::new(
            "E_PROJECT_LINKER_LEX",
            format!("프로젝트 alias rewrite 토큰화 실패: {}", err.message),
        )
    })?;
    let mut replacements: Vec<(usize, usize, String)> = Vec::new();
    for window in tokens.windows(3) {
        let [left, dot, right] = window else {
            continue;
        };
        if !matches!(dot.kind, TokenKind::Dot) {
            continue;
        }
        let Some(alias) = token_name(left) else {
            continue;
        };
        let Some(symbol) = token_name(right) else {
            continue;
        };
        if !is_whitespace_only(text, left.span.end, dot.span.start)
            || !is_whitespace_only(text, dot.span.end, right.span.start)
        {
            continue;
        }
        let key = format!("{alias}.{symbol}");
        if let Some(to) = rewrites.get(&key) {
            replacements.push((left.span.start, right.span.end, to.clone()));
        }
    }
    if replacements.is_empty() {
        return Ok(text.to_string());
    }
    replacements.sort_by_key(|(start, _, _)| *start);
    let mut out = String::with_capacity(text.len());
    let mut cursor = 0usize;
    for (start, end, to) in replacements {
        if start < cursor {
            return Err(LocalProjectError::new(
                "E_PROJECT_LINKER_REWRITE_OVERLAP",
                "프로젝트 alias rewrite 범위가 겹칩니다",
            ));
        }
        out.push_str(&text[cursor..start]);
        out.push_str(&to);
        cursor = end;
    }
    out.push_str(&text[cursor..]);
    Ok(out)
}

fn token_name(token: &Token) -> Option<&str> {
    match &token.kind {
        TokenKind::Ident(name) | TokenKind::Josa(name) => Some(name.as_str()),
        _ => None,
    }
}

fn is_whitespace_only(text: &str, start: usize, end: usize) -> bool {
    start <= end && text[start..end].chars().all(char::is_whitespace)
}

fn is_identifier_char(ch: char) -> bool {
    ch == '_' || ch.is_alphanumeric() || ('가'..='힣').contains(&ch)
}

fn json_string_array(value: Option<&JsonValue>) -> Vec<String> {
    value
        .and_then(JsonValue::as_array)
        .map(|items| items.iter().map(json_scalar_to_output_text).collect())
        .unwrap_or_default()
}

fn json_scalar_to_output_text(value: &JsonValue) -> String {
    match value {
        JsonValue::String(text) => text.clone(),
        JsonValue::Number(number) => number.to_string(),
        JsonValue::Bool(value) => {
            if *value {
                "참".to_string()
            } else {
                "거짓".to_string()
            }
        }
        JsonValue::Null => "없음".to_string(),
        other => serde_json::to_string(other).unwrap_or_default(),
    }
}

fn build_project_observation_trace(
    output_rows: &[String],
    resolved_symbols: &[ResolvedSymbol],
    target_path: &str,
    runtime_state_hash: &str,
    runtime_execution_envelope: &JsonValue,
) -> JsonValue {
    let committed_madi = runtime_execution_envelope
        .get("effective_ticks")
        .and_then(JsonValue::as_u64)
        .unwrap_or(1);
    let mut rows = Vec::new();
    for (index, value_text) in output_rows.iter().enumerate() {
        let symbol = resolved_symbols.get(index);
        let source = symbol
            .map(|item| {
                json!({
                    "alias": item.alias,
                    "symbol": item.symbol,
                    "module_path": item.module_path,
                    "internal_name": item.internal_name,
                })
            })
            .unwrap_or(JsonValue::Null);
        let display_name = symbol
            .map(|item| {
                if item.alias.is_empty() {
                    item.symbol.clone()
                } else {
                    format!("{}.{}", item.alias, item.symbol)
                }
            })
            .unwrap_or_else(|| format!("output_{}", index + 1));
        let internal_name = symbol
            .map(|item| item.internal_name.clone())
            .unwrap_or_else(|| display_name.clone());
        rows.push(json!({
            "index": index,
            "observation_id": format!("project.obs.{}", index + 1),
            "name": display_name,
            "internal_name": internal_name,
            "value_text": value_text,
            "unit": null,
            "committed_madi": committed_madi,
            "target_path": target_path,
            "runtime_state_hash": runtime_state_hash,
            "source": source,
            "state_hash_participation": false,
        }));
    }
    let mut trace = json!({
        "schema": "ddn.local_project.observation_trace.v1",
        "row_count": rows.len(),
        "rows": rows,
        "determinism": {
            "source": "teul-cli project-run",
            "requested_ticks": 1,
            "committed_madi": committed_madi,
            "runtime_state_hash": runtime_state_hash,
            "state_hash_formula_change": false,
        },
    });
    let trace_hash = sha256_hex(
        serde_json::to_string(&trace)
            .expect("project observation trace hash input serialization")
            .as_bytes(),
    );
    if let JsonValue::Object(map) = &mut trace {
        map.insert("trace_sha256".to_string(), JsonValue::String(trace_hash));
    }
    trace
}

pub fn build_project_gaji_lock(
    source: VirtualProjectSource,
    require_existing_lock: bool,
) -> Result<LocalGajiLock, LocalProjectError> {
    let mut graph_source = source.clone();
    graph_source.files.retain(|file| {
        normalize_project_path(&file.path)
            .map(|path| path != "ddn.lock")
            .unwrap_or(true)
    });
    let graph = build_project_graph(graph_source)?;
    let mut text_by_path = BTreeMap::new();
    for file in source.files {
        let path = normalize_project_path(&file.path)?;
        text_by_path.insert(path, file.utf8_text);
    }

    let mut manifests = BTreeMap::new();
    for (alias, raw_path) in &graph.gaji_aliases {
        let path = normalize_project_reference(raw_path)?;
        let manifest = load_gaji_manifest_for_path(&path, &text_by_path)?;
        manifests.insert(manifest.id.clone(), manifest);
        let mut stack = vec![format!("project:{alias}")];
        collect_gaji_dependencies(&path, &text_by_path, &mut manifests, &mut stack)?;
    }

    let direct_ids = graph
        .gaji_aliases
        .values()
        .map(|path| normalize_project_reference(path))
        .collect::<Result<Vec<_>, _>>()?
        .into_iter()
        .map(|path| gaji_id_from_vendor_path(&path).map(|id| id.to_string()))
        .collect::<Result<BTreeSet<_>, _>>()?;

    let mut dependency_of = BTreeMap::<String, BTreeSet<String>>::new();
    for manifest in manifests.values() {
        for dep_id in manifest.dependencies.keys() {
            dependency_of
                .entry(dep_id.clone())
                .or_default()
                .insert(manifest.id.clone());
        }
    }

    let mut packages = Vec::new();
    for manifest in manifests.values() {
        packages.push(LocalGajiPin {
            id: manifest.id.clone(),
            version: manifest.version.clone(),
            path: gaji_vendor_path_for_id(&manifest.id),
            direct: direct_ids.contains(&manifest.id),
            dependency_of: dependency_of
                .remove(&manifest.id)
                .unwrap_or_default()
                .into_iter()
                .collect(),
            dependencies: manifest.dependencies.clone(),
            manifest_path: manifest.manifest_path.clone(),
            manifest_sha256: manifest.manifest_sha256.clone(),
            package_sha256: manifest.package_sha256.clone(),
        });
    }
    packages.sort_by(|a, b| a.id.cmp(&b.id));

    let lock_hash_input = serde_json::to_string(&json!({
        "schema": "ddn.local_gaji_lock.hash_input.v1",
        "project_graph_sha256": graph.project_graph_sha256,
        "packages": packages,
    }))
    .expect("local gaji lock hash input serialization");
    let lock_sha256 = sha256_hex(lock_hash_input.as_bytes());
    let lock = LocalGajiLock {
        schema: LOCAL_GAJI_LOCK_SCHEMA,
        lock_format: "ddn.lock.v0-local",
        root_path: graph.root_path,
        entry_path: graph.entry_path,
        project_graph_sha256: graph.project_graph_sha256,
        packages,
        lock_sha256,
        diagnostics: Vec::new(),
    };

    let canonical = to_canonical_json_line(&lock);
    match text_by_path.get("ddn.lock") {
        Some(existing) => {
            if existing.trim_end() != canonical.trim_end() {
                return Err(LocalProjectError::with_path(
                    "E_LOCK_HASH_MISMATCH",
                    "ddn.lock",
                    "ddn.lock 내용이 현재 vendored 가지 해소 결과와 다릅니다",
                ));
            }
        }
        None if require_existing_lock => {
            return Err(LocalProjectError::with_path(
                "E_LOCK_MISSING",
                "ddn.lock",
                "frozen 검증에는 ddn.lock이 필요합니다",
            ));
        }
        None => {}
    }

    Ok(lock)
}

pub fn build_project_prepare_link(
    source: VirtualProjectSource,
    target: &str,
    inspect_graph: bool,
    inspect_lock: bool,
) -> Result<LocalProjectPrepareLink, LocalProjectError> {
    let target = if target.trim().is_empty() {
        "앱"
    } else {
        target.trim()
    };
    let normalized_project = normalize_virtual_project_source(source.clone())?;
    let graph = build_project_graph(source.clone())?;
    let target_path = graph.targets.get(target).cloned().ok_or_else(|| {
        LocalProjectError::with_path(
            "E_PROJECT_TARGET_MISSING",
            graph.root_path.clone(),
            format!("프로젝트 목표 {target}을 찾을 수 없습니다"),
        )
    })?;
    let lock_required = !graph.gaji_aliases.is_empty();
    let verified_lock = if inspect_lock && lock_required {
        Some(build_project_gaji_lock(source.clone(), true)?)
    } else {
        None
    };
    let linked = build_linked_project_with_options(source, Some(&target_path), false)?;
    let linked_execution_source_sha256 = sha256_hex(linked.execution_source.as_bytes());
    let runtime_execution_envelope =
        runtime_surface::execution_envelope_from_source(&linked.execution_source, Some(1))
            .map_err(|err| {
                LocalProjectError::with_path(
                    "E_PROJECT_EXECUTION_MODE_DECISION",
                    target_path.clone(),
                    format!("프로젝트 실행 모드 판정 실패: {err}"),
                )
            })?;
    let mut prepared = LocalProjectPrepareLink {
        schema: "ddn.local_project.prepare_link.v1",
        frontdoor: "wasm_project_prepare_link_json",
        root_path: graph.root_path.clone(),
        entry_path: graph.entry_path.clone(),
        target: target.to_string(),
        target_path,
        file_count: graph.file_count,
        normalized_project,
        project_graph: graph,
        graph_inspected: inspect_graph,
        lock_required,
        lock_inspected: inspect_lock,
        verified_lock,
        linked_execution_source: linked.execution_source,
        linked_execution_source_sha256,
        runtime_execution_envelope,
        symbol_boundary: linked.symbol_boundary,
        diagnostics: Vec::new(),
        state_hash_formula_change: false,
        prepare_link_sha256: String::new(),
    };
    let hash_input = serde_json::to_string(&json!({
        "schema": "ddn.local_project.prepare_link.hash_input.v1",
        "root_path": &prepared.root_path,
        "entry_path": &prepared.entry_path,
        "target": &prepared.target,
        "target_path": &prepared.target_path,
        "project_graph_sha256": &prepared.project_graph.project_graph_sha256,
        "lock_required": prepared.lock_required,
        "lock_sha256": prepared.verified_lock.as_ref().map(|lock| lock.lock_sha256.clone()),
        "linked_execution_source_sha256": &prepared.linked_execution_source_sha256,
        "runtime_execution_envelope": &prepared.runtime_execution_envelope,
        "symbol_boundary_sha256": &prepared.symbol_boundary.symbol_boundary_sha256,
        "state_hash_formula_change": prepared.state_hash_formula_change,
    }))
    .expect("local project prepare/link hash input serialization");
    prepared.prepare_link_sha256 = sha256_hex(hash_input.as_bytes());
    Ok(prepared)
}

pub fn build_project_run_summary(
    source: VirtualProjectSource,
    target: &str,
    inspect_graph: bool,
    inspect_lock: bool,
) -> Result<LocalProjectRunSummary, LocalProjectError> {
    let target = if target.trim().is_empty() {
        "앱"
    } else {
        target.trim()
    };
    let graph = build_project_graph(source.clone())?;
    let target_path = graph.targets.get(target).cloned().ok_or_else(|| {
        LocalProjectError::with_path(
            "E_PROJECT_TARGET_MISSING",
            graph.root_path.clone(),
            format!("프로젝트 목표 {target}을 찾을 수 없습니다"),
        )
    })?;
    if inspect_lock && !graph.gaji_aliases.is_empty() {
        build_project_gaji_lock(source.clone(), true)?;
    }
    let lock_sha256 = if graph.gaji_aliases.is_empty() {
        None
    } else {
        Some(build_project_gaji_lock(source.clone(), false)?.lock_sha256)
    };
    let linked = build_linked_project(source, Some(&target_path))?;
    let symbols = linked.symbol_boundary;
    let runtime =
        runtime_surface::run_summary_from_source(&linked.execution_source, &target_path, Some(1))
            .map_err(|err| {
            LocalProjectError::with_path(
                "E_PROJECT_RUNTIME",
                target_path.clone(),
                format!("프로젝트 entry 실제 실행 실패: {err}"),
            )
        })?;
    let runtime_output_log_texts = json_string_array(runtime.get("output_log_texts"));
    let runtime_final_row = runtime
        .get("final_row")
        .cloned()
        .unwrap_or_else(|| JsonValue::Object(Default::default()));
    let runtime_state_hash = runtime
        .get("state_hash")
        .and_then(JsonValue::as_str)
        .unwrap_or_default()
        .to_string();
    let runtime_execution_envelope = runtime
        .get("execution_envelope")
        .cloned()
        .unwrap_or(JsonValue::Null);
    let canonical_ddn = runtime
        .get("canonical_ddn")
        .and_then(JsonValue::as_str)
        .unwrap_or_default()
        .to_string();
    let linked_execution_source_sha256 = sha256_hex(linked.execution_source.as_bytes());
    let linked_execution_canonical_sha256 = sha256_hex(canonical_ddn.as_bytes());
    let project_observation_trace = build_project_observation_trace(
        &runtime_output_log_texts,
        &symbols.resolved_symbols,
        &target_path,
        &runtime_state_hash,
        &runtime_execution_envelope,
    );
    let execution_preparation = json!({
        "schema": "ddn.local_project.execution_preparation.v1",
        "root_path": graph.root_path,
        "entry_path": graph.entry_path,
        "target": target,
        "target_path": target_path,
        "file_count": graph.file_count,
        "graph": {
            "project_graph_sha256": graph.project_graph_sha256,
            "module_graph_order": symbols.module_graph_order,
            "module_graph_sha256": symbols.module_graph_sha256,
        },
        "lock": {
            "inspected": inspect_lock,
            "required": !graph.gaji_aliases.is_empty(),
            "lock_sha256": lock_sha256,
        },
        "linked_source": {
            "source_sha256": linked_execution_source_sha256,
            "canonical_sha256": linked_execution_canonical_sha256,
        },
        "runtime_request": {
            "frontdoor": "teul-cli project-run",
            "requested_ticks": 1,
            "target": target,
            "target_path": target_path,
        },
        "limits": {
            "max_project_files": MAX_PROJECT_FILES,
            "max_file_bytes": MAX_FILE_BYTES,
            "max_serialized_artifact_bytes": MAX_SERIALIZED_ARTIFACT_BYTES,
        },
        "provenance": {
            "imports": symbols.imports,
            "exports": symbols.exports,
            "resolved_symbols": symbols.resolved_symbols,
        },
        "diagnostics": [],
        "state_hash_formula_change": false,
    });
    let summary_hash_input = serde_json::to_string(&json!({
        "schema": "ddn.local_project_run_summary.hash_input.v1",
        "target": target,
        "target_path": target_path,
        "project_graph_sha256": graph.project_graph_sha256,
        "lock_sha256": lock_sha256,
        "symbol_boundary_sha256": symbols.symbol_boundary_sha256,
        "output_rows": runtime_output_log_texts,
        "runtime_state_hash": runtime_state_hash,
        "runtime_execution_envelope": runtime_execution_envelope,
        "execution_preparation": execution_preparation,
        "project_observation_trace": project_observation_trace,
        "linked_execution_source_sha256": linked_execution_source_sha256,
        "linked_execution_canonical_sha256": linked_execution_canonical_sha256,
    }))
    .expect("local project run summary hash input serialization");
    let bounded_state_sha256 = sha256_hex(
        serde_json::to_string(&json!({
            "schema": "ddn.local_project_run_summary.bounded_state.v1",
            "state_hash": runtime_state_hash,
            "output_rows": runtime_output_log_texts,
        }))
        .expect("bounded state hash input serialization")
        .as_bytes(),
    );
    let summary_sha256 = sha256_hex(summary_hash_input.as_bytes());
    Ok(LocalProjectRunSummary {
        schema: LOCAL_PROJECT_RUN_SUMMARY_SCHEMA,
        frontdoor: "teul-cli project-run",
        root_path: graph.root_path,
        entry_path: graph.entry_path,
        target: target.to_string(),
        target_path,
        file_count: graph.file_count,
        project_graph_sha256: graph.project_graph_sha256,
        lock_sha256,
        symbol_boundary_sha256: symbols.symbol_boundary_sha256,
        output_rows: runtime_output_log_texts.clone(),
        runtime_output_log_texts,
        runtime_final_row,
        runtime_state_hash,
        runtime_execution_envelope,
        execution_preparation,
        project_observation_trace,
        linked_execution_source: linked.execution_source.clone(),
        linked_execution_canonical_ddn: canonical_ddn.clone(),
        linked_execution_source_sha256,
        linked_execution_canonical_sha256,
        bounded_state_sha256,
        graph_inspected: inspect_graph,
        lock_inspected: inspect_lock,
        summary_sha256,
        diagnostics: Vec::new(),
    })
}

pub fn discover_virtual_project_root(
    request: ProjectRootDiscoveryRequest,
) -> Result<ProjectRootDiscoveryResult, LocalProjectError> {
    if request.schema != PROJECT_ROOT_DISCOVERY_REQUEST_SCHEMA {
        return Err(LocalProjectError::new(
            "E_PROJECT_DISCOVERY_SCHEMA",
            format!("schema는 {PROJECT_ROOT_DISCOVERY_REQUEST_SCHEMA} 이어야 합니다"),
        ));
    }
    let start = normalize_project_path(&request.start_path)?;
    let explicit = request
        .explicit_project_path
        .as_deref()
        .map(normalize_project_path)
        .transpose()?;
    let mut files = BTreeSet::new();
    let mut file_texts = BTreeMap::new();
    for file in request.files {
        let path = normalize_project_path(&file.path)?;
        if let Some(text) = file.utf8_text {
            file_texts.insert(path.clone(), text);
        }
        files.insert(path);
    }
    discover_root_from_file_set(&files, Some(&file_texts), &start, explicit.as_deref())
}

pub fn discover_disk_project_root(
    start: &Path,
    explicit_project: Option<&Path>,
) -> Result<ProjectRootDiscoveryResult, LocalProjectError> {
    let start_abs = if start.is_absolute() {
        start.to_path_buf()
    } else {
        std::env::current_dir()
            .map_err(|err| LocalProjectError::new("E_PROJECT_CWD", err.to_string()))?
            .join(start)
    };
    let start_for_walk = if start_abs.is_file() {
        start_abs
            .parent()
            .map(Path::to_path_buf)
            .unwrap_or_else(|| start_abs.clone())
    } else {
        start_abs.clone()
    };
    if let Some(explicit) = explicit_project {
        let explicit_abs = if explicit.is_absolute() {
            explicit.to_path_buf()
        } else {
            std::env::current_dir()
                .map_err(|err| LocalProjectError::new("E_PROJECT_CWD", err.to_string()))?
                .join(explicit)
        };
        let result = discover_disk_explicit_project(&explicit_abs)?;
        ensure_no_symlink_escape(&start_abs, &explicit_root_dir(&explicit_abs)?)?;
        return Ok(result);
    }
    discover_disk_upward(&start_for_walk, &start_abs)
}

pub fn build_virtual_project_source_from_disk(
    start: &Path,
    explicit_project: Option<&Path>,
) -> Result<VirtualProjectSource, LocalProjectError> {
    let root_dir = discover_disk_project_root_dir(start, explicit_project)?;
    let root_text = fs::read_to_string(root_dir.join(PROJECT_ROOT_FILE)).map_err(|err| {
        LocalProjectError::with_path(
            "E_PROJECT_FILE_READ",
            PROJECT_ROOT_FILE,
            format!("뿌리.ddn을 읽을 수 없습니다: {err}"),
        )
    })?;
    let project_block = extract_project_block(&root_text).ok_or_else(|| {
        LocalProjectError::with_path(
            "E_PROJECT_BLOCK_MISSING",
            PROJECT_ROOT_FILE,
            "뿌리.ddn에 프로젝트 {} 블록이 없습니다",
        )
    })?;
    let first_entry = extract_ddn_string_field(project_block, "첫글").ok_or_else(|| {
        LocalProjectError::with_path(
            "E_PROJECT_ENTRY_MISSING",
            PROJECT_ROOT_FILE,
            "프로젝트 {} 안에 첫글이 필요합니다",
        )
    })?;
    let entry_path = normalize_project_reference(&first_entry)?;
    let mut files = Vec::new();
    collect_disk_project_files(&root_dir, &root_dir, &mut files)?;
    Ok(VirtualProjectSource {
        schema: VIRTUAL_PROJECT_SOURCE_SCHEMA.to_string(),
        kind: Some(LOCAL_PROJECT_TREE_KIND.to_string()),
        root_path: PROJECT_ROOT_FILE.to_string(),
        entry_path,
        files,
    })
}

pub fn normalize_virtual_project_source(
    source: VirtualProjectSource,
) -> Result<NormalizedProjectManifest, LocalProjectError> {
    if source.schema != VIRTUAL_PROJECT_SOURCE_SCHEMA {
        return Err(LocalProjectError::new(
            "E_VIRTUAL_PROJECT_SCHEMA",
            format!("schema는 {VIRTUAL_PROJECT_SOURCE_SCHEMA} 이어야 합니다"),
        ));
    }
    if let Some(kind) = &source.kind {
        if kind != LOCAL_PROJECT_TREE_KIND {
            return Err(LocalProjectError::new(
                "E_VIRTUAL_PROJECT_KIND",
                format!("kind는 {LOCAL_PROJECT_TREE_KIND} 이어야 합니다"),
            ));
        }
    }
    if source.files.len() > MAX_PROJECT_FILES {
        return Err(LocalProjectError::new(
            "E_PROJECT_FILE_COUNT_LIMIT",
            format!("파일 수가 {MAX_PROJECT_FILES}개를 넘었습니다"),
        ));
    }

    let root_path = normalize_project_path(&source.root_path)?;
    let entry_path = normalize_project_path(&source.entry_path)?;
    let mut normalized_paths = BTreeSet::new();
    let mut case_fold_paths = BTreeMap::<String, String>::new();
    let mut files = Vec::with_capacity(source.files.len());
    let mut total_utf8_bytes = 0usize;
    for file in source.files {
        let path = normalize_project_path(&file.path)?;
        validate_role(&file.role, &path)?;
        if !normalized_paths.insert(path.clone()) {
            return Err(LocalProjectError::with_path(
                "E_PROJECT_PATH_DUPLICATE",
                path,
                "같은 정규 경로가 두 번 들어왔습니다",
            ));
        }
        let folded = path.to_ascii_lowercase();
        if let Some(existing) = case_fold_paths.insert(folded, path.clone()) {
            return Err(LocalProjectError::with_path(
                "E_PROJECT_PATH_CASE_COLLISION",
                path,
                format!("Windows 대소문자 접기 기준으로 {existing} 경로와 충돌합니다"),
            ));
        }
        let byte_len = file.utf8_text.as_bytes().len();
        if byte_len > MAX_FILE_BYTES {
            return Err(LocalProjectError::with_path(
                "E_PROJECT_FILE_SIZE_LIMIT",
                path,
                format!("파일이 {MAX_FILE_BYTES} 바이트 제한을 넘었습니다"),
            ));
        }
        total_utf8_bytes = total_utf8_bytes.checked_add(byte_len).ok_or_else(|| {
            LocalProjectError::new("E_PROJECT_TOTAL_SIZE_LIMIT", "프로젝트 크기가 너무 큽니다")
        })?;
        if total_utf8_bytes > MAX_PROJECT_TOTAL_UTF8_BYTES {
            return Err(LocalProjectError::new(
                "E_PROJECT_TOTAL_SIZE_LIMIT",
                format!("프로젝트 UTF-8 본문 합계가 {MAX_PROJECT_TOTAL_UTF8_BYTES} 바이트 제한을 넘었습니다"),
            ));
        }
        let sha256 = sha256_hex(file.utf8_text.as_bytes());
        files.push(PendingFile {
            path,
            role: normalize_role(&file.role),
            byte_len,
            sha256,
        });
    }
    if !normalized_paths.contains(&root_path) {
        return Err(LocalProjectError::with_path(
            "E_PROJECT_ROOT_MISSING",
            root_path,
            "virtual project source에 root 파일이 없습니다",
        ));
    }
    if !normalized_paths.contains(&entry_path) {
        return Err(LocalProjectError::with_path(
            "E_PROJECT_ENTRY_MISSING",
            entry_path,
            "virtual project source에 entry 파일이 없습니다",
        ));
    }

    files.sort_by(|a, b| a.path.cmp(&b.path));
    let graph_input = graph_hash_input(&root_path, &entry_path, &files);
    let project_graph_sha256 = sha256_hex(graph_input.as_bytes());
    let lock_sha256 = files
        .iter()
        .find(|file| file.path == "ddn.lock")
        .map(|file| file.sha256.clone());
    let mut manifest = NormalizedProjectManifest {
        schema: VIRTUAL_PROJECT_MANIFEST_SCHEMA,
        kind: LOCAL_PROJECT_TREE_KIND,
        root_path,
        entry_path,
        file_count: files.len(),
        total_utf8_bytes,
        files: files
            .iter()
            .map(|file| NormalizedProjectFile {
                path: file.path.clone(),
                role: file.role.clone(),
                byte_length: file.byte_len,
                sha256: file.sha256.clone(),
            })
            .collect(),
        project_graph_sha256,
        lock_sha256,
        canonical_manifest_sha256: String::new(),
        limits: ProjectLimits {
            max_files: MAX_PROJECT_FILES,
            max_file_bytes: MAX_FILE_BYTES,
            max_serialized_artifact_bytes: MAX_SERIALIZED_ARTIFACT_BYTES,
        },
    };
    let manifest_without_hash = to_canonical_json_line(&manifest);
    if manifest_without_hash.as_bytes().len() > MAX_SERIALIZED_ARTIFACT_BYTES {
        return Err(LocalProjectError::new(
            "E_PROJECT_SERIALIZED_SIZE_LIMIT",
            format!("정규 manifest가 {MAX_SERIALIZED_ARTIFACT_BYTES} 바이트 제한을 넘었습니다"),
        ));
    }
    manifest.canonical_manifest_sha256 = sha256_hex(manifest_without_hash.as_bytes());
    Ok(manifest)
}

pub fn normalize_project_path(raw: &str) -> Result<String, LocalProjectError> {
    let trimmed = raw.trim();
    if trimmed.is_empty() {
        return Err(LocalProjectError::new(
            "E_PROJECT_PATH_EMPTY",
            "빈 경로는 사용할 수 없습니다",
        ));
    }
    if trimmed.contains('\\') {
        return Err(LocalProjectError::with_path(
            "E_PROJECT_PATH_BACKSLASH",
            trimmed,
            "경로 구분자는 / 만 허용합니다",
        ));
    }
    if trimmed.contains('\0') || trimmed.chars().any(|ch| ch.is_control()) {
        return Err(LocalProjectError::with_path(
            "E_PROJECT_PATH_CONTROL",
            trimmed,
            "제어 문자가 들어간 경로는 사용할 수 없습니다",
        ));
    }
    if trimmed.starts_with('/')
        || trimmed.starts_with("//")
        || trimmed.contains("://")
        || looks_like_windows_drive(trimmed)
    {
        return Err(LocalProjectError::with_path(
            "E_PROJECT_PATH_ABSOLUTE",
            trimmed,
            "프로젝트 경로는 상대 경로여야 합니다",
        ));
    }
    let nfc = trimmed.nfc().collect::<String>();
    let parts: Vec<&str> = nfc.split('/').collect();
    if parts
        .iter()
        .any(|part| part.is_empty() || *part == "." || *part == "..")
    {
        return Err(LocalProjectError::with_path(
            "E_PROJECT_PATH_SEGMENT",
            trimmed,
            ". 또는 .. 또는 빈 경로 조각은 사용할 수 없습니다",
        ));
    }
    Ok(parts.join("/"))
}

fn validate_role(raw: &str, path: &str) -> Result<(), LocalProjectError> {
    let role = normalize_role(raw);
    match role.as_str() {
        "root" | "ddn_source" | "project_json" | "lock" | "gaji_manifest" | "metadata" => Ok(()),
        _ => Err(LocalProjectError::with_path(
            "E_PROJECT_FILE_ROLE",
            path,
            format!("지원하지 않는 project file role입니다: {raw}"),
        )),
    }
}

fn normalize_role(raw: &str) -> String {
    match raw.trim() {
        "뿌리.ddn" => "root".to_string(),
        "DDN source" => "ddn_source".to_string(),
        other => other.to_string(),
    }
}

fn looks_like_windows_drive(path: &str) -> bool {
    let bytes = path.as_bytes();
    bytes.len() >= 2 && bytes[0].is_ascii_alphabetic() && bytes[1] == b':'
}

fn discover_root_from_file_set(
    files: &BTreeSet<String>,
    file_texts: Option<&BTreeMap<String, String>>,
    start_path: &str,
    explicit_project_path: Option<&str>,
) -> Result<ProjectRootDiscoveryResult, LocalProjectError> {
    if let Some(explicit) = explicit_project_path {
        return discover_explicit_from_file_set(files, file_texts, explicit);
    }
    let dirs = virtual_parent_dirs(files, start_path);
    for dir in &dirs {
        if has_file(files, dir, PROJECT_ROOT_FILE) {
            if let Some(legacy) = legacy_in_dir(files, dir) {
                return Err(LocalProjectError::with_path(
                    "E_PROJECT_ROOT_AMBIGUOUS",
                    join_project_path(dir, legacy),
                    "현재 root 이름과 legacy root 이름이 같은 디렉터리에 있습니다",
                ));
            }
            ensure_no_project_json_entry_conflict_virtual(files, file_texts, dir)?;
            return Ok(root_result(join_project_path(dir, PROJECT_ROOT_FILE), None));
        }
    }
    for dir in &dirs {
        if let Some(legacy) = legacy_in_dir(files, dir) {
            return Err(LocalProjectError::with_path(
                "E_LEGACY_PROJECT_ROOT_NAME",
                join_project_path(dir, legacy),
                "legacy root 파일명은 current alias가 아닙니다. 뿌리.ddn을 사용하세요",
            ));
        }
    }
    for dir in &dirs {
        if has_file(files, dir, PROJECT_JSON_FILE) {
            return Ok(root_result(
                String::new(),
                Some(join_project_path(dir, PROJECT_JSON_FILE)),
            ));
        }
    }
    Err(LocalProjectError::new(
        "E_PROJECT_ROOT_MISSING",
        "뿌리.ddn 또는 ddn.project.json을 찾지 못했습니다",
    ))
}

fn discover_explicit_from_file_set(
    files: &BTreeSet<String>,
    file_texts: Option<&BTreeMap<String, String>>,
    explicit: &str,
) -> Result<ProjectRootDiscoveryResult, LocalProjectError> {
    if path_file_name(explicit) == Some(PROJECT_ROOT_FILE) && files.contains(explicit) {
        ensure_no_project_json_entry_conflict_virtual(files, file_texts, &parent_dir(explicit))?;
        return Ok(root_result(explicit.to_string(), None));
    }
    if path_file_name(explicit) == Some(PROJECT_JSON_FILE) && files.contains(explicit) {
        return Ok(root_result(String::new(), Some(explicit.to_string())));
    }
    if LEGACY_ROOT_FILES
        .iter()
        .any(|legacy| path_file_name(explicit) == Some(*legacy) && files.contains(explicit))
    {
        return Err(LocalProjectError::with_path(
            "E_LEGACY_PROJECT_ROOT_NAME",
            explicit,
            "legacy root 파일명은 current alias가 아닙니다. 뿌리.ddn을 사용하세요",
        ));
    }
    let dir = if files.contains(explicit) {
        parent_dir(explicit)
    } else {
        explicit.to_string()
    };
    if has_file(files, &dir, PROJECT_ROOT_FILE) {
        if let Some(legacy) = legacy_in_dir(files, &dir) {
            return Err(LocalProjectError::with_path(
                "E_PROJECT_ROOT_AMBIGUOUS",
                join_project_path(&dir, legacy),
                "현재 root 이름과 legacy root 이름이 같은 디렉터리에 있습니다",
            ));
        }
        ensure_no_project_json_entry_conflict_virtual(files, file_texts, &dir)?;
        return Ok(root_result(
            join_project_path(&dir, PROJECT_ROOT_FILE),
            None,
        ));
    }
    if let Some(legacy) = legacy_in_dir(files, &dir) {
        return Err(LocalProjectError::with_path(
            "E_LEGACY_PROJECT_ROOT_NAME",
            join_project_path(&dir, legacy),
            "legacy root 파일명은 current alias가 아닙니다. 뿌리.ddn을 사용하세요",
        ));
    }
    if has_file(files, &dir, PROJECT_JSON_FILE) {
        return Ok(root_result(
            String::new(),
            Some(join_project_path(&dir, PROJECT_JSON_FILE)),
        ));
    }
    Err(LocalProjectError::with_path(
        "E_PROJECT_ROOT_MISSING",
        explicit,
        "명시한 project 위치에서 뿌리.ddn 또는 ddn.project.json을 찾지 못했습니다",
    ))
}

fn discover_disk_upward(
    start_dir: &Path,
    start_abs: &Path,
) -> Result<ProjectRootDiscoveryResult, LocalProjectError> {
    let dirs = disk_ancestor_dirs(start_dir);
    for dir in &dirs {
        let root = dir.join(PROJECT_ROOT_FILE);
        if root.is_file() {
            if let Some(legacy) = disk_legacy_in_dir(dir) {
                return Err(LocalProjectError::with_path(
                    "E_PROJECT_ROOT_AMBIGUOUS",
                    legacy
                        .file_name()
                        .and_then(|name| name.to_str())
                        .unwrap_or("legacy"),
                    "현재 root 이름과 legacy root 이름이 같은 디렉터리에 있습니다",
                ));
            }
            ensure_no_project_json_entry_conflict_disk(dir)?;
            ensure_no_symlink_escape(start_abs, dir)?;
            return Ok(root_result(PROJECT_ROOT_FILE.to_string(), None));
        }
    }
    for dir in &dirs {
        if let Some(legacy) = disk_legacy_in_dir(dir) {
            return Err(LocalProjectError::with_path(
                "E_LEGACY_PROJECT_ROOT_NAME",
                legacy
                    .file_name()
                    .and_then(|name| name.to_str())
                    .unwrap_or("legacy"),
                "legacy root 파일명은 current alias가 아닙니다. 뿌리.ddn을 사용하세요",
            ));
        }
    }
    for dir in &dirs {
        if dir.join(PROJECT_JSON_FILE).is_file() {
            ensure_no_symlink_escape(start_abs, dir)?;
            return Ok(root_result(
                String::new(),
                Some(PROJECT_JSON_FILE.to_string()),
            ));
        }
    }
    Err(LocalProjectError::new(
        "E_PROJECT_ROOT_MISSING",
        "뿌리.ddn 또는 ddn.project.json을 찾지 못했습니다",
    ))
}

fn discover_disk_project_root_dir(
    start: &Path,
    explicit_project: Option<&Path>,
) -> Result<PathBuf, LocalProjectError> {
    let start_abs = if start.is_absolute() {
        start.to_path_buf()
    } else {
        std::env::current_dir()
            .map_err(|err| LocalProjectError::new("E_PROJECT_CWD", err.to_string()))?
            .join(start)
    };
    if let Some(explicit) = explicit_project {
        let explicit_abs = if explicit.is_absolute() {
            explicit.to_path_buf()
        } else {
            std::env::current_dir()
                .map_err(|err| LocalProjectError::new("E_PROJECT_CWD", err.to_string()))?
                .join(explicit)
        };
        let dir = explicit_root_dir(&explicit_abs)?;
        let _ = discover_disk_explicit_project(&explicit_abs)?;
        ensure_no_symlink_escape(&start_abs, &dir)?;
        return Ok(dir);
    }
    let start_for_walk = if start_abs.is_file() {
        start_abs
            .parent()
            .map(Path::to_path_buf)
            .unwrap_or_else(|| start_abs.clone())
    } else {
        start_abs.clone()
    };
    let dirs = disk_ancestor_dirs(&start_for_walk);
    for dir in &dirs {
        if dir.join(PROJECT_ROOT_FILE).is_file() {
            let _ = discover_disk_upward(dir, &start_abs)?;
            return Ok(dir.clone());
        }
    }
    let _ = discover_disk_upward(&start_for_walk, &start_abs)?;
    Err(LocalProjectError::new(
        "E_PROJECT_ROOT_MISSING",
        "project root directory를 찾지 못했습니다",
    ))
}

fn discover_disk_explicit_project(
    project: &Path,
) -> Result<ProjectRootDiscoveryResult, LocalProjectError> {
    let file_name = project
        .file_name()
        .and_then(|name| name.to_str())
        .unwrap_or("");
    if project.is_file() && file_name == PROJECT_ROOT_FILE {
        let dir = project.parent().unwrap_or(project);
        ensure_no_project_json_entry_conflict_disk(dir)?;
        return Ok(root_result(PROJECT_ROOT_FILE.to_string(), None));
    }
    if project.is_file() && file_name == PROJECT_JSON_FILE {
        return Ok(root_result(
            String::new(),
            Some(PROJECT_JSON_FILE.to_string()),
        ));
    }
    if project.is_file() && LEGACY_ROOT_FILES.contains(&file_name) {
        return Err(LocalProjectError::with_path(
            "E_LEGACY_PROJECT_ROOT_NAME",
            file_name,
            "legacy root 파일명은 current alias가 아닙니다. 뿌리.ddn을 사용하세요",
        ));
    }
    let dir = if project.is_file() {
        project.parent().unwrap_or(project)
    } else {
        project
    };
    if dir.join(PROJECT_ROOT_FILE).is_file() {
        if let Some(legacy) = disk_legacy_in_dir(dir) {
            return Err(LocalProjectError::with_path(
                "E_PROJECT_ROOT_AMBIGUOUS",
                legacy
                    .file_name()
                    .and_then(|name| name.to_str())
                    .unwrap_or("legacy"),
                "현재 root 이름과 legacy root 이름이 같은 디렉터리에 있습니다",
            ));
        }
        ensure_no_project_json_entry_conflict_disk(dir)?;
        return Ok(root_result(PROJECT_ROOT_FILE.to_string(), None));
    }
    if let Some(legacy) = disk_legacy_in_dir(dir) {
        return Err(LocalProjectError::with_path(
            "E_LEGACY_PROJECT_ROOT_NAME",
            legacy
                .file_name()
                .and_then(|name| name.to_str())
                .unwrap_or("legacy"),
            "legacy root 파일명은 current alias가 아닙니다. 뿌리.ddn을 사용하세요",
        ));
    }
    if dir.join(PROJECT_JSON_FILE).is_file() {
        return Ok(root_result(
            String::new(),
            Some(PROJECT_JSON_FILE.to_string()),
        ));
    }
    Err(LocalProjectError::new(
        "E_PROJECT_ROOT_MISSING",
        "명시한 project 위치에서 뿌리.ddn 또는 ddn.project.json을 찾지 못했습니다",
    ))
}

fn explicit_root_dir(project: &Path) -> Result<PathBuf, LocalProjectError> {
    let dir = if project.is_file() {
        project.parent().unwrap_or(project)
    } else {
        project
    };
    Ok(dir.to_path_buf())
}

fn ensure_no_symlink_escape(start: &Path, root_dir: &Path) -> Result<(), LocalProjectError> {
    let Ok(root_real) = fs::canonicalize(root_dir) else {
        return Ok(());
    };
    let start_real = fs::canonicalize(start).unwrap_or_else(|_| start.to_path_buf());
    if !start_real.starts_with(&root_real) {
        return Err(LocalProjectError::new(
            "E_PROJECT_SYMLINK_ESCAPE",
            "project root 밖으로 해소되는 symlink/junction 경로는 사용할 수 없습니다",
        ));
    }
    Ok(())
}

fn disk_ancestor_dirs(start: &Path) -> Vec<PathBuf> {
    let mut dirs = Vec::new();
    let mut current = Some(start);
    while let Some(dir) = current {
        dirs.push(dir.to_path_buf());
        current = dir.parent();
    }
    dirs
}

fn disk_legacy_in_dir(dir: &Path) -> Option<PathBuf> {
    LEGACY_ROOT_FILES
        .iter()
        .map(|name| dir.join(name))
        .find(|path| path.is_file())
}

fn collect_disk_project_files(
    root_dir: &Path,
    current: &Path,
    out: &mut Vec<VirtualProjectFileSource>,
) -> Result<(), LocalProjectError> {
    let mut entries = fs::read_dir(current)
        .map_err(|err| LocalProjectError::new("E_PROJECT_DIR_READ", err.to_string()))?
        .collect::<Result<Vec<_>, _>>()
        .map_err(|err| LocalProjectError::new("E_PROJECT_DIR_READ", err.to_string()))?;
    entries.sort_by_key(|entry| entry.path());
    for entry in entries {
        let path = entry.path();
        let file_type = entry
            .file_type()
            .map_err(|err| LocalProjectError::new("E_PROJECT_FILE_TYPE", err.to_string()))?;
        if file_type.is_dir() {
            if should_skip_project_dir(&path) {
                continue;
            }
            collect_disk_project_files(root_dir, &path, out)?;
            continue;
        }
        if !file_type.is_file() {
            continue;
        }
        let rel_path = path
            .strip_prefix(root_dir)
            .map_err(|_| LocalProjectError::new("E_PROJECT_PATH", "root 밖 파일입니다"))?
            .to_string_lossy()
            .replace('\\', "/");
        let normalized = normalize_project_path(&rel_path)?;
        let utf8_text = fs::read_to_string(&path).map_err(|err| {
            LocalProjectError::with_path(
                "E_PROJECT_FILE_READ",
                normalized.clone(),
                format!("프로젝트 파일을 UTF-8로 읽을 수 없습니다: {err}"),
            )
        })?;
        out.push(VirtualProjectFileSource {
            path: normalized.clone(),
            role: infer_project_file_role(&normalized),
            utf8_text: canonicalize_disk_text(utf8_text),
        });
    }
    Ok(())
}

fn canonicalize_disk_text(text: String) -> String {
    if text.contains("\r\n") {
        text.replace("\r\n", "\n")
    } else {
        text
    }
}

fn should_skip_project_dir(path: &Path) -> bool {
    let Some(name) = path.file_name().and_then(|value| value.to_str()) else {
        return false;
    };
    matches!(
        name,
        ".git" | "target" | "build" | "out" | "dist" | "node_modules" | ".cargo"
    )
}

fn infer_project_file_role(path: &str) -> String {
    if path == PROJECT_ROOT_FILE {
        "root".to_string()
    } else if path == PROJECT_JSON_FILE {
        "project_json".to_string()
    } else if path == "ddn.lock" {
        "lock".to_string()
    } else if path.ends_with("/gaji.toml") {
        "gaji_manifest".to_string()
    } else if path.ends_with(".ddn") {
        "ddn_source".to_string()
    } else {
        "metadata".to_string()
    }
}

fn ensure_no_project_json_entry_conflict_virtual(
    files: &BTreeSet<String>,
    file_texts: Option<&BTreeMap<String, String>>,
    dir: &str,
) -> Result<(), LocalProjectError> {
    if !has_file(files, dir, PROJECT_JSON_FILE) {
        return Ok(());
    }
    let Some(texts) = file_texts else {
        return Ok(());
    };
    let root_path = join_project_path(dir, PROJECT_ROOT_FILE);
    let json_path = join_project_path(dir, PROJECT_JSON_FILE);
    let Some(root_text) = texts.get(&root_path) else {
        return Ok(());
    };
    let Some(json_text) = texts.get(&json_path) else {
        return Ok(());
    };
    ensure_entry_fields_match(root_text, json_text, &json_path)
}

fn ensure_project_json_entry_matches_texts(
    texts: &BTreeMap<String, String>,
    dir: &str,
    root_path: &str,
) -> Result<(), LocalProjectError> {
    let json_path = join_project_path(dir, PROJECT_JSON_FILE);
    let Some(root_text) = texts.get(root_path) else {
        return Ok(());
    };
    let Some(json_text) = texts.get(&json_path) else {
        return Ok(());
    };
    ensure_entry_fields_match(root_text, json_text, &json_path)
}

fn ensure_no_project_json_entry_conflict_disk(dir: &Path) -> Result<(), LocalProjectError> {
    let root_path = dir.join(PROJECT_ROOT_FILE);
    let json_path = dir.join(PROJECT_JSON_FILE);
    if !root_path.is_file() || !json_path.is_file() {
        return Ok(());
    }
    let Ok(root_text) = fs::read_to_string(root_path) else {
        return Ok(());
    };
    let Ok(json_text) = fs::read_to_string(json_path) else {
        return Ok(());
    };
    ensure_entry_fields_match(&root_text, &json_text, PROJECT_JSON_FILE)
}

fn ensure_entry_fields_match(
    root_text: &str,
    json_text: &str,
    json_path: &str,
) -> Result<(), LocalProjectError> {
    let Some(root_entry) = extract_ddn_first_entry(root_text) else {
        return Ok(());
    };
    let Some(json_entry) = extract_project_json_entry(json_text) else {
        return Ok(());
    };
    let root_norm = normalize_project_reference(&root_entry)?;
    let json_norm = normalize_project_reference(&json_entry)?;
    if root_norm != json_norm {
        return Err(LocalProjectError::with_path(
            "E_PROJECT_BLOCK_VS_PROJECTJSON_CONFLICT",
            json_path,
            format!("뿌리.ddn 첫글({root_norm})과 ddn.project.json entry({json_norm})가 다릅니다"),
        ));
    }
    Ok(())
}

fn extract_ddn_first_entry(text: &str) -> Option<String> {
    let key = text.find("첫글")?;
    let after_key = &text[key..];
    let colon = after_key.find(':')?;
    let after_colon = &after_key[colon + 1..];
    extract_first_quoted_string(after_colon)
}

fn extract_project_json_entry(text: &str) -> Option<String> {
    let value: JsonValue = serde_json::from_str(text).ok()?;
    for key in ["entry_path", "entry", "first", "첫글"] {
        if let Some(entry) = value.get(key).and_then(|item| item.as_str()) {
            return Some(entry.to_string());
        }
    }
    value
        .get("targets")
        .and_then(|targets| targets.get("앱"))
        .and_then(|item| item.as_str())
        .map(ToString::to_string)
}

fn extract_first_quoted_string(text: &str) -> Option<String> {
    let start = text.find('"')?;
    let rest = &text[start + 1..];
    let end = rest.find('"')?;
    Some(rest[..end].to_string())
}

fn normalize_project_reference(raw: &str) -> Result<String, LocalProjectError> {
    let trimmed = raw.trim().trim_start_matches("./");
    normalize_project_path(trimmed)
}

fn normalize_project_reference_allow_root(raw: &str) -> Result<String, LocalProjectError> {
    let trimmed = raw.trim();
    if trimmed == "." || trimmed == "./" {
        return Ok(String::new());
    }
    normalize_project_reference(trimmed)
}

fn contains_project_block(text: &str) -> bool {
    Lexer::new(text)
        .tokenize()
        .map(|tokens| {
            tokens
                .windows(2)
                .any(|pair| pair[0].raw == "프로젝트" && matches!(pair[1].kind, TokenKind::LBrace))
        })
        .unwrap_or(false)
}

fn extract_project_block(text: &str) -> Option<&str> {
    let project_pos = text.find("프로젝트")?;
    let open_rel = text[project_pos..].find('{')?;
    let open = project_pos + open_rel;
    let close = find_matching_brace(text, open)?;
    Some(&text[open + 1..close])
}

fn extract_named_block<'a>(text: &'a str, name: &str) -> Option<&'a str> {
    let name_pos = text.find(name)?;
    let open_rel = text[name_pos..].find('{')?;
    let open = name_pos + open_rel;
    let close = find_matching_brace(text, open)?;
    Some(&text[open + 1..close])
}

fn extract_named_block_range(text: &str, name: &str) -> Option<(usize, usize)> {
    let name_pos = text.find(name)?;
    let open_rel = text[name_pos..].find('{')?;
    let open = name_pos + open_rel;
    let close = find_matching_brace(text, open)?;
    Some((open + 1, close))
}

fn find_named_block_key_span(text: &str, block_name: &str, key: &str) -> Option<(usize, usize)> {
    let (start, end) = extract_named_block_range(text, block_name)?;
    let block = &text[start..end];
    for (line_offset, raw_line) in block.split_inclusive('\n').scan(0usize, |offset, line| {
        let current = *offset;
        *offset += line.len();
        Some((current, line))
    }) {
        let trimmed_start = raw_line.len() - raw_line.trim_start().len();
        let line = raw_line.trim().trim_end_matches('.');
        let raw_key = line
            .split_once(':')
            .map(|(raw_key, _)| raw_key)
            .unwrap_or(line);
        let key_start_in_line = trimmed_start + raw_key.find(raw_key.trim()).unwrap_or(0);
        let key_text = raw_key.trim();
        if key_text == key {
            let span_start = start + line_offset + key_start_in_line;
            return Some((span_start, span_start + key_text.len()));
        }
    }
    None
}

fn find_matching_brace(text: &str, open: usize) -> Option<usize> {
    let mut depth = 0usize;
    let mut in_string = false;
    let mut escaped = false;
    for (idx, ch) in text.char_indices().skip_while(|(idx, _)| *idx < open) {
        if in_string {
            if escaped {
                escaped = false;
            } else if ch == '\\' {
                escaped = true;
            } else if ch == '"' {
                in_string = false;
            }
            continue;
        }
        if ch == '"' {
            in_string = true;
            continue;
        }
        if ch == '{' {
            depth += 1;
        } else if ch == '}' {
            depth = depth.checked_sub(1)?;
            if depth == 0 {
                return Some(idx);
            }
        }
    }
    None
}

fn extract_ddn_string_field(block: &str, name: &str) -> Option<String> {
    let name_pos = block.find(name)?;
    let after_name = &block[name_pos + name.len()..];
    let colon = after_name.find(':')?;
    extract_first_quoted_string(&after_name[colon + 1..])
}

fn parse_string_pairs_from_named_block(
    project_block: &str,
    name: &str,
) -> Result<BTreeMap<String, String>, LocalProjectError> {
    let Some(block) = extract_named_block(project_block, name) else {
        return Ok(BTreeMap::new());
    };
    let mut out = BTreeMap::new();
    for raw_line in block.lines() {
        let line = raw_line.trim().trim_end_matches('.');
        if line.is_empty() {
            continue;
        }
        let Some((key, value_part)) = line.split_once(':') else {
            return Err(LocalProjectError::new(
                "E_PROJECT_BLOCK_UNSUPPORTED",
                format!("{name} 블록의 항목은 key: \"value\" 형식이어야 합니다"),
            ));
        };
        let Some(value) = extract_first_quoted_string(value_part) else {
            return Err(LocalProjectError::new(
                "E_PROJECT_BLOCK_UNSUPPORTED",
                format!("{name} 블록의 값은 문자열이어야 합니다"),
            ));
        };
        let key = key.trim().to_string();
        if out.insert(key.clone(), value).is_some() {
            return Err(LocalProjectError::new(
                "E_PROJECT_BLOCK_DUPLICATE_KEY",
                format!("{name} 블록에 중복 키가 있습니다: {key}"),
            ));
        }
    }
    Ok(out)
}

fn parse_string_pair_list_from_named_block(
    project_block: &str,
    name: &str,
) -> Result<Vec<(String, String)>, LocalProjectError> {
    let Some(block) = extract_named_block(project_block, name) else {
        return Ok(Vec::new());
    };
    let mut out = Vec::new();
    for raw_line in block.lines() {
        let line = raw_line.trim().trim_end_matches('.');
        if line.is_empty() {
            continue;
        }
        let Some((key, value_part)) = line.split_once(':') else {
            return Err(LocalProjectError::new(
                "E_PROJECT_BLOCK_UNSUPPORTED",
                format!("{name} 블록의 항목은 key: \"value\" 형식이어야 합니다"),
            ));
        };
        let Some(value) = extract_first_quoted_string(value_part) else {
            return Err(LocalProjectError::new(
                "E_PROJECT_BLOCK_UNSUPPORTED",
                format!("{name} 블록의 값은 문자열이어야 합니다"),
            ));
        };
        let key = key.trim().to_string();
        if key.is_empty() {
            return Err(LocalProjectError::new(
                "E_PROJECT_BLOCK_UNSUPPORTED",
                format!("{name} 블록의 key는 비어 있을 수 없습니다"),
            ));
        }
        out.push((key, value));
    }
    Ok(out)
}

fn load_gaji_manifest_for_path(
    path: &str,
    text_by_path: &BTreeMap<String, String>,
) -> Result<ParsedGajiManifest, LocalProjectError> {
    let id_from_path = gaji_id_from_vendor_path(path)?.to_string();
    let manifest_path = join_project_path(path, "gaji.toml");
    let text = text_by_path.get(&manifest_path).ok_or_else(|| {
        LocalProjectError::with_path(
            "E_GAJI_MANIFEST_MISSING",
            manifest_path.clone(),
            "vendored 가지의 gaji.toml이 없습니다",
        )
    })?;
    let mut manifest = parse_gaji_manifest_text(&manifest_path, text)?;
    if manifest.id != id_from_path {
        return Err(LocalProjectError::with_path(
            "E_GAJI_ID_PATH_MISMATCH",
            manifest_path,
            format!(
                "gaji id({})와 vendor path({id_from_path})가 다릅니다",
                manifest.id
            ),
        ));
    }
    manifest.package_sha256 = gaji_package_sha256(path, text_by_path);
    Ok(manifest)
}

fn collect_gaji_dependencies(
    path: &str,
    text_by_path: &BTreeMap<String, String>,
    manifests: &mut BTreeMap<String, ParsedGajiManifest>,
    stack: &mut Vec<String>,
) -> Result<(), LocalProjectError> {
    let manifest = load_gaji_manifest_for_path(path, text_by_path)?;
    let id = manifest.id.clone();
    if stack.iter().any(|item| item == &id) {
        return Err(LocalProjectError::with_path(
            "E_GAJI_DEP_CYCLE",
            manifest.manifest_path,
            format!("가지 의존성 순환이 있습니다: {}", stack.join(" -> ")),
        ));
    }
    let dependencies = manifest.dependencies.clone();
    manifests.entry(id.clone()).or_insert(manifest);
    stack.push(id.clone());
    for (dep_id, pinned_version) in dependencies {
        if pinned_version.trim().is_empty() || pinned_version == "*" {
            return Err(LocalProjectError::with_path(
                "E_GAJI_DEP_UNPINNED",
                gaji_manifest_path_for_id(&dep_id),
                format!("{id}의 dependency {dep_id}가 exact version pin이 아닙니다"),
            ));
        }
        let dep_path = gaji_vendor_path_for_id(&dep_id);
        let dep_manifest = load_gaji_manifest_for_path(&dep_path, text_by_path).map_err(|err| {
            if err.code == "E_GAJI_MANIFEST_MISSING" {
                LocalProjectError::with_path(
                    "E_GAJI_TRANSITIVE_MISSING",
                    gaji_manifest_path_for_id(&dep_id),
                    format!("{id}가 요구하는 transitive 가지 {dep_id}가 없습니다"),
                )
            } else {
                err
            }
        })?;
        if dep_manifest.version != pinned_version {
            return Err(LocalProjectError::with_path(
                "E_GAJI_VERSION_PIN_MISMATCH",
                dep_manifest.manifest_path.clone(),
                format!(
                    "{id}가 {dep_id}@{pinned_version}을 요구하지만 실제 버전은 {}입니다",
                    dep_manifest.version
                ),
            ));
        }
        collect_gaji_dependencies(&dep_path, text_by_path, manifests, stack)?;
    }
    stack.pop();
    Ok(())
}

fn parse_gaji_manifest_text(
    manifest_path: &str,
    text: &str,
) -> Result<ParsedGajiManifest, LocalProjectError> {
    let mut id = None;
    let mut version = None;
    let mut dependencies = BTreeMap::new();
    let mut in_dependencies = false;
    for raw_line in text.lines() {
        let line = raw_line.split('#').next().unwrap_or("").trim();
        if line.is_empty() {
            continue;
        }
        if line.starts_with('[') && line.ends_with(']') {
            in_dependencies = line == "[dependencies]";
            continue;
        }
        let Some((raw_key, raw_value)) = line.split_once('=') else {
            continue;
        };
        let key = raw_key.trim().trim_matches('"');
        let value = raw_value.trim().trim_end_matches(',').trim();
        if in_dependencies {
            let Some(version_value) = strip_toml_string(value) else {
                return Err(LocalProjectError::with_path(
                    "E_GAJI_DEP_UNPINNED",
                    manifest_path,
                    format!("dependency {key}는 exact string version pin이어야 합니다"),
                ));
            };
            dependencies.insert(key.to_string(), version_value.to_string());
            continue;
        }
        match key {
            "id" => {
                if let Some(value) = strip_toml_string(value) {
                    id = Some(value.to_string());
                }
            }
            "version" => {
                if let Some(value) = strip_toml_string(value) {
                    version = Some(value.to_string());
                }
            }
            "dependencies" => {
                parse_inline_dependency_table(manifest_path, value, &mut dependencies)?;
            }
            _ => {}
        }
    }
    let id = id.ok_or_else(|| {
        LocalProjectError::with_path(
            "E_GAJI_ID_MISSING",
            manifest_path,
            "gaji.toml에 id가 없습니다",
        )
    })?;
    let version = version.ok_or_else(|| {
        LocalProjectError::with_path(
            "E_GAJI_VERSION_MISSING",
            manifest_path,
            "gaji.toml에 version이 없습니다",
        )
    })?;
    Ok(ParsedGajiManifest {
        id,
        version,
        dependencies,
        manifest_path: manifest_path.to_string(),
        manifest_sha256: sha256_hex(text.as_bytes()),
        package_sha256: String::new(),
    })
}

fn parse_inline_dependency_table(
    manifest_path: &str,
    value: &str,
    out: &mut BTreeMap<String, String>,
) -> Result<(), LocalProjectError> {
    let trimmed = value.trim();
    if !(trimmed.starts_with('{') && trimmed.ends_with('}')) {
        return Err(LocalProjectError::with_path(
            "E_GAJI_DEP_UNPINNED",
            manifest_path,
            "dependencies는 { \"id\" = \"version\" } exact pin table이어야 합니다",
        ));
    }
    let inner = &trimmed[1..trimmed.len() - 1];
    for raw_pair in inner.split(',') {
        let pair = raw_pair.trim();
        if pair.is_empty() {
            continue;
        }
        let Some((raw_key, raw_value)) = pair.split_once('=') else {
            return Err(LocalProjectError::with_path(
                "E_GAJI_DEP_UNPINNED",
                manifest_path,
                format!("dependency pin 형식이 아닙니다: {pair}"),
            ));
        };
        let key = raw_key.trim().trim_matches('"');
        let Some(version) = strip_toml_string(raw_value.trim()) else {
            return Err(LocalProjectError::with_path(
                "E_GAJI_DEP_UNPINNED",
                manifest_path,
                format!("dependency {key}가 exact string version pin이 아닙니다"),
            ));
        };
        out.insert(key.to_string(), version.to_string());
    }
    Ok(())
}

fn strip_toml_string(value: &str) -> Option<&str> {
    let trimmed = value.trim();
    if trimmed.starts_with('"') && trimmed.ends_with('"') && trimmed.len() >= 2 {
        Some(&trimmed[1..trimmed.len() - 1])
    } else {
        None
    }
}

fn gaji_id_from_vendor_path(path: &str) -> Result<&str, LocalProjectError> {
    let Some(id) = path.strip_prefix("vendor/") else {
        return Err(LocalProjectError::with_path(
            "E_GAJI_VENDOR_PATH",
            path,
            "local 가지는 vendor/<id> 경로에 있어야 합니다",
        ));
    };
    if id.is_empty() || id.contains('/') {
        return Err(LocalProjectError::with_path(
            "E_GAJI_VENDOR_PATH",
            path,
            "Wave 1 local 가지 id는 vendor/<id> 한 단계로 고정합니다",
        ));
    }
    Ok(id)
}

fn gaji_vendor_path_for_id(id: &str) -> String {
    format!("vendor/{id}")
}

fn gaji_manifest_path_for_id(id: &str) -> String {
    format!("vendor/{id}/gaji.toml")
}

fn gaji_package_sha256(prefix: &str, text_by_path: &BTreeMap<String, String>) -> String {
    let mut input = String::new();
    let package_prefix = format!("{prefix}/");
    for (path, text) in text_by_path {
        if path == &format!("{prefix}/gaji.toml") || path.starts_with(&package_prefix) {
            input.push_str(path);
            input.push('\t');
            input.push_str(&sha256_hex(text.as_bytes()));
            input.push('\n');
        }
    }
    sha256_hex(input.as_bytes())
}

fn parse_imports(text: &str, path: &str) -> Result<Vec<ParsedImport>, LocalProjectError> {
    let pairs = parse_string_pair_list_from_named_block(text, "쓰임")?;
    let mut imports = Vec::new();
    for (alias, source) in pairs {
        if alias.contains('.') || alias.trim().is_empty() {
            return Err(LocalProjectError::with_path(
                "E_IMPORT_ALIAS_INVALID",
                path,
                format!("지원하지 않는 쓰임 alias입니다: {alias}"),
            ));
        }
        imports.push(ParsedImport { alias, source });
    }
    Ok(imports)
}

fn parse_exports(text: &str, path: &str) -> Result<Vec<ParsedExport>, LocalProjectError> {
    let Some(block) =
        extract_named_block(text, "드러냄").or_else(|| extract_named_block(text, "공개"))
    else {
        return Ok(Vec::new());
    };
    let mut exports = Vec::new();
    for raw_line in block.lines() {
        let line = raw_line.trim().trim_end_matches('.');
        if line.is_empty() {
            continue;
        }
        if let Some((external, internal)) = line.split_once(':') {
            let external_name = external.trim().to_string();
            let internal_name = internal.trim().to_string();
            if external_name.is_empty() || internal_name.is_empty() {
                return Err(LocalProjectError::with_path(
                    "E_EXPORT_UNSUPPORTED",
                    path,
                    "드러냄 항목은 이름 또는 외부: 내부 형식이어야 합니다",
                ));
            }
            exports.push(ParsedExport {
                external_name,
                internal_name,
            });
        } else {
            let name = line.trim().to_string();
            if name.is_empty() {
                continue;
            }
            exports.push(ParsedExport {
                external_name: name.clone(),
                internal_name: name,
            });
        }
    }
    Ok(exports)
}

fn collect_alias_show_requests_from_ast(
    text: &str,
    path: &str,
) -> Result<Vec<AliasShowRequest>, LocalProjectError> {
    let stripped = strip_module_metadata_blocks(text)?;
    if stripped.trim().is_empty() {
        return Ok(Vec::new());
    }
    let prepared = runtime_surface::prepare_source_for_execution(&stripped).map_err(|err| {
        LocalProjectError::with_path(
            "E_PROJECT_ENTRY_PARSE",
            path,
            format!("entry DDN 전처리 실패: {err}"),
        )
    })?;
    let program =
        ddonirang_lang::parse_with_mode(&prepared.execution_source, path, ParseMode::Strict)
            .map_err(|err| {
                LocalProjectError::with_path(
                    "E_PROJECT_ENTRY_PARSE",
                    path,
                    format!("entry DDN 파싱 실패: {}", err.message),
                )
            })?;
    let mut requests = Vec::new();
    for item in &program.items {
        let TopLevelItem::SeedDef(seed) = item;
        if let Some(body) = &seed.body {
            collect_alias_show_requests_from_body(body, &mut requests)?;
        }
    }
    for request in collect_alias_show_requests_from_tokens(&stripped)? {
        if !requests
            .iter()
            .any(|existing| existing.alias == request.alias && existing.symbol == request.symbol)
        {
            requests.push(request);
        }
    }
    Ok(requests)
}

fn collect_alias_show_requests_from_tokens(
    text: &str,
) -> Result<Vec<AliasShowRequest>, LocalProjectError> {
    let tokens = Lexer::new(text).tokenize().map_err(|err| {
        LocalProjectError::new(
            "E_PROJECT_ENTRY_PARSE",
            format!("entry DDN 토큰화 실패: {}", err.message),
        )
    })?;
    let mut requests = Vec::new();
    for window in tokens.windows(4) {
        let [left, dot, right, show] = window else {
            continue;
        };
        if !matches!(dot.kind, TokenKind::Dot) || !matches!(show.kind, TokenKind::KwBoyeojugi) {
            continue;
        }
        let Some(alias) = token_name(left) else {
            continue;
        };
        let Some(symbol) = token_name(right) else {
            continue;
        };
        if !is_whitespace_only(text, left.span.end, dot.span.start)
            || !is_whitespace_only(text, dot.span.end, right.span.start)
            || !is_whitespace_only(text, right.span.end, show.span.start)
            || text[left.span.end..show.span.start].contains('\n')
        {
            continue;
        }
        requests.push(AliasShowRequest {
            alias: alias.to_string(),
            symbol: symbol.to_string(),
        });
    }
    Ok(requests)
}

fn collect_alias_show_requests_from_body(
    body: &Body,
    requests: &mut Vec<AliasShowRequest>,
) -> Result<(), LocalProjectError> {
    for stmt in &body.stmts {
        match stmt {
            Stmt::Show { expr, .. } => {
                if let Some(request) = alias_show_request_from_expr(expr)? {
                    requests.push(request);
                }
            }
            Stmt::Receive { body, .. }
            | Stmt::Try { body, .. }
            | Stmt::Repeat { body, .. }
            | Stmt::While { body, .. }
            | Stmt::ForEach { body, .. }
            | Stmt::Quantifier { body, .. }
            | Stmt::Guard { body, .. }
            | Stmt::BeatBlock { body, .. }
            | Stmt::Hook { body, .. }
            | Stmt::HookWhenBecomes { body, .. }
            | Stmt::HookWhile { body, .. } => {
                collect_alias_show_requests_from_body(body, requests)?;
            }
            Stmt::If {
                then_body,
                else_body,
                ..
            } => {
                collect_alias_show_requests_from_body(then_body, requests)?;
                if let Some(else_body) = else_body {
                    collect_alias_show_requests_from_body(else_body, requests)?;
                }
            }
            Stmt::Choose {
                branches,
                else_body,
                ..
            } => {
                for branch in branches {
                    collect_alias_show_requests_from_body(&branch.body, requests)?;
                }
                collect_alias_show_requests_from_body(else_body, requests)?;
            }
            Stmt::Contract {
                then_body,
                else_body,
                ..
            } => {
                if let Some(then_body) = then_body {
                    collect_alias_show_requests_from_body(then_body, requests)?;
                }
                collect_alias_show_requests_from_body(else_body, requests)?;
            }
            Stmt::DeclBlock { .. }
            | Stmt::Mutate { .. }
            | Stmt::Expr { .. }
            | Stmt::Send { .. }
            | Stmt::Inspect { .. }
            | Stmt::MetaBlock { .. }
            | Stmt::Pragma { .. }
            | Stmt::Return { .. }
            | Stmt::Break { .. }
            | Stmt::ContinueLoop { .. } => {}
        }
    }
    Ok(())
}

fn alias_show_request_from_expr(
    expr: &Expr,
) -> Result<Option<AliasShowRequest>, LocalProjectError> {
    let ExprKind::FieldAccess { target, field } = &expr.kind else {
        return Ok(None);
    };
    match &target.kind {
        ExprKind::Var(alias) => Ok(Some(AliasShowRequest {
            alias: alias.clone(),
            symbol: field.clone(),
        })),
        ExprKind::FieldAccess { .. } => Err(LocalProjectError::new(
            "E_PROJECT_SYMBOL_UNSUPPORTED",
            "중첩 alias-qualified 보여주기 대상은 Wave 1에서 지원하지 않습니다",
        )),
        _ => Ok(None),
    }
}

fn has_top_level_show_effect(text: &str) -> bool {
    text.lines()
        .map(str::trim)
        .any(|line| line.trim_end_matches('.').ends_with("보여주기"))
}

fn collect_module_info(
    path: &str,
    entry_path: &str,
    text_by_path: &BTreeMap<String, String>,
    modules: &mut BTreeMap<String, ModuleInfo>,
    stack: &mut Vec<String>,
) -> Result<(), LocalProjectError> {
    if modules.contains_key(path) {
        return Ok(());
    }
    if stack.iter().any(|item| item == path) {
        return Err(LocalProjectError::with_path(
            "E_IMPORT_CYCLE",
            path,
            format!("모듈 순환이 있습니다: {}", stack.join(" -> ")),
        ));
    }
    let text = text_by_path.get(path).ok_or_else(|| {
        LocalProjectError::with_path("E_MODULE_MISSING", path, "모듈 파일이 없습니다")
    })?;
    if path != entry_path && has_top_level_show_effect(text) {
        return Err(LocalProjectError::with_path(
            "E_IMPORTED_TOP_LEVEL_EFFECT_UNSUPPORTED",
            path,
            "imported module의 top-level 보여주기 효과는 Wave 1에서 지원하지 않습니다",
        ));
    }
    stack.push(path.to_string());
    let parsed_imports = parse_imports(text, path)?;
    let mut seen_aliases = BTreeSet::new();
    let mut imports = Vec::new();
    for import in parsed_imports {
        if !seen_aliases.insert(import.alias.clone()) {
            let message = format!("중복 쓰임 alias입니다: {}", import.alias);
            return Err(find_named_block_key_span(text, "쓰임", &import.alias)
                .map(|span| {
                    LocalProjectError::with_path_span(
                        "E_IMPORT_ALIAS_DUPLICATE",
                        path,
                        message.clone(),
                        span,
                    )
                })
                .unwrap_or_else(|| {
                    LocalProjectError::with_path("E_IMPORT_ALIAS_DUPLICATE", path, message)
                }));
        }
        let resolved_path = resolve_import_source_path(path, &import.source)?;
        if !text_by_path.contains_key(&resolved_path) {
            return Err(LocalProjectError::with_path(
                "E_MODULE_MISSING",
                resolved_path,
                format!("쓰임 alias {}의 모듈을 찾을 수 없습니다", import.alias),
            ));
        }
        imports.push(ResolvedImport {
            importer_path: path.to_string(),
            alias: import.alias,
            source: import.source,
            resolved_path,
        });
    }
    imports.sort_by(|a, b| {
        a.alias
            .cmp(&b.alias)
            .then(a.resolved_path.cmp(&b.resolved_path))
    });
    let mut exports = BTreeMap::new();
    for export in parse_exports(text, path)? {
        if exports
            .insert(export.external_name.clone(), export.internal_name.clone())
            .is_some()
        {
            let message = format!("중복 드러냄 이름입니다: {}", export.external_name);
            return Err(
                find_named_block_key_span(text, "드러냄", &export.external_name)
                    .or_else(|| find_named_block_key_span(text, "공개", &export.external_name))
                    .map(|span| {
                        LocalProjectError::with_path_span(
                            "E_EXPORT_DUPLICATE",
                            path,
                            message.clone(),
                            span,
                        )
                    })
                    .unwrap_or_else(|| {
                        LocalProjectError::with_path("E_EXPORT_DUPLICATE", path, message)
                    }),
            );
        }
    }
    modules.insert(
        path.to_string(),
        ModuleInfo {
            path: path.to_string(),
            imports: imports.clone(),
            exports,
        },
    );
    for import in imports {
        collect_module_info(
            &import.resolved_path,
            entry_path,
            text_by_path,
            modules,
            stack,
        )?;
    }
    stack.pop();
    Ok(())
}

fn resolve_exported_symbol(
    modules: &BTreeMap<String, ModuleInfo>,
    module_path: &str,
    external_name: &str,
    stack: &mut Vec<String>,
) -> Result<SymbolValue, LocalProjectError> {
    let key = format!("{module_path}::{external_name}");
    if stack.iter().any(|item| item == &key) {
        return Err(LocalProjectError::with_path(
            "E_IMPORT_CYCLE",
            module_path,
            format!("re-export 순환이 있습니다: {}", stack.join(" -> ")),
        ));
    }
    stack.push(key);
    let module = modules.get(module_path).ok_or_else(|| {
        LocalProjectError::with_path("E_MODULE_MISSING", module_path, "모듈을 찾지 못했습니다")
    })?;
    let internal = module.exports.get(external_name).ok_or_else(|| {
        LocalProjectError::with_path(
            "E_SYMBOL_NOT_EXPORTED",
            module_path,
            format!("{external_name}는 드러냄 목록에 없습니다"),
        )
    })?;
    let result = if let Some((alias, symbol)) = split_alias_symbol(internal) {
        let import = module
            .imports
            .iter()
            .find(|item| item.alias == alias)
            .ok_or_else(|| {
                LocalProjectError::with_path(
                    "E_ALIAS_UNKNOWN",
                    module_path,
                    format!("re-export 내부 alias를 찾지 못했습니다: {alias}"),
                )
            })?;
        resolve_exported_symbol(modules, &import.resolved_path, symbol, stack)?
    } else {
        if !is_supported_internal_symbol_name(internal) {
            return Err(LocalProjectError::with_path(
                "E_SYMBOL_NOT_FOUND",
                module_path,
                format!("내부 심볼 {internal}를 Wave 1 linked 실행으로 확인할 수 없습니다"),
            ));
        }
        SymbolValue {
            module_path: module_path.to_string(),
            internal_name: internal.clone(),
        }
    };
    stack.pop();
    Ok(result)
}

fn is_supported_internal_symbol_name(name: &str) -> bool {
    let trimmed = name.trim();
    !trimmed.is_empty()
        && trimmed == name
        && !trimmed.contains('.')
        && trimmed.chars().all(is_identifier_char)
}

fn split_alias_symbol(text: &str) -> Option<(&str, &str)> {
    let (alias, symbol) = text.split_once('.')?;
    if alias.is_empty() || symbol.is_empty() || symbol.contains('.') {
        return None;
    }
    Some((alias, symbol))
}

fn resolve_import_source_path(
    importer_path: &str,
    source: &str,
) -> Result<String, LocalProjectError> {
    let normalized_ref = normalize_project_reference(source)?;
    let _ = importer_path;
    if normalized_ref.ends_with(".ddn") {
        Ok(normalized_ref)
    } else {
        Ok(format!("{normalized_ref}.ddn"))
    }
}

fn virtual_parent_dirs(files: &BTreeSet<String>, start_path: &str) -> Vec<String> {
    let mut start_dir = if files.contains(start_path) {
        parent_dir(start_path)
    } else {
        start_path.to_string()
    };
    let prefix = format!("{start_path}/");
    if files.iter().any(|path| path.starts_with(&prefix)) {
        start_dir = start_path.to_string();
    }
    let mut dirs = Vec::new();
    let mut current = start_dir;
    loop {
        dirs.push(current.clone());
        if current.is_empty() {
            break;
        }
        current = parent_dir(&current);
    }
    dirs
}

fn root_result(
    root_marker_path: String,
    project_json_path: Option<String>,
) -> ProjectRootDiscoveryResult {
    let used_fallback = root_marker_path.is_empty() && project_json_path.is_some();
    ProjectRootDiscoveryResult {
        schema: PROJECT_ROOT_DISCOVERY_SCHEMA,
        root_kind: if used_fallback {
            "project_json_fallback"
        } else {
            "root_ddn"
        },
        root_marker_path: if root_marker_path.is_empty() {
            None
        } else {
            Some(root_marker_path)
        },
        project_json_path,
        used_fallback,
        diagnostics: Vec::new(),
    }
}

fn has_file(files: &BTreeSet<String>, dir: &str, name: &str) -> bool {
    files.contains(&join_project_path(dir, name))
}

fn legacy_in_dir<'a>(files: &BTreeSet<String>, dir: &str) -> Option<&'a str> {
    for legacy in LEGACY_ROOT_FILES {
        if files.contains(&join_project_path(dir, legacy)) {
            return Some(*legacy);
        }
    }
    None
}

fn join_project_path(dir: &str, name: &str) -> String {
    if dir.is_empty() {
        name.to_string()
    } else {
        format!("{dir}/{name}")
    }
}

fn parent_dir(path: &str) -> String {
    path.rsplit_once('/')
        .map(|(parent, _)| parent.to_string())
        .unwrap_or_default()
}

fn path_file_name(path: &str) -> Option<&str> {
    path.rsplit('/').next()
}

fn graph_hash_input(root_path: &str, entry_path: &str, files: &[PendingFile]) -> String {
    let mut input = String::new();
    input.push_str("ddn.local_project.graph_hash.v1\n");
    input.push_str("root=");
    input.push_str(root_path);
    input.push('\n');
    input.push_str("entry=");
    input.push_str(entry_path);
    input.push('\n');
    for file in files {
        input.push_str(&file.path);
        input.push('\t');
        input.push_str(&file.role);
        input.push('\t');
        input.push_str(&file.sha256);
        input.push('\n');
    }
    input
}

fn sha256_hex(bytes: &[u8]) -> String {
    let mut hasher = Sha256::new();
    hasher.update(bytes);
    format!("{:x}", hasher.finalize())
}

fn to_canonical_json_line<T: Serialize>(value: &T) -> String {
    let mut text = serde_json::to_string(value).expect("manifest serialization must succeed");
    text.push('\n');
    text
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn canonicalizes_disk_crlf_without_changing_lf_or_lone_cr() {
        assert_eq!(canonicalize_disk_text("a\r\nb\r\n".to_string()), "a\nb\n");
        assert_eq!(canonicalize_disk_text("a\nb\n".to_string()), "a\nb\n");
        assert_eq!(canonicalize_disk_text("a\rb\n".to_string()), "a\rb\n");
    }

    fn sample_source() -> VirtualProjectSource {
        VirtualProjectSource {
            schema: VIRTUAL_PROJECT_SOURCE_SCHEMA.to_string(),
            kind: Some(LOCAL_PROJECT_TREE_KIND.to_string()),
            root_path: "뿌리.ddn".to_string(),
            entry_path: "app/main.ddn".to_string(),
            files: vec![
                VirtualProjectFileSource {
                    path: "app/main.ddn".to_string(),
                    role: "ddn_source".to_string(),
                    utf8_text: "\"안녕\" 보여주기.".to_string(),
                },
                VirtualProjectFileSource {
                    path: "뿌리.ddn".to_string(),
                    role: "root".to_string(),
                    utf8_text: "프로젝트 { 이름: \"샘\". }.".to_string(),
                },
            ],
        }
    }

    fn sample_multifile_source() -> VirtualProjectSource {
        VirtualProjectSource {
            schema: VIRTUAL_PROJECT_SOURCE_SCHEMA.to_string(),
            kind: Some(LOCAL_PROJECT_TREE_KIND.to_string()),
            root_path: "뿌리.ddn".to_string(),
            entry_path: "app/main.ddn".to_string(),
            files: vec![
                VirtualProjectFileSource {
                    path: "뿌리.ddn".to_string(),
                    role: "root".to_string(),
                    utf8_text: "프로젝트 { 이름: \"샘\". 첫글: \"./app/main.ddn\". 목표 { 앱: \"./app/main.ddn\". } 모듈길 { 로컬: \"./lib\". } }.".to_string(),
                },
                VirtualProjectFileSource {
                    path: "app/main.ddn".to_string(),
                    role: "ddn_source".to_string(),
                    utf8_text: "쓰임 { 운동: \"./lib/운동\". }\n운동.속도 보여주기.".to_string(),
                },
                VirtualProjectFileSource {
                    path: "lib/운동.ddn".to_string(),
                    role: "ddn_source".to_string(),
                    utf8_text: "드러냄 { 속도. }\n속도 <- 7.".to_string(),
                },
            ],
        }
    }

    #[test]
    fn normalizes_paths_and_hashes_deterministically() {
        let first = normalize_virtual_project_source(sample_source()).expect("normalize");
        let second = normalize_virtual_project_source(sample_source()).expect("normalize");
        assert_eq!(
            first.canonical_manifest_sha256,
            second.canonical_manifest_sha256
        );
        assert_eq!(first.files[0].path, "app/main.ddn");
    }

    #[test]
    fn prepare_link_returns_linked_source_without_runtime_summary() {
        let prepared = build_project_prepare_link(sample_multifile_source(), "앱", true, true)
            .expect("prepare/link");
        assert_eq!(prepared.schema, "ddn.local_project.prepare_link.v1");
        assert_eq!(prepared.frontdoor, "wasm_project_prepare_link_json");
        assert_eq!(prepared.target_path, "app/main.ddn");
        assert!(prepared.linked_execution_source.contains("속도 <- 7."));
        assert!(prepared.linked_execution_source.contains("속도 보여주기."));
        assert!(!prepared.linked_execution_source_sha256.is_empty());
        assert!(prepared.symbol_boundary.output_rows.is_empty());
        assert!(prepared.state_hash_formula_change == false);
        assert!(!prepared.prepare_link_sha256.is_empty());
        assert_eq!(
            prepared.runtime_execution_envelope["execution_mode_decision"]["mode"],
            "oneshot"
        );
        assert_eq!(
            prepared.runtime_execution_envelope["execution_mode_decision"]["authority"],
            "parsed_program"
        );
    }

    #[test]
    fn linked_multifile_tick_hook_uses_parsed_live_execution_mode() {
        let mut source = sample_multifile_source();
        let entry = source
            .files
            .iter_mut()
            .find(|file| file.path == "app/main.ddn")
            .expect("entry file");
        entry.utf8_text =
            "쓰임 { 운동: \"./lib/운동\". }\n(매마디)마다 {\n  운동.속도 보여주기.\n}.".to_string();
        let prepared = build_project_prepare_link(source, "앱", true, true).expect("prepare/link");
        assert_eq!(
            prepared.runtime_execution_envelope["execution_mode_decision"]["mode"],
            "live"
        );
        assert_eq!(
            prepared.runtime_execution_envelope["execution_mode_decision"]["live_hook_count"],
            1
        );
    }

    #[test]
    fn rename_edit_plan_updates_only_structural_references() {
        let mut source = sample_multifile_source();
        let main = source
            .files
            .iter_mut()
            .find(|file| file.path == "app/main.ddn")
            .unwrap();
        main.utf8_text =
            "쓰임 { 운동: \"./lib/운동\". }\n\"./lib/운동\" 보여주기.\n# ./lib/운동은 설명 문자열"
                .to_string();
        let before_hash = virtual_project_source_sha256(&source).expect("hash");
        let plan = build_project_edit_plan(ProjectEditPlanRequest {
            schema: PROJECT_EDIT_PLAN_SCHEMA.to_string(),
            source,
            operation: ProjectEditOperation::RenameFile {
                from_path: "lib/운동.ddn".to_string(),
                to_path: "lib/힘.ddn".to_string(),
            },
            expected_source_sha256: before_hash.clone(),
        })
        .expect("rename plan");
        assert_eq!(plan.before_source_sha256, before_hash);
        assert!(plan.atomic_apply);
        assert!(plan.lock_stale);
        assert!(plan
            .project_source
            .files
            .iter()
            .any(|file| file.path == "lib/힘.ddn"));
        let main = plan
            .project_source
            .files
            .iter()
            .find(|file| file.path == "app/main.ddn")
            .unwrap();
        assert!(main.utf8_text.contains("쓰임 { 운동: \"./lib/힘\". }"));
        assert!(main.utf8_text.contains("\"./lib/운동\" 보여주기."));
        assert!(main.utf8_text.contains("# ./lib/운동은 설명 문자열"));
        let root = plan
            .project_source
            .files
            .iter()
            .find(|file| file.path == PROJECT_ROOT_FILE)
            .unwrap();
        assert!(root.utf8_text.contains("모듈길 { 로컬: \"./lib\". }"));
    }

    #[test]
    fn rename_edit_plan_rejects_stale_hash_without_change() {
        let source = sample_multifile_source();
        let original = serde_json::to_string(&source).unwrap();
        let error = build_project_edit_plan(ProjectEditPlanRequest {
            schema: PROJECT_EDIT_PLAN_SCHEMA.to_string(),
            source: source.clone(),
            operation: ProjectEditOperation::RenameFile {
                from_path: "lib/운동.ddn".to_string(),
                to_path: "lib/힘.ddn".to_string(),
            },
            expected_source_sha256: "stale".to_string(),
        })
        .unwrap_err();
        assert_eq!(error.code, "E_PROJECT_EDIT_SOURCE_CONFLICT");
        assert_eq!(serde_json::to_string(&source).unwrap(), original);
    }

    #[test]
    fn rename_edit_plan_rejects_root_and_duplicate_target() {
        let source = sample_multifile_source();
        let hash = virtual_project_source_sha256(&source).unwrap();
        let root_error = build_project_edit_plan(ProjectEditPlanRequest {
            schema: PROJECT_EDIT_PLAN_SCHEMA.to_string(),
            source: source.clone(),
            operation: ProjectEditOperation::RenameFile {
                from_path: PROJECT_ROOT_FILE.to_string(),
                to_path: "root.ddn".to_string(),
            },
            expected_source_sha256: hash.clone(),
        })
        .unwrap_err();
        assert_eq!(root_error.code, "E_PROJECT_ROOT_RENAME_FORBIDDEN");
        let duplicate_error = build_project_edit_plan(ProjectEditPlanRequest {
            schema: PROJECT_EDIT_PLAN_SCHEMA.to_string(),
            source,
            operation: ProjectEditOperation::RenameFile {
                from_path: "lib/운동.ddn".to_string(),
                to_path: "app/main.ddn".to_string(),
            },
            expected_source_sha256: hash,
        })
        .unwrap_err();
        assert_eq!(duplicate_error.code, "E_PROJECT_PATH_DUPLICATE");
    }

    fn edit_request(
        source: VirtualProjectSource,
        operation: ProjectEditOperation,
    ) -> ProjectEditPlanRequest {
        let expected_source_sha256 = virtual_project_source_sha256(&source).unwrap();
        ProjectEditPlanRequest {
            schema: PROJECT_EDIT_PLAN_SCHEMA.to_string(),
            source,
            operation,
            expected_source_sha256,
        }
    }

    #[test]
    fn structural_edit_plan_supports_add_module_duplicate_and_set_entry() {
        let source = sample_multifile_source();
        let added = build_project_edit_plan(edit_request(
            source,
            ProjectEditOperation::AddModule {
                path: "lib/힘.ddn".to_string(),
                module_name: "힘".to_string(),
            },
        ))
        .expect("add module");
        assert_eq!(added.operation, "add_module");
        assert!(added.project_source.files.iter().any(|file| {
            file.path == "lib/힘.ddn" && file.utf8_text.contains("드러냄 { 값. }")
        }));

        let duplicated = build_project_edit_plan(edit_request(
            added.project_source,
            ProjectEditOperation::DuplicateFile {
                from_path: "lib/힘.ddn".to_string(),
                to_path: "lib/힘_복사.ddn".to_string(),
            },
        ))
        .expect("duplicate");
        assert_eq!(duplicated.operation, "duplicate_file");
        assert!(duplicated
            .project_source
            .files
            .iter()
            .any(|file| file.path == "lib/힘_복사.ddn"));

        let entry = build_project_edit_plan(edit_request(
            duplicated.project_source,
            ProjectEditOperation::SetEntry {
                path: "lib/힘_복사.ddn".to_string(),
            },
        ))
        .expect("set entry");
        assert_eq!(entry.project_source.entry_path, "lib/힘_복사.ddn");
        let root = entry
            .project_source
            .files
            .iter()
            .find(|file| file.path == PROJECT_ROOT_FILE)
            .unwrap();
        assert!(root.utf8_text.contains("첫글: \"./lib/힘_복사.ddn\""));
        assert!(root.utf8_text.contains("앱: \"./lib/힘_복사.ddn\""));
    }

    #[test]
    fn delete_edit_plan_rejects_referenced_module_without_mutation() {
        let source = sample_multifile_source();
        let original = serde_json::to_string(&source).unwrap();
        let error = build_project_edit_plan(edit_request(
            source.clone(),
            ProjectEditOperation::DeleteFile {
                path: "lib/운동.ddn".to_string(),
            },
        ))
        .unwrap_err();
        assert_eq!(error.code, "E_PROJECT_FILE_REFERENCED");
        assert_eq!(serde_json::to_string(&source).unwrap(), original);
    }

    #[test]
    fn delete_edit_plan_removes_unreferenced_file_atomically() {
        let mut source = sample_multifile_source();
        source.files.push(VirtualProjectFileSource {
            path: "lib/안씀.ddn".to_string(),
            role: "ddn_source".to_string(),
            utf8_text: "드러냄 { 값. }\n값 <- 1.".to_string(),
        });
        let plan = build_project_edit_plan(edit_request(
            source,
            ProjectEditOperation::DeleteFile {
                path: "lib/안씀.ddn".to_string(),
            },
        ))
        .expect("delete");
        assert!(plan.atomic_apply);
        assert!(!plan
            .project_source
            .files
            .iter()
            .any(|file| file.path == "lib/안씀.ddn"));
    }

    #[test]
    fn alias_show_token_fallback_does_not_cross_statement_line() {
        let requests = collect_alias_show_requests_from_tokens(
            "속도 <- 속도 - 9.8 * dt.\n위치 보여주기.\n힘.중력가속도 보여주기.",
        )
        .expect("token requests");
        assert_eq!(requests.len(), 1);
        assert_eq!(requests[0].alias, "힘");
        assert_eq!(requests[0].symbol, "중력가속도");
    }

    fn extraction_request(source: VirtualProjectSource) -> GajiExtractionPlanRequest {
        GajiExtractionPlanRequest {
            schema: GAJI_EXTRACTION_PLAN_SCHEMA.to_string(),
            source,
            selected_modules: vec!["lib/운동.ddn".to_string()],
            gaji_id: "운동".to_string(),
            version: "1.0.0".to_string(),
            description: "운동 helper".to_string(),
            tags: vec!["물리".to_string()],
            profile: "내".to_string(),
            origin_project_ref: Some("project:test".to_string()),
            origin_gaji: None,
            relation: "extracted".to_string(),
        }
    }

    #[test]
    fn gaji_extraction_plan_uses_structural_exports_and_dependency_closure() {
        let mut source = sample_multifile_source();
        source.files.iter_mut().find(|file| file.path == "lib/운동.ddn").unwrap().utf8_text =
            "쓰임 { 수치: \"./lib/수치\". }\n드러냄 { 속도. }\n# 드러냄 { 가짜. }\n설명 <- \"드러냄 { 문자열가짜. }\".\n속도 <- 수치.기본값.".to_string();
        source.files.push(VirtualProjectFileSource {
            path: "lib/수치.ddn".to_string(),
            role: "ddn_source".to_string(),
            utf8_text: "드러냄 { 기본값. }\n기본값 <- 7.".to_string(),
        });
        let first = build_gaji_extraction_plan(extraction_request(source.clone())).expect("plan");
        let second = build_gaji_extraction_plan(extraction_request(source)).expect("plan repeat");
        assert_eq!(first.included_modules, vec!["lib/수치.ddn", "lib/운동.ddn"]);
        assert_eq!(first.public_symbols.len(), 2);
        assert!(!first
            .public_symbols
            .iter()
            .any(|item| item.external_name.contains("가짜")));
        assert_eq!(first.content_sha256, second.content_sha256);
        assert!(first.publishable);
    }

    #[test]
    fn gaji_extraction_plan_rejects_private_only_module() {
        let mut source = sample_multifile_source();
        source
            .files
            .iter_mut()
            .find(|file| file.path == "lib/운동.ddn")
            .unwrap()
            .utf8_text = "비공개값 <- 7.".to_string();
        let error = build_gaji_extraction_plan(extraction_request(source)).unwrap_err();
        assert_eq!(error.code, "E_GAJI_PUBLIC_API_EMPTY");
    }

    #[test]
    fn local_gaji_artifact_is_deterministic_and_rejects_tamper() {
        let first = build_local_gaji_artifact(extraction_request(sample_multifile_source()))
            .expect("artifact");
        let second = build_local_gaji_artifact(extraction_request(sample_multifile_source()))
            .expect("artifact repeat");
        assert_eq!(first.package_sha256, second.package_sha256);
        assert_eq!(first.manifest_path, "gaji.toml");
        assert!(first
            .files
            .iter()
            .any(|file| file.path == "ddn/lib/운동.ddn"));
        let mut tampered = first;
        let source = tampered
            .files
            .iter_mut()
            .find(|file| file.path.starts_with("ddn/"))
            .unwrap();
        source.utf8_text.push_str("\n변조 <- 1.");
        assert_eq!(
            verify_local_gaji_artifact(&tampered).unwrap_err().code,
            "E_GAJI_ARTIFACT_FILE_HASH"
        );
    }

    #[test]
    fn local_gaji_remix_preserves_origin_and_requires_explicit_lineage() {
        let original =
            build_local_gaji_artifact(extraction_request(sample_multifile_source())).unwrap();
        let mut remix_request = extraction_request(sample_multifile_source());
        remix_request.gaji_id = "운동-내버전".to_string();
        remix_request.origin_gaji = Some(format!("{}@{}", original.gaji_id, original.version));
        remix_request.relation = "remix".to_string();
        let remix = build_local_gaji_artifact(remix_request).unwrap();
        assert_eq!(remix.provenance.origin_gaji.as_deref(), Some("운동@1.0.0"));
        assert_eq!(remix.provenance.relation, "remix");
        assert_eq!(original.provenance.origin_gaji, None);
        let mut missing = extraction_request(sample_multifile_source());
        missing.relation = "remix".to_string();
        assert_eq!(
            build_local_gaji_artifact(missing).unwrap_err().code,
            "E_GAJI_REMIX_ORIGIN_REQUIRED"
        );
    }

    #[test]
    fn local_gaji_artifact_enforces_path_hash_and_size_bounds() {
        let base =
            build_local_gaji_artifact(extraction_request(sample_multifile_source())).unwrap();
        let mut manifest_mismatch = base.clone();
        manifest_mismatch.content_sha256 = "0".repeat(64);
        assert_eq!(
            verify_local_gaji_artifact(&manifest_mismatch)
                .unwrap_err()
                .code,
            "E_GAJI_MANIFEST_CONTENT_HASH"
        );

        let mut case_duplicate = base.clone();
        let mut duplicate = case_duplicate
            .files
            .iter()
            .find(|file| file.path.starts_with("ddn/"))
            .unwrap()
            .clone();
        duplicate.path = duplicate.path.to_uppercase();
        case_duplicate.files.push(duplicate);
        case_duplicate.package_sha256 = local_gaji_artifact_package_hash(&case_duplicate.files);
        assert_eq!(
            verify_local_gaji_artifact(&case_duplicate)
                .unwrap_err()
                .code,
            "E_GAJI_ARTIFACT_PATH_DUPLICATE"
        );

        let mut oversized = base.clone();
        oversized.files.push(local_gaji_artifact_file(
            "ddn/lib/큰파일.ddn",
            "가".repeat(GAJI_ARTIFACT_MAX_SINGLE_FILE_BYTES),
        ));
        oversized.package_sha256 = local_gaji_artifact_package_hash(&oversized.files);
        assert_eq!(
            verify_local_gaji_artifact(&oversized).unwrap_err().code,
            "E_GAJI_ARTIFACT_FILE_BOUND"
        );

        let mut too_many = base;
        while too_many.files.len() <= GAJI_ARTIFACT_MAX_FILES {
            let index = too_many.files.len();
            too_many.files.push(local_gaji_artifact_file(
                &format!("ddn/lib/파일{index}.ddn"),
                "값 <- 1.".to_string(),
            ));
        }
        too_many.package_sha256 = local_gaji_artifact_package_hash(&too_many.files);
        assert_eq!(
            verify_local_gaji_artifact(&too_many).unwrap_err().code,
            "E_GAJI_ARTIFACT_FILE_COUNT_BOUND"
        );
    }

    #[test]
    fn local_gotgan_publish_is_immutable_and_searches_public_metadata() {
        let artifact = build_local_gaji_artifact(extraction_request(sample_multifile_source()))
            .expect("artifact");
        let empty = LocalGotganStore {
            schema: LOCAL_GOTGAN_STORE_SCHEMA.to_string(),
            artifacts: Vec::new(),
        };
        let store = publish_local_gotgan(empty, artifact.clone()).expect("publish");
        let repeated =
            publish_local_gotgan(store.clone(), artifact.clone()).expect("idempotent same bytes");
        assert_eq!(repeated.artifacts.len(), 1);
        let rows = search_local_gotgan(&store, "속도", &["내".to_string()]).expect("search");
        assert_eq!(rows.len(), 1);
        assert_eq!(rows[0].gaji_id, "운동");
        let mut conflicting = artifact;
        let file = conflicting
            .files
            .iter_mut()
            .find(|file| file.path.starts_with("ddn/"))
            .unwrap();
        file.utf8_text.push_str("\n다른값 <- 1.");
        file.byte_length = file.utf8_text.len();
        file.sha256 = sha256_hex(file.utf8_text.as_bytes());
        conflicting.package_sha256 = local_gaji_artifact_package_hash(&conflicting.files);
        assert_eq!(
            publish_local_gotgan(store, conflicting).unwrap_err().code,
            "E_GOTGAN_VERSION_IMMUTABLE"
        );
    }

    #[test]
    fn local_gotgan_search_orders_one_hundred_artifacts_deterministically() {
        let mut store = LocalGotganStore {
            schema: LOCAL_GOTGAN_STORE_SCHEMA.to_string(),
            artifacts: Vec::new(),
        };
        for index in (0..105).rev() {
            let mut request = extraction_request(sample_multifile_source());
            request.gaji_id = format!("도구-{index:03}");
            request.description = "결정적 검색 도구".to_string();
            store =
                publish_local_gotgan(store, build_local_gaji_artifact(request).unwrap()).unwrap();
        }
        let first = search_local_gotgan(&store, "검색", &["내".to_string()]).unwrap();
        let second = search_local_gotgan(&store, "검색", &["내".to_string()]).unwrap();
        assert_eq!(first.len(), 105);
        assert_eq!(
            serde_json::to_string(&first).unwrap(),
            serde_json::to_string(&second).unwrap()
        );
        assert_eq!(first.first().unwrap().gaji_id, "도구-000");
        assert_eq!(first.last().unwrap().gaji_id, "도구-104");
    }

    fn lifecycle_request(
        source: VirtualProjectSource,
        operation: GajiLifecycleOperation,
    ) -> GajiLifecyclePlanRequest {
        GajiLifecyclePlanRequest {
            schema: GAJI_LIFECYCLE_PLAN_SCHEMA.to_string(),
            expected_source_sha256: virtual_project_source_sha256(&source).unwrap(),
            expected_lock_sha256: None,
            source,
            operation,
        }
    }

    #[test]
    fn gaji_lifecycle_installs_with_lock_and_removes_unused_atomically() {
        let artifact =
            build_local_gaji_artifact(extraction_request(sample_multifile_source())).unwrap();
        let installed = build_gaji_lifecycle_plan(lifecycle_request(
            sample_multifile_source(),
            GajiLifecycleOperation::Install {
                alias: "힘".to_string(),
                artifact,
            },
        ))
        .expect("install");
        assert!(installed.atomic_apply);
        assert!(installed.after_lock_sha256.is_some());
        assert!(installed
            .project_source
            .files
            .iter()
            .any(|file| file.path == "vendor/운동/gaji.toml"));
        build_project_gaji_lock(installed.project_source.clone(), true)
            .expect("installed lock verifies");
        let removed = build_gaji_lifecycle_plan(lifecycle_request(
            installed.project_source,
            GajiLifecycleOperation::Remove {
                alias: "힘".to_string(),
            },
        ))
        .expect("remove unused");
        assert!(removed.after_lock_sha256.is_none());
        assert!(!removed
            .project_source
            .files
            .iter()
            .any(|file| file.path.starts_with("vendor/운동/")));
    }

    #[test]
    fn gaji_lifecycle_rejects_stale_source_and_referenced_remove_without_mutation() {
        let source = sample_multifile_source();
        let artifact = build_local_gaji_artifact(extraction_request(source.clone())).unwrap();
        let mut stale = lifecycle_request(
            source.clone(),
            GajiLifecycleOperation::Install {
                alias: "힘".to_string(),
                artifact: artifact.clone(),
            },
        );
        stale.expected_source_sha256 = "0".repeat(64);
        assert_eq!(
            build_gaji_lifecycle_plan(stale).unwrap_err().code,
            "E_GAJI_LIFECYCLE_SOURCE_STALE"
        );
        let installed = build_gaji_lifecycle_plan(lifecycle_request(
            source,
            GajiLifecycleOperation::Install {
                alias: "운동".to_string(),
                artifact,
            },
        ))
        .unwrap();
        let before = serde_json::to_string(&installed.project_source).unwrap();
        let error = build_gaji_lifecycle_plan(lifecycle_request(
            installed.project_source.clone(),
            GajiLifecycleOperation::Remove {
                alias: "운동".to_string(),
            },
        ))
        .unwrap_err();
        assert_eq!(error.code, "E_GAJI_REMOVE_REFERENCED");
        assert_eq!(
            serde_json::to_string(&installed.project_source).unwrap(),
            before
        );
    }

    #[test]
    fn gaji_lifecycle_updates_with_diff_and_rolls_back_to_retained_bytes() {
        let source = sample_multifile_source();
        let artifact_v1 = build_local_gaji_artifact(extraction_request(source.clone())).unwrap();
        let installed = build_gaji_lifecycle_plan(lifecycle_request(
            source.clone(),
            GajiLifecycleOperation::Install {
                alias: "힘".to_string(),
                artifact: artifact_v1.clone(),
            },
        ))
        .unwrap();
        let v1_lock = installed.after_lock_sha256.clone();

        let mut changed_source = source;
        changed_source
            .files
            .iter_mut()
            .find(|file| file.path == "lib/운동.ddn")
            .unwrap()
            .utf8_text = "드러냄 { 추가힘. }\n추가힘 <- 2.".to_string();
        let mut request_v2 = extraction_request(changed_source);
        request_v2.version = "2.0.0".to_string();
        let artifact_v2 = build_local_gaji_artifact(request_v2).unwrap();
        let updated = build_gaji_lifecycle_plan(lifecycle_request(
            installed.project_source,
            GajiLifecycleOperation::Update {
                alias: "힘".to_string(),
                artifact: artifact_v2,
            },
        ))
        .unwrap();
        let diff = updated.version_diff.as_ref().expect("version diff");
        assert_eq!(diff.from_version.as_deref(), Some("1.0.0"));
        assert_eq!(diff.to_version.as_deref(), Some("2.0.0"));
        assert!(diff
            .changed_files
            .iter()
            .any(|path| path == "ddn/lib/운동.ddn"));
        assert!(diff
            .added_public_symbols
            .iter()
            .any(|symbol| symbol.ends_with(":추가힘")));
        assert!(diff
            .removed_public_symbols
            .iter()
            .any(|symbol| symbol.ends_with(":속도")));
        assert!(diff.risky);

        let rolled_back = build_gaji_lifecycle_plan(lifecycle_request(
            updated.project_source,
            GajiLifecycleOperation::Update {
                alias: "힘".to_string(),
                artifact: artifact_v1,
            },
        ))
        .unwrap();
        assert_eq!(rolled_back.after_lock_sha256, v1_lock);
        let rollback_diff = rolled_back.version_diff.as_ref().unwrap();
        assert_eq!(rollback_diff.from_version.as_deref(), Some("2.0.0"));
        assert_eq!(rollback_diff.to_version.as_deref(), Some("1.0.0"));
        assert!(rollback_diff.risky);
    }

    #[test]
    fn rejects_traversal_and_backslash() {
        assert_eq!(
            normalize_project_path("../x").unwrap_err().code,
            "E_PROJECT_PATH_SEGMENT"
        );
        assert_eq!(
            normalize_project_path("lib\\x.ddn").unwrap_err().code,
            "E_PROJECT_PATH_BACKSLASH"
        );
    }

    #[test]
    fn project_block_detection_ignores_title_strings_and_comments() {
        assert!(!contains_project_block(
            "설정 { 제목: \"내 프로젝트\". }.\n# 프로젝트 { 가짜. }"
        ));
        assert!(contains_project_block("프로젝트 { 이름: \"정본\". }."));
    }

    #[test]
    fn discovers_virtual_root_before_project_json_fallback() {
        let request = ProjectRootDiscoveryRequest {
            schema: PROJECT_ROOT_DISCOVERY_REQUEST_SCHEMA.to_string(),
            start_path: "app/main.ddn".to_string(),
            explicit_project_path: None,
            files: vec![
                ProjectRootDiscoveryFile {
                    path: PROJECT_ROOT_FILE.to_string(),
                    utf8_text: None,
                },
                ProjectRootDiscoveryFile {
                    path: PROJECT_JSON_FILE.to_string(),
                    utf8_text: None,
                },
                ProjectRootDiscoveryFile {
                    path: "app/main.ddn".to_string(),
                    utf8_text: None,
                },
            ],
        };
        let result = discover_virtual_project_root(request).expect("discover");
        assert_eq!(result.root_kind, "root_ddn");
        assert_eq!(result.root_marker_path.as_deref(), Some(PROJECT_ROOT_FILE));
    }

    #[test]
    fn virtual_root_discovery_rejects_legacy_only() {
        let request = ProjectRootDiscoveryRequest {
            schema: PROJECT_ROOT_DISCOVERY_REQUEST_SCHEMA.to_string(),
            start_path: "app/main.ddn".to_string(),
            explicit_project_path: None,
            files: vec![
                ProjectRootDiscoveryFile {
                    path: "프로젝트.ddn".to_string(),
                    utf8_text: None,
                },
                ProjectRootDiscoveryFile {
                    path: "app/main.ddn".to_string(),
                    utf8_text: None,
                },
            ],
        };
        assert_eq!(
            discover_virtual_project_root(request).unwrap_err().code,
            "E_LEGACY_PROJECT_ROOT_NAME"
        );
    }
}
