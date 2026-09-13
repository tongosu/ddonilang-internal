# PG-CLI-07 frontdoor typecheck correction handoff

## Claim

- Correction product: `654ca58a377560eb0a79a510890c810b29e75b57`
- Tree: `30650a0262891c445c7457cdab931566029e8c02`
- Parent: `3b4ac66e6c275fc3220634404d58871f4b3e5b40`
- Corrected predecessor: `00ee7a85829e313eba94e025923836547c51f124`

The V25 frontdoor now rejects statically-known invalid `글 + 수` and `수 + 글`
pairs before it constructs an executable `DdnProgram`. It reuses the existing
`E_RUNTIME_TYPE_MISMATCH` diagnostic identity. Dynamic or unknown values are
not guessed by this check and remain subject to the existing runtime boundary.
No implicit numeric-to-text conversion was added; explicit `(점수) 글로` then
`글 + 글` remains the supported current path.

## Product paths

- `tool/src/ddn_runtime.rs`
- tracked `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
- tracked `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

The fixture from the predecessor is reused unchanged. No parser, AST,
JavaScript lowering, public wire, SSOT, or public SPEC path changed.

## Gates

```text
cargo test -p ddonirang-tool pg_cli_text --lib --offline             # 2 passed
cargo check -p ddonirang-tool --offline
python tests/run_ddn_cli_wasm_freshness_check.py --write-manifest
python tests/run_ddn_cli_wasm_freshness_check.py
```

The three source-built aliases (`ddonilang`, `또니랑`, `ddonirang`) produced
byte-identical `점수: 7` output for the unchanged explicit-conversion fixture.
Direct tracked WASM ran that source twice byte-identically and rejected raw
`글 + 수` at its source frontdoor with `E_RUNTIME_TYPE_MISMATCH`.

Tracked artifact SHA-256: `1DD162C387067D14147BA0A7F622A43CD1DCD572C0575BB608954DF4ABA86FB8`.
Manifest SHA-256: `2745529BB7FE4E8041C52B68D94E95692A3E5116DA277862D2B912C4E763E91E`.

The applicable full tool library run remains `676 passed; 14 failed`. The
same sparse-worktree failures are in `ai_prompt`, `project_authoring`, and one
`runtime_surface` profile assertion; this correction neither changes those
paths nor adds a new failure.

## Mutation evidence

Fixed runtime blob / SHA-256: `8b4a0b8581204720ea65be409b1ee7d9b56947ab` /
`5A94410DAF9C1E9E453A7D21682BFE7DBCB1DE65FE78090D8019B447CA53C370`.

| Mutation | Observed RED | Exact restore | Green gate |
| --- | --- | --- | --- |
| M1: bypass V25 known-infix validator | Raw `글 + 수` reached `DdnProgram` construction; the frontdoor-failure assertion panicked. | fixed runtime blob and SHA-256 above | `pg_cli_text` 2/2 |
| M2: downgrade known text-left mismatch to unknown | Raw `글 + 수` again constructed a program; the frontdoor-failure assertion panicked. | fixed runtime blob and SHA-256 above | `pg_cli_text` 2/2 |

Each mutation was restored byte-exactly before focused GREEN. `git diff --check`
passed before the correction product commit.

## Review request and nonclaims

Review that the V25 check is limited to statically-known operands, preserves
explicit `글로` plus `string_concat`, emits the existing typed diagnostic before
execution/publication, and is shared by Native and tracked WASM. This writer
does not claim independent PASS, official blocker-row closure, broader static
typing, new public diagnostics, release/support, SSOT/public-SPEC transition,
or recovery of the missing L0 source artifact.
