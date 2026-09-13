# DDN-LONG-RELINT-PRODUCT-01 G8 isolated integration baseline

## Custody

- gate: `G8`
- worktree: `I:/home/urihanl/ddn/codex/build/worktrees/ddn-long-relint-product-01-integration-g8-20260826`
- branch: `codex/ddn-long-relint-product-01-integration-g8-20260826`
- starting HEAD: `723c5b37fa48caa4a0560cf0715411bc07a5bdc2`
- starting source tree: `8036b67df85c700d0c17da7618bac5af53731036`
- parent owner-decision baseline: `a930f0c227cf73c640a49c09a634398c9bedbd85`
- worktree at creation: clean
- staged at creation: `0`
- merge commits from public R2 `fab6315ccddbec9b11bac748aed1c419f3ba4dad`: `0`

The shared dirty root was not reset, cleaned, stashed, or checked out. This
worktree is the only writer for G8 successor integration.

## Owner-bound membership

- reviewed T5 scope: include with explicit prerequisite custody; standalone T5
  program claims remain open.
- independently closed W1-A/B prerequisites and reviewed W1 scoped composition:
  include.
- PC02: exclude by applying the exact inverse of
  `04566a2426b56084f4449b363530192aa1166d2a` in this successor.
- PC01: excluded from release-integration membership until a fresh targeted
  independent plain PASS is bound. Existing inherited bytes are not evidence of
  PC01 membership or closure.
- R10: preserve as a reviewed T5 prerequisite; standalone R10 claim remains
  open.
- tracked WASM: rebuild the combined source through the official A/B procedure
  and bind one byte-identical family.
- public SPEC: bind only the exact live v0.5.0 18-file bytes.

## Pre-mutation exact-inverse audit

- PC02 is an ancestor of the starting HEAD.
- PC02 changed-path count: `28`.
- paths whose starting-HEAD blob differs from the PC02 commit blob: `0`.
- automatic `ours`/`theirs` resolution is forbidden.
- if the inverse does not apply without conflict or the resulting patch is not
  byte-for-byte the reverse of PC02, integration stops before commit.

## PC01 custody observation

PC01 product commit `cf97f134aebc4889bd3e13ff4850cbf76ca4c2d6`,
format correction `3ac1cefbffa4c00857f99debad3b1aad24ed08ea`, and
handoff `9cb28ee8044dd0562d99f8d5fce5911dfd01c652` are ancestors of the
starting HEAD. Of the 18 PC01 product-range paths, 16 still match the PC01 fixed
HEAD exactly; `tool/src/ddn_runtime.rs` and `tool/src/local_project.rs` have later
successor changes. This is dependency custody only. No PC01 PASS or release
membership is inferred. A fresh targeted independent review remains mandatory.

## Rights-sensitive public copies

- PC01 exact five-file public pack copy: `0`; pending fresh targeted plain PASS
  and Owner rights confirmation.
- projectile public example copy to `examples/physics/projectile_xy.ddn`: `0`;
  membership and path are selected, exact lesson bytes remain pending Owner
  rights confirmation.
