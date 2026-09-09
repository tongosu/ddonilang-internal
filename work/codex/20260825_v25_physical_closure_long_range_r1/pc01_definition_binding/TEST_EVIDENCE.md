# V25 PC-01 Definition / Binding test evidence

All commands used offline dependencies and the isolated target directory
`I:\home\urihanl\ddn\codex\build\targets\ddn-v25-physical-closure-20260825`.

| Command | Result |
|---|---|
| `cargo test -p ddonirang-lang` | PASS: 263 unit + 3 pack + 0 doc failures |
| `cargo test -p ddonirang-tool --lib v25_definition_then_rebinding_executes_as_distinct_local_operations -- --nocapture` | PASS: 1/1; output `2` |
| `node tests/ddn_v25_pc01_definition_binding_mutation_runner.mjs` | PASS: baseline GREEN; M1/M2/M3 RED; restored GREEN; residue 0 |
| `cargo check --workspace` | PASS; pre-existing dead-code warnings only |
| `git diff --check` | PASS |

Mutation mapping:

1. `M1_DEFINITION_TO_BINDING_COLLAPSE` — RED.
2. `M2_OLD_EQUALS_SILENT_ALIAS` — RED.
3. `M3_DEFINITION_CANON_BINDING_SYMBOL` — RED.

Protection checks at handoff preparation:

```text
docs/ssot/** diff: 0
publish/spec/** diff: 0
tracked WASM diff: 0
shared dirty root mutation: 0
network install: 0
mutation residue: 0
merge commits since program baseline: 0
```

`cargo fmt --all -- --check` is not green on this historical product lineage:
it reports broad pre-existing formatting differences across untouched files.
No workspace-wide formatter write was performed. The newly added standalone
Rust pack test was formatted directly.
