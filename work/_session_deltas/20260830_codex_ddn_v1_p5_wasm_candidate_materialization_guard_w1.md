# 2026-08-30 DDN V1 P5 WASM candidate materialization guard W1

- CURRENT: internal SSOT v25.32.0 / RD-001~483; public SPEC v0.6.0.
- FU02 independent PASS `436b6b6b...` was bound by ff-only from exact HEAD
  `2a71996c...`; no status-only commit was added.
- P2 durable save/reopen remains blocked by the Owner-open physical revision
  file/wire/serialization/storage contract. Product mutation for P2 was 0.
- A Workbench `strict` to `v1-core-v25` default switch was reproduced as a RED
  candidate but stopped because it is the still-open default-ingress decision.
  The temporary test edit was byte-exact restored; P3 product mutation was 0.
- Existing P5 candidate entrypoint actual RED: a long Windows build root omitted
  one tracked long-path file while checkout/build returned success.
- Product fixed `6edf6b586d0c0ff62761174fe958a204ce5f6938` adds
  `core.longpaths=true` and a clean fixed-tree guard; diff is exactly build
  script plus its existing focused test.
- Existing tests: 26/26 PASS. New test artifact 0, meta-test 0.
- Post-fix offline long-path candidate: exact clean fixed HEAD/tree, WASM
  5,558,787 bytes / SHA-256
  `58a32eb83527da6da3b39dfb8f335d5293cc6499bbbae628bfe390018a6577bc`,
  internal/unknown/private path counts 0/0/0.
- Candidate receipt: 2,470 bytes / SHA-256
  `2ad1120cdeeef3521a07bfdda31ac98e9cc34a92fbc20e6d0f30ff8b4655cf28`,
  semantic identity
  `sha256:2716d1eb7b81b2482766457b174f890eee2ed4258fd43786c7dfc0cd2db0f85b`.
- Tracked WASM/manifest, product runtime, packs, UI, SSOT, SPEC, membership and
  release transitions: 0.
- Review dispatch: 0. Queue the coherent milestone for the one existing rolling
  reviewer only after management verifies this handoff.
- VC17 untracked/ignored custody was preserved byte-for-byte and unstaged.
- V1.2 JIEUM implementation was not started.
