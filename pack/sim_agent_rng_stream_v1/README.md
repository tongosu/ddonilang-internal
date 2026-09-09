# sim_agent_rng_stream_v1

Per-agent RNG stream proof fixture for declarative closure G10.

Scope:

- Fixes derivation identity as `(global_seed, agent_id, stream_name)`.
- Demonstrates that traversal order A/B produces the same per-stream draw
  sequence for the same stream set.

Boundary:

- This is a proof/checker fixture only.
- It does not replace product runtime RNG and does not change `state_hash`.

Verification:

- `python tests/run_pack_golden.py sim_agent_rng_stream_v1`
- `python tests/run_declarative_closure_g10_agent_rng_stream_red_check.py`
