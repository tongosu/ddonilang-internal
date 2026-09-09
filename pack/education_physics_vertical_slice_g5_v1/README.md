# education_physics_vertical_slice_g5_v1

G5 education + physics vertical-slice evidence pack.

Evidence tier: `pack_skeleton_plus_existing_product_smoke_reference`.

This pack does not add language surface, parser behavior, runtime semantics, or state hash input. It connects existing evidence only:

| Slice part | Evidence |
|---|---|
| WASM/browser delivery | `python tests/run_seamgrim_wasm_web_smoke_contract_pack_check.py` |
| Physics integrators | `python tests/run_stdlib_l1_integrators_g1_check.py` |
| Three-layer diagnostics | `diag_three_layer_fixture.detjson` |
| Graph payload bridge | `physics_graph2d_fixture.detjson` lowered by the checker |

The checker records browser delivery smoke as scoped behavior evidence when it passes. The education/physics graph bridge remains `닫힘-문서` until a product browser workflow renders this slice directly.

Verification:

```bash
python tests/run_education_physics_vertical_slice_g5_check.py
```
