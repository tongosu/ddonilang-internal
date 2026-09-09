use std::path::Path;

use clap::ValueEnum;

#[derive(Clone, Copy, Debug, ValueEnum)]
#[clap(rename_all = "kebab-case")]
pub enum PreviewFormat {
    Diff,
    Json,
}

pub use ddonirang_tool::patch_workflow::{run_apply, run_approve, run_propose, run_verify};

pub fn run_preview(path: &Path, format: PreviewFormat) -> Result<(), String> {
    let format = match format {
        PreviewFormat::Diff => ddonirang_tool::patch_workflow::PreviewFormat::Diff,
        PreviewFormat::Json => ddonirang_tool::patch_workflow::PreviewFormat::Json,
    };
    ddonirang_tool::patch_workflow::run_preview(path, format)
}
