# PG-CLI-02 WASM freshness correction handoff

Correction product: `6de0545c053b2b03e6dee3888e70d8811e2eb305`

Parent: `c914f3b57e9c331b27ff1406dd3b4a8a7a109c86`

The independent review of PG-CLI-02 found that product `921bd230…` carried a
freshness manifest referring to an earlier WASM size/hash. The tracked binary
itself was the official-builder output, but the manifest was not bound to that
immutable binary. This correction changes only the tracked deterministic
freshness manifest; SelectionPlace product source remains unchanged.

Official builder then manifest writer evidence:

- `python tests/run_ddn_cli_wasm_freshness_check.py --write-manifest` — PASS
- `python tests/run_ddn_cli_wasm_freshness_check.py` — PASS
- `ddonirang_tool_bg.wasm` SHA-256:
  `66B8C4718FD940BAE1BC14DDF478E44DE266A21B1CFC53143091112994F8CE3E`
- WASM byte size: `5688560`
- manifest SHA-256:
  `156645DD0FBBAA1317AE213D04090CDBEE17F179A4E3A5D5CAE2EF246016D112`

The original PG-CLI-02 focused language/runtime/three-name tests and M1/M2
restore blobs remain applicable because no selection source changed. Same
reviewer rereview is requested for this correction target. No self-issued PASS
is claimed.
