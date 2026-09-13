# DDN V1 CLI gaji native/WASM Cargo target isolation W119

- AI_PROVIDER: OpenAI
- AI_SURFACE: Codex Work
- AI_CAPABILITY: single-writer product/test implementation and QA
- SESSION_NICKNAME: DDN V1제품마감Codex
- PROJECT_ROLE: DDN V1 closure single writer
- RETURN_LABEL: DDN V1제품마감Codex
- DEEP_RESEARCH_CHECK: NOT_USE; the reproduced local Cargo target contamination
  and existing runner determine this correction.

## Result

The existing gaji native/WASM parity runner had a release-custody blocking false
RED when nested `teul-cli` and the official root workspace reused one Cargo target
despite distinct lock graphs.  It now gives each workspace a process-owned target
subdirectory, preserving its existing official CLI/WASM parity workflow.

- Fixed commit: `003395300054d256aebfeac7bfb94945c1d4ed56`
- Parent: `80f058c12d7f65fb8854b1936a9fc6d39585e54b`
- Fixed tree: `8f86eb963398239c73e3c128256fe2c54ba09ecf`
- Changed path: `tests/gaji_creator_wasm_parity_runner.mjs` only.
- Baseline RED: duplicate `bzip2-sys` linker collision (`LNK2005`/`LNK1169`).
- Green: existing runner under an explicitly shared outer target prints
  `gaji_creator_wasm_parity: ok`; syntax check and diff check pass.
- New pack/runner/framework/meta-test/dependency: 0. Reused runner: 1.
- Protected untracked VC06/VC17/P1 custody was not staged, moved, or changed.

This is C6 parity-runner materialization correction only.  It does not close
CLI/teul convergence, P5, PathIR/Proof P1, V1 readiness/release, or Human gates.
