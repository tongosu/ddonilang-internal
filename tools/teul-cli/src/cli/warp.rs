use std::path::Path;

use ddonirang_tool::warp_workflow::{WarpBackend, WarpPolicy};

pub fn run_bench(
    path: &Path,
    backend: WarpBackend,
    policy: WarpPolicy,
    threads: usize,
    measure: bool,
    out: Option<&Path>,
) -> Result<(), String> {
    let output = ddonirang_tool::warp_workflow::run_warp_bench_workflow(
        path, backend, policy, threads, measure, out,
    )?;
    print!("{output}");
    Ok(())
}
