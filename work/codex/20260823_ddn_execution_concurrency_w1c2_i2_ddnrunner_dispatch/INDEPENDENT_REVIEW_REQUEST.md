# DDN-W1C2-I2 fixed-HEAD 독립 검토 요청

## 검토 고정점

```text
TASK: DDN-W1C2-I2-INTERNAL-DDNRUNNER-DISPATCH-CONNECTION
BASELINE: af7ad5224c4645c81316fe72fb092ac337374347
PRODUCT_IMPLEMENTATION: 242857bb70cfd2f5bb18797210481d97e86f3577
PRODUCT_TEST_FIXED_HEAD: 5b822e3f8754d3cf38fa1d26a9786dc9fbd6115e
EXPECTED_DIRECT_PARENT: 242857bb70cfd2f5bb18797210481d97e86f3577
REVIEW_MODE: FIXED_HEAD_READ_ONLY
VERDICT_OWNER: CLAUDE_INDEPENDENT_REVIEW
```

Codex는 독립 판정을 발행하지 않는다. 검토자는 fixed HEAD를 수정하지 않고 직접 재현한
근거로만 `PASS / PASS_WITH_FOLLOW_UP / REWORK`를 발행한다.

## 필수 검토 질문

1. 실제 `DdnRunner::run_update` delivery가 I1 typed provider core를 사용하며 standalone
   helper-only 증거가 아닌가?
2. route 0/2건에서 provider callback 0이고 exactly-one route에서만 resolve되는가?
3. 기본 public runtime registry가 empty이고 typed injection만 내부 검증 경로인가?
4. 동일 settled snapshot, diamond dedup, distinct fan-out, nested occurrence, execution
   instance identity가 실제 DdnRunner 15건에서 보존되는가?
5. provider failure/conflict에서 route state, candidate, outbox, effect, trace가 부분
   publish되지 않는가?
6. outer commit 뒤 provider publish/effect release 순서와 WAIT/RESUME, FIFO/no-reentry가
   보존되는가?
7. case 22의 tool actual run과 teul-cli static scan 표기가 실제 근거와 일치하는가?
8. 10축 mutation이 compile error를 RED로 세지 않고 실제 assertion RED를 검출하는가?
9. source A/B/tracked WASM raw bytes와 clean-detached/actual Edge 증거가 재현되는가?
10. public syntax, source ingress, CLI/env/WASM/UI control, stable wire/diagnostic 승격이 0인가?

## 직접 실행 진입점

```powershell
$env:DDN_W1C2_I2_CARGO_TARGET_DIR='<isolated-target>'
node tests/ddn_execution_concurrency_w1c2_ddnrunner_dispatch_runner.mjs

$env:DDN_W1C2_I2_CARGO_TARGET_DIR='<isolated-mutation-target>'
node tests/ddn_execution_concurrency_w1c2_i2_fault_injection_runner.mjs
```

Edge runner는 `DDN_PLAYWRIGHT_MODULE`, `DDN_W1C2_I2_EDGE_CLI`,
`DDN_W1C2_I2_EXPECTED_WASM_SHA256`를 모두 명시해야 fail-open하지 않는다.

## 비주장 경계

plain PASS라도 이번 검토 범위는 I2 internal DdnRunner dispatch connection뿐이다.
public ReactionProvider 한국어 이름·문법·source ingress·stable identity wire·stable
diagnostics, Workbench phase projection, rendezvous runtime, W1 전체, RD-207, activation,
Human PASS는 계속 OPEN이다.
