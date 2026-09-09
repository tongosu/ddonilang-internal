# DDN current public rejection parity successor 결과

## 고정점

- 과업: `DDN-LONG-RELINT-PRODUCT-01-G14-PARITY-SUCCESSOR`
- 시작 기준점: `fc09a1f4c857c97db20194173b19e17a3b83f9aa`
- 최초 제품·테스트 commit: `fcd3ed516221942ca97a96b1aa7a82d4a94f8e9e`
- 재현성 correction/fixed HEAD: `64f8556c92bdbad4ff4c796082cea2d7f07f382f`
- 분류: `CURRENT_PUBLIC_EXPECTED_REJECTION_PARITY`
- 제품 코드 변경: 0
- PC02 exact inverse: 보존

## 현재 계약

다음 historical case를 삭제하거나 현재 공개 성공으로 되돌리지 않았다.

1. `c09_boim_structured_view`
2. `c11_show_and_boim_split`
3. `c13_bogae_draw_madi_view_sugar`

세 case 모두 native CLI와 WASM이 같은 Rust 실행 owner
`ddonirang_tool::runtime_surface::run_summary_from_source`를 사용해 다음 결과로
수렴한다.

- normalized exit code: `1`
- outer diagnostic: `E_EXECUTION_PREPROCESS`
- semantic diagnostic: `E_BOIM_LEGACY_REMOVED`
- phase: `preprocess`
- source path: 각 contract input의 exact 상대 경로
- source span: `null`
- state mutation: `0`
- partial output/effect: `0 / 0`
- compatibility fallback: `0`

`DdnWasmVm.fromPreV25Source`는 현재 제품 표면에 존재하지 않으며 successor
runner도 이를 fail-closed로 검사한다.

## 구현된 증거 owner

- 계약: `pack/ddn_current_public_rejection_parity_v1/contract.detjson`
- 정방향 runner: `tests/ddn_current_public_rejection_parity_runner.mjs`
- 적대 runner: `tests/ddn_current_public_rejection_parity_mutation_runner.mjs`
- 재현 wrapper: `tests/run_ddn_cli_wasm_true_parity_successor_check.py`
- D7 aggregate: `tests/run_ddn_public_specific_conformance_check.py`

기존 historical fixed-target runner와 evidence는 수정하지 않았다. D7은 exact
11 leaf와 parity 3, durability 3을 유지하면서 true-parity leaf가 이 successor
wrapper를 소비하도록 갱신했다.

## 재현 결과

- tracked WASM: `3/3 PASS`
- source-built WASM A: `3/3 PASS`
- source-built WASM B: `3/3 PASS`
- A/B/tracked SHA-256:
  `14deea06dd4f6d1ea72ff1460e68f938c636fb3cd697afabed5296ef95a490b6`
- artifact bytes: `5,541,127`
- D7 files-only: exact leaf `11`, parity `3`, durability `3`
- WASM freshness: `PASS`
- view-only state-hash invariant: `PASS`

적대 검증은 잘못된 진단, 한쪽만 성공, case 누락, hidden compatibility 허용,
실패 후 state/effect 잔존을 각각 `GREEN -> RED -> exact restore -> GREEN`으로
검출했으며 residue는 `0`이다. clean-detached Windows checkout에서 CRLF 때문에
M4 anchor를 찾지 못한 하네스 결함은 입력 runner text만 LF로 정규화하고 원본
residue 비교는 raw bytes를 유지하는 correction으로 닫았다. 기대값과 제품 의미는
변경하지 않았다.

이 결과는 current rejection parity의 fixed evidence일 뿐 public conformance 전체
PASS, release readiness, activation 또는 Human PASS가 아니다.
