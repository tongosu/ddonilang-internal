# seamgrim_wasm_sealed_runtime_binding_v1

G7 contract pack for binding the Seamgrim product browser runtime to the
sealed `ddonirang_tool` WASM manifest.

Verification:

```bash
python tests/run_seamgrim_wasm_sealed_runtime_binding_check.py
python tests/run_pack_golden.py seamgrim_wasm_sealed_runtime_binding_v1
```

The browser runner covers four lessons across four viewports and a tampered
manifest negative control. It does not claim full CLI/WASM single-runtime
closure or change any hash formula.
