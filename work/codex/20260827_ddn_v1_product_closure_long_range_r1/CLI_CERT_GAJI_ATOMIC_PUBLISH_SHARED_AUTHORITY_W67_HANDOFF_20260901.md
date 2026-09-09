# CLI cert/gaji atomic publish shared authority W67 handoff

## Status

- `CLI_CERT_GAJI_ATOMIC_PUBLISH_SHARED_AUTHORITY_W67_IMPLEMENTED_UNDER_REVIEW`
- Persistent goal remains `ACTIVE`.
- This is a bounded V1 release/package artifact correctness slice, not V1/P5/release closure.

## Authority and lineage

- Internal live CURRENT: v25.47.0 / RD-001~543, Owner-final 2026-08-31.
- Public Language SPEC: v0.6.0.
- Successor impact: `ADDITIVE_NO_RELEVANT_SEMANTIC_CONFLICT` for this internal artifact publication correction. No prior PASS is promoted or automatically inherited.
- Baseline/handoff parent: `e75638f2b79c5d0bf5ee18d8727443ecdb6d4860`.
- Product fixed commit: `91d07847e5b585d7fbfa99e94d123bd9c077dcd5`.
- Product fixed tree: `18832ab22c60ad34fd35b219641c875ff5192b53`.
- Direct parent: yes. Merge commit: no.

## Product value and exact diff

The existing certificate key-pair flow wrote the private key before discovering that the public-key target was invalid. A failed keygen could therefore replace one half of the pair. The fixed flow serializes both documents first and delegates the two-file transaction to the existing shared artifact-set writer. Certificate sign/report outputs and `gaji lock` now consume the same shared atomic text-artifact writer.

Changed product paths only:

- `tools/teul-cli/src/cli/cert.rs`
- `tools/teul-cli/src/cli/gaji.rs`

No new pack, runner, checker, framework, public spelling, wire schema, executable name, or semantic authority was added. `gaji vendor` directory replacement is explicitly outside this slice; it needs a coherent directory-transaction design and is not claimed atomic here.

## Product-facing RED to GREEN

Baseline fault setup used an existing `cert_private.key` plus a directory at the intended `cert_public.key` path.

- Baseline exit: 1, `E_CERT_OUT_WRITE` after private-key replacement.
- Predecessor private SHA-256 before: `de3de6abc4fe4cf8b629ad66724678156dc71c532d86e43415923b7365c2c202`.
- Baseline private SHA-256 after: `fb317355ff7629baf2eca2faa51fe78cb1cbe388633b7e6a778bf62837745fc7`.
- Baseline predecessor preservation: FAIL (actual partial publish).
- Fixed exit: 1, fail-closed `E_SHARED_ARTIFACT_OUTPUT_TARGET_NOT_FILE`.
- Fixed private SHA-256 before/after: `de3de6abc4fe4cf8b629ad66724678156dc71c532d86e43415923b7365c2c202` / same.
- Fixed predecessor preservation: PASS.
- Fixed temporary artifact residue: 0.

## Verification

- Product binary offline build: PASS.
- Actual certificate keygen -> sign -> verify: PASS, two independent executions.
- Deterministic artifact repeat: private key, public key, signed manifest 3/3 byte-identical.
- Actual `gaji lock`: PASS, two independent executions; lock SHA-256 `a8c73439499ebc8cf79193c271fc9f73de9ebd0df63b56a7efece625f27e3fb`, repeat identical.
- Existing `cli::gaji::tests`: 47/47 PASS.
- Existing shared `artifact_output::tests`: 5/5 PASS.
- `git diff --check`: PASS.
- External test/build file residue after cleanup: 0.
- New test artifacts: 0. Meta-tests: 0.

The unfiltered teul test-binary compilation remains OPEN at 13 pre-existing dual-`ddonirang_core` type mismatches in unrelated warp/latency/test-only paths. This slice did not alter dependency manifests or those paths. Product binary build and the affected focused/product frontdoors pass; whole-suite PASS is not claimed.

## CLI convergence state

- C0: 91-command registry remains custody (28 tool + 63 teul); no membership promotion.
- C1: `ddn.project-run.v1` remains the neutral semantic identity; executable/package/alias decisions remain OPEN.
- C2: shared source/canon/preprocess/execution/artifact authority convergence is additive; this slice removes three more direct artifact-write sites.
- C3: official V1 command reachability remains 12/15; public test/view/repl membership is slice-frozen.
- C4: internal/deferred commands remain custody; no deletion or public promotion.
- C5: bounded V1-required build/test/pack/publish teul execution dependency remains 0.
- C6: cert/gaji artifact publication behavior is fixed as scoped; whole native/WASM/Workbench CLI parity remains OPEN.
- C7: P5 target-bound review PASS remains bound; whole P5/Windows RC closure remains OPEN.
- C8: teul physical binary/package/directory retirement remains Owner-gated.

## Anti-meta and review custody

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: certificate key-pair creation, signing/report output, and lockfile publication no longer expose the identified direct-write partial-publish seam.
- `NEW_TEST_ARTIFACT_COUNT`: 0.
- `EXISTING_TEST_REUSED_COUNT`: 52 focused Rust tests plus two actual CLI workflows.
- `META_TEST_CREATED`: 0.
- `STOP_RULE_APPLIED`: yes; no hash-tamper suite, pack, runner, or review task was created.
- `NEXT_PRODUCT_DECISION_ENABLED`: include W62~W67 shared artifact publication convergence in the next coherent existing rolling-review bundle.
- Existing reviewer handle `01a04b17-66bb-7fa3-b827-53ad450005b4` is preserved; no new reviewer/worktree/branch was created or dispatched here.

## Open boundaries and nonclaims

- PathIR/Proof P0 containment is preserved. Public P1 assumption/obligation ingress and receipt closure remain slice-frozen where exact public contract is absent.
- `gaji vendor` directory transaction, public test/view/repl membership, VC17 exact provider landing, SPEC history, executable naming, teul physical deletion, legal/distribution, P5 whole closure, P6 Human Smoke, V1 readiness/release/activation/Human PASS remain OPEN.
- `docs/ssot/**`, public SPEC, tracked WASM, UI, membership, release state: diff 0.

