# CLI Universe Shared Atomic Authority W52 Handoff

## Identity

- Authority: internal SSOT v25.47.0 / RD-001~543; public Language SPEC v0.6.0.
- Baseline / direct parent: `7d3aea070f05bd0edefe51204a53d8b27742664b`.
- Product/test fixed commit: `35702f09d55c40e860e38610c9ef61ecbd27f62a`.
- Fixed tree: `d97ed62ce2988bbea71ff58322902daa4437eeff`.
- Branch: `codex/ddn-v1-p1a-core-supported-ingress-w1-20260829`.
- Merge count from baseline: `0`.

## Product value and exact scope

The existing `universe pack -> unpack -> repack` user workflow now consumes one
shared native product authority in `ddonirang_tool::universe_workflow`. The
`teul-cli` module is an adapter-only re-export; its duplicate pack/unpack
implementation is removed. No executable name, public command membership,
package name, alias duration, SSOT, SPEC, WASM, Workbench UI, or release state
was changed.

Pack output is assembled before one atomic file publication. Unpack validates
and reads the complete archive, rejects duplicate/unsafe paths, then publishes
the output files as one atomic artifact set. A late invalid archive entry can no
longer leave earlier files partially published.

Exact fixed paths:

- `tool/src/universe_workflow.rs` (new shared owner)
- `tool/src/lib.rs` (native-only module export)
- `tools/teul-cli/src/cli/universe.rs` (adapter-only re-export)
- `tests/run_w93_universe_pack_check.py` (existing product runner extended)

## RED, mutation, and restore

- Baseline product RED: an archive containing `safe/first.txt` followed by
  `../escape.txt` failed late but left `safe/first.txt` published.
  Signature: `E_W93_UNPACK_PARTIAL_PUBLISH msg=safe/first.txt`.
- Risk mutation: bypassing shared archive-path preflight produced actual RED
  `E_W93_UNSAFE_ARCHIVE_ACCEPTED`, exit `1`.
- Exact restore source SHA-256:
  `9f0a3d2f0c5a79628665cf0755b07acdbec01ce748a3e1009b0c9cb5ec635e66`.
- Restored executable GREEN: W93 runner PASS; mutation residue `0`.
- The existing runner's binary freshness scan observes `tools/teul-cli/src/**`
  only. Mutation runs therefore explicitly rebuilt the executable after shared
  `tool/src/**` mutation; no new freshness framework was added.

## Verification

- `python tests/run_w93_universe_pack_check.py`: PASS, one product case, one
  golden case, deterministic pack hash
  `sha256:8e53e4d329aa001c59ddb30ce3a0fcb87ccd8655a512e58e11e030d081c4fb29`.
- `cargo test -q -p ddonirang-tool --lib artifact_output`: `5/5` PASS.
- `cargo check -q -p ddonirang-tool --lib`: PASS.
- `cargo check -q --manifest-path tools/teul-cli/Cargo.toml`: PASS.
- `cargo test -q -p ddonirang-tool --lib`: `561/564` PASS. The two missing
  isolated-worktree `docs/ssot` ai-prompt fixtures and the untouched
  PathIR definedness test remain pre-existing failures; W52 changed none of
  their owner paths.
- `cargo test -q --manifest-path tools/teul-cli/Cargo.toml`: `1047/1056` PASS,
  with the same nine pre-existing failures as W51 and new drift `0`.
- Clean fixed-head W93 reproduction after exact restore: PASS.

## C0-C8 and gate effect

- C0: historical 91-command inventory custody remains; membership transition 0.
- C1: `ddn.project-run.v1` remains bound; naming/alias gates remain open.
- C2: shared universe pack/unpack authority owner count is now 1.
- C3: no public command membership change.
- C4: one INTERNAL/DEFERRED teul private implementation became adapter-only;
  other private/deferred modules remain.
- C5: V1 required CI dependency remains 0; W93 historical/internal runner still
  invokes the adapter command.
- C6: deterministic roundtrip and unsafe-archive partial-publish boundary PASS.
- C7: no new reviewer or review worktree was created.
- C8: teul binary/package/directory physical retirement remains Owner-gated.

## Anti-meta and nonclaims

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: unsafe universe archive failure now has
  partial file publish 0; the deterministic pack/unpack workflow has one shared
  product owner.
- `NEW_TEST_ARTIFACT_COUNT`: 0.
- `EXISTING_TEST_REUSED_COUNT`: 2 (W93 runner and shared artifact-output tests).
- `META_TEST_CREATED`: 0.
- `NEXT_PRODUCT_DECISION_ENABLED`: another private teul implementation can be
  evaluated independently without treating this internal command as public V1
  membership.

This is `IMPLEMENTED_UNDER_REVIEW` for the exact W52 product slice only. It does
not claim whole CLI convergence, teul required-dependency 0 for every historical
surface, physical retirement, P0~P6 closure, V1 membership/readiness, release,
activation, legal disposition, or Human PASS.
