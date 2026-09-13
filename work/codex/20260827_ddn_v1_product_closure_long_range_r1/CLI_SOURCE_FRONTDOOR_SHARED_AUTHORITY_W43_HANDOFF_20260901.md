# CLI source frontdoor shared authority W43 handoff

## Identity

- authority: internal SSOT v25.47.0 / RD-001~543; public Language SPEC v0.6.0
- successor impact: additive implementation convergence; no SSOT/SPEC or membership transition
- branch: `codex/ddn-v1-p1a-core-supported-ingress-w1-20260829`
- baseline: `0636fd217b9f568ec0598f594c99e296382f5bb5`
- product/test fixed: `17d4a12af485686a76c0ea1b934f1979edd62dab`
- fixed tree: `adebdc20bf0e3ac210b6f04bf4e173d8949b934a`
- direct parent: exact; merge count: 0

## Product behavior

The explicit `v1-core-v25` source workflows `check`, `build`, `canon`, and `lint`
now use one typed `ddonirang-tool` source-frontdoor workflow authority. The official
`ddonirang` binary and the retained `teul-cli` adapter consume the same source read,
profile analysis, canonicalization, lint patch publication, typed diagnostic, and
exit-code result. No command spelling, executable/package name, public membership,
global default profile, or legacy alias policy changed.

The `teul-cli` legacy/internal canon path and other deferred command modules remain
custody; this commit does not claim whole-tree private authority zero or physical
retirement.

## Exact product paths

- `tool/src/source_frontdoor_workflow.rs`
- `tool/src/lib.rs`
- `tool/src/bin/ddonirang.rs`
- `tools/teul-cli/src/cli/check.rs`
- `tools/teul-cli/src/cli/canon.rs`
- `tools/teul-cli/src/cli/lint.rs`
- `tools/teul-cli/src/main.rs`

Product/test/pack/tracked-WASM/UI/SSOT/SPEC paths outside this list changed: 0.

## RED to GREEN and parity

Baseline product-facing RED on a missing source:

- `canon`: official `E_CLI_SOURCE_READ <path>` / exit 1, teul `E_CLI_READ` without
  path / exit 1.
- `lint`: official `E_LINT_READ <path>` / exit 2, teul `E_LINT_READ` without path /
  exit 1.

Fixed results:

- missing input: check/build/canon/lint native-teul stdout, stderr, and exit exact
  parity 4/4; exits 1/1/1/2.
- positive V25 source: exact stdout/stderr/exit parity 4/4.
- unknown profile: exact parity 4/4 and fail closed.
- legacy definition `=`: exact parity 4/4 and fail closed.
- lint `--suggest-patch --out`: semantic stdout parity and artifact SHA-256 exact;
  artifact SHA-256 `73fd87a883b3a08e2000dd462d9407c513c6c5a85b07b2a61166922c350de6e2`.
- positive stdout SHA-256: check/build
  `9fa8ce5d86fcc63da743d670f119c0671cbc8bde9ada38eb8bebc84e24c7adaf`,
  canon `89d716055039510594a4a878364e74e4247183d50e97ed8630a9efb88ea3a98b`.

Risk mutation: replace the lint adapter's typed exit propagation with constant exit
1. Missing-source lint became RED (teul exit 1 versus official exit 2). Restore was
byte-exact (`tools/teul-cli/src/main.rs` SHA-256
`70ee27cfd92211635c17152077d5688cf9ce05e073f6df9a07611972e38ba9a6`),
then GREEN exit 2; residue 0.

## Regression

- `ddonirang` binary tests: 10/10 PASS.
- tool source-analysis focused: 12/12 PASS.
- tool lint focused: 4/4 PASS.
- teul supported-profile focused: 3/3 PASS.
- tool library: 560 PASS + 2 pre-existing isolated-worktree environment FAIL
  (`ai_prompt` cannot read absent `docs/ssot`); no new failure.
- legacy canon focused: 10 PASS + the same 2 pre-existing legacy/Foundation failures;
  no new failure.
- existing P1-A aggregate runner reached an unrelated concurrency integration compile
  failure caused by duplicate `ddonirang-lang` crate identities; the direct product
  parity and focused gates above are authoritative for W43.
- `git diff --check`: PASS.

## Anti-meta and custody

- user workflow changed or unblocked: supported source workflows now converge on one
  shared typed implementation; teul adapter diagnostic/exit drift is removed.
- new test artifact count: 0.
- new pack/runner/framework/meta-test count: 0.
- existing product tests/fixtures reused: 5 groups plus direct four-command parity.
- independent review task/worktree created: 0.
- task-owned untracked custody was neither staged nor modified.

## Status and nonclaims

Status: `CLI_SOURCE_FRONTDOOR_SHARED_AUTHORITY_IMPLEMENTED_UNDER_REVIEW`.

This is not whole C0~C8 closure, whole teul semantic-authority zero, required
dependency zero, physical teul retirement, command membership, executable naming,
P0~P6 closure, V1 readiness, release, activation, legal approval, or Human PASS.

