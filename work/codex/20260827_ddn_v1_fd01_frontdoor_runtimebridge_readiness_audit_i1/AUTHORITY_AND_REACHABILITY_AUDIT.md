# 권위·도달성 감사

## 판정 기준

코드가 존재한다는 사실과 사용자가 도달 가능한 제품 경로는 구분한다. 테스트에서만
호출되는 constructor는 공개 제품 ingress로 세지 않으며, Workbench가 Rust/WASM
결과를 소비해도 그 Rust 경로가 어떤 epoch parser를 사용하는지 별도로 추적한다.

## 실제 호출 경로

| 표면 | 현재 권위와 호출 | 현재 판정 |
|---|---|---|
| Rust V25 parser | `lang/src/lib.rs`의 `parse_v25_with_mode`, `SourceEpoch::V25` | 내부 구현 존재 |
| tool V25 constructor | `tool/src/ddn_runtime.rs`의 `from_v25_source` | 내부 테스트에서만 도달 |
| 공식 CLI `run` / `run-summary` | `tool/src/main.rs` → `runtime_surface` → pre-V25 경로 | V25 ingress 0 |
| WASM 기본 VM | `tool/src/wasm_api.rs`의 기본 constructor → pre-V25 경로 | V25 ingress 0 |
| source analysis | `DdnProgram::from_source_with_mode` | Rust 권위지만 pre-V25 parser |
| RuntimeBridge source analysis | `wasm_source_analysis_snapshot_json` export를 요구 | 연결됨, export 누락 시 fail-closed |
| Workbench source readiness | RuntimeBridge snapshot의 generation/source 일치 검사 | 연결됨, stale/unavailable fail-closed |
| native observation | WASM manifest를 contract로 검사 | 연결됨, JS semantic synthesis 0 |
| legacy JS manifest builder | runtime index에서 re-export되나 active 호출 없음 | housekeeping OPEN |
| T5F current grid | source는 수용되지만 native grid result 없음 | 제품 gap OPEN |

## fail-closed 경계

- source-analysis WASM export가 없으면 `E_SOURCE_ANALYSIS_WASM_REQUIRED`로 실패한다.
- Workbench는 요청 generation이나 source가 맞지 않는 분석 결과를 현재 결과로 쓰지 않는다.
- observation channel은 native manifest가 없거나 틀리면 JS가 성공 결과를 만들어내지 않는다.
- PC01 V25 원문을 현 공식 CLI에 넣으면 `E_SHARED_CANONICAL`로 실패한다. 이것은 V25
  지원 증거가 아니라 현재 제품 ingress가 연결되지 않았다는 증거다.

## 결론

FD01의 문제는 RuntimeBridge 전체가 가짜라는 것이 아니다. Rust/WASM → RuntimeBridge
→ Workbench 전달 골격은 이미 쓸 수 있다. 미수렴 지점은 **입력 원문의 epoch를 누가
명시적으로 선택하고, 그 선택이 source analysis와 execution 양쪽에 같은 identity로
전달되는가**이다.

따라서 다음 구현은 JS parser나 content sniffing을 추가하지 않고 Rust의 typed epoch
선택을 공통 권위로 만들고, source analysis와 execution이 동일한 선택을 쓰도록 해야 한다.

