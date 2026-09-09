# Canonical View T5D/T4f evidence housekeeping — targeted independent review request

```text
REVIEW_KIND: FIXED_HEAD_READ_ONLY_TARGETED
BASELINE_HEAD: f90c3d08cc8a665341214c3b34bf23f768c06618
REVIEW_FIXED_HEAD: dc0b4129f4ce5c6ebd8a4a61d80c4f112984c6fd
EXPECTED_PRODUCT_SOURCE_DIFF: 0
ALLOWED_VERDICTS: PASS / PASS_WITH_FOLLOW_UP / REWORK
```

## Review scope

1. Confirm the fixed HEAD is a linear successor of the baseline and changes only the T5D pack/test evidence plus the T4f mutation harness.
2. Confirm `format: "html"` under exact `seamgrim.text.v0` has an independent exact golden for `invalid`, `E_CANONICAL_TEXT_INVALID_CANDIDATE`, and `text_format_invalid`.
3. Confirm the T5D runner consumes that golden and M4 detects an independently changed expected diagnostic.
4. Confirm the T4f mutation runner works under both LF and CRLF source checkout without normalizing or permanently modifying the product source.
5. Confirm the mutation produces semantic RED, does not count syntax/compile failure as RED, restores byte-identically, and leaves residue `0`.
6. Confirm T5H aggregate remains `13/13`, T5I pre-audit remains `14/14`, and product/SSOT/SPEC/tracked-WASM diffs are `0`.

Do not modify product or test files during review. This targeted verdict cannot close T5G, T5H, T5I, the full View program, Native readiness, or any public ABI.
