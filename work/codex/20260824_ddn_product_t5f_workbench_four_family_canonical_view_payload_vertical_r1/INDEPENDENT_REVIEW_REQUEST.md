# [셈그림Codex -> 셈그림검증ClaudeCode] T5F Workbench 4-family canonical payload 독립 검토 요청

```text
PROGRAM_ID: DDN_PRODUCT_LONG_RANGE_CANONICAL_VIEW_CONVERGENCE_R1
VERTICAL_ID: DDN_PRODUCT_T5F_WORKBENCH_FOUR_FAMILY_CANONICAL_VIEW_PAYLOAD_VERTICAL_R1
PRODUCT_FIXED_HEAD: 0abec54b30b26dbe99ce249aa3de5d7681907eab
DIRECT_BASELINE: cfc019776f1b49ba5f00b3c31b87f616719376bd
T5E_CLOSURE_ANCESTOR: 27acdb0f4633da7473187d772ce1875dc6d5d729
REVIEW_MODE: FIXED_HEAD_READ_ONLY
ALLOWED_VERDICT: PASS / PASS_WITH_FOLLOW_UP / REWORK
```

## 필수 판정

1. Rust/WASM tool이 exact four-family structured result를 생산하고 JS가 raw state 의미를 발명하지 않는가.
2. 기존 `semantic_view_payload.js`만 canonical owner이며 제3 abstraction이 없는가.
3. line/pendulum/projectile/grid exact schema, identity, provenance, numeric fields가 검증되는가.
4. partial/alias-only/malformed/unknown schema/missing family가 fail-closed하며 raw fallback으로 성공하지 않는가.
5. Workbench renderer가 canonical payload만 소비하고 raw committed state decoy가 결과에 침투하지 않는가.
6. animation/history/trajectory/labels/current point/velocity overlay 기능이 canonical current/history로 보존되는가.
7. pack oracle 4건과 mutation 5건을 독립 재현할 수 있는가.
8. Run/Workbench/Playground projection byte parity 및 실제 Chromium vertical이 통과하는가.
9. T5B~T5E와 RuntimeBridge/HostBridge/observation channel 회귀가 보존되는가.
10. tracked WASM이 source-built artifact와 byte-identical하고 freshness manifest가 현재 source tree를 가리키는가.
11. `docs/ssot/**`, public SPEC, state/storage에 무단 변화가 없는가.
12. candidate contract를 public ABI/stable wire/SSOT current/Web S0로 과장하지 않는가.

## 재현

```powershell
$env:DDN_T5F_SOURCE_WASM_DIR = '<source-built-or-verified-tracked-wasm-directory>'
cargo test -p ddonirang-tool --features wasm workbench_authoritative -- --nocapture
node tests/seamgrim_workbench_four_family_canonical_view_payload_runner.mjs
node tests/seamgrim_workbench_four_family_canonical_view_payload_mutation_runner.mjs
node tests/seamgrim_workbench_committed_view_verticals_browser_runner.mjs
node tests/seamgrim_console_graph_canonical_view_payload_runner.mjs
node tests/seamgrim_space2d_canonical_view_payload_runner.mjs
node tests/seamgrim_table_text_structure_canonical_view_payload_runner.mjs
node tests/seamgrim_console_grid_grid2d_canonical_view_payload_runner.mjs
node tests/seamgrim_workbench_runtime_bridge_t1_runner.mjs
node tests/seamgrim_workbench_host_bridge_t2_runner.mjs
node tests/seamgrim_workbench_observation_channel_t4f_runner.mjs
python tests/run_ddn_cli_wasm_freshness_check.py
```

브라우저는 기존 local Playwright/Chromium만 사용하며 network install을 하지 않는다. `seamgrim_ui_common_runner`의 T5C 유래 stale expectation 및 나머지 명시된 housekeeping은 제품 fallback을 되살리는 사유가 아니다.

plain `PASS` 전에는 T5F closure 또는 T5G 시작을 승인하지 않는다.
