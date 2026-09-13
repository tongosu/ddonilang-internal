# PG-CLI-07 callable-body typecheck correction

Product: `0c04d6769106ca2b1ca42ffa5fe39d9c94b85894` (parent `66175f73394dad657fad197c77694a288b176d2f`).

This correction makes the V25 known-infix frontdoor validator traverse named callable bodies and nested statement bodies.  A statically known `글 + 수` now returns `E_RUNTIME_TYPE_MISMATCH` before execution in Native and tracked WASM.

Changed product paths: `tool/src/ddn_runtime.rs`, `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`, and its deterministic manifest.

Focused: two frontdoor tests GREEN; direct tracked-WASM callable rejection GREEN; freshness checker GREEN.

Mutations: M1 omitting the frontdoor guard caused both root and callable assertions RED. M2 omitting callable traversal caused the callable assertion RED. Both restored byte-exactly to blob `d334a9f4425dd4efbdb1a04aa4748d1c42ba7333`, SHA-256 `794D284BFF85D2E69BC8A876DEB859A710E00D6E29F28CF9FB480594BCE9D4D2`.

Ready for same-reviewer rereview; no independent PASS is claimed here.
