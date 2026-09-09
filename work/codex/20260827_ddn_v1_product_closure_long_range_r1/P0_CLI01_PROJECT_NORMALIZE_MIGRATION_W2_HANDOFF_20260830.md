# DDN V1 CLI convergence — project-normalize first migration vertical

Date: 2026-08-30
Goal: existing `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1`
Status: `IMPLEMENTED_UNDER_COHERENT_MILESTONE_REVIEW`

## Authority and fixed lineage

- live internal CURRENT: v25.40.0 / RD-001~515, Owner final 2026-08-30
- live pointer SHA-256: `91fc1cbf89f6782e581dec8070b0798d0714029b69be42de16210a7df4d05ed5`
- internal pointer SHA-256: `077d62cb5237e7a6ae57aba55b72c23a95dc6036c5a7ca784f1d92fd8884de81`
- index SHA-256: `01588eb9b3de4c1420db8489c14d78b125185457f79436fbccc4e3e7fe8351ec`
- manifest SHA-256: `23cbd9f58f26f3e52ab26d3aac829c0fa9c160de058fa3f1c2f6da03094dae80`
- seal SHA-256: `26770b32f516acfe11af0c678bec3c3ece019b1a5e5327b980147a3dd653e5b1`
- public Language SPEC: v0.6.0; CURRENT SHA-256 `6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0`
- requested v25.35 is the live predecessor; v25.40 is additive for this vertical.
- P5 predecessor custody: `d47ed2df -> ee9d28bb`; not rebuilt or rewritten.
- CLI retirement predecessor handoff: `294fc227d7da17fd54bb90e3efeca83572e85fcd`.
- product/test fixed: `e64e5163e0ca47a7818726531ccdc2a0eff14bfb`.
- fixed tree: `4e5f3fc8f98316640c4dd277c1b64fb27c734987`.
- fixed parent: `294fc227d7da17fd54bb90e3efeca83572e85fcd`.
- merge count from `ee9d28bb`: 0.

## C0 registry and C0~C8 actual status

The immutable C0 audit at `4a68c9f1` counted 28 `ddonirang-tool` commands and
63 `teul-cli` commands. The same extraction against the fixed source still
returns 28 and 63. The historical 91-row registry remains custody; it is not a
public-membership table. The later candidate `ddonirang` frontdoor now has four
reachable commands and is not silently inserted into the historical 91 rows.

| gate | actual status |
|---|---|
| C0 | `VERIFIED_CURRENT_SOURCE`: 28 + 63 = 91 historical binary-command identities; candidate frontdoor 4 |
| C1 | `CONCRETE_DETAIL_GAP_DETECTED`: final executable name and legacy alias duration remain Owner-open; `ddonirang` remains a candidate identity |
| C2 | `LIMITED_SCOPE_CLOSED`: shared canon/preprocess authority is independently bound; no reverse source import |
| C3 | `IN_PROGRESS_4_OF_15`: run/check/canon/project-normalize reach the candidate shared frontdoor |
| C4 | `PROPOSAL_ONLY`: 15 core-migration, 15 move-to-shared, 33 internal/deferred custody; exact public membership is still Owner-open |
| C5 | `NOT_STARTED`: selected extended-command migration not inferred |
| C6 | `OPEN`: compatibility/golden migration and alias duration not selected |
| C7 | `OPEN`: one coherent CLI milestone review has not been dispatched by this writer |
| C8 | `OPEN`: public projection excludes teul, but repository dependencies and independent PASS are incomplete; physical deletion is forbidden |

The 15 historical V1 core migration candidates are:

`project-normalize`, `project-discover`, `project-graph`, `project-symbols`,
`project-lock`, `project-run`, `run`, `currentline-run`, `view`, `check`,
`test`, `build`, `lint`, `repl`, `canon`.

## Product vertical

User workflow changed from a deterministic command-not-found failure to:

```text
ddonirang project-normalize <virtual-project.json>
  -> tool::local_project::normalize_virtual_project_source_json
  -> canonical normalized project manifest
```

The command uses the existing shared product API directly. It does not import,
execute or fall back to `teul-cli`. Input/read and semantic failures fail closed;
semantic failures preserve the same structured JSON and exit 2 as the current
teul adapter.

Exact fixed diff:

- `tool/src/bin/ddonirang.rs`
- `tests/run_ddn_local_project_cli_wasm_parity_check.py`

The existing parity runner now executes `tool/Cargo.toml --bin ddonirang` rather
than `tools/teul-cli/Cargo.toml`. New pack/runner/checker/meta-test count is 0.

## RED, GREEN and parity

- RED before product edit: `ddonirang project-normalize ...` ->
  `E_CLI_COMMAND_UNKNOWN project-normalize`, exit 2.
- candidate bin unit tests: 3/3 PASS.
- reused local-project CLI/WASM runner: PASS; one positive normalization and six
  fail-closed path/collision/limit cases.
- local-project library regression: 40/40 PASS.
- P1-A supported ingress regression: native 7, native/WASM exact 2, tracked-WASM
  cases 10, candidate CLI positive 3 / negative 3 PASS.
- current teul vs candidate positive output: exact, 1,218 characters,
  SHA-256 `b35b6acca28534fb29160fd26e68be23c92501c7e4b5eea83bfad91827f4c57d`.
- representative traversal failure: both exit 2 and exact stderr JSON,
  SHA-256 `008c391da7d47d05262865b1215556a6fe8bd2462ee5e6d3eec1584f5278f6dc`.
- no product mutation harness was added; the original missing-command product RED
  and existing six negative workflows were sufficient.

## Remaining teul custody and dependencies

- private parser source: 7 files / 9,531 lines; 22 Rust consumer files.
- private runtime source: 7 files / 25,141 lines; 9 Rust consumer files.
- private core/value source: 11 files / 5,350 lines; 10 value consumer files.
- `tools/teul-cli/src/canon.rs` is a 34-byte shared re-export and is not a second
  canon owner. `tools/teul-cli/src/cli/canon.rs`, check/lint/frontdoor helpers and
  the private parser/runtime/value stack remain retirement residue.
- public Windows candidate build and public projection include no teul source or
  artifact, but repository CI still builds it from one workflow file.
- tracked test references decreased from 191 files at the parent to 190 files at
  the fixed head. Required-test dependency is not yet zero.
- pack references remain 367 files; required/deferred classification is not yet
  complete.
- publish references remain 50 files overall; `publish/v1/**` references are 0.
- the 33 internal/deferred top-level commands and 15 move-to-shared commands are
  preserved in place; no public promotion, deletion or final physical placement
  is inferred.

## Next coherent safe slice

Migrate the remaining local-project family as one user workflow
(`project-discover -> project-graph -> project-symbols -> project-lock ->
project-run`) through the same `tool::local_project` authority, parameterizing
the existing local-project tests instead of creating a runner family.

Proposed exact FILE_OWNER:

- `tool/src/bin/ddonirang.rs`
- `tests/run_ddn_local_project_cli_wasm_parity_check.py`
- `tests/ddn_local_project_cli_wasm_parity_runner.mjs` only if the existing WASM
  invocation must be parameterized
- existing `tests/run_ddn_local_project_graph_check.py` only for direct reuse

No `tool/src/local_project.rs` product lease is expected. If a shared API gap is
reproduced, stop that sub-slice and return exact FILE_OWNER expansion evidence.

## Nonclaims

This handoff does not decide the final executable name, legacy alias duration,
public command membership, internal/deferred physical placement, or an
incompatible migration. It does not close C3~C8, whole P0~P6, V1 readiness,
release, activation, legal/distribution gates, Owner Human Smoke or Human PASS.

