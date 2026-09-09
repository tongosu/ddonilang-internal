# CLI run supported-profile shared authority W4 handoff

## Execution custody

```text
AI_PROVIDER: OpenAI
AI_SURFACE: Codex Work
AI_CAPABILITY: product single-writer implementation and fixed evidence custody
SESSION_NICKNAME: DDN V1제품마감Codex
PROJECT_ROLE: DDN V1 closure execution owner / FILE_OWNER
RETURN_LABEL: [DDN V1제품마감Codex -> Codex관리Work]
CONTROL_OWNER: Owner / Codex관리Work
MANAGER: Codex관리Work
EXECUTION_OWNER: thread 01a04a01-b812-7840-a2a3-33208dd36e36
FILE_OWNER: tools/teul-cli/src/main.rs, tools/teul-cli/src/cli/run.rs,
  tools/teul-cli/src/cli/worker.rs, tools/teul-cli/src/cli/world_diff.rs
REVIEWER: existing rolling reviewer 01a04b17-66bb-7fa3-b827-53ad450005b4;
  no new reviewer/task/worktree was created or dispatched
ORIGIN_TASK_ID: DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1
```

## Authority, baseline, and review custody

Read-only live authority is internal SSOT v25.45.0 / RD-001~536 and public
Language SPEC v0.6.0. `docs/ssot/**` and `publish/spec/**` were not modified.

```text
ROOT_CURRENT_SHA256: 965ddee47d2e6bedfffa09f90548463eccb4f462da9cb7ec8d03b78daace6dbc
INTERNAL_CURRENT_SHA256: d7e48af95b77f797b1c5a439e441813ea42c48d347320637b4df8716156e77ad
PUBLIC_SPEC_CURRENT_SHA256: 6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0
BASELINE: cafc5acd1cae07caf7263f77c6036b1c122e0715
BASELINE_TREE: 6007a7495727ae4f71120090ed3b2b27cee5abf1
PRODUCT_FIXED: 1b7290aebaafb7f7841a0e4be04e1d4bd1706171
PRODUCT_FIXED_TREE: 93e7d2b2be681a8abd4d0672417d7029e7f9fa73
DIRECT_PARENT: true
MERGE_COUNT: 0
```

Review commit `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf` is already an ancestor of
the baseline and remains target-bound to its reviewed CLI test workflow. The
verified P5 review (`bc84d81d4faa55974975bdb7ec60cb18d9a7ebda`, blocking finding
0) also remains bound in the inherited lineage. Neither verdict is widened by
this handoff.

## Product RED and fixed workflow

Before this change, the retained command rejected an explicit supported source
profile at argument parsing time:

```text
teul-cli run <source.ddn> --source-profile v1-core-v25 --madi 1
exit 2: unexpected argument --source-profile
```

The fixed product path is:

```text
raw Korean V25 source + explicit v1-core-v25
-> retained teul run adapter
-> ddonirang_tool::runtime_surface::run_summary_from_supported_source_profile
-> shared resolver and typed V25 DdnProgram
-> shared structured result/state/diagnostic authority
```

The retained adapter adds no parser, runtime, value, canonicalizer, retry, or
fallback authority. Without `--source-profile`, the historical teul run path is
preserved as internal/deferred custody; it is not promoted to V1. An explicit
profile cannot be combined with `--age-target` because no approved combined
shared contract exists; that combination fails closed with the existing
`E_SHARED_RUNTIME_OPTION_UNSUPPORTED` diagnostic.

## Verification

Reused product evidence:

```text
new focused inline product case: 1/1 PASS
shared-runtime teul focused cases: 4/4 PASS
repl shared-authority focused regression: PASS
P1-A official native cases: 7/7 PASS
native/WASM exact cases: 2/2 PASS
tracked-WASM cases: 10/10 PASS
deterministic repeats: 4
partial summary publish: 0
official tracked-WASM freshness: PASS
teul full suite: 1047 PASS + 9 pre-existing FAIL
new full-suite drift: 0
git diff --check: PASS
```

