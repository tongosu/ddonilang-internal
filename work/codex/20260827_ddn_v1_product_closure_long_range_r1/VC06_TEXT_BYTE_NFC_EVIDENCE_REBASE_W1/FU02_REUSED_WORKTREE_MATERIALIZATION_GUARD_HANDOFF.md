# VC06 FU02 Reused Worktree Materialization Guard — Handoff

## Fixed lineage

- coherent milestone review parent: `86a094d556a2c87104cbb56cdc94576e8e8c0a94`
- scoped review `PASS_WITH_FOLLOW_UP`: `61c8dce6b9fbdb9921a71339ae7d788e6534f016`
- review report: `8,560 bytes` / SHA-256 `61620d61283184533fd65b266950f4c456a710712f5447341120c8a3f9709781`
- FU02 evidence fixed: `eefef28db6a9e3bf660331dca8568829e8b41c45`
- fixed tree: `6e62ed2087871c1bb8f13fc445366eee1f37e504`
- fixed direct parent: `61c8dce6b9fbdb9921a71339ae7d788e6534f016`
- fixed diff: `tests/run_v1_core_text_byte_nfc_rebase_w1.py` exactly one path
- runner SHA-256: `817b9b05367bb3cdf6d84513065fe76e64072d8ad45680eb0cb18717f672655b`
- merge count: `0`

## Product value and correction

The existing VC06 product-facing runner now fails closed before semantic
execution when a reused checkout's raw pack bytes do not satisfy the repository's
declared `eol=lf` materialization contract.

It records two separate identity sets:

1. fixed Git blob SHA-256 identities used by the manifest;
2. current checkout raw-byte SHA-256 identities.

The manifest plus eleven fixtures must be tracked, declare `eol=lf`, contain no
raw CR/CRLF materialization, and be byte-identical to their `HEAD` Git blobs.
The runner does not normalize or rewrite source bytes and does not add a Python
or JavaScript semantic implementation.

No `.gitattributes`, product source, pack fixture, manifest, tracked WASM, SSOT,
public SPEC, public documentation, or visible UI file changed.

## Verification

- Python compile: `PASS`
- normal materialization preflight: `PASS`, files `12/12`, declared EOL `lf`
- controlled T01 CRLF materialization mutation: `RED`, exit `1`
- exact RED diagnostic: `E_CHECKOUT_MATERIALIZATION_CRLF`
- mutated checkout SHA-256: `cce147687ae6dbda410555d3caf3db6b0d174e7f9f8c674d72c5ca321e0499f2`
- original/restored T01 SHA-256: `c0f201ec2c1b378047d888600e417a0033bbe00e9880e79046f2f3e32d4aae15`
- byte-exact restore: `PASS`
- restored preflight: `GREEN`
- full existing VC06 runner: `GREEN=7 / RED=0 / PRODUCT_GAP=4`
- native/tracked-WASM full structured payload exact parity: `11/11`
- deterministic repeats: `3`
- official tracked-WASM freshness: `PASS`
- existing local-project CRLF unit: `PASS`
- `git diff --check`: `PASS`

## Authority impact and open gaps

- live internal CURRENT: `v25.25.0 / RD-001~469`
- public Language SPEC: `v0.6.0`
- successor impact on this evidence-only materialization correction: `UNAFFECTED`
- actual C2 membership `40` and blocker `28` remain authority facts, not product
  closure evidence from this slice.

Preserved OPEN/PRODUCT_GAP items:

- ordinary identifier NFC resolution/original-span custody;
- byte literal and explicit UTF-8 conversion;
- BOM-as-data ingress;
- invalid UTF-8 before the product String API;
- local-project raw-byte/InputSnapshot receipt surface;
- model string NFC;
- stable public diagnostic spelling.

## Anti-meta and review custody

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: a clean Git checkout can now be trusted
  to execute the exact VC06 raw sources, while a stale CRLF materialization is
  rejected before semantic execution.
- `NEW_TEST_ARTIFACT_COUNT`: `0`
- `EXISTING_TEST_REUSED_COUNT`: `3` (VC06 product runner, freshness, local-project CRLF unit)
- `META_TEST_CREATED`: `0`
- `STOP_RULE_APPLIED`: yes; one risk-relevant CRLF mutation only
- `NEXT_PRODUCT_DECISION_ENABLED`: management can determine whether the scoped
  VC06 evidence is reproducible in a reused Windows review worktree.
- `NEW_REVIEW_TASK_COUNT`: `0`
- `NEW_REVIEW_WORKTREE_COUNT`: `0`
- targeted rereview must reuse rolling reviewer thread
  `01a04b17-66bb-7fa3-b827-53ad450005b4` and its existing clean worktree only.
- pre-dispatch custody check: the designated
  `C:/Users/ddongosu/.codex/worktrees/3a1f/codex` path is currently absent;
  no review message was sent and no replacement worktree was created.

## Nonclaims

This handoff does not claim VC06/VC12/VC04 closure, whole P1/P1-A/V1 closure,
membership/readiness, public command or WASM membership, release, activation,
legal clearance, external-user success, Owner Human Smoke, or Human PASS.

Status: `VC06_FU02_REUSED_WORKTREE_MATERIALIZATION_GUARD_READY_FOR_TARGETED_REREVIEW / REVIEW_WORKTREE_REBIND_REQUIRED`.
