# DDN V1 CLI integration / teul-cli retirement W1 session delta

Date: 2026-08-30
Session: DDN V1제품마감Codex
Goal: existing DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1 persistent goal

## Request rebind

The user redirected the next safe product vertical to V1 CLI integration and
`teul-cli` retirement. The existing session, product worktree, branch and
single writer were reused. No new goal, task, branch, worktree, control tower,
reviewer or review worktree was created.

The live read-only authority had advanced from the requested v25.35 baseline to
Owner-approved v25.40.0 / RD-001~515. Public SPEC remains v0.6.0. The v25.40
direction is additive for this slice: one shared lang/runtime frontdoor,
no legacy compatibility alias for external-user count 0, and command/golden
migration before physical predecessor deletion.

## Fixed result

```text
WORKTREE: I:/home/urihanl/ddn/codex/build/worktrees/ddn-p-v1-project-ux-r2-census-r1-20260828
BRANCH: codex/ddn-v1-p1a-core-supported-ingress-w1-20260829
BASELINE: ee9d28bb45e04c9d7b7247d790509dbe0d4bd799
PRODUCT_TEST_FIXED: 274183623f43c526975c7402ffa0fdf6e0d11e66
PUBLIC_PROJECTION_CONTRACT_FIXED: 31f00c58993dd7ba153de7839c5c1a99dbede023
MERGES: 0
```

The product fixed commit adds the small shared-authority `ddonirang` candidate,
extends the existing P1-A supported-ingress runner, and changes the Windows
candidate builder to collect only `ddonirang.exe`. The projection contract
removes `tools/teul-cli` and projects 169 files from the product fixed commit.

Verification summary:

- initial no-bin RED, then candidate bin unit 2/2 PASS
- supported ingress native 7, native/WASM exact 2, tracked cases 10,
  official CLI positive 3 / negative 3 PASS
- tool lib 527/527 PASS
- historical teul source `cargo check` PASS
- projection/remap/validator 61/61 PASS; actual projection validation PASS
- fixed candidate WASM path scan 0; tracked write 0
- Windows A/B one-file builds PASS; byte-identical `ddonirang.exe`
- `teul-cli` source/artifact count in public candidate 0
- new pack/runner/checker/meta-test/reviewer/worktree/branch 0

## Custody and next owner

Known pre-existing task-owned untracked session/census documents were preserved
byte-for-byte and unstaged. Shared dirty root and `docs/ssot/**` were untouched.
The existing management-owned rolling reviewer is the next review owner; this
writer did not dispatch or wake it.

Physical `tools/teul-cli` deletion, exact command/golden migration, final public
executable/installer identity, tracked-WASM refresh, P5 closure, release and
Human gates remain OPEN.

## Project-normalize first migration vertical

The same goal, branch and worktree continued from `294fc227`. Live authority was
revalidated as v25.40.0 / RD-001~515 with public SPEC v0.6.0. The current source
still contains the historical 28 `ddonirang-tool` + 63 `teul-cli` command
identities. The later candidate frontdoor is tracked separately and now reaches
four of the 15 historical core migration candidates.

`project-normalize` was absent at the candidate frontdoor (RED exit 2,
`E_CLI_COMMAND_UNKNOWN`) and was routed directly to the existing
`tool::local_project::normalize_virtual_project_source_json` authority. The
existing local-project CLI/WASM runner was switched from teul to the candidate;
no pack, runner, checker, meta-test, reviewer, worktree, branch or goal was
created.

Fixed result:

```text
PARENT: 294fc227d7da17fd54bb90e3efeca83572e85fcd
PRODUCT_TEST_FIXED: e64e5163e0ca47a7818726531ccdc2a0eff14bfb
FIXED_TREE: 4e5f3fc8f98316640c4dd277c1b64fb27c734987
DIFF: tool/src/bin/ddonirang.rs + existing local-project parity runner
```

Verification: candidate unit 3/3, local-project 40/40, existing CLI/WASM parity
runner PASS, P1-A supported ingress native 7 / native-WASM 2 / tracked 10 /
candidate CLI positive 3-negative 3 PASS. Current teul and candidate produced
byte-exact positive output and representative structured failure JSON with the
same exit 2.

