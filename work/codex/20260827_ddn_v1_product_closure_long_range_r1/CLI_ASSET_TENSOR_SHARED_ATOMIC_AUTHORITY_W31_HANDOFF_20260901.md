# CLI asset/tensor shared atomic authority W31 handoff

## Identity

- Authority at execution: internal SSOT v25.47.0 / RD-001~543, public Language SPEC v0.6.0.
- Baseline: `787fb9963ed915d88ba2860f417ff5c17177975d`.
- Product fixed commit: `bbdf66392a029f919645b897be0f441c8a63053b`.
- Product fixed tree: `12ae52d521c77971e891dcc079efdca602e94ef2`.
- Direct lineage and merge count: baseline -> fixed, merge 0.

## Product workflow changed

The existing `asset manifest` and `tensor validate/hash/canon` workflows now consume product-owned `ddonirang_tool` authorities. `teul-cli` retains only command adapters for these workflows. Asset and tensor artifact publication uses the shared atomic artifact writer and rejects an existing non-file output target before publication.

Exact product paths:

- `tool/src/asset_manifest.rs`
- `tool/src/tensor_artifact.rs`
- `tool/src/lib.rs`
- `tools/teul-cli/src/cli/asset.rs`
- `tools/teul-cli/src/cli/tensor.rs`

Product/source semantics were moved without adding a second parser, runtime, value, canonicalization, or fallback authority. Public executable naming, package naming, command membership, and legacy alias duration were not decided.

## Executable evidence

- Existing `pack/bogae_asset_manifest_v1`: 1/1 execution PASS; generated LF text exactly equals the fixed Git blob text. The reused checkout golden has historical CRLF materialization and was not edited.
- Existing `pack/tensor_v0_dense` and `pack/tensor_v0_sparse`: positive hash/canon 3/3 PASS; negative diagnostic cases 4/4 PASS.
- Existing output-directory failure: asset and tensor both exit 1 with their explicit non-file-target diagnostic; artifact entries published: 0.
- `cargo test -p ddonirang-tool --lib --offline --quiet`: 552 PASS and the same 2 isolated-checkout `docs/ssot` environment failures in `ai_prompt`; new regression 0.
- `cargo build --manifest-path tools/teul-cli/Cargo.toml --offline`: PASS.
- `git diff --check`: PASS.

No new pack, runner, checker, or meta-test was created.

## Risk mutation

The tensor output-target guard was inverted. The command then lost `E_TENSOR_V0_OUTPUT_TARGET_NOT_FILE` and fell through to generic `E_TENSOR_V0_OUT_WRITE` (RED, exit 1). The source was restored byte-exact to SHA-256 `8323c3c52ed86723a803d4bc3d97501f64680852e6d9185936da531d23294a16`; rebuild and the exact guarded failure returned GREEN, residue 0.

## Gate impact

- Asset-manifest and Tensor-v0 private teul semantic authority: removed from these two workflows.
- Required dependency and physical teul custody: not declared zero repository-wide by this slice.
- Native command adapter: PASS.
- WASM/Workbench: these filesystem artifact commands are not projected as new public WASM/Workbench commands; no semantic reconstruction was added.
- Dotbogi multi-file output remains OPEN because its three-artifact publication cannot be made all-or-nothing by the existing single-artifact writer without a larger transaction authority.

## Review and nonclaims

This fixed target is ready to join the next coherent W25~W31 rolling-review bundle on the existing reviewer only. No reviewer task or worktree was created here.

This handoff does not claim C0~C8 closure, repository-wide teul authority/dependency zero, public command membership, executable/package retirement, P0~P6 closure, V1 readiness, release, activation, legal approval, or Human PASS.
