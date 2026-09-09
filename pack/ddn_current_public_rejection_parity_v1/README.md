# Current public rejection parity V1

This successor oracle classifies three preserved historical `보임 {}` cases as
`CURRENT_PUBLIC_EXPECTED_REJECTION_PARITY`. It does not alter or overwrite the
historical 13-case pack, its runner, or any fixed-HEAD evidence.

The runner invokes the same Rust `run_summary_from_source` owner through the
native CLI and the tracked or source-built WASM export. Both surfaces must
reject before creating a summary, state mutation, output, or effect, with the
same structured diagnostic, source location, phase, and span. A compatibility
constructor or hidden source conversion is forbidden.

```powershell
$env:DDN_G14_WASM_DIR = '<tracked-or-source-built-WASM-directory>'
node tests/ddn_current_public_rejection_parity_runner.mjs
```

`DDN_G14_CLI` may name an already source-built `ddonirang-tool` executable.
When it is absent, the runner builds the executable offline into the external
`DDN_G14_TARGET_DIR` (or the repository build-root default), never into the
tracked tree.
