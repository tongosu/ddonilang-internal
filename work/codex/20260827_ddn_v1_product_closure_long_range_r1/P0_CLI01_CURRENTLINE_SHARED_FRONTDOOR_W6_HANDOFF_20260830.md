# P0 CLI01 currentline shared frontdoor W6 handoff

Date: 2026-08-30
Session: DDN V1제품마감Codex
Persistent goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1`

## Status and fixed identities

```text
STATUS: IMPLEMENTED_UNDER_REVIEW
CURRENT_AUTHORITY: internal v25.40.0 / RD-001~515
PUBLIC_SPEC: v0.6.0
WORKTREE: I:/home/urihanl/ddn/codex/build/worktrees/ddn-p-v1-project-ux-r2-census-r1-20260828
BRANCH: codex/ddn-v1-p1a-core-supported-ingress-w1-20260829
BASELINE: 38a9f97b96cab41bc1061bcad6e4272eca51f6ab
PRODUCT_TEST_FIXED: 7ddae25dafa4cb92dbb23638133c0e26101b61bd
FIXED_TREE: 48524cae8d41be1a917ea1a94c04d346e63d98e6
MERGE_COUNT: 0
```

The live pointer/index state was read-only revalidated. v25.40 is additive for
this vertical and does not promote product membership, readiness or the public
SPEC. `docs/ssot/**` and `publish/spec/**` were not modified.

## User workflow changed

Before this vertical, the candidate `ddonirang` frontdoor rejected
`currentline-run` with `E_CLI_COMMAND_UNKNOWN` and exit 2. It now accepts an
explicit `--source-profile v1-core-v25`, consumes one raw Korean currentline
cell plus an optional prior context, runs through the shared typed V25
`DdnProgram` authority, prints the product output and atomically materializes
the next context and structured summary when requested.

The legacy `apply_currentline_cell` output remains byte-compatible for existing
internal callers. The new candidate path uses `apply_currentline_cell_v25` and
the same supported-profile resolver as native execution. Missing and unknown
profiles fail closed; there is no hidden PreV25 retry, global default switch,
second parser or test-only lowering.

The tracked WASM family exposes the corresponding explicit-profile candidate
entry and the existing wrapper consumes it. This is internal candidate custody,
not stable public command/API membership.

## Exact product/test diff

```text
lang/src/currentline.rs
lang/src/lib.rs
tool/src/bin/ddonirang.rs
tool/src/wasm_api.rs
solutions/seamgrim_ui_mvp/ui/wasm_ddn_wrapper.js
tests/seamgrim_wasm_cli_runtime_parity_runner.mjs
solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm
solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson
solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.js
solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.d.ts
```

No new pack, runner, checker, meta-test, branch, worktree or reviewer was
created. Two already tracked currentline fixture sources and the existing
native/WASM parity runner were reused.

Tracked WASM identities at the fixed head:

```text
ddonirang_tool_bg.wasm: 5,565,352 bytes / sha256 0bf10b01ddcce821f7c8edc419703e638108f65c564cdefc46a89d07ad57ef55
ddonirang_tool.manifest.detjson: 19,717 bytes / sha256 6973b2d9096cd0db77fa75fe55db590cc8a4d76aa53b77531832a2f402fab513
ddonirang_tool.js: 92,069 bytes / sha256 948db0355f34fdd422a5f18f0ebad6de4368bfa1e62c823cc8cf7438efdc8f71
ddonirang_tool.d.ts: 17,244 bytes / sha256 2d21fa96da2874076159a616b58f5603fec9175120f13f557c1f444a05823ae4
```

## RED, GREEN and failure custody

- Product RED: candidate `currentline-run` was unknown, exit 2.
- Authority RED: legacy-generated currentline source failed V25 parsing at
  `:=`; the correction routes only the explicit candidate through typed V25.
- Freshness RED: the source tree/build-script identity changed before tracked
  WASM refresh; the official freshness checker then passed after the owned
  family refresh.
- Candidate direct positive cases: existing c01 printed `콘솔 보개 예제`,
  `23`, `15`, `8`; existing c06 printed `참`.
- Missing profile: `E_SOURCE_PROFILE_REQUIRED`, exit 2.
- Unknown profile: `E_SOURCE_PROFILE_UNSUPPORTED`.
- Invalid context: `E_CURRENTLINE_CONTEXT_JSON`, outputs published 0.
- Missing second output parent: `E_CURRENTLINE_OUTPUT_PARENT`; an existing
  summary sentinel remained byte-identical and sidecar residue was 0.
- Three identical runs produced one state hash, one summary hash and one
  context hash.

The historical teul currentline execution still fails before product output at
`E_SHARED_RUNTIME_OPTION_UNSUPPORTED`. It is classified as remaining private
runtime/adapter drift, not as migrated authority or parity evidence.

## Verification

```text
cargo test --manifest-path tool/Cargo.toml --bin ddonirang: 6/6 PASS
cargo test --manifest-path lang/Cargo.toml currentline: 5/5 PASS
cargo test --manifest-path lang/Cargo.toml --lib: 366/366 PASS
cargo test --manifest-path tool/Cargo.toml --lib: 527/527 PASS
official tracked-WASM freshness: PASS
existing native/WASM currentline parity: 2/2 PASS
  state hash exact: 2/2
  final row exact: 2/2
  full value_json exact: 2/2
  output log exact: 2/2
explicit profile WASM smoke: legacy/raw and v1 candidate state hash equal;
  omitted/unknown profile fail closed
generated JS and wrapper syntax: PASS
git diff --check: PASS
```

The currentline WASM state API does not expose the native execution envelope;
that non-exposed field was not silently synthesized or claimed as exact parity.

## C0~C8 actual status after W6

```text
C0: 91-command historical registry custody confirmed (tool 28 + teul 63).
C1: V1 core 15 semantic owners audited; convergence remains partial.
C2: candidate ddonirang reaches 10/15 core command workflows.
C3: currentline-run moved to shared lang/tool frontdoor; check/build teul adapters
    and prior candidate migrations remain in lineage.
C4: teul private parser/runtime/value/canon/fallback residues remain nonzero.
C5: V1 build/test/pack/publish required-dependency-zero classification OPEN.
C6: currentline native/WASM state/result parity PASS as scoped; whole CLI parity OPEN.
C7: tracked WASM freshness PASS for this slice; clean Windows/public projection
    must be rebound at the final coherent CLI milestone.
C8: teul public binary/package retirement and physical deletion remain OPEN.
```

The 15 custody commands are:

```text
run, check, build, canon, project-normalize, project-discover, project-graph,
project-symbols, project-lock, project-run, view, currentline-run, test, lint, repl
```

Reached on the candidate frontdoor: run, check, build, canon,
project-normalize, project-discover, project-graph, project-symbols,
project-lock and currentline-run. The remaining five require product/schema,
visible UI, command-membership or private semantic convergence and were not
guessed in this vertical.

## Remaining teul dependency and custody

The bounded repository scan still finds explicit teul references in 190 test
files, 367 pack files, 50 publish files (0 under `publish/v1/**`) and two
CI/script files. These are reference-custody counts, not a claim that every
reference is V1-required. The V1-required dependency-zero classification and
removal remain open until each reachable workflow is rebound or explicitly
deferred.

Known private source custody remains nonzero (prior bounded inventory: parser
7 files, runtime 7 files, core/value 11 files), along with private CLI dispatch
and internal/deferred command implementations. The 63 teul commands are not
promoted to public API and the internal/deferred subset is neither deleted nor
rearranged here.

## Gates and next safe work

`project-run` still needs exact artifact/wire/executable-neutral identity;
`view` needs a separately approved visible frontdoor; `test` risks becoming a
harness launcher rather than a product command; `lint` and `repl` retain
private parser/runtime meaning. These are `CONCRETE_DETAIL_GAP_DETECTED` or
semantic convergence gates, not permission to invent behavior.

The next safe coherent milestone is a bounded required-dependency audit of the
five remaining workflows followed by the first workflow whose existing shared
product authority and public behavior are already exact. It must reuse current
tests, create no new evidence family, and join this W6 result in one rolling
review milestone rather than dispatching a micro-review.

## Nonclaims

This handoff does not claim whole CLI convergence, teul semantic authority 0,
required dependency 0, public executable or command membership, teul binary or
package retirement, deletion approval, independent PASS, P0~P6 closure, V1
readiness, release, activation, legal clearance or Human PASS.
