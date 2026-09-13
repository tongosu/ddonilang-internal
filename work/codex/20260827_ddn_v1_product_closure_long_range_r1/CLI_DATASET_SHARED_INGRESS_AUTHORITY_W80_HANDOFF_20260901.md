# CLI dataset shared ingress authority W80 handoff

## Identity and status

- Live authority: internal SSOT `v25.47.0 / RD-001~543`, public Language SPEC `v0.6.0`.
- Authority impact: `ADDITIVE`; no fixed-target PASS is inherited or promoted.
- Baseline: `90516bc57bbdd527eb8839b0fe2097427c3725c2`.
- Product fixed: `b59c9f4e049317ac10c0f8964579fbbb20f036b5`.
- Status: `CLI_DATASET_SHARED_INGRESS_AUTHORITY_W80_IMPLEMENTED_UNDER_REVIEW`.
- Goal status: active; slice-local blockers are not a whole-goal impasse.

## Product value and exact ownership

The existing `dataset export` workflow now reads the Geoul bundle, derives source
provenance/state hashes/seed, and performs atomic Nurigym projection under the
shared `ddonirang_tool::dataset_workflow` authority.  The retained teul command
module is a 3-line compatibility adapter and contains no private Geoul reader,
snapshot decode, provenance assembly, value conversion, or export fallback.

Exact changed product paths:

- `tool/src/dataset_workflow.rs`
- `tools/teul-cli/src/cli/dataset.rs`

No new pack, runner, framework, public command spelling, public membership,
WASM export, Workbench UI, SSOT, or public SPEC path was added or changed.

## Evidence

- Build: `cargo build --offline --locked --manifest-path tools/teul-cli/Cargo.toml` PASS.
- Existing tool tests: `dataset_workflow` 2/2 PASS, 586 filtered out.
  - deterministic `nurigym_v0` and `nurigym_v1` projections.
  - invalid target preserves the complete predecessor, partial publish 0.
- Existing Geoul W53 fixture direct CLI export: PASS twice.
  - exit `0 / 0`.
  - dataset identity `sha256:f6075c8014833f5136a7ce2afccada8efe2b638d026ba43ca719d4888a7d4a88`.
  - all five projected artifact hashes equal across the two runs.
- Existing W53 end-to-end golden: baseline and fixed both `0/1` with the same
  predecessor `run --geoul-out` failure `E_SHARED_RUNTIME_OPTION_UNSUPPORTED`.
  This is `PRE_EXISTING_SHARED_RUN_OPTION_CONTRACT_DRIFT`; it was neither caused
  by this change nor promoted to PASS.
- Mutation: collected state hashes cleared after real Geoul ingestion.
  - RED exit 1 with `E_DATASET_EMPTY`.
  - the five predecessor artifact hashes remained byte-identical.
  - exact source restore SHA-256
    `cbc119b733b18a855a9cb89b12aa5053da4bf12edf11644185a7f33ae19358ef`.
  - rebuilt direct export GREEN exit 0; mutation residue 0.
- `git diff --check`: PASS.

## Frontdoor and C0-C8 boundary

- Native retained CLI: dataset subcommand reaches the shared product owner.
- WASM: not an applicable dataset-export frontdoor in this slice; no JS semantic reconstruction was added.
- Workbench: not an applicable direct dataset-export ingress in this slice; visible UI change 0.
- C0 registry custody is unchanged.
- C1-C7 receive one additional reversible private-authority reduction and shared-owner convergence.
- C8 physical retirement remains OPEN and Owner-gated.
- Required build/test/pack/publish dependency-zero and public artifact projection
  remain governed by their fixed evidence; this internal/deferred workflow does
  not enlarge public membership.

## Anti-meta and review boundary

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: existing Geoul-to-Nurigym dataset export now has one shared product authority; the full W53 chain remains blocked at its predecessor run option.
- `NEW_TEST_ARTIFACT_COUNT`: 0.
- `EXISTING_TEST_REUSED_COUNT`: 3 logical checks (2 tool tests + 1 W53 golden/direct workflow family).
- `META_TEST_CREATED`: 0.
- `STOP_RULE_APPLIED`: yes; no fixture/receipt tamper matrix was created.
- `NEXT_PRODUCT_DECISION_ENABLED`: the rolling reviewer can assess W78-W80 as one coherent retained-CLI authority bundle without a new reviewer or worktree.

This does not claim whole C0-C8 closure, repository-wide teul semantic authority
or required dependency zero, physical teul retirement, public command membership,
P0-P6 closure, V1 membership/readiness/release, activation, legal approval,
Owner Human Smoke, or Human PASS.
