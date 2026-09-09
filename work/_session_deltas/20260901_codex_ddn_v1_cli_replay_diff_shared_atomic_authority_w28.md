# 2026-09-01 DDN V1 CLI replay-diff shared atomic authority W28

Status: Pending

- persistent goal remains active; whole-goal BLOCKED was rejected by current
  evidence and slice-local blockers remain isolated.
- live authority: internal v25.47.0/RD-001~543; public SPEC v0.6.0.
- baseline: `3ef1a26feef575b3af8a954ce288d7f459a614c5`.
- fixed: `9e7f88ea3375b8cfa909d96b06dfc14d87ccc84a`,
  tree `3bc551b654a7637bf18fb515ce62795f88839448`.
- replay-diff comparison/render/output authority moved from teul into tool;
  teul is a one-line adapter.
- product RED: blocked summary left one published result.
- product GREEN: equal/divergent/no-summary/blocked cases 4/4; blocked partial
  publish 0; successful report bytes unchanged.
- tests: focused 2/2; teul offline build PASS; tool regression 547 PASS plus the
  same 2 absent-SSOT environment failures; new regression 0.
- mutation: target-kind preflight bypass RED -> exact SHA restore -> GREEN;
  source residue 0.
- new pack/runner/meta-test/reviewer/worktree/branch: 0.
- protected four pre-existing untracked custody files remained unstaged and
  byte-untouched.
- next: management-dispatched existing rolling review for W25~W28, while safe
  non-overlapping internal convergence may continue.

Nonclaims: public command membership, whole P4/P5/V1 closure, physical teul
retirement/deletion, release, activation, legal or Human PASS are OPEN.
