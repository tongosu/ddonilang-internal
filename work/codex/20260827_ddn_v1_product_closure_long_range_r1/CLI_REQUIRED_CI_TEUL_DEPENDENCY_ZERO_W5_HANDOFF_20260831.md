# V1 required CI teul dependency-zero W5 handoff

## Custody and authority

- Persistent goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` (active).
- Live internal authority: SSOT v25.45.0 / RD-001~536.
- Public Language SPEC: v0.6.0.
- Branch: `codex/ddn-v1-p1a-core-supported-ingress-w1-20260829`.
- Baseline: `d9a4dcc5f01b49e39ebf4904848a126ee589f04d`.
- Product/test fixed: `454da54179488bd1bba0ffc1bf09d8be96ec25b6`.
- Fixed tree: `68e9a069481b13754a8ed417b81e677017c9ce05`.
- Direct parent: exact; merge count 0.
- P5 target-bound review custody remains `3e205ce8... -> ccaa7132... -> bc84d81d...`, report SHA-256 `05d9522c900d5c164064a003f92fabc100f64daf40100690b0e3c3747892a6d6`, blocking 0. It is not rerun or broadened here.

## Product and release-gate change

The required branch-protection context remains exactly `seamgrim-gate`, but its
execution graph no longer builds or invokes `teul-cli`. It now exercises the
existing official supported-profile product runner:

```text
python tests/run_v1_core_supported_ingress_w1.py
```

Historical W49/W111/W109/W107 teul goldens are not deleted or promoted. They
remain in the same workflow under `historical-teul-custody`, gated to explicit
`workflow_dispatch`. This is reversible INTERNAL/DEFERRED custody, not a final
physical-layout or public membership decision.

Exact fixed diff:

1. `.github/workflows/seamgrim-ci.yml`
2. `tests/run_seamgrim_workflow_contract_check.py`

The existing workflow contract checker was extended because the required CI
execution graph is a release-critical product dependency. No new runner, pack,
checker family, meta-test, reviewer, worktree, branch, or task was created.

## RED, GREEN, and regression evidence

- Baseline RED: the required `seamgrim-gate` contained `tools/teul-cli`,
  `TEUL_CLI_BIN`, and `run_golden.py` execution dependencies.
- Contract GREEN: `run_seamgrim_workflow_contract_check.py` PASS.
- Worker-env contract: PASS, 10 checked files.
- YAML parse: PASS; exact jobs are `seamgrim-gate` and
  `historical-teul-custody`.
- Official V1 supported ingress: native 7/7, native/WASM exact 2/2,
  tracked-WASM 10/10, deterministic repeats 4, partial summary 0,
  official CLI positive 4 and negative 4 PASS.
- Risk mutation: a `tools/teul-cli` dependency marker was reintroduced into
  the required job; the checker returned RED with
  `check=v1_required_teul_dependency_present`. Exact restore returned GREEN.
- Immutable W5 workflow identity at product fixed `454da54179488bd1bba0ffc1bf09d8be96ec25b6`:
  `.github/workflows/seamgrim-ci.yml`, 3,531 bytes,
  SHA-256 `bc83a85ca89cbf96ecb7b5f6a6eaac821b3a2d2ee8b134ca9a2d7e4c48c3c624`,
  Git blob `ad56c77adfac4058600784c774b8e70f09b6d367`.
- Immutable W5 checker identity at the same product fixed:
  `tests/run_seamgrim_workflow_contract_check.py`, 4,411 bytes,
  SHA-256 `aac30e5276ba3b3032f14d9170f28db54749c20371f113ea3ca1285181abe785`,
  Git blob `66209be82c9e38b1167ae058d86e8c2c95d2985c`.
- The earlier restored working-tree SHA-256 values are unbound projections and
  are not attached to this immutable W5 review target.
- Mutation residue: 0; `git diff --check` PASS.
- Existing deploy-artifacts check remains RED at the unrelated baseline
  `nginx_conf_required_tokens missing=location /wasm/`; this slice did not
  modify nginx or projection content and does not convert that release gate
  into PASS.

## C0 through C8 actual status

| Gate | W5 status |
|---|---|
| C0 | Historical 28 tool + 63 teul = 91 identity custody unchanged. |
| C1 | `ddn.project-run.v1` and executable/package naming boundaries unchanged. |
| C2 | Shared canon/preprocess authority unchanged. |
| C3 | Official required CI now exercises the supported `run/check/build/canon` frontdoor; public `view/test/repl` membership remains OPEN. |
| C4 | INTERNAL/DEFERRED teul commands and sources preserved; historical goldens are manual custody. |
| C5 | Required branch-protection CI execution dependency on teul is 0. Standalone optional historical script/reference custody is not deleted. |
| C6 | Supported source/diagnostic/result parity remains GREEN as scoped. |
| C7 | Native/WASM parity remains GREEN; Workbench/browser and unrelated deploy projection gates are not promoted. |
| C8 | P5 reviewed projection still excludes teul; physical binary/package/source retirement and deletion remain Owner-gated. |

## Anti-meta and nonclaims

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED: pull requests can satisfy the required V1 gate without building or executing teul-cli
NEW_TEST_ARTIFACT_COUNT: 0
EXISTING_TEST_REUSED_COUNT: 4 groups
META_TEST_CREATED: 0
STOP_RULE_APPLIED: YES
NEXT_PRODUCT_DECISION_ENABLED: distinguish required V1 CI from historical teul custody at fixed Git identity
ACTIVE_REVIEW_TASK_COUNT: 0
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
REVIEW_BUNDLE_TARGET: next coherent CLI/teul convergence milestone on the existing rolling reviewer only
```

This does not close all teul private semantic authority, choose public command
membership or executable naming, retire/delete the teul binary/package/source,
close the unrelated nginx/public projection gate, or claim P0~P6, V1 readiness,
release, activation, legal approval, Owner Human Smoke, or Human PASS.
