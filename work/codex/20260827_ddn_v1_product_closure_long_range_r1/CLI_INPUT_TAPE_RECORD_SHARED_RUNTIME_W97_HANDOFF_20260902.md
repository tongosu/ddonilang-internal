# CLI input-tape record shared-runtime W97 handoff

## Scope and authority

- Persistent goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` (`ACTIVE`, not blocked)
- Branch: `codex/ddn-v1-p1a-core-supported-ingress-w1-20260829`
- Baseline/handoff parent: `da4d956910bd67163fa15ba7b31fbc45b7c22737`
- Product/test fixed HEAD: `9334404370ccd9c1c8722e94fc5c85ee96e06f36`
- Fixed tree: `c49031bdb099c7dfd29ba456371219f6a2841ff5`
- Merge count from baseline: `0`
- Internal live CURRENT: `v25.49.0 / RD-001~543`
- Public Language SPEC: `v0.6.0`
- Successor impact: `UNAFFECTED`; v25.49 adds no product semantic change to this existing input-tape contract.
- SSOT/SPEC diff: `0 / 0`

The P5 fixed-target review remains bound in ancestry at
`bc84d81d4faa55974975bdb7ec60cb18d9a7ebda` with `PASS_TARGET_BOUND`,
blocking finding `0`, and report SHA-256
`05d9522c900d5c164064a003f92fabc100f64daf40100690b0e3c3747892a6d6`.
This milestone neither repeats nor broadens that PASS.

## User workflow changed

Before this change, the existing
`teul-cli run <source> --record-sam <path>` option was rejected at the shared
runtime with `E_SHARED_RUNTIME_OPTION_UNSUPPORTED`. It now records interactive
key masks through the CLI host adapter, constructs the versioned tape in the
shared tool authority, executes that same tape in the shared supported-profile
runtime, and atomically publishes the tape only after successful execution.
The resulting artifact can be replayed immediately through the already shared
`--sam` path with identical state and observation identities.

This is internal convergence of an existing option and tape format. It does
not decide executable/package naming, public command membership, alias duration
or any new public spelling.

## Exact product diff

From baseline `da4d9569` to fixed HEAD `93344043`:

1. `tool/src/input_tape.rs`
2. `tools/teul-cli/src/cli/run.rs`
3. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
4. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

The shared tool now owns tape construction from ordered masks, including
registry bounds and deterministic tick ordering. The teul route is an adapter
and consumer; its previous private direct `InputTape` construction is removed
from both the shared route and the retained legacy helper.

Tracked WASM custody at the fixed commit:

- binary Git blob: `f95b8b7b1a949792d88e9f959e1ee775c0e6012a`
- binary bytes/SHA-256: `5,579,269` / `46fd7b9533fd96c2c2ac569dc80bbde28aa15fd02fb65fa3ac5124934101267a`
- manifest Git blob: `ddf3c04b8e302ddcd35f972df27a5682aaa15e81`
- manifest Git-blob bytes: `28,754`
- checkout manifest SHA-256 before Git LF filtering: `e4581a1fb7014a14a3044dffb55156c29fa74495bcc71113d2bdb1b0a988d70c`
- official freshness: `PASS`

## Product evidence

- Product RED: valid `v1-core-v25` source with `--madi 1 --record-sam` returned
  `E_SHARED_RUNTIME_OPTION_UNSUPPORTED`, exit `1`, artifact absent.
- Actual CLI GREEN: `ArrowRight` was recorded into a 95-byte tape with SHA-256
  `05872dfb30edf77c8da4f972538bf0b08943384adc831ad1fb74525950f6b02c`.
- Record/replay identity: both paths produced state hash
  `blake3:d3623fcee76ad52f26063ecb2fd9fe2ef6f25a38292e07136f7d5db39365203c`
  and public-observation hash
  `sha256:04a851958dff5499b568e339226cd45642bb6e4e6f285f46bddfa5e6c3e4f1d9`.
- Repeat determinism: replay repeated twice with the exact same semantic output.
- Partial publish: a V25 legacy-definition parse failure returned exit `1` and
  preserved the pre-existing tape SHA-256 exactly; partial artifact publish `0`.
- Fail-closed options: `--sam` plus `--record-sam` gives
  `E_SAM_MODE_CONFLICT`; omitted finite `--madi` gives
  `E_SAM_RECORD_MADI_REQUIRED`; multi-artifact output gives the existing
  `E_SHARED_RUNTIME_OPTION_UNSUPPORTED` until a multi-file atomic contract exists.
- Shared tape tests: `4/4 PASS`.
- Focused teul shared-runtime test: `1/1 PASS`.
- P1-A supported-ingress runner: native `7`, native/WASM exact `2`, WASM `10`,
  official CLI positive `4`, negative `4`, all PASS.
- Tracked-WASM parity: `10/10`, deterministic repeats `4`, partial summary `0`.
- Tool lib: `606 PASS + 2 pre-existing isolated-worktree environment failures`;
  both failures are the absent `docs/ssot` input in this product worktree.
- Official WASM freshness and fixed-head CLI build: PASS.
- `git diff --check`: PASS; only the known manifest checkout LF-filter warning was emitted.

## Mutation

`RECORD_MADI_ORDER_COLLAPSED` changed every shared tape record index to zero.
The existing roundtrip test produced actual RED because `[0, 0] != [0, 1]`
(exit `101`). The source was restored byte-exactly to SHA-256
`f934d57d0036ee9ce90a71f965cf0777e8be6701872ed16a5f257f5180d77612`,
then the focused test returned GREEN. Mutation residue: `0`.

## C0-C8 actual state

| Gate | Current fixed-object disposition |
|---|---|
| C0 | Historical `28 tool + 63 teul = 91` registry custody remains; no bulk public promotion. |
| C1 | `ddn.project-run.v1` identity and executable naming remain unchanged. |
| C2 | Shared tool owns supported source, versioned input-tape decode/encode/construction, replay, seed and run identity. |
| C3 | Existing teul `run --record-sam` now reaches the shared runtime and shared tape authority; public membership is not inferred. |
| C4 | Migrated record/replay/seed routes have private parser/runtime/value/canon fallback `0`; other internal/deferred routes remain custody. |
| C5 | Bounded V1-required build/test/pack/publish teul execution dependency remains `0`; historical/internal references remain. |
| C6 | Native record/replay identity, tracked WASM freshness and supported-ingress native/WASM parity pass. |
| C7 | W90-W97 is ready as one coherent rolling-review bundle; no reviewer/task/worktree was created here. |
| C8 | Public projection continues to exclude the teul binary/package; physical deletion and final retirement remain Owner-gated. |

## Anti-meta and custody

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: interactive input recording and deterministic replay on the shared runtime
- `NEW_TEST_ARTIFACT_COUNT`: `0`
- `NEW_PACK`: `0`
- `NEW_RUNNER`: `0`
- `META_TEST_CREATED`: `0`
- Existing tests/runners reused: `6` focused/product commands plus direct record/replay/failure workflows
- New test file: `0`; one existing shared unit test was strengthened
- New review task/worktree/branch: `0 / 0 / 0`
- Protected untracked VC06/VC17/P1 custody: byte-untouched and unstaged

## Open gates and nonclaims

PathIR public registry, public test/view/repl membership, VC17 exact landing,
public executable/package naming, alias duration, legal/signing/distribution,
final teul physical deletion, P5 whole closure and P6 Human Smoke remain open
at their own slices. This handoff does not claim whole C0-C8 closure,
repository-wide teul authority/dependency zero, V1 membership/readiness,
release, activation, legal clearance, Owner Human PASS or external-user success.

Status: `CLI_INPUT_TAPE_RECORD_SHARED_RUNTIME_W97_IMPLEMENTED_UNDER_REVIEW`.
