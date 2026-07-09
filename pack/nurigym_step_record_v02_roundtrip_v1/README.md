# nurigym_step_record_v02_roundtrip_v1

NuriGym `step_record.v0.2` producer/wire/consumer roundtrip evidence pack.

- evidence_tier: `runner_golden`
- closure_claim: `no`
- language_syntax_change: `0`
- runtime_semantics_change: `false`
- state_hash_change: `false`

This pack implements the six ANNEX A fixture cases from `docs/context/proposals/PROPOSAL_NURIGYM_STEP_RECORD_V02_COMPAT_AND_ROUNDTRIP_V1_20260707_ANNEX_A.md:55` through `:60`.

Verification:

```bash
python tests/run_nurigym_step_record_v02_roundtrip_pack_check.py
```

The checker validates six golden cases, cross-checks the v0.2 field names against `pack/nurigym_step_record_v02_consumer_g6_v1`, and keeps this pack at wire-schema evidence only.
