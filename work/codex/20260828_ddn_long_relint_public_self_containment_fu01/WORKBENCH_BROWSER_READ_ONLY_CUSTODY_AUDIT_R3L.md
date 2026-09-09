# Workbench/browser read-only custody audit — R3L

## 판정

```text
WORKBENCH_EXACT_TRACKED_PATH_CUSTODY: RECORDED
WORKBENCH_PUBLIC_MEMBERSHIP: NOT_AUTHORIZED
WORKBENCH_PATH_RIGHTS: UNKNOWN_GIT_PROVENANCE_ONLY
LOCKED_BROWSER_PACKAGE_REQUIREMENT: PLAYWRIGHT_1_44_0
EXACT_LOCKED_PLAYWRIGHT_MODULE_AVAILABLE_LOCALLY: NO
SEALED_OFFLINE_BROWSER_BUNDLE: NO
LOCAL_CACHE_RELEASE_AUTHORITY: NO
EDGE_MACHINE_INSTALL_RELEASE_AUTHORITY: NO
PRODUCT_WRITE_COUNT: 0
NETWORK_ACCESS: 0
```

## 제품 경로 후보 custody

fixed product HEAD `91e56e597a920a8346e18bf68fa80afadf92d3aa`의
`solutions/seamgrim_ui_mvp/ui/workbench/index.html`에서 HTML `src`/`href`와 정적 ES
module import를 재귀 추적했다. Workbench에서 전역 UI로 이동하는 tracked link도 실제
도달 경로이므로 포함했다. 여기에 UI module metadata와 tracked WASM family 5개를
명시적으로 더했다.

```text
STATIC_ENTRYPOINT_CLOSURE: 101 paths
EXPLICIT_UI_AND_WASM_SUPPORT: 6 paths
TOTAL_TRACKED_CANDIDATE_PATHS: 107
PATH_MANIFEST_SHA256: 74226b6ba784ec7ed2f0e5b499733a7656309860d14f9f61aa82587cfe84e0f4
EXACT_LEDGER: WORKBENCH_BROWSER_PATH_RIGHTS_LEDGER_R3L.detjson
```

대표 fixed bytes는 다음과 같다.

| path | bytes | SHA-256 |
|---|---:|---|
| `solutions/seamgrim_ui_mvp/ui/workbench/index.html` | 31,284 | `6d9ff055dc24d0833e5a4a6a841f488e47c8f41b80874cc0db3233eea5615f88` |
| `solutions/seamgrim_ui_mvp/ui/workbench/workbench.js` | 262,061 | `3f70b14e2cb88ecc8a98c227db79d90dc68efdf7147c7538322f2dba8ef8d953` |
| `solutions/seamgrim_ui_mvp/ui/runtime/runtime_bridge.js` | 8,113 | `df38464543abe2c6a5570d42e79f4d2dee4a4d4d638e98088fd7151576ae49f5` |
| `solutions/seamgrim_ui_mvp/ui/runtime/wasm_vm_runtime.js` | 17,091 | `a759990e95b3ca9c5825714fb422d405cbf80ca30a03fca80b4d348739552abe` |
| `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm` | 5,541,461 | `77c787961f2902745845d907c8f2528d56e063d4a41373f4e7d605e195269f34` |

이 107개는 public membership 목록이 아니라 exact tracked-path custody 입력이다. lesson,
sample, selected example 같은 동적 content membership은 D3에 따라 제외한다. Git history의
author identity와 blob custody는 법적 ownership 또는 공개 허가가 아니므로 107개 전체의
권리 상태는 `UNKNOWN`으로 유지한다.

## locked package와 로컬 custody

tracked root metadata는 다음과 같다.

```text
package.json: 63 bytes / 9b3ff4b17d4ab08dc648a92b920566dc78b7b25bd4732a6c21bacd3417b0a199
package-lock.json: 1,707 bytes / 755d4cced0b6aa5517350dbf65bd518fb1555d70c5340acbcbc86ecbda3ad518
LOCKFILE_VERSION: 3
LOCKED_ROWS: playwright@1.44.0, playwright-core@1.44.0, fsevents@2.3.2
```

감사 시 `DDN_LOCAL_PLAYWRIGHT_NODE_MODULES`, `DDN_PLAYWRIGHT_MODULE`,
`DDN_PLAYWRIGHT_PACKAGE_DIR`, `PLAYWRIGHT_BROWSERS_PATH`는 모두 비어 있었다. shared root
`node_modules`에는 exact package가 없었다. Playwright cache `.links`의 세 대상 중 하나는
이미 사라진 temp path였고, 남은 npm cache package는 `1.62.1`과
`1.63.0-alpha-2026-08-05`였다. lock의 `1.44.0`과 일치하지 않는다.

로컬 `ms-playwright`에는 chromium 1117/1217/1232, headless shell 1217/1232,
ffmpeg 1009/1011, winldd 1007이 존재했다. 핵심 executable 7개의 path/size/hash canonical
digest는 `b1911d8e71931122007810cbf183a83148c7fd1ab973df78759409fe64298311`이다.
그러나 cache 전체 file manifest, exact package-to-browser mapping, 재배포 권리, immutable
seal이 없으므로 sealed bundle로 승격하지 않는다.

machine Edge는 `151.0.4129.101`, executable SHA-256
`24f626e48dae3574b4d59adc8f23722f890fd0a64f78c772384b783b96bcf1a0`로 읽혔다.
이는 설치 사실일 뿐 release bundle이나 public entrypoint custody가 아니다.

## 결론

D6 read-only custody는 exact 후보 path와 현지 dependency 상태까지 기록했다. 그러나
exact locked Playwright module이 없고 local browser cache는 sealed artifact가 아니므로
offline browser bundle은 OPEN이다. public membership, actual Edge G31, tracked WASM refresh,
publication은 이번 방향으로 승인되지 않았다.
