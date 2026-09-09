# P4 shared runtime explicit AGE target W1 handoff

## 실행 계약

- AI_PROVIDER: OpenAI
- AI_SURFACE: Codex local task
- AI_CAPABILITY: product single-writer implementation and verification
- SESSION_NICKNAME: DDN V1제품마감Codex
- PROJECT_ROLE: DDN V1/V1.x single product writer
- RETURN_LABEL: `[DDN V1제품마감Codex -> Codex관리Work]`
- DEEP_RESEARCH_CHECK: NOT_USE — live repository authority와 실행 가능한 기존 제품 테스트로 결정 가능했다.

## 권위와 계보

- internal live CURRENT: v25.35.0 / RD-001~490
- public Language SPEC: v0.6.0
- baseline: `65dcb1872d7b6b9099d85138c36bf2381c52bbed`
- fixed product/test HEAD: `926175c52b42fca0e36d2891a37260ec3f69f6d1`
- fixed tree: `15b0295f55e2b7ab6b32ca6c5a65566d15491361`
- fixed parent: baseline과 exact direct parent
- merge count: 0
- authority impact: `UNAFFECTED_WITH_EXPLICIT_PRODUCT_CONVERGENCE`. v25.35의 U-01~U-07 higher-structure successor는 이 AGE-target route의 의미를 바꾸지 않는다.

## 사용자 workflow와 제품 변경

기존 `teul-cli run --age-target AGE*` 공개 옵션은 shared runtime 진입 시 항상 `E_SHARED_RUNTIME_OPTION_UNSUPPORTED`로 거부됐다. 이제 일반 DDN 원문 실행은 기존 `AgeTarget` parser와 shared `DdnProgram` age gate를 한 번만 소비한다.

- `AGE0`: AGE1 상태머신 원문을 `E_AGE_NOT_AVAILABLE` / `state_machine_literal`로 fail-closed 거부
- `AGE1`: 동일 원문을 official CLI shared runtime에서 수용
- 명시 AGE identity: shared summary와 execution envelope에 기록하며 run identity material에 포함
- global default: 읽기만 하고 변경하지 않음; 명시 호출 전후 값 불변
- legacy/default caller: 기존 default path와 run-id material 보존
- model source + explicit AGE: 기존 generic unsupported guard를 유지하여 옵션을 묵살하지 않음
- hidden PreV25 fallback, private teul semantic lowering, 새 parser/canon authority: 0

## exact product diff

- `tool/src/ddn_runtime.rs`
- `tool/src/runtime_surface.rs`
- `tools/teul-cli/src/cli/run.rs`

변경은 위 3개 경로뿐이다. tracked WASM, UI, pack, docs/ssot, publish/spec, public naming/command membership diff는 0이다.

## RED, GREEN, mutation

- pre-implementation RED: 기존 `run_file_routes_explicit_age_target_through_shared_runtime` 제품-facing test가 `E_SHARED_RUNTIME_OPTION_UNSUPPORTED`를 관찰해 실패했다.
- focused GREEN:
  - native shared runtime explicit AGE test 1/1 PASS
  - official teul-cli shared-runtime AGE test 1/1 PASS
- mutation `EXPLICIT_AGE_TARGET_FALLS_BACK_TO_GLOBAL_DEFAULT`:
  - 명시 target 전달을 default target으로 한 번 치환
  - AGE0 상태머신이 잘못 수용되어 actual RED exit 1
  - exact source restore 후 focused native/CLI GREEN
  - mutation residue 0

## 회귀와 환경 분리

- `cargo test --manifest-path tool/Cargo.toml --lib`: 526/526 PASS
- clean external target의 `cargo test --manifest-path tools/teul-cli/Cargo.toml --bin teul-cli`: 1044 PASS / 14 FAIL
- 14 failures는 새 AGE test가 아니며 legacy 보임/assignment/foreach private-runtime 축이다. 이 slice는 이를 PASS로 승격하거나 수정하지 않는다.
- shared Cargo target에서는 stale artifact가 `serde_json 1.0.147`와 `1.0.149`를 혼합해 compile error를 냈다. 새 clean target은 단일 `serde_json 1.0.149`로 정상 compile/test했으므로 제품 결함으로 분류하지 않는다.
- clean target path: `I:/home/urihanl/ddn/codex/out/ddn-v1-shared-runtime-age-target-w1`

## anti-meta

- USER_WORKFLOW_CHANGED_OR_UNBLOCKED: `teul-cli run --age-target AGE0|AGE1|AGE2|AGE3`가 일반 DDN shared runtime에 실제로 도달한다.
- NEW_TEST_ARTIFACT_COUNT: 0
- EXISTING_TEST_REUSED_COUNT: 3 (기존 teul in-file test 확장, tool lib, teul full suite)
- META_TEST_CREATED: 0
- NEW_PACK_COUNT: 0
- NEW_RUNNER_COUNT: 0
- STOP_RULE_APPLIED: true
- NEXT_PRODUCT_DECISION_ENABLED: official CLI의 invocation-local AGE 계약을 coherent P4/P5 review bundle에 포함할 수 있다.

## review와 열린 gate

- status: `P4_SHARED_RUNTIME_EXPLICIT_AGE_TARGET_IMPLEMENTED_UNDER_REVIEW`
- rolling reviewer dispatch: 0. 관리가 기존 rolling reviewer와 coherent milestone을 선택한다.
- P2 durable revision physical schema/wire, VC15 typed morphology physical schema, VC17 exact provider membership은 계속 Owner/open gate다.
- broad P1/P2/P3/P4/P5/P6 closure, V1 membership/readiness, Windows RC, release/activation/legal, Owner Human Smoke/Human PASS는 주장하지 않는다.
