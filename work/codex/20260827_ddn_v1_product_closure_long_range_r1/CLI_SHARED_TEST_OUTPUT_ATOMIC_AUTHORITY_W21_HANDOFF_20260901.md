# DDN V1 CLI convergence — shared test output atomic authority W21 handoff

Date: 2026-09-01
Goal: existing `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1`
Status: `IMPLEMENTED_PENDING_COHERENT_MILESTONE_REVIEW`

## Authority and fixed lineage

- live internal CURRENT: v25.47.0 / RD-001~543
- public Language SPEC: v0.6.0
- successor impact: `UNAFFECTED_WITH_ADDITIVE_OUT_OF_SCOPE_SUCCESSOR`
- baseline / W20 handoff: `c6b175985c49d66afe720ee9ee2d4bc40bdf027b`
- product fixed: `753fa87c424987597ecb98fbdc6a948356a5c82a`
- product fixed tree: `a5a38d1402e0a0f8d000a53cc8302a69a8a12167`
- fixed parent: exactly `c6b175985c49d66afe720ee9ee2d4bc40bdf027b`
- merge count: 0
- prior test-workflow review `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf`
  is an ancestor and remains `PASS_TARGET_BOUND` only to fixed product
  `eba99e9d...`; this successor is not auto-reviewed.

## User workflow and exact product diff

The shared `tool::test_workflow::run_realms_test` already owns input parsing,
thread-mode selection, deterministic evaluation and result serialization. The
retained teul command is only a four-line re-export adapter. The remaining
output path nevertheless used direct `std::fs::write`, allowing an existing
result artifact to be truncated before a failed replacement completed.

W21 changes that one shared-owner call site to consume the existing
`artifact_output::write_text_artifact_atomic` authority.

Exact fixed diff:

- `tool/src/test_workflow.rs`

Diff size: 3 insertions / 1 deletion. Input, evaluator, output JSON, thread
semantics, CLI spelling and adapter source are unchanged. New public test
membership, pack, runner, checker, framework, meta-test or registry: 0.

## Verification

- shared owner focused tests: 3/3 PASS before and after mutation restore
- coherent retained teul build: PASS
- actual W78 basic fixture, threads 1 and 8: exit 0, stdout/out exact, thread
  modes exact, 378 bytes, SHA-256
  `09dfc4847b1dac2668a4b254727fede6729dcd0750e1e9f4f7d0f2119c33fd22`
- predecessor output replacement: threads 1/8 both PASS
- blocked replacement target: exit 1, target directory preserved, stdout 0,
  temp residue 0
- zero-realms: exit 1, exact `E_REALM_INPUT realm_count must be > 0`, output
  absent, stdout 0
- post-fixed reproduction: threads 1/8 exact with the same 378-byte hash and
  temp residue 0
- direct-write regression mutation: shared owner call changed back to
  `std::fs::write`; production guard RED count 1
- exact restore SHA-256:
  `23dd1614f8fad4080a324636a477e1b878dbbce247c7b591e93778ce292500d7`
- restored guard count 0 and focused tests 3/3 GREEN
- partial result publication observed: 0
- mutation residue: 0

## C0~C8 impact and anti-meta

| gate | bounded impact |
|---|---|
| C0 | historical 28+63 command custody unchanged |
| C1 | executable/package/alias decisions unchanged and OPEN |
| C2 | shared semantic authority preserved |
| C3 | public test membership remains OPEN; no command was promoted |
| C4 | shared test output direct-write authority reduced from 1 to 0 |
| C5 | bounded V1-required execution dependency state unchanged |
| C6 | retained test invocation/output determinism remains exact |
| C7 | W18~W21 current-source coherent review bundle ready |
| C8 | teul physical deletion/public retirement remains Owner-gated |

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: retained shared test output now replaces
  existing artifacts atomically and fails without partial publication.
- `NEW_TEST_ARTIFACT_COUNT`: 0
- `EXISTING_TEST_REUSED_COUNT`: 3 surfaces (shared focused tests, W78 fixture,
  shared atomic fault contract)
- `META_TEST_CREATED`: 0
- `STOP_RULE_APPLIED`: yes
- `ACTIVE_REVIEW_TASK_COUNT`: 0 executing; one existing rolling reviewer handle
  remains reusable
- `NEW_REVIEW_TASK_COUNT`: 0
- `NEW_REVIEW_WORKTREE_COUNT`: 0
- `REVIEW_BUNDLE_TARGET`: W18 check-schema + W19 retained canon + W20 retained
  project artifacts + W21 shared test output

## Nonclaims

This handoff does not decide public `test` membership, final executable or
package naming, legacy alias duration, view/repl membership, physical teul
deletion, whole CLI parity/convergence, P0~P6 closure, V1 membership/readiness,
release, activation, legal/distribution approval, Owner Human Smoke, or Human
PASS.
