# 2026-08-29 DDN V1 public docs latest-authority refresh R1

## Result

- verified filesystem live CURRENT: internal SSOT v25.22.0 / RD-001~469; public SPEC v0.6.0.
- product baseline `2c78dad8d4ce9732054ced6441b830ce4e5b032d` was tracked clean, staged0, merge0, target conflict0 and active writer conflict0.
- fixed `ee700e8e73b4213104d7f4f7517b0a3cb3f006cc` changes only `publish/v1/CURRENT.md` line 16 from v25.19.0 to v25.22.0/RD-001~469.
- other five public docs preserve predecessor bytes and SHA-256 exactly.
- old adoption `363f3e15...` and review FAIL `d08d67b9...` remain predecessor custody; no rewrite/revert/merge.
- product/test/pack/WASM/UI/SSOT/SPEC/membership/release diff0.
- VC17 task-owned residue preserved byte-for-byte, uncommitted and unstaged.

## Validation and review

- UTF-8/no-BOM/LF 6/6, local links7/7, PRE_RELEASE and all zero-count nonclaims PASS.
- new test/pack/checker/framework/meta-test0.
- new reviewer/worktree/branch0.
- existing rolling reviewer is not dispatched until management binds this handoff.

## Worktree lifecycle

- product worktree: task-local `IMPLEMENTED_PENDING_REVIEW` after handoff.
- existing 3a1f worktree remains `REVIEW`; other unaudited worktrees remain `UNKNOWN`.
- remove/prune/branch-ref deletion0; protected-process lifecycle change0.

## Nonclaims

Independent PASS, P5/release, membership/readiness, activation and Human PASS remain OPEN.
