# M1 teul-cli V1 required dependency handoff

## Authority and lineage

- Persistent goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1`
- Internal authority: SSOT v25.42.0 / RD-001~534
- Public Language SPEC: v0.6.0
- Product branch: `codex/ddn-v1-p1a-core-supported-ingress-w1-20260829`
- Direct baseline: `5806eecf64af5c69d76ea65e527ecd4a847f48fc`
- Product/test fixed: `f7fe6041273188ae7309a9b4a4b8028c9f0d0cc2`
- Fixed tree: `a6f93ff3671dbc795d11cd458a353865f4113d80`
- Merge count: 0

This fixed milestone implements the Owner-approved `project-run` contract and
removes `teul-cli` as an execution requirement from the bounded V1-required
build/test/pack/public-projection workflow. It does not delete historical or
INTERNAL/DEFERRED custody.

## User workflow and product contract

The official shared-authority CLI now runs local projects through the existing
typed V25 project linker/runtime and tracked WASM frontdoor.

- Semantic identity: exactly `ddn.project-run.v1`; independent of executable,
  package and legacy alias names.
- `--virtual` combined with positional start or `--project` fails closed with
  `E_CLI_OPTION_CONFLICT`.
- `--out` creates its parent, writes beside the target and atomically replaces
  the final artifact. A failure leaves the old target intact and publishes no
  partial file.
- Official CLI, the retained teul adapter and WASM consume one shared
  `tool::local_project` authority. The adapter has no private project-run
  parser/runtime/value/canon fallback.
- The generic legacy Rust library entry remains byte/behavior compatible;
  explicit V25 selection is confined to the product frontdoors.

## Exact product/test diff

The fixed commit changes 16 paths:

1. `tool/src/bin/ddonirang.rs`
2. `tool/src/local_project.rs`
3. `tool/src/runtime_surface.rs`
4. `tool/src/wasm_api.rs`
5. `tools/teul-cli/src/main.rs`
6. `tests/_run_pack_golden_impl.py`
7. `tests/run_ddn_local_project_graph_check.py`
8. `tests/run_ddn_local_project_workbench_multifile_check.py`
9. `pack/ddn_local_project_graph_v1/expected/project_run_alias_normal_v1.detjson`
10. `pack/ddn_local_project_graph_v1/expected/project_run_alias_spacing_v1.detjson`
11. `pack/ddn_local_project_graph_v1/expected/project_run_grid_summary_v1.detjson`
12. `pack/ddn_local_project_graph_v1/expected/project_run_summary_v1.detjson`
13. `pack/ddn_local_project_workbench_multifile_v1/contract.detjson`
14. `pack/ddn_local_project_workbench_multifile_v1/expected/workbench_project_run_v1.detjson`
15. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
16. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

No new pack, runner, checker or meta-test was created.

## RED to GREEN and verification

The product RED at the baseline was concrete:

- official `ddonirang project-run` returned `E_CLI_COMMAND_UNKNOWN`;
- the teul handler accepted mutually exclusive virtual/disk selectors;
- its output path used direct overwrite rather than an atomic replacement.

Fixed-head verification:

- candidate CLI unit: 8/8 PASS;
- local-project library: 40/40 PASS;
- full tool library in an isolated task Cargo target: 532/532 PASS;
- existing local-project graph/native/WASM runner: PASS, including G7/G8;
- existing workbench multi-file pack golden: PASS;
- candidate/teul virtual project-run output: byte-exact parity, both exit 0;
- teul conflict probe: nonzero with `E_CLI_OPTION_CONFLICT`;
- atomic create/replace/directory-failure and partial-publish-zero checks: PASS
  in the existing graph runner;
- official tracked-WASM freshness: PASS;
- Python source AST parse: 3/3 PASS;
- `git diff --check`: PASS.

The Workbench browser wrapper reached its browser gate but the local checkout
does not contain the `playwright` package (`ERR_MODULE_NOT_FOUND`). No network
download was authorized. The same product pack golden and native/WASM payload
checks are GREEN; actual browser execution remains an environment-gated review
item rather than an inferred PASS.

## C0 through C8 actual status

| Gate | Current fixed-head status |
|---|---|
| C0 | Historical registry custody remains 28 tool + 63 teul = 91 identities. No 91-command public promotion. |
| C1 | `project-run` semantic identity is fixed. Final executable name, package name and alias lifetime remain OPEN. |
| C2 | Existing shared canon/preprocess authority is reused; this milestone adds no semantic parser family. |
| C3 | Official candidate reaches 12/15 audited core workflows. `view`, `test`, and `repl` remain outside this fixed migration. |
| C4 | INTERNAL/DEFERRED commands and physical teul source remain custody; exact public command membership remains OPEN. |
| C5 | Bounded V1-required build/test/pack/public-projection execution dependency on teul is 0. Repository-wide historical references are not deleted. |
| C6 | Project-run input, diagnostic, state, artifact and candidate/adapter parity pass as scoped. Alias lifetime remains OPEN. |
| C7 | Native/WASM parity and freshness pass; browser execution and coherent independent review remain OPEN. |
| C8 | The existing public Windows projection excludes teul source/binary/package, but final retirement and physical deletion require independent PASS, exact deletion inventory and Owner deletion approval. |

## Dependency and residue boundary

The bounded V1-required path audit reports:

- build: official `tool` manifest/bin requires no teul executable;
- tests: supported-ingress and project-run product runners require no teul
  executable (forbidden-name assertions are not dependencies);
- pack: V1 supported-ingress has no teul reference; the existing multi-file
  pack runner now routes `project-run` to the official candidate;
- publish: `publish/v1/**` has zero teul reference;
- public Windows projection: builder and validator retain the prior fixed
  teul-excluded contract.

Historical/non-required physical custody remains explicit: private teul lang
7 files, runtime 7, core/value 11; repository reference-bearing files are
tests 193, packs 363, publish 50, CI workflow 1 and script 1. These counts are
inventory, not required execution dependencies or deletion targets. Private
canon semantic owner count remains 0. No path was deleted.

## M2 scheduling recalculation

PathIR/Proof P1 can now use this handoff as its direct execution base. Read-only
preflight found the internal P0 types in `symbolic/src/lib.rs`, but the P0
handoff still marks a public/sealed product registry and raw-DDN checked-
assumption surface OPEN.

- remaining Owner/detail decisions currently visible: 2 (versioned physical
  wire/CLI/diagnostic/receipt registry; raw DDN checked-assumption surface);
- remaining coherent implementation verticals: 3 (internal checker/identity
  closure, structured native/CLI/WASM receipt path, Workbench/raw-DDN
  projection where authorized);
- reusable evidence: 7 existing command/test groups plus the existing
  `symbolic_rational_expr_v1` corpus; no new framework is planned;
- required verification bundles: symbolic/proof/tool regression, structured
  native/CLI/WASM parity, Workbench structured-consumer check, P1-M01~M14
  risk mutations, tracked-WASM freshness;
- independent-review prerequisites: clean fixed target, exact registry/open-
  surface disposition, mutation restore identities, parity and partial-publish
  evidence.

`P1_ETA=UNKNOWN`: two public physical-contract decisions and the missing local
browser dependency prevent a defensible calendar date. Reversible internal
checker/wire-independent work can continue immediately without inventing those
contracts.

## Status and nonclaims

Status: `M1_TEUL_REQUIRED_DEPENDENCY_IMPLEMENTED_UNDER_REVIEW`.

This is not independent PASS, full C0~C8 closure, final public command
membership, teul source deletion/retirement approval, P0~P6 closure, V1
readiness, release, activation or Human PASS. SSOT and public SPEC changes are
zero.
