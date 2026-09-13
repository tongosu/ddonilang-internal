# CLI test workflow shared authority W1 handoff

## Execution custody

```text
AI_PROVIDER: OpenAI
AI_SURFACE: Codex local product worktree
AI_CAPABILITY: product single-writer implementation and verification
SESSION_NICKNAME: DDN V1제품마감Codex
PROJECT_ROLE: DDN V1 closure single writer
RETURN_LABEL: [DDN V1제품마감Codex -> DDN V1 관리 Chat]
CONTROL_OWNER: Owner / DDN V1 관리 Chat
MANAGER: DDN V1 관리 Chat
EXECUTION_OWNER: thread 01a04a01-b812-7840-a2a3-33208dd36e36
FILE_OWNER: tool/src/lib.rs, tool/src/test_workflow.rs, tools/teul-cli/src/cli/test.rs, tracked WASM freshness manifest only
REVIEWER: existing rolling reviewer 01a04b17-66bb-7fa3-b827-53ad450005b4; no new review task/worktree
ORIGIN_TASK_ID: DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1
```

## Authority and fixed lineage

- Internal CURRENT: SSOT v25.45.0 / RD-001~536.
- Index SHA-256: `3f998ad22bd1442b07978482877333ae238770ff6d069106d23fde027667cd7d`.
- Aggregate SHA-256: `e94623f128cf9894d76e0b0d8db8de07d4c86ed0aada6cfafab5a2d6f74fad3e`.
- Manifest SHA-256: `4a5656c86dd80c33383075a5dd6a7319bb83d396a205c0baff75e858ee88bb5d`.
- Seal SHA-256: `d8437401411f860e3f9bac5122d6ca76ce659e29185e4f2ebae6894402d8f9b7`.
- Public Language SPEC: v0.6.0; CURRENT SHA-256 `6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0`.
- Baseline/review-bound predecessor: `0ba60fac3b930f9f6d8554bd8e9fe53ea36a64f9`.
- Product/test fixed: `eba99e9d9ff7490400c2ef3ebae151df90fdd390`.
- Fixed tree: `f301267d7845bd77ad234d4f8710c32274194fff`.
- Direct parent: yes. Merge count: 0.

The v25.45 successor has no relevant semantic delta for this bounded native
test workflow. Prior PathIR B-01 PASS remains target-bound only. No broader
PathIR, P1, ERQ, V1, release or readiness verdict is inherited.

## User workflow and product change

The existing `test` workflow previously owned its realms input model,
deterministic execution, result construction, and Python-runner dispatch inside
`tools/teul-cli`. This fixed milestone moves that complete behavior to the
shared `ddonirang-tool` library. The retained teul command is now a four-line
adapter that re-exports the shared owner.

The command spelling and output are unchanged. This is reversible internal
authority convergence, not public command membership or executable naming.
It removes one private teul runtime/value/result and runner-dispatch authority
family without deleting the physical teul package.

Exact product diff:

1. `tool/src/test_workflow.rs` — one shared owner for realms test execution and
   the two existing Python runner dispatches, plus three inline product tests.
