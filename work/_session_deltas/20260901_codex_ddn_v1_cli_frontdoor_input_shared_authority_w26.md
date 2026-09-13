# 2026-09-01 DDN V1 CLI frontdoor input shared authority W26

## Session contract

- persistent goal remains ACTIVE
- single writer/worktree/branch reused
- FILE_OWNER: `tool/src/preprocess.rs`,
  `tools/teul-cli/src/cli/frontdoor_input.rs`, and this two-document handoff
- shared dirty root and `docs/ssot/**` untouched
- four pre-existing task-owned untracked custody files preserved and unstaged

## Result

Baseline `4ff914348644da96e1c3340f6da854d5196255da` advanced linearly to
product fixed `f0f0755c535117fdb2054c73db89e2488d668586` (tree
`05d7657b884b54044be32e81ae38b23f4fe2549b`). The tool now owns the
aggregate legacy guard and metadata-aware canon preparation; teul consumes the
shared API through an adapter. Product paths changed: 2. Merge count: 0.

Focused verification passed for tool rejection, teul header/root behavior, and
supported-profile atomic canon. Both binaries built from separate clean Cargo
targets. The known contradictory boim expectation remains the same one failure
and was not promoted or changed. Mutation of the private aggregate guard was
RED, restored byte-exactly, and returned GREEN with residue 0.

No new pack, runner, test artifact, meta-test, reviewer, worktree, or branch was
created. W25+W26 form the next coherent rolling-review target. Whole CLI/V1
closure and all release/Human transitions remain open.
