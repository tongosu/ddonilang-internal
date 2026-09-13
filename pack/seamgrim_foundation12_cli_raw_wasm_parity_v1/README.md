# seamgrim_foundation12_cli_raw_wasm_parity_v1

G6 contract pack for proving the fixed Foundation12 cohort runs through both
the CLI frontdoor and the product raw WASM frontdoor from the same lesson DDN
sources.

Verification:

```bash
python tests/run_seamgrim_foundation12_cli_raw_wasm_parity_check.py
python tests/run_pack_golden.py seamgrim_foundation12_cli_raw_wasm_parity_v1
```

This pack requires strict equality for the shared execution envelope, canonical
DDN, output rows/logs, and state_hash. It does not claim full CLI/WASM
single-runtime closure and does not change hash formulas.
