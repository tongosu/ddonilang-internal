# 2026-09-01 DDN V1 source-coordinate shared authority W90

- AI_PROVIDER: OpenAI
- AI_SURFACE: Codex local task
- AI_CAPABILITY: product single-writer implementation, testing, handoff
- SESSION_NICKNAME: DDN V1제품마감Codex
- PROJECT_ROLE: DDN V1 closure execution owner / file owner
- RETURN_LABEL: `[DDN V1제품마감Codex -> Codex관리Work]`
- persistent goal: active; whole-goal BLOCKED removed after verified reviewer
  custody showed blocking finding 0.
- live authority: v25.49.0 / RD-001~543; public SPEC v0.6.0; successor impact is
  additive and does not auto-inherit scoped PASS.
- baseline/fixed: `f566727a` -> `bfe1b67d`, tree `fc95c39a`.
- exact FILE_OWNER: `lang/src/source_coordinate.rs`, `lang/src/lib.rs`,
  `tool/src/lsp/server.rs`, `tool/src/project_authoring.rs`.
- product result: fixed UTF-16 non-BMP LSP coordinate drift and converged LSP
  plus Workbench project-authoring on the shared language helper.
- tests: lang 369/369; LSP 2/2; project-authoring coordinate 1/1; tool lib
  586 PASS plus two isolated-checkout `docs/ssot` environment failures.
- mutation: scalar-count injection RED (1 vs 2, exit 101) -> exact restore SHA
  `a4fb2527ccc6db7ff05efe4c6ba75e2f119c9e7e613593018ab6e0ec41b99672`
  -> GREEN; residue 0.
- tracked WASM: unchanged; freshness correctly RED on new source inventory,
  queued for coherent refresh/review rather than overwriting frozen custody.
- anti-meta: new pack 0, runner 0, meta-test 0, review task/worktree 0.
- historical task-owned untracked custody files remain unstaged and untouched.
- nonclaims: no whole C0~C8, PathIR, VC17, P5/P6, V1 readiness/release,
  activation, legal, Human Smoke or Human PASS closure.
