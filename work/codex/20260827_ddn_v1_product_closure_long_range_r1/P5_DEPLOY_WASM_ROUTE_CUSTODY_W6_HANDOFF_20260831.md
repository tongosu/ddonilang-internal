# P5 deploy WASM route custody W6 handoff

## Authority and lineage

- Persistent goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` (active).
- Live internal authority: SSOT v25.45.0 / RD-001~536.
- Public Language SPEC: v0.6.0.
- Baseline: `9b2fcd784195d84ff09454664b29f39a2d30c690`.
- Release-check fixed: `122648f0548a7a44be0f455fdc2408a93d8fe23e`.
- Fixed tree: `8bc86ea0ae52f2a4f7fdd4d53598a20322fef2aa`.
- Direct parent exact; merge count 0.

## Release blocker corrected

The tracked nginx product configuration serves WASM at the existing exact path:

```text
/solutions/seamgrim_ui_mvp/ui/wasm/
```

The existing deployment checker had drifted back to the obsolete `/wasm/`
expectation and therefore returned a false release-gate RED. The fixed commit
changes exactly one physical contract token in the existing checker:

```text
tests/run_seamgrim_deploy_artifacts_check.py
```

No nginx route, UI behavior, WASM artifact, public command, SSOT, or public
Language SPEC was changed. The correction matches the already established
product route and its deployment README custody.

## Evidence

- Baseline RED: `check=nginx_conf_required_tokens missing=location /wasm/`.
- Deploy artifacts check after correction: PASS.
- Required workflow contract: PASS.
- Seamgrim CI worker-env contract: PASS, 10 files.
- Risk mutation: stale `/wasm/` expectation reintroduced -> exact RED.
- Byte-exact restore -> deploy artifacts GREEN.
- Immutable W6 checker identity at product fixed `122648f0548a7a44be0f455fdc2408a93d8fe23e`:
  `tests/run_seamgrim_deploy_artifacts_check.py`, 3,819 bytes,
  SHA-256 `9e850bb3916e9c5ea6969a0dd3bb83153a6e5898389d32a5438c7bbc9c906fd8`,
  Git blob `e2771b5fca0ce42f461bc1dcc7c0b0ffb4e0b441`.
- The earlier `8898db47f3f06d299130271c0f93b67a4bb26869eadca2f585bdbdac2f0456a1`
  value is an unbound working-tree projection and is not attached to the
  immutable W6 review target.
- Mutation residue: 0.
- `git diff --check`: PASS.

## Product-value and review boundary

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED: P5 deployment custody no longer rejects the tracked WASM route with a stale expectation
NEW_TEST_ARTIFACT_COUNT: 0
EXISTING_TEST_REUSED_COUNT: 3
META_TEST_CREATED: 0
STOP_RULE_APPLIED: YES; this is a reproduced release-critical checker defect
NEXT_PRODUCT_DECISION_ENABLED: run the existing P5 deploy/projection bundle against one consistent tracked route identity
ACTIVE_REVIEW_TASK_COUNT: 0
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
REVIEW_BUNDLE_TARGET: W5 required-CI dependency zero plus W6 deploy route custody on the existing rolling reviewer only
```

This is release custody, not P5 closure or publication authorization. It does
not choose public executable/command membership, retire/delete teul, promote
SUPPORTED_FOR_V1, or claim V1 readiness, release, activation, Owner Human
Smoke, or Human PASS.
