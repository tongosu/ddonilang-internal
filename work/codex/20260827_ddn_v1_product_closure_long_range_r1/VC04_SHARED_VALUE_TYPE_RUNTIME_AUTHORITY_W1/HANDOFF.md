# VC04 Shared Value / Type / Runtime Authority W1 — Consolidated Handoff

## Fixed identity

- authority: internal SSOT `v25.22.0 / RD-001~469`, public SPEC `v0.6.0` (read-only)
- baseline: `83fdf911ea7a59c44ae6aac541eb0b2b4e3f3a8e`
- product/test fixed HEAD: `163f14b47180ffd84312fb6609e8ce721c02acc7`
- fixed tree: `868b402622840d4c220b019118adafd5458e17cf`
- direct parent: baseline exactly
- merge count: `0`
- changed paths: exact 10 paths; no `docs/ssot/**`, `publish/spec/**`, visible UI, public command spelling, or public membership change

## User workflow changed or unblocked

An explicit `v1-core-v25` program that supplies a value of the wrong type now
uses one language-core value/type authority and returns the same structured
failure identity through native, tracked WASM, and the official `teul-cli` run
adapter:

- code: `E_RUNTIME_TYPE_MISMATCH`
- offending field: `값`
- expected: `수`
- actual: `글`
- partial result/output publication: `0`

Before this slice, the tool runtime privately owned `TypeRef` matching and the
official CLI collapsed this failure to generic `E_RUNTIME_EXECUTION` with empty
structured fields.

## Product convergence

1. `lang::runtime::{check_value_type, value_type_name, TypeMismatchDetail}` now
   owns runtime value/type identity, including aliases, units, numeric packs and
   nested List/Set/Map element identity.
2. `tool::ddn_runtime` consumes that language-core authority and no longer keeps
   a second matcher/type-name implementation.
3. `EvalError::TypeMismatch` preserves the existing Korean message while
   carrying typed pin/expected/actual fields to `runtime_surface`.
4. Native supported-profile, tracked WASM and official `teul-cli` frontdoors
   consume the same tool runtime diagnostic.
5. Existing public spelling, AST, parser/canon authority and default ingress are
   unchanged. No hidden PreV25 retry or test-only lowering was introduced.

The private `tools/teul-cli/src/runtime/eval.rs::value_type_name` remains legacy
internal custody outside the official run path. It is not promoted as supported
authority, and whole legacy-engine deletion/convergence is not claimed here.

## RED to GREEN

- authority RED: the new language-core nested collection identity test failed to
  compile because `check_value_type` and `value_type_name` did not exist in
  `lang::runtime`; after convergence it is GREEN.
- frontdoor RED: official `teul-cli` returned `E_RUNTIME_EXECUTION` and null
  structured fields for an actual type mismatch; after the typed error path it
  returns exact `E_RUNTIME_TYPE_MISMATCH / 값 / 수 / 글`.
- one attempted native-host call of the error-returning wasm-bindgen wrapper
  aborted at `JsValue::from_str` because wasm-bindgen error conversion is not
  implemented on non-wasm32. This is an environment/test-invocation event, not a
  product result. The invalid host-only assertion was removed; actual tracked
  WASM execution below is GREEN.

## Verification

- `ddonirang-lang --lib`: `366/366 PASS`
- `ddonirang-tool --lib`: `525/525 PASS`
- existing runtime type-check pack tests: `3/3 PASS`
- official `teul-cli` structured type identity: `1/1 PASS`
- supported-profile native: `7/7 PASS`
- native/WASM success payload exact: `2/2 PASS`
- tracked-WASM supported-ingress cases: `10/10 PASS`
- supported-ingress deterministic repeats: `4`
- official tracked-WASM freshness: `PASS`
- reused VC06 workflow: `GREEN 7 / RED 0 / PRODUCT_GAP 4`, native/WASM exact
  `11/11`, deterministic repeats `3`, local-project CRLF unit `PASS`
- `git diff --check`: `PASS`

Tracked WASM internal-candidate identity:

- `ddonirang_tool_bg.wasm`: `5,561,603 bytes` /
  `74e935d194173bb3199bd7573d320742ca928cd5899c6a4567b3b065b4bbe170`
- `ddonirang_tool.manifest.detjson`: `19,550 bytes` /
  `d25f1ef349dd34fdaac0337a2e1f21bbda7f0cbe4f603fa7d30ef8e9c7cb73af`

This refresh is a fixed internal candidate, not final tracked-WASM promotion or
release activation.

## Anti-meta and review consolidation

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: supported source type failures retain
  one authority and exact structured identity across product frontdoors.
- `NEW_TEST_ARTIFACT_COUNT`: `0` new runners/frameworks; one fixture was added
  to the existing supported-ingress pack and existing Rust/JS tests were extended.
- `EXISTING_TEST_REUSED_COUNT`: `7` test groups (lang, tool, type pack,
  teul-cli, supported ingress, freshness, VC06 workflow/CRLF).
- `META_TEST_CREATED`: `0`.
- mutation/tamper harness added: `0`; the two direct product REDs were sufficient.
- `STOP_RULE_APPLIED`: yes.
- `NEXT_PRODUCT_DECISION_ENABLED`: one rolling review can now judge the coherent
  VC06 supported canon + VC12 collection authority + VC04 value/type/runtime
  authority product milestone.
- `ACTIVE_REVIEW_TASK_COUNT`: `0` for this milestone before management dispatch.
- `NEW_REVIEW_TASK_COUNT`: `0`.
- `NEW_REVIEW_WORKTREE_COUNT`: `0`.
- `REVIEW_BUNDLE_TARGET`: VC06 fixed `429c8dec3b1a8022005552f2eb1de050991c8e0e`
  + VC12 fixed `2a83ec409fedd00b9f7642362fe55bf72f00b583`
  + VC04 fixed `163f14b47180ffd84312fb6609e8ce721c02acc7`, reviewed at this handoff successor.
- `REVIEW_NEEDED_NOW`: yes; the bundle changes shared canon, collection and
  runtime type authorities plus tracked WASM behavior. Management should reuse
  rolling reviewer thread `01a04b17-66bb-7fa3-b827-53ad450005b4` and its existing
  clean review worktree only.

## Protected custody and nonclaims

- protected server/port/browser/process start, stop, restart or kill commands: `0`
- final observed TCP 8787 listener: `0`
- final task cargo/rustc/python process residue: `0`
- protected Node processes were not modified; final observed count: `16`
- VC17 untracked custody remains byte-preserved and unstaged
- product paths outside the 10 fixed paths, SSOT, SPEC and visible UI diff: `0`

Status: `VC04_SHARED_VALUE_TYPE_RUNTIME_AUTHORITY_IMPLEMENTED_UNDER_REVIEW_BUNDLE_PENDING`.

VC04/VC06/VC12 closure, P1-A/P1/V1 membership or readiness, public command or
Workbench default ingress, release, activation, legal status, Owner Human Smoke
and Human PASS remain OPEN.
