# P5 tracked-WASM path-clean successor W88 handoff

STATUS: `P5_TRACKED_WASM_PATH_CLEAN_SUCCESSOR_IMPLEMENTED_UNDER_REVIEW`

## Authority and fixed lineage

- Internal CURRENT: v25.49.0 / RD-001~543.
- Public Language SPEC: v0.6.0.
- Baseline: W87 handoff `865c73db69d94d47dbd995d1cd5650d2987c143a`.
- WASM compile-boundary fix: `84ef438110738228b724f8052cd0711a7d036a89`,
  tree `bdfe308c96b2f67a54aae4fb885588f21cdc1107`.
- Product/artifact fixed: `0e57a5b9a1f3e3c16ad427687530587b164f2e21`,
  tree `9fc7e64563c9b921deaf71a9a72b383e90683461`.
- Every relation is direct-parent linear; merge count 0.
- Exact product paths:
  1. `tool/src/lib.rs`
  2. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
  3. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`
- SSOT, public SPEC, UI source/copy/layout, pack and test source diff: 0.

## Product-facing RED and correction

The current tracked WASM had regressed after the prior path-clean checkpoint:
the release inventory reported 115 embedded absolute paths and
`tests.test_wasm_candidate_remap` was 20/21 RED. The fixed W87 public
projection validator therefore correctly stopped at
`E_PUBLIC_INTERNAL_ABSOLUTE_PATH`.

The official candidate build then exposed a second real product RED before
remapping: `dataset_workflow` was exported for wasm32 while its atomic file
writer `artifact_output` was native-only, producing Rust `E0432`. W88 aligns
that existing native file-output workflow with the established wasm cfg
boundary; it adds no alternate dataset semantics or WASM file writer.

After that minimal correction, the existing official candidate entrypoint
produced and sealed a remapped WASM family. No new build script, runner, pack,
checker, framework or meta-test was added.

## Fixed identities

- Candidate source commit: `84ef438110738228b724f8052cd0711a7d036a89`.
- Remap receipt: 2,470 bytes, SHA-256
  `8f91864df7de3d790e7ffee66ae8c1c7beb162f33156edb4c828daeaf2768668`.
- Remap semantic identity:
  `sha256:1e67018cff9b770a9eaed0ae0310fb554cdb0aef632853f626a6685be9f27540`.
- Tracked WASM: 5,572,371 bytes, SHA-256
  `50e7a22e735da6eba4b5966b0b6e05e113a9f15a31204c2a63c61f75fbb7e484`.
- Tracked manifest: 29,111 bytes, SHA-256
  `4534fe5e3d0a4840215a019141019c250a2ccfee528bced35872dd615663f667`.
- Internal absolute/private/official-store/unknown path counts: 0/0/0/0.
- Virtual remap occurrences in WASM: repository 1, cargo registry 95,
  Rust toolchain 21.

## Verification

- Native dataset focused tests: 2/2 PASS, including atomic predecessor
  preservation.
- wasm32 release library check with feature `wasm`: PASS.
- Existing remap and materialization tests: 26/26 PASS.
- Official tracked-WASM freshness: PASS.
- P1-A supported-ingress native/WASM parity: 10 cases PASS.
- VC11 control-flow native/WASM parity: 10/10, repeats 3, partial publish 0.
- VC06 text/canon tracked-WASM workflow: exit 0.
- Fixed public projection: 219 files, identity
  `sha256:ce5121d320ab32b57704da83309c80bd11f1f94609ffc5d50190e23ee2eff621`.
- Public projection validation receipt: 542 bytes, SHA-256
  `fff45050a5e3497632f1aab337f7a92cf1a4909f672b39308657f2e76cbf18a3`.
- Fixed projection Windows x64 candidate: PASS; `ddonirang.exe` 7,043,072
  bytes, SHA-256
  `7a638db296da098e65cf573484ef9d6d66af2ca564de3bace23240a4399950c5`;
  help exit 0; teul artifact count 0.
- Full tool library: 585 PASS / 3 FAIL. Two failures are the known isolated
  worktree `docs/ssot` absence in `ai_prompt`; one is the pre-existing PathIR
  definedness test `raw_ddn_simplify_rejects_definedness_losing_cancellation`.
  None of the three paths changed in W88, so whole-lib PASS is not claimed.
- VC09 evidence runner remains fail-closed at the pre-existing
  `VC09_RECEIPT_MISMATCH id=NC05_TYPE_MISMATCH`; no VC09 closure is inferred.

## Gate effect and nonclaims

W88 restores the current tracked-WASM artifact to the repository's existing
path-clean contract and makes W85-W87 projection/Windows retirement gates
jointly executable from the current fixed source. It does not promote the
artifact to a final release or independently close P5.

Review target is one coherent W84-W88 CLI/teul/release-custody bundle through
the existing rolling reviewer after management dispatch. New reviewer,
worktree, branch or task count is 0.

PathIR definedness/P1, VC09 receipt drift, public test/view/repl membership,
VC17 exact landing, remaining INTERNAL/DEFERRED teul authority, physical teul
deletion, final executable naming, rights/license/distribution, P5/P6 closure,
V1 readiness/release/activation, Owner Human Smoke and Human PASS remain OPEN.
