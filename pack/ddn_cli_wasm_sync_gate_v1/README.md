# DDN CLI/WASM sync gate v1

This pack records bounded evidence for the CLI/WASM single runtime closure work.
It starts with the G0 baseline and is intentionally scoped to runtime parity,
WASM provenance, and product smoke checks. It does not claim full DDN language
equivalence.

G9 integrated gate:

```bash
python tests/run_ddn_cli_wasm_sync_gate_check.py
```

The gate runs the G0-G8 bounded checks in order and writes
`build/ddn_cli_wasm_sync_gate_report.detjson`. The report records stage
start/end, failure codes, negative-control detection, bounded closed behavior,
and open scope. The generated report is a local verification artifact, not a
pack golden.
