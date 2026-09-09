# stdlib_l1_integrators_g1_v1

G4 runner pack for the existing L1 numeric helpers used by simple physics lessons.

Evidence tier: `runner_golden`.

This pack uses existing product-path helpers only:

| G4 label | Product surface used | Pendulum sample role |
|---|---|---|
| `적분.오일러` | `적분.오일러` | explicit Euler one-step theta/omega |
| `적분.반암시적오일러` | `적분.반암시적오일러` | semi-implicit Euler one-step theta/omega |
| `선형보간` | `보간.선형` | interpolation between explicit and semi-implicit theta |

No new language surface, runtime helper, or physics solver is introduced here.

Verification:

```bash
python tests/run_pack_golden.py stdlib_l1_integrators_g1_v1
python tests/run_stdlib_l1_integrators_g1_check.py
```
