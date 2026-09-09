# CLI currentline teul shared authority W2 handoff

## Roles and scope

```text
AI_PROVIDER: OpenAI
AI_SURFACE: Codex Work
AI_CAPABILITY: product single-writer implementation and fixed evidence custody
SESSION_NICKNAME: DDN V1제품마감Codex
PROJECT_ROLE: DDN V1 closure execution owner / file owner
RETURN_LABEL: [DDN V1제품마감Codex -> Codex관리Work]
CONTROL_OWNER: Owner / Codex관리Work
MANAGER: Codex관리Work
EXECUTION_OWNER: thread 01a04a01-b812-7840-a2a3-33208dd36e36
FILE_OWNER: the six fixed paths listed below
REVIEWER: existing rolling reviewer 01a04b17-66bb-7fa3-b827-53ad450005b4, not dispatched by this handoff
ORIGIN_TASK_ID: DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1
```

This milestone binds the already verified P5 review and removes the retained
`currentline-run` private teul execution/writer path. It does not decide public
executable naming, command membership, alias lifetime, or physical teul
retirement.

## Authority and lineage

Live read-only authority is internal SSOT v25.45.0 / RD-001~536 and public
Language SPEC v0.6.0. Shared-root identities were rechecked without modifying
`docs/ssot/**`:

- root CURRENT: `965ddee47d2e6bedfffa09f90548463eccb4f462da9cb7ec8d03b78daace6dbc`
- internal CURRENT: `d7e48af95b77f797b1c5a439e441813ea42c48d347320637b4df8716156e77ad`
- index: `3f998ad22bd1442b07978482877333ae238770ff6d069106d23fde027667cd7d`
- aggregate: `e94623f128cf9894d76e0b0d8db8de07d4c86ed0aada6cfafab5a2d6f74fad3e`
- manifest: `4a5656c86dd80c33383075a5dd6a7319bb83d396a205c0baff75e858ee88bb5d`
- seal: `d8437401411f860e3f9bac5122d6ca76ce659e29185e4f2ebae6894402d8f9b7`
- public SPEC CURRENT: `6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0`

The P5 review-handle blocker was stale. The exact review is bound in the
product lineage:

```text
P5_FIXED: 3e205ce816e47d29f6488bd86d029750e6afaaf5
P5_HANDOFF: ccaa7132e9192a26f003917ae4f2795482c4e74f
P5_REVIEW_PASS: bc84d81d4faa55974975bdb7ec60cb18d9a7ebda
P5_REVIEW_REPORT_SHA256: 05d9522c900d5c164064a003f92fabc100f64daf40100690b0e3c3747892a6d6
P5_REVIEW_BLOCKING_FINDINGS: 0
IMPLEMENTATION_1: fa31528265aff73cbc7abbc72e7610bc72b115ba
IMPLEMENTATION_2_AND_FIXED: 31f22354f74afcf30eba40c1ab6e6e5f0775b979
FIXED_TREE: c21b165ccac519e49a6693739cc2cb708f4b9151
DIRECT_LINEAGE: true
MERGE_COUNT: 0
```

## User workflow and product change

Product RED was the retained teul invocation of the existing V25 source:

```text
teul-cli currentline-run --cell
  pack/seamgrim_wasm_cli_runtime_parity_v1/cases/c01_console_grid_scalar/input.ddn
exit 1: E_SHARED_RUNTIME_OPTION_UNSUPPORTED
```

The fixed path is now:

```text
raw V25 cell + explicit v1-core-v25 profile
-> shared supported-profile resolver
-> shared currentline execution transaction
-> shared atomic summary/context writers
-> official CLI or retained teul adapter
```

The teul adapter requires an explicit profile. Omission fails closed with exit
2 and `E_SOURCE_PROFILE_REQUIRED`; there is no hidden PreV25/default retry.
The official CLI and retained adapter now emit byte-identical stdout, summary,
and context for the reused source fixture.

Exact product paths across the two implementation commits:

```text
tool/src/currentline_workflow.rs
tool/src/bin/ddonirang.rs
tool/src/lib.rs
tools/teul-cli/src/main.rs
solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm
solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson
```

The first commit introduced the one shared product authority and lowered both
CLIs to consumers. The second commit refreshed only the fixed-source internal
WASM candidate and its official freshness manifest after a clean detached
candidate build proved the prior tracked binary was not byte-identical.

## Verification

Successful reused checks:

