# 2026-09-02 DDN V1 CLI teul shared typed bridge W116

- AI_PROVIDER: OpenAI
- AI_SURFACE: Codex Work
- PROJECT_ROLE: persistent V1 closure single writer
- FILE_OWNER: `tool/src/runtime_surface.rs`, `tools/teul-cli/src/cli/run.rs`
- PRODUCT_VALUE: an existing internal CLI adapter can compile while consuming
  the shared runtime's typed input/profile authority; V1 `project-run` remains
  reachable from the single shared tool frontdoor.
- RED: legacy direct types at the shared boundary produced duplicate-crate
  `E0308` in the existing lifecycle runner.
- GREEN: offline teul-cli check and direct shared `ddn.project-run.v1` run.
- Existing gaji lifecycle result: unchanged first `gaji plan` stack overflow
  (`3221225725`), so full runner is `REBASE_REQUIRED`, not a project-run PASS.
- NEW_TEST_ARTIFACT_COUNT: 0; META_TEST_CREATED: 0; dependency additions: 0.
- SSOT/SPEC/public command/membership/release transition: 0.
- REVIEW: no new task, worktree, branch, or dispatch.
