# GOER-R1-U1 guard fault fail-closed handoff

## Scope

`c666c20a69c48632d53eaf41d4accbe514e1c358` is the direct successor of
`970ce7df99d6e51c62485e54f875b6b3ce240669`.  It changes only
`tool/src/ddn_runtime.rs`.

The StateMachine selector now distinguishes a guard that evaluates to a normal
false result from a guard whose assertion evaluation faults.  A fault aborts
the complete candidate selection before an alternative transition can be
selected or its action can publish.  It reuses the existing
`E_STATE_TRANSITION_GUARD_REJECTED` diagnostic family; no public spelling,
wire contract, parser surface, dependency, or UI is added.

## Product-facing regression and verification

- New in-file runtime regression: a first guard references an unresolved name
  while a later guard would otherwise pass.  Before this fix, the later
  transition was selected (RED); after it, execution fails closed.
- `cargo test -p ddonirang-tool --lib state_machine_guard_fault_aborts_whole_candidate_set_without_selection -- --nocapture`: PASS.
- `cargo test -p ddonirang-tool --lib state_machine_guard_ -- --nocapture`: 5/5 PASS.
- `cargo test -p ddonirang-tool --lib state_machine_ -- --nocapture`: 10/10 PASS.
- Risk mutation changed the fault arm back to `Ok(false)`: RED (exit 101),
  selecting the alternative candidate.  The exact source SHA-256 was restored
  to `1E730CD22596BC393028E565497ED51F7865133A3B34BF0ACF931847543B7461`,
  then the focused and guard suites were GREEN again.  Residue: 0.
- `git diff --check`: PASS.

## Boundaries

This is an internal, reversible typed-runtime safety correction.  It is not a
V1 membership, readiness, release, activation, legal/right attribution, P5,
P6, Human Smoke, or Human PASS claim.  It makes no SSOT or public SPEC change
and creates no external dependency, new pack, runner, reviewer, worktree, or
branch.

The next review may bundle this with a coherent product milestone only through
the existing rolling-review custody; this handoff does not dispatch one.
