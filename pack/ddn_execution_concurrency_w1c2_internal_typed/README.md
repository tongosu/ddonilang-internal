# W1-C2-I1 internal typed product evidence

이 pack은 public DDN provider 문법 pack이 아니다. `expected.jsonl`의 사례는 제품 Rust
library API를 직접 실행하는 `INTERNAL_TYPED_PRODUCT_CASE`, 기존 public source 비후퇴를
확인하는 `PUBLIC_SOURCE_REGRESSION_CASE`, 아직 public ingress가 없는
`PRODUCT_UNSUPPORTED`로만 분류한다.

```text
REACTION_PROVIDER_PRODUCT_INTERNAL_ONLY
PUBLIC_PROVIDER_SOURCE_INGRESS_0
STABLE_WIRE_OPEN
PUBLIC_DIAGNOSTICS_OPEN
```

재현:

```powershell
$env:DDN_W1C2_CARGO_TARGET_DIR='I:\home\urihanl\ddn\codex\build\targets\w1c2-i1-evidence'
node tests/ddn_execution_concurrency_w1c2_internal_typed_runner.mjs
```

runner는 ledger의 exact compiled test ID를 `cargo test -- --list`와 대조한 뒤 전체
integration test binary를 실행한다. zero-match filter나 설명 hash를 제품 실행 근거로
세지 않는다. case 22는 `ddonirang-tool`의 실제 `DdnRunner` public-provider ingress 0을
검사한다. teul-cli는 case 22의 실행 주장이 아니라 shared-route/empty-registry 코드에
대한 별도 정적 scan 증거로만 기록한다.
