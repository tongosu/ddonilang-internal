# CLI retained Gaji plan shared authority W120 handoff

## Scope and authority

- `AI_PROVIDER`: OpenAI
- `AI_SURFACE`: Codex Work
- `PROJECT_ROLE`: DDN V1 closure single writer
- `CURRENT_AUTHORITY`: internal SSOT v25.50.0 / RD-001~551; public Language SPEC v0.6.0 (read-only)
- `BASE`: `8fb1e15a7fb55c76069ccede927b94f914ab35be`
- `PRODUCT_FIXED`: `c3e56f62c53114c7afe2ab14bb952aa248fd9615`
- `PRODUCT_TREE`: `6d46e50a45ccbce0744d87df8f9a8f415442d2ca`
- `DIRECT_PARENT`: `8fb1e15a7fb55c76069ccede927b94f914ab35be`
- `MERGE_COUNT`: 0

This is an internal retained/deferred CLI convergence slice. It neither decides public command membership nor executable/package spelling or legacy alias retention.

## User workflow changed

`teul-cli gaji plan` and `teul-cli gaji lifecycle-plan` now call one shared native tool authority for request read, local-project planning, stdout emission, and atomic `--out` publication. The retained CLI is only an adapter. Existing JSON payloads and existing diagnostic strings remain unchanged.

Changed product paths:

- `tool/src/gaji_plan_workflow.rs` (new shared owner)
- `tool/src/lib.rs` (native-only module export)
- `tools/teul-cli/src/main.rs` (two adapter arms)

No `docs/ssot/**`, `publish/spec/**`, tracked WASM, public UI, dependency, pack, or new runner change is included.

## Evidence

- Actual retained CLI RED before implementation: `gaji plan --input pack/gaji_creator_wave1/g2_extraction_request.detjson` exited 1 with `E_GAJI_PLAN_SHARED_AUTHORITY_UNIMPLEMENTED`.
- Same actual CLI GREEN after implementation: exit 0 and canonical `ddn.gaji_extraction_plan.v1` JSON output.
- Existing `node tests/gaji_creator_wasm_parity_runner.mjs` was reused for extraction/lifecycle native-to-tracked-WASM payload and nested atomic-output parity; it completed without an assertion failure.
- Existing focused command: `cargo test --offline --manifest-path tool/Cargo.toml local_project::tests -- --nocapture` passed 40/40.
- Mutation: replaced extraction planner with lifecycle planner in the new shared owner. The actual extraction request exited 1 with `E_GAJI_LIFECYCLE_JSON` and the schema-field mismatch. The exact source SHA-256 before and after restore was `c2e16f40df12012553469c557a03cd1a765890e5bf49163dbf32dbce767b338f`; restored direct CLI exit 0.
- `git diff --check`: PASS before commit.

## C0-C8 narrow update

- C0: historical 91-command inventory remains custody only (tool 28 / teul 63).
- C1: shared owners remain the V1-core requirement; no membership promotion.
- C2: `gaji plan` and `gaji lifecycle-plan` now have shared request/read/plan/output authority.
- C3: public executable and command membership remain undecided.
- C4: private parser/runtime/value/canon authority is reduced only for these two adapter arms; broader teul residue remains.
- C5: this slice adds no build/test/pack/publish dependency; bounded V1-required dependency classification remains separate.
- C6: existing native/WASM/project-run parity runner is reused; no new parity framework.
- C7: no release/WASM materialization claim.
- C8: no physical teul directory, binary, or package retirement.

## Nonclaims and next gate

`V1_CLI_CONVERGENCE_REQUIRED` remains open; this does not close P0-P6, V1 membership/readiness, release, activation, Human Smoke/Human PASS, rights attribution, publication, or distribution. PathIR/Proof P0 containment remains preserved and its public structured P1 ingress stays owner-contract gated.

No reviewer was created or dispatched. The next coherent CLI slice must remain within existing physical contracts and resolve another real private semantic or required-dependency path without selecting public naming or deletion semantics.
