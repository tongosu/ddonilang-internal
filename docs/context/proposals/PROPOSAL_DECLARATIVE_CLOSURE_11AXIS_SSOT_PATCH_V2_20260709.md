# PROPOSAL_DECLARATIVE_CLOSURE_11AXIS_SSOT_PATCH_V2_20260709

Status: proposal-ready, docs-first. Runtime landed claim: no.
Supersedes: `PROPOSAL_DECLARATIVE_CLOSURE_11AXIS_SSOT_PATCH_V1_20260709.md`.
Generated: 2026-07-09 KST.
Source instruction: `CODEX HANDOFF 2026-07-09 — 11축 proposal V2 수정 + G1~G3 구현 재개 지시서`.

## Boundary

Codex did not edit `docs/ssot/**`. `AGENTS.md` and `SSOT_POLICY.md` forbid direct SSOT edits by Codex, so this file is the SSOT owner handoff for the requested V2 correction.

This proposal must be read as `v24.13.0-candidate` candidate text only:

- No new core block.
- `= / <- / =:=` semantics unchanged.
- No `잇기{}`, `풀림길{}`, `성질{}`, `이야기{}`, or `사건{}` block introduction.
- No runtime landed claim for SolvePlan, acausal solve, derivative semantics, constraints, unit inference, or experiment manifest.
- No `state_hash` formula implementation change in this proposal.

## V2 Drift Corrections

| ID | Correction |
|---|---|
| P1 | A7 direction corrected: `채비 {}` remains top-level only, and `세움 {}` inside `채비 {}` is the t=0 one-shot init solve candidate. |
| P2 | S0 restored to explicit algebra plus deterministic causalization: bipartite matching, topological sort, and source-declaration-order tie-break. Constants/assignments are only a subset. |
| P3 | A4 full runtime contracts restored, including hook write ordering and next-segment application. `다시놓기` is a sub-path of contract 2, not the whole contract. |
| P4 | Constraint naming reopened in V1 is closed: family `막음`, verb `막기`. Reaction vocabulary restored to `멈춤`, `튕김(e)`, `조임`, `감쌈`. |
| P5 | Pack queue omissions added, including connect lowering/diagnostics, circuit/econ demos, init equation, and vector ODE packs. |

## Current Evidence

| Evidence | Current source |
|---|---|
| `세움{}` is canonical, and `세움값` content is state-hash relevant while check results/diagnostics are excluded | `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5747`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5755`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5756` |
| Existing v24.12.9 candidate already says `세움`, prime notation, owner-inner `세움`, and `잇기` lowering are candidates, not runtime landed | `docs/ssot/ssot/SSOT_UPDATE_NOTES_v24.12.9.md:16`, `docs/ssot/ssot/SSOT_UPDATE_NOTES_v24.12.9.md:17`, `docs/ssot/ssot/SSOT_UPDATE_NOTES_v24.12.9.md:19` |
| `될때` / `인 동안` are designed surfaces, not full runtime | `docs/ssot/ssot/SSOT_DECISIONS_v24.12.9.md:446`, `docs/ssot/ssot/SSOT_DECISIONS_v24.12.9.md:453`, `docs/ssot/ssot/SSOT_DECISIONS_v24.12.9.md:539` |
| D-STRICT excludes external I/O/time/random host calls except sealed deterministic paths | `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:4075`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6589`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6608` |
| Unit postfix and caret exponent rules already exist in v24.12.9 | `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3330`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3173`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6302` |
| Deterministic RNG currently exists as seed-based global sequence | `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6437`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6449`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6450` |

Line numbers are current as of V1 proposal generation and must be rechecked immediately before SSOT landing.

## Proposed `SSOT_UPDATE_NOTES_v24.13.0-candidate` Entry

Target file/section: `docs/ssot/ssot/SSOT_UPDATE_NOTES_v24.12.9.md`, new top section before the v24.12.9 notes.

Proposed text:

