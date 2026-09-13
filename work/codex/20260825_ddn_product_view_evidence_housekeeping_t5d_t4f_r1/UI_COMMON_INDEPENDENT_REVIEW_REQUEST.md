# UI-common native `모양:` fixture — targeted independent review request

```text
REVIEW_KIND: FIXED_HEAD_READ_ONLY_TARGETED
BASELINE_HEAD: c8e93015e4b33ec3ea8f80edc600b19f5437d231
REVIEW_FIXED_HEAD: f89c16856871d8e0f12e986e3bbf6a10dad5f75a
EXPECTED_CHANGED_FILE: tests/seamgrim_ui_common_runner.mjs
EXPECTED_PRODUCT_SOURCE_DIFF: 0
ALLOWED_VERDICTS: PASS / PASS_WITH_FOLLOW_UP / REWORK
```

Confirm that the changed fixture matches the already-landed T5C authority boundary: native `모양:` and its primitives are preserved for Rust/WASM, legacy JS observation-marker lowering is not reintroduced, the focused and aggregate commands reproduce, and the clean-detached worktree remains clean. The verdict may close only this stale-fixture follow-up.
