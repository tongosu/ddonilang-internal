# DDN V1 CLI project-run teul test dependency W114

- EXECUTION_OWNER / FILE_OWNER: DDN V1제품마감Codex, existing single writer.
- BASE: `358af346b97c6d04a8e86e9aca299750395d1f32`.
- FIXED: `52c87186c4299f6ea6ad23cc8993f7d99a45be95`.
- Changed only the existing project-workbench boundary runner: its one
  disk-project `project-run` invocation now consumes `ddonirang-tool` instead
  of `tools/teul-cli`.
- `project-run` retained `ddn.project-run.v1`, existing option conflict
  behavior, and existing atomic output implementation; public naming and
  legacy custody remain OPEN.
- Focused native checks passed. The full existing WASM matrix stopped at an
  unrelated stale `running_file_change_fake_summary` expectation before the
  migrated seam, so it is recorded as `REBASE_REQUIRED`, not product PASS.
- New pack/runner/dependency/meta-test: 0. SSOT/SPEC/release/rights changes: 0.
