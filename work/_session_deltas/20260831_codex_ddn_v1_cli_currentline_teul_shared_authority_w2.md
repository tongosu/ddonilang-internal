# 2026-08-31 DDN V1 CLI currentline teul shared authority W2

- Persistent goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1`, active/incomplete.
- Stale whole-goal blocker corrected: P5 reviewer handle existed and review
  `bc84d81d4faa55974975bdb7ec60cb18d9a7ebda` is now ff-bound.
- Authority: internal v25.45.0 / RD-001~536; public SPEC v0.6.0, read-only.
- Baseline: `bc84d81d4faa55974975bdb7ec60cb18d9a7ebda`.
- Product commits:
  - `fa31528265aff73cbc7abbc72e7610bc72b115ba` shared authority/consumers;
  - `31f22354f74afcf30eba40c1ab6e6e5f0775b979` fixed-source WASM candidate refresh.
- Final tree: `c21b165ccac519e49a6693739cc2cb708f4b9151`; direct lineage, merge 0.
- User workflow: retained teul `currentline-run` moved from private execution to
  the shared supported-profile currentline transaction and atomic writers.
- Product RED: existing V25 fixture failed `E_SHARED_RUNTIME_OPTION_UNSUPPORTED`.
- GREEN: official/teul exit 0; stdout, summary and context byte-exact.
- Fail-closed: missing teul source profile exits 2 with
  `E_SOURCE_PROFILE_REQUIRED`; partial publish 0.
- Mutation: hidden profile default produced actual RED, then byte-exact restore
  and GREEN; residue 0.
- Reused tests: shared focused 1/1, tool lib 536/536, official CLI 9/9, lang
  currentline 5/5, teul check, freshness, post-WASM consumer, clean offline
  candidate seal.
- Fixed candidate WASM: 5,568,161 bytes /
  `1c898279c3ba61f2334013aebb3d796ec7ee7ee8f38f59c4fd9c6e392c3c3b40`.
- New pack/runner/checker/meta-test/reviewer/worktree: 0/0/0/0/0/0.
- The existing broad parity checker has pre-existing invocation and obsolete
  corpus drift; this was classified rather than repaired as test-only work.
- Remaining slice gates: PathIR public physical contract, public
  `test/view/repl` membership, SPEC history and VC17 exact landing. Each remains
  local to its slice, not a persistent-goal blocker.
- Teul physical source/binary/package custody remains. No deletion, prune,
  branch/ref removal, public naming, alias-lifetime decision or release claim.
- Four pre-existing untracked custody deltas were preserved byte-for-byte and
  unstaged.
