# W1-C2-I2 actual DdnRunner internal dispatch evidence

이 pack은 public ReactionProvider 문법이나 stable wire가 아니다. 모든 사례는 Rust 내부
typed registry를 주입하되 실제 DDN source를 `DdnProgram`으로 parse하고
`DdnRunner::run_update`로 실행한다. standalone `InternalTypedReactionRuntime::execute`
직접 호출은 이 pack의 통합 증거로 세지 않는다.

```text
DEFAULT_PUBLIC_RUNTIME_PROVIDER_REGISTRY_EMPTY
INTERNAL_TYPED_REGISTRY_INJECTION_EVIDENCE_ONLY
REACTION_PROVIDER_PUBLIC_SOURCE_REACHABILITY_0
```

재현:

```powershell
$env:DDN_W1C2_I2_CARGO_TARGET_DIR='I:\home\urihanl\ddn\codex\build\targets\w1c2-i2-ddnrunner'
node tests/ddn_execution_concurrency_w1c2_ddnrunner_dispatch_runner.mjs
```

runner는 crate 내부 runtime test module의 15개 exact compiled test ID와 15/15 실행,
실제 DdnRunner 연결
문자열, public source/CLI/env/WASM/UI ingress 0, case 22의 tool 실행과 teul-cli 정적
scan 분리를 fail-closed로 검사한다.

typed registry injection helper는 `pub(crate)`에 한정되며, 외부 integration crate에서
호출할 수 없다. 위 module은 실제 한국어 DDN과 `DdnRunner::run_update`를 그대로 실행하고
별도 runtime 의미 구현을 만들지 않는다.
