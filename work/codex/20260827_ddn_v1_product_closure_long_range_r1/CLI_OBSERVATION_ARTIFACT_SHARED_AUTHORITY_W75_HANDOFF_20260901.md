# CLI observation artifact shared authority W75 handoff

## Status and product value

- status: `CLI_OBSERVATION_ARTIFACT_SHARED_AUTHORITY_W75_IMPLEMENTED_UNDER_REVIEW`
- goal: existing `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1`, ACTIVE
- user workflow 1: `alrim registry` scans DDN alarm variants and publishes one deterministic conflict-checked registry through shared product authority.
- user workflow 2: `dotbogi case` preserves view/event/state-write boundaries and now publishes output, after-state and report as one all-or-nothing artifact set.
- release value: two more private teul semantic owners are removed, and a reproduced partial-publish defect is closed without changing command membership or wire spelling.

## Authority and exact lineage

- internal CURRENT: v25.47.0 / RD-001~543, read-only
- public Language SPEC: v0.6.0, read-only
- branch: `codex/ddn-v1-p1a-core-supported-ingress-w1-20260829`
- baseline/W74 handoff: `27a59e14d28c089afe97102a196f62dbe58f8140`
- product fixed: `d67889db1deade1ce7e4f41d03f47c3b78708947`
- product fixed tree: `e74181ca789452ab9f55a63fb9b99efbf0894b6c`
- direct lineage: yes
- merge count: 0

The coherent review bundle is:

1. W74 certificate shared authority fixed `146ac3d46b536967e4c34e02f67bcd54263690a4`
2. W74 handoff `27a59e14d28c089afe97102a196f62dbe58f8140`
3. W75 alrim/dotbogi shared authority and atomicity fixed `d67889db1deade1ce7e4f41d03f47c3b78708947`
4. this W75 handoff direct successor

Previously bound review custody `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf` and P5 review `bc84d81d4faa55974975bdb7ec60cb18d9a7ebda` remain ancestors and are not broadened.

## Exact product paths

- `tool/src/alrim_workflow.rs`
  - shared product owner for registry scan, variant/schema identity, deterministic order and atomic publication
  - Git blob `8b2ac66810526e10a9d68584f248f5aadc2f5b65`, 18,129 Git bytes
- `tool/src/dotbogi_workflow.rs`
  - shared product owner for case decode, view/event projection, state-write prohibition, roundtrip and atomic artifact set
  - Git blob `102c2e540778c13629241f475e5f1d3787e0049d`, 19,639 Git bytes
- `tool/src/lib.rs`
  - host-only shared module exports
  - Git blob `4c1d6e0e27afdd25d1c712733600b3386057d913`
- `tools/teul-cli/src/cli/alrim.rs`
  - retained 3-line adapter, private functions 0
  - Git blob `74d499549269f04515329e17cbbcf56d813f9f0b`
- `tools/teul-cli/src/cli/dotbogi.rs`
  - retained 3-line adapter, private functions 0
  - Git blob `08e2339b91b37c7e643f5d33d4f88163de3dd931`

No parser, runtime, value, public command, executable/package name, docs/ssot, public SPEC, tracked WASM or visible UI path changed.

## Product RED to GREEN

### Authority RED

Baseline:

- private teul product functions: alrim 1 + dotbogi 1 = 2
- corresponding shared tool owner files: 0

Fixed:

- private teul product functions: 0
- shared tool product functions: 2
- existing main dispatch consumes the retained adapters, which re-export only the shared authority

### Partial-publish RED

Using the fixed baseline executable, `dotbogi case` was invoked with valid output and after-state targets plus a report target occupied by a directory.

- exit: 1 / `E_SHARED_ARTIFACT_OUTPUT_TARGET_NOT_FILE`
- output published: yes
- after-state published: yes
- report published: no
- result: actual partial-publish RED

Fixed behavior validates all selected targets and publishes the three serialized payloads through `write_text_artifacts_atomic`:

