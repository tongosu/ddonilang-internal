# CLI frontdoor input shared authority W26 handoff

## Identity

- Authority: internal SSOT v25.47.0 / RD-001~543; public Language SPEC v0.6.0
- Baseline: `4ff914348644da96e1c3340f6da854d5196255da`
- Product fixed: `f0f0755c535117fdb2054c73db89e2488d668586`
- Fixed tree: `05d7657b884b54044be32e81ae38b23f4fe2549b`
- Merge count: 0
- Existing rolling reviewer: `01a04b17-66bb-7fa3-b827-53ad450005b4`

## Product change

The legacy-frontdoor guard composition and file-metadata-aware canon input
preparation now have one shared owner in `ddonirang_tool::preprocess`.
`teul-cli` retains only an adapter re-export. The shared tool preprocessing
path itself consumes the same aggregate guard, so official tool and retained
teul consumers cannot independently reorder or omit one legacy check.

Exact product paths:

- `tool/src/preprocess.rs`
- `tools/teul-cli/src/cli/frontdoor_input.rs`

No command membership, executable/package name, alias lifetime, public wire,
raw DDN syntax, SSOT, public SPEC, tracked WASM, or visible UI changed.

## Verification

- clean isolated tool target: focused preprocess legacy rejection 1/1 PASS
- clean isolated teul target: legacy-header removal and legacy-root rejection
  2/2 PASS
- supported-profile canon shared authority and atomic output 1/1 PASS
- official `ddonirang` binary build PASS
- teul-only clean target binary build PASS
- known `boim_is_accepted_via_frontdoor_guard` baseline remains FAIL with
  `E_BOIM_LEGACY_REMOVED`; this slice does not choose that semantic conflict
- new regression: 0

The reused mixed Cargo target first resolved a different worktree's lang crate,
and a later shared target combined `serde_json` 1.0.147/1.0.149 artifacts.
Both were classified as target-materialization events. Separate clean targets
built the fixed source successfully; no dependency/source workaround was made.

## Mutation

One risk-relevant mutation reintroduced a private teul aggregate legacy guard.

- mutation SHA-256: `a7b9c2a57b6cc6e46d668728f61222bc5e4603342d843a997d5b7da9ed4334aa`
- RED: `PRIVATE_FRONTDOOR_GUARD_AUTHORITY_REINTRODUCED`, private owner count 1
- exact pre-cleanup restore SHA-256: `96d543706b47f9388e7828a49865d7f43c151881a7812ef6340434ef9d31bf19`
- final adapter SHA-256: `27c32d2fe11c668cd0e0747dc1f4d95b202aaa4bd968da67868d6edbe99bfb9c`
- final private implementation count: 0
- restored focused GREEN: 1/1
- residue: 0

## Anti-meta and review queue

- User workflow changed or unblocked: official/tool and retained teul canon/run
  ingress now share one complete legacy fail-closed and metadata preparation
  decision.
- New pack: 0
- New runner: 0
- New test artifact: 0
- Meta-test: 0
- Existing tests reused: 4 focused cases plus two binary builds
- New reviewer/worktree/branch: 0
- Review bundle target: W25 file metadata + W26 frontdoor input shared authority

## Nonclaims

This is implemented under review. It does not close C0~C8, whole CLI
convergence, physical teul retirement, P0~P6, V1 membership/readiness/release,
activation, legal approval, Owner Human Smoke, or Human PASS. SPEC history,
PathIR public contract, public test/view/repl membership, and VC17 exact landing
remain slice-local OPEN rather than whole-goal blockers.
