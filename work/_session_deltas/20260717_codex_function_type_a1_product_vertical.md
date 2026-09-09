# 2026-07-17 Codex 함수 타입 A1 제품 세로줄

## 목적

v24.15.1 docs-first current가 승인한 함수 타입 정본 화살표 A1 `-->`를 테스트 전용 lowering이
아닌 공통 Rust 언어 frontdoor, CLI, 제품 WASM 경로에 착지한다.

## 결정과 경계

- `-->`는 타입 위치 전용, 최장 일치, 비결합 정본 화살표다.
- `->`는 함수 타입 입력 별칭이 아니며 기존 오른쪽 대입 입력 역할을 유지한다.
- 이 세로줄은 함수 타입 구조와 정본/진단 parity만 닫는다.
- 일반 함수값의 호출·저장·반환·capture·효과·직렬화와 K0~K7은 범위 밖이다.
- `docs/ssot/**`는 읽기만 했고 변경하지 않았다.

## 구현

- `lang`: `TypeArrow`, `TypeRef::Function`, 영항/단항/다항/고차 parser, 정본화, frontdoor label,
  전용 음수 진단과 6개 집중 테스트를 추가했다.
- `tool`: 함수 타입 표시와 schema 순회를 추가하고, 아직 함수값이 아닌 runtime value check에는
  명시적 mismatch 경계를 유지했다.
- `pack/lang_function_type_a1_v1`: 양수 1건과 음수 3건의 공통 원문 parity 계약을 추가했다.
- 소스 커밋 `139457e`, 깨끗한 clone 산출물 커밋 `6e5aa85`로 분리했다.

## 검증 결과

- `cargo test -p ddonirang-lang`: 257/257 PASS
- `cargo test -p ddonirang-tool --lib`: 304/304 PASS
- `cargo check --manifest-path tools/teul-cli/Cargo.toml`: PASS
- 깨끗한 `139457e` clone에서 WASM release build: PASS
- 같은 clone에서 freshness: PASS
- 같은 clone에서 `lang_function_type_a1_v1` CLI/WASM parity: 4/4 PASS
  - 정본 DDN과 `state_hash` strict equality
  - 세 음수 진단 코드 strict equality

## 실패·이슈 기록

- 첫 양수 pack은 함수 선언만 있어 공통 실행기가 `매마디`를 찾지 못했다. 최소 `매마디:움직씨`
  진입점을 넣어 함수 타입 선언이 실행 상태를 바꾸지 않는 조건으로 검증했다.
- 첫 clean archive 추출은 PowerShell binary pipe가 tar를 손상해 폐기하지 않고 외부 `out/`에 남겼다.
  이후 ZIP과 실제 local clone으로 재검증했다.
- clean clone에는 비추적 방언 TSV가 없어 기존 `include_str!` 빌드가 실패했다. 현재 작업공간의 동일
  TSV bytes(SHA-256 `9bed0c54de463dab2ee05bd90fd5da0adf8527de547b5aaed09e8982c2db06d6`)를
  clone에만 보충해 검증했다. 제품 재현성 문제로 후속 분리해야 한다.

## 다음 작업

1. K0 parse/canon-only 세로줄을 A1과 겹치지 않게 시작한다.
2. 비추적 방언 TSV 의존을 추적 입력 또는 생성 관문으로 닫는다.
3. 함수값 의미는 별도 승인·설계·runtime vertical 전에는 A1 완료 주장에 포함하지 않는다.
