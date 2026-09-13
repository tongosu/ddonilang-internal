# PG-CLI-07 explicit text-addition parity handoff

## Claim

- Product target: `00ee7a85829e313eba94e025923836547c51f124`
- Tree: `fff51105707706e844580af5825dbf345a272694`
- Parent: `a737228f57aa8a670d6a16160d9a8095987b9769`

Current V25 text addition accepts only `글 + 글`. The existing `글로` owner
remains the explicit numeric-to-text conversion surface: `(점수) 글로`.
The runtime now routes two strings through the shared `string_concat` owner.
It does not add implicit number-to-text conversion. A `글 + 수` expression
fails before publication with `E_RUNTIME_TYPE_MISMATCH`, rather than falling
through to the generic numeric-coercion diagnostic.

## Product paths

- `tool/src/ddn_runtime.rs`
- `tool/tests/fixtures/pg_cli_text_addition.ddn`
- tracked `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
- tracked `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

No parser, AST, language grammar, JavaScript lowering, public wire, SSOT, or
public SPEC path changed.

## Primary gates

```text
cargo test -p ddonirang-tool pg_cli_text --lib --offline             # 2 passed
cargo test -p ddonirang-tool pg_cli_result_flow_updates_a_selection_only_after_the_candidate_is_ready --lib --offline
cargo check -p ddonirang-tool --offline
python tests/run_ddn_cli_wasm_freshness_check.py --write-manifest
python tests/run_ddn_cli_wasm_freshness_check.py
```

Source-built `ddonilang`, `또니랑`, and `ddonirang` produced byte-identical
output containing `점수: 7` for `pg_cli_text_addition.ddn` with explicit
profile `v1-core-v25`. Direct tracked-WASM execution of the same source
published `점수: 7`; the raw `글 + 수` source threw a typed
`E_RUNTIME_TYPE_MISMATCH` diagnostic.

Tracked artifact SHA-256: `93D6CA0F0AE3C1408B086563B4B9A13BCC62F47023FF54DBCC893B3869DAEDEE`.
Manifest SHA-256: `63AFE7ED14EF7633BF9068F3591D13B9083B05038AE9B6A3C1201FAC261CD8E8`.

`cargo test -p ddonirang-tool --lib --offline` had 676 passing and 14
pre-existing failures outside this vertical (`ai_prompt`, `project_authoring`,
and one `runtime_surface` profile assertion). They neither cover this `+`
dispatch nor are modified by this target; the focused runtime, ResultFlow,
Native CLI, direct WASM, freshness, and offline check gates above passed.

## Mutation evidence

Fixed runtime blob / SHA-256: `23e1292cce247260af561a83150463d47012abf7` /
`2F13B4A611B9480615CC4BF184EDD4A685CC2481CA388E3ADB6BD7E7595648D2`.

| Mutation | Observed RED | Exact restore | Green gate |
| --- | --- | --- | --- |
| M1: remove the `글 + 글` `string_concat` route | Explicit `(점수) 글로` conversion then failed with `E_RUNTIME_TYPE_MISMATCH` at the left `+` operand. | fixed runtime blob and SHA-256 above | `pg_cli_text` 2/2 |
| M2: restore generic numeric coercion errors | The raw `글 + 수` negative returned `수치가 필요합니다`; its exact typed-diagnostic assertion failed. | fixed runtime blob and SHA-256 above | `pg_cli_text` 2/2 |

Both mutations were restored byte-exactly before focused GREEN. `git diff --check`
passed before the product commit.

## Review request and nonclaims

Review the exact product target, explicit-only `글로` conversion, typed
`글 + 수` failure and no output/state publication, source-built three-name
parity, direct WASM parity, and tracked-WASM freshness. This writer does not
claim independent PASS, official blocker-row closure, release/support, SSOT or
public-SPEC transition, implicit numeric stringification, or restoration of
the unavailable L0 regression seed.
