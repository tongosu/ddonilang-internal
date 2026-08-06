use std::collections::{BTreeMap, BTreeSet};
use std::fs;
use std::path::Path;

use serde::Serialize;
use serde_json::Value;
use sha2::{Digest, Sha256};

use crate::canon;
use crate::cli::bogae::{BogaeCmdPolicy, BogaeCodec};
use crate::cli::bogae_console::ConsoleCellAspect;
use crate::cli::frontdoor_input::validate_no_legacy_frontdoor_surface;
use crate::cli::run::RunEmitSink;
use crate::cli::trace_tier::TraceTierArg;
use crate::{execute_run_command, RunCommandArgs};

#[derive(Serialize)]
struct SourceSnapshot {
    path: String,
    canonical_source_hash: String,
    control_plan_hash: String,
    warning_count: usize,
}

#[derive(Serialize)]
struct DiffValue {
    canon: String,
}

#[derive(Serialize)]
struct SemanticChange {
    id: String,
    axis: String,
    role: String,
    subject: String,
    before: DiffValue,
    after: DiffValue,
    korean: String,
    applies_as: String,
}

#[derive(Serialize)]
struct Coverage {
    control_init: &'static str,
    control_range: &'static str,
    control_step: &'static str,
    settings: &'static str,
    seum_relations: &'static str,
    solveplan: &'static str,
    mageum: &'static str,
    first_state_hash_divergence: &'static str,
}

#[derive(Serialize)]
struct RunSnapshot {
    state_hash: String,
    trace_hash: String,
}

#[derive(Serialize)]
struct ExecutionPreview {
    engine: &'static str,
    madi: u64,
    baseline: RunSnapshot,
    candidate: RunSnapshot,
    state_hash_equal: bool,
    trace_hash_equal: bool,
    first_divergence_madi: Option<u64>,
    first_divergence_status: &'static str,
}

#[derive(Serialize)]
struct ReviewBoundary {
    requires_human_confirmation: bool,
    approval_event_required: bool,
    rejection_event_supported: bool,
    auto_apply: bool,
    file_write: bool,
    runtime_ast_persisted: bool,
}

#[derive(Serialize)]
struct FalseClaims {
    ai_call: bool,
    automatic_authority: bool,
    automatic_apply: bool,
    file_write: bool,
    full_ast_diff: bool,
    solveplan_diff: bool,
    first_divergence_madi: bool,
}

#[derive(Serialize)]
struct WorldDiffArtifact {
    schema: &'static str,
    status: &'static str,
    authority: &'static str,
    world_id: String,
    candidate_origin: String,
    baseline: SourceSnapshot,
    candidate: SourceSnapshot,
    coverage: Coverage,
    change_count: usize,
    changes: Vec<SemanticChange>,
    summary_ko: Vec<String>,
    execution_preview: Option<ExecutionPreview>,
    review: ReviewBoundary,
    false_claims: FalseClaims,
}

struct CanonSnapshot {
    source: SourceSnapshot,
    controls: BTreeMap<String, Value>,
}

#[derive(Default)]
struct CaptureEmitter {
    out: Vec<String>,
    err: Vec<String>,
}

impl RunEmitSink for CaptureEmitter {
    fn out(&mut self, line: &str) {
        self.out.push(line.to_string());
    }

    fn err(&mut self, line: &str) {
        self.err.push(line.to_string());
    }
}

fn sha256_text(text: &str) -> String {
    format!("sha256:{:x}", Sha256::digest(text.as_bytes()))
}

fn normalized_path(path: &Path) -> String {
    let display = if path.is_absolute() {
        std::env::current_dir()
            .ok()
            .and_then(|cwd| path.strip_prefix(cwd).ok().map(Path::to_path_buf))
            .unwrap_or_else(|| path.to_path_buf())
    } else {
        path.to_path_buf()
    };
    display.to_string_lossy().replace('\\', "/")
}

fn canon_text(value: Option<&Value>) -> String {
    match value {
        None | Some(Value::Null) => "-".to_string(),
        Some(Value::String(text)) => text.clone(),
        Some(other) => serde_json::to_string(other).unwrap_or_else(|_| "-".to_string()),
    }
}

