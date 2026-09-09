use std::path::Path;

use crate::cli::bogae::{BogaeCmdPolicy, BogaeCodec};
use crate::cli::bogae_console::ConsoleCellAspect;
use crate::cli::run::RunEmitSink;
use crate::cli::trace_tier::TraceTierArg;
use crate::{execute_run_command, RunCommandArgs};

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

fn run_snapshot(
    path: &Path,
    madi: u64,
) -> Result<ddonirang_tool::world_diff_workflow::RunSnapshot, String> {
    let mut emit = CaptureEmitter::default();
    let execution_path = if path.is_absolute() {
        std::env::current_dir()
            .ok()
            .and_then(|cwd| path.strip_prefix(cwd).ok().map(Path::to_path_buf))
            .unwrap_or_else(|| path.to_path_buf())
    } else {
        path.to_path_buf()
    };
    let execution_path = execution_path.to_string_lossy().replace('\\', "/").into();
    execute_run_command(
        RunCommandArgs {
            file: execution_path,
            source_profile: None,
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
            no_open: false,
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
        .find_map(|line| {
            line.strip_prefix("public_observation_trace_hash=")
                .or_else(|| line.strip_prefix("trace_hash="))
        })
        .unwrap_or("")
        .to_string();
    if state_hash.is_empty() || trace_hash.is_empty() {
        return Err("E_WORLD_DIFF_EXECUTION_HASH 실행 해시가 없습니다".to_string());
    }
    Ok(ddonirang_tool::world_diff_workflow::RunSnapshot {
        state_hash,
        trace_hash,
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
    ddonirang_tool::world_diff_workflow::run(
        baseline,
        candidate,
        out,
        madi,
        world_id,
        candidate_origin,
        run_snapshot,
    )
}