2. `tool/src/lib.rs` — native-only shared module export.
3. `tools/teul-cli/src/cli/test.rs` — consumer/adapter only.
4. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson` — official
   source-inventory freshness refresh only; the tracked WASM binary is unchanged.

No pack, runner, checker, framework, public schema, visible UI, parser,
canonicalizer, SSOT or public SPEC was added or changed.

## RED, mutation, tests and artifact custody

Baseline structural RED:

- shared tool owner absent;
- three private teul realms input/output structs;
- six direct private runtime manager references;
- two private Python runner-dispatch functions.

Risk mutation `REALM_COUNT_ZERO_GUARD_BYPASS` disabled the fail-closed zero-realm
guard. The existing inline product test failed with exit 101 and showed a
published zero-realm result. Byte-exact restore returned
`tool/src/test_workflow.rs` SHA-256
`96149ed6f311719ab1d516c6c03f7ceb7ef0c66b5e6a47939ad2e625284a05d9`,
then focused GREEN 3/3. Mutation residue is zero.

Verification:

- full `ddonirang-tool` library: 535/535 PASS;
- existing `gogae8_w78_parallel_realms` pack golden: PASS;
- actual retained CLI `test` command, threads 1 and 8: exit 0 and byte-identical
  output, SHA-256
  `97d4f9402a18aa5cb95298c6a665b9189aa39a9b10c716082ea9670dcd3819b4`;
- official tracked-WASM freshness: PASS;
- `git diff --check`: PASS;
- private teul realms structs/direct manager references after fixed: 0/0;
- partial result/state/outbox publish on the tested invalid input: 0.

The private teul full suite produced 1040 PASS / 14 FAIL. The same 14
pre-existing legacy `보임`, right-assignment and foreach atomicity failures are
already fixed-head custody; this milestone adds no new failure. They are not
promoted to PASS and are outside this adapter-only correction.

Tracked artifact identities:

- manifest Git blob: 20,428 bytes / SHA-256
  `d0e3d64c38f025486e37dd7016f87f6c09307eb2c39717ef775ccfffb2c86d35`;
- tracked WASM: 5,571,041 bytes / SHA-256
  `ac750ce56f9ee34200136147ba7dd6b3d9187c5e023b0817c4ab030dade35de2`;
- WASM binary diff: 0.

## C0 through C8 actual status

| Gate | Fixed-head status |
|---|---|
| C0 | Historical 28 tool + 63 teul = 91 identity inventory remains custody; no bulk public promotion. |
| C1 | `ddn.project-run.v1` remains fixed; executable/package/alias decisions remain OPEN. |
| C2 | Shared source/canon/preprocess authority is unchanged; no semantic parser family was added. |
| C3 | Official candidate remains 12/15 audited workflows. `test` behavior now has one shared tool owner, but official/public command spelling is not inferred. `view` and `repl` also remain open. |
| C4 | INTERNAL/DEFERRED commands and physical teul source remain custody; exact public membership and final placement are OPEN. |
| C5 | Bounded V1-required build/test/pack/publish teul execution dependency remains 0. Historical references are not deletion targets. |
| C6 | The retained native test adapter has exact threads 1/8 result parity; whole command/source/diagnostic/state/artifact parity remains OPEN. |
| C7 | Applicable native workflow and official freshness PASS. This native-only workflow adds no WASM or Workbench command surface. |
| C8 | Public projection exclusion custody is preserved. Physical teul retirement/deletion still needs full authority/dependency inventory, coherent independent PASS, backup/hash/restore and exact Owner deletion approval. |

## PathIR boundary and next safe gate

PathIR P0 containment is preserved. Internal B-01 is independently PASS on its
fixed target. The public PathIR XP-02/M12 and CLI/WASM/Workbench/raw-DDN
positive ingress remain `CONCRETE_DETAIL_GAP_DETECTED`: v25.45 keeps exact wire
schema/version, field spelling, hash prefix, CLI option, transport mapping and
raw morphology OPEN. The existing `P1_CONTRACT_DECISION_REQUIRED.md` packet is
the single decision packet; no duplicate was created.

The next safe CLI choices are constrained:

- `view` would require settling its private codec/wire and public projection;
- `repl` would require settling V25 state/session behavior and command
  membership;
- neither is inferred from historical behavior.

Recommended next decision is to approve a versioned physical PathIR registry,
or separately fix the `view` codec/transport contract. Until then, this fixed
milestone is `IMPLEMENTED_UNDER_REVIEW`, not whole C0-C8 closure.

## Existing rolling review request

```text
ORIGIN_TASK_ID: 01a04a01-b812-7840-a2a3-33208dd36e36
RETURN_TO: 01a04a01-b812-7840-a2a3-33208dd36e36
REVIEWER_TASK_ID: 01a04b17-66bb-7fa3-b827-53ad450005b4
TARGET_COMMIT: eba99e9d9ff7490400c2ef3ebae151df90fdd390
TARGET_TREE: f301267d7845bd77ad234d4f8710c32274194fff
CLAIM: retained native test workflow consumes one shared tool authority with exact prior behavior and no private teul fallback
SCOPE: the four fixed product paths, focused fail-closed mutation, W78 pack/CLI determinism, freshness and protected custody
CANONICAL_PRIMARY_GATE: real teul test invocation consuming ddonirang_tool::test_workflow
STOP_CONDITION: private execution remains, output/diagnostic drift, mutation restore mismatch, new teul regression, or protected diff
NONCLAIMS: public test command membership, full CLI convergence, teul retirement/deletion, PathIR public P1, ERQ closure, V1 readiness/release/Human PASS
```

`NEW_REVIEW_TASK_COUNT=0`, `NEW_REVIEW_WORKTREE_COUNT=0`. Dispatch must reuse
the existing rolling reviewer only.

