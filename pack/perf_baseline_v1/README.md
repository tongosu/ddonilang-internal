# perf_baseline_v1

Deterministic performance baseline contract for seven-purpose G1 work.

- evidence_tier: `runner_skeleton`
- closure_claim: `no`
- product_perf_claim: `no`

This pack does not publish sufficient performance numbers. It fixes the three
measurement axes, the regression gate shape, and the runner entrypoint. Existing
`benchmark_baseline_v1` remains the lower-level source pack.

Axes:

- tick throughput
- WASM load to first-frame axis, with CLI startup fallback when real browser WASM
  first-frame measurement is unavailable
- NuriGym rollout step throughput

Verification:

- `python tests/run_perf_baseline_check.py`
- `python tests/run_perf_baseline_v1_pack_check.py`
- `python tests/run_pack_golden.py perf_baseline_v1`