- exit: 1 with the same failure identity
- output published: no
- after-state published: no
- report published: no
- partial publish count: 0

Successful baseline/fixed bytes remained exact for all four checked artifacts:

- empty-root alrim registry SHA-256 `4d8549f72e44c88abd76829b72accddca708d94b2d00f076cc129e56eb7e6dc3`
- dotbogi output SHA-256 `1fcf2ec967d3a73fd29af87b63cf08606f70eca50b42e8cd0878bcbd408d22a9`
- dotbogi after-state SHA-256 `7b5a93bdb871da149e6310427579076d03754875e79ed55484a602fc9ccf7c29`
- dotbogi report SHA-256 `931bd7966666ec1855a4e9ee0a69d0129b9718c62c4dc18141558301da931a5c`

## Tests, determinism, mutation and residue

- `ddonirang-tool` dotbogi unit selection: 3/3 PASS
- `teul-cli` build: PASS
- dotbogi smoke/event-roundtrip/write-forbidden existing packs: PASS
- actual dotbogi success with output/after-state/report: PASS
- actual dotbogi blocked-target fault: PASS, partial publish 0
- actual alrim registry with two variants: PASS
- alrim repeat registry bytes: exact, SHA-256 `58402ec36029acca49d0a8d2592700b81ada7f8902d5a21fff69775db08caeb7`
- conflicting alrim variant schemas: deterministic `E_ALRIM_VARIANT_CONFLICT`, output 0

Risk mutation replaced the shared atomic set with sequential single-file writes:

- RED: blocked report target left output and after-state published
- exact restore: `tool/src/dotbogi_workflow.rs` checkout SHA-256 `6e0edd763081aa3515023e966506b564f59608d35630e1150915d951b0f474f0`
- GREEN: same fault left output/after-state/report count 0
- mutation/build/test residue: 0

No new pack, runner, checker or meta-test was created. Existing product packs and direct CLI workflows were reused.

## C0~C8 and frontdoor state

| Gate | Actual W75 state |
|---|---|
| C0 | Historical 28 tool + 63 teul = 91-command registry remains custody; membership transition 0. |
| C1 | V1 core 15 whole convergence is not re-declared; individual previously bound owners remain fixed-target custody. |
| C2 | Certificate, alrim registry and dotbogi case now have shared `tool` product owners. |
| C3 | No public executable or command-membership claim; retained CLI reachability is preserved. |
| C4 | Private teul semantic/fallback authority is 0 for the three W74/W75 workflows. Other physical/internal custody remains nonzero. |
| C5 | Repository-wide required dependency0 remains OPEN; historical proof bundle prerequisite still stops at `E_SHARED_RUNTIME_OPTION_UNSUPPORTED`. |
| C6 | W75 successful bytes are preserved; dotbogi failure atomicity and alrim deterministic conflict failure pass. |
| C7 | Public-source/release projection remains separately gated; P5 materialization review PASS custody is preserved. |
| C8 | `tools/teul-cli`, binary and package remain physical custody; deletion/retirement approval is not inferred. |

- native retained CLI: PASS for W74/W75 workflows
- WASM: not applicable to these host filesystem modules; no export added
- Workbench: existing structured consumer/UI paths unchanged; no visual or semantic parity claim added
- semantic field loss introduced: 0
- hidden fallback introduced: 0

## Review and nonclaims

- existing rolling reviewer: `01a04b17-66bb-7fa3-b827-53ad450005b4`
- new reviewer/task/worktree/branch: 0/0/0/0
- review target: the exact W74+W75 fixed/handoff lineage above, after management dispatch
- independent PASS: not self-declared

The four pre-existing task-owned untracked session files remain byte-identical and unstaged. This handoff does not claim public alrim/dotbogi membership, public PathIR ingress, whole PathIR P1, VC17 exact landing, whole C0~C8 or P0~P6 closure, repository-wide teul authority/dependency zero, physical retirement, V1 membership/readiness/release, activation, legal approval, Owner Human Smoke or Human PASS.
