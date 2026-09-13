# Fixed64 중앙차분 checked 연산 handoff

## 고정 대상

- Product commit: `4dab82abfeb15cfdb77f42689a0163ea701c8862`
- Tree: `b483a341444bbb34be19a4f8957be9d436a7c0c1`
- Parent: `c4812cf706913c9149dc5d20fa99c97ca1b2699f`
- Product path: `tool/src/ddn_runtime.rs`

## 변경

`미분.중앙차분`의 point 이동, step/denominator, 차분, Richardson 보정과
오차 계산을 saturation 대신 shared `Fixed64::checked_*` 및 `try_div`로
연결했다. 산술 실패는 `EvalError::ArithmeticFault`를 통해
`E_RUNTIME_ARITH_OVERFLOW` 등 기존 typed diagnostic으로 fail-closed한다.

정상 `x^3` 중앙차분 결과는 유지하고, raw maximum point에서 step을 더하는
입력은 state/output/receipt publication 전에 typed overflow로 거부하는
focused assertion을 추가했다.

## 검증

- `cargo test -p ddonirang-tool --lib numeric_central_difference -- --nocapture` — PASS (2)
- `cargo check -p ddonirang-tool --lib --target wasm32-unknown-unknown --features wasm --offline` — PASS
- `git diff --check` — PASS

## Mutation M1

- mutation: `x_plus`와 `x_plus2`의 checked addition을 `saturating_add`로 임시 복귀
- RED: `numeric_central_difference_overflow_is_typed_and_publishes_nothing`가 성공 publication을 허용해 실패
- fixed/restore SHA-256: `5ea31b4cd4d146cb810fc036ee5d153c2f25d99262486683d502b4f1cb910580`
- fixed/restore Git blob: `f871911a110171b5749a9c8382ec5ab45baa252a`
- restore 후 focused GREEN: PASS

## 검토 요청과 비주장

CLAIM: 중앙차분 active caller의 checked Fixed64 migration과 typed overflow
failure atomicity가 target-bound로 구현되었다.

INDEPENDENT_REVIEW_REQUIRED: YES

이 기록은 Native/WASM 전체 Fixed64 boundary convergence, 모든 active caller,
release readiness, public support 또는 Human PASS를 주장하지 않는다.
