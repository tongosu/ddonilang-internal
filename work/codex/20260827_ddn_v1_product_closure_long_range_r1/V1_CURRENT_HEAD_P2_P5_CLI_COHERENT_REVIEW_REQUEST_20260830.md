# DDN V1 current-head P2~P5 + CLI coherent independent review request

Date: 2026-08-30
Execution owner: DDN V1제품마감Codex / persistent goal
`DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1`
Review disposition: `READY_FOR_EXISTING_ROLLING_REVIEWER_REBIND`
New reviewer/task/worktree/branch authorized: `0`

## Fixed identities

```text
LAST_REVIEWED_BASE: 65dcb1872d7b6b9099d85138c36bf2381c52bbed
LAST_REVIEWED_BASE_TREE: c3228683ae8e475ebdadad76646907a283f48d5d
PRODUCT_TEST_FIXED_HEAD: 64abb938b7eccf38ce71213ec03dfec2dd15fd5e
PRODUCT_TEST_FIXED_TREE: bfb1482af0055abe6a1e9a8d057ba852664fe866
PRODUCT_HANDOFF_PARENT: 67980c0b68bcf30689d52c4bb4c47dafbfd6ed34
PRODUCT_HANDOFF_PARENT_TREE: ba4d6fe1185e2013adc45e9a5ea0f2f4cfa322a2
PRODUCT_HANDOFF_DIRECT_PARENT: 64abb938b7eccf38ce71213ec03dfec2dd15fd5e
MERGE_COUNT_BASE_TO_HANDOFF: 0
CURRENT_AUTHORITY: internal v25.42.0 / RD-001~534
PUBLIC_LANGUAGE_SPEC: v0.6.0
AUTHORITY_IMPACT: ADDITIVE_CUSTODY_ONLY / NEW_SEMANTIC_RD_0
```

The review target is the fixed product/test commit, not this request document.
The review parent is the direct-successor commit that contains only this request
and its execution-owner session delta. Management must bind its exact commit
identity before execution.

## Why this is one coherent milestone

The prior broad product review and its focused follow-ups are already in the
base lineage. The delta from the reviewed base to the fixed target is the first
current-head V1 product milestone that joins:

1. P2 saved-project HEAD custody for Run creation;
2. P3 Workbench saved-HEAD propagation and stale-writer rejection;
3. P4 shared runtime age/trace/unit authority, CLI failure exits, and atomic
   native summary output custody;
4. P5 path-clean projected Windows x64 candidate materialization; and
5. official CLI/public projection convergence through eleven of the fifteen
   command workflows, including the latest shared lint authority.

These paths converge on the same runtime, project identity, public candidate,
and failure-atomicity boundary. Splitting them into another review per handoff
would review evidence files instead of the current product.

## Exact delta contract

`git diff --name-status 65dcb1872d7b6b9099d85138c36bf2381c52bbed
64abb938b7eccf38ce71213ec03dfec2dd15fd5e` contains exactly 78 paths:

```text
PRODUCT_OR_CONFIG: 24
TEST: 6
PACK: 1
SCRIPT: 1
TRACKED_WASM_FAMILY: 4
WORK_CUSTODY: 35
OTHER_PROJECT_CONFIG_OR_UI_BRIDGE: 7
DOCS_SSOT: 0
PUBLIC_SPEC: 0
MERGES: 0
```

The product-facing paths are:

```text
ddn.project.json
ddn.units.json
lang/src/currentline.rs
lang/src/lib.rs
pack/seamgrim_workbench_run_archive_store_v1/golden.jsonl
scripts/build_windows_x64_public_candidate.ps1
solutions/seamgrim_ui_mvp/tools/ddn_exec_server.py
solutions/seamgrim_ui_mvp/tools/project_store.py
solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.d.ts
solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.js
solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson
solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm
solutions/seamgrim_ui_mvp/ui/wasm_ddn_wrapper.js
solutions/seamgrim_ui_mvp/ui/workbench/persistence/run_archive_adapter.js
solutions/seamgrim_ui_mvp/ui/workbench/workbench.js
tests/run_ddn_local_project_cli_wasm_parity_check.py
tests/run_ddn_local_project_graph_check.py
tests/run_seamgrim_project_run_prerequisite_check.py
tests/run_seamgrim_workbench_run_archive_store_check.py
tests/run_v1_core_supported_ingress_w1.py
tests/seamgrim_wasm_cli_runtime_parity_runner.mjs
tool/src/ai_prompt.rs
tool/src/bin/ddonirang.rs
tool/src/ddn_runtime.rs
tool/src/detmath_assets.rs
tool/src/gate0_registry.rs
tool/src/lib.rs
tool/src/lint.rs
tool/src/main.rs
tool/src/project_meta.rs
tool/src/runtime_surface.rs
tool/src/schema.rs
tool/src/wasm_api.rs
tools/public_cargo_config.toml
tools/teul-cli/src/ai_prompt.rs
tools/teul-cli/src/cli/check.rs
tools/teul-cli/src/cli/lint.rs
tools/teul-cli/src/cli/patch.rs
tools/teul-cli/src/cli/run.rs
tools/teul-cli/src/core/bogae.rs
tools/teul-cli/src/main.rs
tools/teul-cli/tests/golden/W90/W90_G05_lint_suggest_patch/test.dtest.json
tools/teul-cli/tests/run_golden.py
```

