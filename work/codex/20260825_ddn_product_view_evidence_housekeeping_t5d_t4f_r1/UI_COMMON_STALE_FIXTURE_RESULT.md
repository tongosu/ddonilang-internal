# UI-common native `모양:` stale fixture correction result

```text
PROGRAM_ID: DDN_PRODUCT_LONG_RANGE_CANONICAL_VIEW_CONVERGENCE_R1
BASELINE_HEAD: c8e93015e4b33ec3ea8f80edc600b19f5437d231
FIXED_HEAD: f89c16856871d8e0f12e986e3bbf6a10dad5f75a
CLASSIFICATION: STALE_FIXTURE
PRODUCT_SOURCE_CHANGE: 0
```

## Cause and correction

`tests/seamgrim_ui_common_runner.mjs` still expected the historical JS preprocessor to erase `모양:` and synthesize `보개_출력_줄들` markers. Since T5C, the active product path preserves native `모양:` so Rust/WASM can emit authoritative `seamgrim.space2d.v0`; the old lowering would erase that structured input.

The fixture now verifies:

- native `모양: {` remains present;
- line, circle, and point primitives remain present;
- legacy `space2d` and `space2d.shape` observation markers are absent.

No product behavior, compatibility branch, expected runtime result, or canonical payload was changed.

## Verification

```text
seamgrim_ui_common_runner: PASS
T5C golden: PASS
T5C mutation: 3/3 GREEN -> RED -> GREEN / residue 0
pendulum bogae regression: PASS
T5H aggregate: 13/13 PASS
T5I pre-audit: 14/14 PASS
clean-detached f89c1685: PASS / clean
product/SSOT/SPEC/tracked-WASM diff: 0
```

This correction is ready for a narrow read-only targeted review. It does not revise T5C's already-bound independent verdict and does not authorize T5H dependent product work.
