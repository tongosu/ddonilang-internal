# CLI canon shared profile authority W10 handoff

## Fixed identity

- authority: internal SSOT v25.45.0 / RD-001~536, public Language SPEC v0.6.0
- baseline: `c1285b49f0948197425a032ede8e8227dfdde849`
- product/test fixed: `87a5d2dba04f0f63023215fe79919ca06a0acf63`
- fixed tree: `e1133ef347da620231c6afedf5b6a8b0acad8234`
- direct parent: yes
- merge count: 0

## User workflow and product change

`teul-cli canon <V25 source> --source-profile v1-core-v25` now consumes
`canonicalize_shared_source_with_supported_profile`, the same shared supported-profile
authority as the official `ddonirang canon` frontdoor. The adapter no longer selects a
private/legacy semantic path when the profile is omitted. Omission fails closed with
`E_SOURCE_PROFILE_REQUIRED`; unknown profiles retain the shared profile diagnostic.

Historical/internal canon custody remains available only through the already established
hidden `--legacy-internal` switch. The historical golden runner now states that custody
explicitly. No public command membership, executable name, package name, or alias lifetime
was selected.

Supported-profile canon accepts only the shared DDN projection plus `--out` and `--check`.
Legacy-only projection options fail closed rather than re-entering the private parser/canon.
`--out` uses the existing shared atomic text-artifact writer, including parent creation and
no replacement before the new artifact is fully written.

## Exact changed paths

- `tools/teul-cli/src/main.rs`
- `tools/teul-cli/src/cli/canon.rs`
- `tools/teul-cli/tests/run_golden.py`

Product code outside these paths, tracked WASM, Workbench UI, SSOT, and public SPEC changed 0.

## RED, tests, parity, and mutation

- baseline RED: `--source-profile` was rejected by clap (exit 2); profile omission entered
  the legacy canon path and rejected the V25 fixture under the wrong authority.
- supported-profile adapter tests: 2/2 PASS.
- existing canon module: 10 PASS + the same two pre-existing failures
  (`E_BOIM_LEGACY_REMOVED` / historical quiet-jjaim expectation); new drift 0.
- official supported-ingress regression: native 7/7, native/WASM exact 2/2,
  tracked-WASM cases 10/10, deterministic repeats 4, partial summary 0.
- direct official-tool/teul canon output SHA parity: PASS.
- profile omitted: exit 2 / `E_SOURCE_PROFILE_REQUIRED`.
- unknown profile: exit 1 / `E_SOURCE_PROFILE_UNSUPPORTED`.
- explicit historical `--legacy-internal`: PASS; omitted historical profile: fail-closed.
- shared atomic artifact writer regression: 2/2 PASS.
- official tracked-WASM freshness: PASS; no WASM refresh required because the product diff
  is confined to the teul adapter and historical test custody.
- risk mutation: the omitted-profile branch was changed to call private canon. A historical
  source then succeeded with exit 0 (RED: private fallback accepted). The exact source was
  restored to SHA-256
  `628c16957dfc42fb70be04a99dee0f93c2169ae761d1e275e3f13a3991941316`;
  omission returned exit 2 and the focused tests returned GREEN 2/2. Residue 0.
- historical W01/W02 golden execution remains failing for unrelated/stale output and legacy
  corpus expectations; no whole-golden PASS is claimed and generated fixture residue was
  restored exactly.

## Anti-meta and review state

- user workflow changed or unblocked: explicit V1 supported-profile canon is reachable from
  the teul custody binary without private semantic fallback.
- new pack: 0
- new runner: 0
- new test artifact: 0 (two inline product unit cases added)
- meta-test: 0
- new review task/worktree/branch: 0
- review bundle target: the next coherent V1 CLI/teul convergence milestone, using the
  existing rolling reviewer only after management dispatch.

## Status and nonclaims

Status: `CLI_CANON_SUPPORTED_PROFILE_SHARED_AUTHORITY_IMPLEMENTED_UNDER_REVIEW`.

This handoff does not claim whole CLI convergence, public `test/view/repl` membership,
physical teul retirement/deletion, PathIR public contract closure, VC17 landing, P0~P6
closure, V1 readiness, release, activation, legal approval, or Human PASS.
