# econ_model_supply_demand_equilibrium_v1

Model-first G1 skeleton for a linear supply-demand equilibrium.

- evidence_tier: `skeleton/docs_first`
- track: `model-first`
- counterpart shape: `agent-first` five-slot symmetry
- closure claim: executable pack recognition only

Agent-first symmetry slots:

| Slot | Model-first role | Agent-first counterpart name |
|---|---|---|
| household | demand curve | `agent_first_household_v1` |
| firm | supply curve | `agent_first_firm_v1` |
| market | equilibrium solve | `agent_first_market_v1` |
| government | no policy shock in this baseline | `agent_first_government_v1` |
| central_bank | not used in this micro model | `agent_first_central_bank_v1` |

This pack does not claim real-world prediction, policy advice, parser changes, grammar changes, or runtime semantics changes.

Verification:

```bash
python tests/run_pack_golden.py econ_model_supply_demand_equilibrium_v1
```