Direct positive frontdoor comparison used the same fixed Korean fixture. The
official CLI and retained teul adapter produced exactly equal full JSON values
(key set and every value), including `source_profile_identity=v1-core-v25`,
output `2`, state hash, public observation trace hash, and `ticks_run=1`.

Fail-closed direct cases:

```text
legacy definition `=`: exit 1 / E_V25_DEFINITION_MIGRATION_REQUIRED
unknown profile: exit 1 / E_SOURCE_PROFILE_UNSUPPORTED
profile + age-target: exit 1 / E_SHARED_RUNTIME_OPTION_UNSUPPORTED
failure summary artifacts published: 0
```

One risk-relevant mutation replaced the supported-profile call with the legacy
source call. The existing product case failed at exit 101 because the legacy
definition was accepted (`RED`). Exact restoration returned the focused case
to 1/1 GREEN. Final `tools/teul-cli/src/cli/run.rs` SHA-256 is
`4b160c11134a8396b3cde47af7abdd4a577ba98f550c556555aa43e713295890`;
mutation residue is 0.

The first attempted mutation run was excluded from evidence: an official-tool
feature build had contaminated that Cargo target with incompatible path-crate
fingerprints. The accepted mutation sequence used a fresh dedicated target and
was GREEN-before, RED-under-mutation, and GREEN-after-exact-restore.

## C0 through C8 current state

| Gate | Current fixed-head status |
|---|---|
| C0 | Historical 28 tool + 63 teul = 91 command identities remain inventory custody; no bulk public promotion. |
| C1 | `ddn.project-run.v1` and other approved neutral identities remain fixed; executable/package/alias decisions are unchanged. |
| C2 | Shared source/canon/preprocess authority is preserved; explicit teul run now consumes the same supported-profile runtime owner. |
| C3 | The prior audited official candidate remains 12/15 workflows. This run adapter convergence does not decide public command membership. |
| C4 | Explicit supported-profile run private parser/runtime/value/canon/fallback authority is 0. Historical no-profile run and other internal/deferred commands remain custody. |
| C5 | The earlier bounded V1-required dependency claim is not widened: required branch-protection `seamgrim-gate` and `scripts/seamgrim_batch_quality_gate_v1.py` still invoke teul over historical legacy corpora. They require a separate approved V1 gate/projection separation, not silent source rewriting. |
| C6 | Official/retained-teul full JSON parity and applicable native/WASM structured parity pass for this V25 run workflow. Whole 91-command parity remains open. |
| C7 | Tracked WASM freshness passes and no tracked WASM refresh was required. P5 target-bound PASS remains preserved, not whole P5 closure. |
| C8 | Teul public binary/package retirement and physical deletion remain open and Owner-gated. |

## Product value and anti-meta accounting

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED: retained teul run accepts explicit V25
  source profile and executes through the shared supported-profile authority
NEW_PACK: 0
NEW_RUNNER: 0
NEW_TEST_ARTIFACT_COUNT: 0
META_TEST_CREATED: 0
EXISTING_TEST_REUSED_COUNT: 7 command/gate groups plus direct parity execution
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
NEXT_PRODUCT_DECISION_ENABLED: separate required V1 CI/release projection from
  historical legacy corpus execution without rewriting that corpus
```

The repository-wide `cargo fmt --check` remains RED on pre-existing unrelated
teul files. The new `run.rs` hunks were formatted locally; no unrelated
format-only churn was introduced.

## Frozen gates and nonclaims

SPEC history, PathIR public physical contract, public `test/view/repl`
membership, and VC17 exact landing remain frozen only in their own slices.
They are not a whole-goal impasse.

This milestone is `IMPLEMENTED_UNDER_REVIEW`. It is not whole C0~C8 closure,
global teul semantic-authority zero, V1-required dependency zero across the
current protected CI graph, public command membership, physical retirement or
deletion approval, P0~P6 closure, V1 readiness, release/publication,
activation, legal clearance, Owner Human Smoke, or Human PASS.
