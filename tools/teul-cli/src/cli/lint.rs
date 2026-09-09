use std::path::Path;

pub fn run(
    file: &Path,
    source_profile_identity: &str,
    suggest_patch: bool,
    out: Option<&Path>,
) -> Result<(), ddonirang_tool::source_frontdoor_workflow::SourceFrontdoorError> {
    let output = ddonirang_tool::source_frontdoor_workflow::run_lint_supported_profile(
        file,
        source_profile_identity,
        suggest_patch,
        out,
    )?;
    if !output.stdout.is_empty() {
        print!("{}", output.stdout);
    }
    for warning in output.warnings {
        eprintln!("{warning}");
    }
    Ok(())
}
