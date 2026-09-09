# CLI explicit seed shared-runtime W96 handoff

## Scope and authority

- Persistent goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` (`ACTIVE`, not blocked)
- Branch: `codex/ddn-v1-p1a-core-supported-ingress-w1-20260829`
- Baseline/handoff parent: `dc6c44a9cd645e0ef7edaa0db62d0f9dea311dc3`
- Code/WASM commit: `fc647a273aee60c95a448961964a8dc90d3fa9f8`
- Product/test fixed HEAD: `fa649d7ec12fcac207f65b9ac2673c29101c8619`
- Fixed tree: `c94142e47d6f92d794e84850dca07d519824da2f`
- Merge count from baseline: `0`
- Internal live CURRENT: `v25.49.0 / RD-001~543`
- Public Language SPEC: `v0.6.0`
- Successor impact: `UNAFFECTED`; v25.49 adds custody correction and no new product semantics for this slice.
- SSOT/SPEC diff: `0 / 0`

The independently reviewed P5 target-bound PASS remains in ancestry at
`bc84d81d4faa55974975bdb7ec60cb18d9a7ebda` (report SHA-256
`05d9522c900d5c164064a003f92fabc100f64daf40100690b0e3c3747892a6d6`).
This milestone neither repeats nor broadens that PASS.

## User workflow changed

Before this change, the already existing command
`teul-cli run <source> --seed <u64>` reached the shared runtime ingress but a
valid V25 source failed with `E_SHARED_RUNTIME_OPTION_UNSUPPORTED`. It now sends
the explicit seed through the shared `tool::runtime_surface` authority. The
seed is sealed in the input snapshot and, when nonzero, participates in run
identity. Same source plus same seed repeats exactly; changing the seed changes
the run identity.

This is an internal convergence of an existing option. It does not decide the
public executable name, package name, command membership, alias duration, or
stable public spelling.

## Exact product diff

From `dc6c44a9` through fixed HEAD `fa649d7e`:

1. `tool/src/runtime_surface.rs`
2. `tools/teul-cli/src/cli/run.rs`
3. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
4. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

The shared runtime owns seed application, tick-seed derivation, input snapshot
and run identity. The teul path is an adapter/consumer and has no private parser
or runtime fallback on this route. Seed with model execution and seed with an
unapproved age-target combination fail closed instead of being ignored.

The final manifest-only successor records the post-format source identity; it
does not change product semantics. Final tracked WASM custody:

- binary Git blob: `003d4681ebd93e83264d227b388b60cfc428008e`
- binary bytes/SHA-256: `5,579,269` / `c3532ea9e03642c34ea9aaf99548e5d14663e3e24cf3c5bea80b63dd29d804ac`
- manifest Git blob: `d4b48c606504f02957d11946258b301dc6886e29`
- manifest Git-blob bytes: `28,754`
- checkout bytes/SHA-256 (CRLF materialization): `29,626` / `de43f9cfd543a0c1ae8b66ca1b7f7cf7675ec205cf3056391e7df334fc53cc97`
- official freshness: `PASS`

## Product evidence

- Product RED: valid `v1-core-v25` `:=`/`<-` source plus `--seed 7` returned
  `E_SHARED_RUNTIME_OPTION_UNSUPPORTED`, exit `1`.
- Actual CLI GREEN: seed 7 repeated byte-identically; summary SHA-256
  `bd5ed407812d96eab52ef6a50ae0be99f947a412b80589e9ac035bdcf0d5ab57`.
- Seed identity: seed 7 and seed 8 produced distinct run identities.
- Native/tracked-WASM applicable parity: existing
  `pack/age1_container_resource/input.ddn`, seed 7, one tick produced the exact
  state hash
  `blake3:cd91eb3ebb891c8226dd16bbbf16549f0ccf49175fb3997ffd5a15ef2fd83c1a`
  and `rng_base_seed=7` on both paths.
- Existing P1-A native/WASM runner: `10/10`, repeats `4`, partial summary `0`.
- Existing P1-A supported-ingress runner: native `7`, native/WASM exact `2`,
  WASM `10`, official CLI positive `4`, negative `4`, all PASS.
- Focused tool seed test: `1/1 PASS`.
- Focused teul adapter seed test: `1/1 PASS`.
- Tool lib: `606 PASS + 2 environment failures`; both failures are the
  pre-existing isolated-worktree absence of `docs/ssot`, not this diff.
- Full teul test attempt: environment/dependency graph compile failure
  (`E0308`, duplicate `serde_json`/`ddonirang_core` instances). The changed
  focused test and actual executable path pass; no claim of whole-suite PASS.
- `git diff --check`: PASS.

## Mutation

`RNG_SEED_RUN_IDENTITY_OMISSION` replaced the nonzero seed identity suffix with
an empty string. The focused product test RED because seed 7 and seed 8 received
the same run identity (exit `101`). The exact formatted source was restored to
SHA-256 `92a38ab2c78a801f2de2b0af0b5e74e71dfed4ed6210ed42088cd212b0040a48`,
then the focused test returned GREEN `1/1`. Mutation residue: `0`.

## C0-C8 actual state

| Gate | Current fixed-object disposition |
|---|---|
| C0 | Historical `28 tool + 63 teul = 91` identity custody remains; no bulk promotion. |
| C1 | `ddn.project-run.v1` and executable naming remain unchanged. |
| C2 | Shared tool owns supported source, input tape, and now explicit seed execution identity. |
| C3 | Existing teul `run --seed` reaches the shared runtime; no official public command membership is inferred. |
| C4 | Migrated seed and input-tape routes have private parser/runtime fallback `0`; other internal/deferred combinations remain custody. |
| C5 | Bounded V1-required build/test/pack/publish teul execution dependency remains `0`; historical/internal references remain. |
| C6 | Tracked WASM freshness, P1-A parity, and applicable seeded native/WASM state parity pass. |
| C7 | W90-W96 source is ready to be queued as one coherent rolling-review milestone; no reviewer/task/worktree was created here. |
| C8 | Public projection continues to exclude the teul binary/package; physical deletion and final retirement remain Owner-gated. |

## Anti-meta and custody

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: explicit deterministic seed execution
- `NEW_TEST_ARTIFACT_COUNT`: `0`
- `NEW_PACK`: `0`
- `NEW_RUNNER`: `0`
- `META_TEST_CREATED`: `0`
- Existing tests/runners reused: `7` commands plus direct native/WASM product execution
- New test code: one focused tool test added and one existing teul test replaced in already-owned product files
- New review task/worktree/branch: `0 / 0 / 0`
- Protected untracked VC06/VC17/P1 census custody: byte-untouched and unstaged

## Open gates and nonclaims

PathIR public registry, public test/view/repl membership, VC17 exact landing,
public executable/package naming, legacy alias duration, legal/signing/
distribution, final teul physical deletion, P5 whole closure and P6 Human Smoke
remain open at their own slices. This handoff does not claim whole C0-C8
closure, repository-wide teul authority/dependency zero, V1 membership or
readiness, release, activation, legal clearance, Owner Human PASS, or external
user success.

Status: `CLI_EXPLICIT_SEED_SHARED_RUNTIME_W96_IMPLEMENTED_UNDER_REVIEW`.
