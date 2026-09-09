# PathIR/Proof B-01 targeted fixed-target rereview request

Use only existing rolling reviewer thread
`01a04b17-66bb-7fa3-b827-53ad450005b4` and its existing clean review
worktree. Create no reviewer, task, branch or worktree.

Review target:

- correction product/test fixed commit:
  `c44279d4c4a3cd8b6289de76b125c29e46257a50`;
- correction fixed tree:
  `220087d516f6f1bd25db0dc1a299579ed5346c1c`;
- fixed direct parent:
  `5eff9bda328fb9b3a1c6318970808a25e65258b6`;
- predecessor verdict: `FAIL`, B-01 only;
- review parent: the direct-successor docs-only handoff commit containing this
  request;
- merge count: 0.

Targeted scope:

1. receipt identity is never calculated for incomplete checker evidence;
2. result publish count must be exactly 1;
3. state publish and outbox release counts must be 0;
4. pre/post state hashes must match for the current pure-proof profile;
5. the exact reviewer compound counterexample is rejected;
6. wrong provider/checker/check-execution/check-result/report bindings remain
   rejected;
7. fixed source mutations for single and compound guards produce RED, exact
   restore, GREEN and residue 0;
8. symbolic 17, proof 18, tool 532, existing pack, freshness and tracked-WASM
   deterministic/fail-closed evidence remain GREEN;
9. correction product diff is exactly two paths and SSOT/SPEC/public contract/
   visible UI diff is 0.

Required nonclaims:

- this targeted rereview does not approve the OPEN public registry, field
  spelling, CLI option, WASM transport, Workbench mapping or raw-DDN assumption
  role;
- public M12 remains NOT RUN;
- XP-02 public completion, whole P1 PASS, ERQ closure, V1 support/readiness,
  release, activation and Human PASS remain OPEN.
