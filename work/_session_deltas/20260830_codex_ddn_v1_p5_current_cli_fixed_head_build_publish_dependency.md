# [DDN V1제품마감Codex -> Codex관리Work] P5 current CLI fixed-head build/publish dependency — 결과

## Fixed custody

```text
CURRENT_AUTHORITY: v25.42.0 / RD-001~534
PUBLIC_SPEC: v0.6.0
AUTHORITY_IMPACT: ADDITIVE_CUSTODY_ONLY / new semantic RD 0
PRODUCT_TEST_FIXED: 64abb938b7eccf38ce71213ec03dfec2dd15fd5e
PRODUCT_TEST_TREE: bfb1482af0055abe6a1e9a8d057ba852664fe866
PREVIOUS_REVIEW_REQUEST: 3db8503f32c28569dcb0a7e811358a5d618e390c
```

The existing public projection, validator, WASM remap and Windows candidate
builder were reused against the exact current product/test fixed commit.
No product/test/pack/tracked-WASM/UI/SSOT/SPEC mutation occurred.

## Results

- Existing unittest modules: 56/56 PASS.
- Candidate WASM: 5,562,704 bytes /
  `b0c75e3e112777c0ca1dc66d428607e6596924c630675f42ef393b00d38e5385`.
- Public tree: 170/170 security scanned /
  `sha256:7200b36c0cab0b0810187b03c0a25fe14d60f6cb49d47fa2d8778d115bd4b6ad`.
- Windows x64 candidate executable: 6,917,632 bytes /
  `763f1546b2a429bffd5d10ecfebd2c1c5c549e77567fbf562207a47a3215603b`.
- Workspace members 6, teul source files 0, teul public binary/package 0.
- `BUILD_REQUIRED_TEUL_DEPENDENCY=0` and candidate-projection
  `PUBLISH_REQUIRED_TEUL_DEPENDENCY=0` are directly evidenced.
- `--require-spec-links` remains RED: ten historical SPEC manifest link targets
  referenced by `publish/spec/CURRENT.md` are absent from the current
  projection membership.

Recommended next decision: grant exact FILE_OWNER to add those ten frozen link
target directories to the projection manifest without changing SPEC bytes or
meaning. Relaxing link validation is not recommended.

## CLI and anti-meta boundary

`ddn.project-run.v1` is bound as the executable-neutral semantic identity.
Selector-conflict and `--out` atomicity contracts remain unconfirmed, so
`project-run` was not implemented. Candidate reachability remains 11/15;
`view`, `test` and `repl` remain open.

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED:
  path-clean current fixed-head Windows public-source candidate produced;
  build/publish candidate teul dependency zero directly established
NEW_TEST_ARTIFACT_COUNT: 0
EXISTING_TEST_REUSED_COUNT: 3 modules / 56 cases
META_TEST_CREATED: 0
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
ACTIVE_REVIEW_TASK_COUNT: 0
STOP_RULE_APPLIED: YES
REVIEW_BUNDLE_TARGET:
  existing rolling reviewer after management resolves missing review isolation
```

P5/CLI/V1 closure, teul retirement, public naming, release, activation and
Human PASS remain OPEN.
