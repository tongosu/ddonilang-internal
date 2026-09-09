# [DDN V1제품마감Codex -> Codex관리Work] P5 current-source Windows A/B reproducibility W17

- Persistent goal remains ACTIVE. The supplied P5 review identity
  `bc84d81d4...` proves existing reviewer custody and removes the prior
  reviewer-handle blocker classification.
- Current product baseline remained `dd859d3c...`; product/test/pack/WASM/UI,
  `docs/ssot/**`, and public SPEC changes are zero.
- Reused the W16 path-clean projection and existing Windows build script.
- Independent output roots r1/r2 produced byte-identical `ddonirang.exe`:
  7,043,584 bytes, SHA-256 `8129df4e...`, stack reserve 16 MiB, forbidden path0,
  teul artifact0.
- Reused `project_run_physics_v1.json`. With exact inspection options, r1/r2
  project-run artifacts are byte-identical: 16,488 bytes, SHA-256 `f9c2e36f...`.
- Positional start plus `--virtual` remains exit2 / `E_CLI_OPTION_CONFLICT`,
  successful partial artifact0.
- New pack/runner/meta-test/reviewer/worktree/branch: 0.
- Workspace regression before this release check was 409 PASS / 2 environment
  FAIL because this managed worktree intentionally lacks `docs/ssot`; both
  failures are `ai_prompt` test fixture/materialization dependencies, not a
  product semantic regression or whole-goal blocker.
- W13-W17 successor review remains queued to the existing rolling reviewer.
  Public membership, PathIR wire, VC17, SPEC history, legal/distribution and
  Human gates remain slice-local OPEN.
