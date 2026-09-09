# CLI migration plan

## 원칙

- 명령 이름보다 semantic authority를 먼저 수렴한다.
- 공개 표면과 internal research 표면을 분리한다.
- 기존 PASS는 새 binary identity에 자동 상속하지 않는다.
- 각 이행 slice는 원문 source, 진단, state hash, artifact parity를 검증한다.
- 하나의 실행 파일을 없애는 것은 마지막 단계다.

## DAG

| gate | 작업 | 선행 |
|---|---|---|
| C0 | 현행 binary·91 command registry 결속 | - |
| C1 | 공개 executable identity Owner 결정 | C0 |
| C2 | canon/preprocess를 shared library 권위로 추출 | C1 |
| C3 | 핵심 명령을 하나의 product frontdoor로 연결 | C2 |
| C4 | extended 명령 V1/internal/deferred 분류 | C1 |
| C5 | 선택된 extended 명령 이행 | C3, C4 |
| C6 | legacy alias·golden compatibility | C5 |
| C7 | CLI/WASM/Workbench 독립 parity 검토 | C6 |
| C8 | teul-cli binary retirement 여부 별도 결정 | C7 |

## 추천 첫 구현 vertical

```text
DDN-V1-CLI02-SHARED-CANON-PREPROCESS-AUTHORITY-W1
```

범위:

1. `tools/teul-cli/src/canon.rs`와 `tool/src/preprocess.rs`의 실제 호출·테스트 inventory
2. shared crate/module target 결정
3. 동작 변경 없는 move-only 또는 adapter-first 수렴
4. tool/teul/CLI/WASM source exact parity
5. fault injection으로 각 frontend의 독자 fallback 0 검증

비범위:

- 공개 binary 이름 변경
- teul-cli 삭제
- 63개 명령 migration
- SSOT/SPEC/UI 변경
- release/activation

Owner가 D1~D7을 아직 결정하지 않아도 C2의 상세 설계·반례 연구는 병행할 수 있다. 실제 path move와 public alias 착지는 exact implementation packet 승인 뒤 시작한다.
