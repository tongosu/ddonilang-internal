# DDN Product T5D table/text/structure canonical view payload 독립 검토 요청

## Fixed point

- PROGRAM_ID: `DDN_PRODUCT_LONG_RANGE_CANONICAL_VIEW_CONVERGENCE_R1`
- VERTICAL_ID: `DDN_PRODUCT_T5D_TABLE_TEXT_STRUCTURE_CANONICAL_VIEW_PAYLOAD_VERTICAL_R1`
- BASELINE: `0c037a2ff4e4c6268ea8e4a82a1a23182a5234a8`
- IMPLEMENTATION: `e0c687eb9eecef877eb0cf44d48a747acc98e8ec`
- EVIDENCE_FORMAT_CORRECTION: `29f88e2d8ddf4f1c7d526745fe02b1a0aa6ace45` — extra blank EOF only
- REVIEW_FIXED_HEAD: 이 문서를 포함하는 handoff commit
- T5C owner-packet verdict input: `PASS`

제품·테스트·golden·보고서를 수정하지 않는 fixed-HEAD 읽기 전용 독립 검토를 요청한다. 직접 재현한 근거로만 `PASS / PASS_WITH_FOLLOW_UP / REWORK`를 발행한다.

## 필수 검토 질문

1. 기존 `semantic_view_payload`만 확장했고 제3 semantic/view abstraction이 없는가?
2. canonical input이 exact `seamgrim.table.v0`, `seamgrim.text.v0`, `seamgrim.structure.v0`에 한정되는가?
3. schema-less shape, output text, resource-name heuristic, previous frame에서 canonical success를 만들지 않는가?
4. missing/no-view, invalid, unsupported, ambiguous, missing identity가 fail-closed하는가?
5. table column/order/value, text content/format, structure node identity/order/edge reference가 보존되는가?
6. Run, Workbench, Playground가 byte-equivalent renderer-independent payload를 반환하는가?
7. actual browser가 canonical table/text/structure payload를 렌더하고 semantic identity를 바꾸지 않는가?
8. Run active path에서 hidden text fallback이 0인가?
9. mutations 3개가 GREEN→RED→GREEN이고 residue가 0인가?
10. T5B/T5C, T1/T2/T4/T4f, Playground, Workbench, Bogae, measurement, Foundation12가 보존되는가?
11. active view `14`, registry-only `2`, feature removal `0`인가?
12. state/hash/storage, SSOT/SPEC/tracked-WASM diff가 0인가?
13. `seamgrim_ui_common_runner` 실패가 baseline-preexisting인지 직접 대조했는가?

## 최소 재현

```text
node tests/seamgrim_table_text_structure_canonical_view_payload_runner.mjs
node tests/seamgrim_table_text_structure_canonical_view_payload_mutation_runner.mjs
node tests/seamgrim_table_text_structure_canonical_view_payload_browser_runner.mjs
node tests/seamgrim_console_graph_canonical_view_payload_runner.mjs
node tests/seamgrim_space2d_canonical_view_payload_runner.mjs
node tests/seamgrim_workbench_semantic_view_payload_runner.mjs
node tests/seamgrim_pendulum_bogae_runner.mjs
python tests/run_seamgrim_bridge_surface_api_parity_check.py --out <isolated-output>
```

browser runner는 network install 없이 기존 local Playwright/Chromium artifact를 사용한다. dependency가 없으면 제품 PASS로 확대하지 말고 `NOT_REPRODUCED`로 기록한다.

## 판정 경계

plain independent `PASS` 전에는 T5E, NativeRenderer/ABI, public ABI, SSOT/SPEC 승격, Web S0, deployment 또는 Human PASS를 시작·주장하지 않는다.
