# CLI teul Windows artifact retirement guard W87 handoff

STATUS: `TEUL_CLI_WINDOWS_ARTIFACT_RETIREMENT_GUARD_IMPLEMENTED_UNDER_REVIEW`

## Fixed lineage and scope

- Authority: internal v25.49.0 / RD-001~543; public Language SPEC v0.6.0.
- Baseline: W86 handoff `b9cbb67244d14ecaf051bf12976b062293be7f97`.
- Product fixed: `181d0cb203d06ef85d48051b698dc4dd535c8c3c`.
- Fixed tree: `61f45a0369f78e45d80ae2c9ec6eab5de6399fde`.
- Direct parent: yes; merge count: 0.
- Exact changed path: `scripts/build_windows_x64_public_candidate.ps1`.
- Product source, tests, packs, tracked WASM, UI, Workbench, SSOT and public SPEC diff: 0 outside that script.

## User and release value

The official Windows x64 public-candidate builder now fails closed if its
artifact tree contains a `teul-cli` package, directory, executable, archive, or
other `teul-cli`-prefixed target. This enforces the already approved V1
retirement boundary at the actual artifact-assembly seam without selecting a
new public executable name, deleting private historical custody, or promoting
INTERNAL/DEFERRED commands.

## RED, mutation, restore and GREEN

- Pre-fix RED: an isolated copy of the baseline builder was made to copy the
  built executable as `teul-cli.exe`; the builder returned exit 0 and published
  both `ddonirang.exe` and `teul-cli.exe`.
- Pre-fix published executables: 2; each 7,043,072 bytes with SHA-256
  `7a638db296da098e65cf573484ef9d6d66af2ca564de3bace23240a4399950c5`.
- Baseline script exact restore SHA-256:
  `7f68426350aa966c442633747f97d6094205fa722b14246778c22d4fb915f74d`.
- Post-fix controlled mutation: the same `teul-cli.exe` injection returned
  nonzero with `E_WINDOWS_CANDIDATE_RETIRED_TEUL_ARTIFACT: teul-cli.exe` before
  candidate success.
- Fixed script exact restore SHA-256:
  `885fdae4448b13bec900b75314219fcaa1e8ce0d0f68e1d047d191155b2dc8c3`.
- Clean fixed-target GREEN: `WINDOWS_X64_PUBLIC_CANDIDATE_BUILD_PASS`; artifact
  count 1, `teul-cli` artifact count 0, `ddonirang.exe` 7,043,072 bytes,
  SHA-256 `7a638db296da098e65cf573484ef9d6d66af2ca564de3bace23240a4399950c5`,
  and `--help` exit 0.
- Mutation residue: 0 in tracked product paths.

## Reused verification and projection custody

- Existing projector and validator tests: 37/37 PASS (11 + 26).
- New pack, runner, framework, or meta-test: 0.
- Fixed projection: 219 files; public-tree identity
  `sha256:bad49850badee0b5afde4d241d5e6a8336947df54af18f4f6221212b8e78a1b3`.
- The full fixed projection validator remains fail-closed at the pre-existing
  tracked-WASM embedded absolute-path finding:
  `E_PUBLIC_INTERNAL_ABSOLUTE_PATH: solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`.
  W87 did not change that binary. Therefore W87's Windows artifact guard is
  GREEN while whole-P5 clean projection remains OPEN.
- `git diff --check`: PASS.

## Gate effect and nonclaims

- W85, W86 and W87 now enforce teul package/binary exclusion at projection
  creation, independent projection validation, and Windows artifact assembly.
- Review target: one coherent W84-W87 CLI/teul authority and release-custody
  bundle using the existing rolling reviewer only after management dispatch.
- New reviewer, review worktree, branch, task, runner, pack, or meta-test: 0.
- Other INTERNAL/DEFERRED teul commands and private parser/runtime/value custody
  remain nonzero; physical deletion and final binary/package retirement remain
  separately Owner-gated.

This does not claim public test/view/repl membership, final executable naming,
PathIR public contract closure, VC17 exact landing, whole P1/P5/P6 closure, V1
readiness/release/activation, legal approval, Owner Human Smoke, or Human PASS.
