# settings_keyset_policy_v1

Decision Closure D2 fixture pack for settings keyset policy.

Scope:

- `설정.누리` closed key set is `시앗`, `시앗묶음`.
- `설정.이야기` closed key set is `들머리`.
- `문서.*` stays excluded from `run_config_hash`.
- `이야기.들머리`, `누리.시앗`, and `누리.시앗묶음` stay included in `run_config_hash`.
- `설정.셈 { 적분: ... }` remains artifact-behavior status only until a separate keyset decision.

Boundary:

- Pack/checker policy only.
- No parser/runtime grammar change.
- No runtime `state_hash` formula change.

Verification:

- `python tests/run_pack_golden.py settings_keyset_policy_v1`
- `python tests/run_settings_keyset_policy_check.py`
