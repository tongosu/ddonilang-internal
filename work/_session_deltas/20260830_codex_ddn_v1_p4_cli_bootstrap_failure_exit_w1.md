# 2026-08-30 DDN V1 P4 CLI bootstrap failure exit W1

- Session/role: `DDN V1제품마감Codex` / single product writer
- Authority: internal `v25.35.0 / RD-001~490`; public SPEC `v0.6.0`
- Baseline: `a5225a3a4c42621365bfbd9fc9e835c811076cae`
- Fixed: `174d7312e8773630fafc2ca0a5ff4fd0e5486531`
- Fixed tree: `a7f76cf9f9cbd9b863f800be4745026f1539012f`
- Exact product path: `tool/src/main.rs`
- RED: required SSOT/project-policy bootstrap failure printed, output absent, exit 0.
- GREEN: same failure exit 1; invalid lang-mode exit 2; help exit 0.
- Regression: binary build PASS; tool lib 527/527; diff-check PASS.
- New test/runner/pack/framework/meta-test: 0/0/0/0/0.
- Review: queue with coherent P4 milestone; new reviewer/worktree 0.
- Open: command-local post-bootstrap fail-open branches require separate bounded correction; all broad closure/release/Human gates remain OPEN.
