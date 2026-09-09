# CLI REPL Session Authority Zero W15 Handoff

## Execution contract

```text
AI_PROVIDER: OpenAI
AI_SURFACE: Codex Work
AI_CAPABILITY: product single-writer implementation and evidence custody
SESSION_NICKNAME: DDN V1제품마감Codex
PROJECT_ROLE: DDN V1 closure execution owner / file owner
RETURN_LABEL: [DDN V1제품마감Codex -> Codex관리Work]
CONTROL_OWNER: Owner / Codex관리Work
MANAGER: Codex관리Work
EXECUTION_OWNER: thread 01a04a01-b812-7840-a2a3-33208dd36e36
FILE_OWNER: tool/src/repl_workflow.rs; tool/src/lib.rs; tools/teul-cli/src/cli/repl.rs; tracked WASM binary/manifest; this handoff/session delta
REVIEWER: existing rolling reviewer only; not dispatched
ORIGIN_TASK_ID: DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1
```

## Authority and lineage

- Internal CURRENT: v25.45.0 / RD-001~536
- Public Language SPEC: v0.6.0
- persistent goal: ACTIVE, not BLOCKED or complete
- baseline: `abb8bc626a8da958ead128903f3244f68fed2e25`
- product/test fixed: `edd4a158d1ff95bd1f68bf972709bacf40f334cc`
- fixed tree: `2396b2e85dd5675eaafda4e73465a02d85f8c070`
- direct parent: YES
- merge count: 0

The earlier W3 lineage `245ff604 -> 45376a96 -> cafc5acd` moved REPL execution onto shared currentline authority but retained `ReplSession`, context/state/hash orchestration in `tools/teul-cli`. W15 is an additive authority-zero successor, not a duplicate public command migration.

## User workflow and product result

The retained `repl` workflow keeps its existing command spelling and console behavior while consuming a single shared native tool owner for:

- explicit supported-profile session creation
- context carry-forward
- per-line execution
- state-hash extraction
- failed-cell atomicity
- reset

`tools/teul-cli/src/cli/repl.rs` now contains only console input/output and meta-command adaptation. Static residue count for private `ReplSession`, direct currentline execution, context/state fields and state-hash extraction in the teul adapter is zero.

No public command membership, executable/package name, alias lifetime, wire schema, UI surface, raw DDN syntax or diagnostic spelling was decided.

## Exact product diff

1. `tool/src/repl_workflow.rs` — new shared native session authority and two in-file product tests
2. `tool/src/lib.rs` — native-only module export
3. `tools/teul-cli/src/cli/repl.rs` — console adapter only
4. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm` — official fixed-source refresh
5. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson` — official source/artifact freshness identity

## RED, mutation, and verification

### RED-first

The new shared owner was first introduced with an explicit unimplemented result. Both product tests failed with `E_REPL_SHARED_AUTHORITY_UNIMPLEMENTED` (0/2), proving that the user workflow could not run through the intended shared authority before implementation.

### Risk mutation

An `unknown-profile -> v1-core-v25` hidden-default mutation made the existing unknown-profile assertion RED. Exact source restore returned SHA-256 `50ba7682decc5e1c91b97356c76ad0824433837cd46610d4ec9c9ba02d0fa216` before final formatting. Final formatted source SHA-256 is `c811d1c3b3badd0cfb2a765c805ece76a7b21d04adc7c14e72482240e75b10d4`. Focused tests returned GREEN and mutation residue is 0.

### Fixed-head checks

- shared REPL focused: 2/2 PASS
- full `ddonirang-tool --lib`: 542/542 PASS
- teul-cli build/check: PASS (pre-existing warnings only)
- actual retained REPL: context accumulation, `:hash`, observation, `:reset`, second hash, exit 0
- profile omission: fail-closed `E_SOURCE_PROFILE_REQUIRED --source-profile`
- official WASM freshness: PASS
- isolated post-WASM shared-changes checker: PASS
- `git diff --check`: PASS
- partial context/state/result publish after invalid cell: 0

The first post-WASM checker attempt hit a shared Cargo target file lock and duplicate PDB output collision before product execution. Re-execution with an isolated target passed; no product defect or residue was inferred from the environment event.

## Artifact identities

- tracked WASM: 5,576,156 bytes
- tracked WASM SHA-256: `4a0ea96206781078cd26f9b546904371ed6a02155f353855f60b87e804ce108e`
- freshness manifest SHA-256: `b1e0c4f4c0634625b7b9e06b862d8240d05faa5245172efb069973809489edad`
- shared REPL source SHA-256: `c811d1c3b3badd0cfb2a765c805ece76a7b21d04adc7c14e72482240e75b10d4`

## C0 through C8 actual state

| Gate | Current status |
|---|---|
| C0 | Historical 28 tool + 63 teul = 91 identities remain custody; no bulk promotion. |
| C1 | `ddn.project-run.v1` remains fixed; executable/package/alias decisions remain OPEN. |
| C2 | Shared parser/canon/preprocess/currentline authorities are preserved; no new semantic family. |
| C3 | Retained `repl` now consumes one shared session authority. Public `test/view/repl` membership remains frozen. |
| C4 | REPL private teul session/runtime/value/state/hash/fallback authority is 0. Other INTERNAL/DEFERRED teul custody remains. |
| C5 | Bounded V1-required build/test/pack/publish teul execution dependency remains 0. Historical references are custody. |
| C6 | Retained REPL profile/diagnostic/context/state behavior passes; whole CLI parity remains OPEN. |
| C7 | Applicable native workflow, tracked WASM freshness and post-WASM shared checks PASS. Current-source P5 W13 review remains separate. |
| C8 | Physical teul source/binary/package deletion and public retirement remain Owner-gated. |

## Anti-meta and review custody

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED: retained REPL no longer owns private semantic session/state execution
NEW_PACK: 0
NEW_RUNNER: 0
NEW_TEST_ARTIFACT_COUNT: 0
NEW_PRODUCT_TEST_CASES: 2 in-file
META_TEST_CREATED: 0
ACTIVE_REVIEW_TASK_COUNT: 0
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
REVIEW_BUNDLE_TARGET: W13 current-source P5 + W14 guard full-set + W15 REPL authority-zero coherent current-lineage milestone
REVIEW_NEEDED_NOW: YES before authority-zero or release closure; management dispatches existing rolling reviewer only
```

## Frozen slices and next safe gate

- SPEC history: frozen in that slice only
- PathIR public physical contract: `CONCRETE_DETAIL_GAP_DETECTED`, internal containment preserved
- public `test/view/repl` membership: Owner gate
- VC17 exact provider landing: Owner/detail gate
- public `view` codec/transport contract: detail gate; no implementation inferred

These are not aggregated into a whole-goal impasse. The next safe work is a fixed-object inventory of remaining private teul semantic owners followed by one reversible internal convergence only where existing authority is complete; otherwise proceed to release custody/P6 preparation without inventing public semantics.

## Nonclaims

This milestone is `CLI_REPL_SESSION_AUTHORITY_ZERO_IMPLEMENTED_UNDER_REVIEW`. It is not public REPL support/membership, whole teul semantic-authority zero, physical retirement/deletion, P0~P6 closure, V1 readiness/release/activation/legal status, Owner Human Smoke or Human PASS.
