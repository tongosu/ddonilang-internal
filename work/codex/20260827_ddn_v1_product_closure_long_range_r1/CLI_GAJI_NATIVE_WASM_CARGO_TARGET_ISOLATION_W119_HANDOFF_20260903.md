# CLI gaji native/WASM Cargo target isolation W119 handoff

## Fixed identity

- Product parent: `80f058c12d7f65fb8854b1936a9fc6d39585e54b`
- Product fixed commit: `003395300054d256aebfeac7bfb94945c1d4ed56`
- Product fixed tree: `8f86eb963398239c73e3c128256fe2c54ba09ecf`
- Branch: `codex/ddn-v1-p1a-core-supported-ingress-w1-20260829`
- Authority, read-only: internal SSOT `v25.50.0 / RD-001~551`; public Language SPEC `v0.6.0`.

## Product-facing correction

The existing `gaji_creator_wasm_parity_runner.mjs` runs the nested `teul-cli`
workspace and the official root workspace in one user-facing native/WASM parity
workflow.  Their separate lock graphs could share an inherited Cargo target and
link duplicate `bzip2-sys` metadata, producing `LNK2005`/`LNK1169` before the
parity assertion ran.

The existing runner now assigns one temporary Cargo target subtree per workspace.
It still invokes the same official native CLI, nested retained internal custody,
and tracked WASM inputs; it neither changes source semantics nor makes any public
command, package, or retirement decision.

## Verification

- Reproduced baseline failure: mixed shared target caused the concrete native
  linker false-RED (`LNK2005`/`LNK1169` for duplicate `bzip2-sys`).
- Existing runner reused, with an explicitly shared outer `CARGO_TARGET_DIR`:
  `node tests/gaji_creator_wasm_parity_runner.mjs` — PASS
  (`gaji_creator_wasm_parity: ok`).
- `node --check tests/gaji_creator_wasm_parity_runner.mjs` — PASS.
- `git diff --check` — PASS.
- The runner's existing cleanup removed its process-owned temporary output and
  Cargo-target roots after the green run.

## Custody and limits

- Product/test diff: only `tests/gaji_creator_wasm_parity_runner.mjs`.
- Reused product-facing tests/runners: 1. New test artifacts, packs, runners,
  dependencies, and meta-tests: 0.
- The concrete false-RED is the risk-relevant RED; no synthetic test-of-test
  mutation was added.
- This enables an honest native/WASM parity decision for the existing gaji
  workflow (C6), not a broader C0--C8, P5, or V1 closure.
- No reviewer, worktree, branch, or public artifact was created.  Review remains
  reserved for the next meaningful coherent milestone through the existing rolling
  reviewer.

Nonclaims: no teul-cli physical deletion or public retirement, V1 command
membership, release/publication/rights clearance, readiness, activation, or Owner
Human PASS is claimed.
