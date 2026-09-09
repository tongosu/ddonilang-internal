# Seamgrim console-grid / grid2d canonical view payload v1

T5E product-local candidate golden이다. `console-grid`는 canonical console entry의 결정적 cell projection이고, `grid2d`는 exact `seamgrim.nurimaker.grid_state.v1`의 tile/actor 의미 projection이다. Workbench-grid public meaning이나 stable ABI를 정의하지 않는다.

```powershell
node tests/seamgrim_console_grid_grid2d_canonical_view_payload_runner.mjs
node tests/seamgrim_console_grid_grid2d_canonical_view_payload_mutation_runner.mjs
node tests/seamgrim_console_grid_grid2d_canonical_view_payload_browser_runner.mjs
```
