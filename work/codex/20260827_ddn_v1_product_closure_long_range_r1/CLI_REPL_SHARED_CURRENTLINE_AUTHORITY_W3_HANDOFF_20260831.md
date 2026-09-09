# CLI REPL shared currentline authority W3 handoff

## Identity

- persistent goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` (active; not replaced or completed)
- live authority observed read-only: internal SSOT `v25.45.0 / RD-001~536`
- public Language SPEC: `v0.6.0`
- predecessor handoff: `d1080556b1deeeb93df90fc222dabc6f1a6e1f76`
- predecessor review already bound in lineage: `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf`
- predecessor review report: 9,108 bytes / SHA-256 `b9de1396842326cf6e974574d58486272da17db9ac9916a43d417bc73e0f4d34`
- product fixed: `245ff6040e34f015179cf6d0096ebca7b09f8ebb`
- product fixed tree: `65d8870ef57d53b035bca7931cec6b30abfedece`
- tracked-WASM refresh fixed: `45376a9695817e50d44cae0401cb61342635d099`
- tracked-WASM refresh tree: `2605f553e342252367b0830869eb0ec76e477814`
- merge count: 0

## User workflow changed or unblocked

The retained `teul-cli repl` adapter now requires an explicit supported source profile and consumes the shared `ddonirang_tool::currentline_workflow` authority. A user can enter `x <- 15.`, then `y <- x + 8.`, then `x 보여주기.` in one session and observe `15` while retaining shared context and shared state identity. An invalid V25 cell fails closed without publishing its context, and the session remains usable.

This is an internal convergence of a retained command. It does not decide public command membership, executable naming, package naming, or legacy alias duration.

## Product diff

Product fixed, exact three paths:

- `lang/src/currentline.rs`
- `tools/teul-cli/src/cli/repl.rs`
- `tools/teul-cli/src/main.rs`

Tracked-WASM refresh, exact two paths:

- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

`tools/teul-cli/src/cli/repl.rs` no longer imports or invokes the private teul parser/runtime/state/hash path. Missing `--source-profile` is rejected with existing profile-boundary custody rather than silently selecting a profile. Unknown V25 currentline statements now fail closed; legacy currentline custody remains unchanged.

## RED, mutation, and restore

- Product RED: the retained REPL used the private teul parser/runtime/state/hash authority and rejected the approved shared-currentline workflow.
- Product RED: explicit `v1-core-v25` currentline silently accepted unsupported `z = 1.` and published it into context.
- GREEN: the shared currentline authority executes the supported binding/show workflow and rejects the unsupported statement without changing context.
- Risk mutation: the missing-profile fail-closed branch was changed temporarily to a hidden `v1-core-v25` default. Invocation incorrectly succeeded (RED), then the exact bytes were restored.
- Restored `tools/teul-cli/src/main.rs` SHA-256: `46c8025c86fd085399dedac6869510aa7f60fce26ef73b3b589bbf3bde20e7bf`.
- Final focused GREEN: PASS; mutation residue 0.

## Tests and parity

- lang V25 unknown-statement focused test: 1/1 PASS
- lang currentline tests: 6/6 PASS
- retained REPL shared-authority test: 1/1 PASS
- tool library regression: 536/536 PASS
- direct scripted REPL supported workflow: exit 0; output `15`; deterministic shared state hashes observed
- invalid-cell workflow: existing error returned, prior context preserved, subsequent observation still `15`
- missing profile: exit 2 and fail-closed
- supported-ingress tracked-WASM parity: 10/10 PASS; deterministic repeats 4; partial summary 0
- post-WASM shared-changes gate: PASS
- official tracked-WASM freshness: PASS
- current teul binary suite: 1046 PASS + 9 FAIL
- immutable predecessor materialization: 1045 PASS + the same 9 FAIL
- new regression failures: 0

The nine inherited failures are the same legacy `보임 {}` / right-assignment contract drift at the predecessor and fixed target. They are not promoted to PASS and are not caused by this vertical.

## Tracked WASM identity

- `ddonirang_tool_bg.wasm`: 5,568,437 bytes / SHA-256 `2b16ea041317b835bcf5a1574dd12e0427b5ce221005da733a7b63f8b800c9f6`
- `ddonirang_tool.manifest.detjson`: 21,217 bytes / SHA-256 `1c65626924e0f88f189739d82c9023140142c20ae5f292763e917325b2b022dd`
- JS, DTS, and package candidate bytes were unchanged.

## Authority and dependency disposition

- REPL private parser/runtime/value/state/hash semantic authority: removed for this command.
- hidden PreV25 retry/fallback: 0 in this vertical.
- hidden profile default: 0.
- Python/JS semantic lowering: 0.
- new pack: 0.
- new runner: 0.
- meta-test: 0.
- visible Workbench copy/layout/UI change: 0.
- Workbench-specific REPL surface: not created; applicable shared currentline/WASM product authority was validated.

## Review bundle

Ready to add this retained-REPL vertical to the next coherent CLI/teul convergence review bundle using the existing rolling reviewer only. No reviewer, review worktree, task, branch, or goal was created or dispatched here.

## Open gates and nonclaims

- `view` remains frozen on unresolved public projection/codec/transport details.
- public `test`/`repl`/`view` membership remains Owner-gated.
- exact public executable/package naming and legacy alias period remain open.
- internal/deferred physical custody remains open.
- the inherited nine teul regression failures remain open contract drift.
- whole teul physical deletion/retirement remains prohibited pending dependency 0, parity, clean projection, independent PASS, deletion inventory, backup/restore evidence, and Owner deletion approval.

This handoff does not claim whole CLI convergence, whole teul retirement, P0~P6 closure, V1 membership/readiness, release, activation, legal approval, Owner Human Smoke PASS, or Human PASS.

