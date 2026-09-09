# P4 shared host-resource contract V1 — product handoff

## Fixed target

- Product fixed commit: `8c730857b7590c14c19c5b8889824d37a3af6580`
- Direct parent: `c796d45344e521d2c4d50220a1e28909552537bc`
- Product fixed tree: `55f156aa77de12ce10e1540d5f7b3d9cfc57e0c1`
- Merge count: `0`
- Live authority read-only at implementation handoff: internal SSOT `v25.53.0 / RD-001~553`; public Language SPEC `v0.6.0`.
- Successor impact: `ADDITIVE_OUT_OF_SCOPE` for the relation-surface/LanguageProfile SSOT delta; no host-resource semantic contradiction found. This product target does not promote CURRENT, membership, readiness, or release.

## Product behavior

`ddonirang-tool` now owns the declared-host-resource request, transcript, receipt, record preflight, and replay validation through `tool/src/host_resource.rs`.

- Record accepts only declared UTF-8 regular files; relative locators reject parent/root/prefix/current-directory traversal, URI-looking locators, glob-like locators, symlinks/reparse points, and non-regular files.
- The semantic transcript/receipt contains logical resource ID, SHA-256, byte length, media type, and sealed UTF-8 text. Host locator is omitted.
- Record reads each declared file once after manifest validation. Any preflight failure occurs before runtime invocation and before CLI result or project artifact publication.
- Replay consumes a sealed transcript or bundle and has no declared resource locator. Duplicate IDs, payload hash/length drift, transcript-order identity drift, malformed schema, and bundle receipt mismatch fail closed.
- Official `ddonirang run` and `project-run` share the same `PreparedHostResources` invocation object. The Local Project summary rebinding includes transcript/receipt and changes its summary identity only for this explicit host-resource path.
- Native CLI supports `--open deny|record|replay`, `--open-log`, `--open-bundle`, and `--open-resources`; omitted `--open` remains deny. `--unsafe-open` is not recognized.
- WASM exposes typed request consumers for ordinary run and Local Project. No Workbench UI, CLI subprocess adapter, tracked WASM refresh, or visible UI surface was changed.

## Changed product paths

- `tool/src/host_resource.rs`
- `tool/src/lib.rs`
- `tool/src/runtime_surface.rs`
- `tool/src/local_project.rs`
- `tool/src/wasm_api.rs`
- `tool/src/bin/ddonirang.rs`

`tools/teul-cli/**`, tracked WASM, UI, `docs/ssot/**`, and `publish/spec/**` diff: `0`.

## Focused evidence

- `cargo check -p ddonirang-tool`: PASS (pre-existing warnings only).
- `host_resource` unit tests: `3/3` PASS — locator-free record/replay identity, duplicate/hash tamper rejection, order-identity rejection.
- Local Project supported-profile preflight/binding test: `1/1` PASS — receipt bound and malformed declaration stops before project run.
- Official CLI product path: `1/1` PASS — `run --open record --open-log --open-resources`, delete only the test-owned declared input, then `run --open replay --open-log` produces identical structured output.
- WASM feature test: `1/1` PASS — Native/WASM full structured payload equality for record and replay requests.
- Mutation: disabled transcript-order identity comparison produced RED in `replay_rejects_order_identity_tamper`; exact source restore then GREEN, residue `0`.
- `git diff --check`: PASS.

## Review and remaining gates

This is a coherent P4 product milestone, not VE03 or P4 closure. It is ready to be bundled for the existing rolling reviewer when management chooses a compatible fixed target. Do not create a new reviewer/worktree.

Open: tracked-WASM artifact refresh/freshness at the future fixed target, existing RuntimeBridge/Workbench structured-consumer landing without UI semantic duplication, applicable Native/Local Project/WASM/Workbench fixed-target parity, independent review, and P4/P5/P6 release gates.

Nonclaims: V1 readiness, membership, release, publication, activation, legal clearance, and Owner Human PASS remain open.
