# DDN-P-V1-VC09-NAMED-CALLABLE-EVIDENCE-REBASE-W1 handoff / independent review request

## Status and scope

- status: `VC09_NAMED_CALLABLE_EVIDENCE_FIXED_IMPLEMENTED_UNDER_REVIEW`
- evidence baseline: `88c8bd664c03320f53baaaa917da11d7770a462a`
- product/evidence fixed HEAD: `23f6087e1a932d9c813c485fa117c58da20e081c`
- fixed tree: `eb4a4341260938876d41243f5af1d51f7e6cafc1`
- fixed direct parent: `88c8bd664c03320f53baaaa917da11d7770a462a`
- merge count from baseline: `0`
- source profile: exact `v1-core-v25`
- product source lease: `0`

This slice rebinds the existing non-recursive named-callable behavior to the
official supported-profile native and tracked-WASM frontdoors. It creates no
Python or JavaScript semantic implementation, lowering, parser, canon, or
hidden PreV25 retry path.

## Fixed diff contract

The fixed commit changes exactly 17 leased paths:

1. `pack/v1_core_named_callable_evidence_rebase_w1/README.md`
2. `pack/v1_core_named_callable_evidence_rebase_w1/manifest.detjson`
3. `pack/v1_core_named_callable_evidence_rebase_w1/fixtures/nc01_numeric_arguments_result.ddn`
4. `pack/v1_core_named_callable_evidence_rebase_w1/fixtures/nc02_text_argument_result.ddn`
5. `pack/v1_core_named_callable_evidence_rebase_w1/fixtures/nc03_unknown_callable.ddn`
6. `pack/v1_core_named_callable_evidence_rebase_w1/fixtures/nc04_arity_mismatch.ddn`
7. `pack/v1_core_named_callable_evidence_rebase_w1/fixtures/nc05_type_mismatch.ddn`
8. `pack/v1_core_named_callable_evidence_rebase_w1/fixtures/nc06_recursion_attempt.ddn`
9. `pack/v1_core_named_callable_evidence_rebase_w1/expected/nc01.detjson`
10. `pack/v1_core_named_callable_evidence_rebase_w1/expected/nc02.detjson`
11. `pack/v1_core_named_callable_evidence_rebase_w1/expected/nc03.detjson`
12. `pack/v1_core_named_callable_evidence_rebase_w1/expected/nc04.detjson`
13. `pack/v1_core_named_callable_evidence_rebase_w1/expected/nc05.detjson`
14. `pack/v1_core_named_callable_evidence_rebase_w1/expected/nc06.detjson`
15. `tests/run_v1_core_named_callable_evidence_rebase_w1.py`
16. `tests/run_v1_core_named_callable_wasm_parity_w1.mjs`
17. `tests/run_v1_core_named_callable_fault_injection_w1.py`

Diff from the baseline is zero for product source, tracked WASM, SSOT, public
SPEC, visible Workbench UI, `lang`, and `tools/teul-cli`.

## Packet identity

- manifest: 2,019 bytes / SHA-256 `b3ffe6c96853da2789b836d9311677908002da8286f3d6c3b26d101fb70d66ed` / Git blob `8bcccd899fa3b93f0b811c15a3a98ac0199a6cfe`
- native runner: 13,520 bytes / SHA-256 `1060c1d8244303acd85c6a7a0656a5b42a23f8890022640b260b7eb9aeae4e71` / Git blob `3fae3a8c44e07d8972501676989d50cdc2c55dd5`
- WASM parity runner: 7,157 bytes / SHA-256 `b6ee7162fe7f0641eb777d19894b1e697680d2699c9f25bb31cdb8cecd32e45f` / Git blob `591b6fb6f1dd3fdb5df2aa5d12628e7ae5f84cdb`
- fault runner: 5,383 bytes / SHA-256 `79e5455a360fedf29097d96d550bcc0cbc3b3f79175ba5c39a3adb7b6f7df13b` / Git blob `74700cab9aee752b7d658eb6fcb26e4acc93ed43`

Fixture and receipt hashes are exact in the manifest. For checkout-independent
text identity, the runners normalize only CRLF to LF before hashing and before
passing the same raw Korean source into the official frontdoors. They perform
no token, syntax, or semantic rewrite.

## Exact cases and observed contract

| Case | Expected | Observed contract |
|---|---|---|
| NC01 | success | `(2, 3) 더하기` returns and publishes `5` |
| NC02 | success | text argument returns unchanged and publishes `IDENTITY` |
| NC03 | failure | unknown callable, structured `E_EXECUTION_PARSE`, partial publish 0 |
| NC04 | failure | arity mismatch, structured `E_EXECUTION_PARSE`, partial publish 0 |
| NC05 | failure | declared type mismatch, structured `E_RUNTIME_EXECUTION`, partial publish 0 |
| NC06 | failure | recursion attempt, `E_V1_CORE_RECURSION_UNSUPPORTED`, partial publish 0 |

All six cases use one-tick execution and three deterministic repeats. Native
and tracked WASM compare the complete success/error result object exactly, not
only a selected status code. Expected receipts bind source bytes, preprocess
and canonical identities, output, state/trace identity, and WorkCost receipt
for successes; failures bind the structured diagnostic projection and forbid
result/state/output/effect publication fields.

## Verification evidence

### Official native evidence

Command:

`python tests/run_v1_core_named_callable_evidence_rebase_w1.py`

Result:

