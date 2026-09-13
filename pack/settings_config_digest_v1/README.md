# settings_config_digest_v1

Decision Closure D1 fixture pack for config digest policy.

Scope:

- `문서` metadata is excluded from `run_config_hash`.
- `이야기.들머리` is result-affecting and included in `run_config_hash`.
- Alias and section-order canonicalization stay deterministic.

Boundary:

- Tooling/checker only.
- No parser/runtime grammar change.
- No runtime `state_hash` formula change.

Verification:

- `python tests/run_pack_golden.py settings_config_digest_v1`
- `python tests/run_settings_config_digest_v1_check.py`
