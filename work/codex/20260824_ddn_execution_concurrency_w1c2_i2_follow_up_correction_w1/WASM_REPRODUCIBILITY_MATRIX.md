# DDN-W1C2-I2-FU01 WASM 재현성 행렬

## 판정

```text
F3_REPRODUCIBILITY_VERDICT: REPRODUCIBILITY_RESTORED
APPROVED_BUILD_CONTRACT: scripts/build_wasm_tool.ps1 + /ddn-src source remap
DIRECT_WASM_PACK_WITHOUT_SOURCE_REMAP: UNSUPPORTED_NONREPRODUCIBLE_ENVIRONMENT
```

동일 source와 lockfile을 승인된 remap 계약으로 빌드한 A/B/C/D와 tracked artifact가
모두 raw-byte identical하다. 직접 `wasm-pack`을 remap 없이 호출한 독립 검토 절차는
checkout 절대 경로를 WASM panic/debug 문자열에 남겨 서로 다른 worktree에서 다른
바이트를 만들었다. 공식 build entrypoint에는 이미 remap이 있었으며, 이번 교정은
freshness checker와 tracked manifest가 이 계약을 필수 조건으로 검사하도록 결속했다.

## 공통 환경

- rustc: `rustc 1.92.0 (ded5c06cf 2025-12-08)`
- cargo: `cargo 1.92.0 (344c4567c 2025-10-21)`
- wasm-pack: `0.14.0`
- Cargo.lock: `69defff8a2c3e955fb0983db1b1327a2ebabfa302b60b8bb52a704cecf6c586e`
- profile/target/features: `release` / `web` / `wasm`
- network: `CARGO_NET_OFFLINE=true`
- locale: `LANG=C.UTF-8`, `LC_ALL=C.UTF-8`, `LC_CTYPE=C.UTF-8`
- source remap destination: `/ddn-src`
- standalone `wasm-bindgen`/`wasm-opt`: PATH에 없음; wasm-pack의 봉인된 내부 도구 사용
- source file count/tree: `91` / `1ec8eb42c141ef87066cefca962dd7a6668ea2c5d3a19c3bca4afb6438509761`

## 행렬

| 행 | checkout/target 조건 | 실제 명령 계약 | bytes | SHA-256 | first differing byte |
|---|---|---|---:|---|---|
| A | clean-detached `556f63d5`, fresh target A | `RUSTFLAGS=--remap-path-prefix=<A>=/ddn-src`; `wasm-pack build . --target web --release --out-dir <A-out> --out-name ddonirang_tool -- --features wasm` | 5,509,880 | `27d18e40571e8987a3d0149840a231310e800b6895dcf469456958675017cbaa` | none |
| B | 별도 clean-detached `556f63d5`, fresh target B | `RUSTFLAGS=--remap-path-prefix=<B>=/ddn-src`; 동일 wasm-pack 명령 | 5,509,880 | `27d18e40571e8987a3d0149840a231310e800b6895dcf469456958675017cbaa` | none |
| C | A target을 `cargo clean --target-dir` 후 재빌드 | A와 동일 | 5,509,880 | `27d18e40571e8987a3d0149840a231310e800b6895dcf469456958675017cbaa` | none |
| D | 구현 worktree, fresh target D | `scripts/build_wasm_tool.ps1 -Profile release -Target web -CopyToUi:$false` | 5,509,880 | `27d18e40571e8987a3d0149840a231310e800b6895dcf469456958675017cbaa` | none |
| TRACKED | 공식 copy/manifest 절차 | `scripts/copy_wasm_tool_to_ui.ps1` + freshness manifest writer | 5,509,880 | `27d18e40571e8987a3d0149840a231310e800b6895dcf469456958675017cbaa` | none |

A/B/C/D/tracked의 unique hash 수는 `1`, differing byte 수는 `0`이다. 병렬 빌드,
timezone, locale, stale/incremental target은 이 승인 계약에서 결과를 바꾸지 않았다.

## tracked 갱신

- 교정 전: 5,508,839 bytes,
  `d91af594b3848b844f3f2df74217f0d7f6e562720b303bc936497df3fc91bdc8`
- 교정 후: 5,509,880 bytes,
  `27d18e40571e8987a3d0149840a231310e800b6895dcf469456958675017cbaa`
- old/new 최초 차이 offset: `1230`
- 이유: F1/F2의 제품 Rust 변경을 공식 절차로 반영
- JS binding, d.ts, package.json: diff `0`
- `python tests/run_ddn_cli_wasm_freshness_check.py`: `PASS`

## 비주장

이 결과는 public provider surface, stable wire, W1-C2 전체 닫힘, activation 또는
Human PASS의 근거가 아니다.
