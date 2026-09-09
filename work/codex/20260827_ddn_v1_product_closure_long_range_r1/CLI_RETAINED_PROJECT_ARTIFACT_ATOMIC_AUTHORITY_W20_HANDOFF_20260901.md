# DDN V1 CLI convergence — retained project artifact atomic authority W20 handoff

Date: 2026-09-01  
Goal: existing `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1`  
Status: `IMPLEMENTED_PENDING_COHERENT_MILESTONE_REVIEW`

## Authority and lineage

- live internal CURRENT: v25.47.0 / RD-001~543
- public Language SPEC: v0.6.0
- successor impact: `UNAFFECTED_WITH_ADDITIVE_OUT_OF_SCOPE_SUCCESSOR`
- baseline / W19 handoff: `5bc276b7031c9bab4ab449b16d4274f325996d77`
- product fixed: `3209a35413c960da65e20d065a326c1a9763b854`
- product fixed tree: `8433b03b2cc9d1f8d863344427ef14db42244818`
- fixed parent: exactly `5bc276b7031c9bab4ab449b16d4274f325996d77`
- merge count from baseline: 0
- P5 fixed-target review remains bound separately at review commit
  `bc84d81d4faa55974975bdb7ec60cb18d9a7ebda`; its target-bound PASS is not
  expanded to this successor source.

## Product workflow and exact diff

The official candidate already reaches the shared `tool::local_project`
authority for `project-normalize`, `project-discover`, `project-graph`,
`project-symbols`, and `project-lock`. The retained teul adapter consumed the
same semantic APIs but privately published each `--out` artifact through
direct `std::fs::write`, so a failed replacement could truncate an existing
artifact.

W20 changes those five final-publication call sites to consume the existing
shared `ddonirang_tool::artifact_output::write_text_artifact_atomic` authority.
Parent-directory behavior and existing command diagnostics remain in place.
No parser, runtime, value, canon, project schema, public spelling, executable
name, package name, alias, or command-membership decision changed.

Exact fixed diff:

- `tools/teul-cli/src/main.rs`

Diff size: 6 insertions / 5 deletions. New pack, runner, framework, meta-test,
or product registry: 0.

## RED, GREEN, fault and parity evidence

- pre-write product RED: five retained project `--out` paths directly used
  `std::fs::write` instead of the shared artifact authority.
- coherent teul binary build from this worktree in a dedicated external target:
  PASS.
- existing fixtures through the real retained executable:
  normalize/discover/graph/symbols/lock = 5/5 exit 0, JSON 5/5, predecessor
  replacement 5/5, temp residue 0.
- fixed-commit reproduction of the same five workflows: 5/5 PASS, temp residue
  0.
- blocked-target fault: normalize output target was an existing directory;
  exit 2, `E_PROJECT_NORMALIZE_WRITE`, target remained intact, temp residue 0.
- actual regression mutation: one normalize call was changed back to direct
  `std::fs::write`; the production authority guard went RED with count 1.
  Exact restore SHA-256 was
  `55e99a482bd728abde8dbe3ed3e96143ff530f31f0c1fb20d92649f12af9fb16`;
  guard returned GREEN with direct-write count 0 and focused 5/5 stayed GREEN.
- normalize structured bytes matched retained teul, official native candidate,
  and tracked WASM exactly; SHA-256
  `b35b6acca28534fb29160fd26e68be23c92501c7e4b5eea83bfad91827f4c57d`.
- semantic field loss: 0; hidden fallback: 0; partial artifact publish observed:
  0.

The existing `run_ddn_local_project_cli_wasm_parity_check.py` was reused but
its default shared target was not accepted as evidence. Its first current-source
attempt exceeded the runner's 180-second Cargo build timeout. After that build
completed, the second attempt reproduced shared global-target contamination:
Cargo selected a stale `ddonirang_lang` artifact from another worktree and
failed with missing current symbols. This is an environment/target-custody
event, not a changed-product failure. A new root-only target then built the
current fixed source coherently, and the same committed runner completed
`OK G1 shared virtual source`. Exact native/WASM/retained bytes matched.

## C0~C8 and teul custody

| gate | current bounded status |
|---|---|
| C0 | historical 28 tool + 63 teul = 91 custody; no bulk promotion |
| C1 | neutral `ddn.project-run.v1` remains fixed; executable/package/alias OPEN |
| C2 | shared parser/canon/preprocess/currentline authority preserved |
| C3 | official candidate shared-authority command reachability preserved |
| C4 | five retained local-project direct final-write sites eliminated; other internal/deferred teul custody remains |
| C5 | bounded V1-required build/test/pack/publish execution dependency remains 0; historical references remain custody |
| C6 | normalize native/WASM/retained adapter exact bytes PASS; whole CLI parity OPEN |
| C7 | current successor source requires one coherent target-bound review bundle |
| C8 | physical teul deletion/public retirement remains Owner-gated |

## Anti-meta and review custody

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: existing local-project output artifacts
  are no longer directly truncated by the retained adapter during replacement.
- `NEW_TEST_ARTIFACT_COUNT`: 0
- `EXISTING_TEST_REUSED_COUNT`: 3 surfaces (five-command fixture execution,
  tracked-WASM normalize runner, shared atomic-writer fault contract)
- `META_TEST_CREATED`: 0
- `STOP_RULE_APPLIED`: yes
- `ACTIVE_REVIEW_TASK_COUNT`: 0 execution turns observed; one existing rolling
  reviewer handle remains reusable
- `NEW_REVIEW_TASK_COUNT`: 0
- `NEW_REVIEW_WORKTREE_COUNT`: 0
- `REVIEW_BUNDLE_TARGET`: current-source coherent V1 CLI/release-custody
  successor through W20, management-routed to the existing rolling reviewer

## Open gates and nonclaims

Public test/view/repl membership, final executable/package naming, legacy alias
duration, internal/deferred command placement, exact VC17 landing, public
PathIR contract, and physical teul deletion remain slice-local OPEN gates.
This handoff does not claim whole CLI convergence, whole teul authority or
dependency zero, P0~P6 closure, V1 membership/readiness, release, activation,
legal/distribution approval, Owner Human Smoke, or Human PASS.
