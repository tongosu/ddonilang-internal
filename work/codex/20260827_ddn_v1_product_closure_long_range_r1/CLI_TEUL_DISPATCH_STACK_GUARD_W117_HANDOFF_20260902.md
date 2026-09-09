# CLI retained-dispatch stack guard W117 — handoff

AI_PROVIDER: OpenAI
AI_SURFACE: Codex Work
AI_CAPABILITY: single-writer product implementation and internal QA
SESSION_NICKNAME: DDN V1제품마감Codex
PROJECT_ROLE: EXECUTION_OWNER / FILE_OWNER
RETURN_LABEL: [DDN V1제품마감Codex -> Codex관리Work]

## Authority and lineage

- Live authority read-only: internal SSOT v25.50.0 / RD-001~551; public Language SPEC v0.6.0.
- Product base: `9e0ce0979dc54eb824b6e9dc07903aae0127041a`.
- Product fixed: `9543297283c30b5533b01d71002966651bdd8f44`.
- Fixed tree: `d96193949d435e6d4e6365951c54ddcaf9f965f7`.
- Direct parent relation holds; merge count is zero.
- Exact product diff: `tools/teul-cli/src/main.rs` only.

## User workflow and implementation

The retained internal/deferred `teul-cli gaji plan` workflow previously overflowed the process main stack before it could execute.  The command dispatcher now runs on a bounded 32 MiB worker stack and propagates any panic to the process.  This preserves command spelling, source/diagnostic contract, and retained physical custody while allowing the existing gaji plan native workflow and its existing WASM parity workflow to execute.

No public command membership, executable/package name, legacy-alias period, or `teul-cli` deletion/retirement decision was made.

## Reused evidence

- `cargo check --manifest-path tools/teul-cli/Cargo.toml --offline`: PASS from a fresh target directory.
- Existing direct `gaji plan` invocation: baseline RED `-1073741571` main-stack overflow; fixed GREEN exit 0.
- Existing `node tests/gaji_creator_wasm_parity_runner.mjs`: PASS.
- Existing `python tests/run_ddn_local_project_graph_check.py`: PASS (G0/G2/G3/G4/G5/G6/G7/G8, including native/WASM project frontdoor checks).
- Existing focused `ddonirang-tool` gaji extraction and lifecycle tests: 1/1 PASS each.

Risk mutation used no new test artifact: changing the worker stack from 32 MiB to 1 MiB produced actual RED exit `-1073741571` and a `teul-cli-dispatch` stack-overflow diagnostic.  Exact restore returned `tools/teul-cli/src/main.rs` SHA-256 `52BDC9F7A4B96E5BE7786FB27F197B59A306FF55781EFC8578C72B733D5481EB`; the direct workflow then returned GREEN.  Mutation residue: 0.

## C0–C8 bounded status

| Gate | Current status |
|---|---|
| C0 | Historical 91-command registry remains custody only; no bulk promotion. |
| C1 | `ddn.project-run.v1` remains the fixed neutral semantic identity; public executable/package/alias are open. |
| C2 | Shared lang/tool authority is preserved; this change is a retained adapter dispatch correction. |
| C3 | Public test/view/repl membership remains Owner-frozen. |
| C4 | Broad private teul parser/runtime/value/canon authority remains nonzero. |
| C5 | `CONCRETE_DETAIL_GAP_DETECTED`: the exact current V1-required CI/script membership is not versioned; historical teul references are custody, not proof of required dependency. |
| C6 | Scoped gaji native/WASM and project-graph parity pass; broad command parity remains open. |
| C7 | Existing P5 evidence is target-bound; no projection or release closure. |
| C8 | Public binary/package retirement and physical deletion are untouched and require their separate gates and Owner approval. |

## Safety, review, and nonclaims

- New dependency, pack, runner, meta-test, review task, review worktree, worktree, and branch: 0.
- Tracked WASM, UI, SSOT, public SPEC, publish, and rights/legal changes: 0.
- `tools/teul-cli` remains physically retained.  Private semantic authority and global required dependency zero are not claimed.
- UNAVAILABLE-3 rights attribution is a separate nonblocking rights track.  No publication, distribution, rights-cleared artifact, release, activation, readiness, membership, or Human PASS claim is made.
- Status: `IMPLEMENTED_UNDER_REVIEW`.  No reviewer is dispatched by the writer; any rolling-review scheduling remains management custody.

## Next safe decision

Before proving C5 required dependency zero, a versioned V1-required CI/script command registry or equivalent Owner-approved projection is needed.  This does not block independent approved product correctness work on disjoint paths.
