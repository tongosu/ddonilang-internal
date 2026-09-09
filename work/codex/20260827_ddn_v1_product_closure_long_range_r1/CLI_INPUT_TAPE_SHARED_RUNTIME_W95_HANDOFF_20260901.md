# [DDN V1제품마감Codex -> Codex관리Work] CLI INPUT TAPE SHARED RUNTIME W95 — handoff

## Fixed identity and authority

- baseline/handoff parent: `33813e6787eb3a055fc8b8b63a29695a002396a4`
- product/test fixed: `c3d69da0061e2d1c4e20efd8a41b7c05bc26e360`
- fixed tree: `4129174c29e1fdd551b8a905e370696214c599c9`
- direct parent: exact
- merge count: 0
- branch: `codex/ddn-v1-p1a-core-supported-ingress-w1-20260829`

Live authority was verified read-only as internal SSOT v25.49.0 / RD-001~543
and public Language SPEC v0.6.0. Successor impact is `UNAFFECTED`: the change
reuses the existing versioned input-tape format, supported source-profile
authority and runtime input snapshot. It introduces no language meaning,
public command membership, executable/package name, wire spelling, SSOT or
SPEC transition.

Review commits `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf` and
`bc84d81d4faa55974975bdb7ec60cb18d9a7ebda` are verified ancestors of the
fixed target. Their target-bound PASS scopes remain unchanged.

## Product behavior and exact paths

The existing `teul-cli run --sam <versioned-input-tape>` user workflow now
decodes the tape through the shared `tool::input_tape` owner and executes it
through the shared `runtime_surface`/`DdnRunner`. The tape key registry is
converted once to the historical core key-mask identity, record order/count
and `madi_hz` are checked before execution, the exact encoded tape is included
in sealed-input accounting and run identity, and no teul-private parser or
runtime fallback is used for this route.

Exact fixed paths:

- `tool/src/input_tape.rs`
- `tool/src/lib.rs`
- `tool/src/runtime_surface.rs`
- `tools/teul-cli/src/cli/run.rs`
- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

Tracked WASM is 5,578,873 bytes, SHA-256
`78b9cda28e43a459c0175a725fbe89b5c71f8d977888cb649e975807921fe957`.
The manifest is 29,626 bytes, SHA-256
`1e07119325b198cfd67bb9998723be79177a74594c3f1bf0fe98346bfec420c8`.
No new pack, runner, public option, or test framework was created.

## RED, GREEN, determinism and mutation

- product RED: the same `run --sam` request previously stopped at
  `E_SHARED_RUNTIME_OPTION_UNSUPPORTED` before shared execution.
- actual V25 CLI GREEN: existing positive supported-ingress source plus the
  existing `input_key_alias_ko_v2` versioned tape exited 0 and emitted `2`.
- focused shared input-tape tests: 6/6 PASS.
- focused teul adapter/frontdoor test: 1/1 PASS; mismatched 30 Hz request
  returned `E_SAM_MADI_HZ_MISMATCH` with output publish 0.
- supported-ingress native/WASM suite: native 7, native/WASM exact 2,
  tracked-WASM 10, deterministic repeats 4, partial summary 0, PASS.
- tracked-WASM freshness: PASS after official rebuild and manifest refresh.
- fixed-head repeat: identical semantic request/tape returns identical full
  structured summary and run identity; changed tape changes run identity.

Risk mutation `INPUT_TAPE_RIGHT_KEY_MISROUTED` changed the tape registry's
ArrowRight mapping from core `KEY_D` to `KEY_A`. The exact product test went
RED (`left=2`, `right=8`). It was restored byte-exact to
`tool/src/input_tape.rs` SHA-256
`7b5c58354facbdf155f1fa74f7fecf75d8f2d3b847025ea85f1212487a90ade0`,
then the focused suite returned 6/6 GREEN. Mutation residue is 0.

Proportional whole-suite custody:

- `ddonirang-tool --lib`: 605 PASS + 2 environment failures because this
  isolated product worktree intentionally has no `docs/ssot` materialization;
  both failures are in `ai_prompt` and unrelated to the six changed paths.
- `teul-cli --bin`: 1025 PASS + 9 pre-existing semantic/baseline failures in
  untouched canon/frontdoor/right-assignment paths; no W95 focused failure.
- historical W17 now reaches shared canonicalization instead of the option
  guard, but its pre-V25 source fails `E_SHARED_CANONICAL`; it remains
  `REBASE_REQUIRED_SOURCE_EPOCH`, not a W95 product failure and not promoted.

## C0-C8 actual state

| Gate | Actual state after W95 |
|---|---|
| C0 | Historical 28 tool + 63 teul = 91 identity custody remains; no bulk promotion. |
| C1 | `ddn.project-run.v1` and executable naming remain unchanged. |
| C2 | Versioned input-tape decode/key mapping/run binding now has one shared tool authority available to native and wasm32 builds. |
| C3 | Existing teul `run --sam` adapter reaches the shared runtime; adding an official public CLI option remains a separate membership/spelling gate. |
| C4 | This migrated route has private parser/runtime fallback 0. Legacy record/live/net/geoul combinations remain internal/deferred teul custody. |
| C5 | Bounded V1 required build/test/pack/publish teul execution dependency remains 0; historical/internal references remain custody. |
| C6 | wasm32 build, tracked freshness and supported-profile native/WASM parity PASS; no unapproved input-tape WASM wire was invented. |
| C7 | W90-W95 successor source is ready for one coherent rolling review; no new reviewer/task/worktree was created. |
| C8 | Public projection continues to exclude teul binary/package; physical deletion and final retirement remain Owner-gated. |

## Anti-meta, review and nonclaims

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED: versioned input-tape replay executes on the shared supported runtime instead of the teul-private runtime.
REUSED_TEST_COUNT: 6 focused Rust + 1 teul frontdoor + existing supported-ingress native/WASM suites + freshness + actual CLI
NEW_TEST_ARTIFACT_COUNT: 0
META_TEST_CREATED: 0
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
ACTIVE_REVIEW_TASK_COUNT: 0
REVIEW_BUNDLE_TARGET: W90-W95 CLI authority convergence and release-custody successor source
```

Public test/view/repl membership, official input-tape option spelling,
PathIR public registry, VC17 exact landing, legal/signing/distribution and
physical `tools/teul-cli` deletion remain slice-local gates. This handoff does
not claim whole C0-C8 closure, repository-wide teul authority/dependency 0,
P0-P6 closure, V1 readiness/release, activation, Owner Human Smoke or Human
PASS.
