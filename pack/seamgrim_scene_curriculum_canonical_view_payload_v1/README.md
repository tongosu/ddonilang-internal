# seamgrim_scene_curriculum_canonical_view_payload_v1

T5G product-local candidate evidence for `scene-summary` and `curriculum-semantic-scene`.

- canonical owner: `solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_payload.js`
- scene projection: exact explicit primary canonical payload; no graph default or timeline/layer semantic inference
- curriculum projection: validated educational identities and committed bindings; DOM selector, a11y text, reading order, and prompt presentation excluded from canonical identity
- wrapper/session schemas remain `seamgrim.scene.v0` and `seamgrim.curriculum_semantic_scene.v0`
- public schema/ABI promotion: not claimed

Evidence:

```powershell
node tests/seamgrim_scene_curriculum_canonical_view_payload_runner.mjs
node tests/seamgrim_scene_curriculum_canonical_view_payload_mutation_runner.mjs

# 이미 로컬에 설치된 Playwright package root만 지정한다. 이 검증은 network install을 하지 않는다.
$env:DDN_LOCAL_PLAYWRIGHT_NODE_MODULES = '<node_modules containing playwright and playwright-core>'
node --experimental-loader ./tests/local_playwright_module_loader.mjs tests/seamgrim_scene_curriculum_canonical_view_payload_browser_runner.mjs
```

브라우저 검증은 환경변수가 없거나 해당 root에서 `playwright`를 읽을 수 없으면 fail-closed한다.