```md
## v24.13.0-candidate 선언형 closure 11축 후보

- `세움` 중심 선언형 시뮬레이션을 SolvePlan 기반 후보로 확장한다. 이번 반영은 설계 채택(candidate)이며 runtime landed claim이 아니다.
- SolvePlan은 S0 명시적 대수 + 결정적 인과화(이분 매칭 + 위상정렬, tie-break = 소스 선언 순서), S1 선형 방정식계(`N <= 8`), S2 명시 ODE 적분, S3 보류/진단 단계로 나눈다. 상수/대입은 S0의 부분집합이다.
- `위치'` / `위치''`는 `세움{}` 안에서만 시간 미분 슬롯으로 읽는 후보이다. 현 단계에서 `세움{}` 밖 prime-suffix 식별자는 경고 진단(W급)을 내고 식별자로 계속 수용한다. 다음 major에서 `E_PRIME_OUTSIDE_SEUM` 오류로 승격하되, 승격 전 parser/frontdoor 사용자 샘플과 pack 영향 검증을 마친다.
- `E_PRIME_NOT_STATE`는 현 단계부터 `세움{}` 안 비상태 prime 사용 오류다. `base'''`는 계속 거부한다.
- `잇기`는 문장형 endpoint sugar에서 `세움{}` relation row로 낮추는 후보로 유지하고, `잇기{}` 블록은 만들지 않는다.
- `될때` / `인 동안` full runtime은 세 계약이 모두 갖춰진 뒤에만 승격한다: edge/level 내장, hook 쓰기 계약, tick-quantized event와 관통 오차 상한 문서화.
- hook 쓰기 계약은 `<-` 쓰기가 다음 마디 시작 상태에 적용되고, 같은 마디 다중 hook은 선언 순서로 실행되며, 같은 변수는 마지막 쓰기가 승리하고, 이 순서는 SolvePlan 기록에 남는다는 뜻이다.
- `다시놓기`는 prime 상태 불연속 재설정 전용 하위 통로이며 hook 밖 사용은 `E_DASINOKI_OUTSIDE_HOOK`이다.
- constraint family는 `막음`, 동사는 `막기`로 확정한다. 반응 어휘는 `멈춤`, `튕김(e)`, `조임`, `감쌈`이다. `미끄러짐`은 follow-on 후보이고, abort/diag는 반응이 아니라 진단 계열이다.
- 단위/차원 정적 계층은 `@` postfix와 caret exponent 표기를 유지한다. 예: `9.8@m/s^2`. scalar-unit mix 기본값은 명시 변환 없는 혼합 금지다.
- `채비 {}`는 top-level 전용 현행 의미를 유지한다. `채비 {}` 본문 안의 `세움 {}`은 t=0 1회 solve init 후보이며, SolvePlan S0/S1 runtime landing을 기다리지 않고 candidate로 등록한다.
- 벡터 미분 슬롯은 component lowering 후보로 둔다. 신규 벡터 미분 연산자 표면은 추가하지 않는다.
- 실험 manifest는 docs-first 후보로 두며, run artifact/record schema와 runtime state hash 산식은 건드리지 않는다.
- 표준부품 pack과 agent별 RNG stream은 후보로만 등록한다. traversal order와 무관한 per-agent RNG stream은 `(global_seed, agent_id, stream_name)` 파생식을 쓴다.
```

## A1-A11 Reflection Matrix

| Axis | Target SSOT file/section | Proposed decision/candidate text | Status |
|---|---|---|---|
| A1 `세움` acausal-lite / SolvePlan | `SSOT_DECISIONS` near `세움{}` current candidate; `SSOT_LANG` near `§R1A`; `SSOT_PLANS` immediate language hardcut line | `세움{}` relation content may produce a deterministic `SolvePlan` artifact. V2 stages are S0 explicit algebra plus deterministic causalization, S1 linear system with `N <= 8`, S2 explicit ODE integration, and S3 unsupported/deferred diagnostics. S0 causalization uses bipartite matching, topological sort, and source-declaration-order tie-break. Iterative convergence is not allowed in D-STRICT. | candidate, runtime not landed |
| A2 prime derivative slots | `SSOT_LANG` near prime/seum examples and `§R1A`; `SSOT_DEMOS` near current `위치'` demo | `base'` and `base''` are first/second time derivative slots only inside `세움{}` relation interpretation. Outside that context, the current stage keeps prime-suffix identifiers accepted with W-level warning; next major promotes this to `E_PRIME_OUTSIDE_SEUM` after migration checks. `E_PRIME_NOT_STATE` is an immediate error inside `세움{}`. `base'''` remains invalid. | candidate; parser support exists only |
| A3 endpoint `잇기` lowering | `SSOT_DECISIONS` connect/seum lines; `SSOT_DEMOS` endpoint connect examples | Sentence-form `잇기` lowers to `세움{}` relation rows. Potential/level equality rows use direct equality relation. Flow rows use incoming-positive sign convention and emit zero-sum relation. No `잇기{}` block. | candidate; frontdoor row helper exists |
| A4 `될때` / `인 동안` runtime contracts | `SSOT_DECISIONS` hook section; `SSOT_LANG` hook matrix | Full runtime requires three contracts: edge/level built-in state with previous condition values owned by runtime; hook write contract where `<-` writes apply to the next segment start, same-segment hooks run in declaration order, last write to the same variable wins, and ordering is recorded in SolvePlan; tick-quantized event plus penetration error bound `|velocity| x dt`. `다시놓기` is a contract-2 sub-path for prime-state discontinuity reset only. | candidate; current full runtime no |
| A5 `막음` / `막기` constraints | `SSOT_OPEN_ISSUES` existing OI closure note; `SSOT_PLANS` language follow-up queue | Constraint layer canonical family is `막음`, verb is `막기`; close existing `OI-SIM-CONSTRAINT-NAME-01` with this decision. Reaction vocabulary is `멈춤`, `튕김(e)`, `조임`, `감쌈`. `미끄러짐` is follow-on; abort/diag belongs to diagnostics. | candidate name closed, runtime no |
| A6 unit/dimension static layer | `SSOT_LANG` unit sections, especially postfix and exponent rules | Static dimension checking should report `E_UNIT_MISMATCH`. ASCII unit expression keeps caret exponent, e.g. `9.8@m/s^2`. Unknown unit remains current unit error. Scalar/unit mixing uses default B: forbid scalar-unit mix without explicit conversion; education examples must attach explicit units. | candidate; OI closes after corpus validation |
| A7 `채비 {}` containing `세움 {}` | `SSOT_LANG §R1A`; `SSOT_DECISIONS` `채비` section | `채비 {}` remains top-level only. A `세움 {}` inside a `채비 {}` body is a t=0 one-shot init solve candidate. It does not allow `채비 {}` inside `세움{}` and does not leak lexical locals into world state unless materialized by InitPlan/SolvePlan. | candidate now |
| A8 vector prime lowering | `SSOT_LANG` vector/math sections; `SSOT_DEMOS` physics examples | Vector derivative slots lower component-wise to scalar derivative rows. Component order is fixed by source declaration/canonical vector field order. No new vector derivative operator or block is introduced. | candidate only |
| A9 experiment manifest | `SSOT_TOOLCHAIN` / run artifact section; `SSOT_PLANS` toolchain candidate | Experiment manifest is a docs-first/run artifact candidate. It records source, seed, solver method, input snapshot boundary, and result pointers, but does not alter runtime record schema or `state_hash` formula in this batch. | docs-first |
| A10 standard parts packs | `SSOT_PLANS` pack queue; `SSOT_DEMOS` standard examples | Standard part packs should be named as packs, not language blocks. Candidate families: mass/spring/damper, resistor/capacitor/source, supply-demand/tax, queue/server. | pack proposal |
| A11 per-agent RNG stream | `SSOT_LANG` deterministic RNG; `SSOT_PLATFORM` multi-agent ordering | Each agent may own a deterministic RNG stream derived from `(global_seed, agent_id, stream_name)`. Stream consumption must be independent of traversal order. Current global sequence remains baseline until pack proof lands. | candidate; runtime no |

## Proposed `SSOT_OPEN_ISSUES` Updates

Target file/section: `docs/ssot/ssot/SSOT_OPEN_ISSUES_v24.12.9.md`, add/update under language/current candidate OI cluster.

```md
### OI-UNIT-SCALAR-MIX-01

결정 후보 기본값 B 승인: `숫자`와 단위 수(`수@단위`)는 명시 변환 없이 섞을 수 없고 `E_UNIT_MISMATCH`로 막는다. 교육 예제는 명시 단위 부착을 요구한다.

닫힘 조건: 교육 예제 corpus 검증 후 OI를 닫는다.
```

```md
### OI-SOLVEPLAN-ARTIFACT-SCHEMA-01

SolvePlan artifact 최소 field set은 `schema`, `source_hash`, `stage`, `method`, `relations`, `unknowns`, `lowering`, `diagnostics`, `state_hash_inputs`로 승인한다.

`state_hash_inputs`는 manifest field로 유지하며, 별도 proof artifact가 아니다. 실제 `state_hash` 산식 입력 통합은 설계 노트와 별도 승인 뒤 진행한다.
```

```md
### OI-SIM-CONSTRAINT-NAME-01

닫힘 결정: constraint family는 `막음`, 동사는 `막기`다. 신규 `OI-CONSTRAINT-SURFACE-NAME-01`은 만들지 않는다.
```

```md
### OI-RNG-PER-AGENT-STREAM-01

Per-agent RNG stream seed derivation은 `(global_seed, agent_id, stream_name)`로 승인한다. 이 파생식은 시앗묶음 named stream derivation과 같은 축으로 정렬한다.
```

## Proposed `SSOT_PLANS` Pack Queue

Target file/section: `docs/ssot/ssot/SSOT_PLANS_v24.12.9.md`, add to immediate language/simulation plan queue.

| Pack id | Purpose | Closure gate |
|---|---|---|
| `lang_seum_algebraic_v1` | S0 explicit algebra plus deterministic causalization SolvePlan | product runtime + golden |
| `lang_seum_linear_v1` | S1 linear system, `N <= 8`, deterministic unsupported diagnostics | product runtime + golden |
| `sim_seum_tick_phase_v1` | tick phase ordering for seum-derived values | product runtime + state trace |
| `lang_seum_diag_v1` | unsupported/nonlinear/cyclic relation diagnostics | product runtime + error code golden |
| `lang_prime_lexer_v1` | parser/frontdoor prime acceptance, W-level outside-seum warning, and third-prime rejection | already covered by existing prime parser packs; use as alias/checkpoint only |
| `lang_connect_lowering_v1` | 전지-전구 endpoint desugar golden | product runtime + golden |
| `lang_connect_diag_v1` | `E_CONNECT_*` diagnostic golden | product runtime + error code golden |
| `sim_circuit_series_v1` | 직렬 회로 수치 golden + hash | product runtime + numeric golden |
| `sim_econ_market_v1` | 가계-장터 relation demo | product runtime + golden |
| `sim_init_equation_v1` | `채비 { 세움 { ... } }` t=0 solve with InitPlan | product runtime + InitPlan golden |
| `sim_ode_first_order_v1` | `x' = f(...)` S2 explicit ODE lowering | product runtime + golden |
| `sim_ode_second_order_v1` | `x'' = f(...)` lowering to first-order system | product runtime + golden |
| `sim_ode_vector_v1` | vector component prime lowering with fixed component order | product runtime + golden |
| `sim_ode_method_switch_v1` | deterministic method selection, e.g. Euler vs semi-implicit Euler | product runtime + golden |
| `sim_constraint_reaction_v1` | `막음`/constraint reaction candidates | red/green pack after OI |
| `sim_mageum_floor_v1` | floor contact unit under `sim_constraint_reaction_v1` | sub-pack runner |
| `sim_mageum_box_v1` | box contact unit under `sim_constraint_reaction_v1` | sub-pack runner |
| `sim_mageum_chain_v1` | chained constraint unit under `sim_constraint_reaction_v1` | sub-pack runner |
| `lang_mageum_diag_v1` | `막음`/`막기` diagnostics under `sim_constraint_reaction_v1` | sub-pack runner |
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
// t=0 init solve candidate. Runtime landed claim: no.
채비 {
  세움 {
    x + y =:= 5.
    x - y =:= 1.
  }.
}.
```

```ddn
// Hook reset candidate. Runtime landed claim: no.
(HP <= 0)이 될때 {
  상태 <- "끝".
  HP 다시놓기.
}.
```

## Decisions Reflected

1. `OI-UNIT-SCALAR-MIX-01`: candidate default B approved; close after education example corpus validation.
2. `OI-SOLVEPLAN-ARTIFACT-SCHEMA-01`: minimum field set approved; `state_hash_inputs` remains a manifest field.
3. Constraint name: `막음`/`막기` fixed; no new constraint naming OI.
4. `OI-RNG-PER-AGENT-STREAM-01`: derivation `(global_seed, agent_id, stream_name)` approved.
5. `채비`/`세움` nesting: `채비 { 세움 { ... } }` candidate accepted now; V1 question was invalid and is removed.
6. Prime outside `세움`: current stage warning + identifier acceptance; next major promotion to `E_PRIME_OUTSIDE_SEUM` after migration checks.

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