All remaining changed paths are the already committed handoffs, fixed public
projection manifests, and session deltas for those product changes. The
reviewer must independently reproduce the path counts rather than infer them
from this request.

## Required independent checks

1. Verify every direct-parent relation from the reviewed base through the
   product fixed and handoff parent, with merge count zero.
2. Verify `docs/ssot/**` and `publish/spec/**` diff zero and v25.42 successor
   impact remains custody-only for this product target.
3. Re-run the proportional existing Rust/Python/Node suites named in each
   committed P2/P3/P4/P5/CLI handoff; do not create a new runner or pack.
4. Reproduce saved-project HEAD success, stale mismatch fail-closed, Run publish
   zero on failure, and Workbench reopen/retry behavior.
5. Reproduce CLI bootstrap/canon/run-summary failure exits and native summary
   output-directory/partial-publish custody.
6. Verify one shared runtime age/trace/unit authority and no reintroduced hidden
   fallback in the reviewed CLI workflows.
7. Verify the candidate frontdoor reaches exactly the eleven currently claimed
   workflows: `run`, `check`, `build`, `canon`, `project-normalize`,
   `project-discover`, `project-graph`, `project-symbols`, `project-lock`,
   `currentline-run`, and `lint`.
8. Verify candidate/teul parity only for migrated scoped workflows and do not
   promote the four remaining workflows.
9. Reproduce the clean projected Windows x64 build, path-clean scan, artifact
   hashes, link resolution, public-source teul exclusion, and tracked-WASM
   freshness using a clean LF materialization and external build output.
10. Verify protected process/port custody, task-owned residue zero, final clean
    review checkout, and review commit product/test/pack/WASM diff zero.

## Explicit open gates

The following are outside the requested PASS and must remain OPEN:

- `project-run`: semantic identity `ddn.project-run.v1` is fixed, but selector
  conflict behavior and `--out` overwrite versus atomic replace are not fixed;
- `view`: visible official frontdoor is not approved;
- `test`: exact public command membership and its three-mode orchestration are
  not approved;
- `repl`: private state/runtime behavior has not converged;
- whole CLI convergence, whole teul semantic authority zero, test/pack required
  teul dependency zero, physical teul deletion, and internal/deferred command
  placement;
- final executable/package/legacy alias naming;
- whole P0~P5 closure, V1 membership/readiness, rights/license, signing,
  distribution, release, activation, Owner Human Smoke, and Human PASS.

## Review custody

The sole rolling reviewer remains thread
`01a04b17-66bb-7fa3-b827-53ad450005b4`. Its previously designated worktree
`C:/Users/ddongosu/.codex/worktrees/3a1f/codex` is not present at request
preparation time. The execution owner did not create or select a replacement.
Management must rebind the same reviewer to one approved clean existing review
isolation, or explicitly resolve the missing-worktree custody, before tests or
review writes begin. Duplicate reviewer/task/worktree creation is forbidden.

Allowed reviewer commit contract after rebind:

```text
PARENT: exact request commit bound by management
DIFF: REVIEW_RESULT.md + reviewer session delta only
PRODUCT_TEST_PACK_WASM_SSOT_SPEC_DIFF: 0
MERGE_COUNT: 0
```

## Anti-meta

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED: current P2~P5 and 11-command V1 milestone becomes independently reviewable
NEW_TEST_ARTIFACT_COUNT: 0
EXISTING_TEST_REUSED_COUNT: existing handoff suites only
META_TEST_CREATED: 0
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
REVIEW_BUNDLE_TARGET: current-head P2~P5 + official CLI 11/15
```
