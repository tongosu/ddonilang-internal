# CLI BDL/observation shared atomic authority W30 handoff

## Identity and scope

- Authority checked read-only: internal SSOT v25.47.0 / RD-001~543; public Language SPEC v0.6.0.
- Successor impact: ADDITIVE_WITH_NO_PUBLIC_MEMBERSHIP_TRANSITION.
- Baseline: `f15e052bc91848d970cd885cb8482b7e8e3f647e`.
- Product fixed: `c6cf45c32d5f2fbdb27c0fc3adb0fd69d983ceff`.
- Product tree: `f8957777f641f9d832c95f7d6c938119bfdf3df9`.
- Direct parent relation: yes. Merge commit: no.

Exact product paths:

1. `tool/src/artifact_output.rs`
2. `tool/src/bdl_packet.rs`
3. `tool/src/lib.rs`
4. `tool/src/observation_workflow.rs`
5. `tools/teul-cli/src/cli/bdl_packet.rs`
6. `tools/teul-cli/src/cli/observation.rs`
7. `tools/teul-cli/src/core/bdl_packet.rs`

No pack, runner, tracked WASM, UI, SSOT, public SPEC, public registry, command
membership, executable/package name, or legacy-alias path changed.

## Product workflow and authority convergence

Before W30, `bdl packet wrap/unwrap` kept the BDL packet codec, file
orchestration, parent creation, and direct `fs::write` publication inside
teul. `observation canon` consumed the language-core observation codec but
still privately owned its file orchestration and direct write path.

W30 moves the complete BDL packet codec and both file workflows into
`ddonirang_tool::bdl_packet`, moves observation file canonicalization into
`ddonirang_tool::observation_workflow`, and generalizes the existing shared
atomic artifact writer to binary bytes. The retained teul files contain only
shared-tool re-exports. BDL packet codec/orchestration authority and
observation canon file-orchestration authority inside teul are therefore 0.

Both workflows reject an existing non-file output target before publication.
Successful file output uses one shared temp-file, sync, and atomic replacement
path. These diagnostics are reversible internal/deferred custody; W30 does not
select their public membership or spelling.

## Product RED, verification, and mutation

Baseline product RED: running the existing BDL1 pack through
`bdl packet wrap` with a directory as `--out` exited 1 with only the host OS
error `os error 5`; shared target-kind and atomic publication authority was
absent. Directory entries remained 0.

Verification used the isolated external Cargo target
`I:/home/urihanl/ddn/codex/build/cargo-target-w30-artifact-codecs`. Shared
build output was not cleaned or reset.

- Shared BDL codec/file workflow: 2/2 PASS.
- Shared observation file workflow: 1/1 PASS.
- Existing shared atomic artifact tests: 2/2 PASS.
- Existing `pack/bdl1_packet_roundtrip`: actual teul wrap/unwrap PASS; input
  and output SHA-256 both
  `9b6e55cd7fd3ce1321ba5a3f275bca6831d9d4cc8a3d3ca68d680627a33d19ec`.
- Existing `pack/gogae5_w47_observation_spec`: actual teul file output exactly
  matched the existing expected canonical payload; output SHA-256
  `1cc00f3dd57e2036cb284b7bf0eb7ad564c914a02454483a0eb2c8ccd2c5825d`.
- Both directory-target cases: exit 1, exact shared diagnostic present,
  directory entries 0, partial result/state/outbox publish 0.
- Clean isolated `teul-cli` build: PASS.
- Tool library regression: 552 PASS; the same two pre-existing `ai_prompt::*`
  tests failed only because the isolated worktree has no `docs/ssot`
  materialization. New regression: 0.
- `rustfmt --check` on exact edited modules and `git diff --check`: PASS.

Risk mutation: invert the BDL output target-kind guard. The exact file workflow
failed RED with exit 101 because the expected shared diagnostic disappeared.
The source was restored byte-for-byte to SHA-256
`649a8ba4ec73c69629eb4cd79f39121e26201aea453dfb32077af818fc92189c`,
and the same focused workflow returned GREEN 1/1. Mutation residue: 0.

## C0 through C8 bounded state

| Gate | W30 state |
|---|---|
| C0 | Historical 28 tool + 63 teul = 91 command inventory remains custody; no membership transition. |
| C1 | `ddn.project-run.v1` and executable/package/alias gates are unchanged. |
| C2 | BDL packet and observation canon file workflows now have one shared tool authority and one atomic artifact publisher. |
| C3 | Public `test`/`view`/`repl`, BDL, and observation command membership remain OPEN. |
| C4 | BDL codec/orchestration and observation canon file-orchestration private teul authority are 0; other INTERNAL/DEFERRED teul custody remains nonzero. |
| C5 | Bounded V1-required build/test/pack/publish teul execution dependency remains 0. |
| C6 | Output target-kind failure is fail-closed and successful publication is atomic; partial publish is 0 for both workflows. |
| C7 | Prior fixed-target reviews remain bound; W25~W30 await one coherent rolling review when management dispatches it. |
| C8 | Teul public binary/package retirement and physical deletion remain Owner-gated. |

## Anti-meta, review, and next safe slice

- USER_WORKFLOW_CHANGED_OR_UNBLOCKED: existing BDL packet roundtrip and
  observation canonical artifact workflows now use shared product authority
  and atomic publication outside the retained teul adapter.
- NEW_TEST_ARTIFACT_COUNT: 0. New in-module product test cases: 3.
- EXISTING_TEST_REUSED_COUNT: 551 pre-existing library cases, two existing
  product packs, and the existing teul build gate.
- META_TEST_CREATED: 0.
- STOP_RULE_APPLIED: no receipt/hash-tamper harness or duplicate pack was added.
- CHANGED_V1_GATE: two more retained teul authority families converged to the
  shared tool and P4 artifact failure atomicity advanced.
- REVIEW_BUNDLE_TARGET: W25 through W30 CLI shared-authority convergence at
  this fixed lineage, using only existing rolling reviewer
  `01a04b17-66bb-7fa3-b827-53ad450005b4` when management dispatches it.
- NEW_REVIEW_TASK_COUNT: 0. NEW_REVIEW_WORKTREE_COUNT: 0.
- NEXT_SAFE_TASK: continue the fixed-object inventory of remaining teul
  private value/runtime/canon/file-publish owners, then select one coherent
  reversible internal authority convergence with existing product tests.

## Nonclaims

Status is `IMPLEMENTED_UNDER_REVIEW`. This is not whole C0~C8 closure, public
BDL/observation membership, teul binary/package retirement or deletion, whole
P4/P5 closure, PathIR public-contract closure, VC17 landing, V1
readiness/release/activation, legal disposition, Owner Human Smoke, or Human
PASS.