`VC09_NATIVE_EVIDENCE_PASS cases=6 success=2 failure=4 deterministic_repeats=3 partial_publish=0 supplementary_cases=3 supplementary_commands=3`

The three focused product tests are exact non-zero matches for named-call alias
execution, canonical numeric type mismatch, and supported-profile V25 boundary
and recursion fail-closed behavior.

### Official tracked-WASM parity

Command:

`node tests/run_v1_core_named_callable_wasm_parity_w1.mjs`

Result:

`VC09_WASM_PARITY_PASS cases=6 native_wasm_exact=6 deterministic_repeats=3 partial_publish=0 freshness=PASS tracked_wasm_refresh=0`

Tracked frontdoor identities at the fixed head:

- WASM: 5,553,353 bytes / SHA-256 `29480a59d264cffa280d6c1fb8a5a74da857955a6f028cd8b2adaf71e2366f51` / Git blob `899c2734f4267339edf15a8bdfb5aaf70ba33797`
- JS: 89,038 bytes / SHA-256 `c5a80302a3a872fab1e8d14c2385f8b5b6ddde8cfc1096c64ee0231e4ec8df3d` / Git blob `215249c3ab0dd441f4b9a7a200f33b83f4c43cfb`
- tracked manifest checkout: 19,506 bytes / SHA-256 `b3daeb51b7e0d65348b6461785b0aaf34568dd1b624ec43d3d38e77962a21537` / Git blob `74ee08dfe743d41406ce0f0126fbe4a22dde6e43`

Official tracked-WASM freshness passed and no tracked refresh occurred.

### Tamper RED, exact restore, GREEN

Command:

`python tests/run_v1_core_named_callable_fault_injection_w1.py`

Observed in isolated temporary packet copies:

- `CASE_OMISSION`: RED exit 1 / `VC09_CASE_COUNT_MISMATCH`
- `CASE_ORDER_TAMPER`: RED exit 1 / `VC09_CASE_ID_OR_ORDER_MISMATCH`
- `FIXTURE_HASH_TAMPER`: RED exit 1 / `VC09_FIXTURE_HASH_MISMATCH`
- `RECEIPT_TAMPER`: RED exit 1 / `VC09_RECEIPT_HASH_MISMATCH`
- `OUTCOME_TAMPER`: RED exit 1 / `VC09_OUTCOME_MISMATCH`
- `PROFILE_IDENTITY_TAMPER`: RED exit 1 / `VC09_PROFILE_IDENTITY_MISMATCH`

Final marker:

`VC09_FAULT_INJECTION_PASS mutations=6 exact_restore=6 native_green=1 wasm_green=1 residue=0 tracked_identity_sha256=9a1660715619ad4c96253477202d4bd1d612ff89d40e800cba5aae729bf4bbb9`

Correction custody: the superseded `bafb7445...` value was captured before
`pack/v1_core_named_callable_evidence_rebase_w1/README.md` was added to the
fixed packet, while the aggregate deliberately hashes every packet file. The
independent review and the product writer both reproduced `9a166071...` from
the complete fixed tree. Individual fixture, receipt, runner, Git blob, and
before/after restore identities were unchanged.

The task-owned tracked packet and runner identities were identical before and
after. Product source and tracked WASM were never mutated.

### Regression and detached reproduction

- `cargo test -p ddonirang-tool --lib`: 523/523 PASS, 0 failed
- `git diff --check`: PASS
- local clean clone, detached fixed HEAD `23f6087e1a932d9c813c485fa117c58da20e081c`
- detached native: exact same 6-case PASS marker
- detached tracked-WASM: exact same 6-case parity/freshness PASS marker
- detached checkout final status: clean, staged 0, untracked 0
- detached reproduction directory removed after exact-path verification; residue 0

## Protected custody

- Node PID baseline/end: `17232,23912,29264,35048,45264,47736,56500,56632,57068,58644,60632` — identical 11/11
- TCP 8787 listener baseline/end: absent/absent
- server, browser, port, and protected-process start/stop/restart/kill commands: 0
- product worktree tracked state after fixed commit: clean, staged 0, merge 0
- unrelated task-owned untracked preparation document was preserved and never staged

## Independent review request

Review the fixed target `23f6087e1a932d9c813c485fa117c58da20e081c`
from this handoff commit as review parent. Use an isolated clean detached review
checkout. Required review surface:

1. verify direct lineage, fixed tree, exact 17 leased paths, and all protected diff 0;
2. verify packet fixture/receipt/hash/order and exact six-case bijection;
3. rerun official native and tracked-WASM frontdoors and require full payload parity 6/6;
4. verify success argument/result identity and failure partial publish 0;
5. independently reproduce all six tamper RED axes, exact restore, final GREEN, and residue 0;
6. verify no Python/JS semantic lowering, hidden PreV25 retry, product source edit, or tracked-WASM refresh;
7. create a docs-only review commit as a direct successor of the handoff parent.

Return `PASS`, `PASS_WITH_FOLLOW_UP`, or `FAIL` for this exact VC09 evidence
slice only. Do not promote VC09/P1-A/P1/V1 closure or membership/readiness.

## Nonclaims and open gates

This handoff does not claim independent PASS, VC09 closure, P1-A/P1/V1
closure, 18/18 membership, whole execution/exclusion readiness, public
executable or command membership, public stable profile spelling, Workbench
default ingress or visible UI behavior, VC17, P2-P6/RC, release, activation,
legal status, Owner Human Smoke PASS, Human PASS, or external-user success.
