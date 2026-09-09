# CLI evolving-universe shared authority W79 handoff

## Identity and scope

- live authority: internal SSOT v25.47.0 / RD-001~543; public Language SPEC v0.6.0
- successor impact: `ADDITIVE`; no public command membership, spelling, SSOT, SPEC, release or Human transition
- baseline: `907e9978f00d63274439263fd274af9bb33287e4`
- product fixed: `a8a89d20ab632168edd57659c8561e2b9e129baf`
- fixed tree: `85f936fd7eed80c9423b4a7f046b0984362f9250`
- direct lineage: yes; merge count: 0

This vertical moves the complete existing `evolving-universe run` orchestration from
the private teul CLI module into the shared `ddonirang-tool` product authority. The
teul module is now a 133-byte adapter. Existing evolve, certificate, hash, path and
atomic-directory authorities are consumed directly; no parallel implementation or
public surface was added.

## Exact product diff

1. `tool/src/evolving_universe_workflow.rs` — 8,997 bytes / SHA-256 `449a210932cd1e66717d6857adba9db886aabc58eb88236c11a33c6d4d83817d`
2. `tool/src/lib.rs` — 3,417 bytes / SHA-256 `cb7ad5e1cfe0a1c23c98a8c3445ffa2e0185cda9f95dcb6a3fd574af4a88d578`
3. `tools/teul-cli/src/cli/evolving_universe.rs` — 133 bytes / SHA-256 `f5f49d4813eadece12af7214f0a520291aea29bdc1fd12fdcab87b4b8c21ceaf`

Private evolving-universe semantic owner count changed from 1 to 0; shared tool owner
count changed from 0 to 1. The CLI command remains custody only and does not become a
V1 public command by this change.

## Product evidence

- existing W99 product workflow was reused; new pack/runner/framework/meta-test: 0
- baseline W99 golden: 0/1 because its stored `evolving_universe_report_hash` is
  already stale (`9b27...` expected versus current `c714...`); this predecessor
  evidence drift was neither edited nor promoted
- fixed direct workflow: exit 0; `new_rules=1`; `new_entities=1`;
  `final_state_hash=sha256:d878e47e59f33f2261da569019cc5e93a37b5a3af912e26c3675f6c487046ca5`;
  report identity unchanged from the current baseline
- baseline/fixed report, generated DDN, evolve metadata, subject and key bytes match;
  certificate-only byte difference is the expected task-local `subject_path` output
  directory, while subject hash and signature remain equal
- deterministic repeat: directory projection hash
  `cab470f62b43718bf6eb11fd215050563aa0a96e653dd1829ea18d287b4bfbc4`
  before/after, exact equal
- missing-pack fault: exit 1 with `E_EVUNIV_POLICY_READ`; pre-existing published
  directory hash stayed exact, partial publish 0
- teul CLI offline locked compile/check: PASS
- mutation: removing the shared module export produced compile RED `E0432`; exact
  restore returned cargo check GREEN; residue 0

The repository-wide tool library suite was not promoted: its known isolated-worktree
SSOT-environment failures remain outside this change. No WASM or Workbench export was
added because this host artifact workflow has no approved applicable projection.

## C0-C8 and anti-meta checkpoint

- C0: historical 91-command inventory custody preserved
- C1: `ddn.project-run.v1` identity preserved; executable naming remains open
- C2: prior W74-W77 bundle remains review-ready; W78-W79 form the next authority bundle
- C3: V1 public frontdoor remains 12/15; public `test/view/repl` membership is frozen
- C4: internal/deferred commands remain physical custody, without deletion
- C5: bounded V1-required build/test/pack/publish teul execution dependency remains 0
- C6: W79 host workflow deterministic and failure-atomic; no inapplicable projection invented
- C7: P5 fixed `3e205ce8...` / handoff `ccaa7132...` / review `bc84d81d...` remains `PASS_TARGET_BOUND`, blocking 0
- C8: teul physical deletion and public binary/package retirement remain Owner-gated

`USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: the existing evolving-universe user workflow now
executes through one shared tool authority instead of private teul orchestration.
`REUSED_TEST_COUNT`: 1 existing W99 workflow plus direct repeat/failure execution.
`NEW_TEST_ARTIFACT_COUNT`: 0. `META_TEST_CREATED`: 0. `NEW_REVIEW_TASK_COUNT`: 0.

Status: `CLI_EVOLVING_UNIVERSE_SHARED_AUTHORITY_IMPLEMENTED_UNDER_REVIEW`.
This is not P0~P6 closure, V1 membership/readiness, release, activation, physical teul
retirement, legal approval, Owner Human Smoke or Human PASS.
