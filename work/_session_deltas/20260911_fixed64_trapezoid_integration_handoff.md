# Fixed64 사다리꼴 적분 checked 연산 handoff

## 고정 대상

- Product commit: `b7b0586f79cee41160470b7b4d1fc512891af926`
- Tree: `23b0943249d1cff12564a655facafa2ad03f9bd4`
- Parent: `efd0f1b882ed822b667518541dd09e5526c660da`
- Product path: `tool/src/ddn_runtime.rs`

## 변경과 행동

`적분.사다리꼴` 및 `numeric_trapezoid_integral`의 interval, sample point,
weighted sum, approximation, Richardson correction과 sign inversion을 shared
checked Fixed64 operations로 전환했다. 범위를 넘는 integral interval은
`E_RUNTIME_ARITH_OVERFLOW`로 fail-closed하며 product publication 전에 끝난다.

지원되는 `x^2` integral result는 기존 raw result `1431655765` 및 error
`44739243`을 보존한다.

## 검증

- `cargo test -p ddonirang-tool --lib numeric_trapezoid_integral -- --nocapture` — PASS (2)
- `cargo check -p ddonirang-tool --lib --target wasm32-unknown-unknown --features wasm --offline` — PASS
- `git diff --check` — PASS

## Mutation M1

- mutation: outer/helper interval과 sample point 계산을 saturation으로 임시 복귀
- RED: extreme interval focused case가 success로 진행하여 `trapezoid interval overflow must reject before publication` assertion 실패
- fixed/restore SHA-256: `dbdf76707cf8308dfe07c3b91db187860f4ea395ad04d6ddcc6e7c30226ca0fe`
- fixed/restore Git blob: `39a17679bc8c6237a62264ff5faec59440b9eb1f`
- restore 후 focused GREEN: PASS

## 검토 요청과 비주장

CLAIM: 사다리꼴 적분 active caller의 checked Fixed64 migration 및 typed
overflow fail-closed가 target-bound로 구현되었다.

INDEPENDENT_REVIEW_REQUIRED: YES

이 기록은 모든 Fixed64 active caller, Native/WASM 전체 boundary convergence,
release readiness, public support 또는 Human PASS를 주장하지 않는다.
