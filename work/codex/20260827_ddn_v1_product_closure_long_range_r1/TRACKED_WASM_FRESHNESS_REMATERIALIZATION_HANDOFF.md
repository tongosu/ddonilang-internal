# Tracked WASM freshness rematerialization handoff

## Fixed target

- Product commit: `dcffceb0b4b3d9e3ec0687c742981ddadc6d8fb8`
- Product parent: `51b46474d4a5dad788791827f7d42ff051738647`
- Product tree: `903fef4322f72aaa5a8d29f459b7ee7c879ced80`
- Scope: `ddonirang_tool_bg.wasm` and its existing deterministic freshness manifest only.

## Source and artifact binding

- Source tree SHA-256: `8f30b267370b2441da355f8888b875baf9c049e482806e0ebbd3cf1593bffe0e`
- WASM bytes: `5,674,478`
- WASM SHA-256: `866b10e2c185bf60284484057fb46ba03c7e09eac4ccbdfc3f5ec870b1750f15`
- Manifest SHA-256: `ddc87969f8ed74452ae9f6d0ab90502927a0062d80d5d65c6cf3d8176a758b5d`

The official existing `build_wasm_tool.ps1` release/web builder rematerialized the
artifact.  The existing freshness checker then regenerated the manifest from that
exact source tree and artifact; no manual manifest hash was introduced.

## Direct checks

- `run_ddn_cli_wasm_freshness_check.py --write-manifest`: PASS
- `run_ddn_cli_wasm_freshness_check.py`: PASS
- `run_ddn_local_project_graph_check.py`: PASS
- AddModule typed export focused test: PASS (reused from the direct predecessor)
- `git diff --check`: PASS

## Fault checks

- M3: restored the pre-rematerialization WASM (`8a82aee9...`) into the tracked
  path through task-owned scratch materialization.  The existing checker rejected
  it with `wasm_sha256 mismatch` and `wasm_size mismatch`.  The official copy
  path restored the current artifact byte-exactly, then freshness returned GREEN.
- M4: replaced only `source_tree_sha256` in the manifest with zeroes.  The
  existing checker rejected it with `source_tree_sha256 mismatch`; canonical
  manifest rematerialization restored the recorded SHA-256 and GREEN result.

## Scope boundary

The typed module-directive WASM carrier remains an internal versioned product ABI
candidate.  This handoff does not claim public support, V1 readiness, release,
activation, or Human PASS.  No new pack, runner, or meta-test was created.

`cargo test -p ddonirang-tool module_directive_analysis` was still compiling on
the dedicated task target when this fixed target was made; it is non-blocking
evidence and is not represented as a completed regression result here.
