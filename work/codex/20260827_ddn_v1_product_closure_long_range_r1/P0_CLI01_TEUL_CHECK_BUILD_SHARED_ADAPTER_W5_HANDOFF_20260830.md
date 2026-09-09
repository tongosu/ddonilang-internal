# P0 CLI01 teul check/build shared adapter W5 handoff

Date: 2026-08-30
Status: IMPLEMENTED_PENDING_COHERENT_REVIEW

## Fixed identity

- Authority: internal SSOT v25.40.0 / RD-001~515, public Language SPEC v0.6.0
- Branch: `codex/ddn-v1-p1a-core-supported-ingress-w1-20260829`
- Direct parent: `4a192db142675ab727c557eba382bc6046882e7b`
- Product/test fixed HEAD: `268dbd1d0d65464ad8faef9db16bd98ae5912893`
- Fixed tree: `159ace0dfa1e23b82f5fa716b00670b1941ff617`
- Merge count from the preserved P5 handoff lineage: 0

## User workflow changed

Historical `teul-cli check` and `teul-cli build` no longer select the private
parser/type/schema path by default. An explicit `--source-profile
v1-core-v25` routes both commands to the existing shared
`ddonirang_tool::source_analysis` authority and emits the same structured
payload and exit status as the candidate `ddonirang` frontdoor.

Omitted profile fails closed with `E_SOURCE_PROFILE_REQUIRED`, exit 2.
The historical implementation remains available only through the hidden
`--legacy-internal` flag used by the existing golden runner. That flag is
internal/deferred custody, not a public compatibility alias or V1 membership
decision.

## Exact product/test diff

1. `tools/teul-cli/src/main.rs`
2. `tools/teul-cli/src/cli/check.rs`
3. `tools/teul-cli/tests/run_golden.py`

No new pack, runner, checker, meta-test, reviewer, worktree, branch or goal was
created. Product source outside these three paths, tracked WASM, UI,
`docs/ssot/**` and `publish/spec/**` diff are zero.

## RED to GREEN and verification

- RED at parent: `teul-cli check <source> --source-profile v1-core-v25`
  failed in clap as an unknown option, exit 2.
- Clean teul-only external Cargo target build: PASS.
- Existing teul targeted unit: 1/1 PASS, 1057 filtered.
- Existing P1-A fixtures, candidate versus teul:
  6 fixtures x check/build = 12/12 exact exit/stdout/stderr parity.
- Missing profile: exit 2 and exact `E_SOURCE_PROFILE_REQUIRED`.
- Conflicting shared/internal flags: clap exit 2, fail closed.
- `check --help`: `legacy-internal` exposure 0.
- Existing W109 index selfcheck: 20 cases / canon error 4 / parse error 14 PASS.
- Existing W109 affected build/check historical cases: 6/6 PASS.
- Existing W109 whole run: 9 PASS / 11 FAIL; failures were outside the migrated
  build/check commands and are not promoted or hidden.
- Clean fixed-head reproduction: shared parity 12/12 and representative
  internal custody 2/2.

The first combined Cargo target reproduced a duplicate-crate type split because
the candidate and teul package lockfiles had materialized different dependency
versions in one target. A dedicated clean external teul target built GREEN.
This is build-environment custody evidence, not a product semantic failure.

## C0-C8 checkpoint

- C0 registry: 28 tool + 63 teul = 91 historical command identities.
- C1 core candidates: 15 fixed candidates.
- C2 semantic-owner audit: complete for the 15 candidate rows; six rows remain
  blocked by shared authority or detail gates.
- C3 single candidate reachability: 9/15
  (`run`, `check`, `build`, `canon`, `project-normalize`,
  `project-discover`, `project-graph`, `project-symbols`, `project-lock`).
- C4 private authority removal: partial. Public-like check/build default private
  authority is zero; explicit historical internal authority remains.
- C5 required dependency removal: OPEN.
- C6 parity: check/build scoped parity PASS; whole CLI parity OPEN.
- C7 clean projection/candidate: prior fixed P5 guard is preserved, not rerun or
  promoted here.
- C8 coherent independent review/retirement: OPEN.

Repository explicit teul-reference file counts under the current search
contract are: CI 1, scripts 1, tests 195, pack 369, publish 50, publish/v1 0.
These are custody counts, not a claim that every reference is V1-required.
The private parser/runtime/core-value residue inventory remains 7/7/11 source
files and needs later convergence classification.

## Anti-meta and nonclaims

- USER_WORKFLOW_CHANGED_OR_UNBLOCKED: YES
- NEW_TEST_ARTIFACT_COUNT: 0
- EXISTING_TEST_REUSED_COUNT: 4 evidence groups
- META_TEST_CREATED: 0
- NEW_REVIEW_TASK_COUNT: 0
- NEW_REVIEW_WORKTREE_COUNT: 0
- STOP_RULE_APPLIED: YES
- NEXT_PRODUCT_DECISION_ENABLED: classify V1-required versus
  internal/deferred build/test/pack references, then migrate the required
  projection without deleting historical custody.

This handoff does not claim all teul semantic authority zero, required
dependency zero, physical deletion eligibility, whole P0-P6 closure, V1
membership/readiness, final executable name, release, activation or Human PASS.

