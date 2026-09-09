# nurigym_step_record_v02_consumer_g6_v1

G6 AI Gym consumer / `step_record.v0.2` additive fixture pack.

Evidence tier: `consumer_tool_layer_prototype`.

This pack does not change public runtime schema, parser/frontdoor grammar, or state hash. It keeps the current `nurigym.step.v1` fields and adds v0.2 candidate fields as optional consumer-layer data:

- `raw_action`
- `normalized_action`
- `action_status`
- `merge_candidates`
- `merged_action`
- `applied_action`
- `run_config_hash`
- `settings_hash`

Verification:

```bash
python tests/run_nurigym_step_record_v02_consumer_g6_check.py
```

The checker also runs the existing shared-sync action pipeline checker and links the vectorized consumer prototype to `perf_baseline_v1`'s `gym_rollout_step_per_sec` axis.
