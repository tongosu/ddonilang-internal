# 2026-08-31 DDN V1 CLI run supported-profile shared authority W4

## Scope

- Continued persistent goal `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` in the
  existing product worktree and branch.
- Reassessed the stale whole-goal BLOCKED claim: the existing reviewer and P5
  target-bound PASS are present; slice-local public-contract gates do not form
  a global development impasse.
- Migrated one retained teul `run` workflow to the shared supported-profile
  runtime without deciding public membership or executable naming.

## Fixed identities

```text
AUTHORITY: internal v25.45.0 / RD-001~536; public SPEC v0.6.0
BASELINE: cafc5acd1cae07caf7263f77c6036b1c122e0715
PRODUCT_FIXED: 1b7290aebaafb7f7841a0e4be04e1d4bd1706171
PRODUCT_TREE: 93e7d2b2be681a8abd4d0672417d7029e7f9fa73
MERGE_COUNT: 0
```

Exact product paths:

```text
tools/teul-cli/src/main.rs
tools/teul-cli/src/cli/run.rs
tools/teul-cli/src/cli/worker.rs
tools/teul-cli/src/cli/world_diff.rs
```

## Evidence summary

- RED before product change: `run --source-profile` rejected by Clap, exit 2.
- Fixed: explicit `v1-core-v25` routes to the shared tool authority; no hidden
  default or PreV25 fallback.
- Official/teul full structured JSON exact equality: PASS.
- Native 7/7, native/WASM 2/2, tracked WASM 10/10, repeats 4, freshness PASS.
- Teul full suite: 1047 PASS + the same 9 pre-existing legacy failures.
- Fallback mutation: GREEN -> RED exit 101 -> exact restore -> GREEN; residue 0.
- Failure artifacts for legacy/unknown/conflicting profile cases: 0.
- New pack/runner/meta-test/reviewer/worktree/branch: 0.

## Remaining gates

- Branch-protected `seamgrim-gate` and the batch-quality script still execute
  historical legacy corpora through teul. That is a current dependency residue,
  but replacing it requires an approved V1 projection/gate boundary rather
  than treating legacy corpus syntax as V1 supported input.
- Public command membership, executable naming, alias lifetime, PathIR public
  wire, VC17 exact landing, physical teul retirement/deletion, V1 release, and
  Human PASS remain open.

Four pre-existing task-owned untracked custody files were preserved byte for
byte and left unstaged. `docs/ssot/**`, public SPEC, tracked WASM, and visible
UI changed by this milestone: 0.
