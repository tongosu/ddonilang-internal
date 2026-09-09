# DDN V1 CLI patch shared authority W84 session delta

- goal: existing `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` remains active.
- baseline: `5e63c0872e07da197fb72c189c2602c887430d28`
- product fixed: `491e164a3f726732b8638dc0bb763df67fb2cf83`
- fixed tree: `3302ad7d05b9e34ea6f6532ee0238dd84d04ed3d`
- product paths: `tool/src/lib.rs`, `tool/src/patch_workflow.rs`, `tools/teul-cli/src/cli/patch.rs`.
- result: patch propose/preview/approve/apply semantic authority moved from private teul implementation to one shared native tool workflow; teul is a clap adapter.
- direct valid workflow GREEN; approval-hash bypass mutation RED -> exact restore -> mismatch GREEN with partial publish 0.
- new pack/runner/meta-test/reviewer/worktree/branch: 0.
- protected pre-existing untracked custody: four files unchanged and unstaged.
- W81~W83 rolling review bundle remains frozen at fixed `302024e3...` / handoff `5e63c087...`; W84 starts a separate non-overlapping bundle.
- open: exact public command membership/naming, physical teul deletion, legacy Geoul state codec, existing dataset WASM gating, PathIR/public-contract slices and all release/Human gates.
