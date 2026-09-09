# seamgrim_wasm_cli_runtime_parity_v1

`ddonirang-tool run-summary`와 WASM/셈그림 제품 경로가 같은 공통 runtime surface를 지나 같은 실행 결과를 내는지 확인하는 parity pack이다.

`state_hash`, 실행 봉투, canonical DDN, output log/row, 관찰 row, resource value JSON, diagnostics는 strict 비교한다. `domain_mismatch_reported`는 감사 증거일 뿐 이 pack의 성공 조건이 아니다.
