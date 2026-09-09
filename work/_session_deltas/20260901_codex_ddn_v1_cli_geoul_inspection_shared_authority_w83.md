# [DDN V1제품마감Codex -> Codex관리Work] CLI Geoul inspection shared authority W83

- goal: persistent V1 closure active
- authority: internal v25.47.0 / RD-001~543; public SPEC v0.6.0
- baseline: `ea8e2f723c0cffe1b8beb61ba7f69800c144b60f`
- product fixed/tree: `302024e36f663665ae127efbfbe742f9cc2f9b25` / `ee25782790edb544b63e596db0515e122c1b262c`
- product paths: renamed shared `tool/src/geoul_workflow.rs`, `tool/src/lib.rs`, retained `tools/teul-cli/src/cli/geoul.rs`
- authority: private hash/seek 1 -> 0; shared owner 0 -> 1
- fixture: audit hash PASS, frame 0/1 seek PASS, out-of-range fail-closed PASS
- W82 regression: `geoul_min_schema_v0` 3/3 PASS
- mutation: force frame 0 made out-of-range exit 0 RED -> exact restore SHA-256 `1b2932bdda86fd4ba979d309148c727f2acd10dd1b16bd5c03d264cd9920ef7f` -> exit 1 GREEN; residue0
- review target: W81+W82+W83 coherent bundle, existing rolling reviewer only after management dispatch
- new pack/runner/meta-test/reviewer/worktree/branch: 0
- protected untracked custody unchanged and unstaged
- nonclaims: no public membership, whole CLI/teul/P0-P6/V1/release/Human closure
