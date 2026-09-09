# CLI JSON Escape Shared Authority W63 Handoff

## 결속

- persistent goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` (`ACTIVE`, 전체 blocker 아님)
- live authority: internal SSOT v25.47.0 / RD-001~543, public Language SPEC v0.6.0
- baseline: `9070d6b9e57772fd6f52e29fcd3021535e522f56`
- product fixed: `45641bb7d4834dbd1063798a025b273f2e47cdd6`
- product tree: `edbe1a27486a66a825ef812a7765b03ce362bac2`
- merge count: 0

## 사용자·제품 가치

AI/check/run/geoul/bogae playback의 JSON artifact 문자열 escaping이 `ddonirang-tool`의 한 공용 제품 권위를 소비한다. 기존 JSON byte 계약과 공개 schema·명령 spelling은 바꾸지 않았다.

- private escape implementation: 5 -> 0
- shared escape authority: 1
- product paths: `tool/src/state_trace_wire.rs`와 기존 teul consumer 5개
- new pack/runner/meta-test: 0/0/0
- docs/ssot, public SPEC, tracked WASM, visible UI diff: 0

## 검증

- shared state/trace/wire tests: 3/3 PASS
- bogae playback actual consumer test: 1/1 PASS
- `cargo check --manifest-path tools/teul-cli/Cargo.toml --offline`: PASS
- teul full regression: 1043 PASS / 동일 역사 9 FAIL / new drift 0
- risk mutation: quote escaping 제거 시 focused test RED 0/1; exact restore SHA-256 `6af84e3bfb8c6b20ce1bf31567f97c328a76f650e8b5fbda376ce0517c99afb`; restore GREEN 1/1; residue 0

## 검토·비주장

W58~W63을 하나의 coherent shared CLI authority milestone로 기존 rolling reviewer에 제출할 수 있다. 이 handoff 자체는 independent PASS, whole CLI convergence, teul physical retirement, P0~P6 closure, V1 readiness/release/activation 또는 Human PASS를 주장하지 않는다.

