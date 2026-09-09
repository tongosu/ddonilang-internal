# CLI certificate shared authority W74 handoff

## Status and product value

- status: `CLI_CERTIFICATE_SHARED_AUTHORITY_W74_IMPLEMENTED_UNDER_REVIEW`
- user workflow: certificate key generation, deterministic signing, signature verification, and proof-certificate verification now resolve through one shared `ddonirang-tool` product authority instead of a private `teul-cli` implementation.
- V1 value: one private teul semantic owner was removed while retaining the existing CLI adapter and physical teul custody.
- goal: existing `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1`, ACTIVE and not blocked as a whole.

## Authority and exact lineage

- internal CURRENT: v25.47.0 / RD-001~543, read-only
- public Language SPEC: v0.6.0, read-only
- branch: `codex/ddn-v1-p1a-core-supported-ingress-w1-20260829`
- baseline: `5033fb9eb7fad7a40bac987d1b8dcd88e0ce0df7`
- product fixed: `146ac3d46b536967e4c34e02f67bcd54263690a4`
- product fixed tree: `cf1e7dfd6c5a6c4eab38fa085d539a978017d6df`
- direct lineage: yes
- merge count: 0
- previously bound review custody remains in ancestry: `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf` and P5 `bc84d81d4faa55974975bdb7ec60cb18d9a7ebda`; neither is broadened by W74.

Exact product paths:

- `tool/src/cert_workflow.rs`
  - shared authority functions: 8
  - Git blob: `6d873fe1ce6407cd3a29feae6d2fac1a4736a6d1`
  - Git bytes: 18,720
- `tool/src/lib.rs`
  - adds the non-WASM shared module export
  - Git blob: `9f5a4089f741569714bddf618501d1a0fd5201ca`
- `tools/teul-cli/src/cli/cert.rs`
  - retained adapter only; private authority functions: 0
  - Git blob: `b847e4d07c0a0f93ccae6a42a8ae69672ec91386`
  - Git bytes: 114

## Implementation boundary

The existing certificate implementation moved byte-for-semantics into `ddonirang_tool::cert_workflow`. The retained CLI module re-exports that authority. The only dependency adjustment replaces CLI-local artifact/hash references with the existing shared `tool` authorities.

Unchanged:

- certificate, proof-certificate and report schemas and field spellings
- command/option spelling, executable/package name, exit behavior and stdout contract
- signing, verification and deterministic seed behavior
- public command membership and legacy alias duration
- docs/ssot, public SPEC, tracked WASM and visible UI

The shared module is host-only because this exact workflow owns filesystem, process and artifact publication behavior. No WASM export or public API is inferred.

## RED, GREEN, and regression evidence

Baseline authority inventory:

- private `teul-cli` certificate functions: 8
- shared `tool` certificate module: absent

Fixed authority inventory:

- private `teul-cli` certificate functions: 0
- shared `tool` certificate functions: 8
- existing CLI call sites continue through the retained adapter

Fixed-head validation:

- `cargo check -p ddonirang-tool --lib`: PASS
- `cargo check --manifest-path tools/teul-cli/Cargo.toml --bin teul-cli`: PASS
- existing W95 certificate product pack: 2/2 PASS
  - key generation and deterministic double-sign exercised
  - valid signature accepted and tampered signature rejected
- W73 evolving-universe complete output/stdout repeat after migration: byte-exact PASS

The historical proof-certificate bundle selftest was also attempted. Its prerequisite legacy `teul-cli run` stopped before certificate verification with `E_SHARED_RUNTIME_OPTION_UNSUPPORTED`. This is the pre-existing required-dependency migration boundary and is not reported PASS or hidden as W74 evidence.

Risk mutation: reintroduce one private public certificate function into the retained adapter.

- RED: private authority count 1
- exact restore: adapter checkout SHA-256 `720250bf34faf94a9201c7249b3c56a26d61fbdd2f629fbce120086b3c274db7`
- GREEN: private authority count 0; W95 2/2 PASS
- residue: 0

## Anti-meta, C0~C8, and review

- `NEW_PACK`: 0
- `NEW_RUNNER`: 0
- `META_TEST_CREATED`: 0
- existing test/corpus families reused: 3 (tool compile, teul compile, W95; W73 actual workflow was also replayed)
- C2: certificate/proof-certificate private teul semantic authority removed for this seam
- C4: retained adapter consumes shared product authority; private fallback 0
- C5: no new V1-required teul dependency; the pre-existing legacy proof runner dependency remains separately OPEN
- C6: existing deterministic and tamper-rejection behavior preserved
- C8: physical teul source/binary/package custody remains; deletion approval not inferred
- native CLI: PASS for the certificate seam
- WASM/Workbench: not applicable to this host filesystem certificate adapter; no parity claim
- new review task/worktree/branch: 0/0/0
- review bundle target: next coherent CLI/teul authority0 milestone through the existing rolling reviewer after management selection

## Protected custody and nonclaims

The four pre-existing task-owned untracked session files remain byte-identical and unstaged. W74 external build/test residue was deleted only after exact path containment checks; repository residue is 0.

This handoff does not claim the public PathIR obligation contract, whole PathIR P1, proof receipt closure, public command membership, whole C0~C8 closure, required dependency0 across every V1 workflow, teul physical retirement, P0~P6 closure, V1 membership/readiness/release, activation, legal approval, Owner Human Smoke, or Human PASS.