fn snapshot(path: &Path, source: &str) -> Result<CanonSnapshot, String> {
    validate_no_legacy_frontdoor_surface(source)?;
    let output = canon::canonicalize(source, false).map_err(|err| err.to_string())?;
    let plan: Value = serde_json::from_str(&output.maegim_control_json)
        .map_err(|err| format!("E_WORLD_DIFF_CONTROL_PLAN {}", err))?;
    let controls = plan
        .get("controls")
        .and_then(Value::as_array)
        .into_iter()
        .flatten()
        .filter_map(|row| {
            let name = row.get("name")?.as_str()?.trim();
            (!name.is_empty()).then(|| (name.to_string(), row.clone()))
        })
        .collect();
    Ok(CanonSnapshot {
        source: SourceSnapshot {
            path: normalized_path(path),
            canonical_source_hash: sha256_text(&output.ddn),
            control_plan_hash: sha256_text(&output.maegim_control_json),
            warning_count: output.warnings.len(),
        },
        controls,
    })
}

fn push_change(
    changes: &mut Vec<SemanticChange>,
    axis: &str,
    role: &str,
    subject: &str,
    before: String,
    after: String,
    korean_axis: &str,
    applies_as: &str,
) {
    if before == after {
        return;
    }
    changes.push(SemanticChange {
        id: format!("{}:{}", axis, subject),
        axis: axis.to_string(),
        role: role.to_string(),
        subject: subject.to_string(),
        before: DiffValue {
            canon: before.clone(),
        },
        after: DiffValue {
            canon: after.clone(),
        },
        korean: format!("채비 {} {}: {} -> {}", subject, korean_axis, before, after),
        applies_as: applies_as.to_string(),
    });
}

fn semantic_changes(
    baseline: &BTreeMap<String, Value>,
    candidate: &BTreeMap<String, Value>,
) -> Vec<SemanticChange> {
    let names: BTreeSet<String> = baseline.keys().chain(candidate.keys()).cloned().collect();
    let mut changes = Vec::new();
    for name in names {
        let before = baseline.get(&name);
        let after = candidate.get(&name);
        if before.is_none() || after.is_none() {
            push_change(
                &mut changes,
                if before.is_none() {
                    "control_added"
                } else {
                    "control_removed"
                },
                "control",
                &name,
                if before.is_none() {
                    "-".to_string()
                } else {
                    "있음".to_string()
                },
                if after.is_none() {
                    "-".to_string()
                } else {
                    "있음".to_string()
                },
                "존재",
                "control_structure",
            );
            continue;
        }
        let before = before.expect("checked");
        let after = after.expect("checked");
        push_change(
            &mut changes,
            "control_init",
            "constant",
            &name,
            canon_text(before.get("init_expr_canon")),
            canon_text(after.get("init_expr_canon")),
            "기본값",
            "control_value",
        );
        push_change(
            &mut changes,
            "control_range",
            "range",
            &name,
            canon_text(before.get("range")),
            canon_text(after.get("range")),
            "범위",
            "control_contract",
        );
        push_change(
            &mut changes,
            "control_step",
            "step",
            &name,
            canon_text(before.get("step_expr_canon")),
            canon_text(after.get("step_expr_canon")),
            "간격",
            "control_contract",
        );
        let before_type = format!(
            "{}:{}",
            canon_text(before.get("decl_kind")),
            canon_text(before.get("type_name"))
        );
        let after_type = format!(
            "{}:{}",
            canon_text(after.get("decl_kind")),
            canon_text(after.get("type_name"))
        );
        push_change(
            &mut changes,
            "control_type",
            "type",
            &name,
            before_type,
            after_type,
            "자료형",
            "control_contract",
        );
    }
    changes
}

