# AI prompt explicit shared-root W1 handoff

## Scope and lineage

- Product fixed commit: `f10ae697362a9912c56fa9ec4c48fd9da65c330b`
- Direct parent: `478834d3cc399011e5d9741a1d574edf8a57eb60`
- Product fixed tree: `1dcbb4cb181ede60274c45589ea843a3a8a2f9a5`
- Product paths only:
  - `tool/src/ai_prompt.rs`
  - `tool/src/main.rs`
- Merge count: `0`

This is a non-release internal developer workflow repair performed while the
rights/publication track remains separate and unresolved.  It makes no V1
membership, readiness, release, activation, legal, or Human PASS claim.

## User workflow and product change

The actual `ddonirang-tool ai prompt --profile lean --out <path>` workflow
could not read the ignored `docs/ssot` directory from the linked product
worktree.  It can now use the already-existing `DDN_BUILD_REPO_ROOT` as an
explicit runtime source-root binding.  The binding is read-only and does not
scan for, copy, or silently select another worktree.

`ai prompt` command failures now return a nonzero exit status: execution
failure is `1`; argument or subcommand usage failure is `2`.  The success
path, command spelling, bundle contract, output atomic writer, public API,
dependency set, and SSOT contents are unchanged.

## Verification

- Existing focused test reused:
  `cargo test -p ddonirang-tool --lib ai_prompt_output_invariants_hold --offline`
  -> PASS (`1 passed`, `618 filtered`).
- Unbound clean linked-worktree binary -> RED: exit `1`, SSOT directory read
  diagnostic, output artifact absent.
- Invalid `ai prompt --bogus` -> exit `2`.
- Explicit runtime root `I:/dev/ddonilang/codex` -> GREEN: exit `0`.
- Two explicit-root executions were deterministic: `1,288,269` bytes and
  SHA-256
  `4D88803E11ABB3BFC490561BC60712EB893E87561FEC2231799D292B2FB9A8B7`.
- Configuration fault mutation: unset root RED -> exact environment restore
  GREEN; no artifact was published during RED.
- `cargo build -p ddonirang-tool --bin ddonirang-tool --offline` passed using
  a no-root target directory.
- `git diff --check` passed before the fixed commit.

The whole-tree `cargo fmt --check` reports pre-existing formatting differences
outside this two-file diff.  No broad formatting rewrite was made.  The static
`ai_prompt_output_matches_golden` comparison remains `REBASE_REQUIRED`: it
compares a historical golden byte file to the live v25.50.0 SSOT projection;
the invariant test above confirms the current source-selected output instead.
No fixture or semantic output was rewritten for that historical mismatch.

## Boundaries and next work

- New dependency: `0`; new pack/runner/meta-test: `0`.
- Product/test/pack/WASM/UI/SSOT/public-SPEC/membership/release diffs outside
  the two product paths: `0`.
- Independent review was not dispatched; management may bundle this with a
  later coherent milestone if product risk warrants it.
- PathIR/Proof public physical registry and the remaining CLI/teul public
  retirement decisions remain separate scoped gates, not a whole-goal block.
