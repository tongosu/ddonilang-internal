# 2026-09-07 P5 Seamgrim public-candidate continuation

`DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` continued on the existing single-writer
branch.  Product commit `2a89750cc354d731bd674be9d09eddb2ab2174c6` closes the
machine-detected release inventory mismatch: public API and lesson-index
projections now share the release representative allowlist and fail closed on
an absent allowlist.  Two product-risk mutations were RED, byte-restored, and
GREEN.  The Windows candidate artifact set contains the three required names
and no teul artifact; the original detached build host did not return a
terminal exit, so its full-script PASS is deliberately not claimed here.

Protected historical untracked custody was left untouched.  SSOT and public
SPEC were not modified.  Browser validation remains environment-blocked.
