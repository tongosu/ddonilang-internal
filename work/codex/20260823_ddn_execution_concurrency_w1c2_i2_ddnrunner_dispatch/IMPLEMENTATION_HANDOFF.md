# DDN-W1C2-I2 실제 DdnRunner 내부 dispatch 연결 구현 인계

## 판정 경계

```text
DDN_EXECUTION_CONCURRENCY_W1C2_I2_DDNRUNNER_INTERNAL_DISPATCH_CONNECTION_IMPLEMENTED_UNDER_REVIEW
DDNRUNNER_REACTION_PROVIDER_DISPATCH_INTEGRATION_LANDED
DEFAULT_PUBLIC_RUNTIME_PROVIDER_REGISTRY_EMPTY
INTERNAL_TYPED_REGISTRY_INJECTION_EVIDENCE_ONLY
REACTION_PROVIDER_PUBLIC_SOURCE_REACHABILITY_0
W1C2_CASE22_EVIDENCE_LABEL_ACCURACY_FOLLOW_UP_CLOSED
W1C2_I2_INDEPENDENT_PASS_NOT_YET_ISSUED
```

독립 판정, W1-C2 전체 닫힘, public surface, stable wire, activation은 주장하지 않는다.

## 고정점

- baseline: `af7ad5224c4645c81316fe72fb092ac337374347`
- Owner binding: `235d2012`
- I1 product/test fixed: `138b2eb759fb36298663381565ea38a7e245d547`
- I1 review: `3c1a8956`
- I2 product implementation: `242857bb70cfd2f5bb18797210481d97e86f3577`
- I2 product/test fixed: `5b822e3f8754d3cf38fa1d26a9786dc9fbd6115e`
- ancestry: baseline -> product implementation -> product/test fixed
- merge commit count: `0`

## 구현

- I1의 shared typed `EndpointRoute`/`ReactionProvider` core를 실제 `DdnRunner::run_update`
  delivery 경로에 연결했다.
- route cardinality를 먼저 확정하고 exactly-one route일 때만 provider group을 resolve한다.
- provider들은 동일 settled snapshot을 읽고 candidate를 정본 순서로 병합하며, provider나
  route 실패 때 route state, provider candidate, outbox, effect intent를 함께 publish하지 않는다.
- outer commit 뒤 provider publish와 `EffectIntent` release가 일어나도록 순서를 봉인했다.
- 기본 DdnRunner registry는 empty다. 내부 typed injection은 Rust 검증 전용이며 parser,
  CLI option, environment, WASM export, Workbench control을 추가하지 않았다.
- I1 case 22는 tool의 actual DdnRunner 실행과 teul-cli empty-registry static scan을 서로
  다른 근거로 정확히 표기했다. 기대 의미나 public 지원 주장은 바꾸지 않았다.

## 검증 요약

- actual DdnRunner integration: `15/15 PASS`
- public provider ingress tripwires: source token/input, CLI option, env, WASM export,
  UI control 모두 `0`
- fault injection: 10축 각각 `GREEN -> 실제 source mutation RED -> 복원 GREEN`, `10/10`
- I1 regression: `23/23 PASS`
- W1-C1 public regression: `10/10 PASS`
- W1-B native/source-node/tracked parity: `PASS`
- W1-D~F logical oracle: `65/65 PASS`
- W1-D~F capacity와 detached product evidence: `PASS`
- lang: `363/363 PASS`; tool: `492/492 PASS`; teul-cli: `1165/1165 PASS`
- WorkCost CLI/WASM parity: `PASS`, 일반 경로 `rd206_resource_capability=false`
- freshness/deploy artifact checkers: `PASS`
- clean-detached fixed HEAD actual DdnRunner pack: `15/15 PASS`
- actual Microsoft Edge: 성공 실행/저장, server PID 교체, exact 재열기, unhandled와
  ambiguity 오류 보존, console/page/network error `0`, public provider input `0`

## WASM과 보호 경계

- source A = source B = tracked web WASM
- SHA-256: `d91af594b3848b844f3f2df74217f0d7f6e562720b303bc936497df3fc91bdc8`
- bytes: `5,508,839`
- manifest source tree: `5d4b18139bf3a256fcab91af92001160a630ab5a298c912741514488b37ffc37`
- source file count: `91`
- official DB: `540,672` bytes, SHA-256
  `c8fdd4d47e20f7ad7ce4f095389991859432d5af0a87aa1f7b0b06e90fe44228`
- PID `53196` and `127.0.0.1:8787`: unchanged
- official writes: `0`; activation calls: `0`
- `docs/ssot/**`, `publish/spec/**`, Workbench UI source: diff `0`

## 계속 OPEN

```text
PUBLIC_KOREAN_NAME_OPEN
PUBLIC_PROVIDER_EXACT_SYNTAX_OPEN
PUBLIC_PROVIDER_SOURCE_INGRESS_0
STABLE_PROVIDER_IDENTITY_WIRE_OPEN
STABLE_PROVIDER_DIAGNOSTICS_OPEN
WORKBENCH_STRUCTURED_DIAGNOSTIC_PROPAGATION_OPEN
W1_FULL_CLOSURE_OPEN
RENDEZVOUS_RUNTIME_OPEN
RD207_PUBLIC_STABLE_WIRE_OPEN
PUBLIC_ACTIVATION_NOT_AUTHORIZED
HUMAN_PASS_NOT_CLAIMED
external_user_success_count: 0
```
