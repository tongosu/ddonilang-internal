# P0 CLI01 Korean core command surface W8 handoff

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
FILE_OWNER: tool/src/bin/ddonirang.rs and freshness-RED-required tracked WASM binary/manifest
REVIEWER: none dispatched
ORIGIN_TASK_ID: DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1
```

## Fixed lineage

```text
BRANCH: codex/ddn-v1-p1a-core-supported-ingress-w1-20260829
BASE_COMMIT: e80682d08545680f331a504ad579c9f4a41418cb
BASE_TREE: db9fbbe6626bf1d637a458b7b97ad2a27c3ecad6
PRODUCT_TEST_FIXED_COMMIT: dc0a48a9767c3c96b2c8a9e6e0c79ff944a5ce12
PRODUCT_TEST_FIXED_TREE: 05be0cbe751298d613785f4fa23918754edeac47
DIRECT_PARENT: true
MERGE_COUNT: 0
```

The fixed commit changes exactly:

- `tool/src/bin/ddonirang.rs`
- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

## Authority and scope

The read-only live authority is internal SSOT v25.42.0 / RD-001~534 and
public Language SPEC v0.6.0. RD-529 separates CLI spelling from language
profile identity. RD-530 fixes the Korean spellings used here. This successor
is additive to prior fixed evidence and does not inherit or promote a whole
P0/P1/V1 PASS.

This vertical binds only already-implemented command identities:

| Stable command identity | Preferred Korean ingress | Existing technical ingress |
|---|---|---|
| RUN | `실행` | `run` |
| CHECK | `검사` | `check` |
| BUILD | `짓기` | `build` |
| CANON, developer exposure | `개발 정본` | `canon` |
| HELP | `도움`, `--도움` | `help`, `--help`, `-h` |
| VERSION | `판본`, `--판본` | `version`, `--version`, `-V` |

Every localized spelling maps directly to the pre-existing `Command` enum.
Source-command parsing receives the canonical technical identity so missing
profile, unknown option and other structured failure behavior remains exact.
No executable/package name, command membership, legacy duration, new parser,
new runtime or private fallback was introduced.

RD-530 surfaces whose product command owner is not yet present (`시험`,
`다듬기`, `재현`, `검증`, `진단`, `개발 구문` and the larger nested families)
remain product-open and were not inferred from the authority document.

## Product RED and GREEN

At the immutable base:

```text
technical run: exit 0
Korean 실행: exit 2
Korean diagnostic: E_CLI_COMMAND_UNKNOWN 실행
```

At the fixed commit, six technical/Korean command pairs have exact exit,
stdout and stderr parity. The same V25 raw Korean source fixture is consumed
without test-only lowering. Missing `--source-profile` returns exit 2 and the
same `E_SOURCE_PROFILE_REQUIRED` diagnostic for `run` and `실행`.

## Tests and risk mutation

Reused product evidence:

- official CLI bin tests: 9/9 PASS (eight pre-existing tests plus one inline
  command-identity test; no new test file or framework);
- supported ingress native: 7/7 PASS;
- native/WASM exact payload: 2/2 PASS;
- tracked WASM: 10/10 PASS, deterministic repeats 4, partial summary 0;
- direct technical/Korean pairs: 6/6 exact exit/stdout/stderr parity;
- official tracked-WASM freshness: PASS;
- `git diff --check`: PASS.

Risk mutation `KOREAN_RUN_ALIAS_REMOVED` removed only the `실행` match arm.
The focused product test produced actual RED, exit 101 and one failed
assertion. Exact restore returned
`tool/src/bin/ddonirang.rs` SHA-256
`7f5e53da19abbf64428fb5ced71968978e0add1236108455107fe75b83f6b5fa`,
then focused GREEN 1/1 and full bin GREEN 9/9. Mutation residue is zero.

## WASM freshness disposition

The freshness ledger intentionally includes all `tool/src/*.rs`, including
the native-only CLI bin. It therefore failed closed after the CLI source
change. A fixed Git object materialization was built with the existing P5
candidate remap entrypoint:

```text
MATERIALIZATION_COMMIT_OBJECT: 2bdfefd6ba39a0e28d84d8c59007b048f05d1cb8
MATERIALIZATION_TREE: b9882e8313bdaff170b819e2295fac3a594e75ac
CANDIDATE_REMAP_IDENTITY: sha256:902376dae906cfb508f990e289c90fd353f8b94b0a2bf9dc3af28a2aaa40fda3
TRACKED_WASM_BYTES: 5568289
TRACKED_WASM_SHA256: 0826e5d91e07f79900a60fdca5255127eff7c04a6117c5dd174eb258a33e077c
```

Generated JS, d.ts and package files were byte-identical to their tracked
predecessors and were not changed. Only the path-clean candidate binary and
its existing freshness manifest were refreshed. This is not tracked-WASM
public membership, P5 closure or release promotion.

## C0 through C8 actual state

| Gate | Fixed-head status |
|---|---|
| C0 | Historical 28 tool + 63 teul = 91 identities remain inventory custody; public promotion is zero. |
| C1 | `ddn.project-run.v1` remains fixed; executable/package/alias decisions remain open. |
| C2 | Shared canon/preprocess authority is unchanged; no new semantic family exists. |
| C3 | The prior 12/15 official workflow count is unchanged; existing RUN/CHECK/BUILD/CANON/HELP/VERSION now have the authorized Korean ingress subset. `view/test/repl` remain open. |
| C4 | Internal/deferred commands and physical teul source remain custody; exact public membership is open. |
| C5 | Bounded V1-required build/test/pack/publish execution dependency on teul remains zero. Historical references are not dependencies or deletion targets. |
| C6 | Localized and technical native results/diagnostics are exact for the implemented subset; whole command parity remains open. |
| C7 | Native/WASM parity and refreshed path-clean WASM freshness pass; Workbench/browser and coherent independent review remain open. |
| C8 | Public projection exclusion custody is preserved; physical teul retirement/deletion still needs the previously required review, inventory, backup/restore and Owner approval. |

## Anti-meta and remaining gates

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED: Korean-authored users can invoke existing V1 run/check/build/canon/help/version identities through their approved CLI spellings
NEW_PACK: 0
NEW_RUNNER: 0
NEW_TEST_ARTIFACT_COUNT: 0
NEW_INLINE_PRODUCT_TEST_COUNT: 1
META_TEST_CREATED: 0
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
```

PathIR/Proof P0 containment remains preserved. P1 remains
`PARTIAL_IMPLEMENTED_UNDER_REVIEW`: the versioned physical request/result/
receipt registry and raw-DDN checked-assumption surface are still exact
product-detail/Owner gates. No wire key, CLI assumption option or raw syntax
was invented.

No SSOT, public SPEC, visible Workbench UI, public membership, release,
activation, legal state or Human disposition changed. This handoff requests
management custody of one fixed product milestone; it does not self-declare
independent PASS, V1 closure, readiness or release.
