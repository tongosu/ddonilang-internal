# Seamgrim Workbench four-family canonical view payload V1

T5F product-local candidate evidence pack이다.

- authoritative producer: shared Rust `ddonirang_tool.wasm_runtime`
- canonical owner: existing `semantic_view_payload.js`
- families: `workbench-line`, `workbench-pendulum`, `workbench-projectile`, `workbench-grid`
- raw channel/resource alias fallback: active canonical renderer path에서 금지
- stable public ABI / SSOT / SPEC claim: 없음

재현:

```powershell
$env:DDN_T5F_SOURCE_WASM_DIR = 'I:\home\urihanl\ddn\codex\build\wasm\ddn-product-t5f-workbench-four-family-20260824'
node tests/seamgrim_workbench_four_family_canonical_view_payload_runner.mjs
```

환경변수가 없으면 runner는 fail-closed한다. `expected.detjson`은 네 실제 source-built WASM 실행 결과의 canonical hash와 result schema를 봉인한다.
