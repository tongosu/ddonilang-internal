# seamgrim_ui_v2_product_shell_v1

셈그림 UI V2 제품 셸의 L0/L1 최소 동작을 고정하는 검증 pack이다.

- 제품 경로: `solutions/seamgrim_ui_mvp/ui/index.html`
- browser runner: `tests/seamgrim_ui_v2_product_shell_runner.mjs`
- 범위: 배우기/실험실/만들기/배포 전역 셸, L0 lesson catalog, L1 DDN/WASM 실행, 실행 중 역할 토글의 구조적 부재, 데스크톱/모바일 레이아웃
- 제외: 배포 기능 완성, C1 만들기 전체 기능, 새 언어 문법, runtime `state_hash` 변경

이 pack의 golden은 실행 마커만 검증한다. 실제 제품 행동은 checker가 browser runner로 검증한다.
