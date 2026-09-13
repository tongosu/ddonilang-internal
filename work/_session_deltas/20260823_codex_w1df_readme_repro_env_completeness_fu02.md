# DDN-W1DF-FU02 README 재현 환경변수 완결

## 범위와 기준점

- task: `DDN-W1DF-FU02`
- baseline: `ccee4366373c77e48ef929e2fd502dda19ba0a0a`
- bound review: `091a08d107637ce7b282db16f71017cadb552ff9`
- exact README:
  `pack/future_grammar_atlas_owner_closed_delta_r2_w1df/README.md`
- exact product-evidence runner:
  `tests/ddn_execution_concurrency_w1df_product_evidence_runner.mjs`
- inherited official runner:
  `tests/ddn_execution_concurrency_w1c1_sender_route_provider_runner.mjs`
- README before: `1,918` bytes,
  SHA-256 `6c071cf53d25fe583d2eeeb09676263b4bf6092394069aa5373e605b3e8942be`
- README after: `2,628` bytes,
  SHA-256 `daf96b3ef4338abe35cfcb38fe4136b07f7367531bf215d33efaa192d9fed7e8`

## 교정

README 재생 블록에 다음 세 fail-closed 입력을 명시했다.

```text
set DDN_W1C1_CLI=<isolated workspace target>\debug\ddonirang-tool.exe
set DDN_W1C1_WASM_DIR=<source-built Node.js WASM output directory>
set DDN_W1C1_TRACKED_WASM_DIR=<repository>\solutions\seamgrim_ui_mvp\ui\wasm
```

CLI는 파일, 두 WASM 값은 디렉터리다. source-built Node.js WASM과 tracked
Workbench WASM은 서로 다른 identity이고 fallback이나 디렉터리 교환은 허용하지 않는다.
logical oracle은 제품 실행 근거가 아니며 capacity 증거는
`RUST_INTERNAL_TYPED_ONLY`로 유지한다. public bounded-capacity surface는 OPEN이다.

## 재현과 불변

- 봉인 artifact identity를 먼저 확인한 뒤 README 명령을 명시적 환경변수로 실행했다.
- clean-detached CLI SHA-256:
  `9f9f9fad053351a59eddfa8a6f54bf8d5608f3f9f7fc1ebc3d56aef11fee5291`
- source-built Node.js WASM SHA-256:
  `87992c2393592c4f9c568242b37261209708488f1e3e28f5ba69bb4a00054ed2`
- tracked Workbench WASM SHA-256:
  `fbccef544253e2ffe1c05abda1826ce34e785a4de193bfe59dec48d7898dde05`
- W1-C1 official public cases: `10/10` (`success 6`, `failure 4`).
- W1DF 연결 internal named Rust evidence: `7/7`.
- 누락 환경변수, 잘못된 CLI, source-built/tracked WASM 디렉터리 교환은 각각
  fail-closed로 확인했다.
- 제품, runner, oracle, expected ledger, UI, tracked WASM, `docs/ssot/**`,
  `publish/spec/**` diff는 0이다.
- 검증용 v24.44.1 SSOT bridge는 읽기 전용 임시 junction으로만 사용하고 제거한다.
- 공식 DB write, activation call, PID `53196`/port `8787` 접근은 0이다.

## 상태

```text
W1DF_README_REPRO_ENV_COMPLETENESS_FOLLOW_UP_CLOSED
W1DF_README_REPRO_COMMAND_SELF_CHECK_PASS
DDN_EXECUTION_CONCURRENCY_W1DF_FOLLOW_UP_CORRECTION_CLOSED
W1DF_INDEPENDENT_PLAIN_PASS_BOUND
W1_FULL_CLOSURE_OPEN
W1C2_REACTION_PROVIDER_PUBLIC_SURFACE_OPEN
PUBLIC_BOUNDED_CAPACITY_CONFIGURATION_OPEN
RENDEZVOUS_RUNTIME_OPEN
WORKBENCH_STRUCTURED_DIAGNOSTIC_PROPAGATION_OPEN
RD207_PUBLIC_STABLE_WIRE_OPEN
PUBLIC_ACTIVATION_NOT_AUTHORIZED
HUMAN_PASS_NOT_CLAIMED
external_user_success_count: 0
```
