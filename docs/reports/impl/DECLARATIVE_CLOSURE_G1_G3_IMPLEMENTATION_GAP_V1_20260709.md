# DECLARATIVE_CLOSURE_G1_G3_IMPLEMENTATION_GAP_V1_20260709

Generated: 2026-07-09 KST.
Scope: DEVGOALS Part B G1-G3 after Part A boundary review.
Result: partial. Product runtime closure not claimed.

## Boundary

The requested Part A direct SSOT reflection conflicts with repository policy. Codex did not edit `docs/ssot/**`, and G1-G3 were not promoted to behavior-closed status. The current deliverable is a gap report plus an SSOT patch proposal:

- `docs/context/proposals/PROPOSAL_DECLARATIVE_CLOSURE_11AXIS_SSOT_PATCH_V1_20260709.md`
- `work/_session_deltas/20260709_codex_declarative_closure_11axis.md`

## Current Product Evidence

| Area | Evidence | Reading |
|---|---|---|
| `세움{}` parsing | `lang/src/parser.rs:4353` parses assertion blocks and falls back to symbolic `=` / `=:=` bridges at `lang/src/parser.rs:4364` and `lang/src/parser.rs:4370`. | Assertion block syntax exists. This is not a SolvePlan pipeline. |
| `세움{}` runtime check | `tools/teul-cli/src/runtime/eval.rs:6240` parses assertion programs; `tools/teul-cli/src/runtime/eval.rs:6264` evaluates `살피기`; `tools/teul-cli/src/runtime/eval.rs:6310` records diagnostic/proof events. | Proof/check runtime exists. It does not solve and materialize derived simulation values. |
| `세움값` hash boundary | `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5755` says persisted `세움값` content is in `state_hash`; `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5756` excludes execution results/diagnostics. | Hash boundary is documented; requested SolvePlan artifact hash input is not implemented here. |
| Prime parser support | `lang/src/lexer.rs:1008`, `lang/src/lexer.rs:1402`, `lang/src/lexer.rs:1414`, `tools/teul-cli/src/lang/lexer.rs:605`, `tools/teul-cli/src/lang/lexer.rs:1144`, `tools/teul-cli/src/lang/lexer.rs:1155`. | `위치'` and `위치''` lexical support exists; `위치'''` is rejected. |
| Prime runtime semantics gate | `docs/context/proposals/LANG_PRIME_DERIVATIVE_RUNTIME_SEMANTICS_GATE_V1.md:7` and `tests/run_lang_prime_derivative_runtime_semantics_gate_check.py` explicitly preserve no derivative semantics landed claim. | G3 derivative semantics remain unimplemented. |
| Endpoint `잇기` rows | `lang/src/frontdoor.rs:27`, `lang/src/frontdoor.rs:1044`, `lang/src/frontdoor.rs:1554`, `lang/src/frontdoor.rs:1576`, and `tests/run_lang_connect_seum_lowering_parser_spike_check.py:233`. | Frontdoor row helper exists; no `잇기{}` block and no SolvePlan integration. |
| Existing integrators | `tools/teul-cli/src/runtime/eval.rs:3179`, `tools/teul-cli/src/runtime/eval.rs:3188`, `tools/teul-cli/src/runtime/eval.rs:3220`, `lang/src/stdlib.rs:1071`, `lang/src/stdlib.rs:1076`, `lang/src/stdlib.rs:1081`. | Standalone stdlib integrators exist. They are not automatically selected from prime derivative `세움{}` rows. |
| Existing relation solve | `tools/teul-cli/src/runtime/eval.rs:5497`, `tools/teul-cli/src/runtime/eval.rs:12394`, `tool/src/ddn_runtime.rs:12813`, `tool/src/ddn_runtime.rs:22396`. | Bounded relation solving exists in explicit `방정식풀기` paths; it is not named/serialized as SolvePlan S0/S1. |

## G1-G3 Status

| Goal | Requested DoD | Current status | Decision |
|---|---|---|---|
| G1 SolvePlan S0/S1 runtime | `lang_seum_algebraic_v1`, `lang_seum_linear_v1`, state hash inclusion, deterministic artifacts | Missing named `SolvePlan` product API, artifact schema, pack IDs, state hash integration. Some explicit relation-solving pieces exist. | Partial. Do not claim behavior closure. |
| G2 Seum tick phase | `sim_seum_tick_phase_v1`, derived value ordering, diagnostics | Existing proof guard can run each tick, but seum-derived value solve/write phase is not present. | Partial. Needs dedicated runtime design after SSOT acceptance. |
| G3 prime + S2 integrator runtime | `lang_prime_lexer_v1`, ODE first/second order packs, method switch | Prime lexer/parser support and standalone integrators exist. No derivative-slot-to-integrator lowering. | Partial. Parser part exists; runtime semantics not landed. |

## Missing Implementation Units

1. Define `SolvePlan` internal type and detjson artifact schema.
2. Add S0/S1 planner from canonical `세움{}` relation rows.
3. Connect S0/S1 planner to execution phase without changing `= / <- / =:=`.
4. Decide which SolvePlan fields are state hash inputs under DR-179-style boundary.
5. Add diagnostics for unsupported nonlinear, cyclic dependency, over-cap linear system, missing unknown, and unit mismatch.
6. Add S2 derivative slot lowering from `base'` / `base''` to explicit first-order state update.
7. Add method selection manifest for Euler/semi-implicit Euler and deterministic switch evidence.
8. Create packs only after the product path exists; redpacks are acceptable before green implementation, but behavior closure is not.

## Recommended Next Commits

1. `[DC-G1-RED]` Add red packs and checker for SolvePlan S0/S1 artifact shape.
2. `[DC-G1-CORE]` Implement product `SolvePlan` S0/S1 planner behind existing `세움{}` parser output.
3. `[DC-G2-PHASE]` Add seum solve phase in tick order and diagnostics.
4. `[DC-G3-S2]` Add derivative slot lowering to existing stdlib integrators.

## Verification Notes

At report creation time no product code was modified for G1-G3. The verification battery is recorded in `work/_session_deltas/20260709_codex_declarative_closure_11axis.md`.