fn run_snapshot(path: &Path, madi: u64) -> Result<RunSnapshot, String> {
    let mut emit = CaptureEmitter::default();
    execute_run_command(
        RunCommandArgs {
            file: path.to_path_buf(),
            madi: Some(madi.to_string()),
            seed: "0x0".to_string(),
            age_target: None,
            state: Vec::new(),
            state_file: Vec::new(),
            diag_jsonl: None,
            diag_report_out: None,
            enable_repro: false,
            repro_json: None,
            run_manifest: None,
            summary_json: None,
            solveplan_out: None,
            artifact: Vec::new(),
            trace_json: None,
            proof_out: None,
            proof_cert_key: None,
            geoul_out: None,
            geoul_record_out: None,
            latency_madi: 0,
            trace_tier: TraceTierArg::TOff,
            lang_mode: None,
            bogae: None,
            bogae_codec: BogaeCodec::Bdl1,
            bogae_out: None,
            bogae_skin: None,
            bogae_overlay: None,
            bogae_cmd_policy: BogaeCmdPolicy::None,
            bogae_cmd_cap: None,
            bogae_cache_log: false,
            bogae_live: false,
            console_cell_aspect: ConsoleCellAspect::Auto,
            console_grid: None,
            console_panel_cols: 0,
            until_gameover: false,
            gameover_key: "게임오버".to_string(),
            sam: None,
            record_sam: None,
            sam_live: None,
            sam_live_host: "127.0.0.1".to_string(),
            sam_live_port: 5001,
            madi_hz: None,
            open_mode: None,
            open_log: None,
            open_bundle: None,
            no_open: true,
            unsafe_open: false,
            run_command_override: None,
        },
        &mut emit,
    )
    .map_err(|err| {
        let detail = emit.err.join(" | ");
        if detail.is_empty() {
            err
        } else {
            format!("{} | {}", err, detail)
        }
    })?;
    let state_hash = emit
        .out
        .iter()
        .find_map(|line| line.strip_prefix("state_hash="))
        .unwrap_or("")
        .to_string();
    let trace_hash = emit
        .out
        .iter()
        .find_map(|line| line.strip_prefix("trace_hash="))
        .unwrap_or("")
        .to_string();
    if state_hash.is_empty() || trace_hash.is_empty() {
        return Err("E_WORLD_DIFF_EXECUTION_HASH 실행 해시가 없습니다".to_string());
    }
    Ok(RunSnapshot {
        state_hash,
        trace_hash,
    })
}

fn build_artifact(
    baseline_path: &Path,
    baseline_source: &str,
    candidate_path: &Path,
    candidate_source: &str,
    madi: Option<u64>,
    world_id: &str,
    candidate_origin: &str,
) -> Result<WorldDiffArtifact, String> {
    let baseline = snapshot(baseline_path, baseline_source)?;
    let candidate = snapshot(candidate_path, candidate_source)?;
    let changes = semantic_changes(&baseline.controls, &candidate.controls);
    let summary_ko = if changes.is_empty() {
        vec!["세계 조절 규칙의 뜻 단위 변경이 없습니다.".to_string()]
    } else {
        changes.iter().map(|change| change.korean.clone()).collect()
    };
    let execution_preview = match madi {
        Some(madi) => {
            let baseline_run = run_snapshot(baseline_path, madi)?;
            let candidate_run = run_snapshot(candidate_path, madi)?;
            Some(ExecutionPreview {
                engine: "teul-cli",
                madi,
                state_hash_equal: baseline_run.state_hash == candidate_run.state_hash,
                trace_hash_equal: baseline_run.trace_hash == candidate_run.trace_hash,
                baseline: baseline_run,
                candidate: candidate_run,
                first_divergence_madi: None,
                first_divergence_status: "not_computed",
            })
        }
        None => None,
    };
    Ok(WorldDiffArtifact {
        schema: "ddn.world_diff.v1",
        status: if changes.is_empty() {
            "no_change"
        } else {
            "candidate_preview"
        },
        authority: "none",
        world_id: world_id.trim().to_string(),
        candidate_origin: candidate_origin.trim().to_string(),
        baseline: baseline.source,
        candidate: candidate.source,
        coverage: Coverage {
            control_init: "landed",
            control_range: "landed",
            control_step: "landed",
            settings: "not_compared",
            seum_relations: "not_compared",
            solveplan: "not_compared",
            mageum: "not_compared",
            first_state_hash_divergence: "not_computed",
        },
        change_count: changes.len(),
        changes,
        summary_ko,
        execution_preview,
        review: ReviewBoundary {
            requires_human_confirmation: true,
            approval_event_required: true,
            rejection_event_supported: true,
            auto_apply: false,
            file_write: false,
            runtime_ast_persisted: false,
        },
        false_claims: FalseClaims {
            ai_call: false,
            automatic_authority: false,
            automatic_apply: false,
            file_write: false,
            full_ast_diff: false,
            solveplan_diff: false,
            first_divergence_madi: false,
        },
    })
}

