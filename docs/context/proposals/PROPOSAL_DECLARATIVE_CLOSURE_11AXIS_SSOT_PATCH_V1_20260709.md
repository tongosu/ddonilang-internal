# PROPOSAL_DECLARATIVE_CLOSURE_11AXIS_SSOT_PATCH_V1_20260709

Status: superseded by `PROPOSAL_DECLARATIVE_CLOSURE_11AXIS_SSOT_PATCH_V2_20260709.md`.
Previous status: proposal-ready, docs-first. Runtime landed claim: no.
Superseded reason: 2026-07-09 handoff review found five drift items: A7 direction, S0 definition, A4 contract 2, A5 naming/reaction vocabulary, and pack queue omissions.
Generated: 2026-07-09 KST.
Source instruction: `CODEX DEVGOALS 2026-07-09 — 선언형 closure 11축 SSOT 반영`.

## Boundary

Codex did not edit `docs/ssot/**`. `AGENTS.md` and `SSOT_POLICY.md` forbid direct SSOT edits by Codex, so this file is the SSOT owner handoff for the requested Part A reflection.

This proposal must be read as `v24.13.0-candidate` candidate text only:

- No new core block.
- `= / <- / =:=` semantics unchanged.
- No `잇기{}`, `풀림길{}`, `성질{}`, `이야기{}`, or `사건{}` block introduction.
- No runtime landed claim for SolvePlan, acausal solve, derivative semantics, constraints, unit inference, or experiment manifest.
- No `state_hash` formula implementation change in this proposal.

## Current Evidence

| Evidence | Current source |
|---|---|
| `세움{}` is canonical, and `세움값` content is state-hash relevant while check results/diagnostics are excluded | `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5747`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5755`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5756` |
| Existing v24.12.9 candidate already says `세움`, prime notation, owner-inner `세움`, and `잇기` lowering are candidates, not runtime landed | `docs/ssot/ssot/SSOT_UPDATE_NOTES_v24.12.9.md:16`, `docs/ssot/ssot/SSOT_UPDATE_NOTES_v24.12.9.md:17`, `docs/ssot/ssot/SSOT_UPDATE_NOTES_v24.12.9.md:19` |
| `될때` / `인 동안` are designed surfaces, not full runtime | `docs/ssot/ssot/SSOT_DECISIONS_v24.12.9.md:446`, `docs/ssot/ssot/SSOT_DECISIONS_v24.12.9.md:453`, `docs/ssot/ssot/SSOT_DECISIONS_v24.12.9.md:539` |
| D-STRICT excludes external I/O/time/random host calls except sealed deterministic paths | `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4075`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6589`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6608` |
| Unit postfix and caret exponent rules already exist in v24.12.9 | `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3330`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3173`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6302` |
| Deterministic RNG currently exists as seed-based global sequence | `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6437`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6449`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6450` |

Line numbers are current as of this proposal generation and must be rechecked immediately before SSOT landing.

## Proposed `SSOT_UPDATE_NOTES_v24.13.0-candidate` Entry

Target file/section: `docs/ssot/ssot/SSOT_UPDATE_NOTES_v24.12.9.md`, new top section before the v24.12.9 notes.

Proposed text:

```md
## v24.13.0-candidate 선언형 closure 11축 후보

- `세움` 중심 선언형 시뮬레이션을 SolvePlan 기반 후보로 확장한다. 이번 반영은 설계 채택(candidate)이며 runtime landed claim이 아니다.
- SolvePlan은 S0 상수/대입, S1 선형 방정식계(`N <= 8`), S2 명시 ODE 적분, S3 보류/진단 단계로 나눈다.
- `위치'` / `위치''`는 `세움{}` 안에서만 시간 미분 슬롯으로 읽는 후보이며, S2 낮춤 전까지 일반 식별자 parser 수용 이상을 주장하지 않는다.
- `잇기`는 문장형 endpoint sugar에서 `세움{}` relation row로 낮추는 후보로 유지하고, `잇기{}` 블록은 만들지 않는다.
- `될때` / `인 동안`은 `상태`, `edge`, `reset` 계약이 갖춰진 뒤에만 full runtime으로 승격한다. reset 동사는 `다시놓기`를 후보 정본으로 둔다.
- `막음` / `막기`는 constraint/reaction layer 후보로 두되, 접촉/벽/경계 제약의 runtime 구현 claim은 하지 않는다.
- 단위/차원 정적 계층은 `@` postfix와 caret exponent 표기를 유지한다. 예: `9.8@m/s^2`. scalar/unit 혼합 규칙은 `OI-UNIT-SCALAR-MIX-01`로 남긴다.
- `채비 {}` inside `세움{}`는 t=0 solve init 후보로만 둔다. top-level `채비 {}` 현행 의미와 충돌시키지 않는다.
- 벡터 미분 슬롯은 component lowering 후보로 둔다. 신규 벡터 미분 연산자 표면은 추가하지 않는다.
- 실험 manifest는 docs-first 후보로 두며, run artifact/record schema와 runtime state hash 산식은 건드리지 않는다.
- 표준부품 pack과 agent별 RNG stream은 후보로만 등록한다. traversal order와 무관한 per-agent RNG stream은 별도 pack으로 검증하기 전까지 runtime landed claim을 하지 않는다.
```

## A1-A11 Reflection Matrix

| Axis | Target SSOT file/section | Proposed decision/candidate text | Status |
|---|---|---|---|
| A1 `세움` acausal-lite / SolvePlan | `SSOT_DECISIONS` near `세움{}` current candidate; `SSOT_LANG` near `§R1A`; `SSOT_PLANS` immediate language hardcut line | `세움{}` relation content may produce a deterministic `SolvePlan` artifact. V1 stages are S0 direct substitution/constant rows, S1 linear system with `N <= 8`, S2 explicit ODE integration, and S3 unsupported/deferred diagnostics. The artifact is compile-time/runtime-plan deterministic; iterative convergence is not allowed in D-STRICT. | candidate, runtime not landed |
| A2 prime derivative slots | `SSOT_LANG` near prime/seum examples and `§R1A`; `SSOT_DEMOS` near current `위치'` demo | `base'` and `base''` are first/second time derivative slots only inside `세움{}` relation interpretation. Outside that context they remain identifiers accepted by parser/frontdoor but have no derivative semantics. `base'''` remains invalid. | candidate, parser support exists only |
| A3 endpoint `잇기` lowering | `SSOT_DECISIONS` connect/seum lines; `SSOT_DEMOS` endpoint connect examples | Sentence-form `잇기` lowers to `세움{}` relation rows. Potential/level equality rows use direct equality relation. Flow rows use incoming-positive sign convention and emit zero-sum relation. No `잇기{}` block. | candidate; frontdoor row helper exists |
| A4 `될때` / `인 동안` runtime contracts | `SSOT_DECISIONS` hook section; `SSOT_LANG` hook matrix | Full runtime requires three contracts: stored previous-condition state, tick-quantized edge/level evaluation, and explicit reset verb `다시놓기`. Until all three are implemented, the surfaces remain designed/not landed. | candidate; current full runtime no |
| A5 `막음` / `막기` constraints | `SSOT_OPEN_ISSUES` new OI; `SSOT_PLANS` language follow-up queue | Constraint layer candidates: hard stop, bounce, slide, and abort/diag reaction. Names are candidates only and must avoid collision with existing `물림`/contract wording. | proposal only |
| A6 unit/dimension static layer | `SSOT_LANG` unit sections, especially postfix and exponent rules | Static dimension checking should report `E_UNIT_MISMATCH`. ASCII unit expression keeps caret exponent, e.g. `9.8@m/s^2`. Unknown unit remains current unit error. Scalar/unit mixing remains `OI-UNIT-SCALAR-MIX-01`. | candidate; OI open |
| A7 `채비 {}` inside `세움{}` | `SSOT_LANG §R1A`; `SSOT_DECISIONS` `채비` section | Inside `세움{}`, `채비 {}` is a t=0 solve initialization candidate. It does not change top-level `채비 {}` root declaration semantics and must not leak lexical locals into world state unless materialized by SolvePlan. | candidate only |
| A8 vector prime lowering | `SSOT_LANG` vector/math sections; `SSOT_DEMOS` physics examples | Vector derivative slots lower component-wise to scalar derivative rows. No new vector derivative operator or block is introduced. | candidate only |
| A9 experiment manifest | `SSOT_TOOLCHAIN` / run artifact section; `SSOT_PLANS` toolchain candidate | Experiment manifest is a docs-first/run artifact candidate. It records source, seed, solver method, input snapshot boundary, and result pointers, but does not alter runtime record schema or `state_hash` formula in this batch. | docs-first |
| A10 standard parts packs | `SSOT_PLANS` pack queue; `SSOT_DEMOS` standard examples | Standard part packs should be named as packs, not language blocks. Candidate families: mass/spring/damper, resistor/capacitor/source, supply-demand/tax, queue/server. | pack proposal |
| A11 per-agent RNG stream | `SSOT_LANG` deterministic RNG; `SSOT_PLATFORM` multi-agent ordering | Each agent may own a deterministic RNG stream derived from `(global_seed, agent_id, stream_name)`. Stream consumption must be independent of traversal order. Current global sequence remains baseline until pack proof lands. | candidate; runtime no |

## Proposed `SSOT_OPEN_ISSUES` Additions

Target file/section: `docs/ssot/ssot/SSOT_OPEN_ISSUES_v24.12.9.md`, add under language/current candidate OI cluster.

```md
### OI-UNIT-SCALAR-MIX-01

`숫자`와 단위 수(`수@단위`)를 같은 `세움{}` relation이나 arithmetic expression에서 섞을 때, scalar promotion을 허용할지 즉시 `E_UNIT_MISMATCH`로 막을지 결정한다.

- 후보 A: scalar는 dimensionless로만 허용한다.
- 후보 B: scalar-unit mix는 명시 변환 없이 전부 금지한다.
- 이번 후보 기본값: B. 교육 예제에서 필요한 경우 명시 단위 부착을 요구한다.
```

```md
### OI-SOLVEPLAN-ARTIFACT-SCHEMA-01

SolvePlan artifact의 public field set을 확정한다. 최소 후보는 `schema`, `source_hash`, `stage`, `method`, `relations`, `unknowns`, `lowering`, `diagnostics`, `state_hash_inputs`다.
```

```md
### OI-CONSTRAINT-SURFACE-NAME-01

`막음` / `막기` / `턱` / `제약` 중 constraint layer canonical surface를 선택한다. 이번 11축 후보는 이름을 확정하지 않고, block 신설도 하지 않는다.
```

```md
### OI-RNG-PER-AGENT-STREAM-01

Per-agent RNG stream seed derivation과 stream name namespace를 정한다. traversal-independent consumption proof pack 전까지 runtime landed claim을 금지한다.
```

## Proposed `SSOT_PLANS` Pack Queue

Target file/section: `docs/ssot/ssot/SSOT_PLANS_v24.12.9.md`, add to immediate language/simulation plan queue.

| Pack id | Purpose | Closure gate |
|---|---|---|
| `lang_seum_algebraic_v1` | S0 direct substitution / constant relation SolvePlan | product runtime + golden |
| `lang_seum_linear_v1` | S1 linear system, `N <= 8`, deterministic unsupported diagnostics | product runtime + golden |
| `sim_seum_tick_phase_v1` | tick phase ordering for seum-derived values | product runtime + state trace |
| `lang_seum_diag_v1` | unsupported/nonlinear/cyclic relation diagnostics | product runtime + error code golden |
| `lang_prime_lexer_v1` | parser/frontdoor prime acceptance and third-prime rejection | already covered by existing prime parser packs; use as alias/checkpoint only |
| `sim_ode_first_order_v1` | `x' = f(...)` S2 explicit ODE lowering | product runtime + golden |
| `sim_ode_second_order_v1` | `x'' = f(...)` lowering to first-order system | product runtime + golden |
| `sim_ode_method_switch_v1` | deterministic method selection, e.g. Euler vs semi-implicit Euler | product runtime + golden |
| `sim_constraint_reaction_v1` | `막음`/constraint reaction candidates | red/green pack after OI |
| `sim_unit_dimension_static_v1` | `E_UNIT_MISMATCH` and unit exponent static checks | parser/runtime diag golden |
| `sim_experiment_manifest_v1` | experiment manifest docs-first/run artifact shape | checker only first |
| `sim_agent_rng_stream_v1` | traversal-independent per-agent RNG streams | product runtime + determinism golden |

## Proposed `SSOT_DEMOS` Additions

Target file/section: `docs/ssot/ssot/SSOT_DEMOS_v24.12.9.md`, add as candidate demos after the current declarative `세움` demos.

```ddn
// S1 candidate: small linear relation solve. Runtime landed claim: no.
세움 {
  x + y =:= 5.
  x - y =:= 1.
}.
```

```ddn
// S2 candidate: first-order ODE lowering. Runtime landed claim: no.
세움 {
  위치' =:= 속도.
  속도' =:= 가속도.
}.
```

```ddn
// Unit candidate: caret exponent in ASCII unit expression.
채비 {
  중력가속도 <- 9.8@m/s^2.
}.
```

```ddn
// Hook reset candidate. Runtime landed claim: no.
(HP <= 0)이 될때 {
  상태 <- "끝".
  HP 다시놓기.
}.
```

## Questions / Decision Required

1. `OI-UNIT-SCALAR-MIX-01`: scalar-unit mix default.
2. `OI-SOLVEPLAN-ARTIFACT-SCHEMA-01`: public fields and whether `state_hash_inputs` is a manifest field or separate proof artifact.
3. `OI-CONSTRAINT-SURFACE-NAME-01`: `막음`/`막기` vs prior `턱` candidate.
4. `OI-RNG-PER-AGENT-STREAM-01`: stream derivation formula and stream namespace.
5. Whether `채비 {}` inside `세움{}` is accepted as a candidate now or deferred until SolvePlan S0/S1 lands.

## Non-Claims

This proposal does not claim:

- SolvePlan product runtime exists.
- `세움{}` can solve arbitrary algebraic systems.
- `위치'` / `위치''` runtime derivative semantics are implemented.
- `될때` / `인 동안` full runtime is implemented.
- `막음` / `막기` constraints are implemented.
- Unit static checker is implemented.
- Per-agent RNG streams are implemented.
- Any `docs/ssot/**` file was modified by Codex.
