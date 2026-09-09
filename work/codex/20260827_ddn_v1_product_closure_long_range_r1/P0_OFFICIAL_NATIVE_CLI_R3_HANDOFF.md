# P0 official Native CLI R3 handoff

## Fixed target

- baseline: `ceb549ba7afceded268d316b60684bf150ff0697`
- product fixed: `dfa7d3d17b25ffbe394df7f1a44184c01844a2ae`
- product tree: `fc55f37025994b3af2f5a397caf85232c6ed0a1d`
- changed path: `scripts/build_windows_x64_public_candidate.ps1`
- live authority observed read-only: internal SSOT `v25.57.0 / RD-001~562`; public Language SPEC `v0.6.0`.

## Product correction

The public Windows candidate builder now compares the copied executable set with
the exact official set: `ddonilang.exe`, `또니랑.exe`, and `ddonirang.exe`.
It fails closed with `E_WINDOWS_CANDIDATE_OFFICIAL_ARTIFACT_SET_MISMATCH` if
any official executable is missing or an unexpected executable is present.

This preserves one shared source entry and no argv[0] semantic split. It does
not promote the compatibility alias to an additional semantic authority.

## Current-row evidence

- Build: workspace plus all three `ddonirang-tool` bin targets.
- Runtime: `tool/src/bin/ddonirang.rs` uses the shared tool/lang frontdoor.
- CI: `seamgrim-gate` calls `tests/run_v1_core_supported_ingress_w1.py` and
  the workflow contract rejects `tools/teul-cli`, `TEUL_CLI_BIN`, and
  `run_golden.py` within that required job.
- Pack/fixture: only the existing V25 supported-ingress manifest fixtures.
- Publish: the Windows candidate script builds, copies, starts, and path-checks
  all three executables; it rejects retired teul artifact paths.
- Workbench: `N/A` for this Native CLI physical row.

The historical `historical-teul-custody` job and its internal/deferred paths
remain outside this row and were neither deleted nor reclassified.

## Validation and mutation

- `python tests/run_seamgrim_workflow_contract_check.py`: PASS.
- existing `candidate_surface_is_small_and_does_not_name_legacy_cli`: PASS
  after restore.
- direct `cargo build --locked -p ddonirang-tool --bin ddonilang`: GREEN after
  exact restore.
- direct `cargo build --locked -p ddonirang-tool --bin 또니랑`: GREEN after
  exact restore.
- existing `tests/run_v1_core_supported_ingress_w1.py` was re-executed on this
  fixed target; native and WASM subprocesses completed without retained cargo,
  rustc, node, or Python test process.
- clean Windows projection produced the three official artifacts, each
  `7,146,496` bytes.

Actual mutations all restored byte-exactly with no source residue:

1. Removing `ddonilang` bin target: RED, cargo exit `101`; restored hash
   `6add9511e44acf3effc09e34f8eea040a03a5376768f78f3c1f320fe55c59e71`.
2. Removing `또니랑` bin target: RED, cargo exit `101`; same restore hash.
3. Adding a `teul-cli` CLI surface line: RED, existing bin unit failed;
   restored hash `1a0bee81bd33d9f0671fe81ea0574b750eb1ee4f429c354ca6288309046df430`.
4. Adding a real teul build invocation to `seamgrim-gate`: RED, existing
   workflow checker exit `1`; restored hash
   `3659fdfeb32eab7ee6d6e199e5587f8eea8316db22cf9930c23b37b9406292b4`.
5. Removing `ddonilang.exe` from the Windows copy list initially completed
   with only two artifacts, proving the projection gap. After the correction,
   the same mutation reaches the exact artifact-set mismatch guard; source was
   restored before committing.

## Review scope

`P0_CLOSURE_CANDIDATE_READY=YES` applies only to this official Native CLI
physical row and its D1-D4/D7-D8 rebind. The fixed target for one existing
rolling independent reviewer is `dfa7d3d17b25ffbe394df7f1a44184c01844a2ae`.

## Nonclaims

This does not close P0 as a whole, map the other 27 REQUIRED rows, delete
`tools/teul-cli`, resolve P1-P6, or claim V1 membership/readiness/release,
activation, legal clearance, or Human PASS.
