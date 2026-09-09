use serde::Deserialize;
use std::fs;
use std::path::{Path, PathBuf};

use crate::cli::{paths, run};
use crate::core::{hash, State};

const EXAMPLES_SCHEMA: &str = "malmoi.examples_manifest.v1";

use ddonirang_tool::docset_workflow::build_docset_atomic;
pub use ddonirang_tool::docset_workflow::{run_build, DocBuildOptions};

#[derive(Deserialize)]
struct ExamplesManifest {
    schema: String,
    examples: Vec<ExampleSpec>,
}

#[derive(Deserialize)]
struct ExampleSpec {
    id: Option<String>,
    path: String,
    ticks: Option<u64>,
    seed: Option<u64>,
    state_hash: String,
}

pub struct DocVerifyOptions {
    pub pack: PathBuf,
    pub out: Option<PathBuf>,
}

pub fn run_verify(opts: DocVerifyOptions) -> Result<(), String> {
    let pack = &opts.pack;
    let golden_hash_path = pack.join("golden_docset_hash.txt");
    let golden_hash = fs::read_to_string(&golden_hash_path).map_err(|e| {
        format!(
            "E_DOCSET_GOLDEN_READ {} ({})",
            golden_hash_path.display(),
            e
        )
    })?;
    let golden_hash = golden_hash.trim();
    if golden_hash.is_empty() {
        return Err("E_DOCSET_GOLDEN_EMPTY".to_string());
    }

    let out_dir = opts
        .out
        .unwrap_or_else(|| paths::build_dir().join("malmoi_docset"));
    let result = build_docset_atomic(&out_dir)?;
    if result.docset_hash != golden_hash {
        return Err(format!(
            "E_DOCSET_NONDETERMINISM expected={} got={}",
            golden_hash, result.docset_hash
        ));
    }

    let manifest_path = pack.join("examples_manifest.json");
    let manifest_text = fs::read_to_string(&manifest_path).map_err(|e| {
        format!(
            "E_DOCTEST_MANIFEST_READ {} ({})",
            manifest_path.display(),
            e
        )
    })?;
    let manifest: ExamplesManifest = serde_json::from_str(&manifest_text)
        .map_err(|e| format!("E_DOCTEST_MANIFEST_PARSE {e}"))?;
    if manifest.schema != EXAMPLES_SCHEMA {
        return Err(format!("E_DOCTEST_MANIFEST_SCHEMA {}", manifest.schema));
    }

    let mut passed = 0u64;
    for (idx, example) in manifest.examples.iter().enumerate() {
        let entry_id = example
            .id
            .clone()
            .unwrap_or_else(|| format!("example-{}", idx + 1));
        let ticks = example.ticks.unwrap_or(1);
        let seed = example.seed.unwrap_or(0);
        let path = Path::new(&example.path);
        let source = fs::read_to_string(path)
            .map_err(|e| format!("E_DOCTEST_SOURCE_READ {} ({})", path.display(), e))?;
        let output = run::run_source_with_state_seed_ticks(&source, State::new(), seed, ticks)
            .map_err(|err| format!("E_DOCTEST_FAIL {} {}", entry_id, err.format(&example.path)))?;
        let state_hash = hash::state_hash(&output.state);
        if state_hash != example.state_hash {
            return Err(format!(
                "E_DOCTEST_FAIL {} expected={} got={}",
                entry_id, example.state_hash, state_hash
            ));
        }
        passed += 1;
    }

    println!("docset_hash={}", result.docset_hash);
    println!("docset_verify=ok");
    println!("doctest_passed={}", passed);
    Ok(())
}