pub fn run(
    baseline: &Path,
    candidate: &Path,
    out: Option<&Path>,
    madi: Option<u64>,
    world_id: &str,
    candidate_origin: &str,
) -> Result<(), String> {
    let baseline_source = fs::read_to_string(baseline)
        .map_err(|err| format!("E_WORLD_DIFF_READ {}: {}", baseline.display(), err))?;
    let candidate_source = fs::read_to_string(candidate)
        .map_err(|err| format!("E_WORLD_DIFF_READ {}: {}", candidate.display(), err))?;
    let artifact = build_artifact(
        baseline,
        &baseline_source,
        candidate,
        &candidate_source,
        madi,
        world_id,
        candidate_origin,
    )?;
    let text = serde_json::to_string_pretty(&artifact)
        .map_err(|err| format!("E_WORLD_DIFF_JSON {}", err))?
        + "\n";
    if let Some(path) = out {
        if let Some(parent) = path.parent() {
            fs::create_dir_all(parent)
                .map_err(|err| format!("E_WORLD_DIFF_WRITE {}: {}", parent.display(), err))?;
        }
        fs::write(path, text)
            .map_err(|err| format!("E_WORLD_DIFF_WRITE {}: {}", path.display(), err))?;
    } else {
        print!("{}", text);
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::{build_artifact, semantic_changes, snapshot};
    use std::path::Path;

    const BASELINE: &str = r#"채비 {
  중력가속도: 수 <- (9.8) 매김 { 범위: 1..20. 간격: 0.1. }.
}.

(시작)할때 {
  x <- 중력가속도.
}.
"#;

    const CANDIDATE: &str = r#"채비 {
  중력가속도: 수 <- (4.9) 매김 { 범위: 1..20. 간격: 0.1. }.
}.

(시작)할때 {
  x <- 중력가속도.
}.
"#;

    #[test]
    fn world_diff_same_source_is_empty() {
        let baseline = snapshot(Path::new("baseline.ddn"), BASELINE).expect("baseline");
        let candidate = snapshot(Path::new("candidate.ddn"), BASELINE).expect("candidate");
        assert!(semantic_changes(&baseline.controls, &candidate.controls).is_empty());
    }

    #[test]
    fn world_diff_detects_only_changed_control_init() {
        let baseline = snapshot(Path::new("baseline.ddn"), BASELINE).expect("baseline");
        let candidate = snapshot(Path::new("candidate.ddn"), CANDIDATE).expect("candidate");
        let changes = semantic_changes(&baseline.controls, &candidate.controls);
        assert_eq!(changes.len(), 1);
        assert_eq!(changes[0].axis, "control_init");
        assert_eq!(changes[0].subject, "중력가속도");
        assert_eq!(changes[0].before.canon, "9.8");
        assert_eq!(changes[0].after.canon, "4.9");
    }

    #[test]
    fn world_diff_keeps_candidate_without_authority() {
        let artifact = build_artifact(
            Path::new("baseline.ddn"),
            BASELINE,
            Path::new("candidate.ddn"),
            CANDIDATE,
            None,
            "physics.projectile",
            "ai_fixture",
        )
        .expect("artifact");
        assert_eq!(artifact.authority, "none");
        assert!(artifact.review.requires_human_confirmation);
        assert!(!artifact.review.auto_apply);
        assert!(!artifact.review.file_write);
    }
}
