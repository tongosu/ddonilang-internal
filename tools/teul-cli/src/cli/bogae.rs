use std::path::{Path, PathBuf};

use crate::cli::paths;

pub use ddonirang_tool::bogae_playback_workflow::OverlayConfig;

use clap::ValueEnum;

#[derive(Clone, Copy, Debug, ValueEnum)]
pub enum BogaeMode {
    Web,
    Console,
}

#[derive(Clone, Copy, Debug, ValueEnum)]
pub enum BogaeCodec {
    Bdl1,
    Bdl2,
}

#[derive(Clone, Copy, Debug, ValueEnum)]
pub enum BogaeCmdPolicy {
    None,
    Cap,
    Summary,
}

pub fn default_bogae_out_dir() -> PathBuf {
    paths::build_dir().join("bogae")
}

pub fn is_bogae_out_dir(path: &Path) -> bool {
    path.is_dir() || path.extension().is_none()
}

pub fn resolve_bogae_out_dir(bogae_out: Option<&Path>) -> PathBuf {
    match bogae_out {
        Some(path) if is_bogae_out_dir(path) => path.to_path_buf(),
        Some(path) => path
            .parent()
            .map(|dir| dir.to_path_buf())
            .unwrap_or_else(default_bogae_out_dir),
        None => default_bogae_out_dir(),
    }
}