Remaining repository residue is explicit: private parser 7 files, runtime 7,
core/value 11; CI teul reference 1 file; test references 190 files, pack 367,
publish 50 overall and publish/v1 0. Physical deletion and broad retirement
remain unauthorized and OPEN.

## Project inspection/lock migration vertical

The fixed product lineage continued linearly from `fdf4993488d09c8b9a945d2a7be10c66b1910213`.
At that baseline `ddonirang project-graph` returned
`E_CLI_COMMAND_UNKNOWN`, exit 2. One coherent adapter vertical moved
`project-discover`, `project-graph`, `project-symbols` and `project-lock`
to the existing `tool::local_project` product authority without adding a new
parser/runtime/value/canon/fallback or test family.

```text
PRODUCT_TEST_FIXED: a4ca66171df3b2cbc2700ab73d867c01bb76dcb6
FIXED_TREE: a5023dfbbb4a3a16fce42d8897071db547e0658b
DIRECT_PARENT: fdf4993488d09c8b9a945d2a7be10c66b1910213
FIXED_DIFF: tool/src/bin/ddonirang.rs + existing local-project graph runner
```

Verification at the clean fixed head: candidate unit 4/4, reused project
inspection/lock checks 8/8, current teul/candidate representative byte parity
6/6 with three deterministic repeats, normalization CLI/WASM PASS and shared
local-project library 40/40. The historical runner's absent docs reference and
pre-existing project-run text materialization mismatch remain explicit; they
were not converted into product evidence or bypassed in committed code.

C3 shared semantic stdout reachability is now 8/15. The project-run artifact
still embeds `teul-cli project-run`, so its neutral semantic identity versus
public executable spelling is a concrete Owner/detail gate. Repository CI/test/
pack/publish explicit teul-reference counts remain 1/190/367/50, with
`publish/v1/**` 0. New pack/runner/checker/meta-test/reviewer/worktree/branch/
goal count remains 0. The 33 internal/deferred commands and physical
`tools/teul-cli` tree remain custody only; no deletion or public promotion was
performed.

## Shared build migration vertical

The remaining core-handler audit showed that historical `build` and `check`
call the same private handler, while `currentline-run/view/test/lint/repl` still
depend on private execution, UI, harness or parser semantics. The next safe
product RED was therefore candidate `build`, which returned unknown command at
baseline `3b5630b0`.

`build` was added as an exact consumer of the existing supported-profile shared
analysis used by candidate `check`; no compiler, schema writer, parser or
fallback was introduced. The existing P1-A runner was extended in place.

```text
PRODUCT_TEST_FIXED: b4e738b9dc551b1079c79da9e41269c77f99c02c
FIXED_TREE: 75c1087ac82a66229f9142073b84b567e60e46b1
DIRECT_PARENT: 3b5630b0b7599afd0771174b6abcabad6e161224
FIXED_DIFF: tool/src/bin/ddonirang.rs + existing P1-A runner
```

Build/check payload parity was byte-exact, build repeated 3/3 identically and
missing profile failed closed. In a fresh external Cargo target, the reused
P1-A runner passed native 7, native/WASM 2, tracked-WASM 10 and candidate CLI
positive 4/negative 4. A prior cross-checkout target produced duplicate-crate
E0271/E0308 and was classified as environment contamination after the clean
target GREEN.

C3 candidate reachability is now 9/15. The six remaining core commands require
project-run wire identity, shared stateful execution, visible view behavior,
test-command membership or shared lint authority decisions. No new FILE_OWNER,
test artifact, reviewer, worktree, branch or physical teul deletion was
created.


## teul check/build shared adapter vertical

The next safe retirement vertical started from `4a192db142675ab727c557eba382bc6046882e7b`.
The historical public-like `check` and `build` entries previously defaulted
to teul's private parser/type/schema path and rejected an explicit supported
profile in clap.

```text
PRODUCT_TEST_FIXED: 268dbd1d0d65464ad8faef9db16bd98ae5912893
FIXED_TREE: 159ace0dfa1e23b82f5fa716b00670b1941ff617
DIRECT_PARENT: 4a192db142675ab727c557eba382bc6046882e7b
FIXED_DIFF: tools/teul-cli/src/main.rs + cli/check.rs + existing golden runner
```