```text
shared currentline focused test: 1/1 PASS
tool --lib: 536/536 PASS
official CLI bin tests: 9/9 PASS
lang currentline focused tests: 5/5 PASS
teul-cli cargo check: PASS (warnings only)
official tracked-WASM freshness: PASS
post-WASM shared consumer check: PASS
clean fixed-source offline WASM candidate build/seal: PASS
```

Direct currentline parity:

```text
official exit: 0
teul exit: 0
summary SHA256 both: 5103016f218379c1ee87156011c72a3e6912f47f5316dea85694f9a623f7faf9
context SHA256 both: f0975c7ff8dcf1b246439d43be5a876a56413ebb0a4021fab84bd322c2957063
stdout SHA256 both: 149d9f361c36fa3cbb9bf66e378299ac0ea7d87ef9b210b4af82032868d21de5
missing-profile exit: 2
partial summary/context publish on failure: 0
```

The applicable tracked WASM/Workbench structured consumer uses the same runtime
state/output authority and does not reconstruct semantics in JS. The refreshed
fixed-source candidate is:

```text
WASM bytes: 5,568,161
WASM SHA256: 1c898279c3ba61f2334013aebb3d796ec7ee7ee8f38f59c4fd9c6e392c3c3b40
manifest bytes: 20,595
manifest SHA256: e55ac52d3087d02ff603af42a8b763b0822534ff52d322a0146b636788ca432b
candidate receipt semantic identity: sha256:aab8074384295a5e5eeac87132908948f0d94828a5752c508186b83b34a2e474
```

One risk-relevant mutation replaced the missing-profile guard with a hidden
`v1-core-v25` default. The missing-profile case became exit 0 (RED). Exact
restore of `tools/teul-cli/src/main.rs` to SHA256
`8bd67bfd75727e4a4c6645dbec2b3798ac0abc158fd538657ac5de389c288070`
restored exit 2 and the focused GREEN results; residue is 0.

The historical full runtime-parity checker was also attempted. It is not a
valid current gate because its native invocation omits `--bin` after the tool
crate gained two binaries, and its old symbolic/legacy-boim cases intentionally
conflict with current fail-closed behavior. This pre-existing checker drift was
not hidden, rewritten, or counted as a product regression. Direct product
frontdoors and the focused existing fixture above are the evidence for this
vertical.

## C0 through C8 actual state

| Gate | Current fixed-head status |
|---|---|
| C0 | Historical 28 tool + 63 teul = 91 registry remains custody; no bulk promotion. |
| C1 | `ddn.project-run.v1` and prior approved identities are preserved; executable/package/alias decisions remain open. |
| C2 | Shared source/canon/preprocess authority is preserved; currentline now also has one shared execution and atomic-writer authority. |
| C3 | Official candidate remains 12/15 previously audited workflows. The retained teul currentline command is now an adapter to that shared authority. |
| C4 | Currentline private teul runtime/value/canon/fallback authority is 0. Other internal/deferred teul source custody remains nonzero. |
| C5 | Previously bounded V1-required build/test/pack/publish teul execution dependency remains 0; historical references are custody, not deletion targets. |
| C6 | Currentline official/teul result, state artifact, diagnostic, and applicable WASM/Workbench semantic parity pass in this scope. Whole CLI parity remains open. |
| C7 | Fixed-source offline candidate seal and tracked WASM freshness pass; P5 PASS remains target-bound, not whole P5 closure. |
| C8 | Teul public binary/package retirement and physical deletion remain open and Owner-gated. |

## Anti-meta and frozen gates

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED: retained currentline-run now executes V25 through the shared product authority
NEW_PACK: 0
NEW_RUNNER: 0
NEW_TEST_ARTIFACT_COUNT: 0
META_TEST_CREATED: 0
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
REUSED_TEST_COMMAND_COUNT: 8 successful gates plus one direct parity execution
NEXT_PRODUCT_DECISION_ENABLED: classify remaining teul private view/repl authority without treating public membership as decided
```

SPEC history, PathIR public physical contract, public `test/view/repl`
membership, and VC17 exact landing remain frozen only in their own slices. They
are not aggregated into a whole-goal impasse. The next safe product work is a
bounded current-source graph audit followed by a reversible internal
`view` or `repl` convergence only if its semantic contract is already fixed;
otherwise report the exact detail gate and continue a non-overlapping V1
correctness/release-custody vertical.

## Nonclaims

This is `IMPLEMENTED_UNDER_REVIEW`. It is not whole C0~C8 closure, global teul
semantic-authority zero, exact public command membership, physical retirement
or deletion approval, P0~P6 closure, V1 readiness, release/publication,
activation, legal clearance, Owner Human Smoke, or Human PASS.
