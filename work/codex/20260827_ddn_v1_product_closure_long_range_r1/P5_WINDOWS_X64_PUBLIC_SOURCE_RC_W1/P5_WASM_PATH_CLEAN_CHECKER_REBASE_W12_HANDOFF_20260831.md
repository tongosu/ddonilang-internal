# P5 tracked-WASM path-clean checker rebase W12 handoff

## Fixed lineage and scope

```text
AI_PROVIDER: OpenAI
AI_SURFACE: Codex Work
AI_CAPABILITY: product release-gate correction and verification
SESSION_NICKNAME: DDN V1제품마감Codex
PROJECT_ROLE: DDN V1 closure single writer
RETURN_LABEL: [DDN V1제품마감Codex -> Codex관리Work]
ORIGIN_TASK_ID: DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1
```

- Live authority: internal v25.45.0 / RD-001~536; public SPEC v0.6.0.
- Baseline/handoff: `52d693f428a3a14be2cfbd8193dd8e23faa86b7e`.
- Evidence/test fixed: `47aa649b16cc50dd706e321dd5bcdf271c5a68d7`, tree
  `5834fec3ba2dee5017c8156854c773c980c8c633`, direct parent `52d693f4...`, merge 0.
- Exact fixed path: `tests/test_wasm_candidate_remap.py` only.
- Product source, tracked WASM, projection manifest, SSOT, public SPEC, visible UI,
  membership, and release transition diff: 0.

## Release blocker corrected

The existing release-critical remap checker still asserted the historical tracked-WASM
inventory `115 = cargo-registry 94 + rustup 21`. Current tracked WASM is already
path-clean and the product inventory reports:

```text
internal_absolute_path_count=0
root_family_counts={}
unique_path_count=0
unknown_path_count=0
```

Therefore the checker rejected the safer current artifact. The fixed test now verifies
the current path-clean contract rather than preserving the historical unsafe count. This
is not a test of another test: it directly inspects the tracked release artifact and is a
release-decision dependency.

## RED, GREEN, and reused evidence

- Baseline: 55/56 PASS; `test_tracked_inventory_is_exact_115` RED because actual was 0.
- Fixed: projection/remap suite 56/56 PASS.
- Existing W11 projection validation remains PASS: 173 files, candidate tree
  `sha256:8277058de943b241b6252cd0680e8af2d02c164f1ca4924c173bfb900bf1d09d`,
  receipt `sha256:eebce06911086e4bd1b5ab9e47525d1ec23b526a8a7d7c2d48bfb4d9406ebcc4`.
- New pack/runner/checker/framework/meta-test: 0/0/0/0/0.
- Reused test count: 56.
- No mutation harness was added: the actual historical assertion supplied the concrete
  RED and the path-clean artifact supplied the product-facing GREEN.

## Review bundle and nonclaims

W12 is bundled with W11 for the one existing rolling reviewer. This task did not create
or dispatch a reviewer, worktree, branch, or task.

Status is only:

```text
P5_WASM_PATH_CLEAN_RELEASE_CHECKER_REBASED_UNDER_REVIEW
```

Strict SPEC-link history, public test/view/repl membership, physical teul deletion,
whole P5/V1 closure, readiness, release, activation, legal approval, Owner Human Smoke,
and Human PASS remain OPEN.