Both entries now require an explicit supported profile for the shared
`tool::source_analysis` path. Omission fails closed. The old path survives
only as a hidden `--legacy-internal` custody switch used by existing
historical golden cases. Candidate/teul exact parity is 12/12 over six reused
P1-A fixtures and two command spellings; targeted teul unit is 1/1; affected
W109 build/check cases are 6/6. New test artifacts, meta-tests, reviewers,
worktrees and branches are zero.

This closes no broad gate: explicit internal authority, CI/test/pack/publish
references, the six remaining candidate commands, physical deletion and
independent review are still OPEN.

## Currentline shared-frontdoor migration vertical

The next product-facing RED at baseline `38a9f97b96cab41bc1061bcad6e4272eca51f6ab`
was candidate `ddonirang currentline-run`, which failed with
`E_CLI_COMMAND_UNKNOWN`. The existing currentline compiler was given a private
profile selection: its legacy output remains unchanged for existing custody,
while the new explicit candidate emits typed V25 source and consumes the shared
supported-profile runtime. The matching explicit-profile WASM candidate was
added and the existing parity runner was switched from teul to `ddonirang` only
for currentline mode.

```text
PRODUCT_TEST_FIXED: 7ddae25dafa4cb92dbb23638133c0e26101b61bd
FIXED_TREE: 48524cae8d41be1a917ea1a94c04d346e63d98e6
DIRECT_PARENT: 38a9f97b96cab41bc1061bcad6e4272eca51f6ab
FIXED_PATHS: 10 exact lang/tool/runner/tracked-WASM paths
```

Candidate unit 6/6, lang currentline 5/5, lang lib 366/366, tool lib 527/527,
official freshness and generated-JS syntax passed. Two existing fixture cases
passed native/WASM exact state hash, final row, full value JSON and output-log
parity. Missing/unknown profile, invalid context and output-parent failures are
fail-closed; a two-output fault preserved the old target and left no sidecar.
No pack, runner, checker, meta-test, reviewer, worktree, branch or goal was
created.

C3 candidate reachability is now 10/15. The historical teul currentline path
still returns `E_SHARED_RUNTIME_OPTION_UNSUPPORTED`, so private runtime and
required dependency removal remain OPEN. Explicit reference custody is 190
test files, 367 pack files, 50 publish files (publish/v1 0) and two CI/script
files. Physical teul retirement, deletion and all broad V1/release/Human gates
remain unclaimed.

## Lint shared-authority migration and project-run contract gate

At baseline `c0bda454a22df9cf00108f4bd8d0f8117d0637dd`, candidate `lint`
returned `E_CLI_COMMAND_UNKNOWN`. The fixed product commit
`64abb938b7eccf38ce71213ec03dfec2dd15fd5e` (tree
`bfb1482af0055abe6a1e9a8d057ba852664fe866`) introduced one shared
`tool::lint` authority backed by the language lexer and source analysis. Both
candidate and teul now consume it; historical teul golden custody is explicit
and hidden rather than a default public fallback.

Shared lint tests passed 4/4, candidate tests 7/7, full tool library 531/531
and existing W90 G05 passed. Actual V25 candidate/teul patch bytes were exact
at SHA-256 `c9dc90e85e68b92aef4fadb153597dd48346d8f53e40326e44a1e29b707ac38f`.
Missing/unknown profile and output-directory faults failed closed with partial
publish 0. New pack/runner/meta-test/reviewer/worktree/branch count is zero.

Owner bound the versioned executable-neutral `project-run` semantic identity
as `ddn.project-run.v1`. Implementation was stopped before mutation because
the existing teul frontdoor silently ignores disk selectors when `--virtual`
is also supplied, and because direct-overwrite versus atomic `--out` failure
semantics are not fixed by an executable test/pack. The recommended contracts
are conflict fail-closed plus atomic final artifact replacement; both await
Owner detail approval. Candidate reachability is 11/15 and all broad CLI,
retirement, release and Human gates remain OPEN.
