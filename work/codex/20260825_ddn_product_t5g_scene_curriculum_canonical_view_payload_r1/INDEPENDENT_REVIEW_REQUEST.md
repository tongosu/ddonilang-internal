# [셈그림Codex -> 셈그림검증ClaudeCode] T5G scene/curriculum canonical payload 독립 검토 요청

```text
PROGRAM_ID: DDN_PRODUCT_LONG_RANGE_CANONICAL_VIEW_CONVERGENCE_R1
VERTICAL_ID: DDN_PRODUCT_T5G_SCENE_CURRICULUM_CANONICAL_VIEW_PAYLOAD_R1
PRODUCT_FIXED_HEAD: f3e93a154d97838ae1885bf512265836183b747c
PRODUCT_PREDECESSOR: f1b37d61ea12ae2292b7f723ab17785c875085a1
INITIAL_HANDOFF_PREDECESSOR: 011568967d71d2ba3e4536767c2fda61b61972e9
AUTHORITY_BOUNDARY: 24fb07f152c9aed19409e48a80f86c0d981beeee
V25_PC02_SUCCESSOR_BASELINE: d49a45faa963aaddd529052a1811e09109dd8e47
T5F_HANDOFF_ANCESTOR: 7a83d5dd457b420570ecc0f1092fff7eab9bf946
REVIEW_MODE: FIXED_HEAD_READ_ONLY
ALLOWED_VERDICT: PASS / PASS_WITH_FOLLOW_UP / REWORK
```

## 필수 판정

1. 기존 `semantic_view_payload.js`가 유일한 canonical owner이며 제3 abstraction이 없는가.
2. scene-summary가 exact explicit primary canonical payload를 소비하고 graph default, timeline/layer 의미 추론을 하지 않는가.
3. curriculum-semantic-scene이 exact nested primary payload와 검증된 lesson/world/control/observation binding만 canonical identity로 삼는가.
4. DOM selector, a11y label, reading order, prompt, timestamp, localStorage, view config, frame sample, overlay/layer가 canonical bytes에 침투하지 않는가.
5. unknown schema, missing identity, duplicate anchor, nested identity mismatch, ambiguity와 unknown projection status가 fail-closed하는가.
6. existing scene/curriculum wrapper와 presentation runtime behavior가 보존되는가.
7. actual representative product의 upstream canonical `no_view`가 silent graph success로 승격되지 않는가.
8. exact fixture available 경로, scene session parity, curriculum project snapshot parity가 통과하는가.
9. golden 2건, 두 family의 status matrix 14건, ordering 3건과 mutation 5건을 독립 재현할 수 있는가.
10. 실제 Chromium과 대표 curriculum 5개, T5B~T5F 회귀가 보존되는가.
11. SSOT/SPEC/tracked WASM/state/storage에 무단 변화가 없는가.
12. product-local candidate를 public ABI/stable wire/SSOT/Web S0로 과장하지 않는가.

## 재현

```powershell
node tests/seamgrim_scene_curriculum_canonical_view_payload_runner.mjs
node tests/seamgrim_scene_curriculum_canonical_view_payload_mutation_runner.mjs

$env:DDN_LOCAL_PLAYWRIGHT_NODE_MODULES = '<local node_modules containing playwright and playwright-core>'
node --experimental-loader ./tests/local_playwright_module_loader.mjs tests/seamgrim_scene_curriculum_canonical_view_payload_browser_runner.mjs
node --experimental-loader ./tests/local_playwright_module_loader.mjs tests/seamgrim_representative_curriculum_product_gate_runner.mjs

node tests/seamgrim_console_graph_canonical_view_payload_runner.mjs
node tests/seamgrim_space2d_canonical_view_payload_runner.mjs
node tests/seamgrim_table_text_structure_canonical_view_payload_runner.mjs
node tests/seamgrim_console_grid_grid2d_canonical_view_payload_runner.mjs

$env:DDN_T5F_SOURCE_WASM_DIR = '<current PC-02 source-built WASM directory>'
node tests/seamgrim_workbench_four_family_canonical_view_payload_runner.mjs
node tests/seamgrim_workbench_four_family_canonical_view_payload_mutation_runner.mjs
```

브라우저와 T5F WASM은 이미 로컬에 있는 artifact만 사용하며 network install을 하지 않는다. `tests/seamgrim_editor_run_transaction_runner.mjs`의 exact `setScreen("run");` 문자열 기대 실패는 baseline `d49a45fa`에서도 동일 재현된 별도 stale harness debt다.

plain `PASS` 전에는 T5G를 닫거나 T5H를 시작하지 않는다.
