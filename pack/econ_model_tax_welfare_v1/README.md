# econ_model_tax_welfare_v1

Model-first G1 skeleton for a linear tax-welfare calculation.

- evidence_tier: `skeleton/docs_first`
- track: `model-first`
- counterpart shape: `agent-first` five-slot symmetry
- closure claim: executable pack recognition only

Agent-first symmetry slots:

| Slot | Model-first role | Agent-first counterpart name |
|---|---|---|
| household | consumer surplus | `agent_first_household_v1` |
| firm | producer surplus | `agent_first_firm_v1` |
| market | traded quantity | `agent_first_market_v1` |
| government | tax revenue | `agent_first_government_v1` |
| central_bank | not used in this fiscal model | `agent_first_central_bank_v1` |

This pack does not claim real-world prediction, policy advice, parser changes, grammar changes, or runtime semantics changes.

Verification:

```bash
python tests/run_pack_golden.py econ_model_tax_welfare_v1
```
