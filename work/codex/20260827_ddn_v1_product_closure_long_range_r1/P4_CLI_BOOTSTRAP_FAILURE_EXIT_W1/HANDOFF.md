# P4 CLI bootstrap failure exit W1 — handoff

## Status and authority

- Status: `IMPLEMENTED_PENDING_REVIEW`
- Internal CURRENT: `v25.35.0 / RD-001~490`
- Public Language SPEC: `v0.6.0`
- Baseline: `a5225a3a4c42621365bfbd9fc9e835c811076cae`
- Product/test fixed HEAD: `174d7312e8773630fafc2ca0a5ff4fd0e5486531`
- Product/test fixed tree: `a7f76cf9f9cbd9b863f800be4745026f1539012f`
- Direct parent and merge count: exact / 0

## User-facing blocker and correction

The official `ddonirang-tool` executable printed a required project-policy/SSOT
bootstrap failure and produced no requested schema artifact, but returned exit
code 0. Release automation could therefore accept a command that never reached
the requested product operation.

The correction changes only `tool/src/main.rs`:

- invalid `--lang-mode` fails with exit 2;
- project-policy/bootstrap failure fails with exit 1;
- successful help remains exit 0.

No diagnostic spelling, project policy, parser/runtime behavior, command
membership or public name changed.

## Product RED -> GREEN

Direct executable:
`I:/home/urihanl/ddn/codex/build/test-targets/ddn-v1-p4-gb-c84b6d83/debug/ddonirang-tool.exe`.

Baseline RED:

```text
command: build-schema pack/age2_kernel_smoke_v1/input.ddn <external-output>
diagnostic: failed to read required legacy SSOT file
requested output exists: false
exit: 0
```

Fixed GREEN/fail-closed:

```text
same project-policy failure exit: 1
requested output exists: false
unsupported --lang-mode exit: 2
help exit: 0
```

Regression:

- `cargo build -p ddonirang-tool`: PASS
- `cargo test -p ddonirang-tool --lib`: 527/527 PASS
- `git diff --check`: PASS

No new test, runner, pack, checker, mutation harness, framework or meta-test was
created. The real executable baseline failure supplied the RED.

## Scope boundary

This fixed slice covers pre-dispatch language-mode and required project-policy
bootstrap failures. Several historical subcommands still contain later
command-local error branches that print an error and return normally. Those
branches were not exercised or promoted by this slice and remain a separate P4
failure-exit audit/correction surface.

Product/test/pack/tracked-WASM/UI/SSOT/SPEC diff outside `tool/src/main.rs`: 0.

## Review and anti-meta checkpoint

- Bundle with the existing P4 runtime-default and unit-registry corrections in
  one coherent rolling-review milestone; writer created reviewer/worktree 0.
- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: CLI automation can no longer accept a
  project command that failed before dispatch.
- `NEW_TEST_ARTIFACT_COUNT`: 0
- `EXISTING_TEST_REUSED_COUNT`: 527 plus three direct executable checks
- `META_TEST_CREATED`: 0
- `STOP_RULE_APPLIED`: yes
- `NEXT_PRODUCT_DECISION_ENABLED`: independent review can assess the coherent
  P4 bootstrap/runtime authority milestone before broader command-local failure
  closure.

## Nonclaims

No independent PASS, whole CLI/P4/P5 closure, Windows package/RC promotion,
V1 membership/readiness, release, activation, Owner Human Smoke PASS or Human
PASS is claimed.
