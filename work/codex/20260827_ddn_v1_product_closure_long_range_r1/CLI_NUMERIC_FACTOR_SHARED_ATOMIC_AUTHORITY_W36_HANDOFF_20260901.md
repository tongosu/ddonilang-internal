# CLI numeric factor shared atomic authority W36 handoff

## Identity and authority

- Live authority: internal SSOT v25.47.0 / RD-001~543; public Language SPEC v0.6.0.
- Baseline: `a081f0b7de81d5078636e706ddf7aafc7e364155`.
- Baseline tree: `3a660a548e63d94e86df8b85aadba20904742e2d`.
- Product fixed: `f35437f2fe47458dc0e7711ee218f1ddfebeb46b`.
- Fixed tree: `aa4b2aff51f18c13938f4b2eda217b1be41960b3`.
- Direct parent: yes. Merge count: 0.
- Review commit `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf` is already in the fixed ancestry and was not rebound or duplicated.

## User workflow and product change

The existing native `numeric factor` complete and step/resume workflows now consume `ddonirang_tool::numeric_workflow`. The retained `teul-cli` module is a one-line adapter and no longer owns factor orchestration, deterministic serialization, or artifact publication semantics.

Complete mode publishes `factor_result.detjson` and `factor_job.detjson` as one atomic artifact set. Every target is preflighted, all replacement predecessors are backed up, and any staging, backup, or publication failure restores the complete predecessor set. Step/resume job output consumes the existing shared single-artifact atomic writer. Command spelling, input, result/job schema, and numeric kernel semantics are unchanged.

Exact product paths:

- `tool/src/artifact_output.rs`
- `tool/src/numeric_workflow.rs`
- `tool/src/lib.rs`
- `tools/teul-cli/src/cli/numeric.rs`

## Product RED to GREEN

Baseline reproduction used an existing `factor_result.detjson` containing the exact 11 bytes `PREDECESSOR` and a directory at the second target `factor_job.detjson`. The old complete command exited 1 but overwrote the first result before failing the second write: actual partial publish RED.

At the fixed target the same condition exits 1 with `E_NUMERIC_FACTOR_JOB_WRITE E_SHARED_ARTIFACT_OUTPUT_TARGET_NOT_FILE`, keeps the first file byte-identical as `PREDECESSOR`, and leaves artifact-set staging residue 0. An injected failure immediately before the second publication also restores both predecessor files and ends with residue 0. Exact restore is exercised in the shared product helper, followed by all five focused artifact-output tests GREEN.

Two successful complete-mode executions for input `91` produced identical identities:

- result SHA-256: `753a06ac292c806552deee26ba48a518505086334db133d01ec2b2c1427b491b`
- job SHA-256: `992c2ac6148efcf2761d478ba3925a90be5fff179bec403e9102ab87b169b906`
- artifact-set residue: 0

## Verification

- Shared artifact-output focused: 5/5 PASS (2 prior cases plus 3 product-infrastructure cases in the existing file).
- Existing numeric factor golden packs: 2/2 PASS.
- Existing numeric factor resume checker: PASS.
- Existing numeric kernel crate: 3/3 PASS.
- Existing tool numeric route/resource/diagnostic tests: 3/3 PASS when invoked as exact `--lib` targets.
- Existing teul numeric-filtered regression: 13/13 PASS.
- Tool library regression: 560/562 PASS. The same two isolated-worktree `docs/ssot` absence failures remain in `ai_prompt`; W36 regression 0.
- The existing route-diagnostic wrapper itself is environment-blocked because workspace integration-test compilation resolves two `ddonirang_lang` instances. Its exact three intended library tests pass directly; no product source was changed for this environment event.
- `cargo build --manifest-path tools/teul-cli/Cargo.toml --offline`: PASS with the dedicated W36 target directory.
- `git diff --check` and formatting check on the three changed standalone Rust source files: PASS.
- New pack/runner/checker/meta-test files: 0/0/0/0.

## C0 through C8 bounded state

| Gate | Fixed-target state |
|---|---|
| C0 | Historical 28 tool + 63 teul = 91 command inventory remains custody; no membership transition. |
| C1 | `ddn.project-run.v1` remains fixed; executable/package/alias gates are unchanged. |
| C2 | Numeric factor complete/step/resume orchestration and artifact authority now have one shared tool owner. |
| C3 | Public `test`/`view`/`repl` and numeric command membership remain OPEN. |
| C4 | Private teul numeric factor orchestration/value-serialization/artifact fallback authority is 0 for this workflow; other INTERNAL/DEFERRED custody remains nonzero. |
| C5 | Previously bounded V1-required build/test/pack/publish teul execution dependency remains 0; historical/internal references remain custody. |
| C6 | Two-file success is deterministic and second-target failure has partial publish 0. WASM and Workbench add no alternate semantic reconstruction for this native-only command workflow. |
| C7 | Prior target-bound reviews remain preserved; W35~W36 await one coherent rolling-review dispatch by management. |
| C8 | Teul public binary/package retirement and physical deletion remain Owner-gated. |

## Separate frozen gaps and next safe work

`story`/`timeline` still depend on private teul Geoul bundle authority and their current golden prerequisites fail at the pre-existing `E_SHARED_RUNTIME_OPTION_UNSUPPORTED` boundary. `view` remains coupled to unresolved web/console/UI physical contracts. Those slices were not modified and are not an overall V1-goal blocker.

The next safe candidate is another approved internal/deferred command whose complete semantic seam can move into `tool` without deciding public membership, executable naming, or UI contracts. Review target remains the existing rolling reviewer and management dispatch only; new reviewer/task/worktree 0.

## Status and nonclaims

Status is `IMPLEMENTED_UNDER_REVIEW`. This handoff does not claim whole C0~C8 closure, repository-wide teul authority/dependency 0, physical retirement/deletion, PathIR public-contract closure, VC17 exact landing, P0~P6 closure, V1 readiness/release, activation, legal approval, or Human PASS.
