# seamgrim_wave3b_foundation12_model_alignment_v1

Wave3B G1 product gate for the fixed 12-world foundation set.

This pack verifies that all 12 lesson models pass the CLI frontdoor and the
browser product route with at least one observation payload. Browser execution
uses `tab=studio&catalog_mode=full&lesson=<lesson_id>` so G1 can validate the
models before G2 promotes the cohort into the active catalog.

Verification:

```bash
python tests/run_seamgrim_wave3b_foundation12_model_alignment_check.py
python tests/run_pack_golden.py seamgrim_wave3b_foundation12_model_alignment_v1
```
