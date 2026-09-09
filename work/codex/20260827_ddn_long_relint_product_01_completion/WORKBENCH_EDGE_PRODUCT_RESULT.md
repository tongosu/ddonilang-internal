# Microsoft Edge 실제 Workbench 제품 결과

## 환경

- browser: installed Microsoft Edge, headed Playwright CLI, network install `0`
- local server: temporary `127.0.0.1:8879`; protected `8787` untouched
- profile: isolated temporary profile
- product URL: `/ui/workbench/index.html`

## 결과

- Workbench boot and tracked WASM asset load: PASS, initial console/network error 0
- four viewport DOM/reflow smoke: 1440x900, 1024x768, 768x1024, 375x812 all main/editor/run visible, horizontal overflow false
- browser menu zoom: NOT TESTED / NOT CLAIMED
- legacy official/local lessons: runtime fails closed with `E_WASM_OBSERVATION_MANIFEST_MISSING`
- V25 PC01 positive source: shared frontend `strict` source analysis rejects at `:=` with `E_PARSE`; no run frame or state commit
- failure atomicity: frame 0, committed step 0, state hash empty
- local save/reopen: PASS through explicit `local_fallback`; source bytes preserved
- exact server revision: unavailable because temporary static server returns 501 for `POST /api/v1/projects`
- console after save: one expected 501 from absent server API
- PID replacement: temporary Edge/server closed; protected PID/port untouched

```text
WORKBENCH_EDGE_BOOT: PASS
WORKBENCH_EDGE_FAILURE_ATOMICITY: PASS
WORKBENCH_EDGE_LOCAL_SAVE_REOPEN: PASS_WITH_LOCAL_FALLBACK
WORKBENCH_EDGE_CURRENT_RUNTIME_SUCCESS: FAIL
WORKBENCH_EDGE_FULL_C9: OPEN
```

JS semantic fallback이나 pre-V25 restore를 추가하지 않았다. T5F current grid는 실행 성공으로 만들지 않았다.
