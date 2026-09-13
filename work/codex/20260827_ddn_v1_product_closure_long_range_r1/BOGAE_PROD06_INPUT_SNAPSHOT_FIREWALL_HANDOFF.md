# BOGAE-PROD-07 InputSnapshot Firewall — implementation handoff

## Fixed target

- Product commit: `8d40ae3f6b315e15d69c64d66b508cacfbe39ee9`
- Tree: `9837cbf0fba253f094f01fa7cfc87647d134c212`
- Parent: `584668fba51ef92d4ca4a2eb1fa9556c723a2757`
- Scope: `workbench.js` and the existing project-controls browser runner only.

## Implemented behaviour

- A queued GUI action is bound to workspace, document, version, source profile,
  primary view, Bogae family, provider, source identity, and a canonical binding hash.
- A changed binding fails before a new run or live frame is published.
- Committed InputSnapshot records carry the request binding, shared source identity,
  committed world-state identity, and a deterministic snapshot hash.

## Evidence completed locally

- Actual local Workbench: raw V25 source in the pendulum project ran to
  `sealed runtime: 실행 완료`.
- Actual local Workbench: queue action, change source, then run produced
  `sealed runtime: 실행 실패` before a run/frame was created.
- Mutation M-B1: replacing typed binding validation with unconditional success
  admitted a stale queued action to execution success (RED).
- Mutation M-B2: temporarily disabling the queued-binding guard admitted that
  same stale queued action to execution success (RED).
- Mutation M-B3: silently discarding a rejected stale input and continuing as
  a default run admitted execution success (RED).
- Every mutation restored byte-exactly to SHA-256
  `4c6f7b50175e4de010ea5b71aa4eb821ffa841b7fb855c2f863805d3929f0214`
  and blob `3a2fd168888fa8bed5aac0b30312ad4bf9b7b5de`, followed by Green checks.
- `node --check` for both changed JavaScript files; existing semantic payload
  and semantic renderer runners; `git diff --check`: PASS.

## Independent review

- The existing independent reviewer returned `PASS_TARGET_BOUND`, blocking
  findings `0`, for exact product target `8d40ae3f6b315e15d69c64d66b508cacfbe39ee9`.
- The pre-existing project-controls browser runner cannot load because this
  worktree has no `playwright` package (`ERR_MODULE_NOT_FOUND`); no dependency
  was installed or downloaded. The reviewer classified that as environment-only.

## Nonclaims

No V1 readiness/release, public wire, SSOT, SPEC, or browser-runner PASS is
claimed.
