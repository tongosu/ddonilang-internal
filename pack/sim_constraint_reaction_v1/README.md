# sim_constraint_reaction_v1

Umbrella red/contract pack for declarative closure G7 constraint reactions.

This pack records the candidate constraint vocabulary only:

- family: `막음`
- verb: `막기`
- reactions: `멈춤`, `튕김(e)`, `조임`, `감쌈`

Boundary:

- no parser/frontdoor landing
- no runtime landing
- no `state_hash` formula change
- no new language block

Verification:

- `python tests/run_declarative_closure_g7_constraint_red_check.py`
