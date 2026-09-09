# CLI tool shared-runtime authority W113 handoff

## Fixed lineage

- W112 handoff predecessor: `393c4a43c8b903be452885c200c259e723d22085`
- Product fixed: `32b6c48cb609638dfeb1c4ae8446268effa7a468`
- Direct parent: `393c4a43c8b903be452885c200c259e723d22085`
- Fixed tree: `332390191069276a569dd2b7a736363148230535`

## Product value

The native `ddonirang-tool` binary no longer compiles a binary-local copy of
`ddn_runtime`.  It now consumes the existing `ddonirang_tool::ddn_runtime`
module, so parser mode, source execution, keyboard alias state, and runtime
failure behavior have one tool authority rather than a second binary-local
semantic copy.

## Exact product change

`tool/src/main.rs` removes local declarations for `ddn_runtime` and the three
modules that were only present to satisfy that local copy.  It imports the
already-public library runtime API instead.  No runtime implementation body,
command name, public executable/package name, legacy alias, `teul-cli` source,
WASM artifact, visible UI, SSOT, public SPEC, or external dependency changed.

## Verification

- Native binary compile: PASS.
- Existing binary test target: 106 passed, 0 failed.
- Shared library V25 runtime tests: 2 passed, 0 failed.
- Shared keyboard alias runtime test: 1 passed, 0 failed.
- Mutation: remove the shared library runtime import -> compile RED exit 101
  (14 unresolved runtime uses) -> exact restore -> compile GREEN.
- Restored product source SHA-256:
  `a4118c966b489ed105e9559053f04bb6a069e8d107fc6ae7be51703858751b32`.
- Product compile and tests use existing packages and runners only; new pack,
  runner, dependency, and meta-test are all 0.

## Scope boundary

This is a bounded C2/C4 CLI convergence improvement.  It does not establish
complete command parity, Windows release readiness, teul physical retirement,
public command membership, or any release/rights/Human PASS state.  Legacy
`build-schema` policy resolution remains a separate physical-contract issue:
the current project policy asks for an unavailable v20.12 SSOT bundle and
fails closed before input processing.

No independent review task was created.  This fixed target is queued to the
existing rolling reviewer only with the next coherent CLI milestone.
