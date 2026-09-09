# [DDN V1제품마감Codex -> SSOT관리Work] M1 teul required dependency — handoff

- goal: existing `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1`
- authority: internal v25.42.0 / RD-001~534; public SPEC v0.6.0
- baseline: `5806eecf64af5c69d76ea65e527ecd4a847f48fc`
- fixed: `f7fe6041273188ae7309a9b4a4b8028c9f0d0cc2`
- fixed tree: `a6f93ff3671dbc795d11cd458a353865f4113d80`
- branch/worktree reused; new goal/task/worktree/branch/reviewer: 0
- product behavior: official `project-run` with semantic identity
  `ddn.project-run.v1`, conflict fail-closed, atomic output replacement and
  partial publish 0
- V1-required build/test/pack/publish teul execution dependency: 0 in the
  bounded fixed workflows
- candidate reachability: 12/15; `view`, `test`, `repl` remain OPEN
- tool regression: 532/532; candidate unit 8/8; local project 40/40;
  existing graph native/WASM parity PASS; pack golden PASS; freshness PASS
- browser wrapper: environment blocked by missing Playwright, no download
- new pack/runner/meta-test/reviewer/worktree/branch: 0
- historical/private teul custody and repository references preserved; delete 0
- P1 schedule: two public physical-detail decisions, three coherent verticals,
  `ETA=UNKNOWN`; safe internal successor work may continue
- status: `M1_TEUL_REQUIRED_DEPENDENCY_IMPLEMENTED_UNDER_REVIEW`

The four pre-existing untracked VC06/VC17/P1 custody deltas remain byte-
preserved and unstaged. SSOT/SPEC/UI visible-copy changes are zero. This delta
does not claim CLI retirement closure, V1 readiness, release or Human PASS.
