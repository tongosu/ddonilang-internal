# [셈그림Codex -> 독립검토ClaudeCode] T5E console-grid / grid2d canonical payload 독립 검토 요청

```text
PROGRAM_ID: DDN_PRODUCT_LONG_RANGE_CANONICAL_VIEW_CONVERGENCE_R1
VERTICAL_ID: DDN_PRODUCT_T5E_CONSOLE_GRID_GRID2D_CANONICAL_VIEW_PAYLOAD_VERTICAL_R1
PRODUCT_FIXED_HEAD: 15af02d3adcdf28bcc412106811be477d0f875bb
DIRECT_BASELINE: 1395b4491fee66967a0681a3dcc4c5e1cc828c4e
IMPLEMENTATION_COMMIT: 15e54e82810b0a19bd5b28e32d1c96fdf7c71fa3
HARNESS_CORRECTION: 15af02d3adcdf28bcc412106811be477d0f875bb
REVIEW_MODE: FIXED_HEAD_READ_ONLY
ALLOWED_VERDICT: PASS / PASS_WITH_FOLLOW_UP / REWORK
```

## 필수 판정

1. 기존 `semantic_view_payload`만 canonical owner이며 제3 abstraction이 없는가.
2. console-grid가 canonical console ordered entry만 소비하고 raw output/heuristic을 active semantic success로 쓰지 않는가.
3. grid2d가 exact `seamgrim.nurimaker.grid_state.v1`, stable actor identity/order/position만 소비하는가.
4. Workbench-grid meaning과 grid2d를 합치지 않았는가.
5. Canvas/palette/pixel/DOM이 canonical identity에 들어가지 않는가.
6. missing/no-view/invalid/unsupported/ambiguous가 fail-closed하는가.
7. Run/Workbench/Playground 및 Nurimaker renderer port가 byte-equivalent canonical payload를 보존하는가.
8. 3개 mutation과 actual browser를 독립 재현할 수 있는가.
9. T5B~T5D, cell-grid/Nurimaker, T1/T2/T4/T4f 회귀가 보존되는가.
10. SSOT/SPEC/tracked WASM diff가 0인가.

## 재현

```powershell
node tests/seamgrim_console_grid_grid2d_canonical_view_payload_runner.mjs
node tests/seamgrim_console_grid_grid2d_canonical_view_payload_mutation_runner.mjs
node tests/seamgrim_console_grid_grid2d_canonical_view_payload_browser_runner.mjs
node tests/bogae_cell_grid_primitive_runner.mjs
node tests/nurimaker_grid_runner.mjs
node tests/seamgrim_console_graph_canonical_view_payload_runner.mjs
node tests/seamgrim_space2d_canonical_view_payload_runner.mjs
node tests/seamgrim_table_text_structure_canonical_view_payload_runner.mjs
```

브라우저 dependency는 기존 local Playwright만 사용하고 network install을 하지 않는다. `seamgrim_ui_common_runner`의 T5C 유래 stale expectation과 T5D text-format golden coverage gap은 비차단 OPEN으로 명시되어 있다.

plain `PASS` 전에는 T5E closure 또는 T5F 시작을 승인하지 않는다.
