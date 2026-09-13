# SOURCE_COORD tracked-WASM refresh W91 handoff

## Lineage and scope

- W90 implementation fixed: `bfe1b67d917751c0e0107d202c5678c51f7388bd`
- W90 handoff parent: `a7cd7fb89c2e6d4e4b6cd04148a9324f170f169c`
- W91 tracked-WASM fixed: `36485ba42d4782f1551c018daeabad4e58d04be8`
- W91 tree: `b6bb3ce172352fcb9951069357fb8d63c6554880`
- W91 direct parent: `a7cd7fb89c2e6d4e4b6cd04148a9324f170f169c`
- merge count: 0

Exact W91 product paths:

- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

No JS, declaration, package, product source, test, pack, visible UI, SSOT, or
public SPEC path changed in W91.

## Reproduction and parity

- official release/web WASM build: PASS.
- second official build without tracked copy: PASS.
- tracked/rebuilt raw WASM SHA-256 equality: PASS.
- tracked WASM: 5,575,625 bytes,
  `1f7b61c55f799f69b8918f27914db260f62a5efd54acc7b811df0a00c150726e`.
- manifest SHA-256:
  `c72fb8ee6ac528362622d311bbf7cb443739b3442949dc7e5c3fce6cbbb16d4`.
- source inventory: 152 files; source tree
  `86a53fc55be761504eaa03990b8a84d20982c3ae7d7adc72bb8b922686d5fd47`.
- official freshness: PASS.
- tracked-WASM project-authoring snapshot from Korean raw source with a
  non-BMP string prefix reported `이름` at UTF-16 column 12, exactly the
  independently calculated expected column 12; snapshot identity
  `56566eaa50d5a3f6903bb02e67504418a8533beb263dda5a6321ba1f970398d8`.
- native focused LSP and project-authoring results remain W90 GREEN.
- partial result/state publish: 0 (read-only authoring snapshot workflow).

## Gate effect and anti-meta

- C6 delta: the W90 source-coordinate authority is now present in the tracked
  WASM family and freshness is GREEN.
- other C0~C8 rows: unchanged.
- user workflow unblocked: Korean project authoring after non-BMP text now has
  the same UTF-16 coordinate rule in native LSP, Workbench Rust authoring, and
  tracked WASM projection.
- reused test/build gates: 5 (official build twice, freshness, native LSP,
  project-authoring coordinate test).
- new test artifact/pack/runner/meta-test/reviewer/worktree: 0.

Status is `SOURCE_COORD_NATIVE_WASM_WORKBENCH_AUTHORITY_IMPLEMENTED_UNDER_REVIEW`.
This does not claim a stable public coordinate wire, whole C0~C8, PathIR public
closure, VC17 exact landing, teul physical retirement, P5/P6 closure, V1
membership/readiness/release, activation, legal approval, Owner Human Smoke, or
Human PASS. Existing fixed-target review PASS remains scoped to its exact
historical target and is not auto-inherited by W90/W91.
