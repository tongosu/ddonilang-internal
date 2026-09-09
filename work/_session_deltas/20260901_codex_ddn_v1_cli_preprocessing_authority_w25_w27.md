# 2026-09-01 DDN V1 CLI preprocessing authority W25-W27

The persistent V1 goal remains active. The existing single writer, worktree,
branch, and reviewer handle were reused; no new task, branch, worktree, pack,
runner, test artifact, meta-test, or reviewer was created.

W25-W27 form one coherent preprocessing-authority bundle. File metadata has one
tool owner, retained teul frontdoor input consumes the shared aggregate, and
tool legacy/preprocess pass-through wrappers now directly re-export the
language authority. W27 fixed is `e845e72b3f3a48bc96fed0926765b6ca16032180`
with tree `955b26e687a86732cc16d9a7b881c7c26db31fd5`.

Focused product tests and isolated builds are GREEN except the unchanged known
boim expectation conflict documented by W26. W27 mutation was RED, restored
byte-exactly, and returned GREEN with residue 0. Four protected untracked
custody files remain unchanged and unstaged. SSOT/SPEC/public naming/UI changes
are 0. Whole CLI/V1/release/Human closure remains open.
