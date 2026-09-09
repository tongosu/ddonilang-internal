use std::fs;
use std::path::Path;

pub use ddonirang_tool::artifact_output::write_text_artifact_atomic as write_text;
pub use ddonirang_tool::runtime_surface::sha256_hex;

#[allow(dead_code)]
pub fn read_text(path: &Path) -> Result<String, String> {
    fs::read_to_string(path).map_err(|e| e.to_string())
}
