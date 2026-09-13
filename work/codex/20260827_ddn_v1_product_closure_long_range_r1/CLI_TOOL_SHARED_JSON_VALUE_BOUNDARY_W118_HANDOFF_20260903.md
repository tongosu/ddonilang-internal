# CLI shared JSON value boundary W118 handoff

## Identity

- Product parent: `a877c9053c3198129ec552d6bf7655172a947e9a`
- Product fixed commit: `59f6d7d8edceef44928755087ca9960f17c14120`
- Product fixed tree: `58052974e5a4f933f638f4c1d4232461a44359c6`
- Branch: `codex/ddn-v1-p1a-core-supported-ingress-w1-20260829`
- Authority read-only: internal SSOT `v25.50.0 / RD-001~551`; public Language SPEC `v0.6.0`.

## User workflow and scope

The official `ddonirang project-run` and `currentline-run` binary prints JSON values
produced by the shared `ddonirang-tool` runtime.  A reused default Cargo target had
mixed JSON crate metadata and rejected that boundary with `E0277` before either user
workflow could build.

`tool/src/bin/ddonirang.rs` now accepts and serializes the exact
`ddonirang_tool::serde_json::Value` type through the same re-export.  No source
profile, command spelling, diagnostic spelling, JSON field, artifact contract, or
semantic identity changed.  In particular, `ddn.project-run.v1` remains unchanged.

## Verification

- Pre-fix direct product RED: default-target official `project-run` build failed at
  `pretty_json` with `E0277`, because the lib-returned JSON value did not implement
  the binary-local `serde::Serialize` trait instance.
- `cargo test --manifest-path tool/Cargo.toml --bin ddonirang --offline`: PASS, 10/10.
- `python tests/run_ddn_local_project_graph_check.py`: PASS: existing G0--G8 project
  workflow, including official CLI project-run and tracked-WASM virtual parity.
- Clean isolated target check before the fix was also green, proving the defect was
  a reused-target materialization boundary rather than a new JSON/wire contract.
- `git diff --check`: PASS.

`cargo fmt --check` remains repository-wide RED because of pre-existing formatting
drift outside this one-file lease.  It was not normalized.  The changed hunk has no
format diff under rustfmt's suggested output.

## Custody and next gate

- Product diff: exactly `tool/src/bin/ddonirang.rs`.
- Dependency additions: 0; dependency license/distribution impact: 0.
- New packs/runners/meta-tests: 0; existing product tests reused: 2.
- Mutation: no synthetic mutation was added.  The concrete compiler RED was the
  relevant failure and the fixed official workflow is GREEN; a test-of-test mutation
  would not change a product or release decision.
- No reviewer/task/worktree/branch was created.  This fixed target is queued only
  for the existing rolling reviewer when management bundles the next coherent CLI/P5
  milestone.

Nonclaims: this is not C0--C8 closure, teul-cli physical deletion or public retirement,
P5/release closure, V1 membership/readiness, activation, legal/rightsclearance, or
Owner Human PASS.
