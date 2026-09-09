# econ_model_money_supply_v1

Model-first G1 skeleton for a quantity-theory money supply scenario.

- evidence_tier: `skeleton/docs_first`
- track: `model-first`
- counterpart shape: `agent-first` five-slot symmetry
- closure claim: executable pack recognition only

Agent-first symmetry slots:

| Slot | Model-first role | Agent-first counterpart name |
|---|---|---|
| household | spending demand placeholder | `agent_first_household_v1` |
| firm | output supply placeholder | `agent_first_firm_v1` |
| market | price level observation | `agent_first_market_v1` |
| government | fiscal neutral placeholder | `agent_first_government_v1` |
| central_bank | money supply lever | `agent_first_central_bank_v1` |

This pack does not claim real-world prediction, policy advice, parser changes, grammar changes, or runtime semantics changes.

Verification:

```bash
python tests/run_pack_golden.py econ_model_money_supply_v1
```
